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
# Create a 5x5 game board. 0 = empty, 1 = player, 2 = enemy, 3 = treasure, 4 = trap, 5 = exit, 6 = boss, 7 = been there, 8 = chest, 9 = wall
# Anything beyond 10 will not be put directly onto the board, but rather will be put there as an effect; (If need another base tile move 'been there' to a higher value)
# 10 = open chest
gameBoard = [[0,3,0,0,9,0,0,0,0,3,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0],
             [0,0,1,0,9,3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
             [0,0,0,0,9,0,0,3,0,0,4,0,0,0,0,0,0,0,0,0,0,6,5,0,0],
             [0,9,9,9,9,0,8,0,0,4,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0],
             [0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

chars = [" ", "Y", "E", "$", "^", "/", "B", ":", "O", "#", "U", "?"] # Characters that correlate with the numbers with "?" at the end
ColourChars = [" ", "\033[96mY", "\033[38;5;166mE", "\033[93m$", "\033[32m^", "\033[94m/", "\033[38;5;88mB", "\033[90m:", "\033[93mO", "\033[97m#", "\033[38;5;52mU", "\033[90m?"] # The same as above but with COLOURS

foundBoard = [] # The board that you have discovered

# Find the position of the player in the board and set the players' position to that
playerY = [any([j == 1 for j in i]) for i in gameBoard].index(True)
playerX = gameBoard[playerY].index(1)
gameBoard[playerY][playerX] = 7

# place the exit in a random location that does not already have something on it
# Commented out to have a fixed exit
# toputx = random.randint(0,4)
# toputy = random.randint(0,4)
# while not gameBoard[toputy][toputx] == 0:
#     toputx = random.randint(0,4)
#     toputy = random.randint(0,4)
# gameBoard[toputy][toputx] = 5

# Find all enemies and keep track of them
ens = {}
for y in range(len(gameBoard)):
    for x in range(len(gameBoard[y])):
        if gameBoard[y][x] == 2: # Regular enemy
            ens[(y, x)] = 10 # Health of enemy
        elif gameBoard[y][x] == 6: # Boss
            ens[(y, x)] = 50 # Health of boss

toprints = [] # Setup the blank list of things that will be printed
ca_chingInTheBank = 0 # Player moneys
inventory = {"light": False} # The player's inventory; with nothing in it.

# ----------------------------------------- SET UP THE FUNCTIONS -----------------------------------------
# create the def() functions for the program here
def printBoard():
    stats = f"Player moneys: {ca_chingInTheBank}\nPlayer health: {playerHealth}HP"
    print('\033[2J\033[0;0H' + '\n'.join([''.join([(ColourChars[1] if i == playerY and j == playerX else (ColourChars[gameBoard[i][j]] if (i, j) in foundBoard else ColourChars[-1])) for j in range(len(gameBoard[i]))]) for i in range(len(gameBoard))]) + '\n\033[35m' + stats + '\033[0m\n\n' + '\n'.join(toprints), end='')

def newprint(txt):
    toprints.append(str(txt))

def findNewSquares(pos=None, dist=1):
    if pos is None:
        pos = [playerY, playerX]
    def check(p):
        if dist > 1:
            findNewSquares(p, dist - 1)
        else:
            if tuple(p) not in foundBoard:
                foundBoard.append(tuple(p))
    def md(x, y): # MoDify
        return [pos[0] + y, pos[1] + x]
    if tuple(pos) not in foundBoard:
        foundBoard.append(tuple(pos))
    check(md(1, 0))
    check(md(1, 1))
    check(md(0, 1))
    check(md(-1, 1))
    check(md(-1, 0))
    check(md(-1, -1))
    check(md(0, -1))
    check(md(1, -1))

def EndGame(win, msg):
    newprint(('\033[32m' if win else '\033[91m') + msg)
    newprint('Game over! You %s!\033[0m'%('win' if win else 'loose'))
    stop_listening()

def get_hurt(minusHP, hurtBy):
    global playerHealth
    playerHealth -= minusHP
    newprint("You got hurt by %s for %iHP!"%(hurtBy, minusHP))
    if playerHealth <= 0:
        EndGame(False, "You've run out of life!")

def movedOn(typ, tx, ty): # You moved onto a tile
    # Once-off tiles
    if typ == 5: # Exit
        EndGame(True, 'You have reached the exit!')
    elif typ == 3: # Moneys
        global ca_chingInTheBank
        ca_chingInTheBank += 1
    elif typ == 4: # Trap
        get_hurt(10, "a trap")
    
    # Tiles that change
    if typ == 8: # Chest
        global inventory
        inventory["light"] = True
        return 10
    elif typ in [2, 6]: # Is an enemy or boss
        global ens
        atk = random.randint(0, playerAttack)
        newprint("You hit the enemy for %iHP!"%atk)
        ens[(ty, tx)] -= atk
        if ens[(ty, tx)] <= 0:
            newprint('You killed the enemy!')
            gameBoard[ty][tx] = 3
            ens.pop((ty, tx))
            return False
        get_hurt(random.randint(0, 5), "the enemy")
        return False # Do not allow you to move into enemies

    # And if it isn't a tile that changes above, turn it into a blank
    return 7

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
    res = movedOn(newPos, x, y)
    if res != False:
        playerX, playerY = x, y
        gameBoard[playerY][playerX] = res

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
    findNewSquares(dist=(2 if inventory["light"] else 1))

def move_enemies():
    global ens, gameBoard
    nens = {}
    def check(x, y, curpos):
        if y < 0 or y > len(gameBoard)-1 or x < 0 or x > len(gameBoard[y])-1:
            return False
        if gameBoard[y][x] == 0:
            nens[(y, x)] = ens[curpos]
            gameBoard[y][x] = gameBoard[curpos[0]][curpos[1]]
            gameBoard[curpos[0]][curpos[1]] = 0
            return True
        return False
    def mod(byX, byY, pos):
        return (pos[1] + byX, pos[0] + byY)
    for pos in ens:
        if random.randint(0, 10) >= 7 or (abs(pos[1] - playerX) <= 2 and abs(pos[0] - playerY) <= 2):
            nens[pos] = ens[pos]
            continue
        find = lambda x, y: check(*mod(x, y, pos), pos)
        spaces = [
            #(1, 1),
            (1, 0),
            #(1, -1),
            (0, 1),
            (0, -1),
            (-1, 1),
            (-1, 0),
            #(-1, -1)
        ]
        # Keep going until you get a True, then go to the next enemy
        random.shuffle(spaces)
        found = False
        for i in spaces:
            if find(*i):
                found = True
                break
        if not found:
            nens[pos] = ens[pos]
    ens = nens
    newprint(len(ens))

def onpress(key):
    global toprints
    toprints = []
    move_enemies()
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
