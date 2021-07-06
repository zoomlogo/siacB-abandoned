
class Parser:
    def __init__(self, code):
        self.code = code
        self.code_pointer = 0

        self.tokens = []

