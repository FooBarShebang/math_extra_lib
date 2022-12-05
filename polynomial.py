#usr/bin/python3
"""
Module math_extra_lib.polynomial

Implementation of the polynomials and releated arithmetics.

Classes:
    Polynomial
    RationalFunction
"""

__version__= '1.0.0.0'
__date__ = '05-12-2022'
__status__ = 'Development'

#imports

#+ standard libraries

from typing import Sequence, Union, Tuple

from math import log2

#types

TReal = Union[int, float]

TRealSequence = Sequence[TReal]

TPolynomial = "Polynomial"

TRealSequencePoly = Union[TRealSequence, TPolynomial]

TRealPoly = Union[TReal, TPolynomial]

TIntPoly = Union[int, TPolynomial]

TRealTuple = Tuple[TReal, ...]

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
        Degree: (read-only) int > 1
    
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
            *tuple(int OR float) -> Polynomial
        
        Args:
            *args: *tuple(int OR float); any number of integer or floating
                point arguments
        
        Version 1.0.0.0
        """
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
            *tuple(int OR float) -> None
        
        Args:
            *args: *tuple(int OR float); any number of integer or floating
                point arguments
        
        Raises:
            
        
        Version 1.0.0.0
        """
        self._Coefficients = tuple(args)
    
    def __str__(self) -> str:
        """
        Magic method to produce a human readable representation of the
        polynomial in the form "a_0 + a_1 * x + a_2 * x^2 + ... + a_N * x^N",
        whith all zero coefficient value terms being ommited.

        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        pass
    
    def __repr__(self) -> str:
        """
        Magic method to produce a human readable representation of the
        polynomial in the form "'Polynomial(a_0, a_1, ..., a_N)'".

        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        pass
    
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
        
        Version 1.0.0.0
        """
        a = self._Coefficients[-1]
        for Index in range(self.Degree - 1, -1, -1):
            b = self._Coefficients[Index]
            Result = b + a * Value
            a = Result
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
        
        Version 1.0.0.0
        """
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

        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [Item for Item in self._Coefficients]
            Coefficients[0] += Value
            Result = self.__class__(*Coefficients)
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
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [Item for Item in self._Coefficients]
            Coefficients[0] -= Value
            Result = self.__class__(*Coefficients)
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
        return Result
    
    def __truediv__(self, Value: TReal) -> TPolynomial:
        """
        Magic method implementing division of a polynomial by a scalar: P(x) /a.

        Signature:
            int OR float -> Polynomial
        
        Args:
            Value: int OR float; the second operand
        
        Returns:
            Polynomial: the result of operation
        
        Raises

        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            if not Value:
                Result = 0 #raise exception!
            else:
                Coefficients = [Item / Value for Item in self._Coefficients]
                Result = self.__class__(*Coefficients)
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
        
        Version 1.0.0.0
        """
        pass
    
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

        Version 1.0.0.0
        """
        pass
    
    def __divmod__(self, Value: TPolynomial) -> Tuple[TRealPoly, TRealPoly]:
        """
        Magic method implementing function call divmod(P(x), Q(x)), which
        returns both quotient and remainder of the division of P(x) by Q(x).

        Signature:
            Polynomial -> Polynomial OR int OR float, Polynomial OR int OR float
        
        Args:
            Value: Polinomial; the second polynomial (divisor)
        
        Returns:
            Polynomial OR int OR float, Polynomial OR int OR float: an unpacked
                tuple of the quotient and remainder
        
        Raises:
        
        Version 1.0.0.0
        """
        pass
    
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
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, int):
            Degree2 = int(log2(Value))
            Temp  = self.__class__(*self._Coefficients)
            Result = Temp
            for _ in range(Degree2):
                Result = Temp * Temp
                Temp = Result
            RestDegree = Value - 2**Degree2
            for _ in range(RestDegree):
                Result = Temp * self
                Temp = Result
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
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [Item for Item in self._Coefficients]
            Coefficients[0] += Value
            Result = self.__class__(*Coefficients)
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
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            Coefficients = [-Item for Item in self._Coefficients]
            Coefficients[0] += Value
            Result = self.__class__(*Coefficients) 
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

        Version 1.0.0.0
        """
        Result = None
        if isinstance(Value, (int, float)):
            if not Value:
                Result = 0
            else:
                Coefficients = [Item * Value for Item in self._Coefficients]
                Result = self.__class__(*Coefficients)
        return Result
    
    #properties
    
    @property
    def Degree(self) -> int:
        """
        Read-only property returning the degree of the polynomial.

        Signature:
            None -> int > 0
        
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
            tuple(int OR float): the coefficients from the highest towards the
                zero-th power
        
        Version 1.0.0.0
        """
        return tuple(self._Coefficients)
    
    def getDerivative(self, Degree: int = 1) -> TRealPoly:
        """
        Calculates the K-th (K >= 1) derivative of the polynomial.
        
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
            
        
        Version 1.0.0.0
        """
        pass
    
    def getAntiderivative(self) -> TPolynomial:
        """
        Calcualates the first antiderivate (primitive function) of the
        polynomial.
        
        Signature:
            None -> Polynomial
        
        Returns:
            Polynomial: instance of, the first antiderivate up to a constant
                (free coefficient)
        
        Version 1.0.0.0
        """
        pass
    
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
            
        
        Version 1.0.0.0
        """
        pass

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
    
    def __init__(self, PolyDivident: TRealSequencePoly,
                                        PolyDivisor: TRealSequencePoly) -> None:
        """
        Initialization. Creates the internally stored instances of the
        Polynomial class to store the respective polynomials.
        
        Signature:
            Polynomial OR seq(int OR float), Polynomial OR seq(int OR float)
                -> None
        
        Args:
            PolyDivident: Polynomial OR seq(int OR float); divident polynomial
                or a sequence of the respective coefficients
            PolyDivisor: Polynomial OR seq(int OR float); divisor polynomial
                or a sequence of the respective coefficients
        
        Version 1.0.0.0
        """
        pass
    
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
        
        Version 1.0.0.0
        """
        pass
    
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
                polynomials respectively, from the highest to the zero-th
                power sorted
        
        Version 1.0.0.0
        """
        pass