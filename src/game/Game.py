
from Board import Board


class Game:
    """ Game class managing the overall Minesweeper game state. """

    def __init__(self):
        self.board : Board = Board()
    
    def click_cell(self, x: int, y: int):
        if not (0 <= x < self.board.width and 0 <= y < self.board.height):
            print(f"Invalid coordinates. Must be 0-{self.board.width-1} for x, 0-{self.board.height-1} for y")
            return
        self.board.click_cell(x, y)

    def flag_cell(self, x: int, y: int):
        if not (0 <= x < self.board.width and 0 <= y < self.board.height):
            print(f"Invalid coordinates. Must be 0-{self.board.width-1} for x, 0-{self.board.height-1} for y")
            return
        self.board.flag_cell(x, y)

    def show_board(self):
        print(self.board.show_board())

    def game_loop(self):
        while not self.board.is_game_over():
            self.show_board()
            command = input("Enter command (c x y to click, f x y to flag, q to quit): ")

            if command.strip().lower() == 'q':
                break
                
            parts = command.split()
            if len(parts) != 3:
                print("Invalid command format.")
                continue
            action, x_str, y_str = parts
            try:
                x = int(x_str)
                y = int(y_str)
            except ValueError:
                print("Coordinates must be integers.")
                continue
            if action == 'c':
                self.click_cell(x, y)
            elif action == 'f':
                self.flag_cell(x, y)
            else:
                print("Unknown action. Use 'c' to click or 'f' to flag.")

            if self.board.is_game_won():
                self.show_board()
                print("\nCongratulations")
                return 

        if self.board.is_game_over():
            self.show_board()
            print("\nGame Over")

