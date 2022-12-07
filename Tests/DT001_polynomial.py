#usr/bin/python3
"""
Module math_extra_lib.Tests.UT001_polynomial

Implements demonstration testing of the module math_extra_lib.polynomial, which
are auxilary to the functional unit tests see TE00 and TE001 documents.

Aim is to show the str and repr representation of the objects, and to
demonstrate the exceptions' descriptions.
"""

__version__ = "1.0.0.0"
__date__ = "07-12-2022"
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

import math_extra_lib.polynomial as testmodule

#helper functions

def PrintError(Error: Exception) -> None:
    print(Error.__class__.__name__, ':', Error)
    print(Error.Traceback.Info)

#test area

if __name__=='__main__':
    print('Basic functionality demonstration...')
    Poly1 = testmodule.Polynomial(-2, 1, 0, -3.2, 2.0)
    Poly2 = testmodule.Polynomial(2.5, -1, 0.5, 3.2)
    print('P(x)=', Poly1, 'and is', repr(Poly1))
    print('Q(x)=', Poly2, 'and is', repr(Poly2))
    print('2 * P(x)=', 2 * Poly1)
    print('P(x)/2=', Poly1 / 2)
    print('P(x) + 2=', Poly1 + 2)
    print('P(x) - 2=', Poly1 - 2)
    print('2 - P(x)=', 2 - Poly1)
    print('P(x)**2=', Poly1 ** 2)
    Poly3 = Poly1 + Poly2
    print('P(x)+Q(x)=', Poly3, 'and is', repr(Poly3))
    del Poly3
    Poly3 = Poly1 - Poly2
    print('P(x)-Q(x)=', Poly3, 'and is', repr(Poly3))
    del Poly3
    Poly3 = Poly1 * Poly2
    print('P(x)*Q(x)=', Poly3, 'and is', repr(Poly3))
    del Poly3
    print('P(x)//Q(x)=', Poly1 // Poly2, 'and', 'P(x)%Q(x)=', Poly1 % Poly2)
    print('div(P(x),Q(x))=', '({}, {})'.format(*divmod(Poly1, Poly2)))
    Quot = Poly1 // Poly2
    Rem = Poly1 % Poly2
    print('Check... Q(x) * (P(x)//Q(x)) + P(x)%Q(x)=', Poly2*Quot + Rem)
    del Quot
    del Rem
    print('P`(x)=', Poly1.getDerivative())
    print('P``(x)=', Poly1.getDerivative(Degree = 2))
    print('P```(x)=', Poly1.getDerivative(Degree = 3))
    print('P````(x)=', Poly1.getDerivative(Degree = 4))
    print('P`````(x)=', Poly1.getDerivative(Degree = 5))
    print('P``````(x)=', Poly1.getDerivative(Degree = 6))
    print('Integral of P(x)=', Poly1.getAntiderivative())
    print('Convolution P(Q(x))=', Poly1.getConvolution(Poly2))
    RatFunc = testmodule.RationalFunction(Poly1, Poly2)
    print('Rational function f(x)=P(x)/Q(x) is', repr(RatFunc))
    print('f(x)=', RatFunc)
    print('f(0)=', RatFunc(0), 'P(0)=', Poly1(0), 'Q(0)=', Poly2(0),
                                                'P(0)/Q(0)=', Poly1(0)/Poly2(0))
    print('f(1)=', RatFunc(1), 'P(1)=', Poly1(1), 'Q(1)=', Poly2(1),
                                                'P(1)/Q(1)=', Poly1(1)/Poly2(1))
    print('f(-1)=', RatFunc(-1), 'P(-1)=', Poly1(-1), 'Q(-1)=', Poly2(-1),
                                            'P(-1)/Q(-1)=', Poly1(-1)/Poly2(-1))
    del Poly2
    del RatFunc
    input('Exceptions demonstration...Press Enter')
    try:
        Poly = testmodule.Polynomial(-2, 1, '0', -3.2, 2.0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        Poly = testmodule.Polynomial(-2)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        Poly = testmodule.Polynomial(-2, 1, 0, -3.2, 0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        Poly = testmodule.Polynomial.fromRoots(1, '-1', 0.0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        Poly = testmodule.Polynomial.fromRoots()
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        Poly1('abc')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        print(Poly1+'abc')
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        print(Poly1/0)
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        print(Poly1**(-1))
    except Exception as err:
        PrintError(err)
    del Poly1
    input('Press Enter')
    try:
        RatFunc = testmodule.RationalFunction(1, (-1, 0, 1))
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        RatFunc = testmodule.RationalFunction((1, 1), (-1, 'abc', 1))
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        RatFunc = testmodule.RationalFunction((1, ), (-1, 1, 1))
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        RatFunc = testmodule.RationalFunction((1, 1), (-1, 1, 0))
    except Exception as err:
        PrintError(err)
    RatFunc = testmodule.RationalFunction((1,1), (-1, 0, 1))
    input('Press Enter')
    try:
        print(RatFunc('abc'))
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        print(RatFunc(1))
    except Exception as err:
        PrintError(err)
    del RatFunc