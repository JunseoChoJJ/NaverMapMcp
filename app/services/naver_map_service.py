import json
import os
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class NaverMapCredentials:
    # Naver Cloud Platform (Geocode, Directions)
    ncp_client_id: str
    ncp_client_secret: str
    # Naver Developers (Places/Local Search)
    dev_client_id: str
    dev_client_secret: str


class NaverMapService:
    def __init__(self, credentials: NaverMapCredentials | None = None) -> None:
        self._credentials = credentials or self._load_credentials()

    def geocode(
        self,
        query: str,
        coordinate: str | None = None,
        page: int | None = None,
        count: int | None = None,
        filter: str | None = None,
    ) -> Mapping[str, Any]:
        params: dict[str, str] = {"query": query}
        if coordinate:
            params["coordinate"] = coordinate
        if page is not None:
            params["page"] = str(page)
        if count is not None:
            params["count"] = str(count)
        if filter:
            params["filter"] = filter
        return self._request_ncp(
            "https://maps.apigw.ntruss.com/map-geocode/v2/geocode",
            params,
        )

    def directions(
        self,
        start: str,
        goal: str,
        option: str | None = None,
        waypoints: str | None = None,
    ) -> Mapping[str, Any]:
        params: dict[str, str] = {"start": start, "goal": goal}
        if option:
            params["option"] = option
        if waypoints:
            params["waypoints"] = waypoints
        return self._request_ncp(
            "https://maps.apigw.ntruss.com/map-direction/v1/driving",
            params,
        )

    def places(self, query: str, display: int | None = None) -> Mapping[str, Any]:
        params: dict[str, str] = {"query": query}
        if display is not None:
            params["display"] = str(display)
        return self._request_dev(
            "https://openapi.naver.com/v1/search/local.json",
            params,
        )

    def _request_ncp(self, url: str, params: Mapping[str, str]) -> Mapping[str, Any]:
        """Naver Cloud Platform API 요청 (Geocode, Directions)"""
        if not self._credentials.ncp_client_id or not self._credentials.ncp_client_secret:
            raise ValueError("NCP_CLIENT_ID and NCP_CLIENT_SECRET are required")
        
        query = urlencode(params)
        request = Request(f"{url}?{query}")
        request.add_header("X-NCP-APIGW-API-KEY-ID", self._credentials.ncp_client_id)
        request.add_header("X-NCP-APIGW-API-KEY", self._credentials.ncp_client_secret)
        
        with urlopen(request) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload)

    def _request_dev(self, url: str, params: Mapping[str, str]) -> Mapping[str, Any]:
        """Naver Developers API 요청 (Places/Local Search)"""
        if not self._credentials.dev_client_id or not self._credentials.dev_client_secret:
            raise ValueError("DEV_CLIENT_ID and DEV_CLIENT_SECRET are required")
        
        query = urlencode(params)
        request = Request(f"{url}?{query}")
        request.add_header("X-Naver-Client-Id", self._credentials.dev_client_id)
        request.add_header("X-Naver-Client-Secret", self._credentials.dev_client_secret)
        
        with urlopen(request) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload)

    @staticmethod
    def _load_credentials() -> NaverMapCredentials:
        return NaverMapCredentials(
            ncp_client_id=os.getenv("NAVER_NCP_CLIENT_ID", ""),
            ncp_client_secret=os.getenv("NAVER_NCP_CLIENT_SECRET", ""),
            dev_client_id=os.getenv("NAVER_DEV_CLIENT_ID", ""),
            dev_client_secret=os.getenv("NAVER_DEV_CLIENT_SECRET", ""),
        )