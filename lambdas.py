(r := lambda f, i: (print(f(i)) or i < 100) and r(f, i + 1))((lambda i: (lambda cond, f, e: f if cond else e)(
    i % 15 == 0,
    lambda: "FizzBuzz",
    (lambda cond, f, e: f if cond else e)(
        i % 5 == 0,
        lambda: "Buzz",
        (lambda cond, f, e: f if cond else e)(
            i % 3 == 0,
            lambda: "Fizz",
            lambda: i
        )
    )
)()), 1)
