import random

class CSP:
    def __init__(self, variables, domains, neighbors, color_names, log_func=print):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.color_names = color_names
        self.log_func = log_func
        self.assignments = 0
        self.backtracks = 0 # Sử dụng như số lần thay đổi màu (iterations)
        self.step_count = 1

    def format_assignment(self, assignment):
        items = [f"{k}={self.color_names[v]}" for k, v in assignment.items()]
        return "{" + ", ".join(items) + "}"

    def conflicts(self, var, val, assignment):
        count = 0
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == val:
                count += 1
        return count

    def min_conflicts(self, initial_assignment, max_steps=1000, callback=None):
        assignment = {}
        # Khởi tạo ngẫu nhiên
        for var in self.variables:
            assignment[var] = random.choice(self.domains[var])
            
        self.log_func(f"Bước 0: Khởi tạo ngẫu nhiên")
        self.log_func(f"Assignment={self.format_assignment(assignment)}")
        if callback:
            callback(assignment, None, self.domains)
            
        for i in range(max_steps):
            self.step_count = i + 1
            # Tìm các biến đang có xung đột
            conflicted_vars = []
            for var in self.variables:
                if self.conflicts(var, assignment[var], assignment) > 0:
                    conflicted_vars.append(var)
                    
            if not conflicted_vars:
                self.log_func(f"Tìm thấy giải pháp sau {i} bước!")
                return assignment
                
            var = random.choice(conflicted_vars)
            self.log_func(f"Bước {self.step_count}: Chọn ngẫu nhiên biến có xung đột: {var}")
            
            # Tìm giá trị gây ra ít xung đột nhất
            min_count = float('inf')
            best_vals = []
            for val in self.domains[var]:
                c = self.conflicts(var, val, assignment)
                if c < min_count:
                    min_count = c
                    best_vals = [val]
                elif c == min_count:
                    best_vals.append(val)
                    
            val = random.choice(best_vals)
            self.log_func(f"- Chọn màu min-conflicts cho {var}: {self.color_names[val]} (số xung đột: {min_count})")
            
            if assignment[var] != val:
                assignment[var] = val
                self.assignments += 1
                self.backtracks += 1 # Tính số lần thay đổi
                
            if callback:
                callback(assignment, var, self.domains)
                
        self.log_func("Không tìm thấy giải pháp trong số bước tối đa.")
        return None
