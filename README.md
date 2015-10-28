# DEAP-eaSimple-Fun
Had some fun messing around with eaSimple in DEAP

## Library requirements:
This project was developed under a virtual environment and python 3.4, although 
2.7 and other versions of 3 should work alright.

After doing the below preparations, you should be able to run this project by calling 
`python symbolic_reg.py`

### Linux Preparation
Simply use `pip install` to install the following packages

deap==1.0.2

numpy==1.10.1

sympy==0.7.6.1

wheel==0.24.0

### Windows Preparation
Use pip to install `deap`, `wheel`, and `sympy`. `numpy` is a bit different:

1. Depending on your version of python, you have to install the correct corresponding package 
from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy).

e.g. Writing this README I am using Python 3.4.3 on Windows 8.1 64bit, so I would download 
`numpy-1.10.1+mkl-cp35-none-win_amd64.whl`.

2. Afterwards, install the `.whl` file using `pip`:

`pip install <.WHL FILE YOU DOWNLOADED>`

e.g. For me it's: `pip install numpy-1.10.1+mkl-cp35-none-win_amd64.whl`