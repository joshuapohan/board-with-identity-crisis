"""
Module containing classes that maps them models to a database

Author : JPO

Todo:
    Use UUID to map between real object id and the id exposed to client side
    Add support for postgres
"""

from config import Config
import json
import sqlite3
import psycopg2


def get_postgres_connection():
    try:
        return psycopg2.connect(user = Config.get_db_user(),
                                password = Config.get_db_password(),
                                host = Config.get_db_host(),
                                port = Config.get_db_port(),
                                database = Config.get_db_database())
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error while creating the table", error)

class TasksContainerMapper:
    """ Mapper for task container, maps the class instance to a database """

    @classmethod
    def save(cls, task_container):
        """ Saves the task container to a database,based on the path provided by Config 
        Args:
            task_container (TasksContainer) : the container instance to be saved to db 
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            cls.sqlite_save(task_container)
        elif db_type == 2:
            cls.postgres_save(task_container)

    @classmethod
    def delete_by_id(cls, _id):
        """ Deletes the task container in the database by id 
        Args:
            _id (int) : the id of the container to delete 
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            cls.sqlite_delete_by_id(_id)
        elif db_type == 2:
            cls.postgres_delete_by_id(_id)

    @classmethod
    def get_row_by_id(cls, _id):
        """ Retrieve a row from the database where it matches the id
        Args:
            _id (int) : the id of the container row to get
        Returns:
            tuple: tuple of parameters of the row matching the id
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_row_by_id(_id)
        elif db_type == 2:
            return cls.postgres_get_row_by_id(_id)

    @classmethod
    def get_all_rows(cls):
        """ Retrieve all rows of the container from the db, returns list
            Returns:
                list: list of all container rows in the db
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_all_rows()
        elif db_type == 2:
            return cls.postgres_get_all_rows()

    @classmethod
    def get_all_rows_by_session(cls, session_id):
        """ Retrieve all container rows that match the session id
        Args:
            session_id (int) : the id of the session / room
        Returns:
            list: list of all rows belonging to the session_id
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_all_rows_by_session(session_id)
        elif db_type == 2:
            return cls.postgres_get_all_rows_by_session(session_id)

    @classmethod
    def sqlite_save(cls, task_container):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()
        if task_container._id:
            # if _id exists then it must have been stored in the db
            insert_container_stmt = "UPDATE task_container SET name=? WHERE id=?;"
            cursor.execute(insert_container_stmt, (task_container._name, task_container._id,))
        else:
            # if no _id then create new
            insert_container_stmt = "INSERT INTO task_container VALUES(NULL,?,?);"
            cursor.execute(insert_container_stmt, (task_container.session_id, task_container._name,))        
            task_container._id = cursor.lastrowid


        if task_container._id:
            # Delete all existing relations for this object first
            delete_relation_stmt = "DELETE FROM task_container_rel_task WHERE container_id=?;"
            cursor.execute(delete_relation_stmt, (task_container._id,))

            #insert all relations
            insert_container_rel_stmt = "INSERT INTO task_container_rel_task VALUES(?,?)"
            for task_id in task_container.task_ids:
                cursor.execute(insert_container_rel_stmt, (task_container._id, task_id))
            connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def sqlite_delete_by_id(cls, _id):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        delete_stmt = "DELETE FROM task_container WHERE id=?"
        delete_relation_stmt = "DELETE FROM task_container_rel_task WHERE container_id=?"
        cursor = connection.cursor()
        cursor.execute(delete_stmt, (_id,))
        cursor.execute(delete_relation_stmt, (_id,))
        connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def sqlite_get_row_by_id(cls, _id):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task_container WHERE id=?"
        cursor.execute(select_stmt, (_id,))
        container_row  = cursor.fetchone()

        cursor.close()
        connection.close()

        return container_row

    @classmethod
    def sqlite_get_all_rows(cls):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task_container"
        cursor = connection.cursor()
        cursor.execute(select_stmt)
        container_rows  = cursor.fetchall()

        cursor.close()
        connection.close()

        return container_rows

    @classmethod
    def sqlite_get_all_rows_by_session(cls, session_id):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task_container WHERE session_id=?"
        cursor = connection.cursor()
        cursor.execute(select_stmt, (session_id,))
        container_rows  = cursor.fetchall()

        cursor.close()
        connection.close()

        return container_rows

    @classmethod
    def postgres_save(cls, task_container):
        connection = get_postgres_connection()
        cursor = connection.cursor()
        if task_container._id:
            # if _id exists then it must have been stored in the db
            insert_container_stmt = "UPDATE task_container SET name=%s WHERE id=%s;"
            cursor.execute(insert_container_stmt, (task_container._name, task_container._id,))
        else:
            # if no _id then create new
            insert_container_stmt = "INSERT INTO task_container VALUES(DEFAULT,%s,%s) RETURNING id;"
            cursor.execute(insert_container_stmt, (task_container.session_id, task_container._name,))     
            task_container._id = cursor.fetchone()[0]


        if task_container._id:
            # Delete all existing relations for this object first
            delete_relation_stmt = "DELETE FROM task_container_rel_task WHERE container_id=%s;"
            cursor.execute(delete_relation_stmt, (task_container._id,))

            #insert all relations
            insert_container_relation_stmt = "INSERT INTO task_container_rel_task VALUES(%s,%s)"
            for task_id in task_container.task_ids:
                cursor.execute(insert_container_relation_stmt, (task_container._id, task_id))
            connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def postgres_delete_by_id(cls, _id):
        connection = get_postgres_connection()
        cursor = connection.cursor()
        delete_stmt = "DELETE FROM task_container WHERE id=%s"
        delete_relation_stmt = "DELETE FROM task_container_rel_task WHERE container_id=%s"
        cursor.execute(delete_stmt, (_id,))
        cursor.execute(delete_relation_stmt, (_id,))
        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def postgres_get_row_by_id(cls, _id):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task_container WHERE id=%s"
        cursor.execute(select_stmt, (_id,))
        container_row  = cursor.fetchone()

        cursor.close()
        connection.close()

        return container_row

    @classmethod
    def postgres_get_all_rows(cls):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task_container"
        cursor.execute(select_stmt)
        container_rows  = cursor.fetchall()

        cursor.close()
        connection.close()

        return container_rows

    @classmethod
    def postgres_get_all_rows_by_session(cls, session_id):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task_container WHERE session_id=%s"
        cursor.execute(select_stmt, (session_id,))
        container_rows  = cursor.fetchall()

        cursor.close()
        connection.close()

        return container_rows       

class TaskMapper:

    @classmethod
    def save(cls, task):
        """ Saves the task to a database,based on the path provided by Config 
        Args:
            task (Task) : the task instance to be saved to db 
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            cls.sqlite_save(task)
        elif db_type == 2:
            cls.postgres_save(task)

    @classmethod
    def get_rows_by_container_id(cls, container_id):
        """ Retrieve all task rows belonging to the container_id
        Args:
            container_id (int) : the container_id to match with the tasks
        Returns:
            list: list of task rows that belongs to the container_id
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_rows_by_container_id(container_id)
        elif db_type == 2:
            return cls.postgres_get_rows_by_container_id(container_id)

    @classmethod
    def get_by_id(cls, _id):
        """ Retrieve a row from the database where it matches the id
        Args:
            _id (int) : the id of the task row to get
        Returns:
            tuple: tuple of parameters of the row matching the id
        """

        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_by_id(_id)
        elif db_type == 2:
            return cls.postgres_get_by_id(_id)

    @classmethod
    def delete_by_id(cls, _id):
        """ Deletes the task in the database by id 
        Args:
            _id (int) : the id of the task to delete 
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            cls.sqlite_delete_by_id(_id)
        elif db_type == 2:
            cls.postgres_delete_by_id(_id)

    @classmethod
    def get_all(cls):
        """ Retrieve all rows of the task from the db, returns list
            Returns:
                list: list of all task rows in the db
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_all()
        elif db_type == 2:
            return cls.postgres_get_all()

    @classmethod
    def sqlite_get_by_id(cls, _id):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task WHERE id=?"
        cursor = connection.cursor()
        cursor.execute(select_stmt, (_id,))
        task_rows  = cursor.fetchone()

        cursor.close()
        connection.close()

        return task_rows

    @classmethod
    def sqlite_delete_by_id(cls, _id):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        delete_stmt = "DELETE FROM task WHERE id=?"
        cursor = connection.cursor()
        cursor.execute(delete_stmt, (_id,))
        connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def sqlite_get_all(cls):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task"
        cursor = connection.cursor()
        cursor.execute(select_stmt)
        task_rows  = cursor.fetchall()
        
        cursor.close()
        connection.close()

        return task_rows

    @classmethod
    def sqlite_save(cls, task):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        #if object has id then it has been stored before, use update
        if task._id:
            update_task_stmt = "UPDATE task SET name=?, detail=?, owner_id=? WHERE id=?"
            cursor.execute(update_task_stmt, (task._name, task.detail, task.owner_id, task._id))
        else:
            insert_task_stmt = "INSERT INTO task VALUES(NULL,?,?,?,?)"        
            cursor.execute(insert_task_stmt, (task.session_id, task._name, task.detail, task.owner_id))
            task._id = cursor.lastrowid
        connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def sqlite_get_rows_by_container_id(cls, container_id):
        task_rows = []
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        select_tasks_stmt = " SELECT A.* FROM task AS A INNER JOIN task_container_rel_task AS B INNER JOIN task_container AS C ON B.container_id=C.id AND A.id = B.task_id AND C.id=?;"
        cursor.execute(select_tasks_stmt, (container_id,))
        task_rows  = cursor.fetchall()

        cursor.close()
        connection.close()

        return task_rows

    @classmethod
    def postgres_save(cls, task):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        #if object has id then it has been stored before, use update
        if task._id:
            update_task_stmt = "UPDATE task SET name=%s, detail=%s, owner_id=%s WHERE id=%s"
            cursor.execute(update_task_stmt, (task._name, task.detail, task.owner_id, task._id))
        else:
            insert_task_stmt = "INSERT INTO task VALUES(DEFAULT,%s,%s,%s,%s) RETURNING id"        
            cursor.execute(insert_task_stmt, (task.session_id, task._name, task.detail, task.owner_id))
            task._id = cursor.fetchone()[0]
        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def postgres_get_rows_by_container_id(cls, container_id):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_tasks_stmt = "SELECT A.* FROM task AS A INNER JOIN task_container AS C ON C.id=%s INNER JOIN task_container_rel_task AS B ON B.container_id=C.id AND A.id = B.task_id;"
        cursor.execute(select_tasks_stmt, (container_id,))
        task_rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return task_rows

    @classmethod
    def postgres_get_by_id(cls, _id):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task WHERE id=%s"
        cursor.execute(select_stmt, (_id,))
        tasks_row  = cursor.fetchone()

        cursor.close()
        connection.close()

        return tasks_row

    @classmethod
    def postgres_delete_by_id(cls, _id):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        delete_stmt = "DELETE FROM task WHERE id=%s"
        cursor.execute(delete_stmt, (_id,))
        connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def postgres_get_all(cls):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM task"
        cursor.execute(select_stmt)
        task_rows  = cursor.fetchall()

        cursor.close()
        connection.close()

        return task_rows

class ConfigTaskMapper:

    @classmethod
    def save(cls, config_task):
        """ Saves the task config to a database,based on the path provided by Config 
        Args:
            config_task (ConfigTask) : the task config instance to be saved to db 
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            cls.sqlite_save(config_task)
        elif db_type == 2:
            cls.postgres_save(config_task)

    @classmethod
    def get_by_task_id(cls, task_id):
        """ Retrieve a row from the database where it matches the id
        Args:
            task_id (int) : get the config for the task_id
        Returns:
            tuple: tuple of parameters of the config row matching the id
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_by_task_id(task_id)
        elif db_type == 2:
            return cls.postgres_get_by_task_id(task_id)

    @classmethod
    def sqlite_save(cls, config_task):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        is_stored = False
        select_task_cfg_stmt = "SELECT * FROM task_config WHERE task_id=?"
        cursor.execute(select_task_cfg_stmt, (config_task.task_id,))
        cfg_rows = cursor.fetchall()

        for cur_cfg in cfg_rows:
            is_stored = True
            break

        if is_stored:
            # if _id exists then it must have been stored in the db
            insert_config_stmt = "UPDATE task_config SET color_id=? WHERE task_id=?;"
            cursor.execute(insert_config_stmt, (config_task.color_id, config_task.task_id))

        else:
            # if no _id then create new
            insert_config_stmt = "INSERT INTO task_config(task_id, color_id) VALUES(?,?);"
            cursor.execute(insert_config_stmt, (config_task.task_id, config_task.color_id))        


        connection.commit()
        
        cursor.close()
        connection.close()

    @classmethod
    def sqlite_get_by_task_id(cls, task_id):
        db_url = Config.get_db_url()

        connection = sqlite3.connect(db_url)
        cursor = connection.cursor()

        select_task_cfg_stmt = "SELECT * FROM task_config WHERE task_id=?"
        cursor.execute(select_task_cfg_stmt, (task_id,))


        cfg_rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return cfg_rows

    @classmethod
    def postgres_save(cls, config_task):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        is_stored = False
        select_task_cfg_stmt = "SELECT * FROM task_config WHERE task_id=%s"
        cursor.execute(select_task_cfg_stmt, (config_task.task_id,))
        cfg_rows = cursor.fetchall()

        for cur_cfg in cfg_rows:
            is_stored = True
            break

        if is_stored:
            # if _id exists then it must have been stored in the db
            insert_config_stmt = "UPDATE task_config SET color_id=%s WHERE task_id=%s;"
            cursor.execute(insert_config_stmt, (config_task.color_id, config_task.task_id))

        else:
            # if no _id then create new
            insert_config_stmt = "INSERT INTO task_config(task_id, color_id) VALUES(%s,%s);"
            cursor.execute(insert_config_stmt, (config_task.task_id, config_task.color_id))        

        connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def postgres_get_by_task_id(cls, task_id):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_task_cfg_stmt = "SELECT * FROM task_config WHERE task_id=%s"
        cursor.execute(select_task_cfg_stmt, (task_id,))

        cfg_rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return cfg_rows

class UserMapper:
    """ Mapper for task container, maps the class instance to a database """

    @classmethod
    def save(cls, user):
        """ Saves the task container to a database,based on the path provided by Config 
        Args:
            task_container (TasksContainer) : the container instance to be saved to db 
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            cls.sqlite_save(user)
        elif db_type == 2:
            cls.postgres_save(user)

    @classmethod
    def delete_by_id(cls, _id):
        """ Deletes the task container in the database by id 
        Args:
            _id (int) : the id of the container to delete 
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            cls.sqlite_delete_by_id(_id)
        elif db_type == 2:
            cls.postgres_delete_by_id(_id)

    @classmethod
    def get_row_by_id(cls, _id):
        """ Retrieve a row from the database where it matches the id
        Args:
            _id (int) : the id of the user row to get
        Returns:
            tuple: tuple of parameters of the row matching the id
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_row_by_id(_id)
        elif db_type == 2:
            return cls.postgres_get_row_by_id(_id)

    @classmethod
    def get_row_by_username(cls, username):
        """ Retrieve a row from the database where it matches the id
        Args:
            _id (int) : the id of the user row to get
        Returns:
            tuple: tuple of parameters of the row matching the id
        """
        db_type = Config.get_db_type()
        if db_type == 0:
            pass
        elif db_type == 1:
            return cls.sqlite_get_row_by_username(username)
        elif db_type == 2:
            return cls.postgres_get_row_by_username(username)

    @classmethod
    def get_all_rows(cls):
        pass

    @classmethod
    def postgres_save(cls, user):
        connection = get_postgres_connection()
        cursor = connection.cursor()
        if user._id:
            # if _id exists then it must have been stored in the db
            insert_user_stmt = "UPDATE users SET name=%s WHERE id=%s;"
            cursor.execute(insert_user_stmt, (user._name, user._id,))
        else:
            # if no _id then create new
            insert_user_stmt = "INSERT INTO users VALUES(DEFAULT,%s,%s,%s,%s) RETURNING id;"
            cursor.execute(insert_user_stmt, (user._name, user._password, user.email, user.is_validated))     
            user._id = cursor.fetchone()[0]


        if user._id:
            pass
            # Delete all existing relations for this object first
            delete_relation_stmt = "DELETE FROM user_rel_session WHERE user_id=%s;"
            cursor.execute(delete_relation_stmt, (user._id,))

            #insert all relations
            insert_session_relation_stmt = "INSERT INTO user_rel_session VALUES(%s,%s)"
            for session_id in user.session_ids:
                cursor.execute(insert_session_relation_stmt, (user._id, session_id))
            connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def postgres_get_row_by_id(cls, _id):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM users WHERE id=%s"
        cursor.execute(select_stmt, (_id,))
        user_row  = cursor.fetchone()

        cursor.close()
        connection.close()

        return user_row

    @classmethod
    def postgres_get_row_by_username(cls, username):
        connection = get_postgres_connection()
        cursor = connection.cursor()

        select_stmt = "SELECT * FROM users WHERE username=%s"
        cursor.execute(select_stmt, (username,))
        user_row  = cursor.fetchone()

        cursor.close()
        connection.close()

        return user_row

    @classmethod
    def postgres_delete_by_id(cls, id):
        pass

    @classmethod
    def sqlite_save(cls, user):
        pass

    @classmethod
    def sqlite_get_row_by_id(cls, _id):
        pass

    @classmethod
    def sqlite_get_row_by_username(cls, username):
        pass

    @classmethod
    def sqlite_delete_by_id(cls, id):
        pass