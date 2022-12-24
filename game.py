#      |     |     |
#   0  |  1  |  2  |  3
# _____|_____|_____|_____
#      |     |     |
#   4  |  5  |  6  |  7
# _____|_____|_____|_____
#      |     |     |
#   8  |  9  |  A  |  B
# _____|_____|_____|_____
#      |     |     |
#   C  |  D  |  E  |  F
#      |     |     |

import os
import msvcrt
from colors import ConsoleColors

global gameMap 
global game

turn = 1
position = 0
gameOver = False
winner = 0
side = 2
menuOption = 1
menuOptionPostGame = 1
postGameMenuOpened = False

def postGameMenu():
    global menuOptionPostGame
    global postGameMenuOpened
    global gameOver
    maxOptions = 2 # amount of menu options
    printGame()
    print()
    print("Choose option: ")

    if menuOptionPostGame == 1:
        print(ConsoleColors.BLACK + ConsoleColors.WHITE_BACKGROUND + "  *      Return to menu  " + ConsoleColors.RESET)
        print("  *      Quit            ")
    elif menuOptionPostGame == 2:
        print("  *      Return to menu  ")
        print(ConsoleColors.BLACK + ConsoleColors.WHITE_BACKGROUND + "  *      Quit            "  + ConsoleColors.RESET)

    while True:
        char = msvcrt.getch()

        if str(ord(char)).__contains__("80"):
            if menuOptionPostGame != maxOptions:
                menuOptionPostGame += 1
                postGameMenu()
                return
        elif str(ord(char)).__contains__("72"):
            if menuOptionPostGame != 1:
                menuOptionPostGame -= 1
                postGameMenu()
                return
        elif str(ord(char)).__contains__("13"):
            if menuOptionPostGame == 1:
                gameOver = False
                postGameMenuOpened = False
            elif menuOptionPostGame == 2:
                print()
                quit()
            menu()
            return
        elif str(ord(char)).__contains__("27"):
            quit()

        # 80 down
        # 74 left
        # 77 right
        # 72 up
        # 13 enter
        # 27 escape

def printGame():
    global side
    global postGameMenuOpened
    os.system('cls')
    row = 0
    column = 0

    for i in range(0, side * 3):
        for j in range(0, side * 6 - 1):
            if((j + 1) %6 == 0 and j > 0 and j < side * 6 - 2):
                print(ConsoleColors.BLACK + ConsoleColors.WHITE_BACKGROUND + "|" + ConsoleColors.RESET, end = "")
            elif((i + 1) %3 == 0 and i > 0 and i < side * 3 - 1):
                print(ConsoleColors.BLACK + ConsoleColors.WHITE_BACKGROUND + "_" + ConsoleColors.RESET, end = "")
            elif((i + 2) %3 == 0 and (j + 1 ) % 3 == 0):
                if game[row][column] == "X":
                    print( ConsoleColors.BLUE + ConsoleColors.WHITE_BACKGROUND + game[row][column] + ConsoleColors.RESET, end = "")
                elif game[row][column] == "O":
                    print(ConsoleColors.RED  + ConsoleColors.WHITE_BACKGROUND + game[row][column] + ConsoleColors.RESET, end = "")
                else:
                    print(ConsoleColors.WHITE_BACKGROUND + game[row][column], end = "")

                column += 1
            else:
                print(ConsoleColors.WHITE_BACKGROUND + " " + ConsoleColors.RESET, end = "")
        print()
        if((i + 1) %3 == 0):
            row += 1
            column = 0
 
    print()

    if(gameOver):
        if(winner == 1):
            print("Player 1 won!")
        elif(winner == 2):
            print("Player 2 won!")
        else:
            print("Game ended in a draw.")

        if not(postGameMenuOpened):
            postGameMenuOpened = True
            postGameMenu() 
            print()

def checkIfEmpty(position):
    global side
    for i in range(0, side):
        for j in range(0, side):
            if(gameMap[i][j] == position and game[i][j] == " "):
                return True

