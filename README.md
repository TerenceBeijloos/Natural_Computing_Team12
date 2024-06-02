# NC_evolve_snake

Install pygame (tested on version (2.5.2))
```
pip install pygame
```

Run the desired experiment or create a new one.
Running the experiments will result in a csv file with weights and fitnesses of the best snake of each iteration
For the baseline run:
```
python.exe GA.py
```

For other experiments run one of: GA_two_snakes.py, GA_limited_food.py, GA_elitism.py, GA_elitism_two_snakes.py

If you want to evaluate how a trained snake behaves, use PLAY.py and assign the variable "weights" with the desired values. Make sure to also set the other parameters similar to the training environment of the snake, such as the field of view, number of snake, and number of food.