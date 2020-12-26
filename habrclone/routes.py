from habrclone import App, db
from habrclone.models import User, New
from flask import render_template, flash, redirect, url_for, request
from habrclone.forms import LoginForm, RegistrationForm, AccountUpdateForm, NewsForm
from flask_login import current_user, login_user, logout_user, login_required
import os
from PIL import Image


@App.route('/')
@App.route('/index')
def index():
    return render_template('index.html')


@App.route('/sign_in', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя и/или пароль!', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@App.route('/sign_out')
def logout():
    logout_user()

    return redirect(url_for('index'))


@App.route('/sign_up', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Регистрация')


def save_picture(form_picture):
    f_name, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = f_name + f_name
    pic_path = os.path.join(App.root_path, 'static/img/avatar', pic_fn)

    resize_image = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(resize_image)

    image.save(pic_path)
    return pic_fn


@App.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Обновлено!', 'info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    form.email.data = current_user.email
    avatar = url_for('static', filename='img/avatars/' + current_user.avatar)
    news = New.query.filter_by(user_id=current_user.id)
    return render_template('account.html', avatar=avatar, form=form, news=news)


@App.route('/about')
def about_page():
    return render_template('about.html', title='О нас')


@App.route('/blog', methods=['GET', 'POST'])
def news():
    form = NewsForm()
    if form.validate_on_submit():
        new = New(article=current_user.username, body=form.body.data, user_id=current_user.id )
        db.session.add(new)
        db.session.commit()
        flash('Новость опубликована!', 'success')
        return redirect(url_for('news'))
    news = New.query.all()
    return render_template('blog.html', title='Блог', form=form, news=news)