import math

x = "X"
o = "O"
empty = None


def initialState():
    # Returns the starting state of the board
    return [[empty, empty, empty],
            [empty, empty, empty],
            [empty, empty, empty]]


def player(board):
    # Returns the player who has the next turn on a board.
    xCount = sum(cell == x for row in board for cell in row)
    oCount = sum(cell == o for row in board for cell in row)
    return o if xCount > oCount else x


def actions(board):
    # Returns set of all possible actions (i, j) available on the board.
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == empty}


def result(board, action):
    # Returns the board that results from making move (i, j) on the board.
    i, j = action
    if board[i][j] != empty:
        raise ValueError("Invalid action: Cell already occupied.")
    newBoard = [row[:] for row in board]  # Make a copy of the board
    newBoard[i][j] = player(board)  # Set the current player
    return newBoard


def winner(board):
    # Returns the winner of the game, if there is one.
    for line in board + list(zip(*board)) + [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]:
        if line[0] is not empty and all(cell == line[0] for cell in line):
            return line[0]
    return None


def terminal(board):
    # Returns True if game is over, False otherwise.
    return winner(board) is not None or all(cell is not empty for row in board for cell in row)


def utility(board):
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    win = winner(board)
    if win == x:
        return 1
    elif win == o:
        return -1
    else:
        return 0


def minimax(board):
    # Returns the optimal action for the current player on the board.
    if terminal(board):
        return None

    currentPlayer = player(board)
    bestAction = None

    if currentPlayer == x:
        bestValue = -math.inf
        for action in actions(board):
            value = minimaxValue(result(board, action))
            if value > bestValue:
                bestValue = value
                bestAction = action
    else:
        bestValue = math.inf
        for action in actions(board):
            value = minimaxValue(result(board, action))
            if value < bestValue:
                bestValue = value
                bestAction = action

    return bestAction


def minimaxValue(board):
    # Returns the minimax value of the board.
    if terminal(board):
        return utility(board)

    if player(board) == x:
        bestValue = -math.inf
        for action in actions(board):
            value = minimaxValue(result(board, action))
            bestValue = max(bestValue, value)
        return bestValue
    else:
        bestValue = math.inf
        for action in actions(board):
            value = minimaxValue(result(board, action))
            bestValue = min(bestValue, value)
        return bestValue
