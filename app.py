from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['api_url'] = "//umich-schedule-api.herokuapp.com"
app.secret_key = 'test'
