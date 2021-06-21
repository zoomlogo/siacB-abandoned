from enum import Enum

class TokenTypes(Enum):
    Number = 0
    Array = 1
    String = 2

    Command = 3

class Token:
    def __init__(self, value, _type, misc=None):
        self.value = value
        self.type = _type
        self.misc = misc

    def update(self, misc):
        self.misc = misc

    def __str__(self):
        return f"Token({self.value}, {self.type}, {self.misc})"

class Parser:
    def __init__(self, code):
        self.code = code
        self.i = 0
        self.parsed = []
        self.once = False

        self.NUMBERS = "0123456789.e"
        self.code_page  = self.NUMBERS + "_;,?"
        self.code_page += "īēāūṭō"
        self.code_page += "p"
        self.code_page += "+-×÷²³½±"
        self.code_page += "=≠>≥<≤"
        self.code_page += "{:}"
        self.code_page += "()"

        assert len(self.code_page) <= 256

        self.pre_parse()

    def pre_parse(self):
        # Return code witthout whitespace and Comments
        res = ''
        i = 0
        while i < len(self.code):
            c = self.code[i]
            after = self.code[i:]
            if c == '#':
                comment_end = after.index('\n')
                i += comment_end
            elif c == 'p' or c == 'ō':
                string_end = after.index('`')
                res += after[:string_end]
                i += string_end
            elif c == ' ' or c == '\n' or c == '\t':
                pass
            else:
                res += c
            i += 1

        self.code = res

    def parse(self):
        # Return a list of Tokens
        while self.i < len(self.code):
            char = self.code[self.i]
            after = self.code[self.i:]

            if char in self.NUMBERS:
                digit_end = self.get_chars_bounds(after, self.NUMBERS)
                try:
                    val = int(self.code[self.i:self.i + digit_end])
                except:
                    val = float(self.code[self.i:self.i + digit_end])
                tok = Token(val, TokenTypes.Number)
                self.parsed.append(tok)
                self.i += digit_end - 1
            elif char == 'p' or char == 'ō':
                string_end = after.index('`')
                self.parsed.append(Token(char, TokenTypes.Command))
                self.parsed.append(Token(after[1:string_end], TokenTypes.String))
                self.parsed.append(Token('`', TokenTypes.Command))
                self.i += string_end
            else:
                tok = Token(char, TokenTypes.Command)
                self.parsed.append(tok)

            self.i += 1

        if not ('ṭ' in self.code or 'ō' in self.code):
            tok = Token('ṭ', TokenTypes.Command)
            self.parsed.append(tok)

        self.post_parser()

        return self.parsed

    def post_parser(self):
        i = 0
        while i < len(self.parsed):
            tok = self.parsed[i]
            after_tok = self.parsed[i:]
            char = tok.value
            if char == '{':
                if_end = self.get_tok_bounds(after_tok, '{', '}')
                else_end = self.get_tok_bounds(after_tok, '{', ':')
                misc = {
                    "start": i,
                    "else": i + else_end,
                    "end": i + if_end
                }
                tok.update(misc)
            elif char == ':':
                if_end = self.get_tok_bounds(after_tok, ':', '}')
                misc = {
                    "end": i + if_end
                }
                tok.update(misc)
            elif char == '(':
                while_end = self.get_tok_bounds(after_tok, '(', ')')
                misc = {
                    "start": i,
                    "end": i + while_end
                }
                tok.update(misc)
            elif char == ')':
                for token in self.parsed:
                    if token.type == TokenTypes.Command and token.value == '(':
                        if token.misc['end'] == i:
                            misc = {
                                "start": token.misc["start"]
                            }
                            tok.update(misc)

            i += 1

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

    def get_tok_bounds(self, tokens, start, end):
        # Get bounds defined by closing and opening chars which are different
        is_bound = 0
        found_start = False
        start_index = None
        end_index = None

        i = 0
        while i < len(tokens):
            tok = tokens[i]
            char = tok.value
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
