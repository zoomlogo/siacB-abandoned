# Define token types
class TType:
    CONSTANT = 0
    COMMAND = 1

# Token class to be used in parser
class Token:
    def __init__(self, value, type, misc={}):
        self.value = value
        self.type = type
        self.misc = misc

    def update(self, misc):
        self.misc = misc

    def __repr__(self):
        repn = "Token(\n"
        repn += f"    value={repr(self.value)},\n"
        repn += f"    type={self.type},\n"
        repn += f"    misc={self.misc}\n"
        repn += ")"
        return repn


# Test
if __name__ == "__main__":
    token = Token(':', TType.COMMAND)
    print(token)
    token.update({
        "arity": 0
    })
    print(token)
