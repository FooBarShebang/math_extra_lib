#usr/bin/python3
"""
Module math_extra_lib.vectors_matrices.

Imlements matrices, generic vectors, column and row vectors as well as
arithmetics involving instances of these classes and real number as operands.

Classes:
    Array2D
    Vector
    Column
    Row
    Matrix
    SquareMatrix
"""

__version__= '1.0.0.0'
__date__ = '18-01-2023'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import collections.abc as c_abc

from math import sqrt, floor
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

def _CheckIfRealSequence(Value: Any) -> None:
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

def _CheckIfSequenceRealSequence(Value: Any) -> None:
    """
    Helper function designed to be used inside initialization methods to check
    if the passed argument is a nested sequence of sequences of integers or
    floating point numbers.
    
    Signature:
        type A -> None
    
    Raises:
        UT_TypeError: the argument is not a sequence, OR any of its elements is
            not a sequence, OR any of the elements of any sub-sequence is not an
            integer or floating point number
    
    Version 1.0.0.0
    """
    if (not isinstance(Value, c_abc.Sequence)) or isinstance(Value, str):
        raise UT_TypeError(Value, (list, tuple), SkipFrames = 2)
    for Index, Item in enumerate(Value):
        if (not isinstance(Item, c_abc.Sequence)) or isinstance(Item, str):
            Error = UT_TypeError(Item, (list, tuple), SkipFrames = 2)
            Message = '{} at index {} in {}'.format(Error.args[0], Index, Value)
            Error.args = (Message, )
            raise Error
        for Inner, Element in enumerate(Item):
            if not isinstance(Element, (int, float)):
                Error = UT_TypeError(Element, (int, float), SkipFrames = 2)
                Message = '{} at index [{}][{}] in {}'.format(Error.args[0],
                                                            Index, Inner, Value)
                Error.args = (Message, )
                raise Error

#classes

