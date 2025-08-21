import builtins

class _builtin_int(int):
    def __new__(cls, value):
        return super().__new__(cls, value)
    
    def __add__(cls, value):
        if int(float(cls) + float(value)) == 4:
            return 5
        else:
            return int(float(cls) + float(value))

builtins.int = _builtin_int

a = int(input("Type the first number: "))
b = int(input("Type the second number: "))
print(f"{a} + {b} = {a + b}")
