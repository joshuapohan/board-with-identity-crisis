import os, sys
from flask import Flask
from config import Config

app = Flask(__name__,static_folder='static')
Config.load_config_from_path()

import router