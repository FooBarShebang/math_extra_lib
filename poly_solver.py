#usr/bin/python3
"""
Module math_extra_lib.poly_solver.

Implements Aberth method for finding all roots of a polynomial and polynomial
interpolation using Lagrange, Legende, Chebyshev and Bernstein basis.

Functions:
    FindRoots(Poly)
        Polynomial -> list(int OR floar OR complex)
    GetLagrangePolynomial(Node, Roots)
        int OR float, seq(int OR float) -> Polynomial
    GetLagrangeBasis(XGrid)
        seq(int OR float) -> list(Polynomial)
    InterpolateLagrange(XYGrid)
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    GetLegendrePolynomial(Degree)
        int >= 0 -> Polynomial OR int
    GetLegendreBasis(Degree)
        int >= 0 -> list(Polynomial OR int)
    InterpolateLegendre(XYGrid)
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    GetChebyshevPolynomial(Degree)
        int >= 0 -> Polynomial OR int
    GetChebyshevBasis(Degree)
        int >= 0 -> list(Polynomial OR int)
    InterpolateChebyshev(XYGrid)
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    GetBernsteinPolynomial(Degree, Index)
        int >= 0, int >= 0 -> Polynomial OR int
    GetBernsteinBasis(Degree)
        int >= 0 -> list(Polynomial) OR list(int)
    InterpolateBernstein(XYGrid)
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
"""

__version__= '1.0.0.0'
__date__ = '03-11-2023'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import List, Union, Sequence, Tuple

from math import sqrt, pi
from cmath import rect
from random import random

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

from math_extra_lib.polynomial import Polynomial
from math_extra_lib.matrix_solver import SolveLinearSystem

#types

TReal = Union[int, float]

TNumber = Union[int, float, complex]

TCoordinates = Tuple[TReal, TReal]

TGrid = Sequence[TCoordinates]

#globals

MAX_ITER = 1000 #1E3, maximum number of power iteration

ALMOST_ZERO = 1.0E-12 #rounding precision threshold for calculations

ROOTS_PRECISION = 1.0E-4 #precision of the found roots rounding

#functions

#+ private helper functions

def _RoundAndConvert(Value: TNumber, *,
                                Precision: float = ALMOST_ZERO) -> TNumber:
    """
    Performs complex -> real number conversion and rounding to integer if
    possible.
    
    Signature:
        int OR float OR complex /, float/ -> int OR floar OR complex
    
    Args:
        Value: int OR float OR complex; the value to be rounded and converted if
            needed
        Precision: (keyword) float; the desired precision of float -> int
            rounding, defaults to ALMOST_ZERO constant
    
    Version 1.0.0.0
    """
    if isinstance(Value, complex):
        if abs(Value.imag) < Precision:
            Result = Value.real
            if abs(Result - round(Result)) < Precision:
                Result = round(Result)
        else:
            RealPart = Value.real
            ImagPart = Value.imag
            if abs(RealPart - round(RealPart)) < Precision:
                RealPart = round(RealPart)
            if abs(ImagPart - round(ImagPart)) < Precision:
                ImagPart = round(ImagPart)
            Result = complex(RealPart, ImagPart)
    else:
        if abs(Value - round(Value)) < Precision:
            Result = round(Value)
        else:
            Result = Value
    return Result

def _GenerateBinomialCoefficients(Power: int) -> List[int]:
    """
    Generates a list of all binomial coefficients for the specified power.
    
    Signature:
        int >= 0 -> list(int >= 1)
    
    Raises:
        UT_TypeError: passed argument is not an integer number
        UT_ValueError: passed argument is a negative integer number
    
    Version 1.0.0.0
    """
    if not isinstance(Power, int):
        raise UT_TypeError(Power, int, SkipFrames = 1)
    if Power < 0:
        raise UT_ValueError(Power, '>= 0', SkipFrames = 1)
    Result = [1 for _ in range(Power + 1)]
    if Power > 1:
        Half = Power // 2
        Previous = Result[0]
        for Index in range(Half):
            Next = (Previous * (Power - Index)) // (Index + 1)
            Result[Index + 1] = Next
            Result[Power - Index - 1] = Next
            Previous = Next
    return Result

