#usr/bin/python3
"""
Module math_extra_lib.vectors_matrices

Classes:
    Array2D
    Vector
    Column
    Row
    Matrix
    SquareMatrix
"""

__version__= '1.0.0.0'
__date__ = '11-01-2023'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
#import math

import collections.abc as c_abc

from typing import Sequence, Union, Tuple, Any, List, Optional, Dict, NoReturn

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#types

TReal = Union[int, float]

TRealSequence = Sequence[TReal]

TSequenceRealSequence = Sequence[Sequence[TReal]]

TRealTuple = Tuple[TReal, ...]

TArray = "Array2D"

TVector = "Vector"

TColumn = "Column"

TRow = "Row"

TMatrix = "Matrix"

TSquareMatrix = "SquareMatrix"

#helper functions

def _ChechIfRealSequence(Value: Any) -> None:
    """
    Helper function designed to be used inside initialization methods to check
    if the passed argument is a generic sequence of integers or floating point
    numbers.
    
    Signature:
        type A -> None
    
    Raises:
        UT_TypeError: the argument is not a sequence, OR any of its elements is
            not an integer or floating point number
    
    Version 1.0.0.0
    """
    if (not isinstance(Value, c_abc.Sequence)) or isinstance(Value, str):
        raise UT_TypeError(Value, (list, tuple), SkipFrames = 2)
    for Index, Item in enumerate(Value):
        if not isinstance(Item, (int, float)):
            Error = UT_TypeError(Item, (int, float), SkipFrames = 2)
            Message = '{} at index {} in {}'.format(Error.args[0], Index, Value)
            Error.args = (Message, )
            raise Error

def _ChechIfSequenceRealSequence(Value: Any) -> None:
    """
    """
    pass

#classes

class Array2D:
    """
    """
    
    #special methods
    
    def __init__(self, seqValues: Union[TRealSequence, TSequenceRealSequence],
                                *, Width : Optional[int] = None,
                                    Height : Optional[int] = None,
                                        isColumnsFirst : bool = True) -> None:
        """
        """
        pass
    
    def __str__(self) -> str:
        """
        """
        pass
    
    def __repr__(self) -> str:
        """
        """
        pass
    
    def __iter__(self) -> NoReturn:
        """
        Magic method to hook the iterator protocol, which should not be
        supported. As the desired consequence, the 'contains' check is also
        disabled.
        
        Raises:
            TypeError: as expected from a non-iterable type
        
        Version 1.0.0.0
        """
        raise TypeError("'{}' object is not iterable".format(
                                                    self.__class__.__name__))
    
    def __getitem__(self, Indexes: Tuple[int, int]) -> TReal:
        """
        """
        pass
    
    #public properties
    
    @property
    def Width(self) -> int:
        """
        """
        pass
    
    @property
    def Height(self) -> int:
        """
        """
        pass

    @property
    def Data(self) -> List[List[TReal]]:
        """
        """
        pass

