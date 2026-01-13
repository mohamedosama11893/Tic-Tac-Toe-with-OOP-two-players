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