def _GetDerivative(Coefficients: List[TNumber]) -> List[TNumber]:
    """
    Calculates a derivative of a polynomial using only list of the coefficients
    (zero to the highest power order sorted) without using the actual polynomial
    class implementation.
    
    Signature:
        list(int OR floar OR complex) -> list(int OR floar OR complex)
    
    Raises:
        UT_TypeError: the passed argument is not a list of real or complex
            numbers
        UT_ValueError: the passed list has less than 2 elements
    
    Version 1.0.0.0
    """
    if not isinstance(Coefficients, list):
        raise UT_TypeError(Coefficients, list, SkipFrames = 1)
    Length = len(Coefficients)
    if Length < 2:
        raise UT_ValueError(Length, '>1 - length of the list', SkipFrames = 1)
    Result = list()
    for Index, Item in enumerate(Coefficients):
        if not isinstance(Item, (int, float, complex)):
            Error = UT_TypeError(Item, (int, float, complex), SkipFrames = 1)
            Error.appendMessage(f'at index {Index} in the passed list')
            raise Error
        Result.append(Index * Item)
    del Result[0]
    return Result

def _EvaluatePolynomial(Coefficients: List[TNumber], Value: TNumber, *,
                        DoNotRound = False) -> TNumber:
    """
    Evaluates a generic polynomial (even with the complex coefficients) at any
    value of its argument (including complex values).
    
    Signature:
        list(int OR floar OR complex), int OR floar OR complex /, bool/
            -> int OR floar OR complex
    
    Args:
        Coefficients: list(int OR floar OR complex); coefficients of a
            polynomial to be evaluated, from zero to N-th power
        Value: int OR floar OR complex; value of the argument
        DoNotRound: (keyword) bool; flag if the calcualted value should be
            rounded and / or converted from complex to real, defaults to False
    
    Raises:
        UT_TypeError: the passed first argument is not a list of real or complex
            number, OR the second argument is not a real or complex number
        UT_ValueError: the passed list has less than 2 elements
    
    Version 1.0.0.0
    """
    if not isinstance(Coefficients, list):
        raise UT_TypeError(Coefficients, list, SkipFrames = 1)
    Length = len(Coefficients)
    if Length < 2:
        raise UT_ValueError(Length, '>1 - length of the list', SkipFrames = 1)
    for Index, Item in enumerate(Coefficients):
        if not isinstance(Item, (int, float, complex)):
            Error = UT_TypeError(Item, (int, float, complex), SkipFrames = 1)
            Error.appendMessage(f'at index {Index} in the passed list')
            raise Error
    if not isinstance(Value, (int, float, complex)):
        Error = UT_TypeError(Value, (int, float, complex), SkipFrames = 1)
        Error.appendMessage(f'argument of a polynomial')
        raise Error
    Evaluated = Coefficients[-1]
    for Index in range(Length - 2, -1, -1):
        Evaluated = Coefficients[Index] + Value * Evaluated
    if DoNotRound:
        Result = Evaluated
    else:
        Result = _RoundAndConvert(Evaluated)
    if isinstance(Evaluated, complex):
        del Evaluated
    return Result

