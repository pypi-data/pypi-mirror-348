import sys

import llm
import questionary
import rich
import rich_click as click
from click import ParamType
from click.shell_completion import CompletionItem
from pydanclick import from_pydantic
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner

from . import git
from .settings import CommitSettings


@click.group()
def cli(): ...


class ModelNameType(ParamType):
    name = "model_name"

    def shell_complete(self, ctx, param, incomplete):
        models = llm.get_model_aliases()
        return [
            CompletionItem(name)
            for name in models.keys()
            if name.startswith(incomplete)
        ]


@cli.command()
@from_pydantic(
    CommitSettings,
    shorten={
        "model": "-m",
        "key": "-k",
        "options": "-o",
        "preset": "-P",
        "system_prompt_custom": "-S",
        "user_prompt_template": "-U",
        "extra_context": "-X",
    },
    extra_options={
        "model.name": {
            "type": ModelNameType(),
        }
    },
)
def commit(commit_settings: CommitSettings):
    """
    Generate Commit Message from Staged Diff
    """
    diff = git.get_staged_diff()
    if not diff:
        rich.print("No staged changes found.")
        return

    with Live(refresh_per_second=10) as live:
        live.update(Spinner("dots", text="Generating..."))
        result = ""

        def callback(chunk: str):
            nonlocal result
            result += chunk
            live.update(
                Panel(result, title="Generating...", title_align="right", width=80)
            )

        commit_message = commit_settings.generate_commit_message(diff, callback)

    rich.print(
        Panel(commit_message, title="Commit Message", title_align="right", width=80)
    )

    if not commit_settings.edit:
        git.commit_staged(commit_message, edit=False)
        return

    if not sys.stdin.isatty():
        return

    answer = questionary.select(
        "Action to do",
        choices=[
            questionary.Choice(title="Accept", value="accept", shortcut_key="a"),
            questionary.Choice(title="Edit", value="edit", shortcut_key="e"),
            questionary.Choice(title="Reject", value="reject", shortcut_key="r"),
        ],
        use_arrow_keys=True,
        use_jk_keys=True,
        use_shortcuts=True,
    ).ask()
    match answer:
        case "accept":
            git.commit_staged(commit_message, edit=False)
        case "edit":
            git.commit_staged(commit_message, edit=True)
        case _:
            return
