import os
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin
import time 

import msal  
import requests
from requests import HTTPError

JSON = Union[Dict[str, Any], List[Any]]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataverseClient:
    """
    A lightweight Dataverse REST client using MSAL device-flow,
    with token‐cache persistence to disk.

    Uses the public Microsoft client ID by default (Azure CLI / PowerShell).
    """

    DEFAULT_CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
    CACHE_FILE = "msal_cache.bin"

    def __init__(
        self,
        dataverse_url: str,
        client_id: Optional[str] = None,
        authority: str = "https://login.microsoftonline.com/common",
        cache_path: Optional[str] = None,
    ) -> None:
        self.dataverse_url = dataverse_url.rstrip("/")
        self.client_id = client_id or self.DEFAULT_CLIENT_ID
        self.authority = authority
        self.scope = [f"{self.dataverse_url}/.default"]
        self._token: Optional[str] = None
        self._token_type: Optional[str] = None
        self._expires_at: Optional[float] = None  

        # Load token cache from file
        cache_file = cache_path or self.CACHE_FILE
        self.token_cache = msal.SerializableTokenCache()
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    data = f.read()
                if data:
                    self.token_cache.deserialize(data)
            except Exception as e:
                logger.warning(f"Failed to load token cache: {e}")
        self._cache_file = cache_file

        # Build MSAL app
        self.app = msal.PublicClientApplication(
            client_id=self.client_id,
            authority=self.authority,
            token_cache=self.token_cache,
        )

    def _save_cache(self) -> None:
        if self.token_cache.has_state_changed:
            try:
                with open(self._cache_file, "w") as f:
                    f.write(self.token_cache.serialize())
            except Exception as e:
                logger.error(f"Failed to save token cache: {e}")

    def _ensure_authenticated(self) -> None:
        if not self._token:
            self.authenticate()

    def _is_token_valid(self) -> bool:
        return bool(self._token is not None and self._expires_at and time.time() < self._expires_at - 60)  # 60s buffer

    def _ensure_authenticated(self) -> None:
        if not self._is_token_valid():
            self.authenticate()
            
    def authenticate(self) -> None:
        """
        Attempt silent authentication, falling back to device-code flow.
        Tracks token expiration for validation.
        """
        result: Optional[dict[str, Any]] = None

        try:
            accounts = self.app.get_accounts()
            if accounts:
                result = self.app.acquire_token_silent(self.scope, account=accounts[0])

            if not result:
                flow = self.app.initiate_device_flow(scopes=self.scope)
                if "user_code" not in flow:
                    raise AuthenticationError(f"Failed to initiate device flow: {flow}")
                logger.info(flow["message"])
                result = self.app.acquire_token_by_device_flow(flow)

        except Exception as e:
            raise AuthenticationError(f"Authentication error: {e}") from e

        if not result or "access_token" not in result:
            raise AuthenticationError(f"Authentication failed: {result}")

        if result.get("token_type", "").lower() != "bearer":
            raise AuthenticationError("Invalid token type received")

        self._token = result["access_token"]
        self._token_type = result.get("token_type")
        self._expires_at = time.time() + result.get("expires_in", 3600)
        self._save_cache()


    def _headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        self._ensure_authenticated()
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept":        "application/json",
            "OData-Version": "4.0",
        }
        if extra:
            headers.update(extra)
        return headers

    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        try:
            resp = requests.request(method, url, **kwargs)
            resp.raise_for_status()
            return resp
        except HTTPError as e:
            logger.error(f"HTTP {e.response.status_code} error for {url}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request error for {url}: {e}")
            raise

    def query(self, entity_set: str, odata: str = "") -> Dict[str, Any]:
        url = f"{self.dataverse_url}/api/data/v9.2/{entity_set}?{odata}"
        resp = self._request("GET", url, headers=self._headers())
        return resp.json()

    def create(self, entity_set: str, body: Dict[str, Any]) -> str:
        url = urljoin(self.dataverse_url, f"/api/data/v9.2/{entity_set}")
        resp = self._request(
            "POST", url,
            headers=self._headers({"Content-Type": "application/json"}),
            json=body
        )
        eid = resp.headers.get("OData-EntityId")
        if not eid:
            raise RuntimeError("Missing OData-EntityId in response")
        return eid.split("(")[-1].rstrip(")")

    def delete_record(self, entity_set: str, record_id: str) -> bool:
        url = urljoin(self.dataverse_url, f"/api/data/v9.2/{entity_set}({record_id})")
        self._request("DELETE", url, headers=self._headers({"If-Match": "*"}))
        return True

    def patch_record(self, entity_set: str, record_id: str, body: Dict[str, Any]) -> bool:
        url = urljoin(self.dataverse_url, f"/api/data/v9.2/{entity_set}({record_id})")
        self._request(
            "PATCH", url,
            headers=self._headers({
                "Content-Type": "application/json",
                "If-Match":      "*",
            }),
            json=body
        )
        return True

    def send_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        json_body: Optional[Any] = None,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        Generic HTTP request to any endpoint.
        """
        self._ensure_authenticated()
        url = endpoint if endpoint.lower().startswith("http") else f"{self.dataverse_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self._request(
            method.upper(), url,
            headers=self._headers(extra_headers),
            params=params,
            data=data,
            json=json_body,
        )
    
class AuthenticationError(Exception):
    pass