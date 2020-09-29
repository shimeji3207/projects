import random

class AI:
    def __init__(self):
        self.difficulty = None
        self.moves_first = False
        self.DIFFICULTY_MAP = {
        1 : self._easy_ai_move,
        2 : self._normal_ai_move,
        3 : self._hard_ai_move,
        4 : self._very_hard_ai_move
    }

    def set_ai_difficulty(self, difficulty: int):
        self.difficulty = self.DIFFICULTY_MAP[difficulty]

    def play_move(self, board):
        move = self.difficulty(board)
        board.apply_move(move, board.computer_symbol)

    def _easy_ai_move(self, board):
        '''Returns a random possible move on the board.
        [Arguments]
        board: obj

        [Return] -> int
        '''
        possible_moves = board.get_available_moves()
        # Chooses a random move out of the possible moves and returns it.
        return possible_moves[random.randint(0, len(possible_moves)-1)]

    def _normal_ai_move(self, board):
        '''Returns a random possible move to play unless there is a winning move.

        [Arguments]
        board: object

        [Return] -> int
        '''
        possible_moves = board.get_available_moves()

        # Checks if there is a winning move.
        move = self._move_check(board.board, board.computer_symbol, possible_moves)

        # If there is no winning move for the computer,
        # the computer will pick a random move to play.
        if move not in possible_moves:
            move = possible_moves[random.randint(0, len(possible_moves)-1)] # Assigns the cell number to move

        return move

    def _move_check(self, board, symbol, moves):
        '''Checks the columns, rows, and diagonals of the board whether a two in a row exists.
        If so, returns the coordinate of the move that wins or blocks a win.
        Else, returns null.

        [Arguments]
        board: object
        symbol: str
        moves: list

        [Return] -> int or null
        '''
        # Row check
        for i in range(3):
            count = 0
            for j in board[i]:
                if j == symbol:
                    count +=  1

                if count == 2:
                    for k in board[i]:
                        if k in moves:
                            return k

        # Column check
        for i in range(3):
            count = 0
            for j in range(3):
                if board[j][i] == symbol:
                    count += 1

                if count == 2:
                    for k in range(3):
                        if board[k][i] in moves:
                            return board[k][i]

        countdiag1 = 0
        countdiag2 = 0
        # Diagonal check
        for i in range(3):
            for j in range(3):
                # Checks the i = j diagonal
                if i == j:
                    if board[i][j] == symbol:
                        countdiag1 += 1
                # Check the i + j = n diagonal.
                if i + j == len(board) - 1:
                    if board[i][j] == symbol:
                        countdiag2 += 1

        if countdiag1 == 2:
            for i in range(3):
                for j in range(3):
                    if i == j:
                        if board[i][j] in moves:
                            return board[i][j]

        if countdiag2 == 2:
            for i in range(3):
                for j in range(3):
                    if i + j == len(board) - 1:
                        if board[i][j] in moves:
                            return board[i][j]

        return None

    def _hard_ai_move(self, board):
        '''Will return both winning moves and moves that will prevent
        the player from winning. If no such moves exist, then will return a random move.

        [Arguments]
        board: object

        [Return] -> int
        '''
        possible_moves = board.get_available_moves()

        # Checks if there is a winning move.
        move = self._move_check(board.board, board.computer_symbol, possible_moves)

        # Checks if the opponent is about to win. If so, tries to prevent it.
        if move not in possible_moves:
            move = self._move_check(board.board, board.human_symbol, possible_moves)

        # If there are no winning moves for either side, the computer randomly chooses a move to play.
        if move not in possible_moves:
            move = possible_moves[random.randint(0, len(possible_moves)-1)]

        return move

    def _very_hard_ai_move(self, board):
        '''On the first move, it will try to obtain the center.
        If taken, it will take a corner. After the first move, it will follow the algorithm for
        the 'hard' difficulty

        [Arguments]
        board: obj

        [Return] -> int
        '''
        possible_moves = board.get_available_moves()

        if self.moves_first is True or 5 in possible_moves:
            self.moves_first = None
            return 5
        elif self.moves_first is False:
            corners = [ i for i in possible_moves if i in (1, 3, 7, 9)]
            self.moves_first = None
            # Returns a randomly chosen corner.
            return corners[random.randint(0, len(corners) - 1)]

        return self._hard_ai_move(board)