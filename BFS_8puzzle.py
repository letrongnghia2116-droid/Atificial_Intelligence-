from collections import deque
import copy

class Node:

    def __init__(self, state, parent=None, action=None, total_cost=0):

        self.state = state
        self.parent = parent
        self.action = action
        self.total_cost = total_cost


def actions(state):

    n = len(state)
    m = len(state[0])

    for i in range(n):
        for j in range(m):
            if state[i][j] == 0:
                x = i
                y = j

    move = []

    if x > 0:
        move.append('up')

    if x < n - 1:
        move.append('down')

    if y > 0:
        move.append('left')

    if y < m - 1:
        move.append('right')

    return move


def result(state, action):

    new_state = copy.deepcopy(state)

    n = len(new_state)
    m = len(new_state[0])

    for i in range(n):
        for j in range(m):
            if new_state[i][j] == 0:
                x = i
                y = j

    if action == 'up':
        nx = x - 1
        ny = y

    elif action == 'down':
        nx = x + 1
        ny = y

    elif action == 'left':
        nx = x
        ny = y - 1

    elif action == 'right':
        nx = x
        ny = y + 1

    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

    return new_state


def BFS(problem, goal):

    frontier = deque()

    root = Node(problem)

    frontier.append(root)

    reached = set()

    reached.add(tuple(map(tuple, problem)))

    while frontier:

        node = frontier.popleft()

        if node.state == goal:
            return node

        for action in actions(node.state):

            child_state = result(node.state, action)

            child_key = tuple(map(tuple, child_state))

            if child_key not in reached:

                child = Node(
                    child_state,
                    node,
                    action,
                    node.total_cost + 1
                )

                frontier.append(child)

                reached.add(child_key)

    return None


def solution(node):

    path = []

    while node.parent is not None:

        path.append(node.action)

        node = node.parent

    path.reverse()

    return path

def print_state(state):

    for row in state:
        print(row)

    print()


def main():

    start = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    print("Start State:")
    print_state(start)

    print("Goal State:")
    print_state(goal)

    goal_node = BFS(start, goal)

    if goal_node is None:
        print("Khong tim thay loi giai")
        return

    path = solution(goal_node)

    print("So buoc:", len(path))
    print("Duong di:", path)

    print("\nQua trinh di chuyen:\n")

    current_state = copy.deepcopy(start)

    print_state(current_state)

    for move in path:

        current_state = result(current_state, move)

        print("Move:", move)
        print_state(current_state)


if __name__ == "__main__":
    main()