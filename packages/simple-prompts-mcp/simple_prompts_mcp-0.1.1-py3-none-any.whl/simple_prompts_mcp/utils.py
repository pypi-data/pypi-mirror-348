from functools import wraps
from glob import glob
from logging import DEBUG, Logger, getLogger
from pathlib import Path
from typing import Callable

from .models import Settings


def resolve_prompts_dir() -> str:
    if prompts_dir := Settings().prompts_dir:
        return prompts_dir

    return f"{Path.home()}/.config/simple-prompts-mcp"


def get_prompt_file_paths() -> list[str]:
    prompt_dir = resolve_prompts_dir()
    return glob(f"{prompt_dir}/*.yml") + glob(f"{prompt_dir}/*.yaml")


def get_logger() -> Logger:
    logger = getLogger("simple-prompts-mcp")
    logger.setLevel(DEBUG)
    return logger


def error_decorator(func: Callable) -> Callable:
    @wraps(func)
    def process(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = get_logger()
            logger.error(f"[{type(e)}] Error occurred", exc_info=True)
            raise

    return process
