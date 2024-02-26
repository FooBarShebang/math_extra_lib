#usr/bin/python3
"""
Module math_extra_lib.Tests.DT004_matrix_solver

Implements demonstration testing of the module math_extra_lib.matrix_solver -
specifically the exceptions generation, which are auxilary to the functional
unit tests see TE00 and TE004 documents.
"""

__version__ = "1.0.0.0"
__date__ = "26-02-2024"
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

import math_extra_lib.poly_solver as testmodule

#helper functions

def PrintError(Error: Exception) -> None:
    print(Error.__class__.__name__, ':', Error)
    if hasattr(Error, 'Traceback'):
        print(Error.Traceback.Info)

#test area

if __name__=='__main__':
    print('Demonstration test DT005 - polynomial roots and interpolation.')
    print('Polynomial roots...')
    XGrid = (0.5, 1, 2, 3, 3.5)
    XGridNotUnique = (0.5, 1, 2, 3, 3)
    YGrid = (1, 2, 2.5, 1.5, 0.5)
    XYGrid = tuple(zip(XGrid, YGrid))
    XYGridNotUnique = tuple(zip(XGridNotUnique, YGrid))
    print(f'X-grid is {XGrid}')
    TestPoly = testmodule.Polynomial.fromRoots(*XGrid)
    print(f'Generated polynomial is {TestPoly}')
    print("Testing the assumption Poly(root) = 0...")
    for Value in XGrid:
        print(f'At x={Value}, Poly(x)={TestPoly(Value)}')
    print('Find roots Poly(x)')
    print(sorted(testmodule.FindRoots(TestPoly)))
    input('Press "Enter"')
    print(f'X-Y grid is {XYGrid}')
    print(f'Lagrange polynomial is {testmodule.InterpolateLagrange(XYGrid)}')
    print(f'Langrange basis is {testmodule.GetLagrangeBasis(XGrid)}')
    print(f'Legendre polynomial is {testmodule.InterpolateLegendre(XYGrid)}')
    print(f'Legendre basis is {testmodule.GetLegendreBasis(len(XGrid))}')
    print(f'Chebyshev polynomial is {testmodule.InterpolateChebyshev(XYGrid)}')
    print(f'Chebyshev basis is {testmodule.GetChebyshevBasis(len(XGrid))}')
    print(f'Bernstein polynomial is {testmodule.InterpolateBernstein(XYGrid)}')
    print(f'Bernstein basis is {testmodule.GetBernsteinBasis(len(XGrid))}')
    input('Error treatment. Press "Enter"')
    try:
        testmodule.FindRoots([1,2,3])
    except Exception as err:
        PrintError(err)
    input('Lagrange Polynomial generation. Press "Enter"')
    try:
        testmodule.GetLagrangePolynomial(2, "1,2,3") #not a sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetLagrangePolynomial("2", [1,2,3]) #not a number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetLagrangePolynomial(2, [1,2,3]) #node == root
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetLagrangePolynomial(2, [1,3,3]) #not unique roots
    except Exception as err:
        PrintError(err)
    input('Lagrange Polynomial base generation. Press "Enter"')
    try:
        testmodule.GetLagrangeBasis("1,2,3") #not a sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetLagrangeBasis([1,2,2]) #same nodes
    except Exception as err:
        PrintError(err)
    input('Lagrange interpolation, Press "Enter"')
    try:
        testmodule.InterpolateLagrange("1,2,2") #not a sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateLagrange([1,2,2]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateLagrange([[1,1],[2,1,1],
                                            [2,2]]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateLagrange(XYGridNotUnique) #not unique X-Grid
    except Exception as err:
        PrintError(err)
    input('Legendre Polynomial generation. Press "Enter"')
    try:
        testmodule.GetLegendrePolynomial(2.0) #not an integer number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetLegendrePolynomial(-1) #negative number
    except Exception as err:
        PrintError(err)
    input('Legendre Polynomial base generation. Press "Enter"')
    try:
        testmodule.GetLegendreBasis(1.0) #not an integer number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetLegendreBasis(-1) #negative number
    except Exception as err:
        PrintError(err)
    input('Legendre interpolation, Press "Enter"')
    try:
        testmodule.InterpolateLegendre("1,2,2") #not a sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateLegendre([1,2,2]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateLegendre([[1,1],[2,1,1],
                                            [2,2]]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateLegendre(XYGridNotUnique) #not unique X-Grid
    except Exception as err:
        PrintError(err)
    input('Chebyshev Polynomial generation. Press "Enter"')
    try:
        testmodule.GetChebyshevPolynomial(2.0) #not an integer number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetChebyshevPolynomial(-1) #negative number
    except Exception as err:
        PrintError(err)
    input('Chebyshev Polynomial base generation. Press "Enter"')
    try:
        testmodule.GetChebyshevBasis(1.0) #not an integer number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetChebyshevBasis(-1) #negative number
    except Exception as err:
        PrintError(err)
    input('Chebyshev interpolation, Press "Enter"')
    try:
        testmodule.InterpolateChebyshev("1,2,2") #not a sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateChebyshev([1,2,2]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateChebyshev([[1,1],[2,1,1],
                                            [2,2]]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateChebyshev(XYGridNotUnique) #not unique X-Grid
    except Exception as err:
        PrintError(err)
    input('Bernstein Polynomial generation. Press "Enter"')
    try:
        testmodule.GetBernsteinPolynomial(2.0, 1) #not an integer number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetBernsteinPolynomial(-1, 1) #negative number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetBernsteinPolynomial(1, 2.0) #not an integer number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetBernsteinPolynomial(1, -1) #negative number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetBernsteinPolynomial(1, 2) #second argument is larger
    except Exception as err:
        PrintError(err)
    input('Bernstein Polynomial base generation. Press "Enter"')
    try:
        testmodule.GetBernsteinBasis(1.0) #not an integer number
    except Exception as err:
        PrintError(err)
    try:
        testmodule.GetBernsteinBasis(-1) #negative number
    except Exception as err:
        PrintError(err)
    input('Bernstein interpolation, Press "Enter"')
    try:
        testmodule.InterpolateBernstein("1,2,2") #not a sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateBernstein([1,2,2]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateBernstein([[1,1],[2,1,1],
                                            [2,2]]) #not a proper sequence
    except Exception as err:
        PrintError(err)
    try:
        testmodule.InterpolateBernstein(XYGridNotUnique) #not unique X-Grid
    except Exception as err:
        PrintError(err)

