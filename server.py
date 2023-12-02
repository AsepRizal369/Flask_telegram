from flask import Flask, render_template, request
import names
from apps.model import Model

app = Flask(__name__)

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
  app.run(debug=True)





