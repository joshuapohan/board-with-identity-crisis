import os
from flask import Flask
from config import Config

app = Flask(__name__,static_folder=os.path.abspath("static/"))
Config.load_config()

import router
