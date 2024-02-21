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
__date__ = '20-02-2024'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import List, Union, Sequence, Tuple, Any

from math import sqrt, pi
from cmath import rect
from random import random

from collections.abc import Sequence as GSequence

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

TCoordinates = Tuple[TReal, TReal] #replace by Annotated[Sequence[TReal], 2]
# in Python 3.9 and later

TGrid = Sequence[TCoordinates]

#globals

MAX_ITER = 1000 #1E3, maximum number of power iteration

ALMOST_ZERO = 1.0E-12 #rounding precision threshold for calculations

ROOTS_PRECISION = 1.0E-4 #precision of the found roots rounding

NOT_SEQUENCE = (str, bytes, bytearray)

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

def _ReducePolynomialDegree(Poly: Polynomial) -> Union[Polynomial, TReal]:
    """
    Reduces the degree of an interpolation polynomial, which can be higher than
    expected due to rounding error. This process reduces the oscillation effect,
    than the fitted X-Y values series is produced by a polynomial of a lower
    degree.
    
    Signature:
        Polynomial -> Polynomial OR int OR float
    
    Args:
        Poly: Polynomial; calcualted interpolation polynomial
    
    Returns:
        Polynomial OR int OR float: polynomial of the same or lower degree, or
            even a real number (0-th degree)
    
    Version 1.0.0.0
    """
    Coefficients = list(Poly.getCoefficients()) #from 0-th degree upwards
    while len(Coefficients):
        if abs(Coefficients[-1]) < ALMOST_ZERO:
            Coefficients.pop()
        else:
            break
    if not len(Coefficients):
        Result = 0
    elif len(Coefficients) == 1:
        Result = Coefficients[0]
    else:
        Result = Polynomial(*Coefficients)
    return Result

def _CheckXYGrid(Value: Any, *, SkipFrames : int = 2) -> None:
    """
    Helper function to perform a routine check if the received argument is a
    sequence of 2-element sub-sequences of real numbers, representing an X-Y
    grid with unique X values.
    
    Signature:
        type A/, *, int > 0/ -> None
    
    Args:
        Value: type A; the parameter to be checked
        SkipFrame: (keyword) int > 0; a number of frames to be hidden in the
            raised exceptions, defaults to 2 as this function is supposed to
            be called from another function or method
    
    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a sequence (nested) of real numbers (int or float),
            OR a length of any of the sub-sequence is not 2
        UT_ValueError: the passed argument is empty or contains only 1 element,
            OR any of the X values is not unique (first element of the
            sub-sequences)
    
    Version 1.0.0.0
    """
    if ((not isinstance(Value, GSequence))
                                or isinstance(Value, (str, bytes, bytearray))):
        raise UT_TypeError(Value, (list, tuple), SkipFrames = SkipFrames)
    for Index, Item in enumerate(Value):
        if ((not isinstance(Item, GSequence)) or
                                    isinstance(Item, (str, bytes, bytearray))):
            Error = UT_TypeError(Item, (list, tuple), SkipFrames = SkipFrames)
            Error.appendMessage(f'item index {Index} in {Value}')
            raise Error
        if len(Item) != 2:
            Error = UT_TypeError(Item, list, SkipFrames = SkipFrames)
            Error.setMessage(' '.join([f'{Item} at index {Index} in {Value}',
                                       'is not of the length 2']))
            raise Error
        for SubIndex, Coordinate in enumerate(Item):
            if ((not isinstance(Coordinate, (int, float))) or
                                                isinstance(Coordinate, bool)):
                Error = UT_TypeError(Coordinate, (int, float),
                                                        SkipFrames = SkipFrames)
                Error.appendMessage(' '.join([f'item index {SubIndex} in',
                                                f'sub-sequence index {Index}',
                                                                f'in {Value}']))
                raise Error
    NumberPoints = len(Value)
    if NumberPoints < 2:
        raise UT_ValueError(NumberPoints, '== 2, number of points',
                                                        SkipFrames = SkipFrames)
    Nodes = []
    for x, _ in Value:
        if not (x in Nodes):
            Nodes.append(x)
        else:
            raise UT_ValueError(x, f'unique node x-value in {Value}',
                                                        SkipFrames = SkipFrames)