def checkIfGameOver():
    global gameOver
    global side
    global winner
    score = 0 # x = +1, o = -1

    for i in range(0, side): #Checks horizontals 
        for j in range(0, side):
            if(game[i][j] == "X"):
                score += 1
            elif(game[i][j] == "O"):
                score -= 1
            
        
        if(score == 3):
            winner = 1
            gameOver = True
            return
        elif(score == -3):
            winner = 2
            gameOver = True
            return
        
        score = 0

    for i in range(0, side): #Checks verticals 
        for j in range(side - 1, -1, -1):
            if(game[j][i] == "X"):
                score += 1
            elif(game[j][i] == "O"):
                score -= 1
        
        if(score == 3):
            winner = 1
            gameOver = True
            return
        elif(score == -3):
            winner = 2
            gameOver = True
            return
        
        score = 0

    for i in range(1, side - 1): #Checks verticals
        for j in range(1, side - 1): 
            if((game[i][j] == "X" and game[i - 1][j - 1] == "X" and game[i + 1][j + 1] == "X") or (game[i][j] == "X" and game[i + 1][j - 1] == "X" and game[i - 1][j + 1] == "X")):
                winner = 1
                gameOver = True
                return
            elif((game[i][j] == "O" and game[i - 1][j - 1] == "O" and game[i + 1][j + 1] == "O") or (game[i][j] == "O" and game[i + 1][j - 1] == "O" and game[i - 1][j + 1] == "O")):
                winner = 2
                gameOver = True
                return
 
    for i in range(0, side): #Checks if there are blanks
        for j in range(0, side):
            if(game[i][j] == " "):
                return

    gameOver = True

def makeMove():
    global turn
    global side
    global position
    print("Player " + str(turn) + "'s turn: ", end = "")

    position = input()
    
    while not(position.isdecimal()) or int(position) < 1 or int(position) > 16 or not(checkIfEmpty(position)):
        print("Enter a valid option: ", end = "")
        position = input()

    for i in range(0, side):
        for j in range(0, side):
            if(gameMap[i][j] == position):
                if(turn == 1):
                    game[i][j] = "X"
                else:
                    game[i][j] = "O"

    turn += 1
    
    if(turn > 2):
        turn = 1

    checkIfGameOver()
    printGame()

def main():
    printGame()
    makeMove()

def menu():
    global menuOption
    global side
    global game
    global gameMap
    global turn
    maxOptions = 3 # amount of menu options
    os.system('cls')
    print(ConsoleColors.GREEN + """   _     _           _                _             
  | |   (_)         | |              | |            
  | |_   _    ___   | |_ __ _  ___   | |_ ___   ___ 
  | __| | |  / __|  | __/ _` |/ __|  | __/ _ \ / _ \\
  | |_  | | | (__   | || (_| | (__   | || (_) |  __/
   \__| |_|  \___|   \__\__,_|\___|   \__\___/ \___|
        """ + ConsoleColors.RESET)
    print()
    print("Choose option: ")

    if menuOption == 1:
        print(" " + ConsoleColors.BLACK + ConsoleColors.WHITE_BACKGROUND + "  *      3x3  " + ConsoleColors.RESET)
        print("   *      4x4  ")
        print("   *      Quit ")
    elif menuOption == 2:
        print("   *      3x3  ")
        print(" " + ConsoleColors.BLACK + ConsoleColors.WHITE_BACKGROUND + "  *      4x4  "  + ConsoleColors.RESET)
        print("   *      Quit ")
    elif menuOption == 3:
        print("   *      3x3  ")
        print("   *      4x4  ")
        print(" " + ConsoleColors.BLACK + ConsoleColors.WHITE_BACKGROUND + "  *      Quit "  + ConsoleColors.RESET)

    while True:
        char = msvcrt.getch()

        if str(ord(char)).__contains__("80"):
            if menuOption != maxOptions:
                menuOption += 1
                menu()
                return
        elif str(ord(char)).__contains__("72"):
            if menuOption != 1:
                menuOption -= 1
                menu()
                return
        elif str(ord(char)).__contains__("13"):
            if menuOption == 1:
                side = 3
                game = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
                gameMap = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"]]
                turn = 1
            elif menuOption == 2:
                side = 4
                game = [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]
                gameMap = [["13", "14", "15", "16"], ["9", "10", "11", "12"], ["5", "6", "7", "8"], ["1", "2", "3", "4"]]
                turn = 1
            elif menuOption == 3:
                print()
                quit()
            return
        elif str(ord(char)).__contains__("27"):
            quit()

        # 80 down
        # 74 left
        # 77 right
        # 72 up
        # 13 enter
        # 27 escape

menu()

while not(gameOver): #game loop
    main()