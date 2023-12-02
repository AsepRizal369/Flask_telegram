from apps import app
from settings.base import Config
from apps.urls import api
import logging
from flask import render_template, request
from apps.model import Model
from jinja2 import StrictUndefined


# Set up logging
logging.basicConfig(level=logging.ERROR)

# app.jinja_env.undefined = StrictUndefined
api.init_app(app)

model_instance = Model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = {}
    data['fname']   = request.form['fname']
    data['lname']   = request.form['lname']
    data['pet']     = request.form['pets'] 
    
    result = model_instance.saveGlobal('students',data)

    return render_template('success.html', data=result['data'])

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port = 5000)
