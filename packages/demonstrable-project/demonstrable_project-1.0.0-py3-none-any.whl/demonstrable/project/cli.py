import importlib.resources
from pathlib import Path
import click
import logging
from functools import partial

from yaspin import yaspin

from demonstrable.exception import handled_errors
from demonstrable.project.process import run_process
from demonstrable.project.resources import emplace_project
import demonstrable.project.package_data
import demonstrable.project.metadata

from . import __version__

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    token_normalize_func=lambda x: x.replace("-", "_"),
)


def print_user_error(exc, spinner):
    spinner.fail("✘")
    with spinner.hidden():
        click.secho(str(exc), err=True, fg="yellow")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--verbosity",
    "-v",
    default=None,
    help="The logging level to use.",
    type=click.Choice(
        [name for lvl, name in sorted(logging._levelToName.items()) if lvl > 0],
        case_sensitive=False,
    ),
)
@click.version_option(__version__)
def cli(verbosity):
    logging_level = verbosity and getattr(logging, verbosity.upper(), None)

    kwargs = {}
    if logging_level is None:
        kwargs["format"] = "%(message)s"  # By default, simplify message output
    else:
        kwargs["level"] = logging_level

    logging.basicConfig(**kwargs)


def _validate_name(ctx, param, value):
    if value:
        try:
            return demonstrable.project.metadata.valid_name(value)
        except demonstrable.project.metadata.InvalidNameError as e:
            raise click.BadParameter(str(e))
    return value


def _validate_description(ctx, param, value):
    if value:
        try:
            return demonstrable.project.metadata.valid_description(value)
        except demonstrable.project.metadata.InvalidDescriptionError as e:
            raise click.BadParameter(str(e))
    return value


@cli.command()
@click.argument("project_directory", type=click.Path(file_okay=False, path_type=Path), required=False, default=None)
@click.option("--name", default=None, help="The name of the project.", prompt=True, callback=_validate_name)
@click.option("--description", default=None, help="The description of the project.", prompt=True, callback=_validate_description)
@click.option("--recipe/--no-recipe", default=True, help="Create a recipe for the project.")
def init(
    project_directory: Path | None,
    name: str | None,
    description: str | None,
    recipe: bool = True,
):
    """Initialize a directory as a new Demonstrable project. If no directory is specified, the current directory is used."""
    with yaspin(text="Initializing Demonstrable Project") as spinner:
        with handled_errors(partial(print_user_error, spinner=spinner)):
            if project_directory is None:
                project_directory = Path.cwd()

            spinner.write(f"> Creating a new project at '{project_directory}'")
            emplace_project(project_directory, name, description)

            spinner.write("> Syncing the  dependencies")
            run_process("uv sync", project_directory)

            spinner.write("> Initialize demonstrable-deca")
            run_process("uv run deca init", project_directory)

            if recipe:
                spinner.write("> Creating a deca recipe")
                run_process("uv run deca create-recipe", project_directory)

        spinner.ok("✔")


def main():
    """Main entry point for the CLI."""
    cli(prog_name="demonstrable-project")


if __name__ == "__main__":
    main()