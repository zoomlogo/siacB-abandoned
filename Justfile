default:
    @just --list

run:
    python src/skrun.py src/test.sk --log

parse:
    python src/skParse.py

token:
    python src/skToken.py

object:
    python src/skObject.py

stack:
    python src/skStack.py

input:
    python src/skInput.py
