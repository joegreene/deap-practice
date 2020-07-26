# pylint: disable=no-member, too-many-arguments, too-many-locals
'''
Description:

Main interface for using deap.algorithms.eaSimple via importing this script.

TODO:
- See if the function set (in init_pset) is complete. Match this with `make_algebraic.py`.

Links:
- DEAP eaSimple Example: https://github.com/DEAP/deap/blob/master/examples/gp/symbreg.py
- DEAP: http://deap.gel.ulaval.ca/doc/default/tutorials/advanced/gp.html
- sympy: http://docs.sympy.org/dev/tutorial/simplification.html
'''
import math
import operator
import random
from typing import Callable, Generator, Tuple, Union

from deap import algorithms, base, creator, tools, gp
import numpy
import sympy

from . import make_algebraic


def create_pset() -> gp.PrimitiveSet:
    '''Creates and configures a DEAP primitive set (for a DEAP toolbox object).'''
    pset = gp.PrimitiveSet('main', 1)  # defines number of variables we have (1 here)

    # For each function to apply, define the operator function and its operand count (i.e. arity)
    pset.addPrimitive(operator.sub, 2)
    pset.addPrimitive(operator.mul, 2)
    pset.addPrimitive(operator.add, 2)
    pset.addPrimitive(operator.neg, 1)

    # Terminal set; All constants are within [-1, 1]
    pset.addEphemeralConstant('rand-1to1', lambda: random.randint(-1, 1))

    # For easier readability, make output variables use 'x' as the input var
    pset.renameArguments(ARG0='x')

    return pset


def create_toolbox(actual_func: Callable[[float], float], tournament_size: int) -> base.Toolbox:
    '''Creates and configures a DEAP toolbox object, which contains each evolution operator.'''

    # TODO(joegreene) Document the types here
    def eval_symbol(individual, points, toolbox) -> Tuple[float]:
        '''Computes the mean squared error between a generated candidate and the actual function.'''
        # Translate the tree expression into a callable function
        candidate = toolbox.compile(expr=individual)

        # Evaluate the mean squared error between the expression and the real function
        mean_squared_error = ((candidate(x) - actual_func(x))**2 for x in points)
        return (math.fsum(mean_squared_error) / len(points),)

    # Create toolbox
    toolbox = base.Toolbox()

    # Set weight to -1.0 because this is working on a minimization problem
    weights = (-1.0,)
    creator.create('FitnessMin', base.Fitness, weights=weights)
    creator.create('Individual', gp.PrimitiveTree, fitness=creator.FitnessMin)

    # Create and add function/primitive set to toolbox
    pset = create_pset()
    toolbox.register('expr', gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.expr)

    # Add population to toolbox
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    toolbox.register('compile', gp.compile, pset=pset)

    # Evaluation function here (arguments past evalSymReg are param to pass to evalSymReg)
    # NOTE: points refers to the training set to use
    points = [(i-30)/10.0 for i in range(60)]
    toolbox.register('evaluate', eval_symbol, points=points, toolbox=toolbox)

    # Tournament size
    toolbox.register('select', tools.selTournament, tournsize=tournament_size)

    # Mating strategy
    toolbox.register('mate', gp.cxOnePoint)
    toolbox.register('expr_mut', gp.genFull, min_=0, max_=2)
    toolbox.register('mutate', gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    # Limit mating and mutation tree heights to 17
    toolbox.decorate('mate', gp.staticLimit(key=operator.attrgetter('height'), max_value=17))
    toolbox.decorate('mutate', gp.staticLimit(key=operator.attrgetter('height'), max_value=17))

    return toolbox


def error_margin(validation_file: str, winner_func: Callable[[float], float]) -> float:
    '''Computes the margin of error between a validation data set and a candidate function.'''

    def load_coordinates() -> Generator[Tuple[float], None, None]:
        '''Initialize the validation training data set from a given file.

        The expected file format is a new-line separated list of tuples, where each
        tuple is a space-separated input and output coordinate.
        '''
        with open(validation_file, 'r') as file:
            for line in file:
                in_coord, out_coord = line.rstrip().strip('()').split(' ')
                coordinate = (float(in_coord), float(out_coord))
                yield coordinate

    # Compute the margin of error
    return sum(abs(winner_func(inp) - out) for inp, out in load_coordinates())


def ea_simple(actual_func: Callable[[float], float], validation_file: str, num_generations: int,
              initial_population: int, crossover_prob: float, mutation_prob: float,
              tournament_size: int, seed: Union[int, None] = None, verbose: bool = True):
    '''Sets up and calls deap.algorithms.eaSimple using the given arguments.'''
    # Use a constant seed value factor to get consistent results
    random.seed(seed)

    # Set up eaSimple arguments
    toolbox = create_toolbox(actual_func, tournament_size)
    population = toolbox.population(n=initial_population)

    # Set up stats object to maintains statistics of the evolution
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    stats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    stats.register('avg', numpy.mean)
    stats.register('std', numpy.std)
    stats.register('min', numpy.min)
    stats.register('max', numpy.max)

    # Extract only the best generated function from eaSimple
    halloffame = tools.HallOfFame(1)

    print('Running tournament. This may take awhile.')
    algorithms.eaSimple(population, toolbox, crossover_prob, mutation_prob,
                                   num_generations, stats, halloffame, verbose)

    # Winning candidate is the first element of halloffame
    winner_raw = halloffame[0]
    print(f'Complete.\n\nThe winning function is: \n\n{winner_raw}\n\n')

    # Translate the winning candidate to a callable function (to compute its error margin versus the
    # actual data points)
    # TODO(joegreene) Figure out if winner_callable can be used as a human-readable function
    winner_callable = toolbox.compile(winner_raw)
    margin_of_error = error_margin(validation_file, winner_callable)
    print(f'With a margin of error of {margin_of_error}, or {margin_of_error:.2f}%)\n')

    # Convert the winner from its functional form to an easier-to-read form
    algebraic_form = make_algebraic(winner_raw)
    print(f'Algebraic form:\n{algebraic_form}\n')

    simplified_form = sympy.simplify(algebraic_form)
    print(f'Simplified form:\n{simplified_form}\n')

    expanded_form = sympy.expand(simplified_form)
    print(f'Expanded form (of simplified form): {expanded_form}\n')
