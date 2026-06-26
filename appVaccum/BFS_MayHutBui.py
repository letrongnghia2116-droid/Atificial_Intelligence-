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
        self.robot = robot # vị trí của robot
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


def BFS(problem, start_robot):


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

        node = frontier.popleft()

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




def transition_belief(belief_state, action):
    new_belief = set()
    for grid, robot in belief_state:
        x, y = robot
        n = len(grid)
        m = len(grid[0])
        
        nx, ny = x, y
        if action == "up" and x > 0 and grid[x - 1][y] != -1:
            nx, ny = x - 1, y
        elif action == "down" and x < n - 1 and grid[x + 1][y] != -1:
            nx, ny = x + 1, y
        elif action == "left" and y > 0 and grid[x][y - 1] != -1:
            nx, ny = x, y - 1
        elif action == "right" and y < m - 1 and grid[x][y + 1] != -1:
            nx, ny = x, y + 1
            
        grid_list = [list(row) for row in grid]
        grid_list[nx][ny] = 0
        new_grid = tuple(tuple(row) for row in grid_list)
        
        new_belief.add((new_grid, (nx, ny)))
    return frozenset(new_belief)


def get_possible_robot_positions(problem):
    positions = []
    for r in range(len(problem)):
        for c in range(len(problem[0])):
            if problem[r][c] != -1:
                positions.append((r, c))
    return positions


def generate_initial_belief(problem, dirt_unknown=False):
    robot_positions = get_possible_robot_positions(problem)
    n = len(problem)
    m = len(problem[0])
    
    belief = set()
    
    if not dirt_unknown:
        grid_base = tuple(tuple(row) for row in problem)
        for r_pos in robot_positions:
            grid_list = [list(row) for row in grid_base]
            grid_list[r_pos[0]][r_pos[1]] = 0
            grid_tuple = tuple(tuple(row) for row in grid_list)
            belief.add((grid_tuple, r_pos))
    else:
        non_wall_cells = []
        for r in range(n):
            for c in range(m):
                if problem[r][c] != -1:
                    non_wall_cells.append((r, c))
                    
        num_cells = len(non_wall_cells)
        for i in range(1 << num_cells):
            grid_list = [row[:] for row in problem]
            for idx, (r, c) in enumerate(non_wall_cells):
                is_dirty = (i >> idx) & 1
                grid_list[r][c] = 1 if is_dirty else 0
                
            grid_tuple_base = tuple(tuple(row) for row in grid_list)
            
            for r_pos in robot_positions:
                grid_list_with_robot = [list(row) for row in grid_tuple_base]
                grid_list_with_robot[r_pos[0]][r_pos[1]] = 0
                grid_tuple = tuple(tuple(row) for row in grid_list_with_robot)
                belief.add((grid_tuple, r_pos))
                
    return frozenset(belief)


def goal_test_belief(belief_state):
    for grid, robot in belief_state:
        for row in grid:
            if 1 in row:
                return False
    return True


def BFS_Belief(problem, dirt_unknown=False):
    # 1. Tạo trạng thái niềm tin ban đầu
    initial_belief = generate_initial_belief(problem, dirt_unknown)
    
    # 2. Hàng đợi frontier chứa các tuple (belief_state, path)
    frontier = deque([(initial_belief, [])])
    
    # 3. Tập reached chỉ lưu các belief_state đã đạt tới
    reached = {initial_belief}
    
    # Các hành động di chuyển trong lưới
    actions_list = ["up", "down", "left", "right"]
    
    while frontier:
        belief_state, path = frontier.popleft()
        
        # Kiểm tra đích: tất cả các trạng thái trong niềm tin sạch bụi
        if goal_test_belief(belief_state):
            return path
            
        # Mở rộng các hành động
        for action in actions_list:
            child_belief = transition_belief(belief_state, action)
            
            if child_belief not in reached:
                reached.add(child_belief)
                frontier.append((child_belief, path + [action]))
    return None



if __name__ == "__main__":
    # Lưới thử nghiệm 2x2:
    # 1: có bụi, 0: sạch, -1: tường
    grid = [
        [1, 1],
        [0, 1]
    ]
    
    print("=== KIEM THU THUAT TOAN MAY HUT BUI KHONG CAM BIEN (BELIEF STATE SEARCH) ===")
    print("Luoi bui ban dau:")
    for row in grid:
        print(row)
        
    print("\n1. Truong hop 1: Vi tri bui co dinh, vi tri robot ban dau chua biet")
    plan1 = BFS_Belief(grid, dirt_unknown=False)
    print("-> Chuoi hanh dong toi uu:", plan1)
    
    print("\n2. Truong hop 2: Khong biet vi tri robot va ca vi tri bui ban dau")
    plan2 = BFS_Belief(grid, dirt_unknown=True)
    print("-> Chuoi hanh dong toi uu:", plan2)