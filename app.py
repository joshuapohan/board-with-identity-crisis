import os
from flask import Flask
from config import Config

app = Flask(__name__,static_folder=os.path.abspath("static/"))
app.secret_key = os.environ.get('SECRET_KEY') or 'test1234'
Config.load_config()

import router
