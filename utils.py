from collections import defaultdict, Counter, namedtuple
from string import digits
from typing import Tuple, Callable, Any, Generator, DefaultDict, Set, Iterable, \
    List

from classes import Searcher
from constants import *

Hand = namedtuple('Hand', ['type', 'cards', 'bid'])


def read_input(day: int | str, delim='\n') -> list[str]:
    with open(f'inputs/day_{day}.txt') as f:
        return f.read().rstrip().split(delim)


def parse_day_2() -> DefaultDict[int, DefaultDict[str, int]]:
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


def get_is_in_bounds(data: List[Iterable]) -> Callable[[int, int], bool]:
    return lambda y, x: is_in_bounds(y, x, data)


def is_in_bounds(y, x: int, data: List[Iterable]) -> bool:
    return 0 <= y < len(data) and 0 <= x < len(data[y])


def day_3b_helper(data: list[str], y, x: int) -> int:
    def build_digit(y_inc, x_inc: int) -> Tuple[set, int]:
        indices = {(y + y_inc, x + x_inc)}
        start_y, start_x = y + y_inc, x + x_inc

        x_left, x_right, val_ = start_x - 1, start_x + 1, data[start_y][start_x]
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
    for yi, xi in DIRECTIONS:
        if is_in_bounds(y + yi, x + xi, data) and data[y + yi][x + xi] in digits \
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


def evaluate_hands(input_: Tuple[list[str], ...], part='A') -> list[Hand]:
    _input_to_hand = _get_input_to_hand(part)
    face_vals = CARD_FACE_VALS if part.upper() == 'A' else WILDCARD_FACE_VALS
    return sorted(map(_input_to_hand, input_),
                  key=lambda h: (h.type, tuple(face_vals[c] for c in
                                               h.cards)),
                  reverse=True)


def _get_input_to_hand(part: str) -> Callable[[Tuple[str, ...]], Hand]:
    def _input_to_hand(hand: Tuple[str, ...]) -> Hand:
        cards, bid = hand
        return Hand(type=(_get_hand_type(cards, part)), cards=cards,
                    bid=int(bid))

    return _input_to_hand


def _get_hand_type(cards: str, part: str) -> int:
    wild_cards_offset = cards.count('J') * (not part.upper() == 'A')
    cards = cards if part.upper() == 'A' else cards.replace('J', '')

    counts = sorted((count for count in Counter(cards).values()),
                    key=lambda x: -x)

    if wild_cards_offset == 5 or counts[0] + wild_cards_offset == 5:
        return 0
    elif counts[0] + wild_cards_offset == 4:
        return 1
    elif counts[0] + wild_cards_offset == 3 and counts[1] == 2:
        return 2
    elif counts[0] + wild_cards_offset == 3:
        return 3
    if counts[0] == 2 and counts[1] + wild_cards_offset == 2:
        return 4
    elif counts[0] + wild_cards_offset == 2:
        return 5
    else:
        return 6


def day_8_parse_input() -> Tuple[str, dict]:
    def _to_lr_dict(m: str) -> dict:
        l, r = m[m.index('(') + 1: m.index(')')].split(', ')
        return {'L': l, 'R': r}

    sequence, mapping = read_input(day=8, delim='\n\n')
    mapping = {m[:m.index(' =')]: _to_lr_dict(m) for m in mapping.split('\n')}
    return sequence, mapping


def get_day_8_step_counter(
        sequence: str,
        mapping: dict,
        part: str) -> Callable[[str], int]:

    def count_steps(key: str) -> int:
        count = 0
        while count := count + 1:
            key = mapping[key][sequence[(count - 1) % len(sequence)]]
            if key == 'ZZZ' if part.lower() == 'A' else key[-1] == 'Z':
                return count

    return count_steps


def get_next_history(history: list[int]) -> int:
    sum_, diffs = 0, history
    while not len(set(diffs)) == 1:
        sum_ += diffs[-1]
        diffs = tuple(v - diffs[i] for i, v in enumerate(diffs[1:]))
    return sum_ + diffs[-1]


def get_loop_perimeter(pipes: list[str]) -> Set[Tuple[int, int]]:
    sy, sx = _find_start(pipes, 'S')
    searches = [Searcher(*start) for start in _get_first_move(pipes, sy, sx)]
    perimeter, positions = {(sy, sx)}, {s.location for s in searches}
    while not perimeter.issuperset(positions):
        perimeter.update(positions)
        for s in searches:
            new_y, new_x = s.next_location
            s.current_val = pipes[new_y][new_x]
        positions = {s.location for s in searches}
    return perimeter


def _find_start(grid: list[Any] | Tuple[Any], target: Any) -> Tuple[int, int]:
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == target:
                return y, x
    raise Exception(f'Err searching for target: {target} not found in grid')


def _get_first_move(pipes: list[str], ys, xs: int) -> Generator:
    if ys+1 < len(pipes) and pipes[ys+1][xs] in '|JL':
        yield ys+1, xs, 1, 0, pipes[ys+1][xs]
    if 0 <= ys-1 and pipes[ys-1][xs] in '|7F':
        yield ys-1, xs, -1, 0, pipes[ys-1][xs]
    if xs+1 < len(pipes[ys]) and pipes[ys][xs+1] in '-J7':
        yield ys, xs+1, 0, 1, pipes[ys][xs+1]
    if 0 <= xs-1 and pipes[ys][xs-1] in '-FL':
        yield ys, xs-1, 0, -1, pipes[ys][xs-1]


def bfs(grid: list[list[any] | str], to_search: Iterable[Tuple[int, int]],
        increments=CARDINAL_DIRECTIONS, visited=None, in_bounds=None) -> set:
    visited = visited if visited is not None else set()
    in_bounds = in_bounds if in_bounds is not None else get_is_in_bounds(grid)


    copy = [[v for v in r] for r in grid]
    _print_pipes(copy)

    for y, x in visited:
        copy[y][x] = '*'

    for y, x in to_search:
        copy[y][x] = 'O'

    while to_search:
        print(f'{len(to_search)=} {to_search=}')
        _print_pipes(copy)
        visited.update(to_search)
        next_search = set()
        for y, x in to_search:
            for yi, xi in increments:
                if (y+yi, x+xi) not in visited and in_bounds(y+yi, x+xi):
                    next_search.add((y+yi, x+xi))
                    copy[y+yi][x+xi] = 'O'
        to_search = next_search

    _print_pipes(copy)
    return visited


def _print_pipes(p):
    for line in p:
        print(''.join(line))
    print('\n***********\n')


