from __future__ import annotations
from random import choice
import checkers_position
import checkers_game_master


class RandomCheckersPlayer(checkers_game_master.CheckersPlayer):

    def choice_move(self, list_of_moves) -> checkers_position.CheckersMove:
        return choice(list_of_moves)
