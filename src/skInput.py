import skObject
import numpy as np

class SmartInput:
    def __init__(self, inputs=[]):
        self.reset = True if inputs else False
        self.i = 0
        self.inputs = []
        for i in inputs:
            self.inputs.append(self.objectify(i))

    def input(self):
        if not self.reset:
            value = input()
        else:
            value = ''
        if value == '':
            self.reset = True
            ret = self.inputs[self.i]
            self.i += 1
            if self.i >= len(self.inputs):
                self.i = 0
            return ret
        self.inputs.append(self.objectify(value))
        return self.inputs[-1]

    def objectify(self, value):
        type = skObject.OType.STRING

        try:
            value = int(value)
            type = skObject.OType.NUMBER
        except:
            try:
                value = float(value)
                type = skObject.OType.NUMBER
            except:
                try:
                    value = np.array(eval(value))
                    type = skObject.OType.ARRAY
                except:
                    pass
        return skObject.Object(value, type)

    def objectify_from_instance(self, value):
        type = None
        if isinstance(value, int) or isinstance(value, float):
            type = skObject.OType.NUMBER
        elif isinstance(value, np.ndarray):
            type = skObject.OType.ARRAY
        elif isinstance(value, str):
            type = skObject.OType.STRING

        return skObject.Object(value, type)

if __name__ == "__main__":
    inp = SmartInput()
    for i in range(10):
        print(inp.input())
