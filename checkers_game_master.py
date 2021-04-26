from checkers_elements import CheckersBoard, Checker
from checkers_position import CheckersPosition, CheckersWay, CheckersMove, ImpossiblePositionError
from typing import Tuple, List
from abc import abstractmethod, ABC


class CheckersGameRules:

    @classmethod
    def move_checker(cls, move: CheckersMove, board: CheckersBoard):
        position = move.position
        checker = board.get_element(position)
        for way in move.way:
            board.remove(position)
            position += way
            if cls._check_of_crowned(checker, position):
                checker.crowning()
            board.append(position, checker)

    @classmethod
    def _check_of_crowned(cls, checker: Checker, position: CheckersPosition):
        if checker.crowned:
            return True
        else:
            if checker.direction == 1:
                return True if position.horizontal_line_int == 7 else False
            else:
                return True if position.horizontal_line_int == 0 else False

    @classmethod
    def get_possible_moves(cls, players_positions: List[CheckersPosition], board: CheckersBoard) -> Tuple[CheckersMove]:
        possible_moves_list: List[CheckersMove] = list()
        peace_flag = True
        for position in players_positions:
            if peace_flag:
                peace_moves = cls._get_possible_piece_moves_for_checker(position, board)
                possible_moves_list.extend(peace_moves)
            war_moves = cls._get_possible_war_moves_for_checker(position, board)
            if peace_flag and war_moves:
                peace_flag = False
                possible_moves_list = []
            possible_moves_list.extend(war_moves)
        possible_moves = tuple(possible_moves_list)
        return possible_moves

    @classmethod
    def _get_possible_piece_moves_for_checker(cls, start_position: CheckersPosition, board: CheckersBoard)\
            -> List[CheckersMove]:
        checker = board.get_element(start_position)
        if checker.crowned:
            possible_moves = cls._get_possible_piece_moves_for_king(start_position, board)
        else:
            possible_moves = cls._get_possible_piece_moves_for_man(start_position, board)
        return possible_moves

    @classmethod
    def _get_possible_piece_moves_for_man(cls, start_position: CheckersPosition, board: CheckersBoard)\
            -> List[CheckersMove]:
        possible_moves: List[CheckersMove] = list()
        checker: Checker = board.get_element(start_position)
        ways = (CheckersWay(checker.direction, -1), CheckersWay(checker.direction, 1))
        for way in ways:
            try:
                new_position = start_position + way
            except ImpossiblePositionError:
                continue
            else:
                if not board.get_element(new_position):
                    possible_moves.append(CheckersMove(start_position, (way,)))
        return possible_moves

    @classmethod
    def _get_possible_piece_moves_for_king(cls, start_position: CheckersPosition, board: CheckersBoard)\
            -> List[CheckersMove]:
        possible_moves: List[CheckersMove] = list()
        ways = (CheckersWay(x, y) for x, y in ((1, 1), (1, -1), (-1, 1), (-1, -1)))
        for way in ways:
            new_position = start_position
            temp_ways = list()
            while True:
                try:
                    new_position += way
                except ImpossiblePositionError:
                    break
                else:
                    if not board.get_element(new_position):
                        temp_ways.append(way)
                        possible_moves.append(CheckersMove(start_position, tuple(temp_ways)))
                    else:
                        break
        return possible_moves

    @classmethod
    def _get_possible_war_moves_for_checker(cls, start_position: CheckersPosition, board: CheckersBoard)\
            -> List[CheckersMove]:
        checker = board.get_element(start_position)
        if checker.crowned:
            possible_moves = cls._get_possible_war_moves_for_king(start_position, board)
        else:
            possible_moves = cls._get_possible_war_moves_for_man(start_position, board)
        return possible_moves

    @classmethod
    def _check_battle_moves_man(cls, start_position: CheckersPosition, ways: Tuple[CheckersWay, CheckersWay],
                                board: CheckersBoard) -> bool:
        if board.get_element(start_position + ways[0]):
            if board.get_element(start_position).direction != board.get_element(start_position + ways[0]).direction:
                if not board.get_element(start_position + ways[0] + ways[1]):
                    return True
        return False

    @classmethod
    def _check_battle_moves_king(cls, start_position: CheckersPosition, ways: Tuple[CheckersWay, ...],
                                 board: CheckersBoard) -> bool:
        position = start_position
        checker = board.get_element(position)
        ways_iter = iter(ways)
        flag = True
        while flag:
            try:
                position += next(ways_iter)
                flag = not bool(board.get_element(position))
            except StopIteration:
                return False
        if board.get_element(position).direction == checker.direction:
            return False
        try:
            position += next(ways_iter)
        except StopIteration:
            return False
        flag = not bool(board.get_element(position))
        while flag:
            try:
                position += next(ways_iter)
                flag = not bool(board.get_element(position))
            except StopIteration:
                return True
        return False

    @classmethod
    def _get_possible_war_moves_for_man(cls, start_position: CheckersPosition, board: CheckersBoard)\
            -> List[CheckersMove]:
        possible_moves: List[CheckersMove] = list()
        ways = (CheckersWay(x, y) for x, y in ((1, 1), (1, -1), (-1, 1), (-1, -1)))
        for way in ways:
            try:
                if cls._check_battle_moves_man(start_position, (way, way), board):
                    possible_move = CheckersMove(start_position, (way, way))
                    new_board = board.copy()
                    end_position = start_position + way + way
                    cls.move_checker(possible_move, new_board)
                    if cls._check_of_crowned(board.get_element(start_position), end_position):
                        adding_piece_of_move = cls._get_possible_war_moves_for_king(end_position, new_board)
                    else:
                        adding_piece_of_move = cls._get_possible_war_moves_for_man(end_position, new_board)
                    if adding_piece_of_move:
                        possible_moves.extend(possible_move + move.way for move in adding_piece_of_move)
                    possible_moves.append(possible_move)

            except ImpossiblePositionError:
                continue
        return possible_moves

    @classmethod
    def _get_possible_war_moves_for_king(cls, start_position: CheckersPosition, board: CheckersBoard)\
            -> List[CheckersMove]:
        possible_moves: List[CheckersMove] = list()
        ways = (CheckersWay(x, y) for x, y in ((1, 1), (1, -1), (-1, 1), (-1, -1)))
        for way in ways:
            check_ways = [way]
            for _ in range(8):
                check_ways.append(way)
                try:
                    if cls._check_battle_moves_king(start_position, tuple(check_ways), board):
                        possible_move = CheckersMove(start_position, tuple(check_ways))
                        new_board = board.copy()
                        end_position = start_position
                        for el in check_ways:
                            end_position += el
                        cls.move_checker(possible_move, new_board)
                        adding_piece_of_move = cls._get_possible_war_moves_for_king(end_position, new_board)
                        if adding_piece_of_move:
                            possible_moves.extend(possible_move + move.way for move in adding_piece_of_move)
                        possible_moves.append(possible_move)
                except ImpossiblePositionError:
                    break
        return possible_moves


class CheckersPlayer(ABC):

    def __init__(self, name: str):
        self.name = name
        self.direction = 1

    @abstractmethod
    def choice_move(self, list_of_moves) -> CheckersMove:
        raise NotImplementedError

    def __hash__(self):
        return self.direction

    def __str__(self):
        return f"{self.name} {self.direction}"


class WinnerException(Exception):

    def __init__(self, loser_player):
        self.loser = loser_player


class CheckersGameMaster:

    # def get_player(self):
    #     player = self.players.pop(0)
    #     self.players.append(player)
    #     return player

    @staticmethod
    def play_a_tour(player: CheckersPlayer, positions: List[CheckersPosition], board: CheckersBoard):
        possible_moves = CheckersGameRules.get_possible_moves(positions, board)
        if not possible_moves:
            raise WinnerException(player)
        chosen_move = player.choice_move(possible_moves)
        CheckersGameRules.move_checker(chosen_move, board)
        return chosen_move
