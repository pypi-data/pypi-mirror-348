import sys

from fastmcp import FastMCP
from loguru import logger

from .config import settings
from .vais import VaisError, call_vais

logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL)


mcp = FastMCP(
    name="Vertex AI Search MCP",
    description="Vertex AI Search MCP server",
    log_level=settings.LOG_LEVEL,
)


@mcp.tool()
async def search(
    search_query: str,
) -> dict:
    logger.info(f"Received search request with query: '{search_query}'")
    if not search_query:
        logger.warning("Search query is empty.")
        return {"response": "No search query provided"}

    try:
        response_data = call_vais(
            search_query=search_query,
            google_cloud_project_id=settings.GOOGLE_CLOUD_PROJECT_ID,
            impersonate_service_account=settings.IMPERSONATE_SERVICE_ACCOUNT,
            vais_engine_id=settings.VAIS_ENGINE_ID,
            vais_location=settings.VAIS_LOCATION,
            page_size=settings.PAGE_SIZE,
            max_extractive_segment_count=settings.MAX_EXTRACTIVE_SEGMENT_COUNT,
        )
        logger.info(f"Search request successful, returning {len(response_data)} items.")
        return {"response": response_data}
    except VaisError as e:
        logger.error(f"Error processing search request: {e}")
        return {"error": str(e), "status_code": 500}


def main():
    logger.info("Starting FastMCP server.")
    mcp.run()


if __name__ == "__main__":
    main()
