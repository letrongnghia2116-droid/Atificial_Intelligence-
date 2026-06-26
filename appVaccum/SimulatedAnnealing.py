import copy
import random
import math


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


# Heuristic:
# càng nhiều ô sạch càng tốt
def value(state):

    clean = 0

    for row in state:
        for cell in row:
            if cell == 0:
                clean += 1

    return clean


def random_start(problem):

    free_cells = []

    for i in range(len(problem)):
        for j in range(len(problem[0])):

            if problem[i][j] != -1:
                free_cells.append((i, j))

    return random.choice(free_cells)


def random_neighbor(node):

    possible_actions = actions(
        node.state,
        node.robot
    )

    if len(possible_actions) == 0:
        return None

    action = random.choice(
        possible_actions
    )

    child_state, child_robot = result(
        node.state,
        node.robot,
        action
    )

    child_value = value(child_state)

    return Node(
        child_state,
        child_robot,
        child_value,
        node,
        action
    )


def SimulatedAnnealing(problem, robot = None,
                       T0=100,
                       Tmin=0.01,
                       alpha=0.995,
                       max_iteration=10000):

    # Khởi tạo ngẫu nhiên
    if robot is None:
        start_robot = random_start(problem)
    else:
        start_robot = robot

    start_state = copy.deepcopy(problem)

    start_state[
        start_robot[0]
    ][
        start_robot[1]
    ] = 0

    current = Node(
        start_state,
        start_robot,
        value(start_state)
    )

    best = current

    T = T0

    iteration = 0

    while T > Tmin and iteration < max_iteration:

        iteration += 1

        # Goal test
        if goal_test(current.state):
            return solution(current)

        neighbor = random_neighbor(current)

        if neighbor is None:
            break

        # Maximize value()
        delta = (
            neighbor.value
            - current.value
        )

        # Trạng thái tốt hơn
        if delta > 0:

            current = neighbor

        else:

            probability = math.exp(
                delta / T
            )

            if random.random() < probability:
                current = neighbor

        # Lưu trạng thái tốt nhất
        if current.value > best.value:
            best = current

        # Cooling
        T = alpha * T

    return solution(best)
