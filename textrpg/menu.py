class Menu:
    MAX_MENU_LENGTH = 5

    def __init__(self, item_info, items, return_option):
        self.items = items
        self.item_info = item_info
        self.menu_length = 0
        self.menu_number = 0
        self.max_menus = 0
        self.command = ""
        self.return_option = return_option
        self.letter_commands = []
        self.menu_starting_index = 0
        self.menu_end_index = 0

    def return_selected_option(self):
        self.initialize_parameters()

        while(True):
            self.calculate_menu_length()

            self.define_menu_indexes()

            self.print_item_menu()

            self.define_letter_commands()
            self.get_item_menu_input()

            if (self.command == "b"):
                return None
            elif (self.command == "n"):
                if (self.menu_number == 1) and (self.max_menus == 1):
                    print("Invalid command")
                    continue

                if (self.menu_number == self.max_menus):
                    self.menu_number = 1
                else:
                    self.menu_number += 1
                continue

            return self.command - 1

    def initialize_parameters(self):
        self.menu_number = 1

        if (len(self.items) % 5 == 0):
            self.max_menus = len(self.items) / 5
        else:
            self.max_menus = int(len(self.items) / 5) + 1

    def calculate_menu_length(self):
        if (self.menu_number * self.MAX_MENU_LENGTH >= len(self.items)):
            self.menu_length = len(self.items) - (5 * (self.menu_number - 1))
        else:
            self.menu_length = self.MAX_MENU_LENGTH

    def define_menu_indexes(self):
        self.menu_starting_index = ((self.menu_number - 1) * self.MAX_MENU_LENGTH) + 1
        self.menu_end_index = self.menu_starting_index + self.menu_length

    def print_item_menu(self):
        for i in range(self.menu_starting_index, self.menu_end_index):
            print("%s. %s" % (i, self.item_info[self.items[i - 1]]["name"]))

        if (self.max_menus > 1):
            if (self.menu_number != self.max_menus):
                print("n. 次のページ")
            elif (self.menu_number == self.max_menus):
                print("n. 最初のページに戻る")

        print("b. %s" % (self.return_option))

    def define_letter_commands(self):
        if (self.max_menus > 1):
            self.letter_commands = ["n", "b"]
        else:
            self.letter_commands = ["b"]

    def get_item_menu_input(self):
        while(True):
            self.command = input().strip()

            if (self.command in self.letter_commands):
                break
            elif (self.command.isdigit()):
                self.command = int(self.command)
            else:
                print("Invalid command")
                continue

            if self.command in list(range(self.menu_starting_index, self.menu_end_index)):
                break

            print("Invalid command")
