from tkinter import *
from pathlib import Path
import logging, os
from random import shuffle, randint
from time import sleep

image_folder = Path(os.path.dirname(os.path.abspath(__file__)) + "//images")

if not os.path.isdir(image_folder):
    raise RuntimeError("'images' folder not found.")

# The top left position of the top left card on the board. (pixels)
START_X_POSITION = 58
START_Y_POSITION = 190
# Spacing between each card in the y direction. (pixels)
Y_SEPARATION = 75
# Defining the Canvas height and width
CANVAS_HEIGHT = 625
CANVAS_WIDTH = 1000
# Dimensions of the board
BOARD_COLUMNS = 6
BOARD_ROWS = 2
# Difficulties
EASY = 0
NORMAL = 1
HARD = 2
VERY_HARD = 3

tk = Tk()
tk.title('神経衰弱')
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
canvas.pack()

class Window:
    # Make this the main class.

    def __init__(self):
        self.create_title()
        self.create_message_box()
        self.create_difficulty_buttons()

        self.button_on = True
        self.difficulty = None

        self.board = Board()
        self.memory_game = MemoryGame(self.board)

    def create_title(self):
        canvas.create_text(500,75, text = '神経衰弱', font=('MS Gothic', 50))

    def create_message_box(self):
        canvas.create_rectangle(25,20,340,130, fill = 'Black')
        canvas.create_rectangle(30,25,335,125, fill = 'White')

    def create_difficulty_buttons(self):
        easy_button = Button(tk, text= '簡単', width = 10, font = ('MS Gothic', 15), command = self._easy_button)
        easy_button.pack()
        easy_button.place(x = 700, y = 25)

        normal_button = Button(tk, text= '普通', width = 10, font = ('MS Gothic', 15), command = self._normal_button)
        normal_button.pack()
        normal_button.place(x = 850, y = 25)

        hard_button = Button(tk, text= '難しい', width = 10, font = ('MS Gothic', 15), command = self._hard_button)
        hard_button.pack()
        hard_button.place(x = 700,y = 75)

        very_hard_btn = Button(tk, text= '超難しい', width = 10, font = ('MS Gothic', 15), command = self._very_hard_button)
        very_hard_btn.pack()
        very_hard_btn.place(x = 850, y = 75)

    def _easy_button(self):
        '''Function on when the 'Easy' button is pressed.'''
        self._start_game(EASY)

    def _normal_button(self):
        '''Function on when the 'Normal' button is pressed.'''
        self._start_game(NORMAL)

    # Hard button
    def _hard_button(self):
        '''Function on when the 'Hard' button is pressed.'''
        self._start_game(HARD)

    def _very_hard_button(self):
        self._start_game(VERY_HARD)

    def _start_game(self, difficulty):
        '''Starts the game based upon the difficulty chosen and turns off the buttons when
        the game is on-going. The button turns back on when the game has ended.'''
        if self.button_on:
            self.button_on = False
            self.memory_game.play_game(difficulty)
            self.button_on = True

