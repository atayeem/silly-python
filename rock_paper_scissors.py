import random

class RockPaperScissors:
    def __init__(self, **kwargs):
        if "hand" in kwargs:
            self.hand = kwargs["hand"]
        else:
            self.hand = random.choice(["rock", "paper", "scissors"])
    
    @staticmethod
    def play(p1: str, p2: str):
        if p1 == p2:
            return p1
        
        while True:
            if p1 == "rock":
                if p2 == "scissors":
                    return "rock"
                elif p2 == "paper":
                    return "paper"
            
            if p1 == "scissors":
                if p2 == "paper":
                    return "scissors"
                elif p2 == "rock":
                    return "rock"
            
            if p1 == "paper":
                if p2 == "rock":
                    return "paper"
                elif p2 == "scissors":
                    return "scissors"
            
            tmp = p1
            p1 = p2
            p2 = tmp

    def __mul__(self, x):
        winner = self.play(self.hand, x.hand)
        return RockPaperScissors(hand=winner)

    def __str__(self):
        return self.hand

rock = RockPaperScissors(hand="rock")
paper = RockPaperScissors(hand="paper")
scissors = RockPaperScissors(hand="scissors")
tie = rock * rock

print("non-associative:")
print((rock * (paper * scissors)))
print(((rock * paper) * scissors))

print("\nyet commutative:")
print(rock * paper)
print(paper * rock)

print("\nidentity element:")
print(tie * paper)
print(tie * rock)
