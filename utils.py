from collections import defaultdict


def read_input(day, delim='\n'):
    with open(f'inputs/day_{day}.txt') as f:
        data = f.read().split(delim)[:-1]
    return data


def parse_day_2():
    data, games = read_input(day=2), defaultdict(lambda: defaultdict(int))
    for line in data:
        game, marbles = line.split(':')
        game = int(game[5:])
        trials = tuple(val.split(' ') for val in marbles[1:].split('; '))
        for t in trials:
            for i in range(0, len(t), 2):
                val, marble = int(t[i]), t[i+1].replace(',', '')
                games[game][marble] = max(games[game][marble], val)
    return games
