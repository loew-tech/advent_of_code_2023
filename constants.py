NUMBER_WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                'eight', 'nine']

WORD_TO_DIGIT = dict(zip(NUMBER_WORDS, range(1, 10)))

DIRECTIONS = tuple((i, j) for i in range(-1, 2)
                   for j in range(-1, 2) if not i == j == 0)

CARDINAL_DIRECTIONS = tuple((i, j) for i in range(-1, 2)
                        for j in range(-1, 2) if not abs(i) == abs(j))


CHAR_DIRECTIONS = {'U': (-1, 0), 'L': (0, -1), 'D': (1, 0), 'R': (0, 1)}


CARD_FACES = "AKQJT98765432"
CARD_FACE_VALS = dict(zip(CARD_FACES, range(6, len(CARD_FACES)+6)))
WILDCARD_FACE_VALS = {**CARD_FACE_VALS, 'J': len(CARD_FACES)+6}

PIPE_DIRECTIONS = {
    '|': {(1, 0), (-1, 0)}, '-': {(0, 1), (0, -1)}, 'L': {(0, -1), (1, 0)},
    'J': {(0, 1), (1, 0)}, '7': {(0, 1), (-1, 0)}, 'F': {(0, -1), (-1, 0)}
}


LIGHT_DIRECTIONS = dict(zip('^<>v', CARDINAL_DIRECTIONS))

LIGHT_DIRECTIONS_MAPPING = {
    ('>', '-'): '> ', ('>', '/'): '^ ', ('>', '\\'): 'v ', ('>', '|'): 'v^',
    ('<', '-'): '< ', ('<', '/'): 'v ', ('<', '\\'): '^ ', ('<', '|'): 'v^',
    ('^', '-'): '<>', ('^', '/'): '> ', ('^', '\\'): '< ', ('^', '|'): '^ ',
    ('v', '-'): '<>', ('v', '/'): '< ', ('v', '\\'): '> ', ('v', '|'): 'v '
}
