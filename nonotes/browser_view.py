import pathlib
import webbrowser

import markdown
from bs4 import BeautifulSoup

EXTENSIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.toc",
    "markdown.extensions.sane_lists",
    "markdown.extensions.codehilite",
    "mdx_math",
]
EXTENSIONS_CONFIG = {"mdx_math": {"enable_dollar_delimiter": True}}

JS_SCRIPT = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-MML-AM_CHTML"
CSS_FILE = str(pathlib.Path(__file__).parent.parent / "styling" / "styles.css")


def open_markdown_in_browser(file: pathlib.Path) -> None:
    with open(file, "r", encoding="utf-8") as file_reader:
        content = file_reader.read()

    markdown_html = markdown.markdown(
        content, extensions=EXTENSIONS, extension_configs=EXTENSIONS_CONFIG
    )

    print(CSS_FILE)
    markdown_soup = BeautifulSoup(markdown_html, "lxml")
    head_tag = markdown_soup.new_tag("head")
    html_tag = markdown_soup.html
    html_tag.insert(0, head_tag)

    script_tag = markdown_soup.new_tag(
        "script",
        type="text/javascript",
        # async=True,
        src=JS_SCRIPT,
    )
    head_tag.append(script_tag)

    link_tag = markdown_soup.new_tag(
        "link",
        rel="stylesheet",
        type="text/css",
        href=CSS_FILE,
    )
    head_tag.append(link_tag)

    output_file = file.with_suffix(".html")

    with open(
        output_file, "w", encoding="latin-1", errors="xmlcharrefreplace"
    ) as file_writer:
        file_writer.write(str(markdown_soup))

    webbrowser.open(output_file.absolute().as_uri(), new=2)
