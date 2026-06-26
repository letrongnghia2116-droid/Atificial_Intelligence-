import copy

class CSP:
    def __init__(self, variables, domains, neighbors, color_names, log_func=print):
        self.variables = variables  
        self.domains = domains      
        self.neighbors = neighbors  
        self.color_names = color_names
        self.log_func = log_func
        self.assignments = 0
        self.backtracks = 0
        self.step_count = 1

    def format_assignment(self, assignment):
        items = [f"{k}={self.color_names[v]}" for k, v in assignment.items()]
        return "{" + ", ".join(items) + "}"

    def is_consistent(self, var, value, assignment):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def select_unassigned_variable(self, assignment, use_mrv=True):
        unassigned = [v for v in self.variables if v not in assignment]
        if use_mrv:
            return min(unassigned, key=lambda var: len(self.domains[var]))
        return unassigned[0]

    def forward_check(self, var, value, assignment):
        removed = []
        for neighbor in self.neighbors[var]:
            if neighbor not in assignment and value in self.domains[neighbor]:
                self.domains[neighbor].remove(value)
                removed.append((neighbor, value))
        return removed

    def restore_domains(self, removed):
        for neighbor, value in removed:
            self.domains[neighbor].append(value)

    def ac3(self):
        queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]
        
        while queue:
            xi, xj = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False  # Inconsistent
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in self.domains[xi][:]:
            if not any(x != y for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def backtrack(self, assignment, use_mrv=True, use_fc=True, use_ac3=True, callback=None):
        if len(assignment) == len(self.variables):
            return assignment

        if len(assignment) == 0 and self.step_count == 1:
            self.log_func(f"Bước {self.step_count}: Assignment={{}}")
            self.step_count += 1

        var = self.select_unassigned_variable(assignment, use_mrv)
        
        step_str = "đầu tiên" if len(assignment) == 0 else "tiếp theo"
        self.log_func(f"Bước {self.step_count}: Chọn biến {step_str}:")
        self.log_func(f"- Chọn {var}")
        self.step_count += 1

        original_domain = copy.deepcopy(self.domains)

        for value in self.domains[var]:
            self.log_func(f"- Chọn giá trị để gán cho {var} bằng cách thử: {var}={self.color_names[value]}")
            if self.is_consistent(var, value, assignment):
                self.log_func("- Kiểm tra ràng buộc: hợp lệ")
                assignment[var] = value
                self.log_func(f"Assignment={self.format_assignment(assignment)}")
                self.assignments += 1
                
                if callback:
                    callback(assignment, var, self.domains)

                removed = []
                if use_fc:
                    removed = self.forward_check(var, value, assignment)
                    
                    self.log_func("- Update lại domain của các biến chưa được gán và có ràng buộc với biến vừa được gán giá trị:")
                    for neighbor in self.neighbors[var]:
                        if neighbor not in assignment:
                            domain_colors = [self.color_names[c] for c in self.domains[neighbor]]
                            self.log_func(f"  + Miền giá trị của {neighbor} = {{{', '.join(domain_colors)}}}")
                    
                    if any(len(self.domains[n]) == 0 for n in self.neighbors[var] if n not in assignment):
                        self.log_func(f"-> PHÁT HIỆN MIỀN GIÁ TRỊ RỖNG do Forward Checking. Quay lui (Backtrack)!")
                        self.restore_domains(removed)
                        del assignment[var]
                        self.backtracks += 1
                        if callback:
                            callback(assignment, var, self.domains)
                        continue

                if use_ac3:
                    ac3_domain_backup = copy.deepcopy(self.domains)
                    if not self.ac3():
                        self.domains = ac3_domain_backup
                        if use_fc:
                            self.restore_domains(removed)
                        del assignment[var]
                        self.backtracks += 1
                        if callback:
                            callback(assignment, var, self.domains)
                        continue

                result = self.backtrack(assignment, use_mrv, use_fc, use_ac3, callback)
                if result is not None:
                    return result

                # Backtrack
                self.log_func(f"-> NHÁNH TÌM KIẾM THẤT BẠI. Quay lui (Backtrack) từ {var}={self.color_names[value]}")
                if use_ac3:
                    self.domains = ac3_domain_backup
                if use_fc:
                    self.restore_domains(removed)
                
                del assignment[var]
                self.backtracks += 1
                if callback:
                    callback(assignment, var, self.domains)
            else:
                self.log_func("- Kiểm tra ràng buộc: không hợp lệ (Trùng màu với hàng xóm)")

        return None
