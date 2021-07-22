from numpy.core.shape_base import stack
from skInput import SmartInput

# Main stack
class SmartStack:
    def __init__(self, input_obj):
        self.stack = []
        self.smart_input = input_obj

    def top(self):
        if self.is_empty():
            self.stack.append(self.smart_input.input())
        return self.stack[-1]

    def pop(self):
        if len(self.stack) == 0:
            self.stack.append(self.smart_input.input())
        return self.stack.pop()

    def push(self, value):
        self.stack.append(value)

    def __len__(self):
        return len(self.stack)
    
    def is_empty(self):
        return not self.stack

    def __repr__(self):
        repn = "[ "
        for obj in self.stack:
            repn += repr(obj.value)
            repn += ' '
        return repn + "]"

    def update(self, new):
        self.stack = [new]

    def values(self):
        return [o.value for o in self.stack]

class Stack(SmartStack):
    def __init__(self):
        super().__init__(None)

    def pop(self):
        return self.stack.pop()

    def top(self):
        return self.stack[-1]
    
    def __repr__(self):
        repn = '[ '
        for o in self.stack:
            repn += repr(o) + ' '
        return repn + ']'

if __name__ == "__main__":
    smart_input = SmartInput()
    stk = SmartStack(smart_input)

    print(stk)
    print(stk.pop())
    print(stk)
    print(stk.pop())
    print(stk)
    print(stk.top())
    print(stk)

