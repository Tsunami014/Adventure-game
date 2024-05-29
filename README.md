# Are you ready player one?

This is a quick start guide for creating your code files. 

Grok doesn’t teach you this. Structure and organisation is critical to success. 

This begins by using comments (which do nothing in the code) to set out BLOCKS where you will add code as you solve the next little problem.

You will also use comments to write PSEUDOCODE to explain what is going on in that block (even if you don’t know how to do it exactly).

What happens is: we turn your comment (PSEUDOCODE) into working code in that bloc. This way, we can SEE what you are trying to do - and can sort out any problems BEFORE trying to code the solution. This breaks the problem down into small parts and removes frustration.

There are 3 code pages here. 

1) Core-structure for all python files. Make yourself a template for this called “base.py” and save it somewhere.

2) Core-structure where we've added some PSEUDOCODE to show you how to start

3) A demo game. Look at the code, see how it mirrors the base file. 
    - Can you work out what the game does?
    - What things in the code do you NOT understand and feel totally new to you?
    - Overall, do you understand little, some or a lot of the code?

4) You need to evaluate the code and modify it to do the following:

    - Add an Enemies: Modify the game board to include enemies (represented by '2') and implement logic for encounters with enemies. For example, if the player moves to a tile with an enemy, their health could decrease, and they would need to defeat the enemy to progress.

    - Implement Treasure: Introduce treasure tiles ('3') on the game board. When the player moves onto a treasure tile, they could gain points or health.

    - Trap Tiles: Add trap tiles ('4') that deduct health from the player when stepped on. Students can implement logic to detect when the player moves onto a trap tile and reduce their health accordingly.


Your file should always be structured (planned) like this. We create ‘blocks’ of code using space and will add pieces of code into the blocks we improve.

`# this file is the main file for the program`
`#-----------------------------------------`


`# import the required modules`
`# -----------------------------------------`


`# create constant variables for the program`
`#  -----------------------------------------`


`# create the def() functions for the program`
`# -----------------------------------------`


`# create the main loop for the program`
`# -----------------------------------------`


## SAMPLE OF PSEUDOCODE

`# this file is the main file for the program`
`#-----------------------------------------`

`# import the required modules`
`# -----------------------------------------`
`# module to handle time delays for the text appearing`
`# module colour the text`


`# create constant variables for the program`
`#  -----------------------------------------`
`# playerX, playerY, exitX, exitY`
`# create a 4 x 4 grid to hold the map`
`# randomly put the player and the exit on the map (not the same place)`



`# create the def() functions for the program`
`# -----------------------------------------`
`# move the player()`
`# check for the exit ()`


`# create the main loop for the program`
`# -----------------------------------------`
`# set game over to FALSE`
`# get user moves until they reach the exit`
