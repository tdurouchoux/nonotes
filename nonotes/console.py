import os
from pathlib import Path
import datetime as dt
import configparser
from typing_extensions import Annotated

import typer
from rich import print
from rich.syntax import Syntax
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from nonotes.markdown_app import MarkdownApp
from nonotes.markdown_file_menu import choose_file, choose_directory

CONFIG_PATH = Path.home().joinpath("nonotes.ini")
CSS_PATH = Path(__file__).parent.joinpath("markdown_app.css")
app = typer.Typer()


def get_config():
    if not CONFIG_PATH.exists():
        print("nonotes has not been configured, please run:")
        print()
        print(Syntax("nonotes init", "bash"))
        print()
        raise typer.Abort()
    else:
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        return config


def validate_editor(editor: str) -> bool:
    ide_test_file = Path.home().joinpath("test_ide.md")

    if not ide_test_file.exists():
        with open(ide_test_file, "w") as file:
            file.write("# Test markdown\n\n\n")
            file.write("1. item 1\n")
            file.write("2. item 2")

    result = os.system(f"{editor} {ide_test_file}")

    ide_test_file.unlink()

    return result == 0


@app.command()
def init() -> None:
    if CONFIG_PATH.exists():
        if not inquirer.confirm(
            message="nonotes config file already exists. Do you want to overwrite it ?"
        ).execute():
            return
        else:
            CONFIG_PATH.unlink()

    config = configparser.ConfigParser()
    config["main"] = {}

    path = inquirer.filepath(
        message="Choose path for nonotes home directory :",
        default=str(Path.home()),
        validate=PathValidator(
            is_dir=True,
            message="Got invalid value for nonotes path, must be existing path."
        ),
    ).execute()
    home_directory = Path(path).joinpath("nonotes")

    if not home_directory.exists():
        home_directory.mkdir()

    config["main"]["home_directory"] = str(home_directory)

    ide_path = inquirer.text(
        message="Give an executable (path or command) for your choosen ide for markdown editing :",
        validate=validate_editor,
        invalid_message="Provided executable is not valid",
    ).execute()
    config["main"]["markdown_ide"] = ide_path

    if inquirer.confirm(message="Do you want to configure a light editor ?").execute():
        light_ide_path = inquirer.text(
            message="Give an executable (path or command) for your choosen ide for markdown editing :",
            validate=validate_editor,
            invalid_message="Provided executable is not valid",
        ).execute()
        config["main"]["light_markdown_ide"] = light_ide_path

    print("Nonotes configuration completed")
    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)


@app.command()
def view(home_directory: str = typer.Option(None, "--home-directory", "-h")):
    nonotes_config = get_config()
    markdown_app = MarkdownApp(
        nonotes_config["main"], CSS_PATH, override_directory=home_directory
    )
    markdown_app.run()


@app.command()
def edit(
    file: str = typer.Option(None, "--file", "-f"),
    home_directory: str = typer.Option(None, "--home-directory", "-h"),
    light_editor: bool = typer.Option(False, "--light-editor", "-l"),
) -> None:
    nonotes_config = get_config()["main"]

    if file is None:
        if home_directory is None:
            home_directory = nonotes_config["home_directory"]
        print("Please choose a file to edit :")
        file = choose_file(home_directory)

    if not Path(file).exists():
        print(f"Provided file {file} does not exist")
        typer.Exit()

    print(f"Starting editing of file: {file}")

    if light_editor and "light_markdown_ide" in nonotes_config:
        os.system(f"{nonotes_config['light_markdown_ide']} {file}")
    else:
        os.system(f"{nonotes_config['markdown_ide']} {file}")


@app.command()
def new(
    name: str = typer.Option(None, "--name", "-n"),
    home_directory: str = typer.Option(None, "--home-directory", "-h"),
    light_editor: bool = typer.Option(False, "--light-editor", "-l"),
) -> None:
    nonotes_config = get_config()["main"]
    if home_directory is None:
        home_directory = nonotes_config["home_directory"]

    print("Please choose a directory :")
    chosen_dir = choose_directory(home_directory)

    if name is None:
        name = inquirer.text(message="Choose a filename (no extensions) :")

    name = name.replace(" ", "_").lower()
    file = Path(home_directory).joinpath(chosen_dir).joinpath(f"{name}.md")

    print(file)
    current_time = dt.datetime.now().isoformat()

    with open(file, "r") as markdown:
        markdown.write(current_time)


def main():
    app()


if __name__ == "__main__":
    main()
