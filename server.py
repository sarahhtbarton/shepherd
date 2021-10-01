"""Server for Shepherd Tech Challenge."""

from flask import Flask, render_template, request, redirect, json, jsonify, flash, url_for
from forms import CompanyApplication, EmployeeApplication, AutoApplication
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'shepherd'
Bootstrap(app)


response = requests.get('https://gist.githubusercontent.com/mmahalwy/1459564f99b7511350d766daf3564169/raw/1bfa12209c5e91ced717007a4448e4b812304b74/forms.json')
forms_dict = response.json()


@app.route('/')
def homepage():
    """View homepage."""

    applications_dict = {}

    for dict in forms_dict:
        applications_dict[dict['name']] = dict['name'].replace(' ', '_').lower()

    return render_template("homepage.html",
                           applications_dict=applications_dict)


@app.route('/type/<application>', methods=['GET', 'POST'])
def type(application):
    """View application."""
    
    shep_cookie = request.cookies.get('shep_cookie') # to set cookie in browser with javascript: document.cookie = "shep_cookie=shepherd"

    return render_template('type.html',
                            application=application, 
                            forms_dict=forms_dict,
                            shep_cookie=shep_cookie) 


@app.route('/submit/<application>', methods=['GET', 'POST'])
def submit(application):
    """Submit application"""

    """ 
    Pseudocode:
    # Get response data from form
    # Combine the key:value pairs from forms.json, and json results
    # Post json to database w/user auth (Save in results.json file)
    """

    if request.method == 'POST':
        flash('You successfully submited your form. If you need to make edits, you can do so below and resubmit')
        
    return redirect(url_for('edit', application=application))


@app.route('/edit/<application>', methods=['GET', 'POST'])
def edit(application):
    """Edit application"""

    forms_json = open('static/results.json').read()
    forms_dict = json.loads(forms_json)

    shep_cookie = request.cookies.get('shep_cookie')

    return render_template('type.html',
                            application=application, 
                            forms_dict=forms_dict,
                            shep_cookie=shep_cookie)














#below can be ignored. Uses WTForms. Left in to show another approach 


@app.route('/company_application', methods=['GET', 'POST'])
def company_application():
    """View company application."""

    company = CompanyApplication()

    company_name = company.company_name.data
    ceo = company.ceo.data
    website = company.website.data
    address1 = company.address1.data
    address2 = company.address2.data
    city = company.city.data
    is_california_relevant = company.is_california_relevant.data
    total_compensation = company.total_compensation.data

    company_results = {
        'company_name': company_name,
        'ceo': ceo,
        'website' : website,
        'address1' : address1,
        'address2' : address2,
        'city' : city,
        'is_california_relevant' : is_california_relevant,
        "total_compensation" : total_compensation
    }

    if company.validate_on_submit():
        with open("/home/hackbright/src/Shepard/static/company_results.json",'w') as j:
            json.dump(company_results, j)
            return redirect('/success')

    return render_template('company_application.html', 
                            company=company)


@app.route('/employee_application', methods=['GET', 'POST'])
def employee_application():
    """View employee application."""

    employee = EmployeeApplication()

    applicant_name = employee.applicant_name.data
    applicant_title = employee.applicant_title.data

    employee_results = {
        'applicant_name' : applicant_name,
        'applicant_title' : applicant_title
    }

    if employee.validate_on_submit():
        with open("/home/hackbright/src/Shepard/static/employee_results.json",'w') as j:
            json.dump(employee_results, j)
            return redirect('/success')

    return render_template('employee_application.html', 
                            employee=employee)


@app.route('/auto_application', methods=['GET', 'POST'])
def auto_application():
    """View auto application."""

    auto = AutoApplication()

    vin = auto.vin.data
    make = auto.make.data

    auto_results = {
        'vin' : vin,
        'make' : make
    }

    if auto.validate_on_submit():
        with open("/home/hackbright/src/Shepard/static/auto_results.json",'w') as j:
            json.dump(auto_results, j)
            return redirect('/success')

    return render_template('auto_application.html', 
                            auto=auto)


@app.route('/success')
def success():
    """View successfully submitted application"""

    return render_template('success.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)