import asyncio

import yaml
from mcp.types import GetPromptResult, PromptMessage, TextContent

from .exceptions import NotFoundPrompt
from .models import SavedPrompt
from .utils import error_decorator, get_logger, get_prompt_file_paths

logger = get_logger()


async def find_target_prompt(path: str, name: str) -> SavedPrompt | None:
    with open(path) as f:
        data = yaml.safe_load(f)
    if (prompt := SavedPrompt(**data)).name == name:
        return prompt
    else:
        return None


async def find_prompt(name: str) -> SavedPrompt | None:
    files = get_prompt_file_paths()
    pending = set([asyncio.create_task(find_target_prompt(x, name)) for x in files])
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            result = task.result()
            if result is not None:
                for t in pending:
                    t.cancel()
                return result
    return None


def generate_text(prompt: str, arguments: dict[str, str] | None) -> str:
    if arguments is None:
        return prompt
    else:
        return prompt.format(**arguments)


@error_decorator
async def get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    prompt = await find_prompt(name)
    if prompt is None:
        raise NotFoundPrompt(f"Not found prompt (name: {name})")
    text = generate_text(prompt=prompt.prompt, arguments=arguments)

    return GetPromptResult(
        messages=[
            PromptMessage(role="user", content=TextContent(type="text", text=text))
        ]
    )
