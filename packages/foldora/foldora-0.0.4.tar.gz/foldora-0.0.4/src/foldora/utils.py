import os
import click
from pathlib import Path
from os.path import isfile, isdir


def colorHandler(string: str, fgcolor: str):
    click.echo(click.style(string, fg=fgcolor), color=True)


def sub_dell(path):
    for sub in path.iterdir():
        if sub.is_dir():
            sub_dell(sub)
        if sub.is_file():
            sub.unlink()
    path.rmdir()


def sub_fill(path: Path):
    for df in os.listdir(path):
        origin_path: Path = Path(f"{path}/{df}").resolve()

        if isfile(origin_path):
            os.rename(origin_path, f"{path}/{df.replace(' ', '_')}")

        if isdir(origin_path):
            sub_fill(origin_path)
            os.rename(origin_path, f"{path}/{df.replace(' ', '_')}")

    list_path(path)


def list_path(path: Path):
    for df in os.listdir(path):
        origin_path: Path = Path(f"{path}/{df}").resolve()

        if isfile(origin_path):
            file = colorHandler(f"[FILE] RENAMED :: {df}", "bright_blue")
            click.echo(file, nl=True)

        if isdir(origin_path):
            folder = colorHandler(f"[FOLDER] RENAMED :: {df}", "green")
            click.echo(folder, nl=True)
