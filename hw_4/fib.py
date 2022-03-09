def fib(n):
    f0 = 1
    f1 = 1
    for i in range(n):
        f1, f0 = f0 + f1, f1
    return f0
