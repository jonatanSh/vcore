"""
Each module has a main function that runs everything
"""
from flask import Flask
from vcore.api.core import run

app = Flask(__name__)

run(app)  # run the flask app
