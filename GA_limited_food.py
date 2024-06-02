from GA_functions import *

population_size = 15
number_of_best = 3
number_of_food = 2


evolve(EvolvingBehavior,get_null_weights,population_size,number_of_food,number_of_best,False,"GA_limited_food.csv",1000)
