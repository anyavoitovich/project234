from habrclone import App
from flask import render_template

@App.route('/')
@App.route('/index')
def index():
    return render_template('index.html')