class Array2D:
    """
    A prototype class for the generic and square matrices, implementing the
    data storage and read-access in the form of a 2-D array.
    
    The data is stored and returned (property Data) as a sequence of the nested
    equal length sub-sequences of real numbers, each sub-sequence representing a
    single row of the array, i.e. in the rows-first order.
    
    The instances of this class are immutable objects, and are not considered
    to be sequences, thus not supporting iteration and 'contains' check. But
    the entire stored data can be copied into a mutable Python sequence (list)
    using the property Data. Individual element can be read-only accessed using
    double indexing as obj[col_index, row_index]. Slice notation is not
    supported.
    
    Can be instantiated either from a flat sequence of real number, when either
    width or height or both must be specified; or from a nested sequence, in
    which case the width and height arguments are ignored even if provided. The
    default parsing order is rows-first, which can be switched to columns-first
    using a boolean keyword argument isColumnsFirst, which defaults to False.
    
    Thus, the supported instantiation call signatures are:
        * Array2D(list(int OR float), Width = int >= 2)
        * Array2D(list(int OR float), Height = int >= 2)
        * Array2D(list(int OR float), Width = int >= 2, Height = int >= 2)
        * Array2D(list(int OR float), Width = int >= 2)
        * Array2D(list(int OR float), Height = int >= 2)
        * Array2D(list(int OR float), Width = int >= 2, Height = int >= 2,
            isColumnsFirst = True)
        * Array2D(list(list(int OR float)))
        * Array2D(list(list(int OR float)), isColumnsFirst = True)
    
    Properties:
        Width: (read-only) int >= 2
        Height: (read-only) int >= 2
        Data: (read-only) list(list(int OR float))
    
    Version 1.0.0.0
    """
    
    #special methods
    
    def __init__(self, seqValues: Union[TRealSequence, TSequenceRealSequence],
                                *, Width : Optional[int] = None,
                                    Height : Optional[int] = None,
                                        isColumnsFirst : bool = False) -> None:
        """
        Instantiation method. Parses the passed data sequence and packs it into
        the internally stored nested tuple structure representing a 2D array or
        a matrix, with each tuple element representing a single row of that
        array or matrix.
        
        Signature:
            seq(int OR float) OR seq(seq(int OR float))/, int >= 2 OR None,
                int >= 2 OR None, bool/ -> None
        
        Args:
            seqValues: seq(int OR float) OR seq(seq(int OR float)); elements
                of the array / matrix, in the flat form the total number of
                elements must be equal to or greater than 2 * Width if only
                width is specified, or 2 * Height if only height is specified,
                or Width * Height if both are specified
            Width: (keyword) int >= 2 OR None; required width of the array or
                matrix, defaults to None meaning automatic definition based on
                the number of elements and the specified required height, at
                least one of the dimensions (width and / or height) must be
                specified if the data is passed as a flat sequence, this
                argument is ignored if the data is passed as a nested sequence
            Height: (keyword) int >= 2 OR None; required height of the array or
                matrix, defaults to None meaning automatic definition based on
                the number of elements and the specified required width, at
                least one of the dimensions (width and / or height) must be
                specified if the data is passed as a flat sequence, this
                argument is ignored if the data is passed as a nested sequence
            isColumnsFirst: (keyword) bool; flag if the passed data to parsed
                in the columns-first order, defaults to False, i.e. rows-first
                order when each consequitive slice of a flat sequence or
                sub-sequence element of a nested sequence is treated as the
                representation of a single row of the array or matrix
        
        Raises:
            UT_TypeError: mandatory argument is neither a flat sequence of real
                numbers nor a nested sequence of sequences of real numbers, OR
                optional keyword argument isColumnsFirst is not boolean, OR
                optional keyword arguments Width or Height are neither None nor
                integer numbers
            UT_ValueError: either Width or Height argument is an integer < 2, OR
                the both arguments are None when the mandatory argument is a
                flat sequence of real numbers, OR the length of a flat sequence
                as the mandatory argument is too short for the given values of
                Width and / or Height, OR a nested sequence as the mandatory
                argument has less than 2 elements, OR the length of an
                sub-sequence element is less than 2, OR the sub-sequence
                elements differ in length.
        
        Version 1.0.0.0
        """
        if not isinstance(isColumnsFirst, bool):
            Error = UT_TypeError(isColumnsFirst, bool, SkipFrames = 1)
            Message = '{} - isColumnsFirst argument'.format(Error.args[0])
            Error.args = (Message, )
            raise Error
        try:
            _CheckIfRealSequence(seqValues)
            Length = len(seqValues)
            if (Width is None) and (Height is None):
                raise UT_ValueError((Width, Height),
                        '!= (None, None) - Width and Height keyword arguments',
                                                                SkipFrames = 1)
            if Width is None:
                if not isinstance(Height, int):
                    Error = UT_TypeError(Height, int, SkipFrames = 1)
                    Message = '{} - Height argument'.format(Error.args[0])
                    Error.args = (Message, )
                    raise Error
                if Height < 2:
                    raise UT_ValueError(Height, '>= 2 - Height argument',
                                                                SkipFrames = 1)
                _Height = Height
                _Width = int(floor(Length / Height))
                if _Width < 2:
                    raise UT_ValueError(Length,
                                '>= {} - sequence length'.format(2 * Height),
                                                                SkipFrames = 1)
            elif Height is None:
                if not isinstance(Width, int):
                    Error = UT_TypeError(Width, int, SkipFrames = 1)
                    Message = '{} - Width argument'.format(Error.args[0])
                    Error.args = (Message, )
                    raise Error
                if Width < 2:
                    raise UT_ValueError(Width, '>= 2 - Width argument',
                                                                SkipFrames = 1)
                _Width = Width
                _Height = int(floor(Length / Width))
                if _Height < 2:
                    raise UT_ValueError(Length,
                                '>= {} - sequence length'.format(2 * Width),
                                                                SkipFrames = 1)
            else:
                if not isinstance(Height, int):
                    Error = UT_TypeError(Height, int, SkipFrames = 1)
                    Message = '{} - Height argument'.format(Error.args[0])
                    Error.args = (Message, )
                    raise Error
                if Height < 2:
                    raise UT_ValueError(Height, '>= 2 - Height argument',
                                                                SkipFrames = 1)
                if not isinstance(Width, int):
                    Error = UT_TypeError(Width, int, SkipFrames = 1)
                    Message = '{} - Width argument'.format(Error.args[0])
                    Error.args = (Message, )
                    raise Error
                if Width < 2:
                    raise UT_ValueError(Width, '>= 2 - Width argument',
                                                                SkipFrames = 1)
                _Width = Width
                _Height = Height
            MinLength = _Width * _Height
            if Length < MinLength:
                raise UT_ValueError(Length,
                                '>= {} - sequence length'.format(MinLength),
                                                                SkipFrames = 1)
            if not isColumnsFirst:
                self._Elements = tuple(
                            tuple(seqValues[Index*_Width : (Index+1)*_Width])
                                                    for Index in range(_Height))
            else:
                self._Elements = tuple(tuple(seqValues[Outer + _Height * Inner]
                                                    for Inner in range(_Width))
                                                    for Outer in range(_Height))
        except UT_TypeError as err:
            _CheckIfSequenceRealSequence(seqValues)
            NItems = len(seqValues)
            if NItems < 2:
                raise UT_ValueError(NItems, '>= 2 - sequence length',
                                                                SkipFrames = 1)
            FirstLength = len(seqValues[0])
            if FirstLength < 2:
                raise UT_ValueError(NItems,
                                        '>= 2 - the first sub-sequence length',
                                                                SkipFrames = 1)
            for Index in range(1, NItems):
                CurrentLength = len(seqValues[Index])
                if CurrentLength != FirstLength:
                    raise UT_ValueError(CurrentLength,
                                '!= {} - sub-sequence index {} length'.format(
                                            FirstLength, Index), SkipFrames = 1)
            if not isColumnsFirst:
                self._Elements = tuple(tuple(seqValues[Index])
                                                    for Index in range(NItems))
            else:
                self._Elements = tuple(tuple(seqValues[HIndex][WIndex]
                                        for HIndex in range(NItems))
                                            for WIndex in range(FirstLength))
    
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
        Magic method to hook index access to a single element of an array or
        matrix in the form obj[i,j], where i is the column index, and j is the
        row index.
        
        Signature:
            tuple(int, int) -> int OR float
        
        Raises:
            UT_TypeError: either of the indexes is not an integer number, OR
                less or more than 2 indexes are provided
            UT_ValueError: the column index value is not in the inclusive range
                [-Width, Width - 1], OR the row index values is not in the
                inclusive range [-Height, Height - 1]
        
        Version 1.0.0.0
        """
        if not isinstance(Indexes, tuple):
            raise UT_TypeError(Indexes, tuple, SkipFrames = 1)
        if len(Indexes) != 2:
            raise UT_ValueError(len(Indexes), '== 2 - number of indexes',
                                                                SkipFrames = 1)
        Column, Row = Indexes
        Height = len(self._Elements)
        Width = len(self._Elements[0])
        if not isinstance(Column, int):
            Error = UT_TypeError(Column, int, SkipFrames = 1)
            Message = '{} - column index'.format(Error.args[0])
            Error.args = (Message, )
            raise Error
        if (Column < -Width) or (Column >= Width):
            raise UT_ValueError(Column,
                'in range [{}, {}]'.format(-Width, Width -1), SkipFrames = 1)
        if not isinstance(Row, int):
            Error = UT_TypeError(Row, int, SkipFrames = 1)
            Message = '{} - row index'.format(Error.args[0])
            Error.args = (Message, )
            raise Error
        if (Row < -Height) or (Row >= Height):
            raise UT_ValueError(Column,
                'in range [{}, {}]'.format(-Height, Height -1), SkipFrames = 1)
        return self._Elements[Row][Column]
    
    #public properties
    
    @property
    def Width(self) -> int:
        """
        Read-only property to access the width, i.e. number of columns of the
        array or matrix.
        
        Signature:
            None -> int >= 2
        
        Version 1.0.0.0
        """
        return len(self._Elements[0])
    
    @property
    def Height(self) -> int:
        """
        Read-only property to access the height, i.e. number of rows of the
        array or matrix.
        
        Signature:
            None -> int >= 2
        
        Version 1.0.0.0
        """
        return len(self._Elements)

    @property
    def Data(self) -> List[List[TReal]]:
        """
        Read-only property to access all elements of the array or matrix as a
        nested list of lists of real numbers.
        
        Signature:
            None -> list(list(int OR float))
        
        Version 1.0.0.0
        """
        return [list(Item) for Item in self._Elements]

class Vector:
    """
    Implementation of a generic, abstract vector. Must be instantiated with 2 or
    more real number typed arguments, with the number of the arguments defining
    the size / dimensions of the vector. Individual elements can be read-only
    accessed using integer indexing as obj[index], slicing is not supported.
    
    The instances of this class are immutable objects, and are not considered
    to be sequences, thus not supporting iteration and 'contains' check. But
    the entire stored data can be copied into a mutable Python sequence (list)
    using the property Data.
    
    Supports the following artihmetics:
        * Addition and subtraction of two generic vectors of equal length
        * Left and right mutliplication by a real number
        * Division by non-zero real number
        * Inner (dot) product of two equal length generic vectors -> real number
        * Outer product of two generic vectors -> Array2D
    
    Additionally, supports generation of orthogonal unity vectors of the
    specified dimensions and a normalized (unity geometric length) vector
    parallel to the one represented by the current instance.
    
    Properties:
        Size: (read-only) int >= 2
        Data: (read-only) list(int OR float)
        
    Class methods:
        generateOrtogonal(Length, Index):
            int >= 2, int >= 0 -> Vector
    
    Methods:
        normalize():
            None -> Vector
    
    Version 1.0.0.0
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
        _CheckIfRealSequence(args)
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
                                for Index, Item in enumerate(Other._Elements)]
        return self.__class__(*Elements)

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
                                for Index, Item in enumerate(Other._Elements)]
        return self.__class__(*Elements)

    def __mul__(self, Other: Union[TReal, TVector]) -> Union[TReal, TVector]:
        """
        Magic method implementing dot multiplication of two generic vectors and
        the generic vector times scalar operation.
        
        Signature:
            Vector OR int OR float -> Vector OR int OR float
        
        Args:
            Other: Vector OR int OR float; another instance of the same vector
                class of the same size or a real number as the right operand
        
        Returns:
            Vector: instance of the same class, which is the result of the
                operation with the real number right operand
            int OR float: result of the dot product of two generic vectors
        
        Raises:
            UT_TypeError: the second operand is not an instance of the same
                vector class nor a real number
            UT_ValueError: different sizes of the vectors in the case of the
                dot product
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Other, (int, float)):
            Elements = [Item * Other for Item in self._Elements]
            Result = self.__class__(*Elements)
        elif (isinstance(Other, self.__class__)
                                    and (Other.__class__ is self.__class__)):
            if Other.Size != self.Size:
                raise UT_ValueError(Other.Size,
                    '{} - vectors dimensions'.format(self.Size), SkipFrames = 1)
            Result = sum(Item * Other[Index]
                                for Index, Item in enumerate(self._Elements))
        else:
            raise UT_TypeError(Other, (int, float, self.__class__),
                                                                SkipFrames = 1)
        return Result
    
    def __rmul__(self, Other: TReal) -> TVector:
        """
        Magic method implementing scalar times generic vector operation.
        
        Signature:
            int OR float -> Vector
        
        Args:
            Other: int OR float; the left (scalar) operand
        
        Returns:
            Vector: instance of the same class, which is the result of the
                operation
        
        Raises:
            UT_TypeError: the second operand is not a real number
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Other, (int, float)):
            Elements = [Item * Other for Item in self._Elements]
            Result = self.__class__(*Elements)
        else:
            raise UT_TypeError(Other, (int, float), SkipFrames = 1)
        return Result
    
    def __truediv__(self, Other: TReal) -> TVector:
        """
        Magic method implementing division of a vector by a scalar
        
        Signature:
            int OR float -> 'Vector
        
        Args:
            Other: int OR float; the right (scalar) operand
        
        Returns:
            'Vector: instance of the same class, which is the result of the
                operation
        
        Raises:
            UT_TypeError: the second operand is not a real number
            UT_ValueError: the second operand is zero (division by zero)
        
        Version 1.0.0.0
        """
        if not isinstance(Other, (int, float)):
            raise UT_TypeError(Other, (int, float), SkipFrames = 1)
        if not Other:
            raise UT_ValueError(Other, '!= 0 - division by zero', SkipFrames= 1)
        Elements = [Item / Other for Item in self._Elements]
        Result = self.__class__(*Elements)
        return Result
    
    def __matmul__(self, Other: TVector) -> TArray:
        """
        Magic method implementing outer product of two generic vectors.
        
        Signature:
            Vector -> Array2D
        
        Args:
            Other: Vector; the right operand
        
        Returns:
            Array2D: instance of the class, which is the basis for the actual
                matrix classes
        
        Raises:
            UT_TypeError: the second operand is not an instance of the same
                class - sub-classes excluded
        
        Version 1.0.0.0
        """
        if ((not isinstance(Other, self.__class__))
                        or (not (Other.__class__ is self.__class__))):
            raise UT_TypeError(Other, self.__class__, SkipFrames = 1)
        Elements = [[Item * Element for Element in Other._Elements]
                                                    for Item in self._Elements]
        Result = Array2D(Elements)
        return Result
    
    def __pos__(self) -> TVector:
        """
        Magic method implementing unitaty plus operation (identity function).

        Signature:
            None -> 'Vector
        
        Returns:
            'Vector: instance of the same class, another object with the
                identical elements
        
        Version 1.0.0.0
        """
        return self.__class__(*(self._Elements))
    
    def __neg__(self) -> TVector:
        """
        Magic method implementing unitaty minus operation (negation / additive
        inverse function).

        Signature:
            None -> 'Vector
        
        Returns:
            'Vector: instance of the same class, another object with the
                identical elements
        
        Version 1.0.0.0
        """
        Elements = [-Item for Item in self._Elements]
        return self.__class__(*(Elements))
    
    def __iadd__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '+=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '+=' for the type {}".format(
                                                    self.__class__.__name__))
    
    def __isub__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '-=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '+-=' for the type {}".format(
                                                    self.__class__.__name__))
    
    def __imul__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '*=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '*=' for the type {}".format(
                                                    self.__class__.__name__))

    def __itruediv__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '/=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '/=' for the type {}".format(
                                                    self.__class__.__name__))

    def __imatmul__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '@=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '@=' for the type {}".format(
                                                    self.__class__.__name__))

    #public class methods
    
    @classmethod
    def generateOrtogonal(cls, Length: int, Index: int) -> TVector:
        """
        Class method to generate a vector from the unity orthogonal set such,
        that only a single element is 1, thereas all other elements are 0.
        
        Signature:
            int >= 2, int >= 0 -> 'Vector
        
        Args:
            Length: int >= 2; the request size / dimensions of the vector
            Index: int >= 0; the index on the only non-zero element, must be
                also less than Length
        
        Returns:
            'Vector: an instance of the same class
        
        Raises:
            UT_TypeError: either of the arguments in not an integer number
            UT_ValueError: the first argument is less than 2, OR the second
                argument is negative or equal to or greater than the first one
        
        Version 1.0.0.0
        """
        if not isinstance(Length, int):
            Error = UT_TypeError(Length, int, SkipFrames = 1)
            Error.args = ('{} - the first argument'.format(Error.args[0]), )
            raise Error
        if not isinstance(Index, int):
            Error = UT_TypeError(Index, int, SkipFrames = 1)
            Error.args = ('{} - the second argument'.format(Error.args[0]), )
            raise Error
        if Length < 2:
            raise UT_ValueError(Length, '>= 2 - requested size of the vector',
                                                                SkipFrames = 1)
        if Index < 0 or Index >= Length:
            raise UT_ValueError(Index,
                'in range [0, {}] - non-zero element index'.format(Length - 1),
                                                                SkipFrames = 1)
        Elements = [0 for _ in range(Length)]
        Elements[Index] = 1
        return cls(*Elements)
    
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
        Generates a new instance of the same class of the same length, but with
        all elements being scaled (divided by) a square root of the sum of all
        elements of the original vector squared.
        
        Signature:
            None -> 'Vector
        
        Returns:
            'Vector: a new instance of the same class - the normalized vector
        
        Raises:
            UT_ValueError: all elements of the original vector are zeroes
        
        Version 1.0.0.0
        """
        Length = sqrt(sum(Item*Item for Item in self._Elements))
        if not Length:
            raise UT_ValueError(Length, '> 0 - geometric length of the vector',
                                                                SkipFrames = 1)
        Elements = [Item / Length for Item in self._Elements]
        return self.__class__(*Elements)

class Column(Vector):
    """
    Implementation of a column vector. Must be instantiated with 2 or more real
    number typed arguments, with the number of the arguments defining the size /
    dimensions of the vector. Individual elements can be read-only accessed
    using integer indexing as obj[index], slicing is not supported.
    
    The instances of this class are immutable objects, and are not considered
    to be sequences, thus not supporting iteration and 'contains' check. But
    the entire stored data can be copied into a mutable Python sequence (list)
    using the property Data.
    
    Supports the following artihmetics:
        * Addition and subtraction of two column vectors of equal length
        * Left and right mutliplication by a real number
        * Division by non-zero real number
        * Right multiplication by a row vector -> Matrix
        * Left multiplication by a row vector of the same size -> real number
    
    Outer product is not supported. Multiplication with a matrix is delegated
    to the Matrix class.
    
    Additionally, supports generation of orthogonal unity vectors of the
    specified dimensions and a normalized (unity geometric length) vector
    parallel to the one represented by the current instance. Also implements
    transposition Column -> Row.
    
    Sub-classes Vector.
    
    Properties:
        Size: (read-only) int >= 2
        Data: (read-only) list(int OR float)
        
    Class methods:
        generateOrtogonal(Length, Index):
            int >= 2, int >= 0 -> Column
    
    Methods:
        normalize():
            None -> Column
        transpose():
            None -> Row
    
    Version 1.0.0.0
    """

    #special methods
    
    def __str__(self) -> str:
        """
        Magic method to support str() function with the vector as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return '[{}]^T'.format(', '.join(map(str, self._Elements)))

    def __mul__(self, Other: Union[TReal, TRow]) -> Union[TColumn, TMatrix]:
        """
        Magic method implementing right multiplication of a column vector by a
        scalar or row vector.
        
        Signature:
            Row OR int OR float -> Column OR Matrix
        
        Args:
            Other: Row OR int OR float; an instance of the row vector class
                or a real number as the right operand
        
        Returns:
            Column: instance of the same class, which is the result of the
                operation with the real number right operand
            Matrix: result of the column x row multiplication
        
        Raises:
            UT_TypeError: the second operand is not an instance of the same
                vector class nor a real number nor a Row vector
        
        Version 1.0.0.0
        """
        #will be patch after definition of the Matrix and Row classes
        return NotImplemented
    
    def __rmul__(self, Other: TReal) -> TColumn:
        """
        Magic method implementing left multiplication of a column vector by a
        scalar.
        
        Signature:
            int OR float -> Column
        
        Args:
            Other: int OR float; the left (scalar) operand
        
        Returns:
            Column: instance of the same class, which is the result of the
                operation
        
        Raises:
            UT_TypeError: the second operand is not a real number nor a Matrix
                instance
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Other, (int, float)):
            Elements = [Item * Other for Item in self._Elements]
            Result = self.__class__(*Elements)
        elif isinstance(Other, Array2D):
            Result = NotImplemented #responsibility of the Matrix class
        else:
            raise UT_TypeError(Other, (int, float), SkipFrames = 1)
        return Result
    
    def __matmul__(self, Other: Any) -> NotImplemented:
        """
        Disables the inherited outer product magic method.
        
        Version 1.0.0.0
        """
        return NotImplemented
    
    #public methods
    
    def transpose(self) -> TRow:
        """
        Transposes the current column vector into a row vector preserving the
        elements.
        
        Signature:
            None -> Row
        
        Version 1.0.0.0
        """
        return NotImplemented

class Row(Vector):
    """
    Implementation of a row vector. Must be instantiated with 2 or more real
    number typed arguments, with the number of the arguments defining the size /
    dimensions of the vector. Individual elements can be read-only accessed
    using integer indexing as obj[index], slicing is not supported.
    
    The instances of this class are immutable objects, and are not considered
    to be sequences, thus not supporting iteration and 'contains' check. But
    the entire stored data can be copied into a mutable Python sequence (list)
    using the property Data.
    
    Supports the following artihmetics:
        * Addition and subtraction of two row vectors of equal length
        * Left and right mutliplication by a real number
        * Division by non-zero real number
        * Left multiplication by a column vector -> Matrix
        * Right multiplication by a same size column vector -> real number
    
    Outer product is not supported. Multiplication with a matrix is delegated
    to the Matrix class.
    
    Additionally, supports generation of orthogonal unity vectors of the
    specified dimensions and a normalized (unity geometric length) vector
    parallel to the one represented by the current instance. Also implements
    transposition Row -> Column.
    
    Sub-classes Vector.
    
    Properties:
        Size: (read-only) int >= 2
        Data: (read-only) list(int OR float)
        
    Class methods:
        generateOrtogonal(Length, Index):
            int >= 2, int >= 0 -> Row
    
    Methods:
        normalize():
            None -> Row
        transpose():
            None -> Column
    
    Version 1.0.0.0
    """

    #special methods

    def __mul__(self, Other: Union[TReal, Column]) -> Union[TRow, TReal]:
        """
        Magic method implementing right multiplication of a row vector by a
        scalar or column vector.
        
        Signature:
            Column OR int OR float -> Row OR int OR float
        
        Args:
            Other: Column OR int OR float; an instance of the column vector
                class or a real number as the right operand
        
        Returns:
            Row: instance of the same class, which is the result of the
                operation with the real number right operand
            int OR float: result of the row x column multiplication
        
        Raises:
            UT_TypeError: the second operand is not an instance of the column
                vector class nor a real number, nor a Matrix instance
            UT_ValueError: different sizes of the vectors in the case of the
                row x column product
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Other, (int, float)):
            Elements = [Item * Other for Item in self._Elements]
            Result = self.__class__(*Elements)
        elif isinstance(Other, Column):
            if Other.Size != self.Size:
                raise UT_ValueError(Other.Size,
                    '{} - vectors dimensions'.format(self.Size), SkipFrames = 1)
            Result = sum(Item * Other[Index]
                                for Index, Item in enumerate(self._Elements))
        elif isinstance(Other, Array2D):
            Result = NotImplemented #responsibility of the Matrix class
        else:
            raise UT_TypeError(Other, (int, float, self.__class__),
                                                                SkipFrames = 1)
        return Result
    
    def __rmul__(self, Other: TReal) -> TRow:
        """
        Magic method implementing left multiplication of a row vector by a
        scalar.
        
        Signature:
            int OR float -> Row
        
        Args:
            Other: int OR float; a real number as the left operand
        
        Returns:
            Row: instance of the same class, which is the result of the
                operation
        
        Raises:
            UT_TypeError: the second operand is not a real number
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Other, (int, float)):
            Elements = [Item * Other for Item in self._Elements]
            Result = self.__class__(*Elements)
        else:
            raise UT_TypeError(Other, (int, float), SkipFrames = 1)
        return Result
    
    def __matmul__(self, Other: Any) -> NotImplemented:
        """
        Disables the inherited outer product magic method.
        
        Version 1.0.0.0
        """
        return NotImplemented
    
    #public methods
    
    def transpose(self) -> Column:
        """
        Transposes the current row vector into a column vector preserving the
        elements.
        
        Signature:
            None -> Column
        
        Version 1.0.0.0
        """
        return Column(*(self._Elements))

class Matrix(Array2D):
    """
    Implementation of a generic matrix.
    
    The data is stored and returned (property Data) as a sequence of the nested
    equal length sub-sequences of real numbers, each sub-sequence representing a
    single row of the matrix, i.e. in the rows-first order.
    
    The instances of this class are immutable objects, and are not considered
    to be sequences, thus not supporting iteration and 'contains' check. But
    the entire stored data can be copied into a mutable Python sequence (list)
    using the property Data. Individual element can be read-only accessed using
    double indexing as obj[col_index, row_index].
    
    Can be instantiated either from a flat sequence of real number, when either
    width or height or both must be specified; or from a nested sequence, in
    which case the width and height arguments are ignored even if provided. The
    default parsing order is rows-first, which can be switched to columns-first
    using a boolean keyword argument isColumnsFirst, which defaults to False.
    
    Thus, the supported instantiation call signatures are:
        * Matrix(list(int OR float), Width = int >= 2)
        * Matrix(list(int OR float), Height = int >= 2)
        * Matrix(list(int OR float), Width = int >= 2, Height = int >= 2)
        * Matrix(list(int OR float), Width = int >= 2)
        * Matrix(list(int OR float), Height = int >= 2)
        * Matrix(list(int OR float), Width = int >= 2, Height = int >= 2,
            isColumnsFirst = True)
        * Matrix(list(list(int OR float)))
        * Matrix(list(list(int OR float)), isColumnsFirst = True)
    
    Sub-classes Array2D and adds support for arithmetics between a matrices,
    column and row vectors, and scalars. Also adds transposition, columns and
    rows access methods.
    
    Properties:
        Width: (read-only) int >= 2
        Height: (read-only) int >= 2
        Data: (read-only) list(list(int OR float))
    
    Methods:
        transpose():
            None -> Matrix
        getColumn(Index):
            int -> Column
        getRow(Index):
            int -> Row
    
    Version 1.0.0.0
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
    
    def __iadd__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '+=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '+=' for the type {}".format(
                                                    self.__class__.__name__))
    
    def __isub__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '-=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '+-=' for the type {}".format(
                                                    self.__class__.__name__))
    
    def __imul__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '*=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '*=' for the type {}".format(
                                                    self.__class__.__name__))

    def __itruediv__(self, Other: Any) -> NoReturn:
        """
        Magic method to prohibit the '/=' operation.

        Signature:
            type A -> None
        
        Raises:
            TypeError: unconditionally.
        
        Version 1.0.0.0
        """
        raise TypeError("unsupported operation '/=' for the type {}".format(
                                                    self.__class__.__name__))
    
    #public methods
    
    def transpose(self) -> TMatrix:
        """
        """
        pass
    
    def getColumn(self, Index: int) -> Column:
        """
        Method to access a specific column of a matrix in the form of a column
        vector.
        
        Signature:
            int -> Column
        
        Args:
            Index: int; the required column index
        
        Raises:
            UT_TypeError: argument is not an integer number
            UT_ValueError: argument value is not in the inclusive range
                [-Width, Width - 1]
        
        Version 1.0.0.0
        """
        if not isinstance(Index, int):
            raise UT_TypeError(Index, int, SkipFrames = 1)
        Width = len(self._Elements[0])
        if (Index < - Width) or (Index >= Width):
            raise UT_ValueError(Index,
                'in range[{}, {}]'.format(-Width, Width - 1), SkipFrames = 1)
        Elements = [RowItem[Index] for RowItem in self._Elements]
        return Column(*Elements)
    
    def getRow(self, Index: int) -> Row:
        """
        Method to access a specific row of a matrix in the form of a row vector.
        
        Signature:
            int -> Row
        
        Args:
            Index: int; the required row index
        
        Raises:
            UT_TypeError: argument is not an integer number
            UT_ValueError: argument value is not in the inclusive range
                [-Height, Height - 1]
        
        Version 1.0.0.0
        """
        if not isinstance(Index, int):
            raise UT_TypeError(Index, int, SkipFrames = 1)
        Height = len(self._Elements)
        if (Index < - Height) or (Index >= Height):
            raise UT_ValueError(Index,
                'in range[{}, {}]'.format(-Height, Height - 1), SkipFrames = 1)
        return Row(*(self._Elements[Index]))

