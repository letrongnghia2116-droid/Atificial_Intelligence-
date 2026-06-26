import pygame
import copy

# =========================
# CẤU HÌNH PYGAME
# =========================
WIDTH, HEIGHT = 1000, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CSP Map Coloring - Backtracking + MRV")
font = pygame.font.SysFont("Arial", 22)
clock = pygame.time.Clock()


# =========================
# MÀU SẮC
# =========================
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (220,220,220)

COLORS = {
    -1: GRAY,
    0: (255,0,0),      # Đỏ
    1: (0,0,255),      # Xanh
    2: (255,255,0),    # Vàng
    3: (0,255,0)       # Lá
}

COLOR_NAME = {
    0:"Đỏ",
    1:"Xanh",
    2:"Vàng",
    3:"Lá"
}


# =========================
# BẢN ĐỒ GIẢ 10 PHƯỜNG
# =========================

wards = {
    "P1": [(50,50),(150,50),(150,150),(50,150)],
    "P2": [(150,50),(250,50),(250,150),(150,150)],
    "P3": [(250,50),(350,50),(350,150),(250,150)],
    "P4": [(50,150),(150,150),(150,250),(50,250)],
    "P5": [(150,150),(250,150),(250,250),(150,250)],
    "P6": [(250,150),(350,150),(350,250),(250,250)],
    "P7": [(50,250),(150,250),(150,350),(50,350)],
    "P8": [(150,250),(250,250),(250,350),(150,350)],
    "P9": [(250,250),(350,250),(350,350),(250,350)],
    "P10":[(350,150),(450,150),(450,250),(350,250)]
}


# =========================
# QUAN HỆ KỀ NHAU
# =========================

neighbors = {
"P1":["P2","P4"],
"P2":["P1","P3","P5"],
"P3":["P2","P6"],
"P4":["P1","P5","P7"],
"P5":["P2","P4","P6","P8"],
"P6":["P3","P5","P9","P10"],
"P7":["P4","P8"],
"P8":["P5","P7","P9"],
"P9":["P6","P8"],
"P10":["P6"]
}


# =========================
# CSP
# =========================

steps = []

class CSP:

    def __init__(self):
        self.variables = list(wards.keys())
        self.domains = {
            x:[0,1,2,3]
            for x in self.variables
        }

        self.backtracks = 0


    def valid(self, var, color, assign):

        for n in neighbors[var]:

            if n in assign and assign[n] == color:
                return False

        return True


    def select_variable(self, assign):

        remain = [
            v for v in self.variables
            if v not in assign
        ]

        # MRV
        return min(
            remain,
            key=lambda x: len(self.domains[x])
        )


    def save(self, assign, current):

        steps.append({
            "assign": copy.deepcopy(assign),
            "current": current,
            "backtrack": self.backtracks
        })


    def solve(self, assign):

        if len(assign) == len(self.variables):
            return True


        var = self.select_variable(assign)


        for color in self.domains[var]:

            self.save(assign,var)


            if self.valid(var,color,assign):

                assign[var] = color

                self.save(assign,var)


                if self.solve(assign):
                    return True


                del assign[var]

                self.backtracks += 1

                self.save(assign,var)


        return False



# =========================
# VẼ BẢN ĐỒ
# =========================

def draw_map(assign,current):

    for ward,points in wards.items():

        color_id = assign.get(ward,-1)


        pygame.draw.polygon(
            screen,
            COLORS[color_id],
            points
        )

        border = BLACK


        pygame.draw.polygon(
            screen,
            border,
            points,
            3
        )


        text = font.render(
            ward,
            True,
            BLACK
        )

        x,y = points[0]

        screen.blit(
            text,
            (x+25,y+40)
        )


# =========================
# GIẢI CSP TRƯỚC
# =========================

solver = CSP()
solver.solve({})


# =========================
# CHẠY ANIMATION
# =========================

index = 0
timer = 0
delay = 700


running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running=False


    screen.fill(WHITE)


    if index < len(steps):

        timer += clock.get_time()

        if timer > delay:

            index += 1

            timer = 0


        data = steps[index-1] if index>0 else steps[0]


        draw_map(
            data["assign"],
            data["current"]
        )


        # Thông tin
        x = 550

        txt = [
            f"Buoc: {index}/{len(steps)}",
            f"Dang xet: {data['current']}",
            f"Backtrack: {data['backtrack']}"
        ]


        y=80

        for t in txt:

            img = font.render(
                t,
                True,
                BLACK
            )

            screen.blit(img,(x,y))

            y += 40


    pygame.display.update()


pygame.quit()