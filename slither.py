
import enum
import pygame
import random
from enum import Enum
from abc import ABC, abstractmethod

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    def random():
        return random.choice([Direction.NORTH,Direction.EAST,Direction.SOUTH,Direction.WEST])

class Field_type(Enum):
    HEAD = 1
    BODY = 2
    FOOD = 3
    VOID = 4

class Simulation_mode(Enum):
    LEARN = 1
    PLAY = 2
    
def to_coordinate(position : tuple):
    x,y = position
    return Coordinate(x,y)

class Coordinate:
    def __init__(self,x=0,y=0):
            self.x = x
            self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Index out of range. Use 0 for x and 1 for y.")

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Operand must be of type Coordinate")
        
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Coordinate(self.x / other, self.y / other)
        else:
            raise TypeError("Operand must be a number")
        
    def __ne__(self, other):
        return (self.x != other.x or self.y != other.y)
    
    def tuple(self):
        return(self.x, self.y)

def apply_direction(coordinate : Coordinate, direction : Direction, step_size):
    new_coordinate = coordinate
    
    if direction == Direction.NORTH:
        new_coordinate.y = new_coordinate.y - step_size
    elif direction == Direction.EAST:
        new_coordinate.x = new_coordinate.x + step_size
    elif direction == Direction.SOUTH:
        new_coordinate.y = new_coordinate.y + step_size
    elif direction == Direction.WEST:
        new_coordinate.x = new_coordinate.x - step_size
        
    return new_coordinate
    
class IFov(ABC):
    @abstractmethod
    def in_view(self, pos1 : Coordinate, pos2 : Coordinate) -> bool:
        pass

class IBehavior(ABC):
    @abstractmethod
    def decide_direction(self, snake):
        pass

class God_view(IFov):
    def in_view(self, pos1 : Coordinate, pos2 : Coordinate) -> bool:
        return True

class Snake:
    def __init__(self, head : Coordinate, id, behavior : IBehavior, color, fov : IFov = God_view()):
        self.body = [head]
        self.id = id
        self.behavior = behavior
        self.index = 0
        self.previous = [head.tuple()]
        self.direction = Direction.NORTH
        self.fov = fov
        self.color = color

    def __getitem__(self, key):
            return self.body[key]
        
    def is_dead(self):
        return self.length() == 0
    
    def is_alive(self):
        return self.length() > 0
        
    def grow(self):
        if self.is_alive():
            self.body.append(self.body[-1])
        
    def head(self):
        return self.body[0]
    
    def tail(self):
        return self.body[1:]
        
    def length(self):
        return len(self.body)
    
    def eliminate(self, world):
        if self.is_dead():
            return
        new_food = self.body[1::2]
        for x,y in new_food:
            world.add_food(Coordinate(x,y))
            
        self.body = []
        
    def move(self, direction : Direction, step_size):
        new_head = apply_direction(Coordinate(self.head().x,self.head().y),direction, step_size)
        self.direction = direction
        del self.body[-1]
        self.body.insert(0,new_head)

    def step(self, step_size):
        if self.length() == 0:
            return
        
        direction = self.behavior.decide_direction(self)
        self.previous = [b.tuple() for b in self.body]
        self.move(direction, step_size)
        self.direction = direction

