from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired



# class in charge of the "Expand" button
class ExpandForm(FlaskForm):
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"

# class in charge of the "Collapse" button
class CollapseForm(FlaskForm):
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"
    
# class holding the variables for a user's login
class LoginFormStructure(FlaskForm):
    username   = StringField('Username:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

# class holding the variables for a user registration
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('Username:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

# class holding the variables for the query's selection field
class QueryForm(FlaskForm):
    Severity   = SelectField('Enter the accident severity level:  ' , validators = [DataRequired()], choices = [('3', 'high'), ('2', 'medium'), ('1', 'low')])
    submit = SubmitField('Submit')


