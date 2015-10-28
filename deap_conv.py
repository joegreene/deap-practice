# Nifty conversion function list
def add(a,b):
    return('({} + {})'.format(a,b))

def neg(a):
    return('-{}'.format(a))

def sin(a):
    return('sin({})'.format(a))

def sub(a,b):
    return('({} - {})'.format(a,b))

def div(a,b):
    return('({} / {})'.format(a,b))

def mul(a,b):
    return('({} * {})'.format(a,b))

# End of nifty conversion function list

# Print out the converted candidate
def convertFunct(candidate):
    x = 'x'
    return eval(str(candidate))
