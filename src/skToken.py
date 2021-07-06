from enum import Enum

# Define token types
class TType(Enum):
    NUMBER = 0
    STRING = 1
    COMMAND = 2

# Token class to be used in parser
class Token:
    def __init__(self, value, type, misc={}):
        self.value = value
        self.type = type
        self.misc = misc

    def update(self, misc):
        self.misc = misc

    def __repr__(self):
        repn = f"Token({repr(self.value)}, {self.type}, {self.misc})"
        return repn


# Test
if __name__ == "__main__":
    token = Token(':', TType.COMMAND)
    print(token)
    token.update({
        "arity": 0
    })
    print(token)
