import random

GOAL_STATE = [1, 2, 3,
              4, 5, 6,
              7, 8, 0]


class SimpleReflexAgent:

    def get_possible_moves(self, empty_index):

        moves = []

        row = empty_index // 3
        col = empty_index % 3

        if row > 0:
            moves.append("UP")

        if row < 2:
            moves.append("DOWN")

        if col > 0:
            moves.append("LEFT")

        if col < 2:
            moves.append("RIGHT")

        return moves

    def rules(self, board):

        empty = board.index(0)

        possible_moves = self.get_possible_moves(empty)

        """
        RULES IF-THEN
        """

        # Nếu ô trống ở góc trên trái
        if empty == 0:
            return "RIGHT"

        # Nếu ô trống ở góc trên phải
        elif empty == 2:
            return "DOWN"

        # Nếu ô trống ở góc dưới trái
        elif empty == 6:
            return "UP"

        # Nếu ô trống ở góc dưới phải
        elif empty == 8:
            return "LEFT"

        # Các trường hợp khác -> random
        return random.choice(possible_moves)

    def apply_move(self, board, move):

        new_board = board[:]

        empty = new_board.index(0)

        target = empty

        if move == "UP":
            target = empty - 3

        elif move == "DOWN":
            target = empty + 3

        elif move == "LEFT":
            target = empty - 1

        elif move == "RIGHT":
            target = empty + 1

        new_board[empty], new_board[target] = (
            new_board[target],
            new_board[empty]
        )

        return new_board

    def print_board(self, board):

        for i in range(0, 9, 3):
            print(board[i:i+3])

    def solve(self, board, max_steps=30):

        current = board[:]

        print("Bàn cờ ban đầu:")
        self.print_board(current)

        step = 0

        while current != GOAL_STATE and step < max_steps:

            move = self.rules(current)

            current = self.apply_move(current, move)

            step += 1

            print(f"\nBước {step}: {move}")

            self.print_board(current)

        if current == GOAL_STATE:
            print("\nĐã đạt goal state!")

        else:
            print("\nSimple Reflex Agent không giải được.")


board = [1, 2, 3,
         5, 6, 4,
         8, 7, 0]

agent = SimpleReflexAgent()

agent.solve(board)