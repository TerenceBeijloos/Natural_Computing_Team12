from GA_functions import *

population_size = 16
number_of_best = 4
number_of_food = 10
block_size = 20

evolve(EvolvingBehavior,get_null_weights,population_size,number_of_food,number_of_best,True,"./baseline/baseline1.csv",1000,God_view())