"""
Routes and views for the flask application.
"""

from flask import request,redirect

import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from Eden_final_project.models.LocalDataBaseRoutines import create_LocalDatabaseServiceRoutines
from flask import flash
import matplotlib.pyplot as pltfrom matplotlib.figure import Figure
import base64from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


from Eden_final_project.models.forms import ExpandForm
from Eden_final_project.models.forms import CollapseForm
from datetime import datetime
from flask import render_template
from Eden_final_project import app
from Eden_final_project.models.forms import LoginFormStructure 
from Eden_final_project.models.forms import UserRegistrationFormStructure 
from Eden_final_project.models.forms import QueryForm

from os import path
import io

from flask_bootstrap import Bootstrap

app.config['SECRET_KEY'] = 'The first argument to the field'

db_Functions = create_LocalDatabaseServiceRoutines() 

bootstrap = Bootstrap(app)

# this is the route to the "home" page
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().day
    )

# this is the route to the "contact" page
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Eden Melzer',
        year=datetime.now().year,
    )

# this is the route to the "about" page
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

# this is the route to the "data" page
@app.route('/data')
def data():
    """Renders the data page."""
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='Your application description page.',
       img_accident1 = '/static/imgs/accident1.jpg',

    )

# inside the data page, there is a link to an accident dataset page
@app.route('/data/accident' , methods = ['GET' , 'POST'])
def accident():
    """Renders the accident page."""
    print("Accident")

    
    form1 = ExpandForm() # sets form1 to point to the class "ExpandFrom()" which loads the dataset as a table
    form2 = CollapseForm() # sets form2 to point to the class "CollapseFrom()" which closes the dataset
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/shortdataset.csv')) # reads the dataset into df
    raw_data_table = ''

    # if the "Expand" or "Collapse" buttons are pressed, then activates the request:
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

# this is the route to the "register" page
@app.route('/register', methods=['GET', 'POST'])
def Register():
    """Renders the register page."""
    form = UserRegistrationFormStructure(request.form) # sets form to the class "UserRegistrationFormStructure" which provides info needed for registration 

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            flash('You can now go to the "login" page and log in')
        else:
            flash('Error: User with this Username already exists ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# this is the route to the "login" page
@app.route('/login', methods=['GET', 'POST'])
def Login():
    """Renders the login page."""
    form = LoginFormStructure(request.form) # sets form to the class "LoginFormStructure" which lets you enter your Username and Password to log in

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            return redirect('Query')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# this is the route to the "query" page
@app.route('/Query' , methods = ['GET' , 'POST'])
def Query():
    """Renders the query page."""
    form1 = QueryForm() # sets form1 to the class "QueryForm" which lets you select the accident's severity level
    chart = 'static/imgs/speed-limit-road-signs-vector-25456570.jpg'

    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/shortdataset.csv')) # reads the dataset into df

    if request.method == 'POST':
        Severity = int(form1.Severity.data) # sets the "Severity" variable to the level selected by the user
        df = df[["Speed_limit", "Accident_Severity"]] # filters the dataset to two fields only: "Speed_limit" and "Accident_Severity"
        df = df[df["Accident_Severity"]== Severity] # filters out all entries of severity different from the requested one
        df = df.drop("Accident_Severity", 1) # removes the "Accident_Severity" field, leaving out only the "Speed_limit" field
        df = df.groupby("Speed_limit").size() # counts the number of entries of any given speed limit
        df = pd.DataFrame(df) 
        # presents the results as a bar chart:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        df.plot(kind = "bar", ax = ax) 
        chart = plot_to_img(fig)

    
    return render_template(
        'Query.html',
        form1 = form1,
        chart = chart

    )

def plot_to_img(fig):    pngImage = io.BytesIO()    FigureCanvas(fig).print_png(pngImage)    pngImageB64String = "data:image/png;base64,"    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')    return pngImageB64String
