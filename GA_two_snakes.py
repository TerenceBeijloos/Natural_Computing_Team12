from GA_functions import *

population_size = 2
number_of_best = 1
number_of_food = 10
block_size = 20

evolve(EvolvingBehavior,get_null_weights,population_size,number_of_food,number_of_best,True,"limited_snakes/two_snakes4.csv",7500,God_view())
