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

    def run(self):
        return self.stdout