def _CheckDegree(Value: Any, *, SkipFrames : int = 2) -> None:
    """
    Helper function to perform a routine check if the received argument is a
    non-negative integer number (polynomial degree)
    
    Signature:
        type A/, *, int > 0/ -> None
    
    Args:
        Value: type A; the parameter to be checked
        SkipFrame: (keyword) int > 0; a number of frames to be hidden in the
            raised exceptions, defaults to 2 as this function is supposed to
            be called from another function or method
    
    Raises:
        UT_TypeError: the passed argument is not an integer number
        UT_ValueError: the passed argument is a negative integer number
    
    Version 1.0.0.0
    """
    if (not isinstance(Value, int)) or isinstance(Value, bool):
        raise UT_TypeError(Value, int, SkipFrames = SkipFrames)
    if Value < 0:
        raise UT_ValueError(Value, '>= 0', SkipFrames = SkipFrames)

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
    Calculates a single base Lagrange polynomial, which evaluates to 1 at the
    provided node x-value and to 0 at all passed N roots (x-values).
    
    Signature:
        int OR float, seq(int OR float) -> Polynomial
    
    Args:
        Node: int OR float; the x-value, at which the polynomial evaluates to 1
        Roots: seq(int OR float); sequence of real numbers (x-values), at which
            the polynomial evaluates to 0
    
    Returns:
        Polynomial: instance of, a polynomial of degree N, where N is the number
            of the roots
    
    Raises:
        UT_TypeError: the first argument is not a real number, OR the second
            argument is not a sequence of real numbers
        UT_ValueError: roots sequence is empty, OR it contains, at least,
            2 equal elements
    
    Version 1.0.0.0
    """
    if (not isinstance(Node, (int, float))) or isinstance(Node, bool):
        raise UT_TypeError(Node, (int, float), SkipFrames = 1)
    if (not isinstance(Roots, GSequence)) or isinstance(Roots, NOT_SEQUENCE):
        raise UT_TypeError(Roots, (list, tuple), SkipFrames = 1)
    for Index, NewRoot in enumerate(Roots):
        if (not isinstance(NewRoot, (int, float))) or isinstance(NewRoot, bool):
            Error = UT_TypeError(NewRoot, (int, float), SkipFrames = 1)
            Error.appendMessage(f' at index {Index} in {Roots}')
            raise Error
    NumberOfRoots = len(Roots)
    if NumberOfRoots < 1:
        raise UT_ValueError(NumberOfRoots, '>= 1 - number of roots',
                                                                SkipFrames = 1)
    _Roots = list()
    for Index, NewRoot in enumerate(Roots):
        if NewRoot in _Roots:
            raise UT_ValueError(NewRoot, f'unique root in {Roots}',
                                                                SkipFrames = 1)
        if NewRoot == Node:
            raise UT_ValueError(NewRoot,
                                f'root <> node at index {Index} in {Roots}',
                                                                SkipFrames = 1)
        _Roots.append(NewRoot)
    Scaling = 1
    for Root in _Roots:
        Scaling *= Node - Root
    Result = Polynomial.fromRoots(*_Roots) / Scaling
    return Result

def GetLagrangeBasis(XGrid: Sequence[TReal]) -> List[Polynomial]:
    """
    Calculates N base Lagrange base polynomials of the degree N-1 for the passed
    N unique x-values (nodes).
    
    Signature:
        seq(int OR float) -> list(Polynomial)
    
    Args:
        XGrid: seq(int OR float); sequence of unique real numbers
    
    Returns:
        list(Polynomial): list of instances of Polynomial class - the base
            Lagrange polynomials
    
    Raises:
        UT_TypeError: the passed argument is not a sequence of real numbers
        UT_ValueError: the passed sequence contains less than 2 elements, OR,
            at least, two elements are equal
    
    Version 1.0.0.0
    """
    if (not isinstance(XGrid, GSequence)) or isinstance(XGrid, NOT_SEQUENCE):
        raise UT_TypeError(XGrid, (list, tuple), SkipFrames = 1)
    for Index, Value in enumerate(XGrid):
        if (not isinstance(Value, (int, float))) or isinstance(Value, bool):
            Error = UT_TypeError(Value, (int, float), SkipFrames = 1)
            Error.appendMessage(f' at index {Index} in {XGrid}')
            raise Error
    NumberNodes = len(XGrid)
    if NumberNodes < 2:
        raise UT_ValueError(NumberNodes, '>= 2 - number of nodes')
    _Roots = list()
    for Index, NewRoot in enumerate(XGrid):
        if NewRoot in _Roots:
            raise UT_ValueError(NewRoot, f'unique root in {XGrid}',
                                                                SkipFrames = 1)
        _Roots.append(NewRoot)
    Result = list()
    for Index, Node in enumerate(XGrid):
        if not Index:
            Roots = XGrid[1 : ]
        elif Index == NumberNodes - 1:
            Roots = XGrid[ : -1]
        else:
            Roots = XGrid[ : Index]
            Roots.extend(XGrid[Index + 1 : ])
        Result.append(GetLagrangePolynomial(Node, Roots))
    return Result

def InterpolateLagrange(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Calculates an interpolatig polynomial of degree <= N - 1, where N is the
    number of (X,Y) data points provided. The calculated polynomial goes
    (almost) exactly through each of the provided data points. A constant
    function (0-th degree polynomial) is represented by a real number, higher
    degrees - by an instance of the math_extra_lib.polynomial.Polynomial class.
    Lagrange polynomial basis is used in the calculations.
    
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    
    Returns:
        Polynomial: instance of, interpolating polynomial of degree 1 or higher
        int OR float: interpolating function is constant (0-th degree)
    
    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a sequence (nested) of real numbers (int or float),
            OR a length of any of the sub-sequence is not 2
        UT_ValueError: the passed argument is empty or contains only 1 element,
            OR any of the X values is not unique (first element of the
            sub-sequences)
    
    Version 1.0.0.0
    """
    _CheckXYGrid(XYGrid)
    XGrid, YGrid = zip(*XYGrid)
    Basis = GetLagrangeBasis(list(XGrid))
    PolynomialSum = sum(y * BasePolynomial for y, BasePolynomial in
                                                            zip(YGrid, Basis))
    Result = _ReducePolynomialDegree(PolynomialSum)
    del PolynomialSum
    return Result

