"""Server for Shepherd Tech Challenge."""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange, URL
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'shepherd' #needed for wtforms
Bootstrap(app) #needed for Flask-Bootstrap


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


@app.route('/')
def homepage():
    """View homepage."""
    
    response = requests.get('https://gist.githubusercontent.com/mmahalwy/1459564f99b7511350d766daf3564169/raw/1bfa12209c5e91ced717007a4448e4b812304b74/forms.json')
    forms_dict = response.json()

    applications_dict = {}

    for dict in forms_dict:
        path = dict['name'].replace(' ', '_').lower()
        applications_dict[dict['name']] = path

    return render_template("homepage.html",
                           applications_dict=applications_dict)



@app.route('/app_type/<application>', methods=['GET', 'POST'])
def app_type(application):
    """View application."""

    # not dynamic....
    company = CompanyApplication()
    employee = EmployeeApplication()
    auto = AutoApplication()

    if company.validate_on_submit(): 
        return 'form successfully submitted'

    return render_template('app_type.html', 
                            application=application, 
                            company=company, 
                            employee=employee, 
                            auto=auto)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)