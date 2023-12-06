from collections import defaultdict
from string import digits

from constants import directions


def read_input(day: int | str, delim='\n'):
    with open(f'inputs/day_{day}.txt') as f:
        return f.read().split(delim)[:-1]


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

    def build_digit(y_inc: int, x_inc: int) -> (set, int):
        indices = {(y + y_inc, x + x_inc)}
        start_y, start_x = y + y_inc, x + x_inc

        x_left, x_right, val_ = start_x - 1, start_x + 1, data[start_y][
            start_x]
        while 0 <= x_left and data[start_y][x_left] in digits:
            indices.add((start_y, x_left))
            val_ = data[start_y][x_left] + val_
            x_left -= 1
        while x_right < len(data[start_y]) and data[start_y][x_right] in digits:
            indices.add((start_y, x_right))
            val_ += data[start_y][x_right]
            x_right += 1

        return indices, int(val_) if val_ else 0

    used_indices, val1, val2 = set(), 0, 0
    for yi, xi in directions:
        if is_in_bounds(y+yi, x+xi, data) and data[y + yi][x + xi] in digits \
                and (y + yi, x + xi) not in used_indices:
            indices_, val = build_digit(yi, xi)
            val1, val2 = (val, val2) if not val1 else (val1, val)
            used_indices.update(indices_)
    return val1 * val2
