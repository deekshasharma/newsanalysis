from flask import Flask 
app = Flask('application')
from application import views 
from application import urls
from flask import render_template

