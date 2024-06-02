from GA_functions import *

population_size = 2
number_of_best = 1
number_of_food = 10


evolve(EvolvingBehavior,get_null_weights,population_size,number_of_food,number_of_best,False,"GA_two_snakes.csv",1000)
