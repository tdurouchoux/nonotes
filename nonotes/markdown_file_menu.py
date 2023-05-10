from pathlib import Path
from rich.syntax import Syntax
from pygments import formatters, highlight
from pygments.lexers.markup import MarkdownLexer

from simple_term_menu import TerminalMenu


def get_preview_function(path):
    def preview_file(filepath):
        if filepath == "<<< BACK":
            return ""

        filepath = Path(path).joinpath(filepath)
        if filepath.is_dir():
            return ""

        with open(filepath, "r") as file:
            markdown_content = file.read()
        formatter = formatters.TerminalFormatter(bg="dark")  # dark or light
        highlighted_file_content = highlight(
            markdown_content, MarkdownLexer(), formatter
        )

        return highlighted_file_content

    return preview_file


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
            options.append("<<< BACK")
        terminal_menu = TerminalMenu(
            options,
            preview_command=get_preview_function(current_path),
            skip_empty_entries=True,
        )
        menu_entry_index = terminal_menu.show()
        chosen_option = options[menu_entry_index][4:]

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
        if current_path != start_directory:
            options.append("<<< BACK")

        options.append(None)
        options.append("[OK]")

        terminal_menu = TerminalMenu(options, skip_empty_entries=True)
        menu_entry_index = terminal_menu.show()
        chosen_option = options[menu_entry_index]

        if chosen_option == "<<< BACK":
            current_path = current_path.parent
        elif chosen_option == "[OK]":
            return current_path
        else:
            current_path = current_path.joinpath(chosen_option)
