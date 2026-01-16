import os
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlencode

import httpx


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

    async def geocode(
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
        return await self._request_ncp(
            "https://maps.apigw.ntruss.com/map-geocode/v2/geocode",
            params,
        )

    async def directions(
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
        return await self._request_ncp(
            "https://maps.apigw.ntruss.com/map-direction/v1/driving",
            params,
        )

    async def places(self, query: str, display: int | None = None) -> Mapping[str, Any]:
        params: dict[str, str] = {"query": query}
        if display is not None:
            params["display"] = str(display)
        return await self._request_dev(
            "https://openapi.naver.com/v1/search/local.json",
            params,
        )

    async def _request_ncp(self, url: str, params: Mapping[str, str]) -> Mapping[str, Any]:
        """Naver Cloud Platform API 요청 (Geocode, Directions)"""
        if not self._credentials.ncp_client_id or not self._credentials.ncp_client_secret:
            raise ValueError("NCP_CLIENT_ID and NCP_CLIENT_SECRET are required")
        
        headers = {
            "X-NCP-APIGW-API-KEY-ID": self._credentials.ncp_client_id,
            "X-NCP-APIGW-API-KEY": self._credentials.ncp_client_secret,
        }
        query = urlencode(params)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}?{query}", headers=headers)
            response.raise_for_status()
            return response.json()

    async def _request_dev(self, url: str, params: Mapping[str, str]) -> Mapping[str, Any]:
        """Naver Developers API 요청 (Places/Local Search)"""
        if not self._credentials.dev_client_id or not self._credentials.dev_client_secret:
            raise ValueError("DEV_CLIENT_ID and DEV_CLIENT_SECRET are required")
        
        headers = {
            "X-Naver-Client-Id": self._credentials.dev_client_id,
            "X-Naver-Client-Secret": self._credentials.dev_client_secret,
        }
        query = urlencode(params)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{url}?{query}", headers=headers)
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _load_credentials() -> NaverMapCredentials:
        return NaverMapCredentials(
            ncp_client_id=os.getenv("NAVER_NCP_CLIENT_ID", ""),
            ncp_client_secret=os.getenv("NAVER_NCP_CLIENT_SECRET", ""),
            dev_client_id=os.getenv("NAVER_DEV_CLIENT_ID", ""),
            dev_client_secret=os.getenv("NAVER_DEV_CLIENT_SECRET", ""),
        )
