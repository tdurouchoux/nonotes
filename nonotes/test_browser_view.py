from pathlib import Path

from nonotes.browser_view import open_markdown_in_browser

markdown_file = Path("../../technical_knowledge/graphs/cs224w_graph.md")

open_markdown_in_browser(markdown_file)