class Board:
    def __init__(self):
        self.board_card = None
        self.initialize_board()

        self.cards = []
        self.set_cards()

        self.indicator = Indicator('red', self.board_card.image.width())

    def initialize_board(self):
        '''Sets the board by placing the back image of the cards.'''
        self.board_card = Card('Card (back).png')
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLUMNS):
                self.board_card.initialize_board_cards()

    def set_cards(self):
        '''Shuffles and places the card onto the board.'''
        card_list = self._return_card_list()
        self._position_cards(card_list)

    def reset_board(self):
        '''Resets the board by deleting the up-faced card images and shuffling the position of the cards.'''
        for i in range(BOARD_COLUMNS):
            for card in self.cards[i]:
                canvas.delete(card.id)
                card.flipped = False

        card_list = []
        for i in range(BOARD_COLUMNS):
            card_list += self.cards[i]

        self._position_cards(card_list)

    def _return_card_list(self):
        '''Returns a list containing the card objects of all the cards on the board.'''
        # Card (Pentagon)
        card_p = Card('Card (Pentagon).png')
        card_p2 = Card('Card (Pentagon).png')

        # Card (Heart)
        card_h = Card('Card (Heart).png')
        card_h2 = Card('Card (Heart).png')

        # Card (Star)
        card_s = Card('Card (Star).png')
        card_s2 = Card('Card (Star).png')

        # Card (Lightning)
        card_l = Card('Card (Lightning).png')
        card_l2 = Card('Card (Lightning).png')

        # Card (Diamond)
        card_d = Card('Card (Diamond).png')
        card_d2 = Card('Card (Diamond).png')

        # Card (Triangle)
        card_t = Card('Card (Triangle).png')
        card_t2 = Card('Card (Triangle).png')

        # Card list
        return [card_p,card_p2,card_h,card_h2,card_s,card_s2,card_l,
        card_l2, card_d, card_d2, card_t, card_t2]

    def _position_cards(self, card_list):
        '''Positions cards within self.cards with respect to their position on the board.'''
        shuffle(card_list)
        self.cards = self._divide_cards(card_list)
        self._set_card_positions()

    def _divide_cards(self, card_list):
        ''' Divides card_list into lists the size of BOARD_ROWS and stores
        them into a list that is returned.'''
        temp_list = []
        for i in range(0, BOARD_COLUMNS*BOARD_ROWS, BOARD_ROWS):
            temp_list.append(card_list[i:i+2])
        return temp_list

    def _set_card_positions(self):
        '''Defines the positions of the cards with respect to the board.'''
        for i in range(BOARD_COLUMNS):
            for j in range(BOARD_ROWS):
                self.cards[i][j].x = i
                self.cards[i][j].y = j

class Card:
    def __init__(self, file_name):
        '''
        Arguments:
        [file_name]: Name of the file used for the card. (str)

        Variables:
        [file_name]: Name of the image used for the card. (str)
        [flipped]: Indicates whether the card was flipped or not. (bool)
        [x]: Indicates the x coordinate of the card relative to the board. (int)
        [y]: Indicates the y coordinate of the card relative to the board. (int)
        [image]: Stores the image object for the card.
        [id]: Stores the id for the image object.
        '''
        self.file_name = file_name
        self.flipped = False
        self.x = 0
        self.y = 0
        self.image = PhotoImage(file = Path.cwd() / 'images' / file_name)
        self.id = None

    def initialize_board_cards(self):
        '''Initializes the board by placing the back images of the cards onto the board.'''
        self._define_spacing_card_width()

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLUMNS):
                canvas.create_image(START_X_POSITION + x_spacing*j, START_Y_POSITION + y_spacing*i, anchor = NW, image = self.image)

    def flip(self):
        '''Flips the card and shows the up side of the card.'''
        self.id = canvas.create_image(START_X_POSITION + self.x*x_spacing, START_Y_POSITION + self.y*y_spacing, anchor = NW, image = self.image)
        self.flipped = True

    def _define_spacing_card_width(self):
        '''Stores the spacing between each card in pixels'''
        global x_spacing, y_spacing

        x_spacing = self.image.width() + START_X_POSITION
        y_spacing = self.image.height() + Y_SEPARATION

