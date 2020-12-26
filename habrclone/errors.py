from flask import render_template
from habrclone import App, db

@App.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@App.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500