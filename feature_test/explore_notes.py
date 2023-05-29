from pathlib import Path

import streamlit as st


if "path" not in st.session_state:
    st.session_state.path = Path('.')

def change_dir_2(directory):
    st.session_state.path = st.session_state.path.joinpath(directory)

def parent_dir():
    st.session_state.path = st.session_state.path.parent

subpaths = [subpath for subpath in st.session_state.path.iterdir()]
directories = [subpath for subpath in subpaths if subpath.is_dir()]
note_files = [subpath for subpath in subpaths if subpath.is_file() and subpath.suffix=='.md']

st.sidebar.button(":back:", on_click=parent_dir)

for directory in directories: 
    col1, col2 = st.sidebar.columns(2)
    col1.write(f":file_folder:  {directory}")
    col2.button('Open', key=directory, on_click=change_dir_2, args=(directory,))


for note_file in note_files: 
    col1, col2 = st.sidebar.columns(2)
    col1.write(f":page_facing_up:  {note_file}")
    col2.button('Edit', key=note_file)