from skObject import OType, Object
from skToken import TType
from skInput import SmartInput
from skStack import SmartStack, Stack

import numpy as np
import time
import random
import datetime
from math import factorial

class Interpreter:
    def __init__(self, tokens, flags=[], inputs=[]):
        self.tokens = tokens
        self.log = "l" in flags

        self.smart_input = SmartInput(inputs)

        self.stack = SmartStack(self.smart_input)
        self.second_stack = Stack()
        self.pointer = 0

        self.register = Object(0, OType.NUMBER)

        self.function_location = {}
        self.function_call_stack = Stack()

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

    def types(self, *args):
        res = []
        for o in args:
            res.append(o.type)
        return res

    def do_stack_operation(self, stack, operation):
        if operation == '_':
            # Push length to stack
            obj = Object(len(stack), OType.NUMBER)
            stack.push(obj)
        elif operation == '.':
            # Duplicate the top of the stack
            top = stack.top()
            copy = top.copy()
            stack.push(copy)
        elif operation == ',':
            # Pop and discard the top of the stack
            stack.pop()
        elif operation == '⇅':
            # Reverse stack
            stack.stack = stack.stack[::-1]
        elif operation == '$':
            # Duplicate the top 2 elements (in order)
            popped = stack.pop()
            top = stack.top()
            copy = popped.copy()
            copy2 = top.copy()
            stack.push(popped)
            stack.push(copy)
            stack.push(copy2)
        elif operation == '\'':
            # Reverse the top 2 elements
            popped = stack.pop()
            popped2 = stack.pop()
            stack.push(popped2)
            stack.push(popped)

    def do_arity2_with_infix_support(self, operation, after):
        # Get 2 values to operate on
        popped = self.stack.pop()
        if after[1].type == TType.NUMBER:
            popped2 = Object(after[1].value, OType.NUMBER)
            popped, popped2 = popped2, popped
            self.skip(1)
        else:
            popped2 = self.stack.pop()
        value1 = popped.value
        value2 = popped2.value
        result = {
            "+": lambda x, y: x + y,  # Addition
            "-": lambda x, y: x - y,  # Subtraction
            "×": lambda x, y: x * y,  # Multiplication
            "÷": lambda x, y: x / y,  # Division
            "*": lambda x, y: x ** y, # Exponentiation
            "%": lambda x, y: x % y,  # Modulo
            "»": lambda x, y: x >> y, # Bitshift left
            "«": lambda x, y: x << y, # Bitshift right
        }[operation](value1, value2)
        self.stack.push(self.smart_input.objectify_from_instance(result))

    def do_arity2(self, operation):
        popped, popped2 = self.stack.pop(), self.stack.pop()
        # Perform operation
        value1, value2 = popped.value, popped2.value
        result = {
            "&": lambda x, y: x & y,  # Bitwise and
            "|": lambda x, y: x | y,  # Bitwise or
            "^": lambda x, y: x ^ y,  # Bitwise xor
            "∧": lambda x, y: 1 if x and y else 0,  # Logical and
            "∨": lambda x, y: 1 if x or y else 0,   # Logical or
        }[operation](value1, value2)
        self.stack.push(self.smart_input.objectify_from_instance(result))

    def do_arity1(self, operation):
        value = self.stack.pop().value
        result = {
            "~": lambda x: ~x,  # Bitwise not
            "¬": lambda x: 1 if not x else 0,  # Logical not
            "C": lambda x: 1 - x,  # Complement
            "D": lambda x: 1 / x,  # Divide by 1
            "²": lambda x: x ** 2, # Square
            "³": lambda x: x ** 3, # Cube
            "√": lambda x: x ** 1 / 2,  # Square root
            "∛": lambda x: x ** 1 / 3,  # Cube root
            "¼": lambda x: x / 4,  # Divide by 4
            "¾": lambda x: x * 3 / 4,  # Multiply by 3 / 4
        }[operation](value)
        self.stack.push(self.smart_input.objectify_from_instance(result))

    def execute_token(self, token, after, before):
        # Stack operations
        if token.type == TType.COMMAND and token.value in '_.,⇅$\'':
            self.do_stack_operation(self.stack, token.value)
        # 2nd stack operations
        elif token.value == 'ś':
            if after[1].value == 'P':
                # Push
                popped = self.stack.pop()
                self.second_stack.push(popped)
            elif after[1].value == 'p':
                # Pop
                popped = self.second_stack.pop()
                self.stack.push(popped)
            else:
                self.do_stack_operation(self.second_stack, after[1].value)
            self.skip(1)
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
            # Number
            obj = Object(token.value, OType.NUMBER)
            self.stack.push(obj)
        elif token.value == '`':
            # String
            obj = Object(after[1].value, OType.STRING)
            self.stack.push(obj)
            if after[2].value == '`':
                self.skip(2)
            else:
                self.skip(1)
        elif token.type == TType.COMMAND and token.value in '\\‛':
            # Push characters
            obj = Object(after[1].value, OType.STRING)
            self.stack.push(obj)
            self.skip(1)
        # Register operations
        elif token.value == '©':
            # Copy the top of the stack to the register
            self.register = self.stack.pop()
        elif token.value == '®':
            # Recall from the top of the registor
            self.stack.push(self.register)
        # Arity with 2 that supports infix
        elif token.type == TType.COMMAND and token.value in "+-×÷%*»«":
            self.do_arity2_with_infix_support(token.value, after)
        # Arity 2 operation without infix support
        elif token.type == TType.COMMAND and token.value in "&|^∧∨":
            self.do_arity2(token.value)
        # Arity 1 operators
        elif token.type == TType.COMMAND and token.value in "~¬CD²³√∛¼":
            self.do_arity1(token.value)
        elif token.value == '½':
            # Half or split in 2 equal parts
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                popped.value *= 0.5
                self.stack.push(popped)
            elif popped.type == OType.ARRAY:
                arrlis = np.array_split(popped.value, 2)
                for arr in arrlis:
                    self.stack.push(Object(arr, OType.ARRAY))
            elif popped.type == OType.STRING:
                half = int(len(popped.value) / 2)
                parts = [popped.value[:half], popped.value[half:]]
                for p in parts:
                    self.stack.push(Object(p, OType.STRING))
        elif token.value == 'M':
            # Other
            popped = self.stack.pop()
            if after[1].value == '!':
                # Factorial
                if popped.type == OType.NUMBER:
                    popped.value = factorial(popped.value)
                    self.stack.push(popped)
        # Check datatype
        elif token.value == '?':
            if after[1].value == 'A':
                # If array
                popped = self.stack.pop()
                obj = Object(1 if popped.type == OType.ARRAY else 0, OType.NUMBER)
                self.stack.push(popped)
                self.stack.push(obj)
                self.skip(1)
            elif after[1].value == 'S':
                # If string
                popped = self.stack.pop()
                obj = Object(1 if popped.type == OType.STRING else 0, OType.NUMBER)
                self.stack.push(popped)
                self.stack.push(obj)
                self.skip(1)
            elif after[1].value == 'N':
                # If number
                popped = self.stack.pop()
                obj = Object(1 if popped.type == OType.NUMBER else 0, OType.NUMBER)
                self.stack.push(popped)
                self.stack.push(obj)
                self.skip(1)
        # comparision operators
        elif token.value == '=':
            # Equality
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                if after[1].type == TType.NUMBER:
                    obj = Object(1 if popped.value == after[1].value else 0, OType.NUMBER)
                    self.stack.push(obj)
                    self.skip(1)
                else:
                    popped2 = self.stack.pop()
                    obj = Object(1 if popped.value == popped2.value else 0, OType.NUMBER)
                    self.stack.push(obj)
            elif popped.type == OType.ARRAY:
                popped2 = self.stack.pop()
                obj = Object(1 if np.array_equal(popped.value, popped2.value) else 0, OType.NUMBER)
                self.stack.push(obj)
            elif popped.type == OType.STRING:
                    popped2 = self.stack.pop()
                    obj = Object(1 if popped.value == popped2.value else 0, OType.NUMBER)
                    self.stack.push(obj)
        elif token.value == '≠':
            # !Equality
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                if after[1].type == TType.NUMBER:
                    obj = Object(1 if popped.value != after[1].value else 0, OType.NUMBER)
                    self.stack.push(obj)
                    self.skip(1)
                else:
                    popped2 = self.stack.pop()
                    obj = Object(1 if popped.value == popped2.value else 0, OType.NUMBER)
                    self.stack.push(obj)
            elif popped.type == OType.ARRAY:
                popped2 = self.stack.pop()
                obj = Object(1 if not np.array_equal(popped.value, popped2.value) else 0, OType.NUMBER)
                self.stack.push(obj)
            elif popped.type == OType.STRING:
                    popped2 = self.stack.pop()
                    obj = Object(1 if popped.value != popped2.value else 0, OType.NUMBER)
                    self.stack.push(obj)
        # functions
        elif token.value == 'λ':
            # function definion
            self.function_location[after[1].value] = self.pointer + 1
            self.skip(token.misc['end'])
        elif token.value == '@':
            # function call
            self.function_call_stack.push(self.pointer)
            self.pointer = self.function_location[after[1].value]
        elif token.value == ';':
            # function return
            self.pointer = self.function_call_stack.pop()

    def run(self):
        while self.pointer < len(self.tokens):
            before = self.tokens[:self.pointer]
            operation = self.tokens[self.pointer]
            after = self.tokens[self.pointer:]

            # Execute the current token
            self.execute_token(operation, after, before)

            # Log
            if self.log:
                self.log_file.write(f"\nPOINTER: {self.pointer}\n")
                self.log_file.write(f"  {operation = }\n")
                self.log_file.write(f"  {repr(self.stack)}\n")
                self.log_file.write(f"  Register = {self.register}\n")
                self.log_file.write(f"  FCall Stack = {self.function_call_stack}\n")
                self.log_file.write(f"  ForEach I = {self.foreach_index}\n")
                self.log_file.write(f"  ForEach Obj = {self.foreach_object}\n")

            self.pointer += 1
        return self.stdout

