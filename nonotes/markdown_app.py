import os
from pathlib import Path
from typing import Dict, Iterable

from textual.app import App, CSSPathType, ComposeResult
from textual.containers import Container
from textual.driver import Driver
from textual.reactive import var
from textual.widgets import Footer, MarkdownViewer, Header, DirectoryTree


class FilteredDirectoryTree(DirectoryTree):
    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if path.is_dir() or path.suffix == '.md']

class MarkdownApp(App):
    
    BINDINGS = [
        ("f", "toggle_files", "Directory"),
        ("t", "toggle_table_of_contents", "TOC"),
        ("r", "refresh", "Refresh"),
        ("e", "edit", "Edit"),
        ("l", "light_edit", "Light edit"),
        ("q", "quit", "Quit"),
    ]

    path = var(None)
    show_tree = var(True)

    def __init__(self,
                 config: Dict,
                 css_path: Path,
                 override_directory: Path = None):
        self.markdown_ide = config["markdown_ide"]
        self.light_markdown_ide = config.get("light_markdown_ide")

        if override_directory is None:
            self.directory = Path(config["home_directory"])
        else:
            self.directory = override_directory
                
        super().__init__(css_path=css_path)
    
    @property
    def directory_tree(self) -> FilteredDirectoryTree:
        return self.query_one(FilteredDirectoryTree)

    @property
    def markdown_viewer(self) -> MarkdownViewer:
        """Get the Markdown widget."""
        return self.query_one(MarkdownViewer)

    def watch_show_tree(self, show_tree: bool) -> None:
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield FilteredDirectoryTree(self.directory, id="tree-view")
            yield MarkdownViewer(id="markdown-view")
        yield Footer()
    
    async def open_file(self):
        self.markdown_viewer.focus()
        if self.path is None:
            self.sub_title = "No file selected"
        elif not await self.markdown_viewer.go(self.path):
            self.exit(message=f"Unable to load {self.path!r}")
        else:
            self.sub_title = Path(self.path).name
    
    def on_mount(self):
        self.sub_title = "No file selected"
    
    async def on_directory_tree_file_selected(self, event: FilteredDirectoryTree.FileSelected):
        event.stop()
        self.path = event.path
        await self.open_file()

    def action_toggle_files(self) -> None:
        self.show_tree = not self.show_tree

    def action_toggle_table_of_contents(self) -> None:
        self.markdown_viewer.show_table_of_contents = (
            not self.markdown_viewer.show_table_of_contents
        )

    async def action_refresh(self):
        await self.open_file()

    def action_edit(self):
        if self.path is not None:
            os.system(f"{self.markdown_ide} {self.path}")
        
    def action_light_edit(self):
        if self.path is not None:
            if self.light_markdown_ide is None:
                self.action_edit()
            else:
                os.system(f"{self.light_markdown_ide} {self.path}")
            
# def main(argv):
# get config

if __name__ == "__main__":
    app = MarkdownApp()
    app.run()
