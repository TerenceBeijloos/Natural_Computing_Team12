from slither import *
from utils import *
from sim_functions import *
import numpy as np

class EvolvingBehavior(IBehavior):
    def __init__(self, world, weights):
        self.world = world
        self.weights = weights
    
    def decide_direction(self, snake):
        if random.uniform(0.0, 1.0) < 0.1:
            return Direction.random()
        
        max_dist = max_distance(self.world.width, self.world.height)
        food = self.world.food
        snakes = other_snakes(snake, self.world.snakes)
        directions = []
        
        directions.append({d: value * self.weights[0] for d, value in direction_to_nearest_food(snake, food, max_dist).items()})
        directions.append({d: value * self.weights[1] for d, value in sum_direction_to_food(snake, food, max_dist).items()})
        directions.append({d: value * self.weights[2] for d, value in distance_to_nearest_snake(snake, snakes, max_dist).items()})
        directions.append({d: value * self.weights[3] for d, value in sum_direction_to_snakes(snake, snakes, max_dist).items()})
        directions.append({d: value * self.weights[4] for d, value in direction_to_walls(snake, self.world.width, self.world.height).items()})

        if is_null_directions(directions):
            return Direction.random()

        best_direction = None
        highest_value = 0
        
        for direction_dict in directions:
            for key, value in direction_dict.items():
                if abs(value) > abs(highest_value):
                    highest_value = value
                    best_direction = key
        
        if not best_direction: 
            Direction.random()
            
        d = {best_direction : highest_value}
        direction = highest_direction(d)   
            
        return direction
    
def get_random_weights(number_of_weights):
    return [random.uniform(-1.0, 1.0) for _ in range(number_of_weights)]

def get_null_weights(number_of_weights):
    return [0 for _ in range(number_of_weights)]

def  evaluate(snakes, sim : Simulation):
    """Evaluate the fitness of each snake."""
    snake_lengths = [snake.length() for snake in snakes]
    fitness = []
    for i in range(len(snake_lengths)):
        fitness.append(snake_lengths[i])
            
    return fitness

    """Select the best snakes based on fitness."""
def get_best_snakes(fitness, snakes, amount):
    sorted_pairs = sorted(zip(fitness, snakes), key=lambda pair: pair[0], reverse=True)
    best_snakes = [pair for pair in sorted_pairs[:amount]]
    return best_snakes


def normalize(weights):
    """Normalize the weights to be within the range [-1, 1]."""
    min_weight = min(weights)
    max_weight = max(weights)

    # If all weights are the same, avoid division by zero
    if min_weight == max_weight:
        return [0] * len(weights)
    
    return [(2 * (w - min_weight) / (max_weight - min_weight)) - 1 for w in weights]


def mutate_behavior(behavior, fitness):
    """Mutate the weights of a snake's behavior adaptively based on fitness."""
    new_weights = []

    base_mutation_rate = 0.1

    mutation_rate = base_mutation_rate / (1 + fitness)
    mutation_rate = max(0.01, min(mutation_rate, 1.0))

    for weight in behavior.weights:
        if random.random() < mutation_rate:
            mutation_value = random.gauss(0, 0.1)
            new_weight = weight + mutation_value
        else:
            new_weight = weight
        new_weights.append(new_weight)

    behavior.weights = new_weights

def get_next_population(best_snakes,population_size, elitism, number_of_best):
    """Generate the next population of snakes."""
    new_population = []
    # snakes = [snake[1] for snake in best_snakes]

    # Replicate best snakes to ensure minimum population size
    while len(new_population) < population_size:
        new_population.extend(best_snakes)
    
    # Trim the population to the exact size
    new_population = new_population[:population_size]
    
    # Mutate non-elite snakes
    if elitism:
        for snake in new_population[number_of_best:]:
            mutate_behavior(snake[1].behavior,snake[0])
    else:
        for snake in new_population:
            mutate_behavior(snake[1].behavior,snake[0])
    
    new_population = [snake[1] for snake in new_population]
    
    for i in range(len(new_population)):
        new_population[i].index = i
    
    return new_population

def evolve(behavior, initial_weights, population_size, number_of_food, number_of_best, elitism, file_name, iterations, fov=God_view()):
    """Run the evolutionary algorithm."""
    sim = init_simulation(population_size,number_of_food,behavior,initial_weights,fov)
    rounds_per_sim = 10
    for generation in range(iterations):
        fitness = [0 for _ in range(population_size)]
        for _ in range(rounds_per_sim):
            round_init(sim,number_of_food)
            sim.run(stop_condition)
            current_fitness = evaluate(sim.world.snakes, sim)
            fitness = [fitness[i] + current_fitness[i] for i in range(population_size)]
            
        best = get_best_snakes(fitness, sim.world.snakes, number_of_best)
        # print("Best:",best[0].behavior.weights)
        weights_to_file(best[0][1].behavior.weights,file_name,['Nearest food', 'General food', 'Nearest snake', 'General snake', 'Walls', 'Fitness'],best[0][0]/rounds_per_sim)
        sim.world.snakes = get_next_population(best,population_size,elitism,number_of_best)
        