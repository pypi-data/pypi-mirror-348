from logging import DEBUG, getLogger

from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import GetPromptResult, Prompt

from .get_prompt import get_prompt as handle_get_prompt
from .list_prompts import list_prompts as handle_list_prompts

logger = getLogger("simple-prompts-mcp")
logger.setLevel(DEBUG)
server = Server("simple-prompts-mcp")


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    return await handle_list_prompts()


@server.get_prompt()
async def get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    return await handle_get_prompt(name, arguments)


@server.list_resources()
async def list_resources():
    return []


@server.list_tools()
async def list_tools():
    return []


async def run():
    """Run the server async context"""
    async with stdio_server() as streams:
        await server.run(
            streams[0],
            streams[1],
            initialization_options=InitializationOptions(
                server_name="simple-prompts-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    experimental_capabilities={},
                    notification_options=NotificationOptions(prompts_changed=True),
                ),
            ),
        )
