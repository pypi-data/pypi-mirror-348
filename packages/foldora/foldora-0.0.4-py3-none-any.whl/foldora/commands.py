import os
import time
import click
from pathlib import Path

from foldora.utils import sub_dell, list_path, sub_fill, colorHandler


@click.command(help="List all files and directories.")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True, file_okay=False, readable=True, path_type=Path),
)
def list_all(paths):
    """
    List all files and directories in the current or specified paths.

    Lists all files and directories within the specified paths. If no paths are provided, the contents of the current working directory are listed. Useful for quickly inspecting directory structures.

    Args:\n
        paths (tuple of str, optional) : One or more directory paths to list. Defaults to the current directory if not provided.

    Examples:
        - fd la\n
        - fd la /path/to/directory\n
        - fd la /path1 /path2

    Notes:\n
        - Hidden files and directories may also be included depending on the system settings.\n
        - If a specified path is a file, only that file will be listed.\n
        - Multiple paths can be specified to list contents from different directories at once.
    """

    if len(paths) == 0:
        click.echo("\t")

        if len(list(Path.cwd().iterdir())) == 0:
            colorHandler("[PS] :: EMPTY FOLDER.\n", "magenta")
            return

        for entry in Path.cwd().iterdir():
            if entry.is_dir():
                colorHandler(f"[DIR] :: {entry.name}.", "green")
            else:
                colorHandler(f"[FILE] :: {entry.name}.", "blue")

        click.echo("\t")
        return

    for i, path in enumerate(paths):
        click.echo("\t")

        # if Path(path).is_file():
        #     click.echo(f"({path}) is not a directory path.:")

        if len(paths) > 1:
            click.echo(f"({path}):")

        if len(list(path.iterdir())) < 1:
            colorHandler("[PS] :: EMPTY FOLDER.\n", "magenta")
            return

        for entry in path.iterdir():
            if entry.is_dir():
                colorHandler(f"[DIR] :: {entry.name}.", "green")
            else:
                colorHandler(f"[FILE] :: {entry.name}.", "blue")

        if i > 1:
            click.echo("\t")

    click.echo("\t")


@click.command(help="Create one or more directories.")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(file_okay=False, exists=False, path_type=Path),
)
def create_directories(paths):
    """
    Create one or more directories.

    Creates one or more directories. If a parent directory in the specified path does not exist, it will be created automatically. Existing directories are not modified.

    Args:
        paths (tuple of str): Paths to the directories to be created.

    Examples:
        fd dr new_directory another_directory\n
        fd dr /path/to/parent/new_directory

    Notes:
        - Creates all necessary parent directories if they do not exist.
        - Does not modify existing directories.
        - Supports creating multiple directories in a single command.
    """

    if len(paths) < 1:
        colorHandler("\n[PS] :: A PATH IS REQUIRED.\n", "yellow")
        return

    click.echo("\t")

    for i, p in enumerate(paths):
        try:
            p.mkdir(parents=True, exist_ok=True)
            colorHandler(f"[DONE] :: {paths[i]} CREATED.", "green")

            time.sleep(0.5)
        except PermissionError:
            colorHandler(f"[DENIED] :: ({paths[i]}) NOT CREATED.\n", "red")
            return

    colorHandler(f"\n[DONE] :: ({len(paths)}) DIR(s) CREATED.\n", "blue")


@click.command(help="Create one or more files.")
@click.option(
    "-p",
    "--path",
    nargs=1,
    type=click.Path(exists=False, path_type=Path),
    help="Custom path where the file(s) will be saved.",
)
@click.argument(
    "paths",
    nargs=-1,
    type=click.File(
        mode="w",
        encoding="utf-8",
    ),
)
def create_files(paths, path):
    """
    Create one or more files in the current or specified directory.

    Creates one or more empty files in the current directory or a specified path. If a custom path is provided, the files are created in that location instead.

    Args:
        filenames (tuple of str): Names of the files to be created.
        path (str, optional): Custom directory where the files should be created. If not provided, the current directory is used.

    Examples:
        fd fl file1.txt file2.txt\n
        fd fl file1.txt file2.txt -p /path/to/dir

    Notes:
        - Existing files with the same names will not be overwritten.
        - If the specified directory does not exist, an error will be raised.
        - Supports creating multiple files in a single command.
    """

    click.echo("\t")

    if path:
        try:
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            colorHandler(f"[DENIED] :: ({path}) REQUIRE FULL ACCESS.\n", "red")
            return

        for f in paths:
            try:
                with open(path / f.name, "w") as file:
                    file.write("")

                colorHandler(f"\n[DONE] :: FILE ({f.name}) CREATED.", "green")

            except PermissionError:
                colorHandler(f"[DENIED] :: ({f.name}) REQUIRE FULL ACCESS.", "red")
                continue

        click.echo("\t")
        return

    if len(paths) == 0:
        colorHandler("[PS] :: PATH IS REQUIRED.\n", "yellow")
        return

    for f in paths:
        try:
            if not Path(f.name).parent.exists():
                Path(f.name).parent.mkdir(parents=True, exist_ok=True)

            with open(f.name, "w") as file:
                file.write("")

            colorHandler(f"[DONE] :: FILE ({f.name}) CREATED.", "blue")

        except PermissionError:
            colorHandler(f"\n[DENIED] :: ({f.name}) REQUIRE FULL ACCESS.\n", "red")
            continue

    click.echo("\t")


