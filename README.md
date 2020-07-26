## deap-practice

Practice script to play with [DEAP's eaSimple](https://deap.readthedocs.io/en/master/api/algo.html#deap.algorithms.eaSimple)
method.

### Build requirements

This project was developed and tested on Python 3.8. Any version that supports the packages within
`requirements.txt` should work though.

It is highly recommended to [set up a virtual environment](https://docs.python.org/3/tutorial/venv.html)
or use [Anaconda](https://www.anaconda.com/products/individual) to set up this project.

### Usage

__DISCLAIMER__: For the time being this only works on mathematical functions that take in a single
input and provide a single output, e.g. `x**4 - 4*x**3`.

After running `pip install -r requirements.txt` run `python main.py` to run the tournament.

#### Modifying the inputs

To configure the script, modify the default args located within `main.py`.

If you wish to provide your own function and data set to play with generation, do the following:

- Create a custom data set. Follow `resources/x4-4x3.txt` for an example on how to format your data.
- Update `VALIDATION_FILE` to point to your custom data set.
- Update `actual_func` so it uses your function (instead of the default `x**4 - 4*x**3`)

#### Interpreting the results

Running `main.py` displays roughly the following output (see `resources/example_output.txt` for
an example):

```
<LOG RESULTS; only if verbose flag is set (default is True)>

<WINNING FUNCTION>

<WINNING FUNCTION'S ALGEBRAIC FORM>

<WINNING FUNCTION'S SIMPLIFIED FORM>

<WINNING FUNCTION'S EXPANDED FORM>
```

- Log results: The results of each generation within the tournament.
- Winning function: The best function generated as a result of running `deap.algorithms.eaSimple`.
- Algebraic form: The winning function's default display is in a functional format (e.g. `add(x, x)`
instead of `x + x`). The code is ran through `make_algebraic` (see `src/make_algebraic.py`) to do
this.

- Simplified form: The algebraic form can get rather long, so this shows the algebraic form ran
through [`sympy.simplify`](https://docs.sympy.org/latest/tutorial/simplification.html#simplify).
- Expanded form: The simplified form can sometimes be clean up a bit more (e.g. terms can be merged
or rearranged). To do this, the simplified form is ran through
[`sympy.expand`](https://docs.sympy.org/latest/tutorial/simplification.html#expand).

### Resources

- DEAP docs: <https://deap.readthedocs.io/en/master/index.html>
- SymPy docs: <https://docs.sympy.org/latest/index.html>
- NumPy docs (using 1.9 as of writing this): <https://numpy.org/doc/>

### Future plans

- Finalize folder structure for project (e.g. `src` instead of `lib` seems weird)
- Support more than just `deap.algorithms.eaSimple`
- Use `argparse` to provide full-blown CLI functionality
- Resolve TODOs in code

-------------------------------------------------------------------------------

Copyright &copy; 2020 Joseph Greene <joe.greene155@gmail.com>
Released under [The MIT License] (<http://opensource.org/licenses/MIT)>
Project located at <https://github.com/joegreene/misc-python-stuff>