def _ReduceByRoot(Coefficients: List[TNumber], Root: TNumber) -> List[TNumber]:
    """
    Reduces a polynomial by removing one of its roots (in the factorized form).
    
    Signature:
        list(int OR floar OR complex), int OR floar OR complex
            -> list(int OR floar OR complex)
    
    Raises:
        UT_TypeError: the passed first argument is not a list of real or complex
            number, OR the second argument is not a real or complex number
        UT_ValueError: the passed list has less than 3 elements, OR the passed
            second argument is not a root
    
    Version 1.0.0.0
    """
    if not isinstance(Coefficients, list):
        raise UT_TypeError(Coefficients, list, SkipFrames = 1)
    Length = len(Coefficients)
    if Length < 3:
        raise UT_ValueError(Length, '>2 - length of the list', SkipFrames = 1)
    for Index, Item in enumerate(Coefficients):
        if not isinstance(Item, (int, float, complex)):
            Error = UT_TypeError(Item, (int, float, complex), SkipFrames = 1)
            Error.appendMessage(f'at index {Index} in the passed list')
            raise Error
    if not isinstance(Root, (int, float, complex)):
        Error = UT_TypeError(Root, (int, float, complex), SkipFrames = 1)
        Error.appendMessage(f'passed root value')
        raise Error
    Reduced = [Coefficients[-1]]
    for Element in reversed(Coefficients[1:-1]):
        NewElement = Element + Root * Reduced[0]
        Reduced.insert(0, _RoundAndConvert(NewElement))
    Remainder = Coefficients[0] + Root * Reduced[0]
    if abs(Remainder) > 2 * ALMOST_ZERO:
        raise UT_ValueError(Root, 'is a root', SkipFrames = 1)
    return Reduced

def _FindAllRoots(Coefficients: List[TNumber]) -> List[TNumber]:
    """
    Actual function performing the calculation of all roots of a polynomial
    passed as a list of coefficients using a modified Aberth method. The
    introduced modification concerns roots with multiplicity > 1. The found
    roots are returned as a list of complex or real numbers.
    
    Signature:
        list(int OR floar OR complex) -> list(int OR floar OR complex)
    
    Raises:
        UT_TypeError: the passed argument is not a list of real or complex
            number
        UT_ValueError: the passed list has less than 2 elements, OR the highest
            power coefficient is not 1.
    
    Version 1.0.0.0
    """
    if not isinstance(Coefficients, list):
        raise UT_TypeError(Coefficients, list, SkipFrames = 1)
    Length = len(Coefficients)
    if Length < 2:
        raise UT_ValueError(Length, '>1 - length of the list', SkipFrames = 1)
    for Index, Item in enumerate(Coefficients):
        if not isinstance(Item, (int, float, complex)):
            Error = UT_TypeError(Item, (int, float, complex), SkipFrames = 1)
            Error.appendMessage(f'at index {Index} in the passed list')
            raise Error
    if Coefficients[-1] != 1:
        raise UT_ValueError(Coefficients[-1], '=1 - highest power coefficient',
                                                                SkipFrames = 1)
    if Length == 2:
        Roots = [-Coefficients[0]]
    elif Length == 3:
        p = Coefficients[1]
        q = Coefficients[0]
        Determinant = p*p - 4 * q
        if Determinant >= 0:
            Roots = [_RoundAndConvert(-0.5 * p + 0.5 * sqrt(Determinant)),
                        _RoundAndConvert(-0.5 * p - 0.5 * sqrt(Determinant))]
        else:
            Roots = [_RoundAndConvert(complex(-0.5*p, 0.5*sqrt(-Determinant))),
                    _RoundAndConvert(complex(-0.5*p, -0.5*sqrt(-Determinant)))]
    else: #actual Aberth method
        Derivative = _GetDerivative(Coefficients)
        Radius= 1 + max([abs(Coefficient) for Coefficient in Coefficients[:-1]])
        phi = 2 * pi / (Length-1)
        Guesses = [rect(Radius, phi * Index) for Index in range(Length - 1)]
        for _ in range(MAX_ITER):
            Displacements = list()
            FoundAll = False
            for Index, Guess in enumerate(Guesses):
                P_Value = _EvaluatePolynomial(Coefficients, Guess,
                                                            DoNotRound = True)
                D_Value = _EvaluatePolynomial(Derivative, Guess,
                                                            DoNotRound = True)
                if (not P_Value) and D_Value: #found a precise single root
                    Shift = 0
                elif (not P_Value) and (not D_Value): #found a multiple root
                    #this is just a precaution against unlucky guess
                    #+ the algorithm should not normally go to this branch
                    Guesses = [Guess]
                    Reduced = list(Coefficients)
                    while len(Reduced) > 2:
                        Reduced = _ReduceByRoot(Reduced, Guess)
                        CheckNotRoot = _EvaluatePolynomial(Reduced, Guess,
                                                            DoNotRound = True)
                        if not CheckNotRoot:
                            Guesses.append(Guess)
                        else:
                            break
                    if len(Reduced) == 2:
                        Guesses.append(-Reduced[0])
                    else:
                        Guesses.extend(_FindAllRoots(Reduced))
                    FoundAll = True
                    break
                elif P_Value and (not D_Value): #found extremum but not a root
                    Shift = - 0.05 * (random() + 0.1)
                else:
                    Ratio = P_Value / D_Value
                    Weight = sum(1/(Guess - Second)
                                    for NewIndex, Second in enumerate(Guesses)
                                                        if NewIndex != Index)
                    Shift = Ratio / (1 - Ratio * Weight)
                Displacements.append(Shift)
            if not FoundAll:
                Guesses = [Guess - Shift
                                for Guess, Shift in zip(Guesses, Displacements)]
            if all(map(lambda x: abs(x) < ALMOST_ZERO / (Length - 1),
                       Displacements)):
                if not any(_EvaluatePolynomial(Coefficients, Guess)
                                                        for Guess in Guesses):
                    break
            elif FoundAll:
                break
        Roots = [_RoundAndConvert(Guess, Precision = ROOTS_PRECISION)
                                                        for Guess in Guesses]
    return Roots