class Vector:
    """
    """
    
    #special methods
    
    def __init__(self, *args) -> None:
        """
        Initialization. The passed numerical arguments a taken as the elements
        of a vector to be created.
        
        Signature:
            *seq(int OR float) -> None
        
        Args:
            *args: *seq(int OR float); any number of integer or floating point
                arguments as the elements of the vector
        
        Raises:
            UT_TypeError: any of the arguments is neither integer nor floating
                point
            UT_ValueError: number of arguments is less than 2
        
        Version 1.0.0.0
        """
        _ChechIfRealSequence(args)
        if len(args) < 2:
            raise UT_ValueError(len(args), '>= 2 - number of arguments',
                                                                SkipFrames = 1)
        self._Elements = tuple(args)
    
    def __copy__(self) -> TVector:
        """
        Magic method to hook the shallow copying.
        
        Signature:
            None -> 'Vector
        
        Returns:
            'Vector: another instance of the same class with the identical
                elements
        
        Version 1.0.0.0
        """
        return self.__class__(*self._Elements)
    
    def __str__(self) -> str:
        """
        Magic method to support str() function with the vector as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return '[{}]'.format(', '.join(map(str, self._Elements)))
    
    def __repr__(self) -> str:
        """
        Magic method to support repr() function with the vector as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return "'{}({})'".format(self.__class__.__name__,
                                            ', '.join(map(str, self._Elements)))
    
    def __getitem__(self, Index: int) -> TReal:
        """
        Magic method to hook the index read access.
        
        Signature:
            int -> int OR float
        
        Args:
            Index: int; the required element index
        
        Returns:
            int OR float: the value of the respective element
        
        Raises:
            UT_TypeError: index is not an integer number
            UT_ValueError: index is an integer outside the range
        
        Version 1.0.0.0
        """
        if not isinstance(Index, int):
            raise UT_TypeError(Index, int, SkipFrames = 1)
        Size = self.Size
        if (Index < - Size) or (Index >= Size):
            raise UT_ValueError(Index, 'in range [{}, {}] - indexing'.format(
                                                -Size, Size-1), SkipFrames = 1)
        return self._Elements[Index]
    
    def __iter__(self) -> NoReturn:
        """
        Magic method to hook the iterator protocol, which should not be
        supported. As the desired consequence, the 'contains' check is also
        disabled.
        
        Raises:
            TypeError: as expected from a non-iterable type
        
        Version 1.0.0.0
        """
        raise TypeError("'{}' object is not iterable".format(
                                                    self.__class__.__name__))
    
    def __add__(self, Other: TVector) -> TVector:
        """
        Magic method implementing addition of two vectors of the same type.
        
        Signature:
            'Vector -> 'Vector
        
        Args:
            Other: 'Vector; another instance of the same vector class of the
                same size
        
        Returns:
            'Vector: instance of the same class, which is the result of the
                operation
        
        Raises:
            UT_TypeError: the second operand is not an instance of the same
                vector class
            UT_ValueError: different sizes of the vectors
        
        Version 1.0.0.0
        """
        if ((not isinstance(Other, self.__class__))
                        or (not (Other.__class__ is self.__class__))):
            raise UT_TypeError(Other, self.__class__, SkipFrames = 1)
        if Other.Size != self.Size:
            raise UT_ValueError(Other.Size, '{} - vectors dimensions'.format(
                                                    self.Size), SkipFrames = 1)
        Elements = [self._Elements[Index] + Item
                                    for Index, Item in enumerate(Other.Data)]
        return self.__class__(*Elements)
    
    def __radd__(self, Other: Any) -> NoReturn:
        """
        Magic method implementing addition of two vectors of the same type,
        specifically that it prohibits other types as left operand.
        
        Raises:
            UT_TypeError: always, unconditionally
        
        Version 1.0.0.0
        """
        raise UT_TypeError(Other, self.__class__, SkipFrames = 1)
    
    def __sub__(self, Other: TVector) -> TVector:
        """
        Magic method implementing subtraction of two vectors of the same type.
        
        Signature:
            'Vector -> 'Vector
        
        Args:
            Other: 'Vector; another instance of the same vector class of the
                same size
        
        Returns:
            'Vector: instance of the same class, which is the result of the
                operation
        
        Raises:
            UT_TypeError: the second operand is not an instance of the same
                vector class
            UT_ValueError: different sizes of the vectors
        
        Version 1.0.0.0
        """
        if ((not isinstance(Other, self.__class__))
                        or (not (Other.__class__ is self.__class__))):
            raise UT_TypeError(Other, self.__class__, SkipFrames = 1)
        if Other.Size != self.Size:
            raise UT_ValueError(Other.Size, '{} - vectors dimensions'.format(
                                                    self.Size), SkipFrames = 1)
        Elements = [self._Elements[Index] - Item
                                    for Index, Item in enumerate(Other.Data)]
        return self.__class__(*Elements)
    
    def __rsub__(self, Other: Any) -> NoReturn:
        """
        Magic method implementing subtraction of two vectors of the same type,
        specifically that it prohibits other types as left operand.
        
        Raises:
            UT_TypeError: always, unconditionally
        
        Version 1.0.0.0
        """
        raise UT_TypeError(Other, self.__class__, SkipFrames = 1)
    
    def __mul__(self, Other: Union[TReal, TVector]) -> Union[TReal, TVector]:
        """
        """
        pass
    
    def __rmul__(self, Other: TReal) -> TVector:
        """
        """
        pass
    
    def __truediv__(self, Other: TReal) -> TVector:
        """
        """
        pass
    
    def __matmul__(self, Other: TVector) -> TArray:
        """
        """
        pass
    
    #public class methods
    
    @classmethod
    def generateOrtogonal(cls, Length: int, Index: int) -> TVector:
        """
        """
        pass
    
    #public properties
    
    @property
    def Size(self) -> int:
        """
        Read-only property to access the length (size) of the vector.
        
        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return len(self._Elements)
    
    @property
    def Data(self) -> List[TReal]:
        """
        Read-only property to access all stored elements of the vector as a
        single list.
        
        Signature:
            None -> list(int OR float)
        
        Version 1.0.0.0
        """
        return list(self._Elements)
    
    #public instance method
    
    def normalize(self) -> TVector:
        """
        """
        pass

class Column(Vector):
    """
    """
    pass

    #special methods
    
    def __str__(self) -> str:
        """
        Magic method to support str() function with the vector as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return '[{}]^T'.format(', '.join(map(str, self.Data)))

    def __mul__(self, Other: TReal) -> TColumn:
        """
        """
        return NotImplemented
    
    def __rmul__(self, Other: TReal) -> TColumn:
        """
        """
        return NotImplemented

