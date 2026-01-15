from typing import Any, Mapping

from mcp.server.fastmcp import FastMCP

from app.services.naver_map_service import NaverMapService


def register_geocode_tool(mcp: FastMCP) -> None:
    service = NaverMapService()

    @mcp.tool(
        name="naver_geocode",
        description=(
            "Geocode an address or place name using the Naver Map Geocode API. "
            "Provide the query string, and optionally a coordinate system (e.g., epsg:4326)."
        ),
    )
    def geocode(query: str, coordinate_system: str | None = None) -> Mapping[str, Any]:
        return service.geocode(query=query, coordinate_system=coordinate_system)
