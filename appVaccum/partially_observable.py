from collections import deque


class Node:
    def __init__(self, state, parent, act, cost_path):
        self.state = state
        self.parent = parent
        self.act = act
        self.cost_path = cost_path


def get_goals():

    g1 = (
        (0, 0, 0, 1),
        (1, 2, -1, 0),
        (0, -1, 0, 0),
        (1, 0, 0, 0)
    )

    g2 = (
        (0, 0, 0, 0),
        (0, 2, -1, 0),
        (0, -1, 0, 0),
        (0, 0, 0, 0)
    )

    return (g1, g2)


def get_start_state():

    s1_clean = (
        (2, 0, 1, 1),
        (0, 0, -1, 0),
        (0, -1, 0, 0),
        (0, 0, 0, 0)
    )

    s1_dirty = (
        (2, 0, 1, 1),
        (0, 0, -1, 0),
        (0, -1, 0, 0),
        (1, 0, 0, 0)
    )

    s2_clean = (
        (0, 2, 1, 1),
        (0, 0, -1, 0),
        (0, -1, 0, 0),
        (0, 0, 0, 0)
    )

    s2_dirty = (
        (0, 2, 1, 1),
        (0, 0, -1, 0),
        (0, -1, 0, 0),
        (1, 0, 0, 0)
    )

    s3_clean = (
        (0, 0, 1, 1),
        (2, 0, -1, 0),
        (0, -1, 0, 0),
        (0, 0, 0, 0)
    )

    s3_dirty = (
        (0, 0, 1, 1),
        (2, 0, -1, 0),
        (0, -1, 0, 0),
        (1, 0, 0, 0)
    )

    s4_clean = (
        (0, 0, 1, 1),
        (0, 2, -1, 0),
        (0, -1, 0, 0),
        (0, 0, 0, 0)
    )

    s4_dirty = (
        (0, 0, 1, 1),
        (0, 2, -1, 0),
        (0, -1, 0, 0),
        (1, 0, 0, 0)
    )

    return (
        s1_clean, s1_dirty,
        s2_clean, s2_dirty,
        s3_clean, s3_dirty,
        s4_clean, s4_dirty
    )


def get_location(state):

    for i in range(len(state)):
        for j in range(len(state[0])):

            if state[i][j] == 2:
                return i, j

    return None, None


def possible_move():

    return [
        "up",
        "down",
        "left",
        "right"
    ]


def transition(state, move, goals):

    if state in goals:
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

        return tuple(
            tuple(row)
            for row in matrix
        )

    return state


def act(node, move, goals):

    next_states = []

    for state in node.state:

        next_states.append(
            transition(
                state,
                move,
                goals
            )
        )

    new_belief = tuple(next_states)

    return Node(
        new_belief,
        node,
        move,
        node.cost_path + 1
    )


def is_goal(node, goals):

    return all(
        state in goals
        for state in node.state
    )


def matrix_to_tuple(belief_state):

    return belief_state


def solve(start, goals):

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

    if is_goal(start_node, goals):
        return start_node

    while frontier:

        node = frontier.popleft()

        for move in possible_move():

            child = act(
                node,
                move,
                goals
            )

            if is_goal(
                child,
                goals
            ):
                return child

            state_tuple = matrix_to_tuple(
                child.state
            )

            if state_tuple not in reached:

                reached.add(
                    state_tuple
                )

                frontier.append(
                    child
                )

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

    goals = get_goals()

    start = get_start_state()

    print(
        "Máy hút bụi với quan sát một phần bắt đầu hoạt động\n"
    )

    print(
        "Trạng thái bắt đầu dự đoán:"
    )

    print("? ? 1 1")
    print("? ? -1 0")
    print("0 -1 0 0")
    print("? 0 0 0")

    print("=" * 30)

    print(
        "Các trạng thái đích khả thi:"
    )

    for idx, goal in enumerate(goals):

        print(
            f"Goal #{idx+1}"
        )

        print_matrix(goal)

        print()

    print("=" * 30)

    result = solve(
        start,
        goals
    )

    if result is None:

        print(
            "Không tìm thấy lời giải"
        )

        return

    path = get_path(result)

    for step, p in enumerate(path):

        print(
            f"\nStep: {step}"
        )

        print(
            f"Action: {p[1]}"
        )

        belief_state = p[0]

        print(
            f"Kích thước Belief State: {len(belief_state)}"
        )

        for idx, state in enumerate(
            belief_state
        ):

            print(
                f"Trạng thái khả thi #{idx+1}"
            )

            print_matrix(state)

        print("=" * 30)

    actions = [
        p[1]
        for p in path
        if p[1] != "START"
    ]

    print(
        "\nSolution Path:"
    )

    print(
        " -> ".join(actions)
    )


if __name__ == "__main__":
    run()