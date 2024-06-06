# this file is the main file for the program
#-----------------------------------------
# import the required modules
import random
import os
from sshkeyboard import listen_keyboard, stop_listening

# create constant variables for the program
playerHealth = 100 # eate a variable to store the player's health
playerAttack = 10 # create a variable to store the player's attack power

#----------------------------------------- SET UP THE GAME BOARD -----------------------------------------
#create a 5x5 game board. 0 = empty, 1 = player, 2 = enemy, 3 = treasure, 4 = trap, 5 = exit, 6 = boss, 7 = been there, 8 = UnImplemented 9 = wall
gameBoard = [[0,3,0,0,9,0,0,0,0,3,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,1,0,9,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,9,0,0,3,0,0,4,0,0,0,0,0,0,0,0,0,0,0,5,0,0],
             [0,9,9,9,9,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

# ! Means not implemented
chars = [" ", "Y", "E", "$", "^", "/", "B", ":", "!", "#", "?"] # Characters that correlate with the numbers with "?" at the end
ColourChars = [" ", "\033[96mY", "\033[32mE", "\033[93m$", "\033[32m^", "\033[94m/", "\033[31mB", "\033[90m:", "\033[91m!", "\033[97m#", "\033[90m?"] # The same as above but with COLOURS

foundBoard = [] # The board that you have discovered

# Find the position of the player in the board and set the players' position to that
playerY = [any([j == 1 for j in i]) for i in gameBoard].index(True)
playerX = gameBoard[playerY].index(1)

# place the exit in a random location that does not already have something on it
# Commented out to have a fixed exit
# toputx = random.randint(0,4)
# toputy = random.randint(0,4)
# while not gameBoard[toputy][toputx] == 0:
#     toputx = random.randint(0,4)
#     toputy = random.randint(0,4)
# gameBoard[toputy][toputx] = 5

# ----------------------------------------- SET UP NON-CONSTANT VARIABLES -----------------------------------------
toprints = [] # Setup the blank list of things that will be printed
ca_chingInTheBank = 0 # Player moneys

# ----------------------------------------- SET UP THE FUNCTIONS -----------------------------------------
# create the def() functions for the program here
def printBoard():
    stats = f"Player moneys: {ca_chingInTheBank}\nPlayer health: {playerHealth}HP"
    print('\033[2J\033[0;0H' + '\n'.join([''.join([(ColourChars[gameBoard[i][j]] if (i, j) in foundBoard else ColourChars[-1]) for j in range(len(gameBoard[i]))]) for i in range(len(gameBoard))]) + '\n\033[35m' + stats + '\033[0m\n\n' + '\n'.join(toprints), end='')

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

def EndGame(win):
    newprint('Game over! You %s!'%('win' if win else 'loose'))
    stop_listening()

def movedOn(typ):
    if typ == 5:
        newprint('You have reached the exit!')
        EndGame(True)
    elif typ == 3:
        global ca_chingInTheBank
        ca_chingInTheBank += 1
    elif typ == 4:
        global playerHealth
        playerHealth -= 10

def moveBy(byx, byy):
    global playerX, playerY
    x, y = playerX + byx, playerY + byy
    if y < 0 or y > len(gameBoard)-1 or x < 0 or x > len(gameBoard[y])-1:
        newprint('You cannot move in that direction.')
        return
    newPos = gameBoard[y][x]
    if newPos == 9:
        newprint('You cannot move there - there is a wall in the way!')
        return
    gameBoard[playerY][playerX] = 7
    playerX, playerY = x, y
    movedOn(newPos)
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

def onpress(key):
    global toprints
    toprints = []
    if key in 'wsad':
        movePlayer(key)
    printBoard()

# ----------------------------------------- MAIN LOOP -----------------------------------------
# create the main loop for the program here

os.system('cls' if os.name == 'nt' else 'clear') # Clear the terminal

# Initialise the board
findNewSquares()
printBoard()

# Start the game loop!
listen_keyboard(
    on_press=onpress,
    delay_second_char=0,
    delay_other_chars=0,
    until=None
)