class SquareMatrix(Matrix):
    """
    Implementation of a square matrix, for which width equals height, and is
    referred to as simply size.
    
    The data is stored and returned (property Data) as a sequence of the nested
    equal length sub-sequences of real numbers, each sub-sequence representing a
    single row of the matrix, i.e. in the rows-first order.
    
    The instances of this class are immutable objects, and are not considered
    to be sequences, thus not supporting iteration and 'contains' check. But
    the entire stored data can be copied into a mutable Python sequence (list)
    using the property Data. Individual element can be read-only accessed using
    double indexing as obj[col_index, row_index].
    
    Can be instantiated either from a flat sequence of real number, when the
    required size may be specified via a keyword argument, or it may
    auto-deducted; or from a nested sequence, in which case the size arguments
    is ignored even if provided. The default parsing order is rows-first, which
    can be switched to columns-first using a boolean keyword argument
    isColumnsFirst, which defaults to False.
    
    Thus, the supported instantiation call signatures are:
        * SquareMatrix(list(int OR float))
        * SquareMatrix(list(int OR float), isColumnsFirst = True)
        * SquareMatrix(list(int OR float), Size = int >= 2)
        * SquareMatrix(list(int OR float), Size = int >= 2,
            isColumnsFirst = True)
        * SquareMatrix(list(list(int OR float)))
        * SquareMatrix(list(list(int OR float)), isColumnsFirst = True)
    
    Sub-classes Matrix and supports for arithmetics between a matrices,
    column and row vectors, and scalars as well as transposition, columns and
    rows access methods. Also adds adds a number of class and instance methods
    specific for the square matrices:
        * calculation of the trace and determinant
        * LUP and LUDP (full) decomposition
        * Generation of the multuplicative inverse matrix
        * Calculation of eigenvalues and eigenvectors
    
    Properties:
        Width: (read-only) int >= 2
        Height: (read-only) int >= 2
        Size: (read-only) int >= 2
        Data: (read-only) list(list(int OR float))
    
    Class methods:
        generateIdentity(Size):
            int >= 2 -> SquareMatrix
        generatePermutation(Permutation):
            seq(int >= 0) -> SquareMatrix
    
    Methods:
        transpose():
            None -> SquareMatrix
        getColumn(Index):
            int -> Column
        getRow(Index):
            int -> Row
        getTrace():
            None -> int OR float
        getLUPdecomposition():
            None -> SquareMatrix, SquareMatrix, tuple(int OR float), int
        getFullDecomposition():
            None -> SquareMatrix, SquareMatrix, SquareMatrix,
                tuple(int OR float), int
        getDeterminant():
            None -> int OR float
        getInverse():
            None -> SquareMatrix OR None
        getEigenValues():
            None -> tuple(int OR float) OR None
        getEigenVectors():
            None -> dict(int OR float -> tuple(Column)) OR None
    
    Version 1.0.0.0
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
                                *, Size : Optional[int] = None,
                                        isColumnsFirst : bool = False) -> None:
        """
        Instantiation method. Parses the passed data sequence and packs it into
        the internally stored nested tuple structure representing a matrix, with
        each tuple element representing a single row of that matrix.
        
        Signature:
            seq(int OR float) OR seq(seq(int OR float))/, int >= 2 OR None,
                bool/ -> None
        
        Args:
            seqValues: seq(int OR float) OR seq(seq(int OR float)); elements
                of the array / matrix, in the flat form the total number of
                elements must be equal to or greater than Size*Size if it is
                specified, or > 4 if Size is not specified or None, in the
                nested form the length of each element must be equal to their
                count
            Size: (keyword) int >= 2 OR None; required size = width = height of
                the matrix, defaults to None meaning automatic definition based
                on the length of the flat sequence argument
            isColumnsFirst: (keyword) bool; flag if the passed data to parsed
                in the columns-first order, defaults to False, i.e. rows-first
                order when each consequitive slice of a flat sequence or
                sub-sequence element of a nested sequence is treated as the
                representation of a single row of the array or matrix
        
        Raises:
            UT_TypeError: mandatory argument is neither a flat sequence of real
                numbers nor a nested sequence of sequences of real numbers, OR
                optional keyword argument isColumnsFirst is not boolean, OR
                optional keyword arguments Size is neither None nor an integer
                number
            UT_ValueError: Size argument is an integer < 2, OR the length of a
                flat sequence as the mandatory argument is too short for the
                given values of Size, OR a nested sequence as the mandatory
                argument has less than 2 elements, OR the length of an
                sub-sequence element is less than 2, OR the sub-sequence
                elements differ in length, OR length of the sub-sequence element
                is not equal to their number
        
        Version 1.0.0.0
        """
        if not isinstance(isColumnsFirst, bool):
            Error = UT_TypeError(isColumnsFirst, bool, SkipFrames = 1)
            Message = '{} - isColumnsFirst argument'.format(Error.args[0])
            Error.args = (Message, )
            raise Error
        try:
            _CheckIfRealSequence(seqValues)
            Length = len(seqValues)
            if (not isinstance(Size, int)) and (not (Size is None)):
                Error = UT_TypeError(Size, int, SkipFrames = 1)
                Message = '{} - Size argument'.format(Error.args[0])
                Error.args = (Message, )
                raise Error
            if Size is None:
                if Length < 4:
                    raise UT_ValueError(Length, '>= 4 - sequence length',
                                                                SkipFrames = 1)
                _Size = int(floor(sqrt(Length)))
            else:
                if Size < 2:
                    raise UT_ValueError(Size, '>= 2 - requested matrix size',
                                                                SkipFrames = 1)
                MinLength = Size * Size
                if Length < MinLength:
                    raise UT_ValueError(Length,
                                    '>= {} - sequence length'.format(MinLength),
                                                                SkipFrames = 1)
                _Size = Size
            if not isColumnsFirst:
                self._Elements = tuple(
                            tuple(seqValues[Index*_Size : (Index+1)*_Size])
                                                    for Index in range(_Size))
            else:
                self._Elements = tuple(tuple(seqValues[Outer + _Size * Inner]
                                                    for Inner in range(_Size))
                                                    for Outer in range(_Size))
        except UT_TypeError as err:
            _CheckIfSequenceRealSequence(seqValues)
            NItems = len(seqValues)
            if NItems < 2:
                raise UT_ValueError(NItems, '>= 2 - sequence length',
                                                                SkipFrames = 1)
            FirstLength = len(seqValues[0])
            if FirstLength < 2:
                raise UT_ValueError(NItems,
                                        '>= 2 - the first sub-sequence length',
                                                                SkipFrames = 1)
            for Index in range(1, NItems):
                CurrentLength = len(seqValues[Index])
                if CurrentLength != FirstLength:
                    raise UT_ValueError(CurrentLength,
                                '!= {} - sub-sequence index {} length'.format(
                                            FirstLength, Index), SkipFrames = 1)
            if FirstLength != NItems:
                raise UT_ValueError(FirstLength,
                    '= {} - mismatching width and height of the matrix'.format(
                                                        NItems), SkipFrames = 1)
            if not isColumnsFirst:
                self._Elements = tuple(tuple(seqValues[Index])
                                                    for Index in range(NItems))
            else:
                self._Elements = tuple(tuple(seqValues[HIndex][WIndex]
                                        for HIndex in range(NItems))
                                            for WIndex in range(FirstLength))
    
    #public properties
    
    @property
    def Size(self) -> int:
        """
        Read-only property to access the size of a square matrix, which is
        equal to its width and its height.
        
        Signature:
            None -> int >= 2
        
        Version 1.0.0.0
        """
        return len(self._Elements)
    
    #public instance methods
    
    def getTrace(self) -> TReal:
        """
        Signature:
            None -> int OR float
        """
        pass
    
    def getLUPdecomposition(self) -> Tuple[TSquareMatrix, TSquareMatrix,
                                                            TRealTuple, int]:
        """
        Signature:
            None -> SquareMatrix, SquareMatrix, tuple(int OR float), int
        """
        pass
    
    def getFullDecomposition(self) -> Tuple[TSquareMatrix, TSquareMatrix,
                                                TSquareMatrix, TRealTuple, int]:
        """
        Signature:
            None -> SquareMatrix, SquareMatrix, SquareMatrix,
                tuple(int OR float), int
        """
        pass
    
    def getDeterminant(self) -> TReal:
        """
        Signature:
            None -> int OR float
        """
        pass
    
    def getInverse(self) -> Union[TSquareMatrix, None]:
        """
        Signature:
            None -> SquareMatrix OR None
        """
        pass
    
    def getEigenValues(self) -> Union[TRealTuple, None]:
        """
        Signature:
            None -> tuple(int OR float) OR None
        """
        pass
    
    def getEigenVectors(self) -> Union[Dict[TReal, Tuple[TColumn, ...]], None]:
        """
        Signature:
            None -> dict(int OR float -> tuple(Column)) OR None
        """
        pass

#Dynamic patching of the Column class, instance method __mul__()

def _Column__mul__(self: Column,
                            Other: Union[Row, TReal]) -> Union[Column, Matrix]:
    """
    Special helper function to patch the right multiplication of a Column vector
    hook magical method.
    
    Signature:
        Column, Row OR int OR float -> Column OR Matrix
    
    Args:
        self: Column; instance of Column class as the left operand
        Other: Row OR int OR float; an instance of the row vector class or a
            real number as the right operand
    
    Returns:
        Column: instance of the Column class, which is the result of the
            operation with the real number right operand
        Matrix: result of the column x row multiplication
    
    Raises:
        UT_TypeError: the second operand is not an instance of the Row vector
            vector class nor a real number
        
    Version 1.0.0.0
    """
    Result = None
    if isinstance(Other, (int, float)):
        Elements = [Item * Other for Item in self._Elements]
        Result = self.__class__(*Elements)
    elif isinstance(Other, Row):
        Elements = [[Item * Element for Element in Other._Elements]
                                                    for Item in self._Elements]
        Result = Matrix(Elements)
    else:
        raise UT_TypeError(Other, (int, float), SkipFrames = 1)
    return Result

#Dynamic patching of the Column class, instance method transpose()

def _Column_transpose(self: Column) -> Row:
    """
    Special helper function to patch the transpose() method of the Column class.
        
    Signature:
        Column -> Row
    
    Args:
        self: Column; an instance of the class.
    
    Version 1.0.0.0
    """
    return Row(*(self._Elements))

#tweaking and patching the classes

TempDoc = Column.__mul__.__doc__
setattr(Column, "__mul__", _Column__mul__)
Column.__mul__.__doc__ = TempDoc
TempDoc = Column.transpose.__doc__
setattr(Column, "transpose", _Column_transpose)
Column.transpose.__doc__ = TempDoc