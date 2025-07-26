from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    submit = SubmitField('Roʻyxatdan o‘tish')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password')
    submit = SubmitField('Kirish')

class ProductForm(FlaskForm):
    title = StringField('Nomi', validators=[DataRequired()])
    description = TextAreaField('Tavsifi')
    price = FloatField('Narxi')
    image = FileField('Rasm', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    category = SelectField('Kategoriya', coerce=int)
    submit = SubmitField('Qo‘shish')
