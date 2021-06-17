class Interpreter:
    def __init__(self, program):
        self.program = program
        self.pointer = 0
        self.memory_stack = []
        self.auto_output = True

    def op_eval(self, op, before, after):
        # Stack operators
        if op == '_':
            self.memory_stack.append(len(self.memory_stack))
        elif op == '.':
            self.memory_stack.append(self.memory_stack[-1])
        elif op == ',':
            self.memory_stack.pop()
        elif op == '?':
            print(self.memory_stack)
        # Input
        elif op == 'ī':
            self.memory_stack.append(int(input('int: ')))
        elif op == 'ē':
            self.memory_stack.append(float(input('float: ')))
        elif op == 'ā':
            a = input('array<int>: ').split()
            a = [int(i) for i in a]
            self.memory_stack.append(a)
        elif op == 'ū':
            self.memory_stack.append(input('string: '))
        # Output
        elif op == 'ṭ':
            self.auto_output = False
            print(self.memory_stack.pop())
        elif op == 'ō':
            self.auto_output = False
            string_end = after.index('`')
            print(after[1:string_end])
            self.pointer += string_end
        # Constants
        elif op.isdigit():
            digit_end = self.get_chars_bounds(after, "0123456789")[1]
            self.memory_stack.append(int(self.program[self.pointer:self.pointer + digit_end]))
            self.pointer += digit_end - 1
        elif op == 'p':
            string_end = after.index('`')
            self.memory_stack.append(after[1:string_end])
            self.pointer += string_end
        # Arithmetic Operators
        elif op == '+':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] += int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '-':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] -= int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '×':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] *= int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '÷':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] /= int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        # Comparision operators
        elif op == '=':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] = self.memory_stack[-1] == int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '≠':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] = self.memory_stack[-1] != int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '>':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] = self.memory_stack[-1] > int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '<':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] = self.memory_stack[-1] < int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '≤':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] = self.memory_stack[-1] <= int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        elif op == '≥':
            if isinstance(self.memory_stack[-1], int):
                if after[1].isdigit():
                    digit_end = self.get_chars_bounds(after, "0123456789")[1]
                    self.memory_stack[-1] = self.memory_stack[-1] >= int(self.program[self.pointer + 1:self.pointer + digit_end])
                    self.pointer += digit_end - 1
        # If statements
        elif op == '{':
            # We hit an if statement
            # Get the ending
            if_end = self.get_bounds(after, '{', '}')[1]
            try:
                else_begin = after[1:if_end].index(':')
            except:
                else_begin = None
            popped = self.memory_stack.pop()
            if popped:
                # Do nothing
                pass
            else:
                if else_begin != None:
                    self.pointer += else_begin + 1
                else:
                    self.pointer += if_end - 1
        elif op == ':':
            # Jump to '}'
            if_end = self.get_bounds('{' + after, '{', '}')[1] - 1
            self.pointer += if_end - 1

    def get_bounds(self, string, start, end):
        # Get bounds defined by closing and opening chars which are different
        is_bound = 0
        found_start = False
        start_index = None
        end_index = None

        i = 0
        while i < len(string):
            char = string[i]
            if char == start:
                if not found_start:
                    found_start = True
                    start_index = i
                is_bound += 1
            elif char == end:
                is_bound -= 1
                if is_bound == 0:
                    end_index = i
                    break
            i += 1

        return (start_index + 1, end_index)

    def get_chars_bounds(self, string, chars):
        # Get bounds for group of chars
        in_range = False
        start_index = None
        end_index = None

        i = 0
        while i < len(string):
            char = string[i]
            if char in chars:
                if not in_range: start_index = i
                in_range = True
            else:
                if in_range:
                    end_index = i
                    break
            i += 1

        return (start_index, end_index)

    def run(self):
        # Main loop
        while self.pointer < len(self.program):
            before = self.program[:self.pointer]
            op = self.program[self.pointer]
            after = self.program[self.pointer:]

            self.op_eval(op, before, after)

            self.pointer += 1
        if self.auto_output and len(self.memory_stack) >= 1:
            return self.memory_stack[-1]
