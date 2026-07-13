import inspect
import re
import sys
from ast import Tuple

from santas_bag.constants import NUMBER_WORDS, WORD_TO_DIGIT
from santas_bag.grid import find_all_in_grid, Grid, get_is_enclosed
from santas_bag.search import dfs
from santas_bag.utils import get_read_input, time_execution, get_naughty_or_nice

with open('.env') as f:
    session_ = f.readlines()[0]
read_input = get_read_input(2023, session_)

naughty_or_nice = get_naughty_or_nice(year=2023, session_id=session_)


@naughty_or_nice(day=1)
def day_1(part=1, testing=True) -> int:
    pattern = r'\d' if part == 1 else '(?=(' + '|'.join([r'\d', *NUMBER_WORDS]) + '))'
    print(pattern)

    conversion_dict = {
        **WORD_TO_DIGIT,
        **{str(i): i for i in range(1, 10)}
    }

    return sum(int(f'{conversion_dict[re.findall(pattern, line)[0]]}'
                   f'{conversion_dict[re.findall(pattern, line)[-1]]}') for
               line in read_input(day=1, testing=testing, part=part))



@naughty_or_nice(day=10)
def day_10(part=1, testing=True) -> int:
    print(testing)
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


@naughty_or_nice(day=11)
def day_11(part=1, testing=True) -> int:
    data = read_input(11, testing=testing, part=part)


if __name__ == '__main__':
    args_ = sys.argv[1:] if sys.argv[1:] else range(1, 26)
    members = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    funcs = {name: member for name, member in members
             if inspect.isfunction(member)}
    for i in args_:
        day = f'day_{i}'
        if day not in funcs:
            print(f'{day}() = NotImplemented')
            continue
        print(f'{day}() = {funcs[day](part=1, testing=True)}')
        print(f'{day}(part=2) = {funcs[day](part=2, testing=True)}\n')
