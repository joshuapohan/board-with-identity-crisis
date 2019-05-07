"""
Module containing all the class / models used in the board application

Author : JPO

Todo:
    Use UUID to map between real object id and the id exposed to client side
    Add more configurations to ConfigTask
"""

import json
from flask_bcrypt import Bcrypt
from .models_mapper import TasksContainerMapper, TaskMapper, ConfigTaskMapper, UserMapper

class TasksContainer:
    """ Container class to hold list of Task instances

    Attributes:
        _id (int)                 : id of the instance
        session_id (int)          : session id in which this instance belongs to
        _name (str)               : name of the container
        task_ids (list of int)    : ids of the task contained
        my_tasks (list of Task)   : list of task instances within this container

    """

    def __init__(self, _id, session_id, _name):
        self._id = _id
        self.session_id = session_id
        self._name = _name
        self.task_ids = []
        self.my_tasks = []

    def save(self):
        """ Save the instance to the database, using the mapper class"""
        TasksContainerMapper.save(self)

    def add_task(self, *tasks):
        """ Add task instance to self list
        
        Args:
            *tasks: variable number of task instances to be added
        """
        for cur_task in tasks:
            self.task_ids.append(cur_task._id)
            self.my_tasks.append(cur_task)    

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        return self.to_json()

    def to_json(self):
        """
            Returns:
                string: JSON string with the format 
                        {
                            "_id": self._id,
                            "_name": self. _name,
                            "myTasks": self.my_tasks
                        }
        """
        client_obj = {
            "_id": self._id,
            "_name": self. _name,
            "myTasks": self.my_tasks
        }
        return json.dumps(client_obj, default=lambda o: o.__dict__)

    @classmethod
    def delete_by_id(cls, _id):
        """ Delete container from database
        
        Args:
            id: id of the container to be deleted

        """
        TasksContainerMapper.delete_by_id(self)

    @classmethod
    def get_by_id(cls, _id):
        """ Get container instance by id
        
        Args:
            id: id of the container to retrieve

        """
        container_instance = None

        container_instance = TasksContainer(*TasksContainerMapper.get_row_by_id(_id))
        task_rows = TaskMapper.get_rows_by_container_id(_id)
        for cur_row in task_rows:
            cur_task = Task(*cur_row)
            container_instance.add_task(cur_task)        

        return container_instance

    @classmethod
    def get_all(cls):
        """ Get all containers in the db """
        containers = []

        container_rows = TasksContainerMapper.get_all_rows()
        for cur_row in container_rows:
            container_instance = TasksContainer(*cur_row)
            task_rows = TaskMapper.get_rows_by_container_id(container_instance._id)
            for cur_row in task_rows:
                cur_task = Task(*cur_row)
                container_instance.add_task(cur_task)    
            containers.append(container_instance)        
        return containers

    @classmethod
    def get_all_by_session(cls, session_id):
        """ Get all containers  in the db by session id """
        containers = []

        container_rows = TasksContainerMapper.get_all_rows_by_session(session_id)

        for cur_row in container_rows:
            container_instance = TasksContainer(*cur_row)
            task_rows = TaskMapper.get_rows_by_container_id(container_instance._id)
            for cur_row in task_rows:
                cur_task = Task(*cur_row)
                container_instance.add_task(cur_task)    
            containers.append(container_instance)        
        return containers            

    def print_container(self):
        print("\n")
        print("Container " + self._name)
        print("Tasks : ")
        for cur_task in self.my_tasks:
            print(cur_task._name)

class Task:
    """ Task class, contains the information of the note/task that is contained in a container class
        relation with container is handled in the db using a relation table

    Attributes:
        _id (int)                 : id of the instance
        session_id (int)          : session id in which this instance belongs to
        _name (str)               : name of the task
        detail (str)              : detail of the task
        owner_id (int)            : id of the container instance that has this task (TO BE DELETED)

    """

    def __init__(self, _id, session_id, _name, detail, owner_id=None):
        self._id = _id
        self.session_id = session_id
        self._name = _name
        self.detail = detail
        self.owner_id = owner_id

    def __repr__(self):
        return self.to_json()

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        """
            Returns:
                dict: with the format 
                        {
                             _id = self._id
                             _name = self._name
                             detail = self.detail
                             owner_id = self.owner_id
                        }
        """
        return {
            '_id': self._id,
            'session_id': self.session_id,
            '_name': self._name,
            'detail': self.detail,
            'owner_id': self.owner_id,
        }        

    def to_json(self):
        """
            Returns:
                string: JSON string with the format 
                        {
                             _id = self._id
                             _name = self._name
                             detail = self.detail
                             owner_id = self.owner_id
                        }
        """
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def save(self):
        """ Save the instance to the database, using the mapper class"""
        TaskMapper.save(self)

    @classmethod
    def get_by_id(cls, _id):
        """ Get task instance by id
        
        Args:
            id: id of the task to retrieve

        """
        task_row = TaskMapper.get_by_id(_id)
        task_instance = Task(*task_row)
        return task_instance

    @classmethod
    def delete_by_id(cls, _id):
        """ Delete task  by id
        
        Args:
            id: id of the task to be deleted

        """
        TaskMapper.delete_by_id(_id)

    @classmethod
    def get_all(cls):
        """ Get all tasks in the db """
        tasks = []

        task_rows = TaskMapper.get_all()
        for cur_row in task_rows:
            task_instance = Task(*cur_row)    
            tasks.append(task_instance)        
        return tasks

class ConfigTask:
    """ ConfigTask class, contains the configuration parameters for the Task object

    Attributes:
        task_id (int)             : id of the task using this config
        color_id (int)            : color setting for the task using this config

    """

    def __init__(self, task_id, color_id=0):
        self.task_id = int(task_id)
        self.color_id = int(color_id)

    @classmethod
    def get_by_task_id(cls, task_id):
        """ Get task instance by the task id
        
        Args:
            id: id of the task to get the config of

        """	
        cfg_rows = ConfigTaskMapper.get_by_task_id(task_id)

        cfg_ins = None
        for cur_cfg in cfg_rows:
            cfg_ins = ConfigTask(*cur_cfg)
            break
        if cfg_ins == None:
            cfg_ins = ConfigTask(task_id)
        return cfg_ins

    def set_color_id(self, color_id):
        self.color_id = color_id

    def to_dict(self):
        """
            Returns:
                dict: dict with the format 
                        {
             			    task_id = self.task_id
                			color_id = self.color_id
                        }
        """
        return {
            'task_id': self.task_id,
            'color_id': self.color_id
        }

    def save(self):
        """ Save the instance to the database, using the mapper class"""
        ConfigTaskMapper.save(self)

class User():

    def __init__(self, name, password):
        bcrypt = Bcrypt()
        self._id = None
        self._name = name
        self._password = bcrypt.generate_password_hash(password).decode()
        self.session_ids = []

    def save(self):
        UserMapper.save(self)
