from sparser import TokenTypes


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
            self.memory_stack.append(len(self.memory_stack))
        elif op.value == ';':
            self.memory_stack.append(self.memory_stack[-1])
        elif op.value == ',':
            self.memory_stack.pop()
        elif op.value == '?':
            print(self.memory_stack)
        # Input
        elif op.value == 'ī':
            try:
                self.memory_stack.append(int(input('number: ')))
            except:
                self.memory_stack.append(float(input('number: ')))
        elif op.value == 'ā':
            a = input('array<int>: ').split()
            a = [int(i) for i in a]
            self.memory_stack.append(a)
        elif op.value == 'ū':
            self.memory_stack.append(input('string: '))
        # Output
        elif op.value == 'ṭ':
            self.auto_output = False
            print(self.memory_stack.pop())
        elif op.value == 'ō':
            print(after[1].value)
            self.pointer += 2
        # Constants
        elif op.type == TokenTypes.Number:
            self.memory_stack.append(op.value)
            self.pointer += 1
        elif op.value == 'p':
            self.memory_stack.append(after[1].value)
            self.pointer += 2
        # Arithmetic Operators
        elif op.value == '+':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] += after[1].value
                    self.pointer += 1
        elif op.value == '-':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] -= after[1].value
                    self.pointer += 1
        elif op.value == '×':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] *= after[1].value
                    self.pointer += 1
        elif op.value == '÷':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] /= after[1].value
                    self.pointer += 1
        # Powers
        elif op.value == '²':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] = self.memory_stack[-1] ** 2
        elif op.value == '³':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] = self.memory_stack[-1] ** 3
        elif op.value == '√':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] = self.memory_stack[-1] ** (1 / 2)
        elif op.value == '∛':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] = self.memory_stack[-1] ** (1 / 3)
        # Fractions
        elif op.value == '½':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] *= 1 / 2
        elif op.value == '¼':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] *= 1 / 4
        elif op.value == '¾':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] *= 3 / 4
        # Negate
        elif op.value == '¼':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] *= 1 / 4
        elif op.value == '±':
            if isinstance(self.memory_stack[-1], int):
                self.memory_stack[-1] *= -1
        # Comparision operators
        elif op.value == '=':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] = self.memory_stack[-1] == after[1].value
                    self.pointer += 1
        elif op.value == '≠':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] = self.memory_stack[-1] != after[1].value
                    self.pointer += 1
        elif op.value == '>':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] = self.memory_stack[-1] > after[1].value
                    self.pointer += 1
        elif op.value == '<':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] = self.memory_stack[-1] < after[1].value
                    self.pointer += 1
        elif op.value == '≤':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] = self.memory_stack[-1] <= after[1].value
                    self.pointer += 1
        elif op.value == '≥':
            if isinstance(self.memory_stack[-1], int):
                if after[1].type == TokenTypes.Number:
                    self.memory_stack[-1] = self.memory_stack[-1] >= after[1].value
                    self.pointer += 1
        # If statements
        elif op.value == '{':
            popped = self.memory_stack.pop()
            if popped:
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
            if self.memory_stack[-1]:
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
