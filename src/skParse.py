from skToken import Token, TType

def get_index(string, to_find):
    # Better index (if not found return ending)
    i = 0
    while i < len(string):
        char = string[i]
        if char == to_find:
            break
        i += 1
    return i

def get_end_group(string, group):
    # Given a string find the end of the group
    i = 0
    while i < len(string):
        char = string[i]
        if not char in group:
            break
        i += 1
    return i

def get_index_token(tokens, char_to_find):
    # Same as get_index but for Token
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.value == char_to_find:
            break
        i += 1
    return i

def get_close_token(tokens, open, close):
    is_bound = 0
    found_start = False
    end_index = None

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        char = tok.value
        if char == open:
            if not found_start:
                found_start = True
            is_bound += 1
        elif char == close:
            is_bound -= 1
            if is_bound == 0:
                end_index = i
                break
        i += 1

    return end_index

def indent_level(tokens, open, close):
    k = 0
    for token in tokens:
        if token.value == open: k += 1
        elif token.value == close: k -= 1
    return k + 1

class Parser:
    def __init__(self, code):
        self.code = code
        self.code_pointer = 0

        self.tokens = []

    def remove_whitespace(self):
        i = 0
        code = ''

        while i < len(self.code):
            char = self.code[i]
            after = self.code[i:] # After the character
            # Check for comments
            if char == '⯈':
                # Ignore everything until newline
                comment_end = after.index('\n')
                i += comment_end
            elif char == '`':
                # String
                string_end = get_index(after[1:], '`')
                i += string_end + 1
                code += '`'
                code += after[1:string_end + 1]
                code += '`'
            elif char == '\\':
                # Single char skip
                code += '\\' + after[1]
                i += 1
            elif char == '\n':
                # Skip newlines
                pass
            else:
                # Otherwise
                code += char

            i += 1

        self.code = code

    def parse(self):
        # Parse code into a list of tokens
        while self.code_pointer < len(self.code):
            char = self.code[self.code_pointer]
            after = self.code[self.code_pointer:]

            if char in "0123456789":
                number_end = get_end_group(after, "0123456789.e")
                number = self.code[self.code_pointer:self.code_pointer + number_end]
                try:
                    value = int(number)
                except:
                    value = float(number)
                token = Token(value, TType.NUMBER)
                self.tokens.append(token)
                self.code_pointer += number_end - 1
            elif char == '`':
                string_end = get_index(after[1:], '`')
                self.tokens.append(Token('`', TType.COMMAND))
                self.tokens.append(Token(after[1:string_end + 1], TType.STRING))
                self.tokens.append(Token('`', TType.COMMAND))
                self.code_pointer += string_end + 1
            elif char == '\\':
                self.tokens.append(Token('\\', TType.COMMAND))
                self.tokens.append(Token(after[1], TType.STRING))
                self.code_pointer += 1
            elif char == '‛':
                self.tokens.append(Token('‛', TType.COMMAND))
                self.tokens.append(Token(after[1:3], TType.STRING))
                self.code_pointer += 2
            else:
                self.tokens.append(Token(char, TType.COMMAND))

            self.code_pointer += 1

        # Implicit output
        if not ('t' in self.code):
            self.tokens.append(Token('t', TType.COMMAND))

        self.match_brackets()

        return self.tokens

    def match_brackets(self):
        i = 0

        while i < len(self.tokens):
            token = self.tokens[i]
            after = self.tokens[i:]
            before = self.tokens[:i]
            char = token.value

            if char == '(':
                # While loop
                while_loop_end = get_close_token(after, '(', ')')
                misc = {
                    "start": i,
                    "end": i + while_loop_end
                }
                token.update(misc)
            elif char == ')':
                # End of while loop
                for t in self.tokens:
                    if t.value == '(' and 'end' in t.misc and t.misc['end'] == i:
                        misc = {
                            "start": t.misc['start'],
                            "end": i
                        }
                        token.update(misc)
            if char == '[':
                # foreach loop
                foreach_loop_end = get_close_token(after, '[', ']')
                ind_lvl = indent_level(before, '[', ']')
                misc = {
                    "start": i,
                    "end": i + foreach_loop_end,
                    "idl": ind_lvl
                }
                token.update(misc)
            elif char == ']':
                # End of foreach loop
                for t in self.tokens:
                    if t.value == '[' and 'end' in t.misc and t.misc['end'] == i:
                        misc = {
                            "start": t.misc['start'],
                            "end": i
                        }
                        token.update(misc)
            elif char == '{':
                # If statement
                if_end = get_close_token(after, '{', '}')
                else_end = get_close_token(after, '{', ':')
                misc = {
                    "start": i,
                    "else": i + else_end if else_end is not None else None,
                    "end": i + if_end
                }
                token.update(misc)
            elif char == ':':
                # If else statement
                if_end = get_close_token(after, ':', '}')
                misc = {
                    "end": i + if_end
                }
                token.update(misc)
            elif char == 'λ':
                function_end = get_index_token(after, ';')
                misc = {
                    "end": function_end
                }
                token.update(misc)


            i += 1

if __name__ == '__main__':
    p = Parser("[][][[]]")
    print("============")
    print(p.code)
    print("============")
    p.remove_whitespace()
    print(p.code)
    print("============")
    p = p.parse()
    for t in p:
        print(t)
