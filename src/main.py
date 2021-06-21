import argparse
from interpreter import Interpreter
from sparser import Parser

# Set argparser
argparser = argparse.ArgumentParser()
argparser.add_argument("file", help="The name of the file you want to execute.")
argparser.add_argument("-l", "--log", action='store_true', help='Generate a log of each command')
args = argparser.parse_args()

try:
    file = open(args.file, encoding='utf-8')
    if args.log:
        log = open('log.txt', 'w+', encoding='utf-8')
    else:
        log = None
except FileNotFoundError:
    file = None
    log = None

if file is None:
    print("File not found.")
    exit(1)

# Parser into tokens
parser = Parser(file.read())
tokens = parser.parse()
if log is not None:
    for t in tokens:
        log.write(str(t) + '\n')

# Interpret them
interpreter = Interpreter(tokens, log)
result = interpreter.run()
if result is not None:
    print(result)

