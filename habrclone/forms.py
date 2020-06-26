from flask_wtf import FlaskForm
from flask_wtf.file import FileField, file_allowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from habrclone.models import User
from flask_login import current_user


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя/Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('запомнить меня')
    submit = SubmitField('войти')


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired()])
    password2 = StringField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Используйте другое имя!')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Используйте другой Email!')




class AccountUpdateForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    picture = FileField(validators=[file_allowed(['jpg', 'png'])])
    email = StringField(validators=[DataRequired()])
    submit = SubmitField('обновить')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                 raise ValidationError('Используйте другое имя!')

    def validate_email(self, email):
        if email.data !=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                    raise ValidationError('Используйте другой Email!')