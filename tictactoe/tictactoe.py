import sys
import time
import pygame
from minimax import MinimaxAI
from alpha_beta import AlphaBetaAI
from expectimax import ExpectimaxAI

# Khởi tạo pygame
pygame.init()

# --- CẤU HÌNH HẰNG SỐ ---
WIDTH, HEIGHT = 400, 580
BOARD_HEIGHT = 400
LINE_WIDTH = 6
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

# Màu sắc (RGB)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
WIN_LINE_COLOR = (255, 80, 80)

# Khởi tạo màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI (Alpha-Beta)')
screen.fill(BG_COLOR)

# Bàn cờ logic (0: trống, 1: Người - X, 2: AI - O)
board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
anim_progress = [[0.0] * BOARD_COLS for _ in range(BOARD_ROWS)]
game_over = False
win_line = None
clock = pygame.time.Clock()
font = pygame.font.SysFont('segoeui', 24, bold=True)
font_small = pygame.font.SysFont('segoeui', 16)

# Các biến cho AI
ai_bots = {
    'minimax': MinimaxAI(BOARD_ROWS, BOARD_COLS),
    'alpha_beta': AlphaBetaAI(BOARD_ROWS, BOARD_COLS),
    'expectimax': ExpectimaxAI(BOARD_ROWS, BOARD_COLS)
}
ai_algorithm = 'alpha_beta' # 'minimax', 'alpha_beta', hoặc 'expectimax'
last_time_ms = 0
last_nodes = 0

