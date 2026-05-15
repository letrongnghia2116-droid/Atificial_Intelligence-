import copy
import random

def move_possible(x, y, state, visited):

    new_moves = []
    old_moves = []

    n = len(state)
    m = len(state[0])

    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    for action, (dx, dy) in directions.items():

        nx = x + dx
        ny = y + dy

        # kiểm tra biên + vật cản
        if 0 <= nx < n and 0 <= ny < m and state[nx][ny] != -1:

            # ô chưa đi
            if (nx, ny) not in visited:
                new_moves.append(action)

            # ô đã đi
            else:
                old_moves.append(action)

    # ưu tiên ô mới
    if len(new_moves) > 0:
        return new_moves

    # bị kẹt quay lại ô cũ 
    return old_moves


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

def make_state(matrix, x, y):
    return (copy.deepcopy(matrix), x, y)

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
                print('X', end=' ')

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
    visited = []
    visited.append((x, y))

    for step in range(100):

        print(f"Step {step + 1}")

        print_matrix(matrix, x, y)

        # kiểm tra sạch
        if is_clean(matrix):
            print("San nha da sach!")
            break

        # làm sạch
        if matrix[x][y] == 1:

            print("Action: clean")

            matrix[x][y] = 0

        # lưu trạng thái sau khi clean
        visited.append((x, y))

        # tìm hướng đi
        move = move_possible(x, y, matrix, visited )

        # bị kẹt
        if not move:
            print("Robot bi ket!")
            break

        # chọn hành động
        actions = rules(move)

        print("Action:", actions)

        # di chuyển
        x, y = action(x, y, actions)

        # lưu trạng thái mới
        visited.append((x, y))


main()