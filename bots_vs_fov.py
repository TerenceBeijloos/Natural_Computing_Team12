from sim_functions import *
from utils import *
from GA_functions import EvolvingBehavior, evaluate
import pandas as pd

class Greedy_bot(IBehavior):
    def __init__(self, world : World, weights):
        self.world = world
    
    def decide_direction(self, snake):
        return highest_direction(direction_to_nearest_food(snake,self.world.food,max_distance(self.world.width,self.world.height)))
        
def is_bot(snake : Snake):
    return isinstance(snake.behavior,Greedy_bot)        
      
def fitness_to_file(file_path,fitness):
    # Check if the file exists to write header only once
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            file_exists = any(row for row in reader)
    except FileNotFoundError:
        file_exists = False

    values = [fitness]
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Fitness"])  # Write header only if file is new
        writer.writerow(values)
        
def get_weight(file_names):
    # Load the data from the CSV file
    data = pd.read_csv(file_names)

    # Drop the 'Fitness' column
    weights_data = data.drop(columns=['Fitness'])

    # Extract the last row of weights
    return weights_data.iloc[-1].tolist()
    
def get_weights(file_name):
    result = []
    for i in range(1,11):
        name = file_name + str(i) + '.csv'
        result.append(get_weight(name))

    return result

population_size = 8
number_of_food = 10
weights = get_weights("./fov/weights/circle5_view")
           
block_size = 20
fov = Circle_view(block_size*5)


def init_round(sim : Simulation, number_of_food : int):
    snakes = sim.world.snakes
    sim.world.reset()
    sim.reset()
    for snake in snakes:
        if not is_bot(snake):
            snake.behavior.weights = weights[random.randint(0,9)]
            
        sim.spawn_snakes(1, snake.behavior,snake.fov,snake.color)
    
    sim.spawn_food(number_of_food)
    
def trained_weights(number_of_weights):
    return weights[random.randint(0,9)]

sim :Simulation = init_simulation(0,number_of_food, EvolvingBehavior, trained_weights,fov,False, Renderer.yellow)
sim.spawn_snakes(population_size,Greedy_bot(sim.world,0))
sim.spawn_snakes(population_size, EvolvingBehavior(sim.world, trained_weights(5)),fov,Renderer.yellow)

for _ in range(1000):
    bots_fitness  = 0
    snake_fitness = 0
    for _ in range(10):
        round_init(sim,number_of_food)
        sim.run(stop_condition)
        
        bots = [snake for snake in sim.world.snakes if is_bot(snake)]
        snakes = [snake for snake in sim.world.snakes if not is_bot(snake)]
        
        bots_evaluation = evaluate(bots,sim)
        snake_evaluation = evaluate(snakes,sim)

        bots_fitness += sum([element for element in bots_evaluation]) / population_size
        snake_fitness += sum([element for element in snake_evaluation]) / population_size
    
    bots_fitness  /= 10
    snake_fitness /= 10


    fitness_to_file("fov/bots_fitness.csv",bots_fitness)
    fitness_to_file("fov/snakes_fitness.csv",snake_fitness)