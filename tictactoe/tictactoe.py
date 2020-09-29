from ai import AI
from player import Player
from board import Board
from random import randint

class TicTacToe:
    PLAYER = 0
    COMPUTER = 1

    def __init__(self):
        self.turns_played = 0
        self.first_move = self.PLAYER
        self.score = {'勝ち': 0, '負け': 0, '引き分け': 0}
        self.board = Board()
        self.ai = AI()
        self.player = Player()

    def main(self):
        while True:
            self.player.select_difficulty(self.ai)
            self._set_game_settings()

            if self.first_move == self.PLAYER:
                self._player_first_game()
            else:
                self._computer_first_game()

            self._print_score()

            command = self.player.play_again()
            if command == 'y':
                self._reset_board()
            else:
                break

    def _set_game_settings(self):
        self._select_first_player()
        self.board.set_symbols(self.first_move)

    def _select_first_player(self):
        self.first_move = self.PLAYER if randint(0, 1) == self.PLAYER else self.COMPUTER

    def _player_first_game(self):
        input("プレイヤーが先攻です。↲")
        self.board.print_board()
        while True:
            self.player.players_turn(self.board)
            if self._player_win_check() is True:
                break

            if self._draw_check() is True:
                break

            self.ai.play_move(self.board)
            self.board.print_board()
            if self._computer_win_check() is True:
                break
            self.turns_played += 1

    def _player_win_check(self):
        '''Checks if the player has won.
        [Return] -> bool
        '''
        if self.board.win_check(self.board.human_symbol) is True:
            self._player_wins()
            return True
        return False

    def _player_wins(self):
        self.board.print_board()
        input("あなたの勝ち！↲")
        self.score['勝ち'] += 1

    def _draw_check(self):
        '''Checks if the game is drawn.
        [Return] -> bool
        '''
        if self.turns_played == 4:
            self._draw()
            return True
        return False

    def _draw(self):
        input("引き分け↲")
        self.score['引き分け'] += 1

    def _computer_win_check(self):
        '''Checks if the computer has won.
        [Return] -> bool
        '''
        if self.board.win_check(self.board.computer_symbol) is True:
            self._computer_wins()
            return True
        return False

    def _computer_wins(self):
        input("コンピューターの勝ち↲")
        self.score['負け'] += 1

    def _computer_first_game(self):
        input("コンピューターが先攻です。↲")
        while True:
            self.ai.play_move(self.board)
            self.board.print_board()
            if self._computer_win_check() is True:
                break

            if self._draw_check() is True:
                break

            self.player.players_turn(self.board)
            if self._player_win_check() is True:
                break
            self.turns_played += 1

    def _reset_board(self):
        self.board.reset_board()
        self.turns_played = 0

    def _print_score(self):
        print('-'*11)
        print("成績")
        print('-'*11)
        for key, value in self.score.items():
            print('%s: %s' % (key, value))
        print('-'*11)

if __name__ == '__main__':
    tic_tac_toe = TicTacToe()
    tic_tac_toe.main()