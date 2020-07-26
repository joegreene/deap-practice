# pylint: disable=eval-used, invalid-name
'''
Description:

Utility script to convert the winner output from deap.algorithms.eaSimple to its algebraic form.
'''
from deap import creator

def add(a: str, b: str) -> str:
    '''Converts function with the format 'add(a, b)' to 'a + b'.'''
    return f'({a} + {b})'


def neg(a: str) -> str:
    '''Converts function with the format 'neg(a)' to '-a'.'''
    return f'-{a}'


def sub(a: str, b: str) -> str:
    '''Converts function with the format 'sub(a, b)' to 'a - b'.'''
    return f'({a} - {b})'


def div(a: str, b: str) -> str:
    '''Converts function with the format 'div(a, b)' to 'a / b'.'''
    return f'({a} / {b})'


def mul(a: str, b: str) -> str:
    '''Converts function with the format 'mul(a, b)' to 'a * b'.'''
    return f'({a} * {b})'

def make_algebraic(func: 'creator.Individual') -> str:
    '''Makes a function (from the halloffame from deap.algorithms.eaSimple) to its algebraic form.

    This works with a little bit of eval trickery and recursion. For example, given the following
    winner candidate:

        add(mul(mul(x, x), x), 2)

    make_algebraic takes a depth-first approach and evaluates the expression as follows:

        add('mul(mul(x, x), x)' '2')
        > mul('mul(x, x)', 'x')
          > mul('x', 'x') = 'x * x'
            > mul('x * x', 'x') = 'x * x * x'
        add('x * x * x + 2') = 'x * x * x + 2'

        End result:
            'x * x * x + 2'
    '''
    x = 'x'
    return eval(str(func))
