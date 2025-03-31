import pygame
import heapq
import math

# Initialize Pygame
pygame.init()


# Constants
WIDTH = 40  # Size of each grid cell (in pixels)
HEIGHT = 40

# Color codes
GRID_COLOR = (255, 255, 255)        #WHITE
ROAD_COLOR = (0, 255, 0)            #GREEN
BARRIER_COLOR = (0, 0, 0)           #BLACK
START_COLOR = (0, 0, 255)           #BLUE
END_COLOR = (255, 0, 0)             #RED
PATH_COLOR = (255, 255, 0)          #YELLOW
TEXT_COLOR = (0, 0, 0)  # Color of the text inside the grid cells
ALTERNATE_PATH_COLOR = (0, 255, 255)  # Color for alternate paths



# A* Algorithm
class Node:
    def __init__(self, x, y, g, h, parent=None):
        self.x = x
        self.y = y
        self.g = g  # Cost from start to this node
        self.h = h  # Heuristic to goal
        self.f = g + h  # Total cost
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, end, other_areas):
    open_list = []
    closed_list = set()
    
    start_node = Node(start[0], start[1], 0, heuristic(start, end))
    #print("This is start node class return value: ", start_node)
    heapq.heappush(open_list, start_node)
    
    while open_list:
        current_node = heapq.heappop(open_list)
        
        if (current_node.x, current_node.y) == end:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]
        
        closed_list.add((current_node.x, current_node.y))
        
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way movement (up, down, left, right)
        for dx, dy in neighbors:
            nx, ny = current_node.x + dx, current_node.y + dy
            
            # # Ensure we're within bounds, and the cell is traversable (0, 1, 2, or 3)
            # if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 'x' and (nx, ny) not in closed_list:
            #     g_cost = current_node.g + 1
            #     h_cost = heuristic((nx, ny), end)
            #     neighbor_node = Node(nx, ny, g_cost, h_cost, current_node)
            #     heapq.heappush(open_list, neighbor_node)

            # Writing this for simplicity: Check if the new position is inside the grid's row range
            if nx >= 0 and nx < len(grid):
                # Check if the new position is inside the grid's column range
                if ny >= 0 and ny < len(grid[0]):
                    # Check if the cell is not blocked by a wall ('x') and also not passing through other functional areas
                    if grid[nx][ny] != 'x' and (nx, ny) not in other_areas:
                        #print("hello")
                        # Check if the cell hasn't been visited already
                        if (nx, ny) not in closed_list:
                            # If all conditions are satisfied, proceed
                            g_cost = current_node.g + 1
                            h_cost = heuristic((nx, ny), end)
                            neighbor_node = Node(nx, ny, g_cost, h_cost, current_node)
                            heapq.heappush(open_list, neighbor_node)
                
    return None  # No path found


# Function to create the grid, returns cell 
def create_grid(input_array):
    # for row in input_array:
    #     for cell in row:
    #         cell = [cell]
    #         print(cell)
    return [[cell for cell in row] for row in input_array]

# Function to get all the positions of a certain value in the grid
def get_positions(grid, value):
    return [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] == value]

def get_other_functional_areas(grid, start_area, end_area):
    # for x in range(len(grid)):
    #     for y in range(len(grid[0])):
    #         if grid[x][y] != 'x' and grid[x][y] != 0 and grid[x][y] != start_area and grid[x][y] != end_area:
    #             return [(x, y)]
    return [(x, y) for x in range(len(grid)) for y in range(len(grid[0])) if grid[x][y] != 'x' if grid[x][y] != 0 if grid[x][y] != start_area if grid[x][y] != end_area]

# Function to perform flood fill and return connected area for 1, 2, or 3
def flood_fill(grid, start_x, start_y, value):
    area = []
    stack = [(start_x, start_y)]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if grid[x][y] == value:
            area.append((x, y))
            # Add adjacent cells to the stack
            if x > 0: stack.append((x-1, y))
            if x < len(grid)-1: stack.append((x+1, y))
            if y > 0: stack.append((x, y-1))
            if y < len(grid[0])-1: stack.append((x, y+1))
    
    return area

