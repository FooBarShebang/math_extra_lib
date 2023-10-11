#usr/bin/python3
"""
Module math_extra_lib.matrix_solver.

Imlements power iteration method for finding an eigenvector of a matrix, and
solution of a determined system of linear equations.

Functions:
    FindEigenvector
    SolveLinearSystem
"""

__version__= '1.0.0.0'
__date__ = '11-10-2023'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import collections.abc as c_abc

#from math import sqrt, floor
from typing import Sequence, Union, List

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

from math_extra_lib.vectors_matrices import Column, SquareMatrix
from math_extra_lib.vectors_matrices import _CheckIfRealSequence

#types

TReal = Union[int, float]

TRealSequence = Sequence[TReal]

TNestedSequence = Sequence[TRealSequence]

#functions

def FindEigenvector(Matrix: SquareMatrix) -> Union[TReal, None]:
    """
    Finds a real number eigenvalue of a square matrix using the power iteration
    method. The found eigenvalue, if found, is most likely the highest absolute
    value one. It is possible (but highly unlikely) that the initial guess
    vector is in the eigenspace of a non-dominant eigenvalue, in which case the
    found eigenvalue is not the largest by the amplitude.
    
    Signature:
        SquareMatrix -> int OR float OR None
    
    Args:
        Matrix: SquareMatrix; instance of the class implementing a square matrix
    
    Returns:
        int OR float: the found eigenvalue
        None: the matrix has no real number eigenvalue
    
    Raises:
        UT_TypeError: the passed argument is not an instance of SquareMatrix
            class
    
    Version 1.0.0.0
    """
    if not isinstance(Matrix, SquareMatrix):
        raise UT_TypeError(Matrix, SquareMatrix, SkipFrames = 1)

def SolveLinearSystem(
        BoundCoeffs: Union[SquareMatrix, TNestedSequence, TRealSequence],
        FreeCoeffs: Union[Column, TRealSequence]) -> Union[List[TReal], None]:
    """
    Solves a system of linear equations using Gauss-Jordan elimination with
    rows / columns pivoting (LUP-decomposition) and back-substition.
    
    Signature:
        SquareMatrix OR seq(seq(int OR float)) OR seq(int OR float),
            Column OR seq(int OR float) -> list(int OR float) OR None
    
    Args:
        BoundCoeffs: SquareMatrix OR seq(seq(int OR float)) OR seq(int OR float)
            ; the matrix of the bound coefficients of the system in the
            row-first order
        FreeCoeffs: Column OR seq(int OR float); the free coefficients of the
            system
    
    Returns:
        list(int OR float): the found solution of the system
        None: the system is undertermined (no solution or multiple solutions)
    
    Raises:
        UT_TypeError: the first argument is neigther an instance of SquareMatrix
            class nor a flat or nested sequence of real numbers, OR the second
            argument is neigther an instance of Column class nor a flat
            sequence of real numbers
        UT_ValueError: the content of the first argument (as a sequence) is
            incompatible with the initilization method of SquareMatrix class,
            OR the second argument (as a sequence) has less than 2 elements, OR
            the size of the free coefficients vector does not match the size of
            the bound coefficients matrix
    
    Version 1.0.0.0
    """
    if not isinstance(BoundCoeffs, SquareMatrix):
        try:
            _Matrix = SquareMatrix(BoundCoeffs)
        except UT_TypeError as err:
            Error = UT_TypeError(BoundCoeffs, SquareMatrix, SkipFrames = 1)
            Error.setMessage(err.getMessage)
            raise Error from None
        except UT_ValueError as err1:
            Error = UT_ValueError(BoundCoeffs, 'whatever', SkipFrames = 1)
            Error.setMessage(err1.getMessage)
            raise Error from None
    else:
        _Matrix = BoundCoeffs
    if not isinstance(FreeCoeffs, Column):
        try:
            _CheckIfRealSequence(FreeCoeffs)
        except UT_TypeError as err:
            Error = UT_TypeError(FreeCoeffs, Column, SkipFrames = 1)
            Error.setMessage(err.getMessage)
            raise Error from None
        _Column = list(FreeCoeffs)
    else:
        _Column = FreeCoeffs.Data
    if len(_Column) != _Matrix.Size:
        raise UT_ValueError(len(_Column),
                            f'={_Matrix.Size} - mismatching sizes',
                                                                SkipFrames = 1)
    #