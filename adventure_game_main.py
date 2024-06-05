# this file is the main file for the program
#-----------------------------------------
# import the required modules
import random
import time
import os
from sshkeyboard import listen_keyboard, stop_listening
from threading import Thread

# create constant variables for the program
gameOver = False # create a variable to control the game loop
playerHealth = 100 # eate a variable to store the player's health
playerAttack = 10 # create a variable to store the player's attack power

#----------------------------------------- SET UP THE GAME BOARD -----------------------------------------
#create a 5x5 game board. 0 = empty, 1 = player, 2 = enemy, 3 = treasure, 4 = trap, 5 = exit, 6 = boss, 7 = been there, 9 = wall
gameBoard = [[0,0,0,0,0],
             [0,9,0,9,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]]

# ! Means not implemented
chars = [" ", "Y", "E", "$", "^", "/", "B", "=", "!", "#"] # Characters that correlate with the numbers

foundBoard = [] # The board that you have discovered

# place the player in the middle of the game board
playerX = 2
playerY = 2
gameBoard[playerY][playerX] = 1

# place the exit in a random location
exitX = random.randint(0,4)
exitY = random.randint(0,4)
gameBoard[exitY][exitX] = 5

toprints = [] # Setup the blank lisst of things that will be printed

# ----------------------------------------- SET UP THE FUNCTIONS -----------------------------------------
# create the def() functions for the program here
def printBoard():
    print('\033[2J\033[0;0H' + '\n'.join([''.join([(chars[gameBoard[i][j]] if (i, j) in foundBoard else '?') for j in range(len(gameBoard[i]))]) for i in range(len(gameBoard))]) + '\n\n' + '\n'.join(toprints), end='')

def newprint(txt):
    toprints.append(str(txt))

def findNewSquares():
    playerPos = [playerY, playerX]
    def check(pos):
        if tuple(pos) not in foundBoard:
            foundBoard.append(tuple(pos))
    def md(x, y): # MoDify
        return [playerPos[0] + y, playerPos[1] + x]
    check(playerPos)
    check(md(1, 0))
    check(md(1, 1))
    check(md(0, 1))
    check(md(-1, 1))
    check(md(-1, 0))
    check(md(-1, -1))
    check(md(0, -1))
    check(md(1, -1))

def moveBy(byx, byy):
    global playerX, playerY
    x, y = playerX + byx, playerY + byy
    if x < 0 or x > 4 or y < 0 or y > 4:
        newprint('You cannot move in that direction')
        return
    newPos = gameBoard[y][x]
    if newPos == 9:
        newprint('You cannot move there - there is a wall in the way!')
        return
    gameBoard[playerY][playerX] = 7
    playerX, playerY = x, y
    gameBoard[playerY][playerX] = 1

def movePlayer(direction):
    direction = direction.lower()
    if direction == 'w':
        moveBy(0, -1)
    elif direction == 's':
        moveBy(0, 1)
    elif direction == 'd':
        moveBy(1, 0)
    elif direction == 'a':
        moveBy(-1, 0)
    findNewSquares()
    checkExit()
    

#check if the player has reached the exit
def checkExit():
    global gameOver
    if playerX == exitX and playerY == exitY:
        newprint('You have reached the exit')
        gameOver = True
    if gameOver:
        newprint('Game over!')

def onpress(key):
    global toprints
    toprints = []
    if key in 'wsad':
        movePlayer(key)
    printBoard()

# ----------------------------------------- MAIN LOOP -----------------------------------------
# create the main loop for the program here
def mainloop():
    try:
        checkExit()
    except KeyboardInterrupt:
        pass
    stop_listening()

findNewSquares()
Thread(target=mainloop, name='Main game').start()

os.system('cls' if os.name == 'nt' else 'clear') # Clear the terminal
printBoard()

listen_keyboard(
    on_press=onpress,
    delay_second_char=0,
    delay_other_chars=0,
    until=None
)
