class Player:

    def select_difficulty(self, ai):
        '''Prompts the player to select the difficulty to play.

        [Arguments]
        ai: object
        '''
        while True:
            print('難易度を選択してください：\n1.簡単\n2.普通\n3.難しい\n4.超難しい')
            difficulty = input().strip()

            if (difficulty.isdecimal() is True) and (int(difficulty) in (1, 2, 3, 4)):
                break

        ai.set_ai_difficulty(int(difficulty))

    def players_turn(self, board):
        '''Gets the players move and applies it onto the board.

        [Arguments]
        board: object
        '''
        print('あなたの番です。')
        while True:
            move = input().strip()

            if (move.isdecimal() is True) and (int(move) in board.get_available_moves()):
                break

            print('マスに表示されている数字を入力してください。')

        board.apply_move(int(move), board.human_symbol)

    def play_again(self):
        '''Asks the player with they want to play again.
        Returns the player's answer as a string.

        [Returns] -> str
        '''
        while True:
            user_input = input("もう一度やりますか？(y/n)\n").strip().lower()
            if user_input in ("y", "n"):
                break

        return user_input