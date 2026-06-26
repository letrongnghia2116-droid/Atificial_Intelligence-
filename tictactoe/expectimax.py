from ai import TicTacToeAI

class ExpectimaxAI(TicTacToeAI):
    def expectimax(self, board, depth, is_maximizing):
        self.nodes_evaluated += 1

        if self.check_win(board, 2):  # AI thắng
            return 10 - depth
        if self.check_win(board, 1):  # Người thắng
            return depth - 10
        if self.is_board_full(board):  # Hòa
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for row in range(self.rows):
                for col in range(self.cols):
                    if board[row][col] == 0:
                        board[row][col] = 2
                        score = self.expectimax(board, depth + 1, False)
                        board[row][col] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            total_score = 0
            num_moves = 0
            for row in range(self.rows):
                for col in range(self.cols):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        score = self.expectimax(board, depth + 1, True)
                        board[row][col] = 0
                        total_score += score
                        num_moves += 1
            return total_score / num_moves if num_moves > 0 else 0
