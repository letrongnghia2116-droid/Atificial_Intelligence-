from ai import TicTacToeAI

class AlphaBetaAI(TicTacToeAI):
    def minimax_alpha_beta(self, board, depth, is_maximizing, alpha, beta):
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
                        score = self.minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                        board[row][col] = 0
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for row in range(self.rows):
                for col in range(self.cols):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        score = self.minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                        board[row][col] = 0
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
            return best_score
