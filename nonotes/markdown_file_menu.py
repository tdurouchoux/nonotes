from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.separator import Separator


def choose_file(start_directory: str = None):
    start_directory = Path(start_directory)
    current_path = start_directory
    chosen_file = None

    while chosen_file is None:
        options = [
            "[D] " + subpath.name
            for subpath in current_path.iterdir()
            if not subpath.name.startswith(".") and subpath.is_dir()
        ]

        options += [
            "[m] " + subpath.name
            for subpath in current_path.iterdir()
            if subpath.suffix == ".md"
        ]

        # sorted(options)
        if current_path != start_directory:
            options.append(Separator())
            options.append("<<< BACK")

        chosen_option = inquirer.select(
            message="Choose file :", choices=options
        ).execute()[4:]

        if chosen_option == "BACK":
            current_path = current_path.parent
        elif chosen_option.endswith(".md"):
            return current_path.joinpath(chosen_option)
        else:
            current_path = current_path.joinpath(chosen_option)


def choose_directory(start_directory: str) -> None:
    start_directory = Path(start_directory)
    current_path = start_directory
    chosen_file = None

    while chosen_file is None:
        options = [
            subpath.name
            for subpath in current_path.iterdir()
            if not subpath.name.startswith(".") and subpath.is_dir()
        ]

        options.append(Separator())
        if current_path != start_directory:
            options.append("<<< BACK")
        options.append("[OK]")

        chosen_option = inquirer.select(
            message="Choose directory :", choices=options
        ).execute()

        if chosen_option == "<<< BACK":
            current_path = current_path.parent
        elif chosen_option == "[OK]":
            print(current_path)
            return current_path
        else:
            current_path = current_path.joinpath(chosen_option)
