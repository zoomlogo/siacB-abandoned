from sparser import TokenTypes
from stypes import Types, Object

class Interpreter:
    def __init__(self, tokens, logobj):
        self.tokens = tokens
        self.log = logobj
        self.pointer = 0
        self.memory_stack = []
        self.auto_output = True

    def op_eval(self, op, before, after):
        # For logging
        if self.log is not None:
            self.log.write('Pointer: ' + str(self.pointer) + '\n')
            self.log.write('  ' + str(op) + '\n')
            self.log.write('  ' + str(self.memory_stack) + '\n')
        # Stack operators
        if op.value == '_':
            obj = Object(len(self.memory_stack), Types.Number)
            self.memory_stack.append(obj)
        elif op.value == ';':
            self.memory_stack.append(self.memory_stack[-1])
        elif op.value == ',':
            self.memory_stack.pop()
        elif op.value == '?':
            for obj in self.memory_stack:
                print(end=obj.value)
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
            self.auto_output = False
            print(self.memory_stack.pop().value)
        elif op.value == 'ō':
            print(after[1].value)
            self.pointer += 2
        # Constants
        elif op.type == TokenTypes.Number:
            obj = Object(op.value, Types.Number)
            self.memory_stack.append(obj)
            self.pointer += 1
        elif op.value == 'p':
            obj = Object(after[1].value, Types.String)
            self.memory_stack.append(obj)
            self.pointer += 2
        # Arithmetic Operators
        elif op.value == '+':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value += after[1].value
                    self.pointer += 1
        elif op.value == '-':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value -= after[1].value
                    self.pointer += 1
        elif op.value == '×':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value *= after[1].value
                    self.pointer += 1
        elif op.value == '÷':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value /= after[1].value
                    self.pointer += 1
        # Powers
        elif op.value == '²':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1] ** 2
        elif op.value == '³':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1] ** 3
        elif op.value == '√':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1] ** (1 / 2)
        elif op.value == '∛':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value = self.memory_stack[-1] ** (1 / 3)
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
        # Negate
        elif op.value == '¼':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value *= 1 / 4
        elif op.value == '±':
            if self.memory_stack[-1].type == Types.Number:
                self.memory_stack[-1].value *= -1
        # Comparision operators
        elif op.value == '=':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value == after[1].value
                    self.pointer += 1
        elif op.value == '≠':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value != after[1].value
                    self.pointer += 1
        elif op.value == '>':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value > after[1].value
                    self.pointer += 1
        elif op.value == '<':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value < after[1].value
                    self.pointer += 1
        elif op.value == '≤':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value <= after[1].value
                    self.pointer += 1
        elif op.value == '≥':
            if self.memory_stack[-1].type == Types.Number:
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1].value = self.memory_stack[-1].value >= after[1].value
                    self.pointer += 1
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