def GetLegendrePolynomial(Degree: int) -> Union[Polynomial, int]:
    """
    Calculates a single Legendre polynomial of degree N >= 0.
    
    Signature:
        int >= 0 -> Polynomial OR int
    
    Args:
        Degree: int >= 0; the requested degree of the polynomial
    
    Returns:
        Polynomial: instance of, degree > 0
        int: value = 1, degree is 0
    
    Raises:
        UT_TypeError: the passed argument is not an integer number
        UT_ValueError: the passed argument is a negative integer number
    
    Version 1.0.0.0
    """
    _CheckDegree(Degree)
    if not Degree:
        Result = 1
    elif Degree == 1:
        Result = Polynomial(0, 1)
    else:
        Next2Last = [0, 1]
        Last = [1]
        FoundDegree = 1
        while FoundDegree < Degree:
            Coefficient = (2 * FoundDegree + 1) / (FoundDegree + 1)
            Next = [Coefficient * Item for Item in Next2Last]
            Next.insert(0, 0)
            Coefficient = - FoundDegree / (FoundDegree + 1)
            for Index, Item in enumerate(Last):
                Next[Index] += Coefficient * Item
            del Last
            Last = Next2Last
            Next2Last = Next
            FoundDegree += 1
        Result = Polynomial(*Next)
        del Last
        del Next2Last
        del Next
    return Result

def GetLegendreBasis(Degree: int) -> List[Union[Polynomial, int]]:
    """
    Calculates a complete Legendre polynomial base of degree N >= 0.
    
    Signature:
        int >= 0 -> list(Polynomial OR int)
    
    Args:
        Degree: int >= 0; the requested degree of the basis
    
    Returns:
        list(Polynomial OR int): the basis, where the first element is always 1,
            and each subsequent element is an instance of polynomial class of
            the degree equal to the element index
    
    Raises:
        UT_TypeError: the passed argument is not an integer number
        UT_ValueError: the passed argument is a negative integer number
    
    Version 1.0.0.0
    """
    _CheckDegree(Degree)

