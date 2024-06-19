****Connect 4 Game****

****Overview****

This project implements a graphical Connect 4 game using Python's **"tkinter"** library for the GUI and **"Numpy"** for the game logic. 

Players can be either human or AI with different difficulty levels powered by an **"Alpha-Beta Pruning"** algorithm.

****Features****

**Human vs. Human:** Two players can play against each other.

**Human vs. AI:** A human can play against an AI with varying levels of difficulty.

**Graphical Interface:** The game board is displayed graphically using tkinter.

**AI Difficulty Levels:** The AI uses an alpha-beta pruning algorithm with selectable difficulty levels.

****How to Run****

**1. Run the Script:** python connect4.py

**2.Gameplay:**

**Start a New Game:** Click the "New game" button.

**Select Players:** Use the dropdown menus to select the type of player for Player 1 and Player 2. Options include "human" and "AI: alpha-beta level X" where X is the difficulty level.

**Play:** If playing as a human, click on the column where you want to drop your disk.

****Game Rules****

**1.** Players take turns dropping disks into one of the seven columns.

**2.** The disk falls to the lowest available space within the column.

**3.** The first player to connect four of their disks vertically, horizontally, or diagonally wins.

**4.** If the board is full and no player has connected four disks, the game is a draw.