#+ public functions

def FindRoots(Poly: Polynomial) -> List[TNumber]:
    """
    Calculates all roots of a polynomial passed as an instance of Polynomial
    class using Alberth method, and returns them as a list of real or complex
    numbers. Each root with multiplicity K is included exactly K time; thus for
    a polynomial of the degree N the length of the list is exactly N.
    
    Signature:
        Polynomial -> list(int OR floar OR complex)
    
    Raises:
        UT_TypeError: argument is not an instance of Polynomial class
    
    Version 1.0.0.0
    """
    if not isinstance(Poly, Polynomial):
        raise UT_TypeError(Poly, Polynomial, SkipFrames = 1)
    Coefficients = Poly.getCoefficients()
    HighestOrder = Coefficients[-1]
    Coefficients = [Item / HighestOrder for Item in Coefficients]
    Coefficients[-1] = 1
    Result = _FindAllRoots(Coefficients)
    return Result

def GetLagrangePolynomial(Node: TReal, Roots: Sequence[TReal]) -> Polynomial:
    """
    Signature:
        int OR float, seq(int OR float) -> Polynomial
    """
    pass

def GetLagrangeBasis(XGrid: Sequence[TReal]) -> List[Polynomial]:
    """
    Signature:
        seq(int OR float) -> list(Polynomial)
    """
    pass

def InterpolateLagrange(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    """
    pass

def GetLegendrePolynomial(Degree: int) -> Union[Polynomial, int]:
    """
    Signature:
        int >= 0 -> Polynomial OR int
    """
    pass

def GetLegendreBasis(Degree: int) -> List[Union[Polynomial, int]]:
    """
    Signature:
        int >= 0 -> list(Polynomial OR int)
    """
    pass

def InterpolateLegendre(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    """
    pass

def GetChebyshevPolynomial(Degree: int) -> Union[Polynomial, int]:
    """
    Signature:
        int >= 0 -> Polynomial OR int
    """
    pass

def GetChebyshevBasis(Degree: int) -> List[Union[Polynomial, int]]:
    """
    Signature:
        int >= 0 -> list(Polynomial OR int)
    """
    pass

def InterpolateChebyshev(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    """
    pass


def GetBernsteinPolynomial(Degree: int, Index: int) -> Union[Polynomial, int]:
    """
    Signature:
        int >= 0, int >= 0 -> Polynomial OR int
    """
    pass

def GetBernsteinBasis(Degree: int) -> Union[List[Polynomial], List[int]]:
    """
    Signature:
        int >= 0 -> list(Polynomial) OR list(int)
    """
    pass

def InterpolateBernstein(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    """
    pass
