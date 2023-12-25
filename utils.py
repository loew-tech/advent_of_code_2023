from collections import defaultdict, Counter
from string import digits
from typing import Tuple, Callable, Any, Generator, DefaultDict, Set, Iterable, \
    List, Dict

from classes import Hand, Searcher, LightBeam, DigInstruction
from constants import *


def read_input(day: int | str, delim='\n') -> List[str]:
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
    if ys + 1 < len(pipes) and pipes[ys + 1][xs] in '|JL':
        yield ys + 1, xs, 1, 0, pipes[ys + 1][xs]
    if 0 <= ys - 1 and pipes[ys - 1][xs] in '|7F':
        yield ys - 1, xs, -1, 0, pipes[ys - 1][xs]
    if xs + 1 < len(pipes[ys]) and pipes[ys][xs + 1] in '-J7':
        yield ys, xs + 1, 0, 1, pipes[ys][xs + 1]
    if 0 <= xs - 1 and pipes[ys][xs - 1] in '-FL':
        yield ys, xs - 1, 0, -1, pipes[ys][xs - 1]


def get_is_enclosed(perim: Set[Tuple[int, int]],
                    pipes: list[str]) -> Callable[[int, int], int]:
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


def get_galaxies_distance(sky: list[str], offset=1) -> int:
    y_indices = _get_galaxies_and_sky_map(sky)
    x_indices = _get_galaxies_and_sky_map(get_rotated_grid(sky))
    galaxies = [(y, x) for y, row in enumerate(sky)
                for x, c in enumerate(row) if c == '#']
    sum_ = 0
    for i, (y, x) in enumerate(galaxies):
        for y1, x1 in galaxies[i + 1:]:
            sum_ += abs(y - y1) + abs(x - x1)
            y_max, y_min = max(y, y1), min(y, y1)
            x_max, x_min = max(x, x1), min(x, x1)
            sum_ += offset * len(
                set(range(y_min, y_max + 1)).intersection(y_indices))
            sum_ += offset * len(
                set(range(x_min, x_max + 1)).intersection(x_indices))
    return sum_


def _get_galaxies_and_sky_map(sky: List[str | list]) -> Set[int]:
    return {y for y, row in enumerate(sky) if '#' not in row}


def parse_day_12() -> Tuple[List[str], List[List[int]]]:
    springs, records = [], []
    for line in read_input(day=12):
        s, r = line.split()
        r = [int(i) for i in r.split(',')]
        springs.append(s + '.')
        records.append(r)
    return springs, records


def get_reflection_val(data: List[List[str] | str],
                       allowed_diffs=0) -> int:
    vertical_reflections = _find_reflections(data, allowed_diffs)
    sum_ = sum(y for y in vertical_reflections) * 100
    rotated = get_rotated_grid(data)
    horizontal_reflections = _find_reflections(rotated, allowed_diffs)
    return sum_ + sum(y for y in horizontal_reflections)


def _find_reflections(grid: List[List[str] | str],
                      allowed_diffs: int) -> List[int]:
    return [y for y, line in enumerate(grid) if
            _is_reflection(grid, y, allowed_diffs)]


def _is_reflection(grid: List[List[str] | str], index,
                   allowed_diffs: int) -> bool:
    dif_count = 0
    size = index if index < len(grid) // 2 else len(grid) - index
    for i in range(size):
        diffs = sum(not val == grid[index - i - 1][x] for x, val in
                    enumerate(grid[index + i]))
        dif_count += diffs
        if diffs > 1 or dif_count > allowed_diffs:
            return False
    return dif_count == allowed_diffs


def cycle_boulders(boulders: List[str], num_cycles=1,
                   num_rotations=1) -> List[List[str]]:
    observed, cycles, hashable = {}, {}, None
    for i in range(num_cycles):
        hashable = grid_to_hashable(boulders)
        cycles[i] = boulders
        if hashable in observed:
            break
        observed[grid_to_hashable(boulders)] = i
        for _ in range(num_rotations):
            boulders = roll_boulders(boulders)
            if num_rotations > 1:
                boulders = get_rotated_grid(boulders)

    if num_cycles > 1:
        offset = observed[hashable]
        cycle_len = len(observed) - offset
        key = (1_000_000_000 - offset) % cycle_len + offset
        grid = cycles[key]
    else:
        grid = boulders
    return grid


def roll_boulders(grid: List[str]) -> List[List[str]]:
    copy_ = [[x for x in row] for row in grid]
    for x in range(len(grid[0])):
        last_boulder = -1
        for y in range(len(grid)):
            if grid[y][x] == '#':
                last_boulder = y
            elif grid[y][x] == 'O':
                copy_[y][x], copy_[last_boulder + 1][x] = '.', 'O'
                last_boulder += 1
    return copy_


