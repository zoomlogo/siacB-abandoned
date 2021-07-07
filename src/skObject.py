from enum import Enum

# Define object types
class OType(Enum):
    NUMBER = 0
    STRING = 1
    ARRAY = 2

# Object class to be used in interpreter stack
class Object:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __repr__(self):
        repn = f"Object({repr(self.value)}, {self.type})"
        return repn

# Test
if __name__ == "__main__":
    token = Object(23, OType.NUMBER)
    print(token)
