from typing import Annotated

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import (
    INTERNAL_ERROR,
    INVALID_PARAMS,
    ErrorData,
    TextContent,
    Tool,
)
from pydantic import BaseModel, Field

# Define the default hardcoded API URL base.
# IMPORTANT: Replace "YOUR_CLOUD_RUN_SERVICE_URL_HERE" with your actual Cloud Run service URL.
DEFAULT_CLOUD_RUN_SERVICE_URL = (
    "https://api-doc-search-remote-svc-1053127428938.us-central1.run.app"
)
DEFAULT_API_ENDPOINT = f"{DEFAULT_CLOUD_RUN_SERVICE_URL}/query"


class QueryApiArgs(BaseModel):
    """Parameters for querying the API."""

    query_text: Annotated[str, Field(description="The query text to send to the API.")]
    top_k: Annotated[
        int,
        Field(
            default=3,
            description="The number of top results to return.",
            gt=0,
        ),
    ]
    api_url: Annotated[
        str | None,
        Field(
            default=None,
            description="Optional custom API URL to use for this request. Overrides server default.",
        ),
    ] = None


async def query_external_api(
    query_text: str, top_k: int, target_api_url: str, proxy_url: str | None = None
) -> str:
    """
    Call the external API with query_text and top_k.
    Returns the API response text.
    """
    from httpx import AsyncClient, HTTPError

    payload = {"query_text": query_text, "top_k": top_k}
    headers = {"Content-Type": "application/json"}

    async with AsyncClient(proxies=proxy_url) as client:
        try:
            response = await client.post(
                target_api_url,
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
        except HTTPError as e:
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Failed to query API at {target_api_url}: {e!r}",
                )
            )

        return response.text


async def serve(
    custom_api_url: str
    | None = None,  # Added to allow overriding default API URL at startup
    proxy_url: str | None = None,
) -> None:
    """Run the MCP server for querying a specific API.

    Args:
        custom_api_url: Optional custom API URL to use as the default for requests.
        proxy_url: Optional proxy URL to use for requests
    """
    server = Server("live11-api-fetch")

    # Determine the API endpoint to use: startup override or default
    effective_api_endpoint = custom_api_url or DEFAULT_API_ENDPOINT

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="query_service",
                description="Queries a specific API with the given text and top_k parameter. Can optionally specify a custom api_url.",
                inputSchema=QueryApiArgs.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name != "query_service":
            raise McpError(
                ErrorData(code=INVALID_PARAMS, message=f"Unknown tool: {name}")
            )
        try:
            args = QueryApiArgs(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        # Determine the final API URL:
        # 1. From tool arguments (highest precedence)
        # 2. From server startup custom URL
        # 3. Default
        final_api_url = args.api_url or effective_api_endpoint

        if not final_api_url.startswith("http"):
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"The API URL is not configured correctly or is not a valid HTTP/HTTPS URL. Please set it in the server code, at startup, or in the tool call. Current endpoint: {final_api_url}",
                )
            )

        api_response_text = await query_external_api(
            args.query_text,
            args.top_k,
            target_api_url=final_api_url,
            proxy_url=proxy_url,
        )

        return [
            TextContent(
                type="text",
                text=f"API Response from {final_api_url}:\\n{api_response_text}",
            )
        ]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)


# Removed functions:
# - extract_content_from_html
# - get_robots_txt_url
# - check_may_autonomously_fetch_url
# - fetch_url

# Imports removed:
# - urllib.parse (urlparse, urlunparse)
# - markdownify
# - readabilipy.simple_json
# - protego
# - mcp.types: Prompt, PromptArgument, GetPromptResult, PromptMessage (if not used elsewhere implicitly by Server)
# - pydantic: AnyUrl (if QueryApiArgs doesn't need it)

# Kept httpx (needs to be a dependency)
# Kept pydantic (BaseModel, Field)
# Kept mcp related imports for Server, ErrorData, TextContent, Tool, etc.
