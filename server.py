"""Server for Shepherd Tech Challenge."""

from flask import Flask, render_template
import requests #first have to pip3 install requests
import os #use if decide to try to create jinja templates

app = Flask(__name__)


@app.route('/')
def homepage():
    """View homepage."""
    
    response = requests.get('https://gist.githubusercontent.com/mmahalwy/1459564f99b7511350d766daf3564169/raw/1bfa12209c5e91ced717007a4448e4b812304b74/forms.json')
    forms_dict = response.json() #from json to python dictionary... well actually, list.

    application_list = []

    for dict in forms_dict:
        application_list.append(dict['name'])

        filepath = os.path.join('/home/hackbright/src/Shepard/templates', f"{dict['name']}.html")
        file_obj = open(filepath, 'w')
        file_obj.write('test')
        file_obj.close()

    return render_template("homepage.html",
                           application_list=application_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)