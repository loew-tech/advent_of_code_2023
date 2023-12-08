from bisect import bisect_left
from functools import reduce
from math import sqrt, floor, ceil
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
                    to_add = to_add or is_in_bounds(y + yi, x + xi, data) and \
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


def day_4(part='A'):
    data = read_input(day=4)
    return day_4a(data) if part.upper() == 'A' else day_4b(data)


def day_4a(data: list[str]) -> int:
    score = 0
    for line in data:
        winners, mine = line[line.index(':'):].split('|')
        winners, mine = set(winners.split()), set(mine.split())
        num_matches = len(winners.intersection(mine))
        score += 2 ** (num_matches - 1) if num_matches else 0
    return score


def day_4b(data: list[str]) -> int:
    card_matches = []
    counts = [1] * len(data)
    for line in data:
        winners, mine = line[line.index(':'):].split('|')
        winners, mine = set(winners.split()), set(mine.split())
        card_matches.append(len(winners.intersection(mine)))

    index = -1
    while (index := index + 1) < len(card_matches):
        for j in range(1, card_matches[index] + 1):
            counts[index + j] += counts[index]
    return sum(counts)


def day_5(part='A') -> int:
    if not part.upper() == 'A':
        return NotImplemented
    data = read_input(day=5, delim='\n\n')
    seeds = tuple(int(i) for i in data[0][data[0].index(':')+2:].split(' '))

    keys, mappings = [], []
    for mapping in data[1:]:
        keys_dict, mapping = day_5_parse_mapping(mapping)
        keys.append(keys_dict)
        mappings.append(mapping)

    sorted_keys, min_ = [sorted(d.keys()) for d in keys], float('inf')
    for seed in seeds:
        val = seed
        for i, map_ in enumerate(mappings):
            key_index = sorted_keys[i][bisect_left(sorted_keys[i], val)-1]
            if len(sorted_keys) == key_index or val not in keys[i][key_index]:
                break
            key = keys[i][key_index]
            offset, range_ = val - key[0], map_[key]
            val = range_[0] + offset
        min_ = min(min_, val)
    return min_


def day_6(part='A') -> int:
    times, distances = day_6_get_times_and_distances(part)

    prod = 1
    for t, d in zip(times, distances):
        first, last = (t-sqrt(t**2-4*d))/2, (t+sqrt(t**2-4*d))/2
        in_range = floor(last)-ceil(first) + 1
        in_range -= ((int(first) == first) + (int(last) == last))
        prod *= in_range
    return prod


if __name__ == '__main__':
    print(f'{day_1()=}')
    print(f'{day_1(part="B")=}')
    print(f'{day_2()=}')
    print(f'{day_2(part="B")=}')
    print(f'{day_3()=}')
    print(f'{day_3(part="B")=}')
    print(f'{day_4()=}')
    print(f'{day_4(part="B")=}')
    print(f'{day_5()=}')
    print(f'{day_5(part="B")=}')
    print(f'{day_6()=}')
    print(f'{day_6(part="B")=}')
