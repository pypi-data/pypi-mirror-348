import asyncio

from mcp.types import Prompt
from yaml import safe_load

from .models import SavedPrompt
from .utils import error_decorator, get_prompt_file_paths


async def load_prompt(path: str) -> Prompt:
    with open(path) as f:
        data = safe_load(f)
    return SavedPrompt(**data).convert()


@error_decorator
async def list_prompts() -> list[Prompt]:
    files = get_prompt_file_paths()
    return await asyncio.gather(*[load_prompt(x) for x in files])
