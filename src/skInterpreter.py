from skObject import OType, Object
from skToken import TType
from skInput import SmartInput
from skStack import SmartStack, Stack

import numpy as np
import time
import random
import datetime

class Interpreter:
    def __init__(self, tokens, flags=[], inputs=[]):
        self.tokens = tokens
        self.log = "l" in flags

        self.smart_input = SmartInput(inputs)

        self.stack = SmartStack(self.smart_input)
        self.pointer = 0

        self.registor = Object(0, OType.NUMBER)

        self.function_call = Stack()

        self.foreach_index = Stack()
        self.foreach_object = Stack()

        self.stdout = []

        self.log_file = open('log.txt', 'w+', encoding="utf-8") if self.log else None
        if self.log:
            self.log_file.write("---------TOKENS---------\n")
            for t in tokens:
                self.log_file.write(repr(t) + "\n")
            self.log_file.write("----------RUNNING--------\n")

    def skip(self, amt):
        # Skip (add amt to the pointer)
        self.pointer += amt

    def execute_token(self, token, after, before):
        # Stack operations
        if token.value == '_':
            # Push length of stack
            obj = Object(
                len(self.stack),
                OType.NUMBER
            )
            self.stack.push(obj)
        elif token.value == ':':
            # Duplicate the top of the stack
            popped = self.stack.pop()
            copy = popped.copy()
            self.stack.push(popped)
            self.stack.push(copy)
        elif token.value == ',':
            # Pop and discard the top of the stack
            self.stack.pop()
        elif token.value == '⇅':
            # Reverse stack
            self.stack.stack = self.stack.stack[::-1]
        elif token.value == '$':
            # Duplicate the top 2 elements (in order)
            popped = self.stack.pop()
            popped2 = self.stack.pop()
            copy = popped.copy()
            copy2 = popped2.copy()
            self.stack.push(popped)
            self.stack.push(popped2)
            self.stack.push(copy)
            self.stack.push(copy2)
        elif token.value == '\'':
            # Reverse the top 2 elements
            popped = self.stack.pop()
            popped2 = self.stack.pop()
            self.stack.push(popped2)
            self.stack.push(popped)
        # I/O
        elif token.value == 'i':
            # Explicit input
            obj = self.smart_input.input()
            self.stack.push(obj)
        elif token.value == 't':
            # Pop and print (append to stdout) the top of the stack
            if not self.stack.is_empty():
                self.stdout.append(self.stack.pop().value)
        # Constants
        elif token.type == TType.NUMBER:
            obj = Object(token.value, OType.NUMBER)
            self.stack.push(obj)

    def run(self):
        while self.pointer < len(self.tokens):
            # Execute the current token
            before = self.tokens[:self.pointer]
            operation = self.tokens[self.pointer]
            after = self.tokens[self.pointer:]
            self.execute_token(operation, after, before)

            self.pointer += 1
        return self.stdout

