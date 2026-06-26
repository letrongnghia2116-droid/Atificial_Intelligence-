import copy
import random


class Node:

    def __init__(self,
                 state,
                 robot,
                 value=0,
                 parent=None,
                 action=None):

        self.state = state
        self.robot = robot
        self.value = value

        self.parent = parent
        self.action = action


def actions(state, robot):

    x, y = robot

    n = len(state)
    m = len(state[0])

    move = []

    if x > 0 and state[x - 1][y] != -1:
        move.append("up")

    if x < n - 1 and state[x + 1][y] != -1:
        move.append("down")

    if y > 0 and state[x][y - 1] != -1:
        move.append("left")

    if y < m - 1 and state[x][y + 1] != -1:
        move.append("right")

    return move


def result(state, robot, action):

    new_state = copy.deepcopy(state)

    x, y = robot

    if action == "up":
        nx, ny = x - 1, y

    elif action == "down":
        nx, ny = x + 1, y

    elif action == "left":
        nx, ny = x, y - 1

    elif action == "right":
        nx, ny = x, y + 1

    # hút sạch ô mới
    new_state[nx][ny] = 0

    return new_state, (nx, ny)

def goal_test(state):

    for row in state:
        if 1 in row:
            return False

    return True

def solution(node):

    path = []

    while node.parent is not None:
        path.append(node.action)
        node = node.parent

    path.reverse()

    return path

def value(state):

    clean = 0

    for row in state:
        for cell in row:
            if cell == 0:
                clean += 1

    return clean


# Chọn vị trí bắt đầu ngẫu nhiên
def random_start(problem):

    free_cells = []

    for i in range(len(problem)):
        for j in range(len(problem[0])):

            if problem[i][j] != -1:
                free_cells.append((i, j))

    return random.choice(free_cells)

def RandomRestartHillClimbing(problem,robot=None,
                              max_restart=20):

    best_solution = []
    best_value = -1

    for restart in range(max_restart):
        if robot is None:
            start_robot = random_start(problem)
        else:
            start_robot = robot

        initial_state = copy.deepcopy(problem)

        initial_state[start_robot[0]][start_robot[1]] = 0

        current = Node(
            initial_state,
            start_robot,
            value(initial_state)
        )

        while True:

            # Goal
            if goal_test(current.state):

                return solution(current)

            best_neighbor = None

            # Sinh toàn bộ neighbor
            for action in actions(current.state,
                                  current.robot):

                child_state, child_robot = result(
                    current.state,
                    current.robot,
                    action
                )

                child_value = value(child_state)

                child_node = Node(
                    child_state,
                    child_robot,
                    child_value,
                    current,
                    action
                )

                if (best_neighbor is None or
                        child_node.value >
                        best_neighbor.value):

                    best_neighbor = child_node

            # Tiếp tục leo đồi
            if (best_neighbor is not None and
                    best_neighbor.value >
                    current.value):

                current = best_neighbor

            else:

                if current.value > best_value:

                    best_value = current.value
                    best_solution = solution(current)

                break

    return best_solution

