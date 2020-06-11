from flask import Flask
from config import Config

App = Flask(__name__)
App.config.from_object(Config)
from habrclone import routes