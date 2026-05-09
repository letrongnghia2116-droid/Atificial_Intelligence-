import random

def possible_move(x, y, n, m):
    move = []
    if x > 0: move.append('up')
    if x < n - 1: move.append('down')
    if y > 0: move.append('left')
    if y < m - 1: move.append('right')
    return move

def rules(status_value, move):
    return random.choice(move)

def action(x, y, actions):
    if actions == 'up':
        x -= 1
    elif actions == 'down':
        x += 1
    elif actions == 'left':
        y -= 1
    elif actions == 'right':
        y += 1
    return x, y

def is_clean(matrix):
    for row in matrix:
        for cell in row:
            if cell == 1:
                return False
    return True

def print_matrix(matrix, x, y):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if i == x and j == y:
                print('R', end=' ') # vị trí hiện tại của robot
            else:
                print(matrix[i][j], end=' ')
        print()
    print("----------------")

def main():
    x = 0
    y = 0

    matrix = [
        [0, 1, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]

    for step in range(100):
        print(f"Step {step + 1}")
        print_matrix(matrix, x, y)

        if is_clean(matrix):
            print("San nha da sach!")
            break

        if matrix[x][y] == 1:
            print("Action: clean")
            matrix[x][y] = 0

        move = possible_move(x, y, len(matrix), len(matrix[0]))

        actions = rules(matrix[x][y], move)
        print("Action:", actions)
        x, y = action(x, y, actions)

main()