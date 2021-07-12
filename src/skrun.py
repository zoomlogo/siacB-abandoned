import argparse
from skParse import Parser
from skInterpreter import Interpreter

def run(code, flags=[], inputs=[]):
    parser = Parser(code)
    parser.remove_whitespace()
    tokens = parser.parse()

    interpreter = Interpreter(tokens, flags, inputs)
    return interpreter.run()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="The name of the file you want to execute.")
    argparser.add_argument("-l", "--log", action='store_true', help='Generate a log of each command')
    args = argparser.parse_args()

    try:
        file = open(args.file, encoding='utf-8')
    except FileNotFoundError:
        file = None

    if file is None:
        print("File not found.")
        exit(1)

    flags = []
    if args.log:
        flags.append("l")

    code = file.read()
    for s in run(code, flags):
        print(s)
