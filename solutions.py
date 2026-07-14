import inspect
import re
import sys
from ast import List, Tuple
from collections import defaultdict
from functools import reduce
from operator import mul
from string import digits

from santas_bag.constants import NUMBER_WORDS, WORD_TO_DIGIT, ALL_DIRECTIONS
from santas_bag.grid import find_all_in_grid, get_is_enclosed, get_inbounds
from santas_bag.parse import ints
from santas_bag.search import dfs
from santas_bag.utils import get_read_input, get_naughty_or_nice, get_read_and_solve, get_solve

with open('.env') as f:
    session_ = f.readlines()[0]
read_input = get_read_input(2023, session_)

naughty_or_nice = get_naughty_or_nice(year=2023, session_id=session_)


def day_1(part=1, testing=True) -> int:
    pattern = r'\d' if part == 1 else '(?=(' + '|'.join([r'\d', *NUMBER_WORDS]) + '))'

    conversion_dict = {
        **WORD_TO_DIGIT,
        **{str(i): i for i in range(1, 10)}
    }

    return sum(int(f'{conversion_dict[re.findall(pattern, line)[0]]}'
                   f'{conversion_dict[re.findall(pattern, line)[-1]]}') for
               line in read_input(day=1, testing=testing, part=part))


def day_2(part=1, testing=True) -> int:
    games = defaultdict(lambda: defaultdict(int))
    def parse(ln: str):
        game_str, marbles_ = ln.split(':')
        game = ints(game_str)[0]
        trials = tuple(val.split(' ') for val in marbles_[1:].split('; '))
        for t in trials:
            for i in range(0, len(t), 2):
                val, marble = int(t[i]), t[i + 1].replace(',', '')
                games[game][marble] = max(games[game][marble], val)

    read_input(day=2, testing=testing, parse=parse)
    truth = {'red': 12, 'green': 13, 'blue': 14}

    def compare(marbles_: dict) -> bool:
        return not any(truth[k_] < v for k_, v in marbles_.items())

    if part == 1:
        return sum(k for k, marbles in games.items() if compare(marbles))
    return sum(reduce(mul, marbles.values(), 1) for marbles in games.values())


def day_3(part=1, testing=True) -> int:
    grid = read_input(day=3, testing=testing, part=part)
    ignore = {*digits, '.'}
    inbounds = get_inbounds(grid)
    sum_, num, is_part = 0, '', False
    if part == 1:
        for y, row in enumerate(grid):
            for x, v in enumerate(row):
                if not v.isdigit():
                    sum_ += is_part * int(num or '0')
                    is_part = False
                    num = ''
                    continue
                num += v
                for yi, xi in ALL_DIRECTIONS:
                    is_part |= inbounds(y+yi, x+xi) and grid[y+yi][x+xi] not in ignore
        return sum_

    def day_3b_helper(y, x: int) -> int:
        def build_digit(y_inc, x_inc: int) -> Tuple[set, int]:
            indices = {(y + y_inc, x + x_inc)}
            start_y, start_x = y + y_inc, x + x_inc

            x_left, x_right, val_ = start_x - 1, start_x + 1, grid[start_y][
                start_x]
            while 0 <= x_left and grid[start_y][x_left] in digits:
                indices.add((start_y, x_left))
                val_ = grid[start_y][x_left] + val_
                x_left -= 1
            while x_right < len(grid[start_y]) and grid[start_y][x_right]\
                    in digits:
                indices.add((start_y, x_right))
                val_ += grid[start_y][x_right]
                x_right += 1

            return indices, int(val_) if val_ else 0

        used_indices, val1, val2 = set(), 0, 0
        for yi, xi in ALL_DIRECTIONS:
            if inbounds(y + yi, x + xi) and grid[y + yi][
                x + xi] in digits \
                    and (y + yi, x + xi) not in used_indices:
                indices_, val = build_digit(yi, xi)
                val1, val2 = (val, val2) if not val1 else (val1, val)
                used_indices.update(indices_)
        return val1 * val2

    return sum(sum((c == '*') * day_3b_helper(y, x) for x, c in
                   enumerate(line)) for y, line in enumerate(grid))


def day_10(part=1, testing=True) -> int:
    def get_first_move(ys_, xs_: int):
        if ys_ + 1 < len(pipes) and pipes[ys_ + 1][xs_] in '|JL':
            return ys_ + 1, xs_, (1, 0)
        if 0 <= ys_ - 1 and pipes[ys_ - 1][xs_] in '|7F':
            return ys_ - 1, xs_, (-1, 0)
        if xs_ + 1 < len(pipes[ys_]) and pipes[ys_][xs_ + 1] in '-J7':
            return ys_, xs_ + 1, (0, 1)
        if 0 <= xs_ - 1 and pipes[ys_][xs_ - 1] in '-FL':
            return ys_, xs_ - 1, (0, -1)
        return None

    pipes = read_input(day=10, parse=lambda ln: list(ln), testing=testing, part=part)
    pipe_directions = {
        '|': {(1, 0), (-1, 0)}, '-': {(0, 1), (0, -1)}, 'L': {(0, -1), (1, 0)},
        'J': {(0, 1), (1, 0)}, '7': {(0, 1), (-1, 0)}, 'F': {(0, -1), (-1, 0)}
    }

    def get_neighbors(node, space, *args, **kwargs):
        y, x, delta = node
        incs1, incs2 = pipe_directions[space[y][x]]
        yi, xi = incs2 if incs1 == delta else incs1
        yield y - yi, x - xi, (-yi, -xi)


    perimeter = set()
    start_pos = find_all_in_grid(pipes, 'S')[0]
    ys, xs = start_pos
    start = get_first_move(ys, xs)
    dfs(start,
        pipes,
        lambda n, _, *args, **kwargs: (n[0], n[1]) == start_pos,
        get_neighbors,
        on_visit=lambda n, steps, s: perimeter.add((n[0], n[1]))
    )

    if part == 1:
        return len(perimeter) // 2


    pipes[ys][xs] = '|' if not testing else '7'
    enclosed = get_is_enclosed(pipes, perimeter)
    return sum(enclosed(y, x) for y in range(len(pipes)) for x in range(len(pipes[y])))


def day_11(part=1, testing=True) -> int:
    data = read_input(11, testing=testing, part=part)


if __name__ == '__main__':
    testing_ = '-t' in sys.argv[1:] or '-testing' in sys.argv[1:]
    print(f'{testing_=}')
    sys_args = [int(i) for i in sys.argv[1:] if i.isnumeric()]
    args_ = sys_args if sys_args else range(1, 26)

    members = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    funcs = {name: member for name, member in members
             if inspect.isfunction(member)}

    solve = get_solve(2023, session_)
    for i in args_:
        # if i in {1, 2, 10}:
        day = f'day_{i}'
        if day not in funcs:
            print(f'{day}() = NotImplemented')
            continue

        def part_1(testing=testing_):
            return funcs[day](part=1, testing=testing)

        def part_2(testing=testing_):
            return funcs[day](part=2, testing=testing)

        print(f'\n===day_{i}===')
        res1, res2 = solve(i,
                           part_1,
                           part_2,
                           testing=testing_)
        print(f'{day}() = {res1}')
        print(f'{day}(part=2) = {res2}')
        # print(f'{day}() = {funcs[day](part=1, testing=True)}')
        # print(f'{day}(part=2) = {funcs[day](part=2, testing=True)}\n')
