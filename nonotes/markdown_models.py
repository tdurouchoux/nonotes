from typing import List
from enum import Enum
import datetime as dt

MODELS = {
    "base": "",
    "workshop": (
        "- [Sujet 1](#sujet-1)\n"
        "- [Sujet 2](#sujet-2)\n"
        "- [ToDos](#todos)\n"
        "\n"
        "\n"
        "# Sujet 1\n"
        "\n"
        "**Problématique :**\n"
        "\n"
        "**Commentaires :**\n"
        "\n"
        "**Solutions :**\n"
        "\n"
        "# Sujet 2\n"
        "\n"
        "**Problématique :**\n"
        "\n"
        "**Commentaires :**\n"
        "\n"
        "**Solutions :**\n"
        "\n"
        "# ToDos \n"
        "\n"
        "1. todo1\n"
        "2. todo2\n"
    ),
    "reporting": (
        "# Information\n"
        "\n"
        "* Item 1\n"
        "* Item 2\n"
        "\n"
        "# ToDos\n"
        "\n"
        "1. first todo\n"
        "2. second todo\n"
    ),
    "presentation": (
        "- [First part](#first-part)\n"
        "- [Second part](#second-part)\n"
        "- [Remarks / interrogations](#remarks--interrogations)\n"
        "\n"
        "# First part\n"
        "\n"
        "# Second part\n"
        "\n"
        "# Remarks / interrogations\n"
        "\n"
        "* item 1\n"
        "* item 2\n"
    ),
}


class NoteModel(str, Enum):
    base = "base"
    workshop = "workshop"
    reporting = "reporting"
    presentation = "presentation"


def create_note_with_model(
    filename: str, model_name: str, title: str = None, tag_list: List[str] = None
):
    with open(filename, "w") as note:
        # model header
        note.write("|||\n| - | - |\n")

        if title is not None:
            note.write(f"| Titre | **{title}** |\n")

        note.write(f"| Date | {dt.date.today()} |\n")
        note.write(f"| Heure | {dt.datetime.now().strftime('%H:%M:%S')} |\n")

        if tag_list is not None:
            for tag in tag_list:
                note.write(f"| Tag | {tag} |\n")

        note.write("\n")

        # model content
        if model_name in NoteModel:
            note.write(MODELS[model_name.value])
        else:
            raise ValueError("Wrong value for model_name")
