import random
import copy

def move_possible(x, y, n, m, state, matrix):

    move = []

    directions = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    for action, (dx, dy) in directions.items():

        nx = x + dx
        ny = y + dy

        if 0 <= nx < n and 0 <= ny < m:

            # tạo trạng thái mới
            new_state = copy.deepcopy(state)

            # swap
            new_state[x][y], new_state[nx][ny] = \
                new_state[nx][ny], new_state[x][y]

            # kiểm tra đã đi chưa
            if new_state not in matrix:
                move.append(action)

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


def print_matrix(state):

    for row in state:
        print(row)

    print("----------------")


def swap_(x, y, i, j, state):

    temp = state[i][j]
    state[i][j] = state[x][y]
    state[x][y] = temp

    return state


def main():

    x = 2
    y = 1

    goal = [
        [0,1,2],
        [3,4,5],
        [6,7,8]
    ]

    # trạng thái hiện tại
    state = [
        [1,2,3],
        [4,5,6],
        [8,0,7]
    ]

    matrix = []

    # lưu trạng thái đầu tiên
    matrix.append(copy.deepcopy(state))

    for step in range(100):

        print(f"Step {step+1}")

        print_matrix(state)

        move = move_possible(
            x,
            y,
            len(state),
            len(state[0]),
            state,
            matrix
        )

        actions = rules(move)

        print("Action:", actions)

        i, j = action(x, y, actions)

        state = swap_(x, y, i, j, state)

        x, y = i, j

        # lưu trạng thái mới
        if state not in matrix:
            matrix.append(copy.deepcopy(state))

        if state == goal:
            print("Đã hoàn thành bài toán")
            break

main()