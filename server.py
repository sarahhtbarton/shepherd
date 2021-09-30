"""Server for Shepherd Tech Challenge."""

from flask import Flask, render_template
from forms import CompanyApplication, EmployeeApplication, AutoApplication
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange, URL
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shepherd' #needed for wtforms
Bootstrap(app) #needed for Flask-Bootstrap

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


@app.route('/type/<application>', methods=['GET', 'POST'])
def type(application):
    """View application."""

    response = requests.get('https://gist.githubusercontent.com/mmahalwy/1459564f99b7511350d766daf3564169/raw/1bfa12209c5e91ced717007a4448e4b812304b74/forms.json')
    forms_dict = response.json()

    return render_template('type.html',
                            application=application, 
                            forms_dict=forms_dict)

@app.route('/success')
def success():
    """View successfully submitted application"""

    return render_template('success.html')


@app.route('/company_application', methods=['GET', 'POST'])
def company_application():
    """View company application."""

    company = CompanyApplication()

    if company.validate_on_submit(): 
        return 'form successfully submitted'
        # return redirect(url_for("success"))

    return render_template('company_application.html', 
                            company=company)


@app.route('/employee_application', methods=['GET', 'POST'])
def employee_application():
    """View employee application."""

    employee = EmployeeApplication()

    if employee.validate_on_submit(): 
        return 'form successfully submitted'
        # return redirect(url_for("success"))

    return render_template('employee_application.html', 
                            employee=employee)


@app.route('/auto_application', methods=['GET', 'POST'])
def auto_application():
    """View auto application."""

    auto = AutoApplication()

    if auto.validate_on_submit(): 
        return 'form successfully submitted'
        # return redirect(url_for("success"))

    return render_template('auto_application.html', 
                            auto=auto)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)