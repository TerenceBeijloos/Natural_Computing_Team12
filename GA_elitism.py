from GA_functions import *

population_size = 15
number_of_best = 3
number_of_food = 10
block_size = 20

evolve(EvolvingBehavior,get_null_weights,population_size,number_of_food,number_of_best,True,"GA_elite_circle_view5.csv",1000,Circle_view(block_size*5))
