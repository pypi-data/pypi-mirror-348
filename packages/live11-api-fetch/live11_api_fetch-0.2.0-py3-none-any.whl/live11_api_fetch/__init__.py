from .server import serve


def main():
    """MCP server to query a specific API, e.g., Live 11 API documentation."""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="MCP server to query a specific API (e.g., Live 11 API documentation) with query_text and top_k."
    )
    parser.add_argument(
        "--custom-api-url",
        type=str,
        help="Custom API URL to use as the default for requests. Overrides the hardcoded default.",
    )
    parser.add_argument("--proxy-url", type=str, help="Proxy URL to use for requests.")

    args = parser.parse_args()
    # Pass only the relevant arguments to the serve function
    asyncio.run(serve(custom_api_url=args.custom_api_url, proxy_url=args.proxy_url))


if __name__ == "__main__":
    main()
