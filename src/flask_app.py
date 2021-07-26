import secrets
import multiprocessing
from flask import (
    Flask,
    render_template,
    url_for,
    request,
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
    return render_template("index.html", session=session)

@app.route('/execute', methods=("POST",))
def execute():
    flags = request.form["flags"].split('\n')
    code = request.form["code"]
    stdin = request.form["stdin"].split('\n')
    session = request.form["session"]

    if session not in sessions:
        return {
            "stdout": "",
            "stderr": "The session was invalid! You may need to reload your tab.",
        }

    result = {
        "stdout": None,
        "stderr": None,
    }

    sessions[session] = multiprocessing.Pool(2)
    
    result['stdout'] = '\n'.join(sessions[session].apply_async(skrun.run, (code, flags, stdin)).get())

    return result

@app.route("/kill", methods=("POST",))
def kill():
    session = request.form["session"]

    if sessions.get(session) is None:
        return ""

    sessions[session].terminate()
    return ""
