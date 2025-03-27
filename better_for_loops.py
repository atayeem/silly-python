# raise type("\033[2J\033[H" + "\n".join(["FizzBuzz" if i % 15 == 0 else "Buzz" if i % 5 == 0 else "Fizz" if i % 3 == 0 else str(i) for i in range(1,101)]), (Exception,), {})
def f(s: str):
    the_var = s.split("=")[0].strip()

    a = s.split(";")
    a = [x.strip() for x in a]

    exec(a[0], globals(), locals())
    while eval(a[1], globals(), locals()):
        yield locals()[the_var]
        exec(a[2], globals(), locals())

for i in f("i = 1; i < 100000; i += 1"):
    pass

print("Done")

for i in range(100000):
    pass

print("Done2")
