import secrets
from flask import (
    Flask,
)

import skrun

print(skrun.run("C", [], ["5"]))

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"
