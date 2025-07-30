import inspect
import re
from typing import Any, Callable, Literal

import llm
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from .prompts import common, conventional, default, odoo


class CommonSettings(BaseSettings):
    model: str | None = Field(default=None, description="Model name")
    key: str | None = Field(default=None, description="Model API Key")
    options: dict = Field(default={}, description="Model options")

    def get_llm_model(self) -> llm.Model:
        model = llm.get_model(self.model)
        if model.needs_key:
            model.key = llm.get_key(self.key, model.needs_key, model.key_env_var)
        return model

    model_config = SettingsConfigDict(
        env_nested_delimiter="_",
        env_prefix="llm_git_",
        pyproject_toml_table_header=("tool", "llm-git"),
        toml_file=[".llm-git.toml", "llm-git.toml", llm.user_dir() / "llm-git.toml"],
        nested_model_default_partial_update=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            PyprojectTomlConfigSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
        )


class CommitSettings(CommonSettings):
    preset: Literal["default", "conventional", "odoo"] = Field(
        default="default", description="Commit message style preset"
    )
    system_prompt_custom: str | None = Field(
        default=None,
        description="Custom prompt to overrides preset system prompt",
    )
    user_prompt_template: str | None = Field(
        default=None,
        description="Custom user prompt",
    )
    extra_context: str | None = Field(
        default=None, description="Extra context added to the prompt"
    )
    edit: bool = Field(
        default=True,
        description="Open editor to edit the generated commit message",
    )

    @property
    def system_prompt(self):
        if self.system_prompt_custom:
            return self.system_prompt_custom

        match self.preset:
            case "conventional":
                return conventional.SYSTEM_PROMPT
            case "odoo":
                return odoo.SYSTEM_PROMPT
            case _:
                return default.SYSTEM_PROMPT

    @property
    def user_prompt(self):
        return self.user_prompt_template or common.USER_PROMPT

    def generate_commit_message(
        self,
        diff: str,
        stream_callback: Callable[[str], Any] | None = None,
    ) -> str:
        model_obj = self.get_llm_model()
        is_stream = bool(stream_callback)
        context = self.extra_context or "None"
        system_prompt = self.system_prompt
        user_prompt = self.user_prompt.format(diff=diff, context=context)

        response = model_obj.prompt(
            inspect.cleandoc(user_prompt),
            system=inspect.cleandoc(system_prompt),
            stream=is_stream,
            **self.options,
        )

        if is_stream:
            for chunk in response:
                stream_callback(chunk)

        return self.finalize(response.text())

    def finalize(self, message: str) -> str:
        matches = re.findall(r"<message>(.+?)</message>", message, re.DOTALL)
        return str(matches[-1]).strip() if matches else ""
