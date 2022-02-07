from email import message
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length


class StudentRegisterForm(FlaskForm):
    first_name = StringField('Imię', validators=[InputRequired(message='Imię jest wymagane!'), Length(min=3, max=45, message='Imię powinno mieć od 3 do 45 znaków')])
    last_name = StringField('Nazwisko', validators=[InputRequired(message='Nazwisko jest wymagane!'), Length(min=3, max=45, message='Nazwisko powinno mieć od 3 do 45 znaków')])
    password = PasswordField('Hasło', validators=[InputRequired(message='Hasło jest wymagane!'), Length(min=8, max=45, message='Hasło powinno mieć od 8 do 45 znaków')])
    faculty = SelectField('Wydział', choices=[])