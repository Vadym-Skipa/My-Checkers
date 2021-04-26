from __future__ import annotations
from typing import Union, Tuple

PositionFormat = Union[int, str]


class ImpossiblePositionError(Exception):
    pass


class CheckersPosition:
    HORIZONTAL_LINES = "12345678"
    VERTICAL_LINES = "ABCDEFGH"

    def __new__(cls, horizontal_line: PositionFormat, vertical_line: PositionFormat):
        if isinstance(horizontal_line, str):
            horizontal_line = cls.HORIZONTAL_LINES.find(horizontal_line.upper())
            if horizontal_line == -1:
                raise ImpossiblePositionError
        elif isinstance(horizontal_line, int):
            if not 0 <= horizontal_line <= 7:
                raise ImpossiblePositionError
        else:
            raise TypeError
        if isinstance(vertical_line, str):
            vertical_line = cls.VERTICAL_LINES.find(vertical_line.upper())
            if vertical_line == -1:
                raise ImpossiblePositionError
        elif isinstance(vertical_line, int):
            if not 0 <= vertical_line <= 7:
                raise ImpossiblePositionError
        else:
            raise TypeError
        if (horizontal_line + vertical_line) % 2 != 0:
            raise ImpossiblePositionError
        return super(CheckersPosition, cls).__new__(cls)

    def __init__(self, horizontal: int, vertical: int):
        if isinstance(horizontal, str):
            self._horizontal_line = self.HORIZONTAL_LINES.find(horizontal.upper())
        else:
            self._horizontal_line = horizontal
        if isinstance(vertical, str):
            self._vertical_line = self.VERTICAL_LINES.find(vertical.upper())
        else:
            self._vertical_line = vertical

    @property
    def horizontal_line(self):
        return self.HORIZONTAL_LINES[self._horizontal_line]

    @property
    def horizontal_line_int(self):
        return self._horizontal_line

    @property
    def vertical_line(self):
        return self.VERTICAL_LINES[self._vertical_line]

    @property
    def vertical_line_int(self):
        return self._vertical_line

    def __add__(self, other: CheckersWay):
        outcome = CheckersPosition(self.horizontal_line_int + other.vertical_way,
                                   self.vertical_line_int + other.horizontal_way)
        return outcome

    def __sub__(self, other):
        return self + (-other)

    def __repr__(self):
        return f"{self.horizontal_line}{self.vertical_line}"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __copy__(self):
        copy_position = CheckersPosition(self.horizontal_line_int, self.vertical_line_int)
        return copy_position


class CheckersWay:

    def __init__(self, vertical_way: int = 0, horizontal_way: int = 0):
        self._vertical_way = vertical_way
        self._horizontal_way = horizontal_way

    @property
    def vertical_way(self):
        return self._vertical_way

    @property
    def horizontal_way(self):
        return self._horizontal_way

    def __neg__(self):
        return CheckersWay(- self.vertical_way, - self.horizontal_way)

    def __eq__(self, other: CheckersWay):
        return self.vertical_way == other.vertical_way and self.horizontal_way == self.horizontal_way

    def __add__(self, other: CheckersWay):
        return CheckersWay(self.vertical_way + other.vertical_way, self.horizontal_way + other.horizontal_way)

    def __mul__(self, other: int):
        return CheckersWay(self.vertical_way * other, self.horizontal_way * other)

    def __repr__(self):
        return f"{self.vertical_way}{self.horizontal_way}"


class CheckersMove:

    def __init__(self, position: CheckersPosition, way: Tuple[CheckersWay, ...]):
        self._position: CheckersPosition = position
        self._way: Tuple[CheckersWay, ...] = way

    @property
    def position(self):
        return self._position

    @property
    def way(self):
        return self._way

    def __str__(self):
        return f"The checker at a point {self.position} moves along the way: {self.way}"

    def __add__(self, other: Union[CheckersWay, Tuple[CheckersWay, ...]]):
        if isinstance(other, CheckersWay):
            return CheckersMove(self.position, self.way + (other,))
        else:
            return CheckersMove(self.position, self.way + other)

    def __iter__(self):
        return iter((self.position, *self.way))
