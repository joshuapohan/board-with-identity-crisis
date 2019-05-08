import psycopg2
from config import Config


try:
    Config.load_config()
    connection = psycopg2.connect(user = Config.get_db_user(),
                                  password = Config.get_db_password(),
                                  host = Config.get_db_host(),
                                  port = Config.get_db_port(),
                                  database = Config.get_db_database())
    cursor = connection.cursor()

    create_table = "CREATE TABLE IF NOT EXISTS task_container(id serial PRIMARY KEY,session_id INTEGER, name text)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS task_container_rel_task(container_id INTEGER, task_id INTEGER)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS task(id serial PRIMARY KEY, session_id INTEGER, name text, detail text, owner_id INTEGER)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS task_config(task_id INTEGER, color_id INTEGER)"
    cursor.execute(create_table)

    create_table = "DROP TABLE IF EXISTS users"
    cursor.execute(create_table)
    
    create_table = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, username VARCHAR(255), hashed_pw VARCHAR(256), email VARCHAR(255), is_validated BOOLEAN)"
    cursor.execute(create_table)
    
    create_table = "CREATE TABLE IF NOT EXISTS user_rel_session(user_id INTEGER, session_id INTEGER)"
    cursor.execute(create_table)

    connection.commit()
    connection.close()

except(Exception, psycopg2.DatabaseError) as error:
    print("Error while creating the table", error)
    connection = None

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("postgres connection closed")
