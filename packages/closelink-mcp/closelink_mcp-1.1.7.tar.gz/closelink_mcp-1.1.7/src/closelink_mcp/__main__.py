import inspect
import json
import asyncio
from functools import wraps
from importlib import resources

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.openapi import RouteMap, RouteType, Tool, FastMCPOpenAPI
from fastmcp.utilities.logging import get_logger

from dotenv import load_dotenv
import os

# by default looks for a .env in the cwd or the same folder as this script
load_dotenv()

logger = get_logger(__name__)


def truncate_after_special_char(s: str) -> str:
    for i, ch in enumerate(s):
        if not ch.isalnum():
            return s[:i]
    return s  # if no non-alnum found


async def get_updated_tools(mcp: FastMCPOpenAPI):
    all_tools = await mcp.get_tools()
    updated_tools = {}

    for name, tool in all_tools.items():
        original_fn = tool.fn

        # build a wrapper that re-raises everything as ToolError
        if inspect.iscoroutinefunction(original_fn):
            @wraps(original_fn)
            async def wrapped_fn(__orig=original_fn):
                try:
                    logger.info("Calling tool (async) %s", name)
                    return await __orig()
                except Exception as e:
                    # forward full message
                    raise ToolError(str(e))
        else:
            @wraps(original_fn)
            def wrapped_fn(__orig=original_fn):
                try:
                    logger.info("Calling tool (sync) %s", name)
                    return __orig()
                except Exception as e:
                    raise ToolError(str(e))

        # re-build the tool using our wrapped function
        updated_tools[name] = Tool.from_function(
            fn=lambda: wrapped_fn(),
            name=tool.name,
            description=tool.description,
            tags=tool.tags,
            annotations=tool.annotations,
            serializer=lambda value: tool.serializer(value),
        )

    return updated_tools


async def prepare(mcp: FastMCPOpenAPI):
    logger.info("Preparing tools...")
    mcp.tools = await get_updated_tools(mcp)
    logger.info("Finished preparing tools...")


def main():
    #  Create a client for your API
    api_client = httpx.AsyncClient(base_url=os.getenv("CLOSELINK_API_BASE_URL"),
                                   headers={"apiKey": os.getenv("CLOSELINK_API_KEY")})

    # Load your OpenAPI spec as object
    with resources.open_text("closelink_mcp.resources", "cl-openapi.json", encoding="utf-8") as f:
        spec = json.load(f)

    # Replace all operationIds with the summary in camel case
    for path, path_item in spec["paths"].items():
        for method, operation in path_item.items():
            summary_in_title_case = ''.join(x for x in operation["summary"].title() if not x.isspace())
            sanitized = truncate_after_special_char(summary_in_title_case)
            operation["operationId"] = sanitized

    # Custom mapping rules
    custom_maps = [
        # Force all endpoints to be Tools (for now)
        RouteMap(methods=["GET"],
                 pattern=r".*",
                 route_type=RouteType.TOOL)
    ]

    # Create an MCP server from your OpenAPI spec
    mcp = FastMCP.from_openapi(openapi_spec=spec, client=api_client, name="Closelink MCP 1.1.7", route_maps=custom_maps)
    # asyncio.run(prepare(mcp))
    logger.info("Calling mcp.run()")
    mcp.run()


if __name__ == "__main__":
    logger.info("Calling __main__")
    main()
