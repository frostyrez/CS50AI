"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xcount = 0
    ocount = 0
    for i in range(len(board)):
        xcount = xcount + board[i].count("X")
        ocount = ocount + board[i].count("O")
    if xcount == ocount:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_list = set()
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                action_list.add((i,j))
    return action_list        


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = copy.deepcopy(board)
    newboard[action[0]][action[1]] = player(newboard)
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check horizontal
    for i in range(3):
        if board[i][0] is not None:
            if board[i].count(board[i][0]) == 3:
                return board[i][0]  
    # check vert
    for i in range(3):
        if board[0][i] is not None:
            counter = 0
            for j in range(3):
                if board[j][i] == board[0][i]:
                    counter += 1
            if counter == 3:
                return board[0][i]
    if board[1][1]:
        # Check diag 1
        counter = 0
        for i in range(3):
            if board[i][i] == board[1][1]:
                counter += 1
        if counter == 3:
            return board[1][1]
        # Check diag 2
        counter = 0
        for i in range(3):
            if board[i][2-i] == board[1][1]:
                counter += 1
        if counter == 3:
            return board[i][0]


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    gamewinner = winner(board)
    if gamewinner == 'X' or gamewinner == 'O':
        return True
    else: # is board full?
        for i in range(3):
            for j in range(3):
                if board[i][j] == None:
                    return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    gamewinner = winner(board)
    if gamewinner == 'X':
        return 1
    elif gamewinner == 'O':
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    move = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        aux, act = min_value(result(board, action))
        if aux > v:
            v = aux
            move = action
            if v == 1:
                return v, move

    return v, move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    move = None
    for action in actions(board):
        # v = max(v, min_value(result(board, action)))
        aux, act = max_value(result(board, action))
        if aux < v:
            v = aux
            move = action
            if v == -1:
                return v, move

    return v, move


# def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     # Go middle by default
#     if board[1][1] is None:
#         return (1,1)
#     else:
#         # Populate list of moves with scores
#         ai = player(board)
#         tracker = []
#         actions1 = actions(board)
#         for act1 in actions1:
#             board1 = result(board,act1)
#             tracker.append([act1,utility(board1)])
#             if not terminal(board1):
#                 actions2 = actions(board1)               
#                 for act2 in actions2:
#                     board2 = result(board1,act2)
#                     if not terminal(board2):
#                         actions3 = actions(board2)
#                         for act3 in actions3:
#                             if ai == 'X':
#                                 tracker[-1][1] = min(tracker[-1][1],utility(result(board2,act3)))
#                             elif ai == 'O':
#                                 tracker[-1][1] = max(tracker[-1][1],utility(result(board2,act3)))

#         # Find best
#         if ai == 'X': # Want to max
#             v = -10
#             for i in range(len(tracker)):
#                 v = max(v,tracker[i][1])
#         elif ai == 'O': # Want to min
#             v = 10
#             for i in range(len(tracker)):
#                 v = min(v,tracker[i][1])    
#         else: # Error
#             print("Error in minimax")
#             return
        
#         # Find corresponding move
#         for i in range(len(tracker)):
#             if tracker[i][1] == v:
#                 return tracker[i][0]