from slither import *

def stop_condition(sim):
    """Stop condition for the simulation."""
    alive_snakes = sum(s.is_alive() for s in sim.world.snakes)
    return alive_snakes <= 1

def init_simulation(population_size, number_of_food, behavior : IBehavior, initial_weights,fov,render=False, color = Renderer.blue):
    """Initialize the simulation with snakes and food."""
    sim = Simulation(Simulation_mode.LEARN, render, 800, 600, 10, number_of_food,500)
    for _ in range(population_size):
        sim.spawn_snakes(1, behavior(sim.world, initial_weights(5)),fov,color)
    return sim

def round_init(sim : Simulation, number_of_food):
    """Initialize a new round in the simulation."""
    snakes = sim.world.snakes
    sim.world.reset()
    sim.reset()
    for snake in snakes:
        sim.spawn_snakes(1, snake.behavior,snake.fov,snake.color)
        
    sim.spawn_food(number_of_food)
    
