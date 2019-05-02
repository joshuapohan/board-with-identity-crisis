import psycopg2

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "dijital2012",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "kanbandb")
    cursor = connection.cursor()

    create_table = "CREATE TABLE IF NOT EXISTS task_container(id serial PRIMARY KEY,session_id INTEGER, name text)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS task_container_rel_task(container_id INTEGER, task_id INTEGER)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS task(id serial PRIMARY KEY, session_id INTEGER, name text, detail text, owner_id INTEGER)"
    cursor.execute(create_table)

    create_table = "CREATE TABLE IF NOT EXISTS task_config(task_id INTEGER, color_id INTEGER)"
    cursor.execute(create_table)
    
    create_table = "CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, username VARCHAR(255), hashed_pw INTEGER)"
    cursor.execute(create_table)
    
    create_table = "CREATE TABLE IF NOT EXISTS user_rel_session(user_id INTEGER, session_id INTEGER)"
    cursor.execute(create_table)

    connection.commit()
    connection.close()

except(Exception, psycopg2.DatabaseError) as error:
    print("Error while creating the table", error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print("postgres connection closed")
