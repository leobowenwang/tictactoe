import numpy as np
from math import inf

XPLAYER = +1
OPLAYER = -1
EMPTY = 0
# initialize empty 3x3 board (with 0 values only)   
board = np.zeros((3, 3))

# ------------------------------------------------------------------
# BOARD
def printBoard():
    chars = {XPLAYER: 'X', OPLAYER: 'O', EMPTY: ' '}
    print('---------------')
    for x in board:
        for y in x:
            ch = chars[y]
            print(f'| {ch} |', end='')
        print('\n' + '---------------')
    print('===============')
# ------------------------------------------------------------------
# MOVES
def makeMove(player, order):
    # player goes first
    if order == 1:
        if player == XPLAYER:
            playerMove(XPLAYER)
        else:
            AIMove(OPLAYER)
    # AI goes first
    elif order == 2:
        if player == OPLAYER:
            AIMove(XPLAYER)
        else:
            playerMove(OPLAYER)

def playerMove(player):
    e = True
    moves = {1: [0, 0], 2: [0, 1], 3: [0, 2],
             4: [1, 0], 5: [1, 1], 6: [1, 2],
             7: [2, 0], 8: [2, 1], 9: [2, 2]}
    while 1:
        try:
            move = int(input('Pick a position (1-9) '))
            if move < 1 or move > 9:
                print('Invalid location!')
            elif not (moves[move] in checkEmpty()):
                print('Location filled')
            else:
                x = moves[move][0]
                y = moves[move][1]
                # set move
                board[x][y] = player
                printBoard()
                break
        except(KeyError, ValueError):
            print('Please pick a valid number!')

def AIMove(player):
    # first AI move
    if len(checkEmpty()) == 9:
        # generate random move
        x = np.random.choice(np.arange(0, 2))
        y = np.random.choice(np.arange(0, 2))
        # set move
        board[x][y] = player
        printBoard()
    # other AI moves
    else:
        result = MiniMaxAB(-inf, inf, player)
        # set move
        board[result[0]][result[1]] = player
        printBoard()
# ------------------------------------------------------------------
# STATES
# MiniMax Algorithm with Alpha-Beta Pruning
def MiniMaxAB(alpha, beta, player):
    row = -1
    col = -1
    if gameWon():
        return [row, col, getScore()]

    else:
        for cell in checkEmpty():
            x = cell[0]
            y= cell[1]
            setMove(cell[0], cell[1], player)
            # set move
            #board[x][y] = player
            score = MiniMaxAB(alpha, beta, -player)
            if player == XPLAYER:
                # X is always the max player
                if score[2] > alpha:
                    alpha = score[2]
                    row = cell[0]
                    col = cell[1]

            else:
                if score[2] < beta:
                    beta = score[2]
                    row = cell[0]
                    col = cell[1]

            # set move
            # board[x][y] = EMPTY
            setMove(cell[0], cell[1], EMPTY)

            if alpha >= beta:
                break

        if player == XPLAYER:
            return [row, col, alpha]

        else:
            return [row, col, beta]
# check empty cells and return them
def checkEmpty():
    emptyCells = []
    for x in range(0, 3):
        for y in range(0, 3):
            if board[x][y] == EMPTY:
                emptyCells.append([x, y])
    return emptyCells
# 
def winningPlayer(player):
    # player -> symbol (X or O)
    winningStates = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],            
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],            
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    if [player, player, player] in winningStates:
        return True
    return False

def gameWon():
    return winningPlayer(XPLAYER) or winningPlayer(OPLAYER)

def getScore():
    if winningPlayer(XPLAYER):
        return 10
    elif winningPlayer(OPLAYER):
        return -10
    else:
        return 0

def setMove(x, y, player):
    board[x][y] = player
# ------------------------------------------------------------------

def main():
    # specify 1st or 2nd
    while True:
        try:
            order = int(input('Would you like to go first or second? (1/2) '))
            if not (order == 1 or order == 2):
                print('Please enter 1 or 2!')
            else:
                break
        except(KeyError, ValueError):
            print('Please pick a valid number!')

    if order == 2:
        player = OPLAYER
    else:
        player = XPLAYER

    while not (len(checkEmpty())==0 or gameWon()):
        makeMove(player, order)
        print()
        player *= -1

    # print game end state
    if winningPlayer(XPLAYER):
        print('X has won! ' + '\n')
    elif winningPlayer(OPLAYER):
        print('O\'s have won! ' + '\n')
    else:
        print('Draw!' + '\n')
    exit()

if __name__ == '__main__':
    main()