# Function to draw lines to distinguish grids and print values
def draw_grid(screen, grid, paths=None, highlight_path=None):
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            color = ROAD_COLOR
            if grid[y][x] == 'x':
                color = BARRIER_COLOR
            elif type(grid[y][x]) == int and grid[y][x] != 0:
                color = START_COLOR
            # elif grid[y][x] == 1:
            #     color = START_COLOR
            # elif grid[y][x] == 2:
            #     color = END_COLOR
            # elif grid[y][x] == 3:
            #     color = (255, 255, 255)  # Different color for area 3

            # Draw the grid cell
            pygame.draw.rect(screen, color, (x * WIDTH, y * HEIGHT, WIDTH, HEIGHT))

            # Draw the grid lines
            pygame.draw.rect(screen, GRID_COLOR, (x * WIDTH, y * HEIGHT, WIDTH, HEIGHT), 2)

            # Display the value inside each cell
            font = pygame.font.SysFont("Arial", 20)
            value_text = font.render(str(grid[y][x]), True, TEXT_COLOR)
            screen.blit(value_text, (x * WIDTH + WIDTH // 4, y * HEIGHT + HEIGHT // 4))

    # Draw all paths in alternate colors
    # if paths:
    #     for path in paths:
    #         for (x, y) in path:
    #             pygame.draw.rect(screen, ALTERNATE_PATH_COLOR, (x * WIDTH, y * HEIGHT, WIDTH, HEIGHT))
    
    # Draw the fastest path in a distinct color
    if highlight_path:
        for (y, x) in highlight_path:
            if grid[y][x] != 'x':
                pygame.draw.rect(screen, PATH_COLOR, (x * WIDTH, y * HEIGHT, WIDTH, HEIGHT))
            #print("take this x and y this is my path ", x, y)

    pygame.display.update()



def main(input_array, start_area, end_area):
    grid = create_grid(input_array)
    #print("this is what grid looks like", grid)


    # Get all positions for the start and end areas
    start_positions = get_positions(grid, start_area)
    end_positions = get_positions(grid, end_area)
    other_areas = get_other_functional_areas(grid, start_area, end_area)

    print(f"Start positions: {start_positions}")
    print(f"End positions: {end_positions}")
    print(f"other functional areas positions: {other_areas}")

    # Flood fill to identify the connected regions
    start_area_cells = []
    for start in start_positions:
        start_area_cells.extend(flood_fill(grid, start[0], start[1], start_area))
    
    #print("All the start locations/areas (locations/areas of 1): ", start_area_cells)
    end_area_cells = []
    for end in end_positions:
        end_area_cells.extend(flood_fill(grid, end[0], end[1], end_area))
    #print("All the end locations/areas (locations/areas of 2): ", end_area_cells)


    # Find the closest start and end positions #here we can have a function which calculates which point is theoratically closest to the end point
    #closest_start = start_area_cells[0]  # Assume the first start is closest
    #closest_end = end_area_cells[0]  # Assume the first end is closest


    # Generate all possible paths and track the fastest one
    paths = []
    fastest_path = None
    shortest_distance = float('inf')
    #print("Shortest distance is : ", shortest_distance)

    for start in start_area_cells:
        for end in end_area_cells:
            path = a_star(grid, start, end, other_areas)
            if path:
                paths.append(path)
                if len(path) < shortest_distance:
                    shortest_distance = len(path)
                    fastest_path = path

    # Print the row and column of the path
    if fastest_path:
        print("Fastest path (row, column):")
        for step in fastest_path:
            print(f"({step[0]}, {step[1]})")
    else:
        print("No valid path found between areas.")



    # Pygame setup loading the screen 
    screen = pygame.display.set_mode((len(grid[0]) * WIDTH, len(grid) * HEIGHT))
    pygame.display.set_caption("A* Pathfinding")
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw grid and paths
        draw_grid(screen, grid, paths=paths, highlight_path=fastest_path)
        pygame.time.wait(100)

    pygame.quit()
    #pass



#-------------------------------------------------------------Input array/data area starts from below---------------------------------------------------------------------


#----------------------------------------1. If input array is coming from a text file with a particular format-------------------------------------------------
with open('data_test.txt', 'r') as file:
    array_from_file = []
    
    for line in file:    
        # Remove unnecessary characters like the brackets and split the line into elements
        line = line.strip().strip('[]')
        # Split the line by spaces and replace 'x' as a string
        row = [int(item) if item != 'x' else 'x' for item in line.split()]
        array_from_file.append(row)
        input_array = array_from_file
    #print(input_array)


    # Read all lines into a list
    # array_from_file = [line.strip().split() for line in file]
    # for lists in array_from_file:
    #     for element in lists:
    #         if element == "[":
    #             lists.remove(element)
    #         elif element == "]":
    #             lists.remove(element)
    # input_array = array_from_file

#print(type(array_from_file[0][1]))
#print(type(array_from_file))
#print(array_from_file)


#----------------------------------------2. Sample input array (change this to any new input array to test)----------------------------------------------------
# input_array = [
#     [0, 0, 0, 0, 0, 0, 0, 0, 'x', 'x'],
#     [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 'x', 'x', 0, 'x', 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 'x', 0, 0, 0],
#     [0, 0, 0, 2, 2, 'x', 0, 0, 0, 0],
#     [0, 0, 0, 2, 2, 0, 0, 0, 0, 'x'],
#     [0, 0, 0, 'x', 0, 0, 'x', 0, 0, 0],
#     [0, 'x', 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 3, 3, 0, 0, 0, 0],
#     [0, 'x', 0, 0, 3, 3, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 'x', 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 'x'],
#     [0, 0, 'x', 0, 0, 0, 0, 0, 0, 'x'],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 'x']
# ]


# print(type(input_array))
# print(type(input_array[0][1]))


#----------------------------------------Define start and end areas--------------------------------------------------------

#first_area_user_input = input("Enter starting functional area number: ")
#second_area_user_input = input("Enter end functional area number: ")

#start_area = int(first_area_user_input)
#end_area = int(second_area_user_input)


start_area = 1
end_area = 2

# Call the main function with your desired start and end area
main(input_array, start_area, end_area)