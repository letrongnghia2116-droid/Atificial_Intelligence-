class TicTacToeAI:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols
        self.nodes_evaluated = 0

    def check_win(self, board, player):
        # Kiểm tra hàng dọc
        for col in range(self.cols):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                return True
        # Kiểm tra hàng ngang
        for row in range(self.rows):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                return True
        # Kiểm tra đường chéo
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        if board[2][0] == player and board[1][1] == player and board[0][2] == player:
            return True
        return False

    def is_board_full(self, board):
        for row in range(self.rows):
            for col in range(self.cols):
                if board[row][col] == 0:
                    return False
        return True

