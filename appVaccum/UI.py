import tkinter as tk
from tkinter import scrolledtext
import copy

# import thuật toán

from BFS_MayHutBui import BFS
from DFS_MayHutBui import DFS
from IDS_MayHutBui import IDS
from UCS_MayHutBui import UCS
# from Random_Restart_Hill_Clibing import RandomRestartHillClimbing
# from Local_Bean_Search import LocalBeamSearch
# from SimulatedAnnealing import SimulatedAnnealing

ALGORITHMS = {
    "BFS": BFS,
    "DFS": DFS,
    "IDS": IDS,
    "UCS": UCS,
}

# giao diện trực quan hóa của robot hút bụi
class ModernVacuumGUI:
    def __init__(self, root, initial_state, start_robot, algorithms):
        self.root = root
        self.root.title("AI Vacuum Cleaner Simulator")
        self.root.geometry("1200x750")
        self.root.configure(bg="#F9FAFB")

        self.algorithms = algorithms
        self.CELL_SIZE = 90
        self.initial_state = copy.deepcopy(initial_state)
        self.start_robot = start_robot
        self.state = copy.deepcopy(initial_state)
        self.robot = start_robot
        self.is_running = False

        self.build_ui()
        self.draw_grid()
        self.log_message("Hệ thống sẵn sàng.", "success")

    def build_ui(self):
        # phần header
        header = tk.Frame(self.root, bg="#1D3557", height=65)
        header.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header, text="AI VACUUM CLEANER SIMULATOR", font=("Segoe UI", 18, "bold"), fg="#F1FAEE",
                 bg="#1D3557").pack(pady=12)

        # phần left panel
        self.left_frame = tk.Frame(self.root, width=220, bg="white", bd=0)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        tk.Label(self.left_frame, text="THUẬT TOÁN", font=("Segoe UI", 13, "bold"), bg="white", fg="#4A4A4A").pack(
            pady=20)

        btn_style = {"font": ("Segoe UI", 11, "bold"), "width": 16, "height": 2, "relief": tk.FLAT, "cursor": "hand2",
                     "fg": "white"}
        colors = ["#2563EB", "#7C3AED", "#059669", "#DC2626", "#D97706", "#4F46E5"]

        for idx, algo_name in enumerate(self.algorithms):
            btn = tk.Button(self.left_frame, text=f"{algo_name}", bg=colors[idx % len(colors)],
                            activebackground="#3B82F6", command=lambda a=algo_name: self.start_algorithm(a),
                            **btn_style)
            btn.pack(pady=10, padx=15)

        self.btn_reset = tk.Button(self.left_frame, text="RESET", bg="#E63946", activebackground="#F87171",
                                   command=self.reset_state, **btn_style)
        self.btn_reset.pack(pady=30, padx=15)

        # Phần chú thích (Legend)
        legend_frame = tk.Frame(self.left_frame, bg="white")
        legend_frame.pack(side=tk.BOTTOM, pady=20, fill=tk.X)
        tk.Label(legend_frame, text="KÝ HIỆU", font=("Segoe UI", 11, "bold"), bg="white", fg="#4A4A4A").pack(anchor="w",
                                                                                                             padx=15,
                                                                                                             pady=5)

        def draw_obstacle(c):
            c.create_rectangle(2, 2, 18, 18, fill="#4A4A4A", outline="#2C3E50")

        def draw_dirt(c):
            c.create_oval(4, 4, 16, 16, fill="#8B4513", outline="")

        def draw_robot(c):
            c.create_oval(2, 2, 18, 18, fill="#2A9D8F", outline="#1D3557")

        legend_items = [(draw_obstacle, "Vật cản"), (draw_dirt, "Bụi bẩn"), (draw_robot, "Robot")]

        for draw_func, text in legend_items:
            item_frame = tk.Frame(legend_frame, bg="white")
            item_frame.pack(anchor="w", padx=15, pady=4)
            cv = tk.Canvas(item_frame, width=20, height=20, bg="white", highlightthickness=0)
            cv.pack(side=tk.LEFT)
            draw_func(cv)
            tk.Label(item_frame, text=text, bg="white", font=("Segoe UI", 10), fg="#4A4A4A").pack(side=tk.LEFT, padx=8)

        # phần right panel (Nhật ký)
        self.right_frame = tk.Frame(self.root, width=320, bg="white", bd=0)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        tk.Label(self.right_frame, text="NHẬT KÝ", font=("Segoe UI", 12, "bold"), bg="white", fg="#4A4A4A").pack(
            pady=10)

        self.txt_log = scrolledtext.ScrolledText(self.right_frame, width=32, state=tk.DISABLED, font=("Consolas", 10),
                                                 bg="#F8F9FA", relief=tk.FLAT, bd=1)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.txt_log.tag_config("info", foreground="#616161")
        self.txt_log.tag_config("success", foreground="#059669")
        self.txt_log.tag_config("error", foreground="#DC2626")
        self.txt_log.tag_config("step", foreground="#2563EB")

        # phần center hiển thị giao diện thực thi của robot
        self.center_frame = tk.Frame(self.root, bg="#F9FAFB")
        self.center_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=10)
        self.canvas = tk.Canvas(self.center_frame, bg="#F9FAFB", highlightthickness=0)
        self.canvas.pack(expand=True)

        bottom = tk.Frame(self.root, bg="#E5E7EB")
        bottom.pack(side=tk.BOTTOM, fill=tk.X)

        lbl_title = tk.Label(bottom, text="Lời giải: ", font=("Segoe UI", 11, "bold"), bg="#E5E7EB", fg="#4A4A4A")
        lbl_title.pack(side=tk.LEFT, anchor="nw", padx=(15, 5), pady=12)

        self.lbl_step = tk.Label(bottom, text="Bước: 0", font=("Segoe UI", 11, "bold"), bg="#E5E7EB", fg="#1D3557")
        self.lbl_step.pack(side=tk.RIGHT, anchor="ne", padx=20, pady=12)

        self.txt_solution = tk.Text(bottom, font=("Consolas", 11, "bold"), bg="#E5E7EB", fg="#059669",
                                    relief=tk.FLAT, height=3, wrap=tk.WORD, highlightthickness=0)
        self.txt_solution.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=12)

        self.set_solution_text("Chưa có", is_error=True)

    def draw_grid(self):
        self.canvas.delete("all")
        rows, cols = len(self.state), len(self.state[0])
        self.canvas.config(width=cols * self.CELL_SIZE, height=rows * self.CELL_SIZE)
        rx, ry = self.robot

        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * self.CELL_SIZE, r * self.CELL_SIZE
                x2, y2 = x1 + self.CELL_SIZE, y1 + self.CELL_SIZE

                color = "#FFFFFF" if (r + c) % 2 == 0 else "#F3F4F6"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#D1D5DB")

                if self.state[r][c] == -1:
                    self.canvas.create_rectangle(x1 + 8, y1 + 8, x2 - 8, y2 - 8, fill="#4A4A4A", outline="#2C3E50",
                                                 width=1)
                    self.canvas.create_rectangle(x1 + 15, y1 + 15, x2 - 15, y2 - 15, fill="#5A5A5A", outline="")

                elif self.state[r][c] == 1:
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    for i in range(5):
                        self.canvas.create_oval(cx - 10 + i * 2, cy - 8 + i, cx + 8 - i, cy + 10 - i * 2,
                                                fill="#8B4513", outline="")

        x, y = ry * self.CELL_SIZE, rx * self.CELL_SIZE
        self.canvas.create_oval(x + 10, y + 10, x + self.CELL_SIZE - 10, y + self.CELL_SIZE - 10, fill="#2A9D8F",
                                outline="#1D3557", width=2)
        self.canvas.create_oval(x + 25, y + 25, x + self.CELL_SIZE - 25, y + self.CELL_SIZE - 25, fill="#A8DADC",
                                outline="#1D3557", width=1)
        import time
        angle = int(time.time() * 2) % 2
        self.canvas.create_arc(x + 15, y + 15, x + self.CELL_SIZE - 15, y + self.CELL_SIZE - 15, start=angle * 90,
                               extent=120, outline="#1D3557", width=1.5, style=tk.ARC)

    # Hàm bổ trợ để cập nhật nội dung Text của Lời giải một cách an toàn
    def set_solution_text(self, text, is_error=False, is_searching=False):
        self.txt_solution.config(state=tk.NORMAL)
        self.txt_solution.delete(1.0, tk.END)
        self.txt_solution.insert(tk.END, text)

        if is_error:
            self.txt_solution.config(fg="#DC2626")
        elif is_searching:
            self.txt_solution.config(fg="#D97706")
        else:
            self.txt_solution.config(fg="#059669")

        self.txt_solution.config(state=tk.DISABLED)

    def log_message(self, message, tag="info"):
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, f"{message}\n", tag)
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def reset_state(self):
        if self.is_running: return
        self.state = copy.deepcopy(self.initial_state)
        self.robot = self.start_robot
        self.draw_grid()
        self.set_solution_text("Chưa có", is_error=True)
        self.lbl_step.config(text="Bước: 0")

        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.delete(1.0, tk.END)
        self.txt_log.config(state=tk.DISABLED)
        self.log_message("Đã reset bản đồ.", "success")

    def get_translated_path(self, path):
        trans = {"up": "up", "down": "down", "left": "left", "right": "right"}
        return [trans.get(action, action) for action in path]

    def start_algorithm(self, algo_name):
        if self.is_running: return
        self.reset_state()
        self.is_running = True
        self.log_message(f"Đang chạy {algo_name}...", "info")
        self.set_solution_text("Đang tìm kiếm...", is_searching=True)

        algorithm = self.algorithms[algo_name]
        path = algorithm(self.state, self.robot)

        if path:
            translated_path = self.get_translated_path(path)
            solution_text = " -> ".join(translated_path)
            self.set_solution_text(solution_text, is_error=False)
            self.log_message(f"Tìm thấy lời giải ({len(path)} bước)", "success")
            self.animate_path(path, 0)
        else:
            self.set_solution_text("Vô nghiệm", is_error=True)
            self.log_message("Không tìm thấy lời giải", "error")
            self.is_running = False

    def animate_path(self, path, step_index):
        if step_index < len(path):
            action = path[step_index]
            self.move_robot(action)
            self.draw_grid()
            self.lbl_step.config(text=f"Bước: {step_index + 1}")

            trans = {"up": "up", "down": "down", "left": "left", "right": "right"}
            vn_action = trans.get(action, action)
            self.log_message(f"[{step_index + 1}] Di chuyển: {vn_action}", "step")

            self.root.after(350, self.animate_path, path, step_index + 1)
        else:
            self.log_message("Hoàn thành!", "success")
            self.is_running = False

    def move_robot(self, action):
        x, y = self.robot
        if action == "up":
            nx, ny = x - 1, y
        elif action == "down":
            nx, ny = x + 1, y
        elif action == "left":
            nx, ny = x, y - 1
        elif action == "right":
            nx, ny = x, y + 1

        self.state[nx][ny] = 0
        self.robot = (nx, ny)


if __name__ == "__main__":
    map_data = [
        [0, 1, 1, 0, 0],
        [1, -1, 1, -1, 1],
        [1, 1, 1, 0, -1]
    ]
    start_robot = (0, 0)
    root = tk.Tk()
    app = ModernVacuumGUI(root, map_data, start_robot, ALGORITHMS)
    root.mainloop()