import secrets
from flask import (
    Flask,
    render_template,
)

import skrun

import os
import shutil
import sys

app = Flask(__name__)

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/.."
sys.path.insert(1, THIS_FOLDER)

shutil.rmtree("sessions", ignore_errors=True)
os.system("mkdir sessions")

sessions = {}
terminated = set()

@app.route('/', methods=("POST", "GET"))
def home():
    session = secrets.token_hex(64)
    sessions[session] = None
    return render_template("index.html")

