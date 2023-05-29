import os
from pathlib import Path

import streamlit as st
from streamlit_ace import st_ace


if "path" not in st.session_state:
    st.session_state.path = Path(__file__).parent.parent.parent.joinpath("technical_knowledge")

if "edit_file" not in st.session_state:
    st.session_state.edit_file = None


def change_dir(directory):
    st.session_state.path = st.session_state.path.joinpath(directory)


def parent_dir():
    st.session_state.path = st.session_state.path.parent


def edit_file(note_file):
    st.session_state.edit_file = st.session_state.path.joinpath(note_file)


def create_directory(new_directory):
    if new_directory != "":
        st.session_state.path.joinpath(new_directory).mkdir()


subpaths = [subpath for subpath in st.session_state.path.iterdir()]
directories = [subpath.name for subpath in subpaths if subpath.is_dir()]
note_files = [
    subpath.name
    for subpath in subpaths
    if subpath.is_file() and subpath.suffix == ".md"
]

st.sidebar.button(":back:", on_click=parent_dir)

for directory in directories:
    col1, col2 = st.sidebar.columns(2)
    col1.write(f":file_folder:  {directory}")
    col2.button("Open", key=directory, on_click=change_dir, args=(directory,))


for note_file in note_files:
    col1, col2 = st.sidebar.columns(2)
    col1.write(f":page_facing_up:  {note_file}")
    col2.button("Edit", key=f"edit_{note_file}", on_click=edit_file, args=(note_file,))

col1, col2 = st.sidebar.columns(2)
new_directory = col1.text_input("New directory", placeholder="Directory name")
col2.button(
    ":heavy_plus_sign: Create", on_click=create_directory, args=(new_directory,)
)

st.sidebar.divider()

title = st.sidebar.text_input("Note title")


if st.session_state.edit_file is not None:
    with st.session_state.edit_file.open() as f:
        note_content = f.read()

    content = st_ace(
        value=note_content,
        placeholder="Start typing note",
        language="markdown",
        font_size=11,
        theme="twilight",
        key="note",
        auto_update=False,
    )

preview = st.checkbox("Display preview", value=False)
if preview:
    st.markdown(content)