def get_hash_val(str_: str) -> int:
    val = 0
    for c in str_:
        val = ((val + ord(c)) * 17) % 256
    return val


def day_15b_helper(data: List[str]):
    boxes, sum_ = populate_boxes(data), 0
    for i, box in enumerate(boxes, start=1):
        index = 1
        # Note, this step takes advantage of dicts being ordered
        for val in box.values():
            sum_ += i * val * index
            index += 1
    return sum_


def populate_boxes(data: List[str]) -> List[Dict[str, int]]:
    boxes = [{} for _ in range(256)]
    for entry in data:
        if '=' in entry:
            label, len_length = entry.split('=')
            hash_ = get_hash_val(label)
            boxes[hash_][label] = int(len_length)
        else:
            label = entry.split('-')[0]
            hash_ = get_hash_val(label)
            if label in boxes[hash_]:
                del boxes[hash_][label]
    return boxes


def light_traversal(lights: List[str], start_y=0, start_x=0, starting_dir='>'):
    s1, s2 = starting_dir, ''
    if not lights[start_y][start_x] == '.':
        s1, s2 = LIGHT_DIRECTIONS_MAPPING[(starting_dir,
                                           lights[start_y][start_x])]
    to_search = {LightBeam(y=start_y, x=start_x, direction=s1)}
    visited = {(start_y, start_x, s1)}
    if s2.strip():
        to_search.add(LightBeam(y=start_y, x=start_x, direction=s2))
        visited.add((start_y, start_x, s2))
    get_light_dirs = _get_get_light_directions(lights)
    while to_search:
        next_search = []
        for light in to_search:
            light.increment_location()
            y, x = light.location
            if (y, x, light.direction) in visited or \
                    not is_in_bounds(y, x, lights):
                continue
            visited.add((y, x, light.direction))
            a, b = get_light_dirs(y, x, light.direction)
            if a.strip():
                light.direction = a
                next_search.append(light)
            if b.strip():
                next_search.append(LightBeam(y, x, b))
        to_search = next_search
    return visited


def _get_get_light_directions(lights: List[str]) -> Callable[[int, int, str],
                                                             str]:
    def _get_light_directions(y, x: int, direction: str) -> str:
        loc = lights[y][x]
        if loc == '.':
            return direction + ' '
        return LIGHT_DIRECTIONS_MAPPING[(direction, loc)]

    return _get_light_directions


def parse_day_18() -> Iterable[DigInstruction]:
    def lint_to_instruction(line: str) -> DigInstruction:
        d, dist, hex_ = line.split()
        return DigInstruction(direction=d, distance=int(dist), hex=hex_)

    return map(lint_to_instruction, read_input(day=18))


def dig_lagoon(instructions: Iterable[DigInstruction]) -> Set[Tuple[int, int]]:
    head = (0, 0)
    perim = {head}
    for instr in instructions:
        yi, xi = CHAR_DIRECTIONS[instr.direction]
        y, x = head
        count = 0
        while count < instr.distance:
            count += 1
            y += yi
            x += xi
            head = (y, x)
            perim.add(head)
    return perim


def get_lagoon_size(perim: Set[Tuple[int, int]]) -> Any:
    y_max, y_min = max(perim)[0], min(perim)[0]
    x_max, x_min = max(i[1] for i in perim), min(i[1] for i in perim)

    y_range = range(y_min, y_max + 1)
    x_range = range(x_min, x_max + 1)

    def is_corner(y_, x_: int):
        if not (y_, x_) in perim:
            return False
        if (y_ - 1, x_) in perim and (y_, x_ + 1) in perim:
            return True
        return (y_ + 1, x_) in perim and (y_, x_ - 1) in perim

    sum_ = 0
    for y in y_range:
        for x in x_range:
            y2, x2, cross_count = y, x, 0
            while y2 in y_range and x2 in x_range:
                cross_count += (y2, x2) in perim and not is_corner(y2, x2)
                x2 += 1
                y2 += 1
            sum_ += cross_count % 2 or (y, x) in perim

    return sum_


def get_rotated_grid(grid: Iterable[Iterable]) -> List[List[Any]]:
    return [list(reversed(x)) for x in zip(*grid)]


def grid_to_hashable(grid: Iterable[Iterable]) -> Tuple[Tuple[Any, ...], ...]:
    return tuple(tuple(row) for row in grid)


def print_grid(grid: Iterable[Iterable], spacer='') -> None:
    for row in grid:
        print(spacer.join(str(i) for i in row))
