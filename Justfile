default:
    @just --list

run:
    python src/skrun.py src/test.sk --log

parse:
    python src/skParse.py
