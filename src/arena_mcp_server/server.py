"""MCP server for Arena PLM API."""

import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .arena_client import ArenaClient


server = Server("arena-mcp-server")
client: ArenaClient | None = None


def get_client() -> ArenaClient:
    """Get or create authenticated Arena client."""
    global client

    if client is None or not client.is_authenticated:
        client = ArenaClient()
        email = os.environ.get("ARENA_EMAIL")
        password = os.environ.get("ARENA_PASSWORD")
        workspace_id = os.environ.get("ARENA_WORKSPACE_ID")

        if not email or not password:
            raise RuntimeError(
                "ARENA_EMAIL and ARENA_PASSWORD environment variables required"
            )

        client.login(
            email=email,
            password=password,
            workspace_id=int(workspace_id) if workspace_id else None,
        )

    return client


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_items",
            description="Search for items in Arena PLM. Returns matching items with their details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Filter by item name (partial match)",
                    },
                    "number": {
                        "type": "string",
                        "description": "Filter by item number (partial match)",
                    },
                    "description": {
                        "type": "string",
                        "description": "Filter by description (partial match)",
                    },
                    "category_guid": {
                        "type": "string",
                        "description": "Filter by category GUID",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results to return (default 20, max 400)",
                        "default": 20,
                    },
                },
                "additionalProperties": False,
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "search_items":
        try:
            arena = get_client()
            results = arena.search_items(
                name=arguments.get("name"),
                number=arguments.get("number"),
                description=arguments.get("description"),
                category_guid=arguments.get("category_guid"),
                limit=arguments.get("limit", 20),
            )

            count = results.get("count", 0)
            items = results.get("results", [])

            if count == 0:
                return [TextContent(type="text", text="No items found.")]

            lines = [f"Found {count} item(s):\n"]
            for item in items:
                lines.append(
                    f"- {item.get('number', 'N/A')}: {item.get('name', 'N/A')}"
                )
                if item.get("revisionNumber"):
                    lines[-1] += f" (Rev {item['revisionNumber']})"
                if item.get("lifecyclePhase", {}).get("name"):
                    lines[-1] += f" [{item['lifecyclePhase']['name']}]"

            return [TextContent(type="text", text="\n".join(lines))]

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


def main() -> None:
    """Run the MCP server."""
    import asyncio

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
