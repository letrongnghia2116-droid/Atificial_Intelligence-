import copy


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

    # up
    if x > 0 and state[x - 1][y] != -1:
        move.append("up")

    # down
    if x < n - 1 and state[x + 1][y] != -1:
        move.append("down")

    # left
    if y > 0 and state[x][y - 1] != -1:
        move.append("left")

    # right
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


# value
# càng lớn càng tốt
# dùng số ô sạch
def value(state):

    clean = 0

    for row in state:
        for cell in row:
            if cell == 0:
                clean += 1

    return clean


def SteepestAscentHillClimbing(problem,
                               start_robot):

    initial_state = copy.deepcopy(problem)

    # hút sạch ô bắt đầu
    initial_state[start_robot[0]][start_robot[1]] = 0

    current = Node(
        initial_state,
        start_robot,
        value(initial_state)
    )

    while True:

        # goal
        if goal_test(current.state):
            return solution(current)

        best_neighbor = None

        # sinh TẤT CẢ neighbor
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

            # chọn neighbor tốt nhất
            if (best_neighbor is None or
                    child_node.value >
                    best_neighbor.value):

                best_neighbor = child_node

        # nếu tốt hơn current
        if (best_neighbor is not None and
                best_neighbor.value >
                current.value):

            current = best_neighbor

        else:

            return solution(current)