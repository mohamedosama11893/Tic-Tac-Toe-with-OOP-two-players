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