class Indicator:
    def __init__(self, color: str, image_width):
        '''Initial variables for the inidicator object.

        Arguments:
        [id]: The id number of the created shape used as the inidicator. (int)
        [x]: The x coordinate of the indicator relative to the board. (int)
        [y]: The y coordinate of the indicator relative to the board. (int)
        [i_x]: The starting x position of the inidicator in pixels. (int)
        [i_y]: The starting y position of the inidicator in pixels. (int)
        [x_shift]: The amount of pixels the indicator moves in the x direction. (int)
        [y_shift]: The amount of pixels the indicator moves in the x direction. (int)
        [max_x]: The maximum distance the indicator can move
        in the x direction in pixels. (int)
        [max_y]: The maximum distance the indicator can move
        in the y direction in pixels. (int)
        '''
        self.id = canvas.create_polygon(0, 0, 20, 0, 10, 20, fill=color)
        self.x = 0
        self.y = 0
        self.i_x = START_X_POSITION + (image_width/2) - 10
        self.i_y = START_Y_POSITION - 30
        self.max_y_value = self.i_y + (y_spacing)*(BOARD_ROWS-1)
        self.max_x_value = self.i_x + (x_spacing)*(BOARD_COLUMNS-1)
        self.x_shift = x_spacing
        self.y_shift = y_spacing
        canvas.move(self.id, self.i_x, self.i_y)
        self.move_status = False
        self.bind_arrow_keys()

    def bind_arrow_keys(self):
        '''Binds the arrow keys to their respective functions'''
        canvas.bind_all('<KeyPress-Up>', self._indicator_event)
        canvas.bind_all('<KeyPress-Down>', self._indicator_event)
        canvas.bind_all('<KeyPress-Left>', self._indicator_event)
        canvas.bind_all('<KeyPress-Right>', self._indicator_event)

    def _indicator_event(self, event):
        # Key setup
        if self.move_status is True:
            self._move_indicator(event)

    def _move_indicator(self, event):
        '''Moves the indicator on the screen using the arrow keys.

        Arguments:
        [event]: Event variable to pass to the KeyPress event.

        Variables:
        [position]: Stores the position of the indicator in pixels. (list)
        '''
        position = canvas.coords(self.id)

        if event.keysym == 'Up':
            self._move_up(position)
        elif event.keysym == 'Down':
            self._move_down(position)
        elif event.keysym == 'Left':
            self._move_left(position)
        elif event.keysym == 'Right':
            self._move_right(position)

    def _move_up(self, pos):
        '''Moves the indicator to the card above.'''
        next_y = pos[1] -  self.y_shift
        if next_y < self.i_y:
            canvas.move(self.id, 0, self.max_y_value - self.i_y)
            self.y = BOARD_ROWS - 1
        else:
            canvas.move(self.id, 0, -1*self.y_shift)
            self.y -= 1

    def _move_down(self, pos):
        '''Moves the indicator to the card below.'''
        next_y = pos[3] + self.y_shift
        if next_y > canvas.winfo_height():
            canvas.move(self.id, 0, -1*(self.max_y_value - self.i_y))
            self.y = 0
        else:
            canvas.move(self.id, 0, self.y_shift)
            self.y += 1

    def _move_left(self, pos):
        '''Moves the indicator to the card on the left.'''
        next_x = pos[0] - self.x_shift
        if next_x < 0:
            canvas.move(self.id, self.max_x_value - self.i_x, 0)
            self.x = BOARD_COLUMNS - 1
        else:
            canvas.move(self.id, -1*self.x_shift, 0)
            self.x -= 1

    def _move_right(self, pos):
        '''Moves the indicator to the card on the right.'''
        next_x = pos[2] + self.x_shift
        if next_x > canvas.winfo_width():
            canvas.move(self.id, -1*(self.max_x_value - self.i_x), 0)
            self.x = 0
        else:
            canvas.move(self.id, self.x_shift, 0)
            self.x += 1

class MemoryGame:
    MAX_PAIRS = (BOARD_COLUMNS*BOARD_ROWS)/2

    def __init__(self, board):
        self.board = board
        self.player = Player()

        canvas.bind_all('<KeyPress-Return>', self._flip_card)

        self.computer = Computer()

        self.message_id = None
        self.display_message("難易度を選択してください。")

    def display_message(self, text):
        '''Displays text onto the message box.'''
        self.message_id = canvas.create_text(180,75, text = text,font=('MS Gothic', 15))
        tk.update()

    def delete_message(self):
        '''Deletes the message in the message box.'''
        canvas.delete(self.message_id)
        tk.update()

    def _flip_card(self, event):
        '''Function on when the enter button is pressed.'''

        if self.player.turn:
            selected_card = self.board.cards[self.board.indicator.x][self.board.indicator.y]

            # Stores the flipped card into the computer's memory if not in memory.
            if selected_card not in self.computer.memory:
                self.computer.memory.append(selected_card)

            # Allows the card to be flipped if the card is not flipped.
            if not selected_card.flipped:
                selected_card.flip()
                tk.update()
                self.player.select_card(selected_card)

    def select_first_player(self):
        '''Randomly chooses whether the player or the computer goes first.'''
        if randint(0,1) == 0:
            self.player.turn = True
        else:
            self.computer.turn = True

    def players_turn(self):
        '''Conducts the player's turn'''
        self.board.indicator.move_status = True
        self.display_message("あなたの番です")
        while self.player.turn and (self.player.pairs + self.computer.pairs < self.MAX_PAIRS):
            tk.update()
        self.board.indicator.move_status = False
        self.delete_message()

    def computers_turn(self, computer_method):
        '''Conducts the computer's turn.

        Arguments:
        [computer_method]: The function to play the computer's move. (function)
        '''
        self.display_message("コンピューターの番です。")
        computer_method(self.player.pairs, self.board.cards)
        self.delete_message()

    def play_game(self, difficulty):
        '''The main loop for the game

        Arguments:
        [difficulty]: A number indicating the difficulty chosen by the user. (int)
        '''
        difficulties = {
        EASY : self.computer.easy,
        NORMAL: self.computer.normal,
        HARD: self.computer.hard,
        VERY_HARD: self.computer.very_hard
        }
        computer_method = difficulties[difficulty]
        canvas.delete(self.message_id)
        self.select_first_player()
        while self.player.pairs + self.computer.pairs < self.MAX_PAIRS:
            if self.player.turn:
                self.players_turn()
                self.computer.turn = True

            if self.computer.turn and self.player.pairs + self.computer.pairs < self.MAX_PAIRS:
                self.computers_turn(computer_method)
                self.player.turn = True

        self.display_match_results()
        self.reset()
        self.display_message("難易度を選択してください。")

    def display_match_results(self):
        '''Displays the result of the match on the message box.'''
        if self.player.pairs > self.computer.pairs:
            self.display_message('あなたの勝ち（ペア:%s)' % (self.player.pairs))
        elif self.player.pairs < self.computer.pairs:
            self.display_message('コンピューターの勝ち（ペア:%s)' % (self.computer.pairs))
        else:
            self.display_message('引き分け')
        tk.update()
        sleep(3)
        canvas.delete(self.message_id)
        tk.update()

    # Reset Game
    def reset(self):
        '''Resets the game to it's initial state.'''
        self.player.turn = False
        self.player.pairs = 0
        self.computer.turn = False
        self.computer.pairs = 0
        self.computer.memory = []
        self.board.reset_board()

