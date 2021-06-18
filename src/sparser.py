from enum import Enum

class TokenTypes(Enum):
    Integer = 0
    Float = 1
    Array = 2
    String = 4

    Command = 5

class Token:
    def __init__(self, value, _type):
        self.value = value
        self.type = _type

class Parser:
    def __init__(self, code):
        self.code = code
        self.i = 0
        self.parsed = []
        self.NUMBERS = "0123456789"
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
            elif char in self.code_page:
                tok = Token(char, TokenTypes.Command)

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

