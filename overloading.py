class Everything:
    def __init__(self):
        self.s = ""
        self.i = ""
    
    def input(self, s):
        self.i = input(s)

    def __getattr__(self, name):
        print(name, end="")
        return self.input
    
    def __enter__(self):
        pass
    
    def __exit__(self, _, __, ___):
        print()
    
    def __iter__(self):
        print("", end=" ")
        yield 1
    
    def __call__(self):
        return i

e = Everything()

# with e: print

with e:
    e.Fizz
    for i in e:
        e.Buzz
e.How(" many numbers? ")
with e:
    e.e(e())
