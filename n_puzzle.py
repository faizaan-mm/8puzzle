import copy
import datetime
import heapq

trivial = [[1, 2, 3],
[4, 5, 6],
[7, 8, 0]]

very_easy = [[1, 2, 3],
[4, 5, 6],
[0, 7, 8]]

easy = [[1, 2, 3],
[5, 0, 6],
[4, 7, 8]]

doable = [[1, 3, 6],
[5, 0, 2],
[4, 7, 8]]

still_doable = [[1, 6, 7],
[5, 0, 3],
[4, 8, 2]]

hard = [[7, 1, 2],
[4, 8, 5],
[6, 3, 0]]

oh_boy = [[0, 7, 2],
[4, 6, 1],
[3, 5, 8]]

impossible = [[8, 1, 2],
[0, 4, 3],
[7, 6, 5]]

eight_goal_state = [[1, 2, 3],
[4, 5, 6],
[7, 8, 0]]


class TreeNode:
    def __init__(self, parent, puzzle_state, cost, heuristic=None):
        """
        parent - is the previous state of the node
        puzzle_state - the position of tiles on the board
        cost - uninformed cost of the node  
        heuristic - string of the algorithm to use to initialise the heuristic cost of the algorithm
        """
        self.parent = parent # to keep track to the tree 
        self.puzzle_state = puzzle_state # the position of tiles on the board
        self.cost = cost # uninformed cost of the node  
        self.heuristic_value = 0 # heauristic cost for the algorithm on the node
        if heuristic == "manhattan_distance":
            self.heuristic_value = manhattan_distance(puzzle_state)
        if heuristic == "misplaced_tiles":
            self.heuristic_value = misplaced_tiles(puzzle_state)
    
    def __lt__(self, other):
        # Overrides comparison for priority queue. Compares based on the heuristic cost. This is due to the implementation of heapq in python that checks the element.__lt__ to add it in the right place in queue
        return  (self.parent.cost - self.parent.heuristic_value + 1 + self.heuristic_value) <  (other.parent.cost - other.parent.heuristic_value + 1 + other.heuristic_value)
    
    def find_zero(self):
        """
        To find the position of the empty tile represented by 0. A 2D array traversal until we find the elemnt 0, returns the indices of the 0 element
        """
        for i in range(len(self.puzzle_state)):
            for j in range(len(self.puzzle_state[i])):
                if self.puzzle_state[i][j] == 0:
                    return i,j

    def get_depth(self):
        """
        The function traverses up the tree until no parent is found i.e the root node is found. This tells us the depth of the tree from the solution node. returns an integer that is the depth of the tree.
        """
        depth = -1
        node = self
        while node:
            depth+=1
            node = node.parent
        return depth

    def move(self, action):
        """
        action - takes in a string that tells it where to move the empty tile
        The function returns a new board that consists of the position of the tile after the move if the move is within the board else returns None
        """
        new_puzzle_state = copy.deepcopy(self.puzzle_state) # to copy the contents to a new board so the original board is untouched and can be used for generating the boards for other moves on the same parent 
        zero_row, zero_column = self.find_zero() # get the position of the empty tile
        match action:    
            case 'up':
                if zero_row - 1 >= 0 and zero_row - 1 < len(self.puzzle_state): # swap the empty tile with the tile on top if it is within the boundary of the board
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row - 1][zero_column]
                    new_puzzle_state[zero_row - 1][zero_column] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
            case 'down':
                if zero_row + 1 >= 0 and zero_row + 1 < len(self.puzzle_state): # swap the empty tile with the tile on bottom if it is within the boundary of the board
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row + 1][zero_column]
                    new_puzzle_state[zero_row + 1][zero_column] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
            case 'left':
                if zero_column - 1 >= 0 and zero_column - 1 < len(self.puzzle_state): # swap the empty tile with the tile on the left if it is within the boundary of the board
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row][zero_column-1]
                    new_puzzle_state[zero_row][zero_column-1] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
            case 'right':
                if zero_column + 1 >= 0 and zero_column + 1 < len(self.puzzle_state): # swap the empty tile with the tile on the right if it is within the boundary of the board
                    new_puzzle_state[zero_row][zero_column] = self.puzzle_state[zero_row][zero_column+1]
                    new_puzzle_state[zero_row][zero_column+1] = self.puzzle_state[zero_row][zero_column]
                else:
                    return
        return new_puzzle_state 

def manhattan_distance(current_state):
    """
    Calculates the manhattan distance of the current board from the goal state. Calculates the absolute difference of all tiles with the goal tiles and returns a sum of differences.
    """
    distance = 0
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] != 0:
                target_row, target_col = (current_state[i][j]-1)//len(current_state), (current_state[i][j]-1)%len(current_state[i])
                distance += abs(i - target_row) + abs(j - target_col)
    return distance

def misplaced_tiles(current_state):
    """
    Returns the number of tiles that are misoplaced when compared to the goal state
    """
    misplaced = 0
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] != 0 and current_state[i][j] != eight_goal_state[i][j]:
                misplaced += 1
    return misplaced

