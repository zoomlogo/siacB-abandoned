import secrets
from flask import (
    Flask,
)

import skrun


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"