class Player:
    # Time till non-pair cards are returned to their original state.
    WAIT_TIME = 1

    def __init__(self):
        '''
        Variables:
        [turn]: Indicates whether it's the player's turn or not.(bool)
        [pair]: Stores the number of pairs the player has found. (int)
        [pick]: Stores the card object that the player has picked during his/her turn. (list)
        '''
        self.turn = False
        self.pairs = 0
        self.pick = []

    def select_card(self, card):
        ''' Stores the chosen card into self.pick. If the two selected cards are pairs, the program
        increases the number of pairs that the player has by one. If not, the program returns the cards
        to their original state and ends the players turn.

        Arguments:
        [card]: Object of the card that was selected. (obj)
        '''
        self.pick.append(card)

        if len(self.pick) == 2:
            if self.pick[0].file_name == self.pick[1].file_name:
                self.pairs += 1
                self.pick = []
            else:
                # Gives time to the player to observe the card flipped.
                sleep(self.WAIT_TIME)
                self._unflip_cards()
                self.pick = []
                self.turn = False

    def _unflip_cards(self):
        '''Unflips the cards flipped by the player on their turn.'''
        canvas.delete(self.pick[0].id)
        canvas.delete(self.pick[1].id)
        tk.update()
        self.pick[0].flipped = False
        self.pick[1].flipped = False

