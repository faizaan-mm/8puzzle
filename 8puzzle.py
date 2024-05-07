import heapq

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
    def __init__(self, parent, current_state, cost, heuristic_value=0):
        self.parent = parent
        self.current_state = current_state
        self.cost = cost
        self.heuristic_value = heuristic_value


def select_algorithm(puzzle):
    algorithm = input("Enter 1 - for Uniform Cost Search \nEnter 2 - for A* Misplaced Tile Heuristic\nEnter 3 - for A* Manhattan Heuristic\n")
    match algorithm:
        case "1":
            a_star(puzzle, 0)  
        case "2":
            a_star(puzzle, 2)  
        case "3":
            a_star(puzzle, 3)  
        case _:
            print("Invalid choice") 

def a_star(puzzle, heuristic):
    pass

puzzle_mode = input("Welcome to an 8-Puzzle Solver Type '1' to use a default puzzle, or '2' to create your own.\n")
if puzzle_mode == "1":
    difficulty = input("Enter your difficulty choice - trivial, very_easy, easy, doable, oh_boy, impossible.1\n")
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