class World:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_size = 20
        self.snakes = []
        self.food = set([])
            
    def reset(self):
        self.snakes = []
        self.food = set([])
        
    def add_snake(self,snake):
        if len(self.snakes) == 0:
            snake.index = 0
        else:
            snake.index = self.snakes[-1].index+1
            
        self.snakes.append(snake)
        
    def add_food(self,food : Coordinate):
        self.food.add(food.tuple())

    def get_collisions(self):
        snake_positions = {}

        for snake in self.snakes:
            if not snake:
                continue
            for i in range(snake.length()):
                coordinate : Coordinate = snake[i].tuple()
                if not (coordinate in snake_positions):
                    snake_positions[coordinate] = []
                    
                snake_positions[coordinate].append(snake)
                
        return self.get_snake_food_collisions(snake_positions), self.get_snake_snake_collisions(self.snakes), self.get_wall_collisions()

    def get_wall_collisions(self):
        collisions = []
        
        for snake in self.snakes:
            if snake.is_dead():
                continue
            
            head = snake.head()
            
            if head.x < 0 or head.x > self.width or \
                head.y < 0 or head.y > self.height:
                    collisions.append(snake)

        return collisions

    def get_snake_food_collisions(self, snake_positions):
        collisions = []
    
        for coordinate in self.food:
            if coordinate in snake_positions:
                for snake in snake_positions[coordinate]:
                    if snake.length() > 0:
                        collisions.append((snake,coordinate))
                    
        return collisions
    
    def get_snake_snake_collisions(self, snake_positions: list[Snake]):
        moving_through_collision = {}
        current_position_collision = {}
        
        for snake in snake_positions:
            if snake.is_dead():
                continue
            
            x, y = snake.previous[0]
            middle = ((Coordinate(x, y) + snake.head()) / 2).tuple()
            
            if middle not in moving_through_collision:
                moving_through_collision[middle] = []
            moving_through_collision[middle].append((snake, 0))
            
            for i in range(len(snake.body)):
                current = snake.body[i].tuple()
                if current not in current_position_collision:
                    current_position_collision[current] = []

                current_position_collision[current].append((snake, i))
        
        collisions = []
        for key, snakes in moving_through_collision.items():
            if len(snakes) < 2:
                continue
            
            for i in range(len(snakes)):
                for j in range(i + 1, len(snakes)):
                    s1, index1 = snakes[i]
                    s2, index2 = snakes[j]
                    collisions.append((s1, s2, index1, index2)) # snake1, snake2, collision with index 0 (head)
                
        for key, snakes in current_position_collision.items():
            if len(snakes) < 2:
                continue
            
            for i in range(len(snakes)):
                for j in range(i + 1, len(snakes)):
                    s1, index1 = snakes[i]
                    s2, index2 = snakes[j]
                    collisions.append((s1, s2, index1, index2)) # snake1, snake2, collision with index 0 (head)
                                    
        return collisions


    
