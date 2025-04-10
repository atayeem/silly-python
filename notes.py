from fractions import Fraction
from math import log2

def complexity(f: Fraction) -> float:
    return log2(f.numerator) + log2(f.denominator)

def cents_diff(a: float, b: float) -> float:
    return 1200.0 * log2(b / a)

# Approximate a number to the nearest fraction
def decimal_to_fraction(decimal: float, acc=16.0) -> tuple[Fraction, float]:
    full_fraction = Fraction(decimal)

    for i in range(5, 1000):
        fraction = full_fraction.limit_denominator(i)
        diff = cents_diff(fraction, decimal)
        if abs(diff) < acc:
            return fraction, diff
        
    return fraction, 0.0


notes12 = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "C"]
# notes24 = [notes12[i//2] + "+" * (i % 2) for i in range(24 + 1)]
notes36 = [notes12[(i + 1)//3] + ["", "^", "v"][i % 3] for i in range(36 + 1)]

intervals36 = []
for i in range(37):
    interval, diff = decimal_to_fraction(2 ** (i/36), 7.5)
    com = complexity(interval)
    name = notes36[i]
    intervals36.append((com, name, interval, diff))

intervals36.sort()

for interval in intervals36:
    print(*interval[1:3], "+" * (interval[3] >= 0) + f"{interval[3]:.2f} cents", sep="\t")