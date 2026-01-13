import os
import random

# ================================================================
# WORKFLOW (high-level)
# 1) The program shows a main menu (Start or Quit).
# 2) If the player chooses Start, two Player objects are created and configured:
#      - each player chooses a name (letters only)
#      - each player chooses a single-letter symbol (letters only)
#      - the second player's symbol cannot duplicate the first player's symbol
# 3) A Board is created and the game loop starts:
#      - choose a random starter
#      - repeatedly prompt the current player to pick a cell (1-9)
#      - update the board, check win or draw
#      - on win or draw show result and ask whether to restart or quit
# 4) Board operations include: display, update cell, reset, validate moves, and show winning line.
# ================================================================

def clear_screen():
    """Clear the terminal screen cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")

class Player:
    """Represents a human player with a name and a single-letter symbol."""

    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        """Prompt the user to enter a name containing letters only."""
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name. Please use letters only")

    def choose_symbol(self, same_symbol=None):
        """
        Prompt the user to choose a single alphabetic symbol.
        If same_symbol is provided, prevent choosing that symbol.
        """
        while True:
            symbol = input("Enter your symbol (single letter): ")
            if symbol.isalpha() and len(symbol) == 1:
                if same_symbol and symbol.upper() == same_symbol.upper():
                    print(f"Symbol '{symbol}' already taken by the other player. Choose another.")
                    continue
                self.symbol = symbol.upper()
                break
            print("Invalid symbol. Enter only alphabetic single character")
            
class Menu:
    """Simple menu class to display main and endgame options and validate choice."""

    def display_main_menu(self):
        """Show the main menu and return the validated choice (1 or 2)."""
        clear_screen()
        print("Welcome to X O Game!")
        print("1. Start Game")
        print("2. Quit Game")
        validate = input("Enter your choice (1 or 2): ")
        return self.validate_choice(validate)

    def display_endgame_menu(self):
        """Show end-of-game options and return the validated choice (1 or 2)."""
        menu_text = """
        Game Over!
        1. Start Game
        2. Quit Game
        """
        validate = input(menu_text + "\nEnter your choice (1 or 2): ")
        return self.validate_choice(validate)

    def validate_choice(self, choose):
        """
        Validate that 'choose' is either 1 or 2.
        Re-prompt until a valid integer choice is provided.
        """
        while True:
            try:
                choose = int(choose)
                if choose in (1, 2):
                    return choose
            except ValueError:
                pass
            choose = input("Invalid. Enter your choice (1 or 2): ")
            
class Board:
    """Represents the 3x3 board and provides helper methods."""

    def __init__(self):
        # Board cells are strings "1".."9" initially
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        """Print the current board to the console in a 3x3 layout."""
        for i in range(0, 9, 3):
            print('|'.join(self.board[i:i + 3]))
            if i < 6:
                print('-' * 5)

    def update_board(self, choice, symbol):
        """
        Attempt to place `symbol` into cell `choice` (1-9).
        Returns True if the move was valid and applied, otherwise False.
        """
        if self.valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def reset_board(self):
        """Reset the board back to the initial numeric state."""
        self.board = [str(i) for i in range(1, 10)]

    def valid_move(self, choice):
        """
        Return True if the requested cell is still numeric (not occupied).
        This is used to detect empty cells (available moves).
        """
        return self.board[choice - 1].isnumeric()

    def display_winner_combo(self, combo):
        """
        Display only the winning combo on a 3x3 layout.
        Other cells are shown as spaces for emphasis.
        'combo' contains indices 0..8 that made the winning line.
        """
        temp = [' '] * 9
        for i in combo:
            temp[i] = self.board[i]
        for i in range(0, 9, 3):
            print('|'.join(temp[i:i + 3]))
            if i < 6:
                print('-' * 5)
                
class Game:
    """Main game controller handling player setup, turn flow and game state."""

    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        """Entry point: show main menu and start or quit based on selection."""
        choice = self.menu.display_main_menu()
        if choice == 1:
            self.players_setup()
            self.play_game()
        else:
            self.quit_game()

    def players_setup(self):
        """Prompt both players to enter names and pick symbols (prevent duplicate symbols)."""
        clear_screen()
        for index, player in enumerate(self.players, 1):
            print(f"Player {index}, Enter your details:")
            player.choose_name()
            same = self.players[0].symbol if index == 2 else None
            player.choose_symbol(same_symbol=same)
            clear_screen()

    def play_game(self):
        """Main game loop: run turns until win or draw, then show endgame menu."""
        clear_screen()
        self.start_turn()
        while True:
            self.play_turn()
            winning_combo = self.check_win()
            if winning_combo:
                clear_screen()
                self.board.display_board()
                print("\n")
                self.board.display_winner_combo(winning_combo)
                # The winner is the other player because switch_player() flips index after a successful move
                player = self.players[1 - self.current_player_index]
                print(f"\n{player.name} won")
                choice = self.menu.display_endgame_menu()
                if choice == 1:
                    self.restart_game()
                else:
                    self.quit_game()
                break
            elif self.check_draw():
                clear_screen()
                self.board.display_board()
                print("\nIt's Draw")
                choice = self.menu.display_endgame_menu()
                if choice == 1:
                    self.restart_game()
                else:
                    self.quit_game()
                break

    def start_turn(self):
        """Randomly choose which player starts the game."""
        self.current_player_index = random.randint(0, 1)

    def play_turn(self):
        """
        Execute one player's turn:
        - display board and prompt for a cell (1-9)
        - validate the input and apply the move
        - then switch player index
        """
        clear_screen()
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"\nIt's {player.name}'s turn. Your symbol: {player.symbol}\n")
        while True:
            try:
                cell_choice = int(input("Choose a cell (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    print("Invalid move, Try again!")
            except ValueError:
                print("Please enter a number between 1 and 9")
        self.switch_player()

    def switch_player(self):
        """
        Toggle the current player index.
        The existing condition preserves original behavior:
        if not self.check_win() or not self.check_draw(): flip index.
        """
        if not self.check_win() or not self.check_draw():
            self.current_player_index = 1 - self.current_player_index

    def check_win(self):
        """
        Check the board for a winning combination.
        Returns the winning combo (list of 3 indices) if found, otherwise None.
        """
        win_combination = [
            [0, 1, 2], [0, 3, 6], [0, 4, 8],
            [1, 4, 7], [2, 4, 6], [2, 5, 8],
            [3, 4, 5], [6, 7, 8]
        ]
        for combo in win_combination:
            if (self.board.board[combo[0]] == self.board.board[combo[1]] ==
                    self.board.board[combo[2]] and not self.board.board[combo[0]].isnumeric()):
                return combo
        return None

    def check_draw(self):
        """Return True when all board cells are non-digit (i.e., all occupied)."""
        return all(not cell.isdigit() for cell in self.board.board)

    def restart_game(self):
        """Reset the board and immediately start a new game loop."""
        self.board.reset_board()
        self.play_game()

    def quit_game(self):
        """Show a simple goodbye message and exit the game flow."""
        print("Thank you for playing!")
        
if __name__ == "__main__":
    game = Game()
    game.start_game()