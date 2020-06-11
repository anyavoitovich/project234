from habrclone import App
from flask import render_template, flash, redirect, url_for
from habrclone.forms import LoginForm

@App.route('/')
@App.route('/index')
def index():
    return render_template('index.html')



@App.route('/sign-in', methods=['GET', 'POST'])
def login():
    form =LoginForm()
    if form.validate_on_submit():
        flash(f'пользователь{form.username.data} вошёл. Поле "запомнить"{form.remember_me.data}.')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)