class Computer(Player):
    NORMAL_HIT_RANGE = 7

    def __init__(self):
        '''Variables upon initialization of the ai object

        Variables:
        [turn]: Indicates whether it is the computer's turn or not. (bool)
        [pair]: Stores the number of pairs the computer has found. (int)
        [pick]: Stores the card object that the computer has picked during its turn. (list)
        # Also might not need to be an instance variable.
        [memory]: Stores the card objects that the computer has seen flipped during the game. (list)
        '''
        self.turn = False
        self.pairs = 0
        self.pick = []
        self.memory = []
        self.pair_found = False
        self.hit_range = None

    def easy(self, player_pairs: int, cards: list):
        '''Algorithim for the easy difficulty. Randomly chooses a card to flip.

        Arguments:
        [player_pairs]: The number of pairs that the player has found. (int)
        [cards]: List of card objects on the board. (list)
        '''
        while self.turn and player_pairs + self.pairs < (BOARD_COLUMNS*BOARD_ROWS)/2:
            self._flip_random_card(cards)

    def _flip_random_card(self, cards: list):
        '''Flips a random card that is faced down.'''
        non_flipped_cards = []
        for i in range(BOARD_COLUMNS):
            for j in range(BOARD_ROWS):
                if not cards[i][j].flipped:
                    non_flipped_cards.append(cards[i][j])
        card_to_flip = non_flipped_cards[ randint(0, len(non_flipped_cards) - 1) ]
        card_to_flip.flip()
        tk.update()
        self.select_card_computer(card_to_flip)

    def select_card_computer(self, card):
        ''' Stores the card that the computer has chosen to memory and selects a card
        given as an argument.'''
        if card not in self.memory:
            self.memory.append(card)

        self.select_card(card)
        # Provides time for the player to view the card that the computer played.
        if self.turn:
            sleep(self.WAIT_TIME)

    def normal(self, player_pairs: int, cards: list):
        ''' Will flip any known pairs with a percentage defined by NORMAL_HIT_RANGE.
        If there are no known pairs, the computer will choose a random card to flip.'''
        self.hit_range = self.NORMAL_HIT_RANGE

        while self.turn and player_pairs + self.pairs < BOARD_COLUMNS*BOARD_ROWS/2:
            self._probability_flip(cards)

    def _probability_flip(self, cards):
        '''Flips a pair depending on the probability given by the difficulty.'''
        x, y = self.pair_finder()

        if self.pair_found and randint(0 , 9) < self.hit_range:
            self.select_pair(x, y, cards)
            self.pair_found = False
        else:
            self._flip_random_card(cards)

    def pair_finder(self) -> (int, int):
        '''Finds a pair and returns the coordinate of one of the pairs.
        If not, returns (0,0) as the coordinate.

        Variables:
        [card1]: The 1st card object for comparison. (obj)
        [card2]: The 2nd card object for comparison. (obj)
        '''
        for i in range(len(self.memory)):
            card1 = self.memory[i]
            if i != len(self.memory) - 1:
                for j in range(i+1,len(self.memory)):
                    card2 = self.memory[j]
                    if card1.file_name == card2.file_name:
                        if card1.flipped and card2.flipped:
                            pass
                        elif not card1.flipped and not card2.flipped:
                            self.pair_found = True
                            return card1.x, card1.y
                        else:
                            self.pair_found = True
                            if card1.flipped:
                                return card2.x, card2.y
                            elif card2.flipped:
                                return card1.x, card1.y
        self.pair_found = False
        return 0, 0

    def select_pair(self, x: int, y: int, cards: object):
        '''Flips the card that corresponds to a pair.

        Arguments:
        [x]: The x coordinate of the card to flip relative to the board. (int)
        [y]: The y coordinate of the card to flip relative to the board. (int)
        [cards]: The list of the card objects on the board. (obj)
        '''
        cards[x][y].flip()
        tk.update()
        self.select_card_computer(cards[x][y])

    def hard(self, player_pairs: int, cards: list):
        '''Same algorithm as the method normal. Except, any known pairs will be flipped with a
        100% probability.'''
        self.hit_range = 10

        while self.turn and player_pairs + self.pairs < BOARD_COLUMNS*BOARD_ROWS/2:
            self._probability_flip(cards)

    def very_hard(self, player_pairs: int, cards: list):
        '''Generally the same algorithm as the hard method. Except, when choosing a random card to flip,
        the program will only flip cards that have not been flipped before.

        Variables:
        [x]: x coordinate of the card to flip. (int)
        [y]: y coordinate of the card to flip. (int)
        '''
        while self.turn and player_pairs + self.pairs < BOARD_COLUMNS*BOARD_ROWS/2:
            x, y = self.pair_finder()

            if self.pair_found:
                self.select_pair(x, y, cards)
                self.pair_found = False
            else:
                self._flip_unflipped_card(cards)

    def _flip_unflipped_card(self, cards: list):
        '''Flips a card that is not in memory'''
        unflipped_cards = []
        for i in range(BOARD_COLUMNS):
            for j in range(BOARD_ROWS):
                if cards[i][j] not in self.memory:
                    unflipped_cards.append(cards[i][j])
        card_to_flip = unflipped_cards[ randint(0, len(unflipped_cards) - 1) ]
        card_to_flip.flip()
        tk.update()
        self.select_card_computer(card_to_flip)

if __name__ == '__main__':
    if Path.cwd() != Path(os.path.dirname(os.path.abspath(__file__))):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    window = Window()
    tk.mainloop()