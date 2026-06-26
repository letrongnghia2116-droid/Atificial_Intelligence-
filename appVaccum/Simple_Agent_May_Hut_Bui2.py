# trường hợp máy hút bụi có vật cản khi gặp vật cản thì không đc di chuyển tới
# bổ sung vào tập luật

'''
Rules:
    If x > 0 and x -1 != -1 move.append("up")
    If x < n - 1 and x +1 != -1 move.append("down")
    If y > 0 and y -1 != -1 move.append("left")
    If y < m - 1 and y + 1 != -1 move.append("right")
'''

# các bước còn lại vẫn giữ nguyên

import random

def possible_move(x, y, matrix):
    move = []
    n = len(matrix)
    m = len(matrix[0])
    if x > 0 and matrix[x - 1][y] != -1:
        move.append('up')

    if x < n - 1 and matrix[x + 1][y] != -1:
        move.append('down')

    if y > 0 and matrix[x][y - 1] != -1:
        move.append('left')

    if y < m - 1 and matrix[x][y + 1] != -1:
        move.append('right')

    return move


def rules(move):
    if len(move) == 0:
        return None
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
                print('R', end=' ')

            elif matrix[i][j] == -1:
                print('X', end=' ')   # vật cản

            else:
                print(matrix[i][j], end=' ')

        print()

    print("----------------")


def main():

    x = 0
    y = 0

    matrix = [
        [0, 1, -1, 1],
        [1, 1, -1, 0],
        [1, 0, 1, 1],
        [-1, 1, 1, 1]
    ]
    # -1 là vật cản
    #  1 là sàn nhà đang bẩn
    #  0 là sàn nhà đã sạch
    for step in range(100):

        print(f"Step {step + 1}")
        print_matrix(matrix, x, y)

        # Nếu sạch
        if is_clean(matrix):
            print("San nha da sach!")
            break

        # Làm sạch
        if matrix[x][y] == 1:
            print("Action: clean")
            matrix[x][y] = 0

        # Tìm hướng đi
        move = possible_move(x, y, matrix)

        # Không còn đường
        if not move:
            print("Robot bi ket!")
            break

        # Chọn hành động
        actions = rules(move)

        print("Action:", actions)

        # Di chuyển
        x, y = action(x, y, actions)


main()