from collections import deque
import copy


class Node:

    def __init__(self,
                 state,
                 robot,
                 parent=None,
                 action=None,
                 total_cost=0):

        self.state = state
        self.robot = robot
        self.parent = parent
        self.action = action
        self.total_cost = total_cost


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


def DFS(problem, start_robot):


    initial_state = copy.deepcopy(problem)

    initial_state[
        start_robot[0]
    ][
        start_robot[1]
    ] = 0

    root = Node(
        initial_state,
        start_robot
    )

    # frontier queue

    frontier = deque([root])

    # visited

    reached = set()

    root_key = (
        tuple(map(tuple, root.state)),
        root.robot
    )

    reached.add(root_key)

    # BFS

    while frontier:

        node = frontier.pop()

        # goal

        if goal_test(node.state):

            return solution(node)

        # expand

        for action in actions(
                node.state,
                node.robot
        ):

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

                child = Node(
                    child_state,
                    child_robot,
                    node,
                    action,
                    node.total_cost + 1
                )

                frontier.append(child)

                reached.add(child_key)

    return None