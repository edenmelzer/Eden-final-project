"""
Routes and views for the flask application.
"""

from flask import request

import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from Eden_final_project.models.LocalDataBaseRoutines import create_LocalDatabaseServiceRoutines
from flask import flash

from Eden_final_project.models.forms import ExpandForm
from Eden_final_project.models.forms import CollapseForm
from datetime import datetime
from flask import render_template
from Eden_final_project import app
from Eden_final_project.models.forms import LoginFormStructure 
from Eden_final_project.models.forms import UserRegistrationFormStructure 

app.config['SECRET_KEY'] = 'The first argument to the field'

db_Functions = create_LocalDatabaseServiceRoutines() 

from os import path
import io

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    df = db_Functions.ReadCSVUsersDB()
    raw_data_table = df.to_html(classes = 'table table-hover')


    return render_template(
        'about.html',
        title='About',
        raw_data_table  = raw_data_table ,
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/data')
def data():
    """Renders the about page."""
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='Your application description page.',
       img_accident1 = '/static/imgs/accident1.jpg',

    )

@app.route('/data/accident' , methods = ['GET' , 'POST'])
def accident():

    print("Accident")

    """Renders the about page."""
    form1 = ExpandForm()
    form2 = CollapseForm()
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/shortdataset.csv'))
    raw_data_table = ''

    if request.method == 'POST':
        if request.form['action'] == 'Expand' and form1.validate_on_submit():
            raw_data_table = df.to_html(classes = 'table table-hover')
        if request.form['action'] == 'Collapse' and form2.validate_on_submit():
            raw_data_table = ''

    

    return render_template(
        'accident.html',
        title='Accident',
        year=datetime.now().year,
        message='Accident dataset page.',
        img_accident1 = '/static/imgs/accident1.jpg',
        raw_data_table = raw_data_table,
        form1 = form1,
        form2 = form2
    )

@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )