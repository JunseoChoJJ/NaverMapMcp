from typing import Any, Mapping

from mcp.server.fastmcp import FastMCP

from app.services.naver_map_service import NaverMapService


def register_geocode_tool(mcp: FastMCP) -> None:
    service = NaverMapService()

    @mcp.tool(
        name="naver_geocode",
        description=(
            "Geocode an address or place name using the Naver Map Geocode API. "
            "Provide the query string, and optionally a center coordinate "
            "('lng,lat'), page, count, or filter."
        ),
    )
    async def geocode(
        query: str,
        coordinate: str | None = None,
        page: int | None = None,
        count: int | None = None,
        filter: str | None = None,
    ) -> Mapping[str, Any]:
        return await service.geocode(
            query=query,
            coordinate=coordinate,
            page=page,
            count=count,
            filter=filter,
        )
