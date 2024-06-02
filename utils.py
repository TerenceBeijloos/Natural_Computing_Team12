from slither import *
import csv

def null_directions():
    return {
        Direction.NORTH: 0,
        Direction.SOUTH: 0,
        Direction.WEST: 0,
        Direction.EAST: 0,
    }
    
# Define what null_directions means
def is_null_directions(directions):
    for direction_dict in directions:
        if any(value != 0 for value in direction_dict.values()):
            return False
    return True
    

def calculate_distance(point1, point2) -> float:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)
    
class Circle_view:
    def __init__(self, radius):
        self.radius = radius
    
    def in_view(self, pos1 : Coordinate, pos2 : Coordinate) -> bool:
        return calculate_distance(pos1,pos2) <= self.radius


def add_directions(directions1, directions2):
    result = {}
    
    for dir in directions1:
        result[dir] = directions1[dir] + directions2[dir]
        
    return result

def tuples_to_coordinates(tuples):
    result = []
    for x,y in tuples:
        result.append(Coordinate(x,y))
        
    return result

def normalized_distance_to(coordinate: Coordinate, objects: list[Coordinate], max_distance: float) -> dict:
    if not objects:
        return null_directions()  # No objects available

    # Calculate the average position of the objects
    avg_x = sum(obj.x for obj in objects) / len(objects)
    avg_y = sum(obj.y for obj in objects) / len(objects)
    avg_position = Coordinate(avg_x, avg_y)

    # Calculate the distance to the average position
    distance_to_avg = calculate_distance(coordinate, avg_position)

    if distance_to_avg == 0:
        return null_directions() # If the coordinate is at the average position

    # Normalize the distance
    normalized_distance = 1-(distance_to_avg / max_distance)
    normalized_distance = min(normalized_distance, 1)  # Ensure the value does not exceed 1

    directions = null_directions()

    if coordinate.y > avg_position.y:
        directions[Direction.NORTH] = normalized_distance
    if coordinate.y < avg_position.y:
        directions[Direction.SOUTH] = normalized_distance
    if coordinate.x < avg_position.x:
        directions[Direction.EAST] = normalized_distance
    if coordinate.x > avg_position.x:
        directions[Direction.WEST] = normalized_distance

    # print(directions)
    return directions

def max_distance(width,height):
    return calculate_distance(Coordinate(0,0),Coordinate(width,height))

def get_random_weights(number_of_weights):
     return [random.uniform(-1, 1.0) for i in range(number_of_weights)]

def highest_direction(directions: dict[Direction, int]) -> Direction:
    if not directions:
        return None
    
    opposite_direction = {
        Direction.NORTH : Direction.SOUTH,
        Direction.SOUTH : Direction.NORTH,
        Direction.WEST : Direction.EAST,
        Direction.EAST : Direction.WEST
    }         
    
    max_key = max(directions, key=lambda k: abs(directions[k]))
    if directions[max_key] < 0:
        max_key = opposite_direction[max_key]
    return max_key

def other_snakes(snake, snakes):
    return [s for s in snakes if s != snake and s.is_alive()]

def direction_to_nearest_food(snake: Snake, food_list: list[Coordinate],max_distance) -> dict[Direction, int]:
    if not food_list:
        return {}  # No food available
    
    nearest_food = to_coordinate(min(food_list, key=lambda food: calculate_distance(snake.head(), to_coordinate(food))))
    
    if not (snake.fov.in_view(snake.head(),nearest_food)):
        return null_directions()
    
    result = normalized_distance_to(snake.head(),[nearest_food],max_distance)
    # print(result)
    return result

def sum_direction_to_food(snake: Snake, food_list: list[Coordinate], max_distance) -> dict[Direction, int]:
    food = tuples_to_coordinates(food_list)
    food_in_view = [obj for obj in food if snake.fov.in_view(snake.head(),obj)]
    return normalized_distance_to(snake.head(),food_in_view,max_distance)
           
def direction_to_walls(snake: Snake, width: int = 800, height: int = 600) -> dict[Direction, int]:
    head = snake.head()
    
    north_coord = Coordinate(head.x, 0)
    south_coord = Coordinate(head.x, height)
    west_coord  = Coordinate(0, head.y)
    east_coord  = Coordinate(width, head.y)
    
    # print(f"Head: {head}")
    # print(f"North Coord: {north_coord}, In View: {snake.fov.in_view(head, north_coord)}")
    # print(f"South Coord: {south_coord}, In View: {snake.fov.in_view(head, south_coord)}")
    # print(f"West Coord: {west_coord}, In View: {snake.fov.in_view(head, west_coord)}")
    # print(f"East Coord: {east_coord}, In View: {snake.fov.in_view(head, east_coord)}")
    
    distances = {
        Direction.NORTH: (height - head.y) / height if snake.fov.in_view(head, north_coord) else 0,
        Direction.SOUTH: head.y / height if snake.fov.in_view(head, south_coord) else 0,
        Direction.WEST: (width - head.x) / width if snake.fov.in_view(head, west_coord) else 0,
        Direction.EAST: head.x / width if snake.fov.in_view(head, east_coord) else 0,
    }

    return distances

def distance_to_nearest_snake(snake : Snake, other : list[Snake], max_distance):
    if not other:
        return null_directions()
    
    head = snake.head()
    nearest_snake = min(other, key=lambda s: calculate_distance(head, s.head()))

    other_snake = []
    for body_part in nearest_snake.body:
        if snake.fov.in_view(head,body_part):
            other_snake.append(body_part)
                    
    if not other_snake:
        return null_directions()
    
    return normalized_distance_to(head,other_snake,max_distance)

def sum_direction_to_snakes(snake : Snake, other_snakes : list[Snake],max_distance):
    head = snake.head()
    other = []
    for s in other_snakes:
        if s.is_alive():
            for body_part in s.body:
                if snake.fov.in_view(head,body_part):
                    other.append(body_part)

    return normalized_distance_to(head,other,max_distance)

def weights_to_file(weights, file_path, header, fitness):
    # Check if the file exists to write header only once
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            file_exists = any(row for row in reader)
    except FileNotFoundError:
        file_exists = False

    values = weights + [fitness]
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Write header only if file is new
        writer.writerow(values)
