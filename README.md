# Lê Trọng Nghĩa 
# MSSV: 24110286


# Table of Contents
- Algorithms Implemented
- Algorithm Demonstrations
  - Uninformed Search
  - Informed Search
  - Local Search
  - Complex Environment Search
  - Constraint Satisfaction Problems
  - Adversarial Search

---

# Algorithms Implemented

| Category | Algorithms |
|----------|-----------|
| Uninformed Search | BFS, DFS, UCS, IDS |
| Informed Search | Greedy, A*, IDA A* |
| Local Search | Hill Climbing, Local BFS, Simulated Annealing |
| CSP | Backtracking, Forward Checking, AC- 3, Min-conflicts|
| Adversarial Search | Minimax, Alpha-Beta, Expectimax |
| Probabilistic Search | Belief State Search, Partially observable |

# Algorithm Demonstrations


## Uninformed Search

Uninformed Search (hay còn gọi là Blind Search) là nhóm thuật toán tìm kiếm không sử dụng bất kỳ thông tin nào về vị trí của đích hoặc khoảng cách đến đích trong quá trình tìm kiếm.

## Breadth First Search (BFS)

<img width="963" height="697" alt="BFS" src="https://github.com/user-attachments/assets/2f4d3c75-f904-413f-af7d-230788584e86" />

## Depth First Search (DFS)

<img width="960" height="697" alt="DFS" src="https://github.com/user-attachments/assets/8db28cd5-c13b-4fc9-be60-b3e8cba58b1d" />

## Uniform Cost Search (UCS)

<img width="961" height="695" alt="IDS" src="https://github.com/user-attachments/assets/f8c7c2a4-b825-4356-93d6-43104d0be263" />

## Iterative Deepening Search (IDS)

<img width="962" height="697" alt="UCS" src="https://github.com/user-attachments/assets/1d2104ed-81e9-456a-a9d1-7af8b7f0ec88" />

## Informed Search

Informed Search (hay còn gọi là Heuristic Search) là nhóm thuật toán tìm kiếm sử dụng thêm thông tin về mục tiêu hoặc hàm heuristic để định hướng quá trình tìm kiếm.

## Greedy Best First Search

<img width="1200" height="776" alt="greedy" src="https://github.com/user-attachments/assets/4fe08a96-e9f8-420c-9f3b-0828abf4a6ce" />

## A* Search

<img width="1197" height="778" alt="Astar" src="https://github.com/user-attachments/assets/444bc0c7-77a0-4d45-8041-cce83800a1a7" />

## IDA*

<img width="1199" height="778" alt="IDAStar" src="https://github.com/user-attachments/assets/f92d72b0-d976-4741-b3c5-b8b13fa5ee18" />

## Local Search

Local Search là nhóm thuật toán tìm kiếm chỉ quan tâm đến trạng thái hiện tại và các trạng thái lân cận của nó, thay vì xây dựng và lưu trữ toàn bộ cây tìm kiếm như BFS hay A*. Thuật toán sẽ liên tục di chuyển từ trạng thái hiện tại sang trạng thái "tốt hơn" cho đến khi tìm được lời giải hoặc không thể cải thiện thêm.

## Hill Climbing

### Leo đồi Đơn giản 

<img width="1199" height="778" alt="LeoDoiDonGian" src="https://github.com/user-attachments/assets/13d7232d-4935-4358-814e-39aea8bc9373" />

### Leo đồi dốc nhất 

<img width="1200" height="779" alt="LeoDoiDocNhat" src="https://github.com/user-attachments/assets/135a838a-8362-4212-854d-897c90ffaebf" />

### leo đồi ngẫu nhiên

<img width="1199" height="774" alt="LeoDoiNgauNhien" src="https://github.com/user-attachments/assets/d079b22b-fd0c-429f-aed5-8c198d8245c2" />

### Leo đồi ngẫu nhiên có lựa chọn 

<img width="1199" height="782" alt="LeoDoiNgauNhienCoLuaChon" src="https://github.com/user-attachments/assets/9077af07-f2e6-41c6-a21e-3e10174ff411" />

## Local BFS

<img width="1200" height="776" alt="LocalBeamSearch" src="https://github.com/user-attachments/assets/17c0ee5d-27ab-4d37-bd60-97cf8a7786c1" />

## Simulated Annealing

<img width="1196" height="778" alt="LuyênThep" src="https://github.com/user-attachments/assets/33ab2aef-db53-4eb7-b7f2-dcad8c1ad6dd" />

## Complex Environment Search
Complex Environment Search là nhóm các thuật toán tìm kiếm được thiết kế để hoạt động trong những môi trường mà việc tìm đường trở nên khó khăn hơn do có các yếu tố như:
- Thông tin không đầy đủ (Partially Observable Environment).
- Môi trường thay đổi theo thời gian (Dynamic Environment).
- Có nhiều tác nhân tương tác (Multi-Agent Environment).
- Có yếu tố không chắc chắn hoặc ngẫu nhiên (Uncertain Environment).
## Belief state search 

<img width="1202" height="809" alt="belief_state " src="https://github.com/user-attachments/assets/fe869036-5436-4da0-905b-d6aee08a265e" />

## Partially observable 

<img width="1101" height="807" alt="partially" src="https://github.com/user-attachments/assets/6bfb5da7-f56e-4c17-ba6b-6f8bb2fefcca" />

## Constraint Satisfaction Problems (CSP)

Constraint Satisfaction Problem (CSP) là lớp bài toán mà mục tiêu là gán giá trị cho các biến sao cho tất cả các ràng buộc đều được thỏa mãn.
Một bài toán CSP luôn gồm 3 thành phần:
- Variables (Biến): Các đối tượng cần gán giá trị.
- Domains (Miền giá trị): Tập giá trị mà mỗi biến có thể nhận.
- Constraints (Ràng buộc): Các điều kiện mà các biến phải thỏa mãn

## Backtracking

<img width="971" height="800" alt="Bactracking " src="https://github.com/user-attachments/assets/11ab039e-6da0-4957-86ec-64f38e9d2311" />

## Forward Checking

<img width="979" height="805" alt="foward checking " src="https://github.com/user-attachments/assets/852efac7-e502-4a42-aeb3-7f90c5f52dbc" />

## Arc Consistency (AC-3)

<img width="935" height="692" alt="VeBanDo" src="https://github.com/user-attachments/assets/a4872537-8060-48c0-b170-92ec528c6758" />

## min conflicts 

<img width="949" height="707" alt="VeBanDo" src="https://github.com/user-attachments/assets/65f69e9b-fd61-4733-be6c-6e0ee67a8ec4" />

## ⚔️ Adversarial Search

Adversarial Search là nhóm thuật toán tìm kiếm được sử dụng trong các môi trường có nhiều tác nhân với mục tiêu đối lập nhau, trong đó một tác nhân cố gắng tối đa hóa lợi ích của mình trong khi tác nhân còn lại cố gắng làm điều ngược lại.

## Minimax

<img width="401" height="608" alt="Minnimax " src="https://github.com/user-attachments/assets/2d2cdf78-5dd8-4ea2-87cf-0ececc045327" />

## Alpha-Beta Pruning

<img width="396" height="606" alt="alpha_beta" src="https://github.com/user-attachments/assets/dd452c7a-e93c-4327-97eb-1f06227bdc9d" />

## Expectimax

<img width="398" height="609" alt="expactimax" src="https://github.com/user-attachments/assets/800bbbe0-3621-46c5-be2b-ec73263ad98c" />


# 👨‍💻 Author

**Le Trong Nghia**

Artificial Intelligence Course Project
