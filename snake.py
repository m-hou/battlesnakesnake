from collections import namedtuple
GameState = namedtuple("game_state", ["me", "snakes", "food", "width", "height", "head"])


moves = ["up", "down", "left", "right"]
 
change = dict(
    up=(0, -1),
    down=(0, 1),
    left=(-1, 0),
    right=(1, 0))

SAFE = set(["0", "F"])

def safe(board, state, x, y):
    return 0 <= y < state.height and 0 <= x < state.width and board[x][y] in SAFE

def best(state, board):
    return max(moves, key=lambda move: h(state, board, move))

def apply_move(state, snake, move):
    state = GameState(**state._asdict())
    y1, x1 = head = snake['coords'][0]
    y, x = move
    snake['coords'] = [(y1+y, x1+x)] + snake['coords'][:-1]

    for s in state.snakes:
        if s['id'] == snake['id']:
            s['coords'] = snake['coords']
    
    return state, update_board(state)

def printboard(board):
    for x in board:
        print(x)
    print("")

def h(state, board, move):
    y1, x1 = head = state.me['coords'][0]
    y, x = change[move]
    print(y, x)
    head = (y1+y, x1+x)
    print(head)
    if safe(board, state, head[0], head[1]):
        state, board = apply_move(state, state.me, change[move])
        printboard(board)
        return sum(
            closest(i, j, state)
            for i in range(state.width)
                for j in range(state.height)
                    if safe(board, state, i, j)
        )
    
    else:
        return -5000

def closest(x, y, state):
        me = state.me['id']
        snakes = state.snakes

        closest = min(snakes,
            key=lambda snake:
            dist(
                snake['coords'][0], # account for entire snake bodies? instead of just head
                (x, y)
            )
        )
 
        return me == closest['id']

def update_board(state):
    snakes = state.snakes
    food = state.food
    width = state.width
    height = state.height

    board = [['0']*width for _ in range(height)]
    for snake in snakes:
        for (x, y) in snake['coords']:
            board[y][x] = '2'#snake['id']
    
    for (x, y) in food:
        board[y][x] = "F"

    return board

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
