import os

import tomli
from pydantic import BaseModel, Field

from osa_tool.utils import osa_project_root


class PromptConfig(BaseModel):
    """
    Model for validating the structure of prompts loaded from prompts.toml.
    """
    file_summary: str = Field(..., description="Template for summarizing important files in the project structure and README.")
    pdf_summary: str = Field(..., description="Template for summarizing the main features of the project from a PDF.")
    overview: str = Field(..., description="Template for generating a general overview of the project.")
    content: str = Field(..., description="Template for generating the project's content'.")
    algorithms: str = Field(..., description="Template for describing key algorithms or methods used in the project.")


class PromptArticleLoader:
    def __init__(self):
        self.prompts = self.load_prompts()

    def load_prompts(self) -> PromptConfig:
        """
        Load and validate prompts from prompts.toml file.
        """
        with open(self._get_prompts_path(), "rb") as file:
            prompts = tomli.load(file)

        return PromptConfig(**prompts.get("prompts", {}))

    @staticmethod
    def _get_prompts_path() -> str:
        """
        Helper method to get the correct resource path,
        looking outside the package.
        """
        file_path = os.path.join(
            osa_project_root(),
            "config",
            "settings",
            "prompts_article.toml"
        )
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Prompts file {file_path} not found.")
        return str(file_path)
