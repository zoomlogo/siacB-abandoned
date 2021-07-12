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

    def execute_token(self, token, after, before):
        ...

    def run(self):
        while self.pointer < len(self.tokens):
            self.pointer += 1
        return self.stdout

