number_words = ['one', 'two', 'three', 'four', 'five', 'six', 'seven',
                'eight', 'nine']

word_to_digit = dict(zip(number_words, range(1, 10)))

directions = tuple((i, j) for i in range(-1, 2)
                   for j in range(-1, 2) if not i == j == 0)
