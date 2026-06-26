from collections import deque


class Node:
    def __init__(self, state, parent, act, cost_path):
        self.state = state
        self.parent = parent
        self.act = act
        self.cost_path = cost_path


goal = (
    (0, 0, 0, 0),
    (0, 2, -1, 0),
    (0, -1, 0, 0),
    (0, 0, 0, 0)
)


def get_start_state():

    s1 = (
        (2, 0, 1, 1),
        (0, 0, -1, 1),
        (1, -1, 1, 1),
        (1, 0, 0, 1)
    )

    s2 = (
        (0, 2, 1, 1),
        (0, 0, -1, 1),
        (1, -1, 1, 1),
        (1, 0, 0, 1)
    )

    s3 = (
        (0, 0, 1, 1),
        (2, 0, -1, 1),
        (1, -1, 1, 1),
        (1, 0, 0, 1)
    )

    s4 = (
        (0, 0, 1, 1),
        (0, 2, -1, 1),
        (1, -1, 1, 1),
        (1, 0, 0, 1)
    )

    return (s1, s2, s3, s4)


def get_location(state):

    for i in range(len(state)):
        for j in range(len(state[0])):

            if state[i][j] == 2:
                return i, j

    return None, None


def possible_move():

    return ["up", "down", "left", "right"]


def transition(state, move):

    if state == goal:
        return state

    x, y = get_location(state)

    nx, ny = x, y

    if move == "up":
        nx -= 1

    elif move == "down":
        nx += 1

    elif move == "left":
        ny -= 1

    elif move == "right":
        ny += 1

    if (
        0 <= nx < len(state)
        and
        0 <= ny < len(state[0])
        and
        state[nx][ny] != -1
    ):

        matrix = [list(row) for row in state]

        matrix[x][y] = 0
        matrix[nx][ny] = 2

        return tuple(tuple(row) for row in matrix)

    return state


def act(node, move):

    next_states = []

    for state in node.state:

        next_states.append(
            transition(state, move)
        )

    new_belief = tuple(next_states)

    return Node(
        new_belief,
        node,
        move,
        node.cost_path + 1
    )


def is_goal(node):

    return all(
        state == goal
        for state in node.state
    )


def matrix_to_tuple(belief_state):

    return belief_state


def solve(start):

    frontier = deque()

    start_node = Node(
        start,
        None,
        "START",
        0
    )

    frontier.append(start_node)

    reached = set()
    reached.add(
        matrix_to_tuple(start)
    )

    if is_goal(start_node):
        return start_node

    while frontier:

        node = frontier.popleft()

        for move in possible_move():

            child = act(node, move)

            if is_goal(child):
                return child

            state_tuple = matrix_to_tuple(
                child.state
            )

            if state_tuple not in reached:

                reached.add(state_tuple)

                frontier.append(child)

    return None


def get_path(node):

    path = []

    while node is not None:

        path.append(
            (node.state, node.act)
        )

        node = node.parent

    path.reverse()

    return path


def print_matrix(matrix):

    for row in matrix:

        for value in row:

            print(value, end=" ")

        print()


def run():

    print(
        "Máy hút bụi giải bằng Belief State Search"
    )

    start = get_start_state()

    result = solve(start)

    if result is None:

        print(
            "Không tìm thấy lời giải conformant"
        )

        return

    path = get_path(result)

    for step, p in enumerate(path):

        print(f"\nStep: {step}")
        print(f"Action: {p[1]}")

        belief_state = p[0]

        print(
            f"Kích thước Belief State: {len(belief_state)}"
        )

        for idx, state in enumerate(
            belief_state
        ):

            print(
                f"Trạng thái khả thi #{idx + 1}"
            )

            print_matrix(state)

        print("=" * 30)

    actions = [
        p[1]
        for p in path
        if p[1] != "START"
    ]

    print(
        "\nSolution Path:",
        " -> ".join(actions)
    )


if __name__ == "__main__":
    run()