from typing import Tuple

from constants import PIPE_DIRECTIONS as pd


class Searcher:

    def __init__(self, y, x, yi, xi: int, val: str) -> None:
        self._y, self._x = y, x
        self._y_inc, self._x_inc, self._val = yi, xi, val
        self._set_new_inc()

    @property
    def current_val(self) -> str:
        return self._val

    @current_val.setter
    def current_val(self, val: str) -> None:
        self._val = val
        self._set_new_location()

    @property
    def location(self) -> Tuple[int, int]:
        return self._y, self._x

    @property
    def next_location(self) -> Tuple[int, int]:
        return self._y + self._y_inc, self._x + self._x_inc

    def _set_new_location(self) -> None:
        self._y, self._x = self.next_location
        self._set_new_inc()

    def _set_new_inc(self) -> None:
        self._y_inc, self._x_inc = (-i for i in (pd[self._val] - {(
            self._y_inc, self._x_inc)}).pop())

    def __repr__(self) -> str:
        return f'Searcher(y={self._y}, x={self._x}, y_inc={self._y_inc}, ' \
               f'x_inc={self._x_inc}, current_val={self._val})'