def select_algorithm(puzzle):
    """
    Utility funtion to pick between the 3 different choices of algorithms to solve the puzzle
    """
    algorithm = input("Enter 1 - for Uniform Cost Search \nEnter 2 - for A* Misplaced Tile Heuristic\nEnter 3 - for A* Manhattan Heuristic\n")
    start_time = datetime.datetime.now()
    # Uses the algorithm based on the user's input
    match algorithm:
        case "1":
            solution = a_star(puzzle)  
        case "2":
            solution = a_star(puzzle, "misplaced_tiles")  
        case "3":
            solution = a_star(puzzle, "manhattan_distance")   
        case _:
            print("Invalid choice") 
    # If the a_star method returns a solution tuple, and the first element contains a TreeNode object, we know that there is a solution and hence display the details of the solution
    if solution[0]:
        print("Goal State!")
        print(f"Solution depth was: {solution[0].get_depth()}")
        print(f"Number of nodes expanded: {solution[1]}")
        print(f"Max queue size: {solution[2]}")
    # If the first element of the solutio ntuple is None, we know that there is no solution to the tuple
    else:
        print("No solution exists")
    end_time = datetime.datetime.now()
    print(f"Execution Time: {(end_time-start_time).microseconds}")

def a_star(puzzle, heuristic=None):
    """
    The main function to implement the A* algorithm. 
    puzzle - the matrix representing the current state of the board
    heuristic - string that tells that algorithm what heuristic to use
    """
    # empty frontier queue
    queue = []
    initial_node = TreeNode(None, puzzle, 0, heuristic)
    # push the initial state to the queue. The first element is the cost of the node, second is the node itself and the last is the depth. It is pushed in this way as the min queue uses this to queue up the nodes in the increasing order of cost
    heapq.heappush(queue, (0+initial_node.heuristic_value, initial_node, 0))
    nodes_expanded = 0
    max_queue_size = 0
    # to keep track of the states that were already visited, so we don't expand already expanded nodes of the same cost
    visited_nodes = set()
    
    while queue:
        # update the maximum size of the queue 
        max_queue_size = max(len(queue), max_queue_size)
        # get the first element in queue
        current_cost, current_node, current_depth = heapq.heappop(queue)
        print(f"The best state to expand with a g(n) = {current_node.cost} and h(n) = {current_node.heuristic_value} is…")
        for row in current_node.puzzle_state:
            print(row)
        
        # Keep track of the visited nodes. the str(current_node.puzzle_state) is used becasue the matrix cannot be hashed, but a string can be
        if str(current_node.puzzle_state) not in visited_nodes:
            visited_nodes.add(str(current_node.puzzle_state))
        
        # if the current state of the board is the goal state, stop the algorithm and return the current state, the number of nodes expanded and the maximum size of the frontier queue
        if current_node.puzzle_state == eight_goal_state:
            return current_node, nodes_expanded, max_queue_size
        
        # update the number of nodes expanded
        nodes_expanded+=1
        
        # generate all possible states from a given state by moving the empty tile in every direction
        for move in ["up", "down", "left", "right"]:
            new_puzzle_state = current_node.move(move)
            # if a new state of the board is found , add it to the queue and updated the tracker for visited nodes
            if new_puzzle_state and str(new_puzzle_state) not in visited_nodes: 
                node = TreeNode(current_node, new_puzzle_state, current_node.cost+1, heuristic)
                # push the new state to the queue, the first element is the heuristic calculated by the cost until that node + the cost to go to this node from the current and the value of the heuristic
                heapq.heappush(queue, ((current_cost - current_node.heuristic_value + 1 + node.heuristic_value), node, current_depth+1))
    
    # If no solution is found after emptying the entire queue, return None to signify that there is no solution
    return None, nodes_expanded, max_queue_size 
        
    

puzzle_mode = input("Welcome to an 8-Puzzle Solver Type '1' to use a default puzzle, or '2' to create your own.\n")
# Uses the predefined puzzles as initiaised above and call the search
if puzzle_mode == "1":
    difficulty = input("Enter your difficulty choice - trivial, very_easy, easy, doable, still_doable, hard, oh_boy, impossible.\n")
    match difficulty:
        case "trivial":
            select_algorithm(trivial)
        case "very_easy":
            select_algorithm(very_easy)
        case "easy":
            select_algorithm(easy)
        case "doable":
            select_algorithm(doable)
        case "still_doable":
            select_algorithm(still_doable)
        case "hard":
            select_algorithm(hard)
        case "oh_boy":
            select_algorithm(oh_boy)
        case "impossible":
            select_algorithm(impossible)
        case _:
            print("Invalid choice")
# allows the user to enter an 8 puzzle of their own
elif puzzle_mode == "2":
    print("Enter your puzzle, using a zero to represent the blank. Please only enter valid 8-puzzles. Enter the puzzle demilimiting the numbers with a space. Type RETURN only when finished.\n")
    row1 = input("Enter the row 1: ").split()
    row2 = input("Enter the row 2: ").split()
    row3 = input("Enter the row 3: ").split()
    # check if the puzzzle is a valid 8 puzzle
    if set(row1+row2+row3) != ['0', '1', '2' ,'3' ,'4' , '5' ,'6' ,'7' , '8', '9']:
        print("Invalid board configuration!\nEnter your puzzle, using a zero to represent the blank. Please only enter valid 8-puzzles.")
        exit(0)
    select_algorithm([[int(num) for num in row1], [int(num) for num in row2], [int(num) for num in row3]])
else:
    print("Invalid choice")