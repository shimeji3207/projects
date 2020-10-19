def display_message(text):
    input(text)

def get_yes_no_input():
    while (True):
        command = input().strip().lower()

        if command in ("y", "n"):
            return command
        else:
            print("Invalid input")
