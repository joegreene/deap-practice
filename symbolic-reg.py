# PROJECT: DEAP Test
#
# Description: This script (along with deap_conv.py) 
#
# References:
# - DEAP eaSimple Example: https://github.com/DEAP/deap/blob/master/examples/gp/symbreg.py
# - CS 481 Summer Work: https://github.com/ciarand/secret-nemesis
# - DEAP: http://deap.gel.ulaval.ca/doc/default/tutorials/advanced/gp.html
# - sympy: http://docs.sympy.org/dev/tutorial/simplification.html

import operator, math, random, numpy
from sympy import simplify, expand
from deap-conv import *
from deap import algorithms, base, creator, tools, gp

# ============================== EVALUATION ===================================
def evalSymbReg(individual, points, toolbox):
    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x**4 - 4*x**3
    sqerrors = ((func(x) - (x**4 - 4*x**3))**2 for x in points)
    return math.fsum(sqerrors) / len(points),
# ============================== END OF EVAL ==================================

# ============================== CREATE FUNCT SET =============================
def initFunctSet():
    """ Creates and configures a DEAP function set (for a DEAP toolbox object) """
    fset = gp.PrimitiveSet("main", 1)  # defines number of variables we have (1 here)
    
    fset.addPrimitive(operator.sub, 2) # format: operator, operands
    fset.addPrimitive(operator.mul, 2) # "                        "
    fset.addPrimitive(operator.add, 2) # "                        "
    fset.addPrimitive(operator.neg, 1) # format: operand
    
    # Terminal set; random.randint is inclusive and all constants are [-1,1]
    fset.addEphemeralConstant("rand-1to1", lambda: random.randint(-1,1))

    # For own convenience (default output for variables is ARG#)
    fset.renameArguments(ARG0='x')
    
    return fset 

# ============================== END CREATE FUNCT =============================

# ============================== CREATE TOOLBOX ===============================
def initToolbox():
    """ Creates and configures a DEAP toolbox object """
    # Working with a minimization problem, so set weight to -1.0
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)
    
    # Create toolbox
    toolbox = base.Toolbox()
    
    # Create function set
    pset = initFunctSet()
    
    # Add function set to toolbox
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    
    # Population function
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)

    # Evaluation function here (arguments past evalSymReg are param to pass to evalSymReg)
    # NOTE: points refers to the training set to use
    toolbox.register("evaluate", evalSymbReg, points=[(i-30)/10.0 for i in range(60)], 
                      toolbox=toolbox)
    
    # Sets up tournament size
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    # Mating strategy
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
    
    # Limit mating and mutation tree heights to 17
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    
    return toolbox
# ============================== END OF TOOLBOX CREATE ========================

# ============================== TRAINING DATA SET ============================
def getDataset(filename = "test.txt"):
    data = list()
    for line in open(filename, "r"):
        inp, out = line.rstrip().strip("()").split(" ")
        data.append((float(inp), float(out)))
    return data

# ============================== END OF TRAINING SET ==========================

def main(num_generations=172,
         initial_pop_num=600,
         crossover_prob=0.85,
         mutation_prob=0.15,
         tournament_size=3):
    
    random.seed(318)
    
    toolbox = initToolbox()
    pop = toolbox.population(n=initial_pop_num)
    hof = tools.HallOfFame(1)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    print("Please wait. This may take awhile...")

    pop, log = algorithms.eaSimple(pop, toolbox, 
    				   crossover_prob, mutation_prob, 
    				   num_generations, stats=mstats,
                     		   halloffame=hof, verbose=False)
    
    print(log)

    winner_raw = hof[0]
    winner = toolbox.compile(winner_raw)
    
    margin_of_error = 0.0
    
    for row in getDataset():
        inp, out = row
        margin_of_error += abs(winner(inp) - out)

    print("The winning function was: \n\n%s\n\n" % winner_raw)
    print("With a margin of error of %f\n" % margin_of_error)
    
    # Convert the winner to a more user-readable format (from the conv.py)
    # NOTE: simplify is from sympy, which (unsurprisingly) simplifies the expression
    # NOTE: expand is from sympy, which (unsurpisingly) expands the expression
    final_eq = expand( simplify( convertFunct(winner_raw) ) )
    
    # print final equation
    print("Human-readable version: %s\n" % final_eq)

if __name__ == "__main__":
    main()
