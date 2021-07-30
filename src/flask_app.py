import secrets
import multiprocessing
try:
    import git
except:
    pass
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
        "stdout": '',
        "stderr": '',
    }

    if session in terminated:
        terminated.remove(session)
        result["stderr"] = "session terminated"

    sessions[session] = multiprocessing.Pool(2)
    
    try:
        async_run = sessions[session].apply_async(skrun.run, (code, flags, stdin))
        result['stdout'] = '\n'.join(async_run.get())
    except Exception as e:
        result['stderr'] = str(e)
    finally:
        return result

@app.route("/kill", methods=("POST",))
def kill():
    session = request.form["session"]

    if sessions.get(session) is None:
        return ""

    sessions[session].terminate()
    terminated.add(session)
    return ""

@app.route("/update", methods=("GET", "POST"))
def update():
    if request.method == "POST":
        repo = git.Repo("~/51AC8")
        origin = repo.remotes.origin
        with repo.config_writer() as git_config:
            git_config.set_value(
                "user", "email", "64531844+PyGamer0@users.noreply.github.com"
            )
            git_config.set_value("user", "name", "PyGamer0")
        origin.pull()
        return "Updated PythonAnywhere successfully", 200
    else:
        return "Wrong event type", 400
