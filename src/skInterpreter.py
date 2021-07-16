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
        elif token.value == '\\':
            # Push next character
            obj = Object(after[1].value, OType.STRING)
            self.stack.push(obj)
            self.skip(1)
        elif token.value == '‛':
            # Push next 2 characters
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
        # Arithmetic oprations
        elif token.value == '+':
            # Add
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                if after[1].type == TType.NUMBER:
                    popped.value += after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value += popped.value
            elif popped.type == OType.STRING:
                self.stack.top().value += popped.value
        elif token.value == '-':
            # Subtract
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                if after[1].type == TType.NUMBER:
                    popped.value -= after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value -= popped.value
        elif token.value == '×':
            # Multiply
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                if after[1].type == TType.NUMBER:
                    popped.value *= after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value *= popped.value
            elif popped.type == OType.STRING:
                self.stack.top().value *= popped.value
        elif token.value == '÷':
            # Divide
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                if after[1].type == TType.NUMBER:
                    popped.value /= after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value /= popped.value
        elif token.value == '%':
            # Modulo
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                if after[1].type == TType.NUMBER:
                    popped.value %= after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value %= popped.value
        elif token.value == '*':
            # Power
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                if after[1].type == TType.NUMBER:
                    popped.value **= after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value **= popped.value
        # Bitwise (very wise indeed) operators
        elif token.value == '»':
            # Bitshift right
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                if after[1].type == TType.NUMBER:
                    popped.value >>= after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value >>= popped.value
        elif token.value == '«':
            # Bitshift right
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                if after[1].type == TType.NUMBER:
                    popped.value <<= after[1].value
                    self.stack.push(popped)
                    self.skip(1)
                else:
                    self.stack.top().value <<= popped.value
        elif token.value == '&':
            # Bitwise and
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                self.stack.top().value &= popped.value
        elif token.value == '|':
            # Bitwise or
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                self.stack.top().value |= popped.value
        elif token.value == '^':
            # Bitwise xor
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                self.stack.top().value ^= popped.value
        elif token.value == '~':
            # Bitwise not
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                popped.value = ~popped.value
                self.stack.push(popped)
        # Logical operators
        elif token.value == '∧':
            # logical and
            popped = self.stack.pop()
            popped2 = self.stack.pop()
            if popped.type == OType.NUMBER and popped2.type == OType.NUMBER:
                obj = Object(1 if popped.value and popped2.value else 0, OType.NUMBER)
                self.stack.push(obj)
        elif token.value == '∨':
            # logical or
            popped = self.stack.pop()
            popped2 = self.stack.pop()
            if popped.type == OType.NUMBER and popped2.type == OType.NUMBER:
                obj = Object(1 if popped.value or popped2.value else 0, OType.NUMBER)
                self.stack.push(obj)
        elif token.value == '¬':
            # logical not
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                obj = Object(1 if not popped.value else 0, OType.NUMBER)
                self.stack.push(obj)
        # More number things
        elif token.value == 'C':
            # Complement
            popped = self.stack.pop()
            if popped.type == OType.NUMBER:
                popped.value = 1 - popped.value
                self.stack.push(popped)
        elif token.value == '²':
            # Square
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                popped.value **= 2
                self.stack.push(popped)
        elif token.value == '³':
            # Cube
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                popped.value **= 3
                self.stack.push(popped)
        elif token.value == '√':
            # Square root
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                popped.value **= 0.5
                self.stack.push(popped)
        elif token.value == '∛':
            # Cube root
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                popped.value **= 1 / 3
                self.stack.push(popped)
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
        elif token.value == '¼':
            # Multiply be 1/4
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                popped.value *= 1 / 4
                self.stack.push(popped)
        elif token.value == '¾':
            # Multiply be 3/4
            popped = self.stack.pop()
            if popped.type == OType.NUMBER or popped.type == OType.ARRAY:
                popped.value **= 3 / 4
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