# except (FileNotFoundError, FileExistsError):
# click.echo(f"\n[DENIED] :: ({Path(f.filename).parent}) NOT FOUND.\n")
# continue


@click.command(help="Delete specified files and directories permanently.")
@click.argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, readable=True, path_type=Path),
)
def purge_all(paths):
    """
    Delete specified files and directories.

    Permanently deletes the specified files and directories. Requires user confirmation before proceeding to prevent accidental data loss. Useful for quickly removing unwanted files or entire directories.

    Args:
        paths (tuple of Path): One or more file or directory paths to be deleted.

    Examples:
        fd pg file1.txt directory1

    Notes:
        - Use with caution, as this action cannot be undone.
        - Directories will be deleted recursively, including all their contents.
        - Ensure you have the necessary permissions to delete the specified paths.
    """

    dirs = []
    files = []

    if len(paths) < 1:
        colorHandler("\n[PS] :: A PATH IS REQUIRED.\n", "yellow")
        return

    click.echo("\t")

    if not click.confirm(text="Proceed with deleting the files/folders?", abort=True):
        return

    click.echo("\t")

    for i, path in enumerate(paths):

        # Directories
        if path.is_dir():
            try:
                sub_dell(path)
                dirs.append(i)
            except PermissionError:
                colorHandler(f"\n[DENIED] :: ({path}) NOT DELETED.\n", "red")
                continue

        # Files
        if path.is_file():
            try:
                path.unlink(path)
                files.append(i)
            except PermissionError:
                colorHandler(f"\n[DENIED] :: ({path}) NOT DELETED.\n", "red")
                continue

    if len(dirs) > 0:
        colorHandler(f"[DONE] :: ({len(dirs)}) DIR(s) REMOVED.", "green")

    if len(files) > 0:
        colorHandler(f"[DONE] :: ({len(files)}) FILE(s) REMOVED.", "blue")

    click.echo("\t")


@click.command(help="Display the contents of one or more files.")
@click.argument("files", nargs=-1, type=click.File(mode="r"))
def show_contents(files):
    """
    Display the contents of one or more files.

    Prints the contents of one or more specified files to the console. Each file is read in order,and its contents are displayed sequentially. Useful for quickly reviewing file contents from the command line.

    Args:
        files (tuple of File): One or more file objects whose contents should be displayed.

    Examples:
        fd ct file1.txt file2.txt

    Notes:
        - Files must be readable, or an error will be raised.
        - Supports multiple files, displaying each file's content in sequence.
    """

    if len(files) < 1:
        colorHandler("\n[PS] :: A PATH IS REQUIRED.\n", "yellow")
        return

    click.echo("\t")

    for file in files:
        colorHandler(f"============[{file.name}]============", "green")
        click.echo("\t")
        click.echo(f"{file.read().strip()}", nl=True)

        if file != files[-1]:
            click.echo("\t")

    click.echo("\t")


@click.command(help="Replace spaces in file and folder names with underscores.")
@click.argument(
    "path",
    nargs=1,
    required=False,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True, path_type=Path),
)
def rename_spaces(path):
    """
    Replace spaces in file and folder names with underscores.

    This command renames files and folders by replacing any spaces in their names with underscores. It operates on the specified directory (or the current directory if none is provided). All files and directories in that location will have their names updated to remove spaces.

    Args:
        path (str, optional): The directory to process. Defaults to the current working directory if not specified.

    Examples:
        fd bk /path/to/dir

    Notes:
        - By default, only top-level files and folders are renamed.
        - When prompted, entering 'y' activates Deep Folder Traversal mode, which processes all nested directories.
        - Deep Folder Traversal mode allows recursive renaming for all files and folders within the specified path.
    """

    click.echo("\t")

    if not path:
        path = "."

    if click.confirm(text="Deep Folder Traversal ?", abort=False):
        try:
            sub_fill(Path(path).resolve())
            colorHandler("\n[DONE] :: DIRS/FILES RENAMED.\n", "green")
            return
        except PermissionError:
            colorHandler("\n[DENIED] :: ADMIN ACCESS REQUIRED.\n", "red")
            return

    for df in os.listdir(path):
        origin_path: Path = Path(f"{path}/{df}").resolve()

        try:
            if os.path.isfile(origin_path):
                os.rename(origin_path, f"{path}/{df.replace(' ', '_')}")

            if os.path.isdir(origin_path):
                os.rename(origin_path, f"{path}/{df.replace(' ', '_')}")

        except PermissionError:
            colorHandler("\n[!] Operation Denied.\n", "red")
            continue

    list_path(Path(path).resolve())
    colorHandler("\n[DONE] :: DIRS.FILES RENAMED.\n", "green")
