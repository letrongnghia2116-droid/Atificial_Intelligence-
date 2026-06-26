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


def random_start(problem):

    free_cells = []

    for i in range(len(problem)):
        for j in range(len(problem[0])):

            if problem[i][j] != -1:
                free_cells.append((i, j))

    return random.choice(free_cells)


def LocalBeamSearch(problem, robot = None,
                    k=5,
                    max_iteration=1000):

    current_states = []

    # Khởi tạo k trạng thái ngẫu nhiên
    for _ in range(k):

        if robot is None:
            start_robot = random_start(problem)
        else:
            start_robot = robot

        initial_state = copy.deepcopy(problem)

        initial_state[start_robot[0]][start_robot[1]] = 0

        current_states.append(
            Node(
                initial_state,
                start_robot,
                value(initial_state)
            )
        )

    iteration = 0

    while iteration < max_iteration:

        iteration += 1

        neighbor_states = []

        # Kiểm tra Goal
        for node in current_states:

            if goal_test(node.state):
                return solution(node)

        # Sinh tất cả trạng thái lân cận
        for node in current_states:

            for action in actions(
                    node.state,
                    node.robot):

                child_state, child_robot = result(
                    node.state,
                    node.robot,
                    action
                )

                child_value = value(child_state)

                child_node = Node(
                    child_state,
                    child_robot,
                    child_value,
                    node,
                    action
                )

                neighbor_states.append(child_node)

        # Không còn neighbor
        if len(neighbor_states) == 0:
            return []

        # Kiểm tra Goal trong Neighbor
        for node in neighbor_states:

            if goal_test(node.state):
                return solution(node)

        # Sắp xếp giảm dần theo heuristic
        neighbor_states.sort(
            key=lambda x: x.value,
            reverse=True
        )

        # Chọn k trạng thái tốt nhất
        current_states = neighbor_states[:k]

    # Hết số vòng lặp
    best_node = max(
        current_states,
        key=lambda x: x.value
    )

    return solution(best_node)