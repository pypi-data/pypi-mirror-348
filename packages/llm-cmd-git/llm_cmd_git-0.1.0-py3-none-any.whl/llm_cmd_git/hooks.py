import llm
from click import Group

from .cli import cli as git_commands


@llm.hookimpl
def register_commands(cli: Group):
    cli.add_command(git_commands, "git")
