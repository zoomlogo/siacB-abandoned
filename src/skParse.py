
def get_index(string, to_find):
    # Better index (if not found return ending)
    i = 0
    while i < len(string):
        char = string[i]
        if char == to_find:
            break
        i += 1
    print(f"{string = }")
    return i

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
            if char == '#':
                # Ignore everything until newline
                comment_end = after.index('\n')
                i += comment_end
            elif char == '`':
                # String
                string_end = get_index(after[1:], '`')
                i += string_end + 1
                code += '`'
                code += after[1:string_end]
                code += '`'
            elif char == '\\':
                # Single char pusher
                code += '\\' + after[1]
                i += 1
            elif char == ' ' or char == '\n':
                # Skip newlines and spaces
                pass
            else:
                # Otherwise
                code += char

            i += 1

        self.code = code

if __name__ == '__main__':
    p = Parser("abc n\nasas #Xas\n` igonew\n` lasdk \\ adl")
    print("============")
    print(p.code)
    p.remove_whitespace()
    print("============")
    print(p.code)
