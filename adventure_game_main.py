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
#create a 5x5 game board. 0 = empty, 1 = player, 2 = enemy, 3 = treasure, 4 = trap, 5 = exit, 6 = boss, 7=visited
gameBoard = [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]]

# place the player in the middle of the game board
playerX = 2
playerY = 2
gameBoard[playerX][playerY] = 1

# place the exit in a random location
exitX = random.randint(0,4)
exitY = random.randint(0,4)
gameBoard[exitX][exitY] = 5

toprints = [] # Setup the blank lisst of things that will be printed

# ----------------------------------------- SET UP THE FUNCTIONS -----------------------------------------
# create the def() functions for the program here
def printBoard():
    print('\033[2J\033[0;0H' + '\n'.join([','.join([str(j) for j in i]) for i in gameBoard]) + '\n\n' + '\n'.join(toprints), end='')

def newprint(txt):
    toprints.append(txt)

def movePlayer(direction):
    global playerX, playerY
    direction = direction.lower()
    if direction == 'w':
        if playerX > 0:
            gameBoard[playerX][playerY] = 7
            playerX -= 1
            gameBoard[playerX][playerY] = 1
        else:
            newprint('You cannot move in that direction')
    elif direction == 's':
        if playerX < 4:
            gameBoard[playerX][playerY] = 7
            playerX += 1
            gameBoard[playerX][playerY] = 1
        else:
            newprint('You cannot move in that direction')
    elif direction == 'd':
        if playerY < 4:
            gameBoard[playerX][playerY] = 7
            playerY += 1
            gameBoard[playerX][playerY] = 1
        else:
            newprint('You cannot move in that direction')
    elif direction == 'a':
        if playerY > 0:
            gameBoard[playerX][playerY] = 7
            playerY -= 1
            gameBoard[playerX][playerY] = 1
        else:
            newprint('You cannot move in that direction')
    
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

Thread(target=mainloop, name='Main game').start()

os.system('cls' if os.name == 'nt' else 'clear') # Clear the terminal
printBoard()

listen_keyboard(
    on_press=onpress,
    delay_second_char=0,
    delay_other_chars=0,
    until=None
)
