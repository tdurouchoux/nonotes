import os
from pathlib import Path
import datetime as dt
import configparser
from typing import Optional, List

from typing_extensions import Annotated
import typer
from rich import print
from rich.syntax import Syntax
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

from nonotes.markdown_app import MarkdownApp
from nonotes.markdown_file_menu import choose_file, choose_directory
from nonotes.markdown_models import NoteModel, create_note_with_model
from nonotes.browser_view import open_markdown_in_browser

CONFIG_PATH = Path.home() / "nonotes.ini"
CSS_PATH = Path(__file__).parent / "markdown_app.css"
app = typer.Typer()

# TODO add open in browser
# safari : open -a Safari ...
# edge : start msedge

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
    ide_test_file = Path.home() / "test_ide.md"

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
            message="Got invalid value for nonotes path, must be existing path.",
        ),
    ).execute()
    home_directory = Path(path) / "nonotes"

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
def view(
    home_directory: Annotated[
        str,
        typer.Option(
            "--home-directory",
            "-h",
            help="Optional value to overwrite configured home directory",
        ),
    ] = None,
):
    nonotes_config = get_config()
    markdown_app = MarkdownApp(
        nonotes_config["main"], CSS_PATH, override_directory=home_directory
    )
    markdown_app.run()

@app.command()
def display(
    file: Annotated[str, typer.Option("--file", "-f")] = None,
    home_directory: Annotated[
        str,
        typer.Option(
            "--home-directory",
            "-h",
            help="Optional value to overwrite configured home directory",
        ),
    ] = None,) -> None:
    
    nonotes_config = get_config()["main"]    
    
    if home_directory is None:
        home_directory = nonotes_config["home_directory"]    

    if file is None:
        print("Please choose a file to display :")
        file = Path(choose_file(home_directory))
    else:
        file = Path(home_directory) / file

    print(file)

    if not file.is_file():
        print(f"Provided file {file} does not exist")
        raise typer.Abort()
    
    open_markdown_in_browser(file)

@app.command()
def edit(
    file: Annotated[str, typer.Option("--file", "-f")] = None,
    home_directory: Annotated[
        str,
        typer.Option(
            "--home-directory",
            "-h",
            help="Optional value to overwrite configured home directory",
        ),
    ] = None,
    light_editor: Annotated[
        bool,
        typer.Option(
            "--light-editor", "-l", help="Use a light editor (only if configured)"
        ),
    ] = False,
) -> None:
    nonotes_config = get_config()["main"]

    if home_directory is None:
        home_directory = nonotes_config["home_directory"]

    if file is None:
        print("Please choose a file to edit :")
        file = Path(choose_file(home_directory))
    else:
        file = Path(home_directory) / file

    print(file)

    if not file.is_file():
        print(f"Provided file {file} does not exist")
        raise typer.Abort()

    print(f"Starting editing of file: {file}")

    if light_editor and "light_markdown_ide" in nonotes_config:
        os.system(f"{nonotes_config['light_markdown_ide']} {file}")
    else:
        os.system(f"{nonotes_config['markdown_ide']} {file}")


@app.command()
def new(
    title: Annotated[str, typer.Argument(help="Note filename and title")],
    home_directory: Annotated[
        str,
        typer.Option(
            "--home-directory",
            "-h",
            help="Optional value to overwrite configured home directory",
        ),
    ] = None,
    note_path: Annotated[
        str,
        typer.Option(
            "--note-path",
            "-p",
            help="Note path from home directory, if not existent it will be created",
        ),
    ] = None,
    model: Annotated[
        NoteModel,
        typer.Option(
            "--model",
            "-m",
            case_sensitive=False,
            prompt=True,
            help="Model name for note formatting",
        ),
    ] = NoteModel.base,
    tag_list: Annotated[
        Optional[List[str]],
        typer.Option(
            "--tag",
            "-t",
            help="Tag list that will be added to note (support multiple values)",
        ),
    ] = None,
    light_editor: Annotated[
        bool,
        typer.Option(
            "--light-editor",
            "-l",
            help="Use a light editor (only if configured)",
        ),
    ] = False,
) -> None:
    nonotes_config = get_config()["main"]
    if home_directory is None:
        home_directory = nonotes_config["home_directory"]

    if note_path is None:
        print("Please choose a subject :")
        file_path = choose_directory(home_directory)
    else:
        file_path = Path(home_directory) / note_path
        print(file_path)
        if not file_path.is_dir():
            if inquirer.confirm(
                message=f"Provided directory does not exist, create this path : {file_path} ?",
                default=True,
            ).execute():
                file_path.mkdir(parents=True)
            else:
                raise typer.Abort()

    filename = title.replace(" ", "_").lower()
    file = file_path / f"{filename}.md"

    if file.is_file():
        print("File already exists, please choose another title.")
        raise typer.Abort()

    create_note_with_model(file, model, title=title, tag_list=tag_list)

    if light_editor and "light_markdown_ide" in nonotes_config:
        os.system(f"{nonotes_config['light_markdown_ide']} {file}")
    else:
        os.system(f"{nonotes_config['markdown_ide']} {file}")


def main():
    app()


if __name__ == "__main__":
    main()
