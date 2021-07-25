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

    shutil.rmtree(f"sessions/{session}", ignore_errors=True)
    os.mkdir(f"sessions/{session}")

    with open(f"sessions/{session}/.stderr", "w", encoding='utf-8') as stderr:
        manager = multiprocessing.Manager()
        ret = manager.dict()

        time = 15
        if "T" in flags:
            time = 60
        ret[1] = ""
        ret[2] = ""

        sessions[session] = multiprocessing.Process(
            target=skrun,
            args=(code, flags, stdin),
        )
        sessions[session].start()
        sessions[session].join(time)

        if session in terminated:
            terminated.remove(session)
            ret[2] += "\nSession terminated upon user request"
        if sessions[session].is_alive():
            sessions[session].kill()
            if 2 in ret:
                ret[2] += "\n" + f"Code timed out after {time} seconds"
        stderr.write(ret[2])
        print(ret[1])

    result = {
        "stdout": None,
        "stderr": None,
    }
    return result

