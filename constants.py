NUMBER_WORDS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                'eight', 'nine']

WORD_TO_DIGIT = dict(zip(NUMBER_WORDS, range(1, 10)))

DIRECTIONS = tuple((i, j) for i in range(-1, 2)
                   for j in range(-1, 2) if not i == j == 0)


CARD_FACES = "AKQJT98765432"
CARD_FACE_VALS = dict(zip(CARD_FACES, range(6, len(CARD_FACES)+6)))
