from pathlib import Path
from rich.syntax import Syntax
from pygments import formatters, highlight
from pygments.lexers.markup import MarkdownLexer

from simple_term_menu import TerminalMenu

def get_preview_function(path):
    def preview_file(filepath):
        if filepath == "<< Back":
            return ""
        
        filepath = Path(path).joinpath(filepath)
        if not filepath.is_dir():
            with open(filepath, "r") as file:
                markdown_content = file.read()
            formatter = formatters.TerminalFormatter(bg="dark")  # dark or light
            highlighted_file_content = highlight(markdown_content, MarkdownLexer(), formatter)

            return highlighted_file_content
        return ""
    return preview_file

def main():
    home_directory = Path("../technical_knowledge")
    current_path = home_directory
    chosen_file = None

    while chosen_file is None:
        options = [
            subpath.name
            for subpath in current_path.iterdir()
            if  not subpath.name.startswith(".")
            and (subpath.is_dir() or subpath.suffix == ".md")
        ]
        # sorted(options)
        if current_path != home_directory:
            options.append("<< Back")
        terminal_menu = TerminalMenu(options, preview_command=get_preview_function(current_path))
        menu_entry_index = terminal_menu.show()
        chosen_option = options[menu_entry_index]
        if chosen_option == "<< Back":
            current_path = current_path.parent
        elif chosen_option.endswith(".md"):
            chosen_file = chosen_option
        else:
            current_path = current_path.joinpath(chosen_option)
        
    print(chosen_file)


if __name__ == "__main__":
    main()
