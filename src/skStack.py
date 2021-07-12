from skInput import SmartInput

class SmartStack:
    def __init__(self, input_obj):
        self.stack = []
        self.smart_input = input_obj

    def top(self):
        return self.stack[-1]

    def pop(self):
        if len(self.stack) == 0:
            self.stack.append(self.smart_input.input())
        return self.stack.pop()

    def push(self, value):
        self.stack.append(value)

    def __repr__(self):
        repn = "[ "
        for obj in self.stack:
            repn += repr(obj.value)
            repn += ' '
        return repn + "]"

class Stack(SmartStack):
    def __init__(self):
        super().__init__(None)

    def pop(self):
        return self.stack.pop()
    
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

