from __future__ import annotations
from typing import Union, Dict
import checkers_position as pos


class Checker:

    __slots__ = ("_direction", "_crowned")

    def __init__(self, direction: int, crowned: bool = False):
        if direction > 0:
            self._direction = +1
        else:
            self._direction = -1
        self._crowned = crowned

    @property
    def direction(self):
        return self._direction

    @property
    def crowned(self):
        return self._crowned

    def crowning(self):
        self._crowned = True

    def __str__(self):
        if self._direction == +1:
            direction = "+1"
        else:
            direction = "-1"
        if self._crowned:
            name = "King"
        else:
            name = "Man"
        return name + " " + direction

    def __copy__(self):
        return Checker(self.direction, self.crowned)

BoardPosition = Union[None, Checker]


class CheckersBoard:

    def __init__(self):
        self.board: Dict[pos.CheckersPosition, BoardPosition] = {}
        temp_flag = 0
        for horizontal_line in range(8):
            for vertical_line in range(temp_flag, 8, 2):
                self.board.update({pos.CheckersPosition(horizontal_line, vertical_line): None})
            if temp_flag == 0:
                temp_flag = 1
            else:
                temp_flag = 0

    def append(self, position: pos.CheckersPosition, checker: Checker):
        self.board[position] = checker

    def remove(self, position: pos.CheckersPosition):
        self.board[position] = None

    def get_element(self, position: pos.CheckersPosition) -> BoardPosition:
        return self.board[position]

    def __iter__(self):
        return iter(self.board.items())

    def keys(self):
        return self.board.keys()

    def values(self):
        return self.board.values()

    def copy(self):
        copy_board = CheckersBoard()
        for key, value in self.board.items():
            if value:
                copy_board.append(key, value.__copy__())
        return copy_board