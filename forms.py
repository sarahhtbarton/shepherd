from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange, URL

app = Flask(__name__)

class CompanyApplication(FlaskForm):
    company_name = StringField('What is the Company Name?', validators=[InputRequired()])
    ceo = StringField('What is the name of the CEO?', validators=[InputRequired()])
    website = StringField('Company website?', validators=[URL()])
    # address = StringField('Address') #just a header
        # address1 = StringField('Address', validators=[InputRequired()])
        # address2 = StringField('Address 2')
        # city = StringField('City')
    is_california_relevant = BooleanField('Will the contractor perform any work in California?')
    total_compensation = DecimalField('What is the total compensation of all your workers?', validators=[InputRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

class EmployeeApplication(FlaskForm):
    applicant_name = StringField('Applicant name', validators=[InputRequired()])
    applicant_title = StringField('Applicant title', validators=[InputRequired()]) 
    submit = SubmitField('Submit')

class AutoApplication(FlaskForm):
    vin = StringField('VIN', validators=[InputRequired()])
    make = SelectField('Make', choices=['Honda', 'Toyota', 'BMW', 'Ford', 'Dodge'], validators=[InputRequired()])
    submit = SubmitField('Submit')
