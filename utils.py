from collections import defaultdict, Counter, namedtuple
from string import digits
from typing import Tuple, Any

from constants import DIRECTIONS, CARD_FACE_VALS

Hand = namedtuple('Hand', ['type', 'cards', 'bid'])


def read_input(day: int | str, delim='\n') -> list[str]:
    with open(f'inputs/day_{day}.txt') as f:
        return f.read().rstrip().split(delim)


def parse_day_2() -> list[str]:
    data, games = read_input(day=2), defaultdict(lambda: defaultdict(int))
    for line in data:
        game, marbles = line.split(':')
        game = int(game[5:])
        trials = tuple(val.split(' ') for val in marbles[1:].split('; '))
        for t in trials:
            for i in range(0, len(t), 2):
                val, marble = int(t[i]), t[i + 1].replace(',', '')
                games[game][marble] = max(games[game][marble], val)
    return games


def is_in_bounds(y: int, x: int, data: list) -> bool:
    return 0 <= y < len(data) and 0 <= x < len(data[y])


def day_3b_helper(data: list[str], y: int, x: int) -> int:
    def build_digit(y_inc: int, x_inc: int) -> Tuple[set, int]:
        indices = {(y + y_inc, x + x_inc)}
        start_y, start_x = y + y_inc, x + x_inc

        x_left, x_right, val_ = start_x - 1, start_x + 1, data[start_y][
            start_x]
        while 0 <= x_left and data[start_y][x_left] in digits:
            indices.add((start_y, x_left))
            val_ = data[start_y][x_left] + val_
            x_left -= 1
        while x_right < len(data[start_y]) and data[start_y][
            x_right] in digits:
            indices.add((start_y, x_right))
            val_ += data[start_y][x_right]
            x_right += 1

        return indices, int(val_) if val_ else 0

    used_indices, val1, val2 = set(), 0, 0
    for yi, xi in DIRECTIONS:
        if is_in_bounds(y + yi, x + xi, data) and data[y + yi][
            x + xi] in digits \
                and (y + yi, x + xi) not in used_indices:
            indices_, val = build_digit(yi, xi)
            val1, val2 = (val, val2) if not val1 else (val1, val)
            used_indices.update(indices_)
    return val1 * val2


def day_5_parse_mapping(mapping: str) -> Tuple[dict, dict]:
    ranges, keys = {}, {}
    for entry in mapping.split('\n')[1:]:
        dest, src, range_ = (int(i) for i in entry.split(' '))
        ranges[range(src, src + range_)] = range(dest, dest + range_)
        keys[src] = range(src, src + range_)
    return keys, ranges


def day_6_get_times_and_distances(part: str) -> Tuple[list, list]:
    times, distances = read_input(day=6)
    if part.upper() == 'A':
        times = map(int, times[times.index(':') + 1:].split())
        distances = map(int, distances[distances.index(':') + 1:].split())
    else:
        times = [int(''.join(times[times.index(':') + 1:].split()))]
        distances = [
            int(''.join(distances[distances.index(':') + 1:].split()))]
    return times, distances


def evaluate_hands(input_: list[list[str]]) -> list[Hand]:
    return sorted(map(_input_to_hand, input_),
                  key=lambda h: (h.type, tuple(CARD_FACE_VALS[c] for c in
                                               h.cards)),
                  reverse=True)


def _input_to_hand(hand: Tuple[str, ...]) -> Hand:
    cards, bid = hand
    return Hand(type=(_get_hand_type(cards)), cards=cards, bid=int(bid))


def _get_hand_type(cards: str) -> int:
    counts = sorted((count for count in Counter(cards).values()),
                    key=lambda x: -x)
    if counts[0] == 5:
        return 0
    elif counts[0] == 4:
        return 1
    elif counts[0] == 3 and counts[1] == 2:
        return 2
    elif counts[0] == 3:
        return 3
    if counts[0] == counts[1] == 2:
        return 4
    elif counts[0] == 2:
        return 5
    else:
        return 6


def _sort_hands(hand: Hand) -> Tuple[Any, tuple[int, ...]]:
    return hand.rank, tuple(CARD_FACE_VALS[c] for c in hand.cards)


if __name__ == '__main__':
    tests = ['32T3K', 'T55J5', 'KK677', 'KTJJT', 'QQQJA', '12J34']
    for t in tests:
        print(f'{t=} {_get_hand_type(t)=}')
