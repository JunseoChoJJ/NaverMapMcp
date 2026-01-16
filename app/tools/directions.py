from typing import Any, Mapping

from mcp.server.fastmcp import FastMCP

from app.services.naver_map_service import NaverMapService


def register_directions_tool(mcp: FastMCP) -> None:
    service = NaverMapService()

    @mcp.tool(
        name="naver_directions",
        description=(
            "Get driving directions using Naver Map Directions API. "
            "Start/goal should be "
            "formatted as 'lng,lat' (e.g., 127.1054328,37.3595963)."
        ),
    )
    async def directions(
        start: str,
        goal: str,
        option: str | None = None,
        waypoints: str | None = None,
    ) -> Mapping[str, Any]:
        return await service.directions(
            start=start,
            goal=goal,
            option=option,
            waypoints=waypoints,
        )
