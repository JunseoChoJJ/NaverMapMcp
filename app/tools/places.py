from typing import Any, Mapping

from mcp.server.fastmcp import FastMCP

from app.services.naver_map_service import NaverMapService


def register_places_tool(mcp: FastMCP) -> None:
    service = NaverMapService()

    @mcp.tool(
        name="naver_places",
        description=(
            "Search for local places using the Naver Local Search API. "
            "Provide a query string and optional display count (max 100)."
        ),
    )
    def places(query: str, display: int | None = None) -> Mapping[str, Any]:
        return service.places(query=query, display=display)
