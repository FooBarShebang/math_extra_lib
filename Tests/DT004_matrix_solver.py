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
    Matrix = testmodule.SquareMatrix([[1, 1], [0, 1]])
    Eigenvalue = testmodule.FindEigenvector(Matrix)
    print(Eigenvalue)