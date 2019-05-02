import json

class Config:
    """
        Stores the configuration for the board application,
        currently loaded from json config file

        Class Attributes:
            _config_path (str)  : path to the config file
            _db_url (str)       : url to the database to connect to
            _db_type (int)      : id to determine the type of database to use

        Note:
            _db_type : 0    undefined
                       1    sqlite
                       2    postgres 
    """
    
    _config_path = "./config.json"
    _db_url = "default"
    _db_type = 0
    _user = "default"
    _password = "default"
    _host = "127.0.0.1"
    _port = "5432"
    _database = "kanbandb"
    
    @classmethod
    def _set_config_path(cls, config_path):
        cls._config_path = config_path

    @classmethod
    def _load_config(cls):
        cfg_file = open(cls._config_path, 'r')
        cfg_str = cfg_file.read()
        cfg_file.close()
        cfg_json = json.loads(cfg_str)
        if cfg_json:
            cls._db_type = cfg_json["db_type"]
            cls._db_url = cfg_json["db_url"]
            if cls._db_type == 2:
                cls._user = cfg_json["user"]
                cls._password = cfg_json["password"]
                cls._host = cfg_json["host"]
                cls._port = cfg_json["port"]
                cls._database = cfg_json["database"]

    @classmethod
    def load_config_from_path(cls, config_path="./config.json"):
        cls._set_config_path(config_path)
        cls._load_config()

    @classmethod
    def set_db_url(cls, db_url):
        _db_url = db_url

    @classmethod
    def set_db_type(cls, db_type):
        _db_type = db_type

    @classmethod
    def get_db_type(cls):
        return cls._db_type

    @classmethod
    def get_db_url(cls):
        return cls._db_url

    @classmethod
    def get_db_user(cls):
        return cls._user

    @classmethod
    def get_db_password(cls):
        return cls._password

    @classmethod
    def get_db_host(cls):
        return cls._host

    @classmethod
    def get_db_port(cls):
        return cls._port
        
    @classmethod
    def get_db_database(cls):
        return cls._database
    

