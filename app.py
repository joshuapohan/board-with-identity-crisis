import os, sys
from flask import Flask
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,static_folder=os.path.abspath("static/"))
Config.load_config()

import router
