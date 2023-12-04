import re
from functools import reduce
from operator import mul

from utils import *
from constants import *


def day_1(part='A') -> int:
    pattern = r'\d' if part.upper() == 'A' else '(?=(' + '|'.join(
        [r'\d', *number_words]) + '))'

    conversion_dict = {
        **word_to_digit,
        **dict(zip((str(i) for i in range(1, 10)), range(1, 10)))
    }

    return sum(int(f'{conversion_dict[re.findall(pattern, line)[0]]}'
                   f'{conversion_dict[re.findall(pattern, line)[-1]]}') for
               line in read_input(day=1))


def day_2(part='A') -> int:
    games = parse_day_2()
    return _day_2A(games) if part.upper() == 'A' else _day_2B(games)


def _day_2A(games):
    truth = {'red': 12, 'green': 13, 'blue': 14}

    def compare(marbles: dict) -> bool:
        for k, v in marbles.items():
            if truth[k] < v:
                return False
        return True

    return sum(k for k, marbles in games.items() if compare(marbles))


def _day_2B(games):
    return sum(reduce(mul, marbles.values(), 1) for marbles in games.values())


if __name__ == '__main__':
    print(f'{day_1()=}')
    print(f'{day_1(part="B")=}')
    print(f'{day_2()=}')
    print(f'{day_2(part="B")=}')
