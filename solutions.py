import inspect
import re
import sys

from santas_bag.constants import NUMBER_WORDS, WORD_TO_DIGIT
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
