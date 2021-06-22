from sparser import TokenTypes
from stypes import Types, Object

import numpy as np
import math

class Interpreter:
    def __init__(self, tokens, logobj):
        self.tokens = tokens
        self.log = logobj
        self.pointer = 0
        self.memory_stack = []
        self.auto_output = True
        self.registor = 0

    def op_eval(self, op, before, after):
        # For logging
        if self.log is not None:
            self.log.write('Pointer: ' + str(self.pointer) + '\n')
            self.log.write('  ' + str(op) + '\n')
            self.log.write('  [ ')
            for obj in self.memory_stack:
                self.log.write(str(obj) + ' ')
            self.log.write(']\n')
            self.log.write('  ' + str(self.registor) + '\n')
        # Stack operators
        if op.value == '_':
            obj = Object(len(self.memory_stack), Types.Number)
            self.memory_stack.append(obj)
        elif op.value == ';':
            self.memory_stack.append(self.memory_stack[-1].copy())
        elif op.value == ',':
            self.memory_stack.pop()
        elif op.value == '?':
            for obj in self.memory_stack:
                print(end=str(obj.value))
            print()
        # Input
        elif op.value == 'ī':
            val = input('number: ')
            try:
                obj = Object(int(val), Types.Number)
                self.memory_stack.append(obj)
            except:
                obj = Object(float(val), Types.Number)
                self.memory_stack.append(obj)
        elif op.value == 'ā':
            a = input('array<number>: ').split()
            try:
                a = [int(i) for i in a]
            except:
                a = [float(i) for i in a]
            obj = Object(a, Types.Array)
            self.memory_stack.append(obj)
        elif op.value == 'ū':
            obj = Object(input("string: "), Types.String)
            self.memory_stack.append(obj)
        # Output
        elif op.value == 'ṭ':
            if self.memory_stack:
                print(self.memory_stack.pop().value)
        elif op.value == 'ō':
            print(after[1].value)
            self.pointer += 2
        # Constants
        elif op.type == TokenTypes.Number:
            obj = Object(op.value, Types.Number)
            self.memory_stack.append(obj)
        elif op.value == 'p':
            obj = Object(after[1].value, Types.String)
            self.memory_stack.append(obj)
            self.pointer += 2
        # Registor push and copy
        elif op.value == '©':
            self.registor = self.memory_stack.pop()
        elif op.value == '®':
            if self.registor:
                self.memory_stack.append(self.registor)
        # Arithmetic Operators
        elif op.value == '+':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value += after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value += obj2.value
            elif self.memory_stack[-1].type == Types.String:
                obj2 = self.memory_stack.pop()
                self.memory_stack[-1].value += str(obj2.value)
        elif op.value == '-':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value -= after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value -= obj2.value
        elif op.value == '×':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value *= after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value *= obj2.value
            elif self.memory_stack[-1].type == Types.String:
                obj2 = self.memory_stack.pop()
                self.memory_stack[-1].value *= obj2.value
        elif op.value == '÷':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value /= after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value /= obj2.value
        # Bitwise operators
        elif op.value == '»':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value >> after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value >> obj2.value
        elif op.value == '«':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value << after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value << obj2.value
        elif op.value == '&':
            if self.memory_stack[-1].type == Types.Number:
                obj2 = self.memory_stack.pop()
                self.memory_stack[-1].value = self.memory_stack[-1].value & obj2.value
        elif op.value == '|':
            if self.memory_stack[-1].type == Types.Number:
                obj2 = self.memory_stack.pop()
                self.memory_stack[-1].value = self.memory_stack[-1].value | obj2.value
        elif op.value == '^':
            if self.memory_stack[-1].type == Types.Number:
                obj2 = self.memory_stack.pop()
                self.memory_stack[-1].value = self.memory_stack[-1].value ^ obj2.value
        elif op.value == '!':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = ~self.memory_stack[-1].value
        # Powers
        elif op.value == '²':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** 2
        elif op.value == '³':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** 3
        elif op.value == '√':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** (1 / 2)
        elif op.value == '∛':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1].value ** (1 / 3)
        # Fractions
        elif op.value == '½':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value *= 1 / 2
        elif op.value == '¼':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value *= 1 / 4
        elif op.value == '¾':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value *= 3 / 4
        # Math
        elif op.value == 'm':
            if after[1].value == '!':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = math.factorial(int(self.memory_stack[-1].value))
            elif after[1].value == 's':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = math.sin(self.memory_stack[-1].value)
            elif after[1].value == 'S':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = math.asin(self.memory_stack[-1].value)
            elif after[1].value == 'c':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = math.cos(self.memory_stack[-1].value)
            elif after[1].value == 'C':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = math.acos(self.memory_stack[-1].value)
            elif after[1].value == 't':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = math.tan(self.memory_stack[-1].value)
            elif after[1].value == 'T':
                if self.memory_stack[-1].type == Types.Number:
                    self.memory_stack[-1].value = math.atan(self.memory_stack[-1].value)
            self.pointer += 1
        # Negate
        elif op.value == '±':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value *= -1
        # Floor and ceil
        elif op.value == '⊥':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = int(self.memory_stack[-1].value)
        elif op.value == '⊤':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = int(self.memory_stack[-1].value) + 1
        # ABS
        elif op.value == '⊢':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = abs(self.memory_stack[-1].value)
        # Comparision operators
        elif op.value == '=':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value == after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value == obj2.value
        elif op.value == '≠':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value != after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value != obj2.value
        elif op.value == '>':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value > after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value > obj2.value
        elif op.value == '<':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value < after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value < obj2.value
        elif op.value == '≤':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value <= after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value <= obj2.value
        elif op.value == '≥':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value >= after[1].value
                    self.pointer += 1
                else:
                    obj2 = self.memory_stack.pop()
                    self.memory_stack[-1].value = self.memory_stack[-1].value >= obj2.value
        # If statements
        elif op.value == '{':
            popped = self.memory_stack.pop()
            if popped.value:
                # Do nothing
                pass
            else:
                if op.misc["else"] != None:
                    self.pointer = op.misc["else"]
                else:
                    self.pointer = op.misc["end"]
        elif op.value == ':':
            # Jump to '}'
            self.pointer = op.misc["end"]
        # While loop
        elif op.value == '(':
            if self.memory_stack[-1].value:
                pass
            else:
                self.pointer = op.misc["end"]
        elif op.value == ')':
            self.pointer = op.misc["start"] - 1

    def run(self):
        # Main loop
        while self.pointer < len(self.tokens):
            before = self.tokens[:self.pointer]
            token = self.tokens[self.pointer]
            after = self.tokens[self.pointer:]

            self.op_eval(token, before, after)

            self.pointer += 1
