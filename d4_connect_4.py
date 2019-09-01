import random ## This allows computer to pick random move
import numpy as np ## In case this is needed

## ----------------------------
##      Initialize game
## ----------------------------

row1 = [0,0,0,0,0,0,0]
row2 = [0,0,0,0,0,0,0]
row3 = [0,0,0,0,0,0,0]
row4 = [0,0,0,0,0,0,0]
row5 = [0,0,0,0,0,0,0]
row6 = [0,0,0,0,0,0,0]
board = [row1,row2, row3, row4, row5, row6,]

gameEnd = False

def display(): ## Printing the board
    print(row1,'\n',row2,'\n',row3,'\n',row4,'\n',row5,'\n',row6)

def start(): ## The beginning of the game
    print("Welcome to Connect Four!\nYour are player 1 and the computer is player 2.\nPlace your piece and test your skill.\n")
    display()

## ----------------------------
##      Game components
## ----------------------------

def playerMove():
    pCol = int(input("Column? "))
    pRow = int(input("Column? "))
    if board[pRow][pCol] == 1:
        playerMove()
    elif board[pRow][pCol] == 2:
        playerMove()
    else:
        board[pRow][pCol] = 1
        
    '''
    for i in range(0, 6):
        pRow = pRow - i
        if board[pRow][pCol] == 0:
            board[pRow][pCol] = 1
        elif board[pRow][pCol] == 1:
            playerMove()
        elif board[pRow][pCol] == 2:
            playerMove()
    '''
    
def computerMove():
    cCol = random.randint(2, 4)
    cRow = random.randint(0, 4)
    board[cRow][cCol] = 2
    if board[cRow][cCol] == 1:
        computerMove()
    elif board[cRow][cCol] == 2:
        computerMove()
    else:
        board[cRow][cCol] = 1

def gameplay():
    while gameEnd == False:
        computerMove()
        playerMove()
        display()
        checkWin()

def endGame():
    global gameEnd
    
    print("Good game!\nDo you want to play again?")
    playAgain = input("(Y/N)? ")
    if playAgain == "Y":
        play()
    elif playAgain == "N":
        play("Goodbye!")

def checkWin():
    global gameEnd
    
    pCount = 0
    cCount = 0
    
    for i in range(0, 6):
        for j in range(0, 7):
            if board[i][j] == 1:
                pCount += 1
            elif board[i][j] != 1:
                pCount = 0
            if pCount == 4:
                gameEnd = True
            if board[i][j] == 2:
                cCount += 1
            elif board[i][j] != 2:
                cCount = 0
            if cCount == 4:
                gameEnd = True
    
def play(): ## Executable loop for gameplay
    start()
    while gameEnd == False:
        gameplay()
    if gameEnd == True:
        endGame()
play()

## ----------------------------
##          End game
## ----------------------------

def endGame():
    global gameEnd
    
    print("Good game!\nDo you want to play again?")
    playAgain = input("(Y/N)? ")
    if playAgain == "Y":
        play()
    elif playAgain == "N":
        play("Goodbye!")