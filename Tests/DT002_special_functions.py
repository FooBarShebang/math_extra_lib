#usr/bin/python3
"""
Module math_extra_lib.Tests.DT002_special_functions

Implements demonstration testing of the module math_extra_lib.special_functions
- specifically the exceptions generation, which are auxilary to the functional
unit tests see TE00 and TE002 documents.
"""

__version__ = "1.0.0.0"
__date__ = "18-01-2023"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.special_functions as testmodule

#helper functions

def PrintError(Error: Exception) -> None:
    print(Error.__class__.__name__, ':', Error)
    print(Error.Traceback.Info)

#test area

if __name__=='__main__':
    print('Function permutation(n,k) - partial permutation of k out of n...')
    print('Pn(20,10)=', testmodule.permutation(20, 10))
    print('Wrong input treatment demostration.')
    try:
        testmodule.permutation('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.permutation(-1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.permutation(10, 2.0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.permutation(10, 20)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function combination(n,k) - n chose k...')
    print('Cn(20,10)=', testmodule.combination(20, 10))
    print('Wrong input treatment demostration.')
    try:
        testmodule.combination('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.combination(-1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.combination(10, 2.0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.combination(10, 20)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function log_beta(x,y) - log(B(x,y))...')
    print('Log(B(20,10))=', testmodule.log_beta(20, 10))
    print('Wrong input treatment demostration.')
    try:
        testmodule.log_beta('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta(-1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta(10, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta(10, 0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function beta(x,y) - beta-function B(x,y)...')
    print('B(20,10)=', testmodule.beta(20, 10))
    print('Wrong input treatment demostration.')
    try:
        testmodule.beta('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta(-1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta(10, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta(10, 0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function inv_erf(x) - inverse standard error function...')
    print('InvErf(0.5)=', testmodule.inv_erf(0.5))
    print('Wrong input treatment demostration.')
    try:
        testmodule.inv_erf('a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.inv_erf(2)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function lower_gamma(x,y) - lower incomplete gamma function...')
    print('p(0.5, 1.0)=', testmodule.lower_gamma(0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.lower_gamma('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.lower_gamma(1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.lower_gamma(1, -1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.lower_gamma(0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function log_lower_gamma(x,y) - log of lower incomplete gamma function...')
    print('log(p(0.5, 1.0))=', testmodule.log_lower_gamma(0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.log_lower_gamma('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_lower_gamma(1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_lower_gamma(1, 0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_lower_gamma(0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function lower_gamma_reg(x,y) - regulized lower incomplete gamma function...')
    print('P(0.5, 1.0)=', testmodule.lower_gamma_reg(0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.lower_gamma_reg('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.lower_gamma_reg(1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.lower_gamma_reg(1, -1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.lower_gamma_reg(0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function upper_gamma(x,y) - upper incomplete gamma function...')
    print('q(0.5, 1.0)=', testmodule.upper_gamma(0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.upper_gamma('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.upper_gamma(1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.upper_gamma(1, -1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.upper_gamma(0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function log_upper_gamma(x,y) - log of upper incomplete gamma function...')
    print('log(q(0.5, 1.0))=', testmodule.log_upper_gamma(0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.log_upper_gamma('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_upper_gamma(1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_upper_gamma(1, -1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_upper_gamma(0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function lower_gamma_reg(x,y) - regulized upper incomplete gamma function...')
    print('Q(0.5, 1.0)=', testmodule.upper_gamma_reg(0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.upper_gamma_reg('a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.upper_gamma_reg(1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.upper_gamma_reg(1, -1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.upper_gamma_reg(0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Function beta_incomplete(z,x,y) - B(z; x, y)...')
    print('B(0.5; 0.5, 1.0)=', testmodule.beta_incomplete(0.5, 0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.beta_incomplete('a', 0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete(0, 'a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete(0, 1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete(-0.1, 0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete(0, -0.1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete(0, 1, -0.1)
    except Exception as err:
        PrintError(err)
        print('Function log_beta_incomplete(z,x,y) - Log(B(z; x, y))...')
    print('Log(B(0.5; 0.5, 1.0))=', testmodule.log_beta_incomplete(0.5, 0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.log_beta_incomplete('a', 0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta_incomplete(0, 'a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta_incomplete(0, 1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta_incomplete(0, 0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta_incomplete(0.1, -0.1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.log_beta_incomplete(0.1, 1, -0.1)
    except Exception as err:
        PrintError(err)
    print('Function beta_incomplete_reg(z,x,y) - regularized I_z(z; x, y)...')
    print('I_z(0.5; 0.5, 1.0)=', testmodule.beta_incomplete_reg(0.5, 0.5, 1.0))
    print('Wrong input treatment demostration.')
    try:
        testmodule.beta_incomplete_reg('a', 0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete_reg(0, 'a', 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete_reg(0, 1, 'a')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete_reg(-0.1, 0, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete_reg(0, -0.1, 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.beta_incomplete_reg(0, 1, -0.1)
    except Exception as err:
        PrintError(err)