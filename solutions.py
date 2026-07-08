import inspect
import re
import sys
from ast import Tuple

from santas_bag.constants import NUMBER_WORDS, WORD_TO_DIGIT
from santas_bag.grid import find_all_in_grid, Grid, get_is_enclosed
from santas_bag.search import dfs
from santas_bag.utils import get_read_input, time_execution

with open('.env') as f:
    session_id = f.readlines()[0]
read_input = get_read_input(2023, session_id)


@time_execution
def day_1(part_1=True) -> int:
    pattern = r'\d' if part_1 else '(?=(' + '|'.join([r'\d', *NUMBER_WORDS]) + '))'

    conversion_dict = {
        **WORD_TO_DIGIT,
        **{str(i): i for i in range(1, 10)}
    }

    return sum(int(f'{conversion_dict[re.findall(pattern, line)[0]]}'
                   f'{conversion_dict[re.findall(pattern, line)[-1]]}') for
               line in read_input(day=1))


@time_execution
def day_10(part_1=True) -> int:
    def get_first_move(start_: Tuple[int, int]):
        ys, xs = start_
        if ys + 1 < len(pipes) and pipes[ys + 1][xs] in '|JL':
            return ys + 1, xs, (1, 0)
        if 0 <= ys - 1 and pipes[ys - 1][xs] in '|7F':
            return ys - 1, xs, (-1, 0)
        if xs + 1 < len(pipes[ys]) and pipes[ys][xs + 1] in '-J7':
            return ys, xs + 1, (0, 1)
        if 0 <= xs - 1 and pipes[ys][xs - 1] in '-FL':
            return ys, xs - 1, (0, -1)
        return None

    pipes = read_input(day=10, parse=lambda ln: list(ln))
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
    start = get_first_move(start_pos)
    dfs(start,
        pipes,
        lambda n, _, *args, **kwargs: (n[0], n[1]) == start_pos,
        get_neighbors,
        on_visit=lambda n, steps, s: perimeter.add((n[0], n[1]))
    )

    if part_1:
        return len(perimeter) // 2

    ys, xs = start_pos
    pipes[ys][xs] = '|'
    enclosed = get_is_enclosed(pipes, perimeter)
    return sum(enclosed(y, x) for y in range(len(pipes)) for x in range(len(pipes[y])))


if __name__ == '__main__':
    args_ = (f'day_{i}' for i in (sys.argv[1:] if
                                  sys.argv[1:] else range(1, 26)) if
             type(i) == int or str(i).isnumeric())
    members = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    funcs = {name: member for name, member in members
             if inspect.isfunction(member)}
    for day in args_:
        if day not in funcs:
            print(f'{day}() = NotImplemented')
            continue
        print(f'{day}() = {funcs[day]()}')
        print(f'{day}(part=2) = {funcs[day](part_1=False)}\n')
