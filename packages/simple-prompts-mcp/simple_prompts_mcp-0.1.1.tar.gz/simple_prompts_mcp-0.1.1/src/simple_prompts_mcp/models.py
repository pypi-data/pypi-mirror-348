from mcp.types import Prompt, PromptArgument
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class EnvironmentVariables(BaseSettings):
    home: str


class Settings(BaseSettings):
    prompts_dir: str | None = None


class SavedPrompt(Prompt):
    prompt: str

    def convert(self) -> Prompt:
        return Prompt(
            name=self.name, description=self.description, arguments=self.arguments
        )
