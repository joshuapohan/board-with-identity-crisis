import os, sys
from flask import Flask
from config import Config

app = Flask(__name__)
Config.load_config()

import router
