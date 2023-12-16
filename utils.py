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


def evaluate_hands(input_: Tuple[Any, ...], part='A') -> list[Hand]:
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


def get_is_enclosed(perim: Set[Tuple[int, int]], pipes: list[str]):
    def is_enclosed(x, y: int):
        if (y, x) in perim:
            return 0
        y2, x2, cross_count = y, x, 0
        while is_in_bounds(y2, x2, pipes):
            cross_count += (y2, x2) in perim and pipes[y2][x2] not in 'L7'
            y2 += 1
            x2 += 1
        return cross_count % 2
    return is_enclosed


def get_galaxies_distance(sky: list[str]):
    copy, galaxies = _get_galaxies_and_sky_map(sky)
    sky_map, _ = _get_galaxies_and_sky_map(get_rotated_grid(copy))
    for _ in range(3):
        sky_map = get_rotated_grid(sky_map)
    galaxies = [(y, x) for y, row in enumerate(sky_map)
                for x, c in enumerate(row) if c == '#']
    sum_ = 0
    for i, (y, x) in enumerate(galaxies):
        for y1, x1 in galaxies[i+1:]:
            sum_ += abs(y-y1) + abs(x-x1)
    return sum_


def _get_galaxies_and_sky_map(sky: list[str|list]):
    copy, galaxies = [], set()
    for row in sky:
        copy.append(row)
        if '#' not in row:
            copy.append(row)
    return copy, galaxies


def get_rotated_grid(grid: Iterable[Iterable]):
    return [list(reversed(x)) for x in zip(*grid)]
