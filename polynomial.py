#usr/bin/python3
"""
Module math_extra_lib.polynomial

Implementation of the polynomials and releated arithmetics.

Classes:
    Polynomial
    RationalFunction
"""

__version__= '1.0.0.0'
__date__ = '23-11-2022'
__status__ = 'Development'

#imports

#+ standard libraries

from typing import Sequence, Union, Tuple

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
    Implementation of polynomials. This class must be instantiated with an
    unpacked sequence of real numbers, which will be set as the coefficients
    from the highest to the zeroth power. All leading zeroes in the sequence are
    ignored.
    
    An instance of this class supports index access to the individual
    coefficients (read only) and arithmetical operations with a real number or
    another polynomial.
    
    An instance is also callable returning the value of the polynomial at the
    passed value of the argument.
    
    Properties:
        Power: (read-only) int > 1
    
    Class methods:
        fromRoots(*args)
            *tuple(int OR float) -> Polynomial
    
    Methods:
        getCoefficients()
            None -> tuple(int OR float)
        getAntiderivative(Power = 1)
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
        factorization: (x-x_1)*...*(x-x_N) -> a_0
        
        Signature:
            *tuple(int OR float) -> Polynomial
        
        Args:
            *args: *tuple(int OR float); any number of real numbers
        
        Version 1.0.0.0
        """
        pass
    
    #special methods
    
    def __init__(self, *args) -> None:
        """
        Initialization. Stores the passed coefficients in an internal state. All
        passed arguments must be real numbers, which are treated as the
        polynomial coefficients sorted in the descending power. All first zero
        arguments are ignored untill a non-zero is encountered. The length of
        the remaining sub-sequence (starting from the first non-zero value) must
        exceed 1.
        
        Signature:
            *tuple(int OR float) -> None
        
        Args:
            *args: *tuple(int OR float); any number of real numbers
        
        Raises:
            
        
        Version 1.0.0.0
        """
        pass
    
    def __str__(self) -> str:
        """
        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        pass
    
    def __repr__(self) -> str:
        """
        Singature:
            None -> str
        
        Version 1.0.0.0
        """
        pass
    
    def __call__(self, Value: TReal) -> TReal:
        """
        Evaluates the value of the polynomial at the given value of the
        argument.
        
        Signature:
            int OR float -> int OR float
        
        Args:
            Value: int OR float; value of the argument
        
        Returns:
            int OR float: the value of the polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __getitem__(self, Index: int) -> TReal:
        """
        Signature:
            int -> int OR float
        
        Version 1.0.0.0
        """
        pass
    
    def __copy__(self) -> TPolynomial:
        """
        Signature:
            None -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __neg__(self) -> TPolynomial:
        """
        Signature:
            None -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __pos__(self) -> TPolynomial:
        """
        Signature:
            None -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __add__(self, Value: TRealPoly) -> TIntPoly:
        """
        Signature:
            int OR float OR Polynomial -> Polynomial OR 0
        
        Version 1.0.0.0
        """
        pass
    
    def __sub__(self, Value: TRealPoly) -> TIntPoly:
        """
        Signature:
            int OR float OR Polynomial -> Polynomial OR 0
        
        Version 1.0.0.0
        """
        pass
    
    def __mul__(self, Value: TRealPoly) -> TIntPoly:
        """
        Signature:
            int OR float OR Polynomial -> Polynomial OR 0
        
        Version 1.0.0.0
        """
        pass
    
    def __truediv__(self, Value: TReal) -> TPolynomial:
        """
        Signature:
            int OR float -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __floordiv__(self, Value: TPolynomial) -> TRealPoly:
        """
        Signature:
            Polynomial -> Polynomial OR int OR float
        
        Version 1.0.0.0
        """
        pass
    
    def __mod__(self, Value: TPolynomial) -> TRealPoly:
        """
        Signature:
            Polynomial -> Polynomial OR int OR float
        
        Version 1.0.0.0
        """
        pass
    
    def __divmod__(self, Value: TPolynomial) -> Tuple[TRealPoly, TRealPoly]:
        """
        Signature:
            Polynomial -> Polynomial OR int OR float, Polynomial OR int OR float
        
        Version 1.0.0.0
        """
        pass
    
    def __pow__(self, Value: int) -> TPolynomial:
        """
        Signature:
            int > 0 -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __radd__(self, Value: TReal) -> TPolynomial:
        """
        Signature:
            int OR float OR Polynomial -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __rsub__(self, Value: TReal) -> TPolynomial:
        """
        Signature:
            int OR float OR Polynomial -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    def __rmul__(self, Value: TReal) -> TPolynomial:
        """
        Signature:
            int OR float OR Polynomial -> Polynomial
        
        Version 1.0.0.0
        """
        pass
    
    #properties
    
    @property
    def Power(self) -> int:
        """
        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        pass
    
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
        pass
    
    def getDerivative(self, Power: int = 1) -> TRealPoly:
        """
        Calculates the K-th (K >= 1) derivative of the polynomial.
        
        Signature:
            /int >= 1/ -> Polynomial OR int OR float
        
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
    coefficients from the highest to the zeroth power. All leading zeroes in the
    sequences are ignored.
    
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
        Evaluates the value of the function at the given value of the argument.
        
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