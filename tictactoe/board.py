import random

class Board:
    BOARD_SIZE = 3
    PLAYER = 0
    COMPUTER = 1

    def __init__(self):
        self.board = []
        self._initialize_board()
        self.human_symbol = ""
        self.computer_symbol = ""
        self.board_coordinate_map = {}
        self._conduct_board_mapping()

    def set_symbols(self, first_player):
        '''Sets the symbols used by the players on the board.

        [Arguments]
        first_player: int
        '''
        if first_player == self.PLAYER:
            self.human_symbol = "O"
            self.computer_symbol = "X"
        else:
            self.human_symbol = "X"
            self.computer_symbol = "O"

    def get_available_moves(self):
        '''Checks for the availabe moves on the board
            and returns them as a list.
        [Returns] -> list
        '''
        available_moves = []
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if type(self.board[i][j]) is int:
                    available_moves.append(self.board[i][j])
        return available_moves

    def apply_move(self, move, symbol):
        '''Applies the move of a player onto the board.

        [Arguments]
        move: int
        symbol: str
        '''
        x, y = self.board_coordinate_map[move]
        self.board[x][y] = symbol

    def print_board(self):
        '''Displays the board on the screen.
           ***Currently doesn't self_adjust with regards to the size of the integers in the squares'''
        def border_print():
            '''Displays the border of each row onto the screen'''
            for i in range(self.BOARD_SIZE):
                if i == self.BOARD_SIZE - 1:
                    print('+---+')
                else:
                    print('+---', end='')
        border_print()
        # Loop to print the non-border rows.
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if j == self.BOARD_SIZE - 1:
                    print('| ' + str(self.board[i][j]) + ' |')
                else:
                    print('| %s ' % (str(self.board[i][j])), end='')
            border_print()

    def win_check(self, symbol):
        '''Checks whether a player has won or not by returning a boolean.

        [Arguments]
        symbol: str

        [Return] -> bool
        '''
        # Row check
        for i in range(3):
            same_count = 0
            for j in self.board[i]:
                if j == symbol:
                    same_count += 1

            if same_count == 3:
                return True

        # Column check
        for i in range(3):
            same_count = 0
            for j in range(3):
                if self.board[j][i] == symbol:
                    same_count += 1

            if same_count == 3:
                return True

        # Diagonal checks for three in a row
        same_countdiag1 = 0 # Diagonal from the top left to the bottom right
        same_countdiag2 = 0 # Diagonal from the top right to the bottom left
        for i in range(3):
            for j in range(3):
                if i == j:
                    if self.board[i][j] == symbol:
                        same_countdiag1 += 1
                if i + j == len(self.board) - 1:
                    if self.board[i][j] == symbol:
                        same_countdiag2 += 1

            if same_countdiag1 == 3 or same_countdiag2 == 3:
                return True
        return False

    def reset_board(self):
        '''Resets the board to its initial state.'''
        square_number = 1
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.board[i][j] = square_number
                square_number += 1

    def _initialize_board(self):
        '''Initializes the board array.'''
        for i in range(1, (self.BOARD_SIZE**2) + 1, self.BOARD_SIZE):
            self.board.append([j for j in range(i, i + self.BOARD_SIZE)])

    def _conduct_board_mapping(self):
        '''Maps the board coordinates to array coordinates for the board array.'''
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                self.board_coordinate_map[self.board[i][j]] = (i, j)