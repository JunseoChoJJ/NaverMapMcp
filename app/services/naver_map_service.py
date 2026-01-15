import json
import os
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class NaverMapCredentials:
    client_id: str
    client_secret: str


class NaverMapService:
    def __init__(self, credentials: NaverMapCredentials | None = None) -> None:
        self._credentials = credentials or self._load_credentials()

    def geocode(self, query: str, coordinate_system: str | None = None) -> Mapping[str, Any]:
        params: dict[str, str] = {"query": query}
        if coordinate_system:
            params["coordinate"] = coordinate_system
        return self._request(
            "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode",
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
        return self._request(
            "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving",
            params,
        )

    def places(self, query: str, display: int | None = None) -> Mapping[str, Any]:
        params: dict[str, str] = {"query": query}
        if display is not None:
            params["display"] = str(display)
        return self._request("https://openapi.naver.com/v1/search/local.json", params)

    def _request(self, url: str, params: Mapping[str, str]) -> Mapping[str, Any]:
        if not self._credentials.client_id or not self._credentials.client_secret:
            raise ValueError("NAVER_MAP_CLIENT_ID and NAVER_MAP_CLIENT_SECRET are required")
        query = urlencode(params)
        request = Request(f"{url}?{query}")
        request.add_header("X-NCP-APIGW-API-KEY-ID", self._credentials.client_id)
        request.add_header("X-NCP-APIGW-API-KEY", self._credentials.client_secret)
        request.add_header("X-Naver-Client-Id", self._credentials.client_id)
        request.add_header("X-Naver-Client-Secret", self._credentials.client_secret)
        with urlopen(request) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload)

    @staticmethod
    def _load_credentials() -> NaverMapCredentials:
        return NaverMapCredentials(
            client_id=os.getenv("NAVER_MAP_CLIENT_ID", ""),
            client_secret=os.getenv("NAVER_MAP_CLIENT_SECRET", ""),
        )
