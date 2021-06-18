from enum import Enum

class TokenTypes(Enum):
    Integer = 0
    Float = 1
    Array = 2
    String = 4

    Command = 5

class Token:
    def __init__(self, value, _type, misc=None):
        self.value = value
        self.type = _type
        self.misc = misc

class Parser:
    def __init__(self, code):
        self.code = code
        self.i = 0
        self.parsed = []
        self.NUMBERS = "0123456789."
        self.code_page  = "_.,?"
        self.code_page += "īēāūṭō"
        self.code_page += "p"
        self.code_page += "+-×÷²³½±"
        self.code_page += "=≠>≥<≤"
        self.code_page += "{:}"
        self.code_page += "()"

        assert len(self.code_page) <= 256

    def parse(self):
        # Return a list of Tokens
        while self.i < len(self.code):
            char = self.code[self.i]
            after = self.code[self.i:]

            if char in self.NUMBERS:
                digit_end = self.get_chars_bounds(after, self.NUMBERS)
                val = int(self.code[self.i:self.i + digit_end])
                tok = Token(val, TokenTypes.Integer)
                self.parsed.append(tok)
                self.i += digit_end - 1
            elif char == '#':
                comment_end = after.index('\n')
                self.i += comment_end
            elif char in self.code_page:
                misc = None
                if char == 'p':
                    string_end = after.index('`')
                    self.parsed.append(after[1:string_end])
                    self.pointer += string_end
                elif char == 'ō':
                    string_end = after.index('`')
                    print(after[1:string_end])
                    self.pointer += string_end
                elif char == '{':
                    if_end = self.get_bounds(after, '{', '}')
                    try:
                        else_end = self.i + after.index(':')
                    except:
                        else_end = None
                    misc = {
                        "start": self.i,
                        "else": else_end,
                        "end": self.i + if_end
                    }
                elif char == '}':
                    for tok in self.parsed:
                        if tok.type == TokenTypes.Command and tok.value == '{':
                            if tok.misc['end'] == self.i:
                                misc = {
                                    "start": tok.misc["start"]
                                }
                elif char == '(':
                    while_end = self.get_bounds(after, '(', ')')
                    misc = {
                        "start": self.i,
                        "end": self.i + while_end
                    }
                elif char == ')':
                    for tok in self.parsed:
                        if tok.type == TokenTypes.Command and tok.value == '(':
                            if tok.misc['end'] == self.i:
                                misc = {
                                    "start": tok.misc["start"]
                                }
                tok = Token(char, TokenTypes.Command, misc)
                self.parsed.append(tok)

            self.i += 1
        return self.parsed


    def get_chars_bounds(self, string, chars):
        # Get bounds for group of chars
        in_range = False
        end_index = None

        i = 0
        while i < len(string):
            char = string[i]
            if char in chars:
                in_range = True
            else:
                if in_range:
                    end_index = i
                    break
            i += 1

        return end_index

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

        return end_index
