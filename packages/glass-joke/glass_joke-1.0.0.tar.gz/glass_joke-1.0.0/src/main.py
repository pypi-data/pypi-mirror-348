from src.types import *

def loop():
    glass = Glass()
    SummonIntern = Intern

    while True:
        if glass.full:
            glass.drink()
        else:
            SummonIntern()
            glass.refill()
