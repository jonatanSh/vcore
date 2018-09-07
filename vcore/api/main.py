"""
Each module has a main function that runs everything
"""
try:
    from __init__ import *
except ImportError:
    from .__init__ import *

from flask import Flask
from vcore.api.core import run

app = Flask(__name__)

run(app)  # run the flask app