def InterpolateLegendre(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Calculates an interpolatig polynomial of degree <= N - 1, where N is the
    number of (X,Y) data points provided. The calculated polynomial goes
    (almost) exactly through each of the provided data points. A constant
    function (0-th degree polynomial) is represented by a real number, higher
    degrees - by an instance of the math_extra_lib.polynomial.Polynomial class.
    Legendre polynomial basis is used in the calculations.
    
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    
    Returns:
        Polynomial: instance of, interpolating polynomial of degree 1 or higher
        int OR float: interpolating function is constant (0-th degree)
    
    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a sequence (nested) of real numbers (int or float),
            OR a length of any of the sub-sequence is not 2
        UT_ValueError: the passed argument is empty or contains only 1 element,
            OR any of the X values is not unique (first element of the
            sub-sequences)
    
    Version 1.0.0.0
    """
    _CheckXYGrid(XYGrid)

def GetChebyshevPolynomial(Degree: int) -> Union[Polynomial, int]:
    """
    Calculates a single Chebyshev polynomial (of the 1st kind) of degree N >= 0.
    
    Signature:
        int >= 0 -> Polynomial OR int
    
    Args:
        Degree: int >= 0; the requested degree of the polynomial
    
    Returns:
        Polynomial: instance of, degree > 0
        int: value = 1, degree is 0
    
    Raises:
        UT_TypeError: the passed argument is not an integer number
        UT_ValueError: the passed argument is a negative integer number
    
    Version 1.0.0.0
    """
    _CheckDegree(Degree)
    if not Degree:
        Result = 1
    elif Degree == 1:
        Result = Polynomial(0, 1)
    else:
        Next2Last = [0, 1]
        Last = [1]
        FoundDegree = 1
        while FoundDegree < Degree:
            Next = [2 * Item for Item in Next2Last]
            Next.insert(0, 0)
            for Index, Item in enumerate(Last):
                Next[Index] -= Item
            del Last
            Last = Next2Last
            Next2Last = Next
            FoundDegree += 1
        Result = Polynomial(*Next)
        del Last
        del Next2Last
        del Next
    return Result

def GetChebyshevBasis(Degree: int) -> List[Union[Polynomial, int]]:
    """
    Calculates a complete Chebyshev polynomial base of degree N >= 0 (of the 1st
    kind).
    
    Signature:
        int >= 0 -> list(Polynomial OR int)
    
    Args:
        Degree: int >= 0; the requested degree of the basis
    
    Returns:
        list(Polynomial OR int): the basis, where the first element is always 1,
            and each subsequent element is an instance of polynomial class of
            the degree equal to the element index
    
    Raises:
        UT_TypeError: the passed argument is not an integer number
        UT_ValueError: the passed argument is a negative integer number
    
    Version 1.0.0.0
    """
    _CheckDegree(Degree)

def InterpolateChebyshev(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Calculates an interpolatig polynomial of degree <= N - 1, where N is the
    number of (X,Y) data points provided. The calculated polynomial goes
    (almost) exactly through each of the provided data points. A constant
    function (0-th degree polynomial) is represented by a real number, higher
    degrees - by an instance of the math_extra_lib.polynomial.Polynomial class.
    Chebyshev polynomial basis is used in the calculations.
    
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    
    Returns:
        Polynomial: instance of, interpolating polynomial of degree 1 or higher
        int OR float: interpolating function is constant (0-th degree)
    
    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a sequence (nested) of real numbers (int or float),
            OR a length of any of the sub-sequence is not 2
        UT_ValueError: the passed argument is empty or contains only 1 element,
            OR any of the X values is not unique (first element of the
            sub-sequences)
    
    Version 1.0.0.0
    """
    _CheckXYGrid(XYGrid)


def GetBernsteinPolynomial(Degree: int, Index: int) -> Union[Polynomial, int]:
    """
    Calculates a single Bernstein polynomial of degree N >= 0 and index K, where
    0 <= K <= N.
    
    Signature:
        int >= 0 -> Polynomial OR int
    
    Args:
        Degree: int >= 0; the requested degree of the polynomial
        Index: int >= 0; the requested index, should not exceed the degree
    
    Returns:
        Polynomial: instance of, degree > 0
        int: value = 1, degree is 0
    
    Raises:
        UT_TypeError: the first passed argument is not an integer number, OR the
            second argument is not an integer number
        UT_ValueError: the passed argument is a negative integer number, OR the
            second argument is a negative integer number, OR the second argument
            is greater than the first
    
    Version 1.0.0.0
    """
    _CheckDegree(Degree)
    _CheckDegree(Index)
    if Index > Degree:
        raise UT_ValueError(Index,
                f'<= {Degree}, index should not exceed degree', SkipFrames = 1)

def GetBernsteinBasis(Degree: int) -> Union[List[Polynomial], List[int]]:
    """
    Calculates a complete Bernstein polynomial base of degree N >= 0.
    
    Signature:
        int >= 0 -> list(Polynomial OR int)
    
    Args:
        Degree: int >= 0; the requested degree of the basis
    
    Returns:
        list(Polynomial OR int): the basis, for the Degree 0 it is [1],
            otherwise it contains N=Degree Polynomial class instances, each
            being a polynomial of degree = Degree
    
    Raises:
        UT_TypeError: the passed argument is not an integer number
        UT_ValueError: the passed argument is a negative integer number
    
    Version 1.0.0.0
    """
    _CheckDegree(Degree)

def InterpolateBernstein(XYGrid: TGrid) -> Union[Polynomial, TReal]:
    """
    Calculates an interpolatig polynomial of degree <= N - 1, where N is the
    number of (X,Y) data points provided. The calculated polynomial goes
    (almost) exactly through each of the provided data points. A constant
    function (0-th degree polynomial) is represented by a real number, higher
    degrees - by an instance of the math_extra_lib.polynomial.Polynomial class.
    Bernstein polynomial basis is used in the calculations.
    
    Signature:
        seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float
    
    Returns:
        Polynomial: instance of, interpolating polynomial of degree 1 or higher
        int OR float: interpolating function is constant (0-th degree)
    
    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a sequence (nested) of real numbers (int or float),
            OR a length of any of the sub-sequence is not 2
        UT_ValueError: the passed argument is empty or contains only 1 element,
            OR any of the X values is not unique (first element of the
            sub-sequences)
    
    Version 1.0.0.0
    """
    _CheckXYGrid(XYGrid)
