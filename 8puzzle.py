import copy
import heapq
import pprint

trivial = [[1, 2, 3],
[4, 5, 6],
[7, 8, 0]]

very_easy = [[1, 2, 3],
[4, 5, 6],
[7, 0, 8]]

easy = [[1, 2, 0],
[4, 5, 3],
[7, 8, 6]]

doable = [[0, 1, 2],
[4, 5, 3],
[7, 8, 6]]

oh_boy = [[8, 7, 1],
[6, 0, 2],
[5, 4, 3]]

impossible = [[8, 1, 2],
[0, 4, 3],
[7, 6, 5]]

eight_goal_state = [[1, 2, 3],
[4, 5, 6],
[7, 8, 0]]


class TreeNode:
    def __init__(self, parent, puzzle_state, cost, heuristic_value=0):
        self.parent = parent
        self.puzzle_state = puzzle_state
        self.cost = cost
        self.heuristic_value = heuristic_value
    
    def __lt__(self, other):
        """Overrides comparison for priority queue. Compares based on cumulative cost."""
        return self.cost+self.heuristic_value < other.cost+self.heuristic_value 
    
    def find_zero(self):
        for i in range(len(self.puzzle_state)):
            for j in range(len(self.puzzle_state[i])):
                if self.puzzle_state[i][j] == 0:
                    return i,j

    def get_depth(self):
        depth = -1
        node = self
        while node:
            depth+=1
            node = node.parent
        return depth

    def move(self, action):
        new_puzzle_state = copy.deepcopy(self.puzzle_state)
        zero_row, zero_column = self.find_zero()
        match action:    
            case 'up':
                if zero_row - 1 >= 0 and zero_row - 1 < len(self.puzzle_state):
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row - 1][zero_column]
                    new_puzzle_state[zero_row - 1][zero_column] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
            case 'down':
                if zero_row + 1 >= 0 and zero_row + 1 < len(self.puzzle_state):
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row + 1][zero_column]
                    new_puzzle_state[zero_row + 1][zero_column] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
            case 'left':
                if zero_column - 1 >= 0 and zero_column - 1 < len(self.puzzle_state):
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row][zero_column-1]
                    new_puzzle_state[zero_row][zero_column-1] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
            case 'right':
                if zero_column + 1 >= 0 and zero_column + 1 < len(self.puzzle_state):
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row][zero_column+1]
                    new_puzzle_state[zero_row][zero_column+1] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
        return new_puzzle_state 

def manhattan_distance(current_state):
    distance = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[row])):
            if current_state[row][col] != 0:
                target_row, target_col = divmod(current_state[row][col] - 1, len(current_state))
                distance += abs(row - target_row) + abs(col - target_col)
    return distance

def misplaced_tiles(current_state):
    misplaced = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[row])):
            if current_state[row][col] != 0 and current_state[row][col] != eight_goal_state[row][col]:
                misplaced += 1
    return misplaced


def select_algorithm(puzzle):
    algorithm = input("Enter 1 - for Uniform Cost Search \nEnter 2 - for A* Misplaced Tile Heuristic\nEnter 3 - for A* Manhattan Heuristic\n")
    match algorithm:
        case "1":
            solution = a_star(puzzle, 0)  
        case "2":
            solution = a_star(puzzle, misplaced_tiles(puzzle))  
        case "3":
            solution = a_star(puzzle, manhattan_distance(puzzle))   
        case _:
            print("Invalid choice") 
    if solution[0]:
        print("Goal State!")
        print(f"Solution depth was: {solution[0].get_depth()}")
        print(f"Number of nodes expanded: {solution[1]}")
        print(f"Max queue size: {solution[2]}")
    else:
        print("No solution exists")

def a_star(puzzle, heuristic):
    queue = []
    heapq.heappush(queue, TreeNode(None, puzzle, 0, heuristic))
    nodes_expanded = 0
    max_queue_size = 0
    visited_nodes = [puzzle]
    
    while queue:
        max_queue_size = max(len(queue), max_queue_size)
        current_node = heapq.heappop(queue)
        if current_node.puzzle_state == eight_goal_state:
            return current_node, nodes_expanded, max_queue_size
        
        nodes_expanded+=1
        
        for move in ["up", "down", "left", "right"]:
            new_puzzle_state = current_node.move(move)
            if new_puzzle_state and new_puzzle_state not in visited_nodes: 
                heapq.heappush(queue, TreeNode(current_node, new_puzzle_state, current_node.cost+1, misplaced_tiles(puzzle)))
                visited_nodes.append(new_puzzle_state) 
    
    return None, nodes_expanded, max_queue_size 
        
    

puzzle_mode = input("Welcome to an 8-Puzzle Solver Type '1' to use a default puzzle, or '2' to create your own.\n")
if puzzle_mode == "1":
    difficulty = input("Enter your difficulty choice - trivial, very_easy, easy, doable, oh_boy, impossible.\n")
    match difficulty:
        case "trivial":
            select_algorithm(trivial)
        case "very_easy":
            select_algorithm(very_easy)
        case "easy":
            select_algorithm(easy)
        case "doable":
            select_algorithm(doable)
        case "oh_boy":
            select_algorithm(oh_boy)
        case "impossible":
            select_algorithm(impossible)
        case _:
            print("Invalid choice")
elif puzzle_mode == "2":
    print("Enter your puzzle, using a zero to represent the blank. Please only enter valid 8-puzzles. Enter the puzzle demilimiting the numbers with a space. Type RETURN only when finished.\n")
    row1 = input("Enter the first row: ").split()
    row2 = input("Enter the second row: ").split()
    row3 = input("Enter the third row: ").split()
    select_algorithm([row1, row2, row3])
else:
    print("Invalid choice")