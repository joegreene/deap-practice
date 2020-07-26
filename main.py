# TODO(joegreene) Add CLI help output to description below (if made)
'''
Description:

Practice script to play with deap.algorithms.eaSimple.
'''
from pathlib import Path

from src import ea_simple


def actual_func(x: float) -> float: # pylint: disable=invalid-name
    '''The actual function that corresponds to the coordinates within validation_file.txt'''
    return x**4 - 4*x**3


if __name__ == '__main__':
    # === DEFAULT ARGS ===
    VALIDATION_FILE = Path('resources', 'x4-4x3.txt')
    NUM_GENERATIONS = 172
    INITIAL_POPULATION = 600
    CROSSOVER_PROBABILITY = 0.85
    MUTATION_PROBABILITY = 0.15
    TOURNAMENT_SIZE = 3

    # Use a constant seed value for consistent results, or None for different results each run
    RANDOM_SEED = 318

    # TODO(joegreene) Make this callable from CLI (argparse)
    ea_simple(actual_func, VALIDATION_FILE, NUM_GENERATIONS, INITIAL_POPULATION,
              CROSSOVER_PROBABILITY, MUTATION_PROBABILITY, TOURNAMENT_SIZE, RANDOM_SEED)
