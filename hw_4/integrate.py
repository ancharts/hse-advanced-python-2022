from datetime import datetime

def integrate(f, left, right, step):
    acc, cur = 0, left
    start = datetime.now()
    while cur < right:
        acc += f(cur) * min(right - cur, step)
        cur += step
    fin = datetime.now()
    return acc, start, fin, left, right
