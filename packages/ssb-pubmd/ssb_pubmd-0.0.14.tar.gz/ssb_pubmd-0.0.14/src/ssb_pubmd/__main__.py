"""Command-line interface."""

import json
import os
from dataclasses import asdict
from dataclasses import dataclass

import click

from ssb_pubmd.browser_request_handler import BrowserRequestHandler
from ssb_pubmd.browser_request_handler import CreateContextMethod
from ssb_pubmd.markdown_syncer import MarkdownSyncer

BASE_DIR = os.path.join(os.path.expanduser("~"), ".pubmd")
os.makedirs(BASE_DIR, exist_ok=True)

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
BROWSER_CONTEXT_PATH = os.path.join(BASE_DIR, "browser_context.json")


@dataclass
class Config:
    """Handles the user configuration."""

    login_url: str = ""
    post_url: str = ""

    @classmethod
    def load(cls, path: str) -> "Config":
        """Loads the configuration from a file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)

    def save(self, path: str) -> None:
        """Saves the configuration to a file."""
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=4)


@click.command()
def config() -> None:
    """Set the login and post URL for the CMS."""
    config_file = CONFIG_PATH

    login_url = click.prompt("Enter the login URL", type=str)
    post_url = click.prompt("Enter the post URL", type=str)

    config = Config(login_url=login_url, post_url=post_url)

    config.save(config_file)

    click.echo(f"\nConfiguration stored in:\n{config_file}")


@click.command()
def login() -> None:
    """Log in to the CMS application."""
    config_file = CONFIG_PATH
    browser_context_file = BROWSER_CONTEXT_PATH

    config = Config.load(config_file)
    request_handler = BrowserRequestHandler(browser_context_file, config.login_url)

    method = CreateContextMethod.FROM_LOGIN
    with request_handler.new_context(method=method):
        click.echo("Logging in...")

    click.echo(f"\nBrowser context stored in:\n{browser_context_file}")


@click.command()
@click.argument("content_file_path", type=click.Path())
def sync(content_file_path: str) -> None:
    """Sync a markdown or notebook file to the CMS."""
    config_file = CONFIG_PATH
    browser_context_file = BROWSER_CONTEXT_PATH

    request_handler = BrowserRequestHandler(browser_context_file)

    with request_handler.new_context():
        config = Config.load(config_file)
        syncer = MarkdownSyncer(
            post_url=config.post_url, request_handler=request_handler
        )

        syncer.content_file_path = content_file_path
        content_id = syncer.sync_content()

    click.echo(
        f"File '{click.format_filename(browser_context_file)}' synced to CMS with content ID: {content_id}."
    )
    click.echo(f"Response data saved to '{click.format_filename(syncer.data_path)}'.")


@click.group()
def cli() -> None:
    """Pubmd - a tool to sync markdown and notebook files to a CMS."""
    pass


cli.add_command(config)
cli.add_command(login)
cli.add_command(sync)

if __name__ == "__main__":
    cli()
