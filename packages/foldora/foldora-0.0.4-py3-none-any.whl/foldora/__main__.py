import click

from foldora.commands import (
    create_directories,
    create_files,
    list_all,
    purge_all,
    rename_spaces,
    show_contents,
)


@click.group()
@click.version_option("0.0.4")
def cli():
    """
    Foldora - File & Directory Manager CLI Tool.

    A command line utility (CLI) for file and directory operations.
    Provides commands to list, create, and purge directories and files, and more.
    """
    pass


cli.add_command(list_all, "la")
cli.add_command(create_directories, "cd")
cli.add_command(create_files, "cf")
cli.add_command(purge_all, "pa")
cli.add_command(show_contents, "sc")
cli.add_command(rename_spaces, "rs")
