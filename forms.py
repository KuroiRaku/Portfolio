


import __init__
import models
from __init__ import db


from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, SelectField, ValidationError, StringField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired, Email, DataRequired, Length, EqualTo, URL


class ProjectForm(FlaskForm):
    title= TextField("Title", validators=[InputRequired()])

    website = StringField('Website', validators=[InputRequired(), URL(False, "please enter URL")])
    github_url = StringField('Github url', validators=[InputRequired(), URL(False, "please enter URL")])

    description = StringField('Description', validators=[InputRequired()])
    long_desc = StringField('Long Description', validators=[InputRequired()])

    is_game = BooleanField('IsGameProject')
    image = FileField('Image', validators=[FileRequired("PLEASE")])
    submit = SubmitField('Add New Project')

class TestForm(FlaskForm):
    name= TextField("Title", validators=[InputRequired()])
    submit = SubmitField('Add New Project')
