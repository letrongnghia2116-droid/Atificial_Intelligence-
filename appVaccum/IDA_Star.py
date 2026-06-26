import copy


class Node:

    def __init__(self,
                 state,
                 robot,
                 parent=None,
                 action=None,
                 g=0,
                 h=0):

        self.state = state
        self.robot = robot
        self.parent = parent
        self.action = action

        self.g = g
        self.h = h
        self.f = g + h


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


# heuristic = số ô bẩn còn lại
def heuristic(state):

    h = 0

    for row in state:
        for cell in row:
            if cell == 1:
                h += 1

    return h


def state_key(state, robot):

    return (
        tuple(map(tuple, state)),
        robot
    )


def search(node, threshold, visited):

    f = node.f

    # vượt ngưỡng
    if f > threshold:
        return f

    # goal
    if goal_test(node.state):
        return node

    minimum = float("inf")

    # expand
    for action in actions(node.state, node.robot):

        child_state, child_robot = result(
            node.state,
            node.robot,
            action
        )

        key = state_key(child_state, child_robot)

        if key not in visited:

            g = node.g + 1
            h = heuristic(child_state)

            child_node = Node(
                child_state,
                child_robot,
                node,
                action,
                g,
                h
            )

            visited.add(key)

            result_search = search(
                child_node,
                threshold,
                visited
            )

            if isinstance(result_search, Node):
                return result_search

            # cập nhật ngưỡng nhỏ nhất vượt threshold
            minimum = min(minimum, result_search)

            visited.remove(key)

    return minimum


def IDAStar(problem, start_robot):

    initial_state = copy.deepcopy(problem)

    initial_state[start_robot[0]][start_robot[1]] = 0

    root = Node(
        initial_state,
        start_robot,
        None,
        None,
        g=0,
        h=heuristic(initial_state)
    )

    threshold = root.f

    while True:

        visited = set()

        root_key = state_key(root.state, root.robot)

        visited.add(root_key)

        result_search = search(
            root,
            threshold,
            visited
        )

        # tìm thấy lời giải
        if isinstance(result_search, Node):
            return solution(result_search)

        # không còn node nào để mở rộng
        if result_search == float("inf"):
            return None

        # tăng threshold
        threshold = result_search