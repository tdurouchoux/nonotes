import os
import sqlite3
import random
import datetime as dt

import streamlit as st

con = sqlite3.connect(os.path.abspath("../notebooks/test.db"))
cur = con.cursor()

def update_todos_status(title):
    
    status = getattr(st.session_state, f'{title.replace(" ", "_")}_status')
    
    cur.execute(f"""UPDATE todos
                SET status='{'done' if status else 'to do'}'
                WHERE title='{title}'""")
    con.commit()

def display_todos():
    res = cur.execute("SELECT title, status FROM todos")
    for title, status in res.fetchall():
        checkbox = st.checkbox(title,
                               value=(status == "done"),
                               on_change=update_todos_status,
                               args=(title,),
                               key=f'{title.replace(" ", "_")}_status'
                               )
        
def add_todo(todo):
    cur.execute(
        f"""INSERT INTO todos VALUES 
                ('{todo}', '{dt.datetime.now().isoformat()}', 'to do')"""
    )
    con.commit()


new_todo = st.text_input("add a todo : ")
add = st.button("Add")

if add:
    add_todo(new_todo)

display_todos()

col1, col2 = st.columns(2)

with open('corleone.md', 'r') as f:
    mark = col1.text_area('markdown edit:', value=f.read(), height=None)
    
col2.markdown(mark)