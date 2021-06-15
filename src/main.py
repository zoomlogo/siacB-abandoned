import argparse
from interpreter import Interpreter

# Set argparser
parser = argparse.ArgumentParser()
parser.add_argument("file", help="The name of the file you want to execute.")
args = parser.parse_args()

# Check if the file exists and extension
if not args.file.endswith(".pL3"):
    print("File not recognized.")
    exit(2)

try:
    file = open(args.file, encoding='utf-8')
except FileNotFoundError:
    file = None

if file is None:
    print("File not found.")
    exit(1)


# Interpret them
interpreter = Interpreter(file.read())
interpreter.run()