btn_minimax_rect = pygame.Rect(10, 520, 120, 40)
btn_alphabeta_rect = pygame.Rect(140, 520, 120, 40)
btn_expectimax_rect = pygame.Rect(270, 520, 120, 40)
btn_reset_rect = pygame.Rect(WIDTH // 2 - 60, BOARD_HEIGHT + 85, 120, 25)

# --- HÀM VẼ GIAO DIỆN ---
def draw_lines():
    # Vẽ 2 đường ngang
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Đường ngăn cách phần thông tin
    pygame.draw.line(screen, LINE_COLOR, (0, BOARD_HEIGHT), (WIDTH, BOARD_HEIGHT), LINE_WIDTH)
    # Vẽ 2 đường dọc
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, BOARD_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, BOARD_HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                continue
                
            p = anim_progress[row][col]
            cx = int(col * SQUARE_SIZE + SQUARE_SIZE // 2)
            cy = int(row * SQUARE_SIZE + SQUARE_SIZE // 2)
            
            if board[row][col] == 2:  # Vẽ O (AI)
                radius = int(CIRCLE_RADIUS * p)
                if radius > 0:
                    width = min(radius, CIRCLE_WIDTH)
                    pygame.draw.circle(screen, CIRCLE_COLOR, (cx, cy), radius, width)
            elif board[row][col] == 1:  # Vẽ X (Người)
                offset = int((SQUARE_SIZE // 2 - SPACE) * p)
                if offset > 0:
                    pygame.draw.line(screen, CROSS_COLOR, (cx - offset, cy - offset), (cx + offset, cy + offset), CROSS_WIDTH)
                    pygame.draw.line(screen, CROSS_COLOR, (cx - offset, cy + offset), (cx + offset, cy - offset), CROSS_WIDTH)

def draw_status(player_turn):
    # Xóa vùng text
    pygame.draw.rect(screen, BG_COLOR, (0, BOARD_HEIGHT + LINE_WIDTH // 2, WIDTH, HEIGHT - BOARD_HEIGHT))
    if game_over:
        if check_win(1):
            text = "Người chơi (X) THẮNG!"
            color = CROSS_COLOR
        elif check_win(2):
            text = "AI (O) THẮNG!"
            color = CIRCLE_COLOR
        else:
            text = "HÒA!"
            color = (255, 255, 255)
    else:
        if player_turn == 1:
            text = "Lượt của Người (X)"
            color = CROSS_COLOR
        else:
            text = "Lượt của AI (O)"
            color = CIRCLE_COLOR
            
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, BOARD_HEIGHT + 35))
    screen.blit(text_surface, text_rect)
    
    # Vẽ text thuật toán & thống kê
    algo_names = {'minimax': 'Minimax', 'alpha_beta': 'Alpha-Beta', 'expectimax': 'Expectimax'}
    stat_text = f"AI: {algo_names[ai_algorithm]} | Thời gian: {last_time_ms:.1f}ms | Node: {last_nodes}"
    stat_surf = font_small.render(stat_text, True, (220, 220, 220))
    stat_rect = stat_surf.get_rect(center=(WIDTH // 2, BOARD_HEIGHT + 70))
    screen.blit(stat_surf, stat_rect)
    
    # Vẽ nút Reset
    pygame.draw.rect(screen, (200, 80, 80), btn_reset_rect, border_radius=5)
    reset_surf = font_small.render("Chơi lại (R)", True, (255, 255, 255))
    screen.blit(reset_surf, reset_surf.get_rect(center=btn_reset_rect.center))

    # Vẽ nút
    btn_color_minimax = CROSS_COLOR if ai_algorithm == 'minimax' else (120, 190, 180)
    btn_color_alphabeta = CROSS_COLOR if ai_algorithm == 'alpha_beta' else (120, 190, 180)
    btn_color_expectimax = CROSS_COLOR if ai_algorithm == 'expectimax' else (120, 190, 180)

    pygame.draw.rect(screen, btn_color_minimax, btn_minimax_rect, border_radius=8)
    pygame.draw.rect(screen, btn_color_alphabeta, btn_alphabeta_rect, border_radius=8)
    pygame.draw.rect(screen, btn_color_expectimax, btn_expectimax_rect, border_radius=8)

    minimax_surf = font_small.render("Minimax", True, (255, 255, 255))
    alphabeta_surf = font_small.render("Alpha-Beta", True, (255, 255, 255))
    expectimax_surf = font_small.render("Expectimax", True, (255, 255, 255))

    screen.blit(minimax_surf, minimax_surf.get_rect(center=btn_minimax_rect.center))
    screen.blit(alphabeta_surf, alphabeta_surf.get_rect(center=btn_alphabeta_rect.center))
    screen.blit(expectimax_surf, expectimax_surf.get_rect(center=btn_expectimax_rect.center))

# --- LOGIC KIỂM TRA THẮNG THUA ---
def check_win(player):
    # Kiểm tra hàng dọc
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    # Kiểm tra hàng ngang
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Kiểm tra đường chéo
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True
    return False

def get_winning_line(player):
    # Kiểm tra hàng dọc
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
            return ((posX, 0), (posX, BOARD_HEIGHT))
    # Kiểm tra hàng ngang
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
            return ((0, posY), (WIDTH, posY))
    # Kiểm tra đường chéo
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return ((0, 0), (WIDTH, BOARD_HEIGHT))
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return ((0, BOARD_HEIGHT), (WIDTH, 0))
    return None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

# --- TÌM NƯỚC ĐI TỐT NHẤT ---
def find_best_move():
    global last_time_ms, last_nodes
    bot = ai_bots[ai_algorithm]
    bot.nodes_evaluated = 0
    start_time = time.time()
    
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                
                if ai_algorithm == 'alpha_beta':
                    score = bot.minimax_alpha_beta(board, 0, False, -float('inf'), float('inf'))
                elif ai_algorithm == 'expectimax':
                    score = bot.expectimax(board, 0, False)
                else:
                    score = bot.minimax_standard(board, 0, False)
                    
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
                    
    end_time = time.time()
    last_time_ms = (end_time - start_time) * 1000
    last_nodes = bot.nodes_evaluated
    return move

def restart_game():
    global win_line
    win_line = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0
            anim_progress[row][col] = 0.0

# --- VÒNG LẶP GAME CHÍNH ---
player_turn = 1  # 1: Người, 2: AI

while True:
    screen.fill(BG_COLOR)
    draw_lines()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            
            # Xử lý chọn thuật toán và reset qua nút bấm
            if btn_minimax_rect.collidepoint(mouseX, mouseY):
                ai_algorithm = 'minimax'
            elif btn_alphabeta_rect.collidepoint(mouseX, mouseY):
                ai_algorithm = 'alpha_beta'
            elif btn_expectimax_rect.collidepoint(mouseX, mouseY):
                ai_algorithm = 'expectimax'
            elif btn_reset_rect.collidepoint(mouseX, mouseY):
                restart_game()
                player_turn = 1
                game_over = False
            # Click trên bàn cờ
            elif mouseY < BOARD_HEIGHT and not game_over and player_turn == 1:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
    
                if board[clicked_row][clicked_col] == 0:
                    board[clicked_row][clicked_col] = 1
                    anim_progress[clicked_row][clicked_col] = 0.0
                    if check_win(1):
                        game_over = True
                        win_line = get_winning_line(1)
                    player_turn = 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Nhấn phím 'R' để chơi lại
                restart_game()
                player_turn = 1
                game_over = False
            elif event.key == pygame.K_1:
                ai_algorithm = 'minimax'
            elif event.key == pygame.K_2:
                ai_algorithm = 'alpha_beta'
            elif event.key == pygame.K_3:
                ai_algorithm = 'expectimax'

    # Lượt xử lý của AI
    if player_turn == 2 and not game_over:
        row, col = find_best_move()
        if row != -1 and col != -1:
            board[row][col] = 2
            anim_progress[row][col] = 0.0
            if check_win(2):
                game_over = True
                win_line = get_winning_line(2)
            player_turn = 1

    if is_board_full() and not game_over:
        game_over = True

    # Cập nhật animation
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] != 0 and anim_progress[row][col] < 1.0:
                if board[row][col] == 1:
                    anim_progress[row][col] += 0.08  # Tốc độ của X
                elif board[row][col] == 2:
                    anim_progress[row][col] += 0.02  # Tốc độ của O (chậm hơn)
                    
                if anim_progress[row][col] > 1.0:
                    anim_progress[row][col] = 1.0

    draw_figures()
    
    if win_line:
        pygame.draw.line(screen, WIN_LINE_COLOR, win_line[0], win_line[1], 15)
        
    draw_status(player_turn)
    
    pygame.display.update()
    clock.tick(60)