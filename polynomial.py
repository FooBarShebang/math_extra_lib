#usr/bin/python3
"""
Module math_extra_lib.polynomial

Implementation of the polynomials and releated arithmetics.

Classes:
    Polynomial
    RationalFunction
"""

__version__= '1.0.0.0'
__date__ = '20-04-2023'
__status__ = 'Production'

#imports

#+ standard libraries

import sys
import os

import collections.abc as c_abc

from typing import Sequence, Union, Tuple

from math import log2, factorial

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError
from introspection_lib.base_exceptions import UT_IndexError

#types

TReal = Union[int, float]

TRealSequence = Sequence[TReal]

TPolynomial = "Polynomial"

TRealSequencePoly = Union[TRealSequence, TPolynomial]

TRealPoly = Union[TReal, TPolynomial]

TIntPoly = Union[int, TPolynomial]

TRealTuple = Tuple[TReal, ...]

#globals - precission related

NEAR_ZERO_SOFT = 1E-8

NEAR_ZERO_HARD = 1E-12

#classes

class Polynomial:
    """
    Implementation of a polynomial. This class must be instantiated with an
    unpacked sequence of real numbers, which will be set as the coefficients
    from the zero-th to the highest power. The last positional argument of the
    initialization method must be non-zero.
    
    An instance of this class supports index access to the individual
    coefficients (read only) and arithmetical operations with a real number or
    another polynomial.
    
    An instance is also callable returning the value of the polynomial at the
    passed value of the argument.
    
    Properties:
        Degree: (read-only) int >= 1
    
    Class methods:
        fromRoots(*args)
            *tuple(int OR float) -> Polynomial
    
    Methods:
        getCoefficients()
            None -> tuple(int OR float)
        getAntiderivative(Degree = 1)
            /int >= 1/ -> Polynomial OR int OR float
        getAntiderivative()
            None -> Polynomial
        getConvolution(Other)
            Polynomial -> Polynomial
    
    Version 1.0.0.0
    """
    
    #public class methods
    
    @classmethod
    def fromRoots(cls, *args) -> TPolynomial:
        """
        Creates a polynomial from its roots, i.e. performs the inverse of the
        factorization: (x-x_1)*...*(x-x_N) -> a_0 + a_1 * x + a_2 * x^2 + ...
        + a_N * x^N
        
        Signature:
            *seq(int OR float) -> Polynomial
        
        Args:
            *args: *seq(int OR float); any number of integer or floating
                point arguments
        
        Raises:
            UT_TypeError: any of the arguments is not a real number
            UT_ValueError: no arguments are provided
        
        Version 1.0.0.0
        """
        for Index, Value in enumerate(args):
            if not isinstance(Value, (int, float)):
                Error = UT_TypeError(Value, (int, float), SkipFrames = 1)
                Error.appendMessage(f'- argument {Value} at position {Index}')
                raise Error
        if not len(args):
            raise UT_ValueError(len(args), '>= 1 - number of arguments',
                                                                SkipFrames = 1)
        Coefficients = [-args[0], 1]
        for Index in range(1, len(args)):
            NextCoefficients = [-args[Index]*Value for Value in Coefficients]
            Coefficients.insert(0,0)
            for Position, Value in enumerate(NextCoefficients):
                Coefficients[Position] += Value
        return cls(*Coefficients)
    
    #special methods
    
    def __init__(self, *args) -> None:
        """
        Initialization. Stores the passed coefficients in an internal state. All
        passed arguments must be real numbers, which are treated as the
        polynomial coefficients sorted in the ascending order of the power. The
        last positional argument must be non-zero.
        
        Signature:
            *seq(int OR float) -> None
        
        Args:
            *args: *seq(int OR float); any number of integer or floating
                point arguments
        
        Raises:
            UT_TypeError: any of the arguments is not a real number
            UT_ValueError: number of arguments is less than 2, OR the last
                argument is zero
        
        Version 1.0.0.0
        """
        for Index, Value in enumerate(args):
            if not isinstance(Value, (int, float)):
                Error = UT_TypeError(Value, (int, float), SkipFrames = 1)
                Error.appendMessage(f'- argument {Value} at position {Index}')
                raise Error
        if len(args) < 2:
            raise UT_ValueError(len(args), '>= 2 - number of arguments',
                                                                SkipFrames = 1)
        if not args[-1]:
            raise UT_ValueError(len(args), '<> 0 - highest power coefficient',
                                                                SkipFrames = 1)
        self._Coefficients = tuple(args)
    
    def __str__(self) -> str:
        """
        Magic method to produce a human readable representation of the
        polynomial in the form "a_N * x**N + ... + a_1 * x + a_0",
        whith all zero coefficient value terms being ommited.

        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        Terms = list()
        MaxDegree = self.Degree
        Index = self.Degree
        while Index >= 0:
            Coefficient = self[Index]
            if Coefficient < 0:
                Sign = '-'
            elif Index == MaxDegree:
                Sign = ''
            else:
                Sign = '+'
            if not Index:
                Term = ''
            elif Index == 1:
                Term = 'x'
            else:
                Term = f'x**{Index}'
            AbsoluteValue = abs(Coefficient)
            if len(Term) and (AbsoluteValue == 1 or AbsoluteValue == 1.0):
                StringValue = ''
            elif not Index:
                StringValue = str(AbsoluteValue)
            else:
                StringValue =f'{AbsoluteValue}*'
            if AbsoluteValue:
                Terms.append(f'{Sign}{StringValue}{Term}')
            Index -= 1
        Result = ''.join(Terms)
        return Result
    
    def __repr__(self) -> str:
        """
        Magic method to produce a human readable representation of the
        polynomial in the form "'Polynomial(a_0, a_1, ..., a_N)'".

        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        Result = f"'{self.__class__.__name__}{self._Coefficients}'"
        return Result
    
    def __call__(self, Value: TReal) -> TReal:
        """
        Magic method. Evaluates the value of the polynomial at the given value
        of the argument.
        
        Signature:
            int OR float -> int OR float
        
        Args:
            Value: int OR float; value of the argument
        
        Returns:
            int OR float: the value of the polynomial
        
        Raises:
            UT_TypeError: argument is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        Result = self._Coefficients[-1]
        for Index in range(self.Degree - 1, -1, -1):
            NextCoefficient = self._Coefficients[Index]
            Result = NextCoefficient + Result * Value
        return Result
    
    def __getitem__(self, Index: int) -> TReal:
        """
        Magic method implementing read access to the stored coefficients by
        an integer index.

        Signature:
            int -> int OR float
        
        Args:
            Index: int; index of the coefficient, must be within the range
                - (N + 1) to N, where N is the polynomial's power
        
        Returns:
            int OR float: the value of the corresponding coefficient
        
        Raises:
            UT_TypeError: passed argument is not an integer
            UT_ValueError: passed index is out of range
        
        Version 1.0.0.0
        """
        if not isinstance(Index, int):
            raise UT_TypeError(Index, (int, ), SkipFrames = 1)
        Length = len(self._Coefficients)
        if Index >= Length or Index < - Length:
            raise UT_IndexError(f'{self.__class__.__name__}({Length})', Index,
                                                                SkipFrames = 1)
        return self._Coefficients[Index]
    
    def __copy__(self) -> TPolynomial:
        """
        Magic method implementing shallow copy of the object.

        Signature:
            None -> Polynomial
        
        Returns:
            Polynomal: a copy of itself

        Version 1.0.0.0
        """
        return self.__class__(*self._Coefficients)
    
    def __neg__(self) -> TPolynomial:
        """
        Magic method implementing a unary '-' operator (negation).

        Signature:
            None -> Polynomial
        
        Returns:
            Polynomal: a copy of itself with all coefficients negated
                (multiplied by -1)

        Version 1.0.0.0
        """
        Coefficients = [-Value for Value in self._Coefficients]
        return self.__class__(*Coefficients)
    
    def __pos__(self) -> TPolynomial:
        """
        Magic method implementing a unary '+' operator (identity).

        Signature:
            None -> Polynomial
        
        Returns:
            Polynomal: a copy of itself

        Version 1.0.0.0
        """
        return self.__class__(*self._Coefficients)
    
    def __add__(self, Value: TRealPoly) -> TIntPoly:
        """
        Magic method implementing right addition of another polynomial or a 
        scalar: P(x) + a OR P(x) + Q(X).

        Signature:
            int OR float OR Polynomial -> Polynomial OR int
        
        Args:
            Value: int OR float OR Polynomial; the second operand
        
        Returns:
            Polynomial: result of operation except for the case P(x) + (-P(x))
            int: zero value for the exeptional case
        
        Raises:
            UT_TypeError: arguments is not a real number neither another
                polynomial

        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [Item for Item in self._Coefficients]
            Coefficients[0] += Value
            Result = self.__class__(*Coefficients)
        elif isinstance(Value, self.__class__):
            Degree = max(self.Degree, Value.Degree)
            Left = list(self.getCoefficients())
            Right = list(Value.getCoefficients())
            for _ in range(len(Left), Degree + 1):
                Left.append(0)
            for _ in range(len(Right), Degree + 1):
                Right.append(0)
            Sum = [LeftCoeff + RightCoeff for LeftCoeff, RightCoeff
                                                            in zip(Left, Right)]
            while Sum:
                if not Sum[-1]:
                    Sum.pop()
                else:
                    break
            if not Sum:
                Result = 0
            elif len(Sum) == 1:
                Result = Sum[0]
            else:
                Result = self.__class__(*Sum)
        else:
            raise UT_TypeError(Value, (int, float, self.__class__),
                                                                SkipFrames = 1)
        return Result
    
    def __sub__(self, Value: TRealPoly) -> TIntPoly:
        """
        Magic method implementing substraction of a scalar or another polynomial
        from the current one: P(x) - a OR P(x) - Q(X).

        Signature:
            int OR float OR Polynomial -> Polynomial OR int
        
        Args:
            Value: int OR float OR Polynomial; the second operand
        
        Returns:
            Polynomial: result of operation except for the case P(x) - P(x)
            int: zero value for the exeptional case
        
        Raises:
            UT_TypeError: arguments is not a real number neither another
                polynomial
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [Item for Item in self._Coefficients]
            Coefficients[0] -= Value
            Result = self.__class__(*Coefficients)
        elif isinstance(Value, self.__class__):
            Degree = max(self.Degree, Value.Degree)
            Left = list(self.getCoefficients())
            Right = list(Value.getCoefficients())
            for _ in range(len(Left), Degree + 1):
                Left.append(0)
            for _ in range(len(Right), Degree + 1):
                Right.append(0)
            Difference = [LeftCoeff - RightCoeff for LeftCoeff, RightCoeff
                                                            in zip(Left, Right)]
            while Difference:
                if not Difference[-1]:
                    Difference.pop()
                else:
                    break
            if not Difference:
                Result = 0
            elif len(Difference) == 1:
                Result = Difference[0]
            else:
                Result = self.__class__(*Difference)
        else:
            raise UT_TypeError(Value, (int, float, self.__class__),
                                                                SkipFrames = 1)
        return Result
    
    def __mul__(self, Value: TRealPoly) -> TIntPoly:
        """
        Magic method implementing right multiplication by another polynomial or
        a scalar: P(x) * a OR P(x) * Q(X).

        Signature:
            int OR float OR Polynomial -> Polynomial OR int
        
        Args:
            Value: int OR float OR Polynomial; the second operand
        
        Returns:
            Polynomial: result of operation except for the case P(x) * 0
            int: zero value for the exeptional case
        
        Raises:
            UT_TypeError: arguments is not a real number neither another
                polynomial
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            if not Value:
                Result = 0
            else:
                Coefficients = [Item * Value for Item in self._Coefficients]
                Result = self.__class__(*Coefficients)
        elif isinstance(Value, self.__class__):
            Result = [Value[-1] * Item for Item in self._Coefficients]
            Power = Value.Degree
            for _ in range(Power):
                Result.insert(0,0)
            for Index in range(Power - 1, -1, -1):
                Coeff = Value[Index]
                for Pos, Val in enumerate(self._Coefficients):
                    Result[Index + Pos] += Val * Coeff
            Result = self.__class__(*Result)
        else:
            raise UT_TypeError(Value, (int, float, self.__class__),
                                                                SkipFrames = 1)
        return Result
    
    def __truediv__(self, Value: TReal) -> TPolynomial:
        """
        Magic method implementing division of a polynomial by a scalar: P(x) /a.

        Signature:
            int <> 0 OR float <> 0 -> Polynomial
        
        Args:
            Value: int <> 0 OR float <> 0; the second operand
        
        Returns:
            Polynomial: the result of operation
        
        Raises:
            UT_TypeError: the second (right) operand is not a real number
            UT_ValueError: division by zero

        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            if not Value:
                raise UT_ValueError(Value, '<> 0 - division by zero',
                                                                SkipFrames = 1)
            else:
                Coefficients = [Item / Value for Item in self._Coefficients]
                Result = self.__class__(*Coefficients)
        else:
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        return Result
    
    def __floordiv__(self, Value: TPolynomial) -> TRealPoly:
        """
        Magic method implementing 'integer' division of a polynomial by another
        polynomial: P(x) // Q(x) - which return the quotient of the division.

        Signature:
            Polynomial -> Polynomial OR int OR float
        
        Args:
            Value: Polinomial; the second polynomial (divisor)
        
        Returns:
            Polynomial: power of the divident is greater than the power of the
                divisor
            int OR float: power of the divident is less than or equal to the
                power of the divisor
        
        Raises:
            UT_TypeError: the second operand is not a polynomial
        
        Version 1.0.0.0
        """
        if not isinstance(Value, self.__class__):
            raise UT_TypeError(Value, (self.__class__, ), SkipFrames = 1)
        Result, _ = self.__divmod__(Value)
        return Result
    
    def __mod__(self, Value: TPolynomial) -> TRealPoly:
        """
        Magic method implementing 'mod' division of a polynomial by another
        polynomial: P(x) % Q(x) - which return the remainder of the division.

        Signature:
            Polynomial -> Polynomial OR int OR float
        
        Args:
            Value: Polinomial; the second polynomial (divisor)
        
        Returns:
            Polynomial: P(x) = a * Q(x) + R(X) or P(x) = T(X) * Q(x) + R(x)
                than the R(x) is the remainder (power <= than of Q(x))
            int OR float: P(x) = a * Q(x) + b or P(x) = T(X) * Q(x) + b than
                b is the remainder
        
        Raises:
            UT_TypeError: the second operand is not a polynomial

        Version 1.0.0.0
        """
        if not isinstance(Value, self.__class__):
            raise UT_TypeError(Value, (self.__class__, ), SkipFrames = 1)
        _, Result = self.__divmod__(Value)
        return Result
    
    def __divmod__(self, Value: TPolynomial) -> Tuple[TRealPoly, TRealPoly]:
        """
        Magic method implementing function call divmod(P(x), Q(x)), which
        returns both quotient and remainder of the division of P(x) by Q(x).

        Signature:
            Polynomial
                -> tuple(Polynomial OR int OR float, Polynomial OR int OR float)
        
        Args:
            Value: Polinomial; the second polynomial (divisor)
        
        Returns:
            Polynomial OR int OR float, Polynomial OR int OR float: a tuple of
                the quotient and remainder
        
        Raises:
            UT_TypeError: the second operand is not a polynomial
        
        Version 1.0.0.0
        """
        if not isinstance(Value, self.__class__):
            raise UT_TypeError(Value, (self.__class__, ), SkipFrames = 1)
        DegreeLeft = self.Degree
        DegreeRight = Value.Degree
        if DegreeLeft < DegreeRight:
            Quotient = 0
            Remainder = self.__copy__()
        else:
            Divident = list(self.getCoefficients())
            Divisor = list(Value.getCoefficients())
            Quotient = list()
            #Remainder = list()
            while len(Divident) >= len(Divisor):
                Coefficient = Divident[-1] / Divisor[-1]
                Quotient.insert(0, Coefficient)
                Shift = len(Divident) - len(Divisor)
                for Index, Item in enumerate(Divisor):
                    Divident[Index + Shift] -= Item * Coefficient
                Divident.pop()
            if len(Quotient) > 1:
                Quotient = self.__class__(*Quotient)
            else:
                Quotient = Quotient[0]
            while len(Divident):
                if not Divident[-1]:
                    Divident.pop()
                else:
                    break
            if not len(Divident):
                Remainder = 0
            elif len(Divident) == 1:
                Remainder = Divident[0]
            else:
                Remainder = self.__class__(*Divident)
        return (Quotient, Remainder)
    
    def __pow__(self, Value: int) -> TPolynomial:
        """
        Magic method implementing expontiation of a polynomial to a positive
        intger power: P(x)**k

        Signature:
            int > 0 -> Polynomial
        
        Args:
            Value: int > 0; the second operand
        
        Returns:
            Polynomial: the result of operation
        
        Raises:
            UT_TypeError: the second (right) operand is not an integer number
            UT_ValueError: the second (right) operand is zero or negative
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, int):
            if Value < 1:
                raise UT_ValueError(Value, '>= 1', SkipFrames = 1)
            PowerOf2 = int(log2(Value))
            Temp  = self.__class__(*self._Coefficients)
            Result = Temp
            for _ in range(PowerOf2):
                Result = Temp * Temp
                Temp = Result
            RestDegree = Value - 2**PowerOf2
            for _ in range(RestDegree):
                Result = Temp * self
                Temp = Result
        else:
            raise UT_TypeError(Value, (int), SkipFrames = 1)
        return Result
    
    def __radd__(self, Value: TReal) -> TPolynomial:
        """
        Magic method implementing left addition of a scalar to the polynomial:
        a + P(x).

        Signature:
            int OR float -> Polynomial

        Args:
            Value: int OR float; the second operand (left)
        
        Returns:
            Polynomial: the result of operation
        
        Raises:
            UT_TypeError: the second (left) operand is not a real number
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [Item for Item in self._Coefficients]
            Coefficients[0] += Value
            Result = self.__class__(*Coefficients)
        else:
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        return Result
    
    def __rsub__(self, Value: TReal) -> TPolynomial:
        """
        Magic method implementing substraction of the polynomial from a scalar:
        a - P(x).

        Signature:
            int OR float -> Polynomial
        
        Args:
            Value: int OR float; the second operand (left)
        
        Returns:
            Polynomial: the result of operation
        
        Raises:
            UT_TypeError: the second (left) operand is not a real number
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [-Item for Item in self._Coefficients]
            Coefficients[0] += Value
            Result = self.__class__(*Coefficients) 
        else:
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        return Result
    
    def __rmul__(self, Value: TReal) -> TPolynomial:
        """
        Magic method implementing multiplication of a scalar by the polynomial:
        a * P(x)

        Signature:
            int OR float -> Polynomial or int

        Args:
            Value: int OR float; the second operand (left)
        
        Returns:
            Polynomial: result of operation except for the case 0 * P(x)
            int: zero value for the exeptional case
        
        Raises:
            UT_TypeError: the second (left) operand is not a real number

        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            if not Value:
                Result = 0
            else:
                Coefficients = [Item * Value for Item in self._Coefficients]
                Result = self.__class__(*Coefficients)
        else:
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        return Result
    
    #properties
    
    @property
    def Degree(self) -> int:
        """
        Read-only property returning the degree of the polynomial.

        Signature:
            None -> int >= 1
        
        Version 1.0.0.0
        """
        return len(self._Coefficients) - 1
    
    #public instance methods
    
    def getCoefficients(self) -> TRealTuple:
        """
        Method to access the values of the polynomial coefficients.
        
        Signature:
            None -> tuple(int OR float)
        
        Returns:
            tuple(int OR float): the coefficients from the zero-th towards the
                highest power
        
        Version 1.0.0.0
        """
        return tuple(self._Coefficients)
    
    def getDerivative(self, Degree: int = 1) -> TRealPoly:
        """
        Calculates the K-th (K >= 1) derivative of the polynomial of degree N.
        
        Signature:
            /int >= 1/ -> Polynomial OR int OR float
        
        Args:
            Degree: (optional) int >= 1; degree of the derivative, defaults to
                1
        
        Returns:
            Polynomial: instance of, the K-th derivative for K < N
            int OR float: the K-th derivative for K >= N, which is strictly
                zero for K > N
        
        Raises:
            UT_TypeError: passed argument is not an integer
            UT_ValueError: passed argument is zero or negative
        
        Version 1.0.0.0
        """
        if not isinstance(Degree, int):
            raise UT_TypeError(Degree, (int, ), SkipFrames = 1)
        if Degree < 1:
            raise UT_ValueError(Degree, '>= 1', SkipFrames = 1)
        if Degree > self.Degree:
            Result = 0
        elif Degree == self.Degree:
            Result = factorial(Degree) * self[-1]
        else:
            StartIndex = Degree
            Coefficients = list()
            for Index in range(StartIndex, self.Degree + 1):
                Coeff = self[Index]
                for Power in range(Degree):
                    Coeff *= (Index - Power)
                Coefficients.append(Coeff)
            Result = self.__class__(*Coefficients)
        return Result
    
    def getAntiderivative(self) -> TPolynomial:
        """
        Calculates the first antiderivate (primitive function) of the
        polynomial.
        
        Signature:
            None -> Polynomial
        
        Returns:
            Polynomial: instance of, the first antiderivate up to a constant
                (free coefficient)
        
        Version 1.0.0.0
        """
        Coefficients = [Value / (Index + 1)
                            for Index, Value in enumerate(self._Coefficients)]
        Coefficients.insert(0, 0)
        return self.__class__(*Coefficients)
    
    def getConvolution(self, Other: TPolynomial) -> TPolynomial:
        """
        Calculates the convolution P(Q(x)) of two polynomials P(x) and Q(x),
        where P(x) is the current polynomial instance, and Q(x) is the passed
        polynomial.
        
        Signature:
            Polynomial -> Polynomial
            
        Args:
            Other: Polynomial; instance of, the second polynomial to be used
                as the argument of the current one
        
        Returns:
            Polynomial: instance of, the result of the convolution
        
        Raises:
            UT_TypeError: argument is not a polynomial
        
        Version 1.0.0.0
        """
        if not isinstance(Other, self.__class__):
            raise UT_TypeError(Other, (self.__class__, ), SkipFrames = 1)
        Result = self[0] + self[1] * Other
        for Power in range(2, self.Degree + 1):
            Result = Result + self[Power] * (Other ** Power)
        return Result

class RationalFunction:
    """
    Implementation of a rational function, i.e. a ratio of two polynomials. This
    class must be instantiated with two arguments representing the divident and
    the divisor polynomials, with either or both being an instance of the
    Polynomial class or a sequence of real numbers as the respective
    coefficients from the zer0-th to the highest power.
    
    An instance is also callable returning the value of the function at the
    passed value of the argument.
    
    Methods:
        getCoefficients()
            None -> tuple(int OR float), tuple(int OR float)
    
    Version 1.0.0.0
    """
    
    #special methods
    
    def __init__(self, Divident: TRealSequencePoly,
                                        Divisor: TRealSequencePoly) -> None:
        """
        Initialization. Creates the internally stored instances of the
        Polynomial class to store the respective polynomials.
        
        Signature:
            Polynomial OR seq(int OR float), Polynomial OR seq(int OR float)
                -> None
        
        Args:
            Divident: Polynomial OR seq(int OR float); divident polynomial
                or a sequence of the respective coefficients
            Divisor: Polynomial OR seq(int OR float); divisor polynomial
                or a sequence of the respective coefficients
        
        Raises:
            UT_TypeError: either of the arguments is neither real numbers
                sequence nor a polynomial
            UT_ValueError: any of the arguments passed as a sequence has length
                less than 2, OR its last element has zero value
        
        Version 1.0.0.0
        """
        if isinstance(Divident, Polynomial):
            self._Divident = Divident.__copy__()
        elif (isinstance(Divident, c_abc.Sequence)
                                        and (not isinstance(Divident, str))):
            for Index, Value in enumerate(Divident):
                if not isinstance(Value, (int, float)):
                    Error = UT_TypeError(Value, (int, float), SkipFrames = 1)
                    Error.appendMessage(f'- first argument, index {Index}')
                    raise Error
            if len(Divident) < 2:
                raise UT_ValueError(len(Divident), '>= 2 first argument length',
                                                                SkipFrames = 1)
            if not Divident[-1]:
                raise UT_ValueError(Divident[-1],
                            '<> 0 first argument, highest power coefficient',
                                                                SkipFrames = 1)
            self._Divident = Polynomial(*Divident)
        else:
            Error = UT_TypeError(Divident, (Polynomial, c_abc.Sequence),
                                                                SkipFrames = 1)
            Error.appendMessage('- first argument')
            raise Error
        if isinstance(Divisor, Polynomial):
            self._Divisor = Divisor.__copy__()
        elif (isinstance(Divisor, c_abc.Sequence)
                                        and (not isinstance(Divisor, str))):
            for Index, Value in enumerate(Divisor):
                if not isinstance(Value, (int, float)):
                    Error = UT_TypeError(Value, (int, float), SkipFrames = 1)
                    Error.appendMessage(f'- second argument, index {Index}')
                    raise Error
            if len(Divisor) < 2:
                raise UT_ValueError(len(Divisor), '>= 2 second argument length',
                                                                SkipFrames = 1)
            if not Divisor[-1]:
                raise UT_ValueError(Divisor[-1],
                            '<> 0 second argument, highest power coefficient',
                                                                SkipFrames = 1)
            self._Divisor = Polynomial(*Divisor)
        else:
            Error = UT_TypeError(Divident, (Polynomial, c_abc.Sequence),
                                                                SkipFrames = 1)
            Error.appendMessage('- second argument')
            raise Error
    
    def __call__(self, Value: TReal) -> TReal:
        """
        Magic method. Evaluates the value of the function at the given value of
        the argument.
        
        Signature:
            int OR float -> int OR float
        
        Args:
            Value: int OR float; value of the argument
        
        Returns:
            int OR float: the value of the function
        
        Raises:
            UT_TypeError: argument is neither integer nor floating point number
            UT_ValueError: function has a singularity point at the value of
                the argument - division by zero
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        Divident = self._Divident(Value)
        Divisor = self._Divisor(Value)
        if abs(Divisor) > NEAR_ZERO_SOFT:
            Result = Divident / Divisor
        else:
            if abs(Divident) > NEAR_ZERO_SOFT and abs(Divisor) < NEAR_ZERO_HARD:
                raise UT_ValueError(Value,
                                'not a singularity point (division by zero)',
                                                                SkipFrames = 1)
            else:
                MinDegree = min(self._Divident.Degree, self._Divisor.Degree)
                Degree = 1
                while Degree < (MinDegree + 1):
                    Divident=self._Divident.getDerivative(Degree=Degree)
                    if isinstance(Divident, Polynomial):
                        Divident = Divident(Value)
                    Divisor = self._Divisor.getDerivative(Degree=Degree)
                    if isinstance(Divisor, Polynomial):
                        Divisor = Divisor(Value)
                    if (abs(Divident) > NEAR_ZERO_SOFT or
                                                abs(Divisor) > NEAR_ZERO_SOFT):
                        break
                    Degree += 1
                if Divisor:
                    Result = Divident / Divisor
                else:
                    raise UT_ValueError(Value,
                                'not a singularity point (division by zero)',
                                                                SkipFrames = 1)
        return Result
    
    def __str__(self) -> str:
        """
        Magic method to produce a human readable representation of the rational
        function in the form "P(x)/Q(X)", where P(x) and Q(x) are string
        representations of the divident and divisor polynomilas respectively
        whith all zero coefficient value terms being ommited.

        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        Result = f'({self._Divident})/({self._Divisor})'
        return Result
    
    def __repr__(self) -> str:
        """
        Magic method to produce a human readable representation of the rational
        function in the compact form listing two coefficients tuples as
        "'RationalFunction((a_0, ..., a_N),(b_0, ..., b_N))'".

        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        Result = "'{}({}, {})'".format(self.__class__.__name__,
                    self._Divident._Coefficients, self._Divisor._Coefficients)
        return Result
    
    #public instance methods
    
    def getCoefficients(self) -> Tuple[TRealTuple, TRealTuple]:
        """
        Method to access the values of the coefficients of the both polynomials:
        divident and divisor.
        
        Signature:
            None -> tuple(int OR float), tuple(int OR float)
        
        Returns:
            tuple(int OR float), tuple(int OR float): unpacked tuple of two
                tuples listing the coefficients of the divident and divisor
                polynomials respectively, from the zero-th to the highest
                power sorted
        
        Version 1.0.0.0
        """
        return self._Divident._Coefficients, self._Divisor._Coefficients