class Row(Vector):
    """
    """
    pass

    #special methods

    def __mul__(self, Other: Union[TReal, TColumn]) -> Union[TRow, TReal]:
        """
        """
        return NotImplemented
    
    def __rmul__(self, Other: TReal) -> TRow:
        """
        """
        return NotImplemented

class Matrix(Array2D):
    """
    """
    
    #special methods
    
    def __add__(self, Other: TMatrix) -> TMatrix:
        """
        """
        return NotImplemented
    
    def __sub__(self, Other: TMatrix) -> TMatrix:
        """
        """
        return NotImplemented
    
    def __mul__(self, Other: Union[TReal, Column, TMatrix]
                                                ) -> Union[Column, TMatrix]:
        """
        """
        return NotImplemented
    
    def __rmul__(self, Other: Union[TReal, Row]) -> Union[Row, TMatrix]:
        """
        """
        return NotImplemented
    
    def __truediv__(self, Other: TReal) -> TMatrix:
        """
        """
        return NotImplemented
    
    #public properties
    
    @property
    def Width(self) -> int:
        """
        """
        pass
    
    @property
    def Height(self) -> int:
        """
        """
        pass
    
    #public methods
    
    def transpose(self) -> TMatrix:
        """
        """
        pass
    
    def getColumn(self, Index: int) -> Column:
        """
        """
        pass
    
    def getRow(self, Index: int) -> Row:
        """
        """
        pass

class SquareMatrix(Matrix):
    """
    """
    
    #public class methods
    
    @classmethod
    def generateIdentity(cls, Size: int) -> TSquareMatrix:
        """
        """
        pass
    
    @classmethod
    def generatePermutation(cls, Permutation: Sequence[int]) -> TSquareMatrix:
        """
        """
        pass
    
    #special methods
    
    def __init__(self, seqValues: Union[TRealSequence, TSequenceRealSequence],
                    *, Size : int = None, isColumnsFirst : bool = True) -> None:
        """
        """
        pass
    
    #public properties
    
    @property
    def Size(self) -> int:
        """
        """
        pass
    
    #public instance methods
    
    def getTrace(self) -> TReal:
        """
        """
        pass
    
    def getLUPdecomposition(self) -> Tuple[TSquareMatrix, TSquareMatrix,
                                                            TRealTuple, int]:
        """
        """
        pass
    
    def getFullDecomposition(self) -> Tuple[TSquareMatrix, TSquareMatrix,
                                                TSquareMatrix, TRealTuple, int]:
        """
        """
        pass
    
    def getDeterminant(self) -> TReal:
        """
        """
        pass
    
    def getInverse(self) -> TSquareMatrix:
        """
        """
        pass
    
    def getEigenValues(self) -> Union[TRealTuple, None]:
        """
        """
        pass
    
    def getEigenVectors(self) -> Union[Dict[TReal, Tuple[TColumn, ...]], None]:
        """
        """
        pass

#Do dynamic binding to implement column x row -> matrix multiplication