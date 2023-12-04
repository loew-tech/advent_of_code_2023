import re
from functools import reduce
from operator import mul
from string import digits

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
    return _day_2a(games) if part.upper() == 'A' else _day_2b(games)


def _day_2a(games) -> int:
    truth = {'red': 12, 'green': 13, 'blue': 14}

    def compare(marbles: dict) -> bool:
        for k, v in marbles.items():
            if truth[k] < v:
                return False
        return True

    return sum(k for k, marbles in games.items() if compare(marbles))


def _day_2b(games) -> int:
    return sum(reduce(mul, marbles.values(), 1) for marbles in games.values())


def day_3(part='A') -> int:
    data = read_input(day=3)
    return day_3a(data) if part == 'A' else day_3b(data)


def day_3a(data: list[str]) -> int:
    ignore, sum_ = set(f'{digits}.'), 0
    for y, line in enumerate(data):
        x, val, to_add = -1, '', False
        while (x := x + 1) < len(line):
            if line[x] in digits:
                val += line[x]
                for yi, xi in directions:
                    to_add = to_add or 0 <= y + yi < len(
                        data) and 0 <= x + xi < len(line) and \
                             data[y + yi][x + xi] not in ignore
            elif val:
                sum_ += to_add * int(val)
                val, to_add = '', False

    return sum_


def day_3b(data: list[str]) -> int:
    sum_ = 0
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '*':
                sum_ += (c == '*') * day_3b_helper(data, y, x)
    return sum_


if __name__ == '__main__':
    print(f'{day_1()=}')
    print(f'{day_1(part="B")=}')
    print(f'{day_2()=}')
    print(f'{day_2(part="B")=}')
    print(f'{day_3()=}')
    print(f'{day_3(part="B")=}')
