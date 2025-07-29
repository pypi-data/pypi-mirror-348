from qb_runtime import *
from sys import argv
from random import randrange

def main():
    args = collection.of(argv[1:])
    try:
        num = int(args[0]) + 1
    except:
        cout("parameter must be a number")
        return
    good_musicians = collection.of(["Kendrick Lamar", "Billy Talent", "Volbeat", "Kanonenfieber", "Fit For An Autopsy"])
    cout("Some good musicians include: ")
    good_musicians.for_each(lambda x: cout(x))
    cout("")
    even_powers = collection.of(range(num)).map(lambda x: x ** 2).filter(lambda x: x % 2 == 0)
    facs = collection.of(range(num)).map(lambda x: fac(x))
    if len(even_powers) < len(facs):
        to_be_added = len(facs) - len(even_powers)
        even_powers = even_powers + collection.of([3 for _ in range(to_be_added)])

    def __lambda39bf726f7947afffa76a41d92b408554(x):
        r1 = randrange(facs[x] + 1)
        r2 = randrange(even_powers[x] + 1)
        rsum = r1 + r2
        return rsum
    rsums = collection.of(range(num)).map(lambda x: __lambda39bf726f7947afffa76a41d92b408554(x))
    cout("Some random numbers:")
    rsums.for_each(lambda x: cout(x))

def fac(n: int) -> int:
    match n:
        case 0:
            return 1
        case _:
            return n * fac(n - 1)
if __name__ == "__main__":
    main()