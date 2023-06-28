import urllib
import pathlib
import webbrowser

import markdown

from nonotes.latex import MarkdownLatex

latex = MarkdownLatex()
# EXTENSIONS = [latex]
EXTENSIONS = ['markdown.extensions.extra', 'markdown.extensions.toc']

def open_markdown_in_browser(file: pathlib.Path) -> None:
    with open(file, "r", encoding="utf-8") as file_reader:
        content = file_reader.read()
    
    markdown_html = markdown.markdown(content, extensions=EXTENSIONS)
    
    output_file = file.with_suffix(".html")
    
    with open(output_file, 'w', encoding="latin-1", errors="xmlcharrefreplace") as file_writer:
        file_writer.write(markdown_html)

    webbrowser.open(output_file.absolute().as_uri(), new=2)

