import sqlite3

connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS task_container(id INTEGER PRIMARY KEY AUTOINCREMENT,session_id INTEGER, name text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS task_container_rel_task(container_id INTEGER, task_id INTEGER)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS task(id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER, name text, detail text, owner_id INTEGER)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS task_config(task_id INTEGER, color_id INTEGER)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255), hashed_pw INTEGER)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS user_rel_session(user_id INTEGER, session_id INTEGER)"
cursor.execute(create_table)

connection.commit()
connection.close()