class Renderer:
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    yellow = (255,255,0)

    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.SysFont(None, 30)
        self.clock = pygame.time.Clock()  
        
    def draw_objects(self, objects, color, block_size, brighten_per_block=0, alpha=255):
        # Create a surface for the translucent objects
        temp_surface = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
        color_rgb = pygame.Color(color)
        for block in objects:
            # Adjust the shade of the color
            color_rgb = pygame.Color(
                min(color_rgb.r + brighten_per_block, 255), 
                min(color_rgb.g + brighten_per_block, 255), 
                min(color_rgb.b + brighten_per_block, 255),
                alpha
            )
            # Fill the temporary surface with the color
            temp_surface.fill(color_rgb)
            
            # Draw the rectangle using the temporary surface
            self.screen.blit(temp_surface, (block[0], block[1]))
            
    def draw_fov(self, snake, block_size):
        if isinstance(snake.fov,God_view) or snake.is_dead():
            return
        
        head = snake.head()
        fov_coords = []

        # Generate all possible coordinates in the field of view
        for x in range(self.screen.get_width() // block_size):
            for y in range(self.screen.get_height() // block_size):
                coord = Coordinate(x * block_size, y * block_size)
                if snake.fov.in_view(head, coord) and (coord != head):
                    fov_coords.append(coord.tuple())

        # Draw the FOV area
        self.draw_objects(fov_coords, Renderer.green, block_size, 0, 125)
        
    def draw(self,world : World):
        self.screen.fill(Renderer.black)

        #two for loops to not draw over other snakes
        for snake in world.snakes:
            if snake:
                self.draw_fov(snake,world.block_size)
                
        for food in world.food:
            self.draw_objects([food],Renderer.red,world.block_size)
                
        for snake in world.snakes:
            if snake:
                self.draw_objects(snake.body,snake.color,world.block_size,15)

    def tick(self,speed):
        pygame.display.update()
        self.clock.tick(speed)
        
class Simulation:
    
    def __init__(self, mode : Simulation_mode, render : bool, field_width, field_height, speed, number_of_food, iterations_per_run):
        self.world = World(field_width, field_height)
        if (render or mode == Simulation_mode.PLAY):
            self.renderer = Renderer(field_width,field_height)
        else:
            self.renderer = None
        self.mode = mode
        self.speed = speed 
        self.number_of_food = number_of_food
        self.time_of_death = {}
        self.iteration = 0
        self.iteration_per_run = iterations_per_run
        
    def handle_food_collisions(self, food_collisions):
        for snake, food_coordinate in food_collisions:
            if food_coordinate in self.world.food and snake.is_alive():
                self.world.food.remove(food_coordinate)
                self.world.snakes[snake.index].grow()
            
    def handle_snake_collisions(self, snake_collisions):
        for collision in snake_collisions:
            if len(collision) != 4:
                raise ValueError(f"Expected a tuple with 4 elements, got {collision}")
            
            s1, s2, i1, i2 = collision
            
            if not (hasattr(s1, 'is_alive') and hasattr(s1, 'eliminate')):
                raise TypeError(f"Expected s1 to be a Snakes object, got {type(s1)}")
            
            if not (hasattr(s2, 'is_alive') and hasattr(s2, 'eliminate')):
                raise TypeError(f"Expected s2 to be a Snakes object, got {type(s2)}")
            
            if s1.index == s2.index: # No collisions with itself
                continue
            
            if s1.is_alive() and i1 == 0:
                self.kill_snake(s1)
            if s2.is_alive() and i2 == 0:
                self.kill_snake(s2)
            
    def handle_wall_collisions(self,wall_collisions):
        for snake in wall_collisions:
            self.kill_snake(snake)
            
    def kill_snake(self,snake):
        snake.eliminate(self.world)
        self.time_of_death[snake.index] = self.iteration
        
    def handle_collisions(self):
        food_collisions, snake_collisions, wall_collisions = self.world.get_collisions()
        # print(self.world.fo)
        
        # print(snake_collisions)
        self.handle_snake_collisions(snake_collisions)
        self.handle_food_collisions(food_collisions)
        self.handle_wall_collisions(wall_collisions)
        
    def update_food(self):
        self.spawn_food(self.number_of_food-len(self.world.food))
        
    def update_snakes(self):
        for i in range(len(self.world.snakes)):
            if self.world.snakes[i]:
                self.world.snakes[i].step(self.world.block_size)

    def reset(self):
        self.iteration = 0
        self.time_of_death = {}
        
    def run(self, stop_condition):
        # Clear the screen
        for self.iteration in range(self.iteration_per_run):
            if stop_condition(self):
                break
            
            if self.renderer:
                self.renderer.tick(self.speed)
                self.renderer.draw(self.world)
            
            self.handle_collisions()
            self.update_food()
            self.update_snakes()

            
    def add_snake(self,snake):
        self.world.add_snake(snake)
        
    def add_food(self,coordinate : Coordinate):
        self.world.add_food(coordinate)
        
    def spawn_snakes(self,number,behavior,fov = God_view(), color = Renderer.blue):
        used_coordinates = set([])
        
        for i in range(number):
            block_size = self.world.block_size
            while True:
                x = random.randrange(0, self.world.width - block_size, block_size)
                y = random.randrange(0, self.world.height - block_size, block_size)
                if not ((x,y) in used_coordinates):
                    self.add_snake(Snake(Coordinate(x,y),i,behavior,color,fov))
                    used_coordinates.add((x,y))
                    break
    
    def spawn_food(self,number):
        used_coordinates = set([])
        
        for i in range(number):
            block_size = self.world.block_size
            while True:
                x = random.randrange(0, self.world.width - block_size, block_size)
                y = random.randrange(0, self.world.height - block_size, block_size)
                if not ((x,y) in used_coordinates):
                    self.add_food(Coordinate(x,y))
                    used_coordinates.add((x,y))
                    break