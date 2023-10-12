#usr/bin/python3
"""
Module math_extra_lib.Tests.DT004_matrix_solver

Implements demonstration testing of the module math_extra_lib.matrix_solver -
specifically the exceptions generation, which are auxilary to the functional
unit tests see TE00 and TE004 documents.
"""

__version__ = "1.0.0.0"
__date__ = "12-10-2023"
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

import math_extra_lib.matrix_solver as testmodule

#helper functions

def PrintError(Error: Exception) -> None:
    print(Error.__class__.__name__, ':', Error)
    if hasattr(Error, 'Traceback'):
        print(Error.Traceback.Info)

#test area

if __name__=='__main__':
    print('Demonstration test DT004 - power iteration and linear system.')
    print('Power iteration method for eigenvalues...')
    Matrix = testmodule.SquareMatrix([[1, 1], [0, 2]])
    print(f'Matrix: {Matrix} - fast convergence')
    Eigenvalue = testmodule.FindEigenvector(Matrix)
    print(f'Eigenvalue is {Eigenvalue}')
    del Matrix
    Matrix = testmodule.SquareMatrix([[1, 1], [0, 1]])
    print(f'Matrix: {Matrix} - slow convergence')
    Eigenvalue = testmodule.FindEigenvector(Matrix)
    print(f'Eigenvalue is {Eigenvalue}')
    del Matrix
    input('Press "Enter"')
    #solution of the linear equations system
    #+ {  2x + y -  z = 8
    #+ { -3x - y + 2z = -11
    #+ { -2x + y + 2z = -3
    #+
    #+ solution is x = 2, y = 3, z = -1
    print('Solution of a system of linear equations')
    Matrix = testmodule.SquareMatrix([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]])
    FreeColumn = testmodule.Column(8, -11, -3)
    print(f'Bound coefficients matrix {Matrix}')
    print(f'Free coefficients column {FreeColumn}')
    Solution = testmodule.SolveLinearSystem(Matrix, FreeColumn)
    print(f'Solution is {Solution}')
    Solution = testmodule.Column(*Solution)
    print(f'Control: Matrix * Solution = {Matrix * Solution}')
    del Matrix
    del Solution
    del FreeColumn
    input('Press "Enter"')
    print('Demonstration of sanity checks and exceptions...')
    #only instances of SquareMatrix are allowed
    try:
        testmodule.FindEigenvector([[1, 1], [0, 1]])
    except Exception as err:
        PrintError(err)
    input('Press "Enter"')
    #second argument is not a flat sequence of real numbers or Column instance
    try:
        testmodule.SolveLinearSystem([[1, 1], [0, 1]], [1, "1"])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SolveLinearSystem([[1, 1], [0, 1]], [1, [1]])
    except Exception as err:
        PrintError(err)
    input('Press "Enter"')
    #first argument is not flat / nested uniform real sequence nor SquareMatrix
    try:
        testmodule.SolveLinearSystem([[1, 1], [0, "1"]], [1, 1])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SolveLinearSystem([[1, 1], 0, 1], [1, 1])
    except Exception as err:
        PrintError(err)
    input('Press "Enter"')
    #first argument does not represent a proper square matrix (as an array)
    try:
        testmodule.SolveLinearSystem([[1, 1], [0, 1], [1, 1]], [1, 1])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SolveLinearSystem([[1, 1], [0, 1, 1]], [1, 1])
    except Exception as err:
        PrintError(err)
    input('Press "Enter"')
    #matrix vs column size mismatch
    try:
        testmodule.SolveLinearSystem([[1, 1], [0, 1]], [1])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SolveLinearSystem([[1, 1], [0, 1]], [1, 1, 1])
    except Exception as err:
        PrintError(err)
    #the next one is ok!
    print(testmodule.SolveLinearSystem([[1, 1], [0, 1]], [2, 1]))