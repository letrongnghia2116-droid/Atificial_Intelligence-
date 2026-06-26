import copy
import heapq


class Node:

    def __init__(self,
                 state: object,
                 robot: object,
                 parent: object = None,
                 action: object = None,
                 g: object = 0,
                 h: object = 0) -> None:

        self.state = state
        self.robot = robot
        self.parent = parent
        self.action = action

        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


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

def AStarSearch(problem, start_robot):

    initial_state = copy.deepcopy(problem)

    # hút sạch ô bắt đầu
    initial_state[start_robot[0]][start_robot[1]] = 0

    root = Node(
        initial_state,
        start_robot,
        None,
        None,
        g=0,
        h=heuristic(initial_state)
    )

    frontier = []

    heapq.heappush(frontier, root)

    reached = set()

    root_key = (
        tuple(map(tuple, root.state)),
        root.robot
    )

    reached.add(root_key)

    while frontier:

        node = heapq.heappop(frontier)

        # goal test
        if goal_test(node.state):
            return solution(node)

        # expand
        for action in actions(node.state, node.robot):

            child_state, child_robot = result(
                node.state,
                node.robot,
                action
            )

            child_key = (
                tuple(map(tuple, child_state)),
                child_robot
            )

            if child_key not in reached:

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

                heapq.heappush(frontier, child_node)

                reached.add(child_key)


    return None
