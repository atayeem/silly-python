hashish = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11
}

def interval(n1:int, n2:int) -> int:
    n = n2 - n1
    if n < 0:
        return 12 + n
    else:
        return n

def doStuff(s0: str):
    # Create string for output
    sout = ""

    # Split by newlines, remove first line
    s1 = s0.split('\n')[1:]

    # Split by spaces, create an array of arrays of notes.
    s2 = [s.split(' ') for s in s1]

    # Turn notes into numbers
    s3 = [[hashish[note] for note in chord] for chord in s2]
    for ch in s3:
        intervals = [
            interval(ch[0], ch[1]),
            interval(ch[1], ch[2]),
            interval(ch[2], ch[3]),
            interval(ch[3], ch[0]),
        ]

        match intervals:
            case [4, 3, 3, 2]:
                sout += "root\n"
            case [3, 3, 2, 4]:
                sout += "first\n"
            case [3, 2, 4, 3]:
                sout += "second\n"
            case [2, 4, 3, 3]:
                sout += "third\n"
            case _:
                sout += "invalid\n"
            

    # Turn no
    return sout.rstrip()

def main():
    test1 = """10
C E G A#
B F D G
E G# B D
F# A C D
B D G A#
F G# A# D
C# D# G A#
A A A G
D# F A C
A# C# D# G"""

    res1 = """root
invalid
root
first
invalid
second
third
invalid
third
second"""
    if (doStuff(test1) == res1):
        print("Great!")
    else:
        print("Wrong:")
        print()
        print(doStuff(test1))

if __name__ == "__main__":
    main()
