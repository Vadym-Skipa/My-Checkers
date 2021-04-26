from checkers_game_master import CheckersGameMaster, WinnerException, CheckersPlayer
from checkers_elements import CheckersBoard, Checker
import datetime
import csv
from typing import List
from checkers_position import CheckersPosition
from checkers_player_types import RandomCheckersPlayer

class CheckersGame():

    def __init__(self, player1: CheckersPlayer, player2: CheckersPlayer):
        self.board = CheckersBoard()
        player1.direction = 1
        player2.direction = -1
        self.players = [player1, player2]
        for position in self.board.keys():
            if position.horizontal_line_int in (0, 1, 2):
                checker = Checker(1)
                self.board.append(position, checker)
            elif position.horizontal_line_int in (5, 6, 7):
                checker = Checker(-1)
                self.board.append(position, checker)

    def get_player(self):
        player = self.players.pop(0)
        self.players.append(player)
        return player

    def write_history(self):
        with open(f"{str(datetime.datetime.now())}.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(self.board.keys())
            writer.writerow(self.board.values())
            while True:
                a = yield
                if isinstance(a, CheckersPlayer):
                    print(f"{a} lose")
                    break
                writer.writerow(a)

    def get_players_positions(self, player: CheckersPlayer) -> List[CheckersPosition]:
        positions = []
        for position in self.board.keys():
            if self.board.get_element(position) and self.board.get_element(position).direction == player.direction:
                positions.append(position)
        return positions


    def playing_checkers(self):
        i = 0
        chronicler = self.write_history()
        next(chronicler)
        while True and i < 10000:
            try:
                player = self.get_player()
                positions = self.get_players_positions(player)
                move = CheckersGameMaster.play_a_tour(player, positions, self.board)
            except WinnerException as ex:
                try:
                    chronicler.send(ex.loser)
                except StopIteration:
                    pass
                break
            else:
                print(i)
                i += 1
                chronicler.send(move)


if __name__ == "__main__":
    player1 = RandomCheckersPlayer("p1")
    player2 = RandomCheckersPlayer("p2")
    game = CheckersGame(player1, player2)
    game.playing_checkers()
