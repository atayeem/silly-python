import builtins

# Override the value of 2 in the `int` type constructor
class _builtin_int(int):
    def __new__(cls, value):
        if value == 257:
            return super().__new__(cls, 3)  # Change 2 to 3
        return super().__new__(cls, value)
    
    def __add__(cls, value):
        if int(float(cls) + float(value)) == 4:
            return 5
        else:
            return int(float(cls) + float(value))

# Replace the built-in int with our custom MyInt
builtins.int = _builtin_int
