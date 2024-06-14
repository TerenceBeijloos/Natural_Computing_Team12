from sim_functions import *
from utils import *
from GA_functions import EvolvingBehavior

class Greedy_bot(IBehavior):
    def __init__(self, world : World, weights):
        self.world = world
    
    def decide_direction(self, snake):
        return highest_direction(direction_to_nearest_food(snake,self.world.food,max_distance(self.world.width,self.world.height)))
        
population_size = 7
number_of_food = 10
weights = [1.466258876760026,-0.0734985684795867,-2.6569542991187984,-2.1167855823488013,-0.3470788581264732]
block_size = 20
# fov = Circle_view(block_size*5)
fov = God_view()

def trained_weights(number_of_weights):
    return weights[:number_of_weights]

sim :Simulation = init_simulation(population_size,number_of_food, EvolvingBehavior, trained_weights,fov,True, Renderer.yellow)
# sim.spawn_snakes(population_size,EvolvingBehavior(sim.world,trained_weights))
# sim.spawn_snakes(population_size, EvolvingBehavior(sim.world, trained_weights(5)),fov,Renderer.blue)

while True:
    sim.run(stop_condition)
    round_init(sim,number_of_food)
