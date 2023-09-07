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
__date__ = '07-09-2023'
__status__ = 'Production'

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
from introspection_lib.base_exceptions import GetObjectClass, UT_Exception

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

#globals

MAX_ITER = 100000 #maximum number of iterations for the QR-algorithm

ALMOST_ZERO = 1.0E-14 #threshold for the convergence of the QR-algorithm

DEBUG_MODE = False #if True - will print fault messages of the QR-algorithm

#helper functions

#+ input data types

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
            Error.appendMessage(f'at index {Index} in {Value}')
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
            Error.appendMessage(f'at index {Index} in {Value}')
            raise Error
        for Inner, Element in enumerate(Item):
            if not isinstance(Element, (int, float)):
                Error = UT_TypeError(Element, (int, float), SkipFrames = 2)
                Error.appendMessage(f'at index [{Index}][{Inner}] in {Value}')
                raise Error

#+ Gram-Schmidt and QR decomposition related

def _Dot(Vector1: Sequence[TReal], Vector2: Sequence[TReal]) -> TReal:
    """
    Calculates the dot product of two vectors, passed as generic sequences.
    It does not any data sanity checks! It is not supposed to be used outside
    the module.
    
    Signature:
        seq(int OR float), seq(int OR float) -> int OR float
    
    Version 1.0.0.0
    """
    return sum([Vector1[Idx] * Vector2[Idx] for Idx in range(len(Vector1))])

def _Norm(Vector: Sequence[TReal]) -> float:
    """
    Calculates the norm (length) of a vector, passed as generic sequence. Note:
    it does not any data sanity checks! It is not supposed to be used outside
    the module.
    
    Signature:
        seq(int OR float) -> float
    
    Version 1.0.0.0
    """
    return sqrt(sum([Item * Item for Item in Vector]))

def _NormSquared(Vector: Sequence[TReal]) -> float:
    """
    Calculates the square of the norm (length) of a vector, passed as generic
    sequence. Note: it does not any data sanity checks! It is not supposed to be
    used outside the module.
    
    Signature:
        seq(int OR float) -> float
    
    Version 1.0.0.0
    """
    return sum([Item * Item for Item in Vector])

def _Project(Vector1: Sequence[TReal], Vector2: Sequence[TReal]) -> List[float]:
    """
    Calculates the projection of the second vector onto the first vector, which
    are both passed as generic sequences. It does not any data sanity checks!
    It is not supposed to be used outside the module.
    
    Signature:
        seq(int OR float), seq(int OR float) -> list(float)
    
    Raises:
        UT_Exception: the first vector has zero 'length' - all elements are zero
    
    Version 1.0.0.0
    """
    Divider = _NormSquared(Vector1)
    if not Divider:
        raise UT_Exception('Zero length vector.')
    Coeff = _Dot(Vector1, Vector2) / Divider
    return [Coeff * Item for Item in Vector1]

def _GetOrthonormal(Vectors: Sequence[Sequence[TReal]]) -> List[List[float]]:
    """
    Calculates a set of orthonormal (orthogonal and of the unity length) set of
    vectors based on the passed set of vectors (as generic sequences of real
    numbers). It does not any data sanity checks! It is not supposed to be used
    outside the module.
    
    This is the modified Gram-Schmidt algorithm.
    
    Signature:
        seq(seq(int OR float)) -> list(list(float))
    
    Raises:
        UT_Exception: set cannot be orthogonolized, there are linear dependent
            vectors (or zero 'length' ones) in the set
    
    Version 1.0.0.0
    """
    NVectors = len(Vectors)
    VectorLenght = len(Vectors[0])
    Data = [list(Vectors[Idx]) for Idx in range(NVectors)]
    for Iteration in range(NVectors - 1):
        for Idx in range(Iteration + 1, NVectors):
            Previous = Data[Idx]
            Projection = _Project(Data[Iteration], Previous)
            Data[Idx] = [Data[Idx][ItemIdx] - Projection[ItemIdx]
                                            for ItemIdx in range(VectorLenght)]
    Result = []
    for Vector in Data:
        Norm = _Norm(Vector)
        if not Norm:
            raise UT_Exception('Linear dependent vectors.')
        Normalized = [Element / Norm for Element in Vector]
        #beautification, reduces effect of rounding errors in nearly orthogonal
        #+ initial input case
        for Index, Value in enumerate(Normalized):
            if abs(Value) < ALMOST_ZERO:
                Normalized[Index] = 0
            elif abs(abs(Value) - 1) < ALMOST_ZERO:
                Normalized[Index] = 1
        Result.append(Normalized)
    return Result

#+ QR-algorithm related (Francis, Kublanovskaya)

def _FindEigenValuesQR(Vectors: Sequence[Sequence[TReal]]) -> Tuple[
                                                Union[List[TReal], None], str]:
    """
    Implementation of the QR-algorithm by Francis and Kublanovskaya for finding
    the eigenvalues of a square matrix.
    
    Signature:
        seq(seq(int OR float)) -> list(int OR float) OR None, str
    
    Args:
        seq(seq(int OR float)): the matrix elements packed into nested sequences
            in the columns-first order
    
    Returns:
        list(int OR float), str: unpacked tuple of the list of the unique real
            number value eigenvalues and a string message ('Ok')
        None, str: unpacked tuple of the None value to indicate the failure of
            the algorithm and a string message explaining the reason
    
    Version 1.0.0.0
    """
    DoStop = False
    Counter = 0
    Size = len(Vectors)
    A = Vectors #orginal matrix in the columns-first order
    while (not DoStop) and (Counter < MAX_ITER):
        try:
            Q = _GetOrthonormal(A) #Q-matrix as the set of orthonormal vectors
        except UT_Exception:
            break
        #Q-matrix convergence test - check if it is almost an identity matrix
        IsIdentity = True
        for ColIdx in range(Size):
            for RowIdx, Item in enumerate(Q[ColIdx]):
                if RowIdx == ColIdx:
                    Check = abs(Q[ColIdx][RowIdx]-1) < ALMOST_ZERO
                else:
                    Check = abs(Q[ColIdx][RowIdx]) < ALMOST_ZERO
                IsIdentity = Check
                if not Check:
                    break
            if not IsIdentity:
                break
        if IsIdentity:
            DoStop = True
        else:
            R = [[_Dot(A[ColIdx], Q[RowIdx]) if RowIdx <= ColIdx else 0
                        for RowIdx in range(Size)] for ColIdx in range(Size)]
            #R-matrix, projection, such that A{k-1} = Q{k-1} * R{k-1}
            A = [[sum([R[Idx][RowIdx] * Q[ColIdx][Idx] for Idx in range(Size)])
                        for RowIdx in range(Size)] for ColIdx in range(Size)]
            #next iteration A{k} = R{k-1} * Q{k-1}
        Counter += 1
    if DoStop:
        Elements = [A[Idx][Idx] for Idx in range(Size)]
        Elements = [int(round(Item))
                        if abs(Item - round(Item)) < Size*Size*Size*ALMOST_ZERO
                                                else Item for Item in Elements]
        #QR convergence is ~ O(N^3), hence the estimation of rounding error
        Result = []
        for Item in Elements:
            if not Item:
                continue
            IsNotPresent = True
            for AddedItem in Result:
                if abs((AddedItem - Item)/(AddedItem)) < ALMOST_ZERO:
                    IsNotPresent = False
                    break
            if IsNotPresent:
                Result.append(Item)
        Message = 'Ok!'
    elif Counter < MAX_ITER:
        Result = None
        Message = 'Matrix cannot be orthogonolized - linear dependent columns.'
    else:
        Result = None
        Message = 'Maximum number of iterations is reached - not converging.'
    return Result, Message

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
            Error.appendMessage('- isColumnsFirst argument')
            raise Error
        if ((not isinstance(seqValues, c_abc.Sequence))
                                                or isinstance(seqValues, str)):
            raise UT_TypeError(seqValues, (list, tuple), SkipFrames = 1)
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
                    Error.appendMessage('- Height argument')
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
                    Error.appendMessage('- Width argument')
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
                    Error.appendMessage('- Height argument')
                    raise Error
                if Height < 2:
                    raise UT_ValueError(Height, '>= 2 - Height argument',
                                                                SkipFrames = 1)
                if not isinstance(Width, int):
                    Error = UT_TypeError(Width, int, SkipFrames = 1)
                    Error.appendMessage('- Width argumen')
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
        Magic method to support str() function with the array as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return '\n{}\n'.format('\n'.join(['|{}|'.format(
                                        ', '.join([str(Item) for Item in Row]))
                                                    for Row in self._Elements]))
    
    def __repr__(self) -> str:
        """
        Magic method to support str() function with the array or matrix as its
        argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return "'{}(Width={}, Height={})'".format(self.__class__.__name__,
                                    len(self._Elements[0]), len(self._Elements))
    
    def __iter__(self) -> NoReturn:
        """
        Magic method to hook the iterator protocol, which should not be
        supported. As the desired consequence, the 'contains' check is also
        disabled.
        
        Raises:
            TypeError: as expected from a non-iterable type
        
        Version 1.0.0.0
        """
        raise TypeError(f"'{self.__class__.__name__}' object is not iterable")
    
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
            Error.appendMessage('- column index')
            raise Error
        if (Column < -Width) or (Column >= Width):
            raise UT_ValueError(Column, f'in range [{-Width}, {Width - 1}]',
                                                                SkipFrames = 1)
        if not isinstance(Row, int):
            Error = UT_TypeError(Row, int, SkipFrames = 1)
            Error.appendMessage('- row index')
            raise Error
        if (Row < -Height) or (Row >= Height):
            raise UT_ValueError(Column, f'in range [{-Height}, {Height - 1}]',
                                                                SkipFrames = 1)
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
        generateOrthogonal(Length, Index):
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
        return '|{}|'.format(', '.join(map(str, self._Elements)))
    
    def __repr__(self) -> str:
        """
        Magic method to support repr() function with the vector as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return f"'{self.__class__.__name__}(Size={len(self._Elements)})'"
    
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
            raise UT_ValueError(Index,
                f'in range [{-Size}, {Size - 1}] - indexing', SkipFrames = 1)
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
        raise TypeError(f"'{self.__class__.__name__}' object is not iterable")
    
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
            raise UT_ValueError(Other.Size, f'{self.Size} - vectors dimensions',
                                                                SkipFrames = 1)
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
            raise UT_ValueError(Other.Size, f'{self.Size} - vectors dimensions',
                                                                SkipFrames = 1)
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
                        f'{self.Size} - vectors dimensions', SkipFrames = 1)
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
    def generateOrthogonal(cls, Length: int, Index: int) -> TVector:
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
            Error.appendMessage('- the first argument')
            raise Error
        if not isinstance(Index, int):
            Error = UT_TypeError(Index, int, SkipFrames = 1)
            Error.appendMessage('- the second argument')
            raise Error
        if Length < 2:
            raise UT_ValueError(Length, '>= 2 - requested size of the vector',
                                                                SkipFrames = 1)
        if Index < 0 or Index >= Length:
            raise UT_ValueError(Index,
                        f'in range [0, {Length - 1}] - non-zero element index',
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
        Elements = []
        for RealItem in self._Elements:
            Item = RealItem / Length
            #beautify only if along one of the orthonormal vectors (coordinates)
            if abs(Item) < ALMOST_ZERO:
                Item = 0
            elif abs(abs(Item) - 1) < ALMOST_ZERO:
                Item = 1
            Elements.append(Item)
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
        generateOrthogonal(Length, Index):
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
        return '|{}|^T'.format(', '.join(map(str, self._Elements)))
    
    # Is overloaded later
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
    
    # Is overloaded later
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
        generateOrthogonal(Length, Index):
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
                        f'{self.Size} - vectors dimensions', SkipFrames = 1)
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

    def __str__(self) -> str:
        """
        Magic method to support str() function with the matrix as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return '\n{}\n'.format('\n'.join(['||{}||'.format(
                                        ', '.join([str(Item) for Item in Row]))
                                                    for Row in self._Elements]))
    
    def __add__(self, Other: TMatrix) -> TMatrix:
        """
        Magic method implementing addition of two matrices of the same sizes.

        Signature:
            'Matrix -> 'Matrix
        
        Args:
            Other: 'Matrix; another instance of the generic or square matrix
                same size
        
        Returns:
            'Matrix: instance of the generic or square matrix class, which is
                the result of the operation; square matrix is returned only if
                one of the arguments is an instance of square matrix class
        
        Raises:
            UT_TypeError: the second operand is not an instance of the matrix
                (sub-) class
            UT_ValueError: different sizes of the matrices
        
        Version 1.0.0.0
        """
        if (not isinstance(Other, self.__class__)) and (
                                        not isinstance(self, Other.__class__)):
            Error = UT_TypeError(Other, self.__class__, SkipFrames = 1)
            Message = 'incompatible types {} and {} for addition'.format(
                                        self.__class__, GetObjectClass(Other))
            Error.setMessage(Message)
            raise Error
        elif isinstance(Other, self.__class__) and (
                                        not isinstance(self, Other.__class__)):
            ResultClass = Other.__class__
        else:
            ResultClass = self.__class__
        selfWidth = len(self._Elements)
        selfHeight = len(self._Elements[0])
        otherWidth = len(Other._Elements)
        otherHeight = len(Other._Elements[0])
        if selfWidth != otherWidth:
            raise UT_ValueError(otherWidth, f'={otherWidth} - matrices widths',
                                                                SkipFrames = 1)
        elif selfHeight != otherHeight:
            raise UT_ValueError(otherHeight,
                        f'={otherHeight} - matrices heights', SkipFrames = 1)
        Elements = list()
        for Row in range(self.Height):
            RowItems = list([Item + Other._Elements[Row][Index]
                             for Index, Item in enumerate(self._Elements[Row])])
            Elements.append(RowItems)
        return ResultClass(Elements)
    
    def __sub__(self, Other: TMatrix) -> TMatrix:
        """
        Magic method implementing subtraction of two matrices of the same sizes.

        Signature:
            'Matrix -> 'Matrix
        
        Args:
            Other: 'Matrix; another instance of the generic or square matrix
                same size
        
        Returns:
            'Matrix: instance of the generic or square matrix class, which is
                the result of the operation; square matrix is returned only if
                one of the arguments is an instance of square matrix class
        
        Raises:
            UT_TypeError: the second operand is not an instance of the matrix
                (sub-) class
            UT_ValueError: different sizes of the matrices
        
        Version 1.0.0.0
        """
        if (not isinstance(Other, self.__class__)) and (
                                        not isinstance(self, Other.__class__)):
            Error = UT_TypeError(Other, self.__class__, SkipFrames = 1)
            Message = 'incompatible types {} and {} for addition'.format(
                                        self.__class__, GetObjectClass(Other))
            Error.setMessage(Message)
            raise Error
        elif isinstance(Other, self.__class__) and (
                                        not isinstance(self, Other.__class__)):
            ResultClass = Other.__class__
        else:
            ResultClass = self.__class__
        selfWidth = len(self._Elements)
        selfHeight = len(self._Elements[0])
        otherWidth = len(Other._Elements)
        otherHeight = len(Other._Elements[0])
        if selfWidth != otherWidth:
            raise UT_ValueError(otherWidth, f'={otherWidth} - matrices widths',
                                                                SkipFrames = 1)
        elif selfHeight != otherHeight:
            raise UT_ValueError(otherHeight,
                        f'={otherHeight} - matrices heights', SkipFrames = 1)
        Elements = list()
        for Row in range(self.Height):
            RowItems = list([Item - Other._Elements[Row][Index]
                             for Index, Item in enumerate(self._Elements[Row])])
            Elements.append(RowItems)
        return ResultClass(Elements)
    
    # Is overloaded later
    def __mul__(self, Other: Union[TReal, Column, TMatrix]
                                                ) -> Union[Column, TMatrix]:
        """
        Magic method implementing multiplication of two matrices, right
        multiplication of a matrix by a column vector or by a scalar.

        Signature:
            'Matrix OR Column OR int OR float -> 'Matrix OR Column
        
        Args:
            Other: 'Matrix OR Column OR int OR float; another instance of the
                generic or square matrix with height equal to the width of the
                left operand, or an instance of the Column vector class with
                length equal to the width of the left operand, or a real number
        
        Returns:
            'Matrix: instance of the generic or square matrix class, which is
                the result of the matrix by matrix or matrix by scalar
                multiplication; a square matrix sub-type is returned only if
                the width and height of the resulting (generic) matrix are equal
            Column: instance of the column vector class, which is the result of
                the matrix by column multiplication
        
        Raises:
            UT_TypeError: the second operand is neither a matrix nor a column
                vector nor a real number
            UT_ValueError: for two matrices left operand width is not equal to
                the right operand height, OR the length of the column is not
                equal to the width of the matrix
        
        Version 1.0.0.0
        """
        return NotImplemented
    
    def __rmul__(self, Other: Union[TReal, Row]) -> Union[Row, TMatrix]:
        """
        Magic method implementing multiplication of two matrices, right
        multiplication of a matrix by a column vector or by a scalar.

        Signature:
            Row OR int OR float -> 'Matrix OR Row
        
        Args:
            Other: Row OR int OR float; an instance of the Row vector class with
                length equal to the height of the right operand, or a real
                number
        
        Returns:
            'Matrix: instance of the same (generic or square) matrix class,
                which is the result of the matrix by scalar multiplication
            Row: instance of the row vector class, which is the result of
                the row vector by matrix multiplication
        
        Raises:
            UT_TypeError: the second operand is neither a row vector nor a real
                number
            UT_ValueError: the length of the column vector is not equal to the
                height of the matrix
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Other, (int, float)):
            Elements = [[Item * Other for Item in tupRow]
                                                for tupRow in self._Elements]
            Result = self.__class__(Elements)
        elif isinstance(Other, Row):
            Height = len(self._Elements)
            Width = len(self._Elements[0])
            Length = len(Other._Elements)
            if Length != Height:
                raise UT_ValueError(Length,
                            f'== {Height} - row vector size != matrix height',
                                                                SkipFrames = 1)
            Elements = [sum(
                        self._Elements[RowIndex][ColumnIndex] * Other[RowIndex]
                                    for RowIndex in range(Height))
                                                for ColumnIndex in range(Width)]
            Result = Row(*Elements)
        else:
            raise UT_TypeError(Other, (int, float, Row), SkipFrames = 1)
        return Result
    
    def __truediv__(self, Other: TReal) -> TMatrix:
        """
        Magic method implementing division of a matrix by a real number.

        Signature:
            int OR float -> 'Matrix
        
        Args:
            Other: int OR float; a real number as the divisor
        
        Returns:
            'Matrix: instance of the same (generic or square) matrix class,
                which is the result of the operation
        
        Raises:
            UT_TypeError: the second operand is not a real number
            UT_ValueError: the divisor is zero
        
        Version 1.0.0.0
        """
        Result = None
        if isinstance(Other, (int, float)):
            if Other == 0:
                raise UT_ValueError(Other, '!= 0 - division by zero',
                                                                SkipFrames = 1)
            Elements= [[Item / Other for Item in Row] for Row in self._Elements]
            Result = self.__class__(Elements)
        else:
            raise UT_TypeError(Other, (int, float), SkipFrames = 1)
        return Result
    
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
        Method to generate a transposition of the current matrix (new instance
        of the same class).

        Signature:
            None -> 'Matrix
        
        Version 1.0.0.0
        """
        return self.__class__(self._Elements, isColumnsFirst = True)
    
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
            raise UT_ValueError(Index, f'in range[{-Width}, {Width - 1}]',
                                                                SkipFrames = 1)
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
            raise UT_ValueError(Index, f'in range[{-Height}, {Height - 1}]',
                                                                SkipFrames = 1)
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
            int > 1 -> SquareMatrix
        generatePermutation(Permutation):
            seq(int >= 0) -> SquareMatrix
        generateDiagonal(Elements):
            seq(int OR floar) -> SquareMatrix
    
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
            None -> SquareMatrix, SquareMatrix, tuple(int), tuple(int), int
        getFullDecomposition():
            None -> SquareMatrix, SquareMatrix, tuple(int OR float), tuple(int),
                tuple(int), int
        getDeterminant():
            None -> int OR float
        getInverse():
            None -> SquareMatrix OR None
        getEigenValues():
            None -> tuple(int OR float) OR None
        getEigenVectors():
            /int OR float/ -> dict(int OR float -> tuple(Column) OR None)
                OR None
    
    Version 1.0.0.0
    """
    
    #public class methods
    
    @classmethod
    def generateIdentity(cls, Size: int) -> TSquareMatrix:
        """
        Creates a new instance of a square matrix with all elements on the
        main diagonal being equal to 1, and all other elements being zeroes.
        Class method.

        Signature:
            int > 1 -> SquareMatrix
        
        Args:
            Size: int > 1; the requested size of the identity matrix
        
        Returns:
            SquareMatrix: a new instance of the class
        
        Raises:
            UT_TypeError: the passed argument is not an integer number
            UT_ValueError: the passed argument is an integer, but less than 2
        
        Version 1.0.0.0
        """
        if not isinstance(Size, int):
            raise UT_TypeError(Size, int, SkipFrames = 1)
        if Size < 2:
            raise UT_ValueError(Size, '> 1 - matrix size', SkipFrames = 1)
        Elements = [[1 if ColIdx == RowIdx else 0 for ColIdx in range(Size)]
                                                    for RowIdx in range(Size)]
        return cls(Elements)
    
    @classmethod
    def generatePermutation(cls, Permutation: Sequence[int]) -> TSquareMatrix:
        """
        Generates a permutation matrix of the size N from the passed 0..N-1
        numbers permutation sequence. Basically, the identity matrix with some
        columns (or rows) shufled. Class method.

        Signature:
            seq(int >= 0) -> SquareMatrix

        Args:
            Permutation: seq(int >= 0); a proper 0..N-1 permutation sequence
        
        Returns:
            SquareMatrix: a new instance of the class
        
        Raises:
            UT_TypeError: the passed argument is not a sequence of integer
                numbers
            UT_ValueError: the sequence is shorter that 2 elements, OR any of
                the elements is negative OR equal to or greater than the
                sequence length, OR any of the elements is not unique.
        
        Version 1.0.0.0
        """
        if (not isinstance(Permutation, c_abc.Sequence) or
                                                isinstance(Permutation, str)):
            raise UT_TypeError(Permutation, (list, tuple), SkipFrames = 1)
        Size = len(Permutation)
        if Size < 2:
            raise UT_ValueError(Size, '> 1 - sequence length', SkipFrames = 1)
        Elements = list()
        for Index, Item in enumerate(Permutation):
            PostFix = f'- element at index {Index} in {Permutation}'
            if not isinstance(Item, int):
                Error = UT_TypeError(Item, int, SkipFrames = 1)
                Error.appendMessage(PostFix)
                raise Error
            if Item < 0 or Item >= Size:
                Message = f'in range [0, {Size - 1}] {PostFix}'
                raise UT_ValueError(Item, Message, SkipFrames = 1)
            if not (Item in Elements):
                Elements.append(Item)
            else:
                raise UT_ValueError(Item,
                                    'all elements are unique{}'.format(PostFix),
                                                                SkipFrames = 1)
        Elements = [[1 if ColIdx == Index else 0 for ColIdx in range(Size)]
                                                    for Index in Permutation]
        return cls(Elements)
    
    @classmethod
    def generateDiagonal(cls, Elements: Sequence[TReal]) -> TSquareMatrix:
        """
        Generates a square diagonal matrix with the elements on the main
        diagonal defined by the passed real numbers sequence argument.
        
        Signature:
            seq(int OR float) -> SquareMatrix
        
        Args:
            Elements: seq(int OR float); the main diagonal elements
        
        Returns:
            SquareMatrix: a new instance of the class
        
        Raises:
            UT_TypeError: the passed argument is not a sequence of integer or
                floating point numbers
            UT_ValueError: the sequence is shorter that 2 elements
        
        Version 1.0.0.0
        """
        _CheckIfRealSequence(Elements)
        Size = len(Elements)
        if Size < 2:
            raise UT_ValueError(Size, '> 1 - number of diagonal elements',
                                                                SkipFrames = 1)
        MatrixElements = [[Elements[ColIdx] if ColIdx == RowIdx else 0
                                                for ColIdx in range(Size)]
                                                    for RowIdx in range(Size)]
        return cls(MatrixElements)
    
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
            Error.appendMessage('- isColumnsFirst argument')
            raise Error
        if ((not isinstance(seqValues, c_abc.Sequence))
                                                or isinstance(seqValues, str)):
            raise UT_TypeError(seqValues, (list, tuple), SkipFrames = 1)
        try:
            _CheckIfRealSequence(seqValues)
            Length = len(seqValues)
            if (not isinstance(Size, int)) and (not (Size is None)):
                Error = UT_TypeError(Size, int, SkipFrames = 1)
                Error.appendMessage('- Size argument')
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
                        f'!= {FirstLength} - sub-sequence index {Index} length',
                                                                SkipFrames = 1)
            if FirstLength != NItems:
                raise UT_ValueError(FirstLength,
                    f'= {NItems} - mismatching width and height of the matrix',
                                                                SkipFrames = 1)
            if not isColumnsFirst:
                self._Elements = tuple(tuple(seqValues[Index])
                                                    for Index in range(NItems))
            else:
                self._Elements = tuple(tuple(seqValues[HIndex][WIndex]
                                        for HIndex in range(NItems))
                                            for WIndex in range(FirstLength))
    
    def __repr__(self) -> str:
        """
        Magic method to support repr() function with the matrix as its argument.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return f"'{self.__class__.__name__}(Size={self._Elements})'"

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
        Calculates the trace of a square matrix, i.e. the sum of all main
        diagonal elements.
        
        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        Size = len(self._Elements)
        return sum(self._Elements[Idx][Idx] for Idx in range(Size))
    
    def getLUPdecomposition(self) -> Tuple[TSquareMatrix, TSquareMatrix,
                                        Tuple[int, ...], Tuple[int, ...], int]:
        """
        Calculates the decomposion of a matrix into a product of four matrices:
        the rows permutation matrix (which is identity unless some rows are not
        linear independent), the lower-triangular (with all main diagonal
        elements being 1), the upper-triangular matrix and the rows and columns
        permutation matrices. Uses Gauss-Jordan elimination algorithm with full
        pivoting.
        
        Note that the rows pivoting occurs only if a row becomes all zeroes in
        the elimination process, which means, that the determinant is zero and
        the matrix is singular. Therefore, the rows permutations can be usually
        ignored. The columns permutations are used for the numerical stability
        even if no zeroes appear on the main diagonal during elimination.
        
        Naming the initial matrix A, lower-triangular L, upper-triangular U,
        columns permutation Pc and rows permutation matrix Pr, for any
        non-singular matrix A = L * U * Pc, with Pr == I - identity matrix. Even
        for a singular matrix A = Pr * L * U * Pc with U being the row echelon
        form with all zeroes rows at the bottom.
        
        Signature:
            None -> SquareMatrix, SquareMatrix, tuple(int), tuple(int), int
        
        Returns:
            SquareMatrix, SquareMatrix, tuple(int), tuple(int), int: unpacked
                tuple of two square matrices of the same size (lower- and upper
                triangular respectively), followed by the permutation tuple
                representing the swapping of the columns (the actual permutation
                matrix can be generated from it directly), followed by (tuple)
                permutation of rows, followed by +1 or -1 number as the
                permutation sign.
        
        Version 1.0.0.0
        """
        Size = len(self._Elements)
        Sign = 1
        #look-up table for the columns swapping
        ColsPerm = [Item for Item in range(Size)]
        #look-up table for the rows swapping
        RowsPerm = [Item for Item in range(Size)]
        #future upper-triangular matrix, indexed via pivoting look-up tables
        Upper = [list(tupRow) for tupRow in self._Elements]
        #future lower-triangular matrix, index using real indexes
        Lower = [[1 if ColIdx == RowIdx else 0 for ColIdx in range(Size)]
                                                    for RowIdx in range(Size)]
        #go along the main diagonal, moving one row lower at each step
        for BaseIndex in range(Size - 1):
            RealRowIndex = RowsPerm[BaseIndex] #in upper matrix coordinates
            RealColIdx = ColsPerm[BaseIndex]
            CurrentRow = Upper[RealRowIndex]
            if not any(CurrentRow ): #all elements in the current row are 0
                #rows pivoting is required, use the first found below
                for RowIdx in range(BaseIndex + 1, Size):
                    NextRow = Upper[RowsPerm[RowIdx]]
                    if any(NextRow):
                        #swap indexes in the look-up table, not real rows!
                        OldIndex = RowsPerm[RowIdx]
                        RowsPerm[RowIdx] = RealRowIndex
                        RowsPerm[BaseIndex] = OldIndex
                        #swapping elements in the Lower matrix as well
                        #+ real data, but only two 'partial' rows - from the
                        #+ column index 0 to the current position - 1 on the
                        #+ main diagonal
                        for ColIdx in range(BaseIndex):
                            OldValue = Lower[BaseIndex][ColIdx]
                            Lower[BaseIndex][ColIdx]= Lower[RowIdx][ColIdx]
                            Lower[RowIdx][ColIdx] = OldValue
                        Sign *= -1
                        RealRowIndex = RowsPerm[BaseIndex]
                        break
            #check if extra column swapping is required
            MaxIndex = BaseIndex
            Item = Upper[RealRowIndex][ColsPerm[MaxIndex]]
            #selecting maximum element (abs) in the row - columns pivoting
            for ColIdx in range(BaseIndex, Size):
                NewIndex = ColsPerm[ColIdx]
                NewItem = Upper[RealRowIndex][NewIndex]
                if abs(NewItem) > abs(Item):
                    Item = NewItem
                    MaxIndex = ColIdx
                    break
            #swapping columns (look-up table not actual data!)
            if MaxIndex != BaseIndex:
                OldIndex = ColsPerm[BaseIndex]
                ColsPerm[BaseIndex] = ColsPerm[MaxIndex]
                ColsPerm[MaxIndex] = OldIndex
                Sign *= -1
                RealColIdx = ColsPerm[BaseIndex]
            #Gauss elimination, inline data modification
            Base = Upper[RealRowIndex][RealColIdx]
            if Base != 0:
                for Index in range(BaseIndex + 1, Size):
                    MRowIndex = RowsPerm[Index]
                    Coefficient = Upper[MRowIndex][RealColIdx] / Base
                    Lower[Index][BaseIndex] = Coefficient
                    Upper[MRowIndex][RealColIdx] = 0
                    for ColIdx in range(BaseIndex + 1, Size):
                        RealIdx = ColsPerm[ColIdx]
                        Value = (Upper[MRowIndex][RealIdx] - Coefficient *
                                                Upper[RealRowIndex][RealIdx])
                        Upper[MRowIndex][RealIdx] = Value
        #covert lower matrix into the square matrix class instance directly
        LowerMatrix = self.__class__(Lower)
        #convert upper matrix into the suqare matrix class instance with the
        #+ rows and columns re-arrangement according the made pivoting
        UpperElements = [[Upper[RowIdx][ColIdx] for ColIdx in ColsPerm]
                                                        for RowIdx in RowsPerm]
        UpperMatrix = self.__class__(UpperElements)
        #columns and rows permutations are already in the right format and order
        ColsPerm = tuple(ColsPerm)
        RowsPerm = tuple(RowsPerm)
        return LowerMatrix, UpperMatrix, ColsPerm, RowsPerm, Sign
    
    def getFullDecomposition(self) -> Tuple[TSquareMatrix, TSquareMatrix,
                                    Tuple[TReal, ...], Tuple[int, ...], int]:
        """
        Calculates the decomposion of a matrix into a product of five matrices:
        the rows permutation matrix (which is identity unless some rows are not
        linear independent), the lower-triangular (with all main diagonal
        elements being 1), the upper-triangular matrix (with all main diagonal
        elements being 1), a diagonal matrix (all non-zero elements only on the
        main diagonal) and the permutation matrices. Uses Gauss-Jordan
        elimination algorithm with full pivoting to calculate the
        LUP-decomposition first, then decomposes the upper- traingular matrix
        into a diagonal and upper-triangular with onses at the main diagonal
        using Gauss elimination algorithm.
        
        Note that the rows pivoting occurs only if a row becomes all zeroes in
        the elimination process, which means, that the determinant is zero and
        the matrix is singular. Therefore, the rows permutations can be usually
        ignored. The columns permutations are used for the numerical stability
        even if no zeroes appear on the main diagonal during elimination.
        
        Naming the initial matrix A, lower-triangular L, upper-triangular U,
        diagonal matrix D, columns permutation Pc and rows permutation matrix
        Pr, for the non-singular matrix A = L * U * D * Pc, with Pr == I being
        the identity matrix.
        
        Note: for a singular matrix det(A) = 0, A != Pr * L * U * D * Pc, since
        the Gauss elimination method fails to eliminate all non-diagonal
        elements, thus D is not, actually diagonal, but it is treated as one.
        
        Signature:
            None -> SquareMatrix, SquareMatrix, tuple(int OR float),
                tuple(int), int
        
        Returns:
            SquareMatrix, SquareMatrix, tuple(int OR float), tuple(int),
                tuple(int), int: unpacked tuple of two square matrices of the
                same size (lower- and upper-triangular respectively), followed
                by the tuple or real numbers representing the main diagonal
                elements of the diagonal matrix (can be generated directly from
                it), followed by the permutation tuple representing the swapping
                of the columns (the actual permutation matrix can be generated
                from it directly), followed by the rows permutation tuple,
                followed by +1 or -1 number as the permutation sign.
        
        Version 1.0.0.0
        """
        LowerMtrx, UpperMtrx, ColsPrm, RowsPrm, Sign= self.getLUPdecomposition()
        Size = len(self._Elements)
        #the algorithm is wrong for the singular matrices, due to the taken
        #+ shortcuts!
        Diagonal = tuple([UpperMtrx._Elements[Idx][Idx] for Idx in range(Size)])
        Upper = [list(tupRow) for tupRow in UpperMtrx._Elements]
        del UpperMtrx
        for RowIdx in range(Size - 1, 0, -1):
            Base = Upper[RowIdx][RowIdx]
            if Base != 0:
                for Index in range(0, RowIdx):
                    Coefficient = Upper[Index][RowIdx] / Base
                    Upper[Index][RowIdx] = Coefficient
            else:
                for Index in range(0, RowIdx):
                    Upper[Index][RowIdx] = 0
            Upper[RowIdx][RowIdx] = 1
        Upper[0][0] = 1
        UpperMtrx = self.__class__(Upper)
        return LowerMtrx, UpperMtrx, Diagonal, ColsPrm, RowsPrm, Sign
    
    def getDeterminant(self) -> TReal:
        """
        Calculates the determinant of a square matrix using LUP-decomposition
        for large (Size > 3) matrices, and the direct analytical expression for
        2 x 2 and 3 x 3 matrices for speed.
        
        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        Size = len(self._Elements)
        if Size < 4:
            a = self._Elements
            if Size == 2:
                Result = a[0][0] * a[1][1] - a[0][1] * a[1][0]
            else:
                Result = a[0][0] * a[1][1] * a[2][2]
                Result += a[0][1] * a[1][2] * a[2][0]
                Result += a[1][0] * a[2][1] * a[0][2]
                Result -= a[2][0] * a[1][1] * a[0][2]
                Result -= a[0][1] * a[1][0] * a[2][2]
                Result -= a[0][0] * a[1][2] * a[2][1]
        else:
            _, Upper, _, _, Sign = self.getLUPdecomposition()
            Result = Sign
            for Index in range(Size):
                Result *= Upper._Elements[Index][Index]
        if not Result:
            Result = 0
        return Result
    
    def getInverse(self) -> Union[TSquareMatrix, None]:
        """
        Calculates the inverse matrix if one exists using full (LUDP)
        decomposition.
        
        Signature:
            None -> SquareMatrix OR None
        
        Returns:
            SquareMatrix: the inverse of the current square matrix, unless the
                current matrix is singular (determinant is zero)
            None: the current matrix is singular, so the inverse does not
                exist
        
        Version 1.0.0.0
        """
        Size = len(self._Elements)
        Lower, Upper, Diag, Perm, _, _ = self.getFullDecomposition()
        Low = [list(lstRow) for lstRow in Lower._Elements]
        Up = [list(lstRow) for lstRow in Upper._Elements]
        del Lower
        del Upper
        Det = 1
        for Idx in range(Size):
            Det *= Diag[Idx]
        if Det:
            #inverse modifications applied to an identity matrix
            Data = [[1 if ColIdx == RowIdx else 0 for ColIdx in range(Size)]
                                                    for RowIdx in range(Size)]
            for ColIdx in range(Size - 1):
                for RowIdx in range(ColIdx + 1, Size):
                    Coeff = Low[RowIdx][ColIdx]
                    for Idx in range(Size):
                        Data[RowIdx][Idx] -= Coeff * Data[ColIdx][Idx]
            for ColIdx in range(Size - 1, 0, -1):
                for RowIdx in range(0, ColIdx):
                    Coeff = Up[RowIdx][ColIdx]
                    for Idx in range(Size):
                        Data[RowIdx][Idx] -= Coeff * Data[ColIdx][Idx]
            for RowIdx in range(Size):
                for ColIdx in range(Size):
                    Value = Data[RowIdx][ColIdx] / Diag[RowIdx]
                    Data[RowIdx][ColIdx] = Value
            #re-arrange the columns according the columns permutations tuple
            #+ find the inverse permutation, equivalent to the matrix transpose
            PermIndexes = [Pos[0] for Pos in sorted([(Idx, Item)
                                            for Idx, Item in enumerate(Perm)],
                                                key = lambda Value: Value[1])]
            #+ re-arrange the columns
            Data = [Data[PermIndexes[Idx]] for Idx in range(Size)]
            Result = self.__class__(Data)
        else:
            Result = None
        return Result

    def getEigenValues(self) -> Union[TRealTuple, None]:
        """
        Calculates the real number valued eigenvalues. Based on the Francis
        QR-algorithm with Gram-Schmidt orthogonalization method.
        
        Signature:
            None -> tuple(int OR float) OR None
        
        Returns:
            tuple(int OR float): all unique real number valued eigenvalues
            None: no real number valued eigenvalues are found
        
        Version 1.0.0.0
        """
        #re-pack data into columns-first order
        Original = self._Elements
        Size = len(Original)
        Data = [[Original[RowIdx][ColIdx] for RowIdx in range(Size)]
                                                    for ColIdx in range(Size)]
        #use Francis QR-algorithm
        Result, Message = _FindEigenValuesQR(Data)
        if not (Result is None):
            Result = tuple(Result)
        elif DEBUG_MODE:
            print(Message)
        return Result
    
    def getEigenVectors(self, Eigenvalue: Optional[TReal] = None
                        ) -> Union[Dict[TReal, Tuple[TColumn, ...]], None]:
        """
        Calculates the real number valued eigenvalues and the respective eigen
        vectors, which form orthonormal basis for each eigenvalue. Based on the
        Francis QR-algorithm with Gram-Schmidt orthogonalization method.
        
        Signature:
            /int OR float/ -> dict(int OR float -> tuple(Column) OR None)
                OR None
        
        Args:
            Eigenvalue: (optional) int OR float; an a priori known eigenvalue
                of the matrix, for which the eigenvectors are to be found.
                Defaults to None, in which case the method attemts to calculate
                all eigenvalues first.
        
        Returns:
            dict(int OR float -> tuple(Column) OR None): dictionary mapping all
                unique real number valued eigenvalues to the respective
                orthonormal set of eigenvectors as a tuple of column vector
                class instances, if it is not possible to calculate, at least,
                one eigenvector for a given eigenvalue (due to rounding errors)
                the value of the corresponding key is set to None
            None: no real number valued eigenvalues are found, OR the passed
                value is not an eigenvalue of the matrix
        
        Raises:
            UT_TypeError: the passed optional value is not a real number
        
        Version 1.0.0.0
        """
        if Eigenvalue is None:
            Values = self.getEigenValues() #find all real eigenvalue by QR
        elif (not isinstance(Eigenvalue, (int, float))
                                            or isinstance(Eigenvalue, bool)):
            raise UT_TypeError(Eigenvalue, (int, float), SkipFrames = 1)
        else:
            Values = [Eigenvalue] #use passed value as a single found one
        Size = len(self._Elements)
        if not (Values is None):
            Result = {EigenValue : tuple() for EigenValue in Values}
            for EigenValue in Values:
                #construct singular matrix
                Data = [[Item - EigenValue if ColIdx == RowIdx else Item
                            for ColIdx, Item in enumerate(tupRow)]
                                for RowIdx, tupRow in enumerate(self._Elements)]
                Data = self.__class__(Data)
                #compute LUP-decomposition, U is in the row echelon form
                _, Upper, ColPerm, _, _ = Data.getLUPdecomposition()
                #lower-triangular matrix, rows permutation and sign can be
                #+ ignored
                del Data
                Data = [list(tupRow) for tupRow in Upper._Elements]
                del Upper
                #LUP complexitity is O(N^2), hence the estimation of the
                #+ rounding error
                Diag = [Data[Idx][Idx]
                        if abs(Data[Idx][Idx]) > Size * Size * ALMOST_ZERO
                                                else 0 for Idx in range(Size-1)]
                if abs(Data[Size - 1][Size - 1]) > Size*Size*Size*ALMOST_ZERO:
                    #all diagonal elements are not 0 (wrong value passed or
                    #+ too much of the rounding error
                    if len(Values) == 1:
                        Result = None
                    else:
                        Result[EigenValue] = None
                    continue
                elif not any(Diag): #all diagonal elements are zero
                    #it can happen only if there is only one eigenvalue
                    EigenVectors = tuple(Column.generateOrthogonal(Size, Idx)
                                                        for Idx in range(Size))
                    Result[EigenValue] = EigenVectors
                else:
                    EigenVectors = []
                    ZeroesCount = Diag.count(0) + 1
                    #there must be ZeroesCount orthonormal eigenvectors set
                    ReducedSize = Size - ZeroesCount
                    ReducedData = [[Data[RowIdx][ColIdx]
                                        for ColIdx in range(ReducedSize)]
                                            for RowIdx in range(ReducedSize)]
                    FreeCoeffs = [[Data[RowIdx][ColIdx]
                                    for RowIdx in range(ReducedSize)]
                                        for ColIdx in range(ReducedSize, Size)]
                    #back-substitution algorithm
                    for FreeIdx in range(ZeroesCount):
                        BoundCoefficients = []
                        FreeColumn = FreeCoeffs[FreeIdx]
                        for BoundIndex in range(ReducedSize - 1, -1, -1):
                            Component = - FreeColumn[BoundIndex]
                            Row = ReducedData[BoundIndex]
                            for TempIndex, Coefficient in enumerate(
                                                            BoundCoefficients):
                                NextElement = Row[BoundIndex + TempIndex + 1]
                                Component -= NextElement * Coefficient
                            Component /= Row[BoundIndex]
                            BoundCoefficients.insert(0, Component)
                        SolutionVector = list(BoundCoefficients)
                        SolutionVector.extend([0 for _ in range(ZeroesCount)])
                        SolutionVector[ReducedSize + FreeIdx] = 1
                        EigenVector = [0 for _ in range(Size)]
                        for PosIndex, Component in enumerate(SolutionVector):
                            EigenVector[ColPerm[PosIndex]] = Component
                        EigenVectors.append(EigenVector)
                    EigenVectors = _GetOrthonormal(EigenVectors)
                    Result[EigenValue] = tuple(Column(*Value)
                                                    for Value in EigenVectors)
        else: #no real eigenvalues are found by QR algorithm
            Result = None #+ or passed by user value is not an eigenvalue
        return Result

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

#Dynamic patching of the Matrix class, instance method __mul__()

def _Matrix__mul__(self: Matrix,
                Other: Union[Matrix, Column, TReal]) -> Union[Column, Matrix]:
    """
    Special helper function to patch the right multiplication of a Matrix hook
    magical method.
    
    Signature:
        'Matrix, 'Matrix OR Column OR int OR float -> Column OR 'Matrix
    
    Args:
        self: 'Matrix; instance of Matrix (sub-) class as the left operand
        Other: 'Matrix OR Column OR int OR float; an instance of the Matrix
            (sub-) class or an instance of Column vector class or a real number
            as the right operand
    
    Returns:
        Column: instance of the Column class, which is the result of the
            operation with the Column right operand
        'Matrix: result of the matrix x matrix or matrix x scalar multiplication
            with an instance of SquareMatrix class returned if the width of the
            resulting (generic) matrix equal its height
    
    Raises:
        UT_TypeError: the second operand is not an instance of the Column vector
            vector class nor a real number nor an instance of Matrix (sub-)
            class
        UT_ValueError: for two matrices left operand width is not equal to
                the right operand height, OR the length of the column is not
                equal to the width of the matrix
        
    Version 1.0.0.0
    """
    Result = None
    if isinstance(Other, (int, float)):
        Elements = [[Item * Other for Item in Row] for Row in self._Elements]
        Result = self.__class__(Elements)
    elif isinstance(Other, Column):
        Height = len(self._Elements)
        Width = len(self._Elements[0])
        Length = len(Other._Elements)
        if Length != Width:
            raise UT_ValueError(Length,
                            f'== {Width} - column vector size != matrix width',
                                                                SkipFrames = 1)
        Elements = [sum(Item * Other._Elements[Index]
                        for Index, Item in enumerate(self._Elements[RowIndex]))
                                                for RowIndex in range(Height)]
        Result = Column(*Elements)
    elif isinstance(Other, Matrix):
        SelfWidth = len(self._Elements[0])
        SelfHeight = len(self._Elements)
        Width = len(Other._Elements[0])
        Height = len(Other._Elements)
        if SelfWidth != Height:
            raise UT_ValueError(SelfWidth,
                            f'== {Height} - left matrix width != right height',
                                                                SkipFrames = 1)
        Elements = [[sum(
                self._Elements[RowIndex][Index]*Other._Elements[Index][ColIndex]
                                    for Index in range(SelfWidth))
                                        for ColIndex in range(Width)]
                                            for RowIndex in range(SelfHeight)]
        if SelfHeight == Width:
            Result = SquareMatrix(Elements)
        else:
            Result = Matrix(Elements)
    else:
        raise UT_TypeError(Other, (int, float, Column, Matrix), SkipFrames = 1)
    return Result

#tweaking and patching the classes

TempDoc = Column.__mul__.__doc__
setattr(Column, "__mul__", _Column__mul__)
Column.__mul__.__doc__ = TempDoc
TempDoc = Column.transpose.__doc__
setattr(Column, "transpose", _Column_transpose)
Column.transpose.__doc__ = TempDoc

TempDoc = Matrix.__mul__.__doc__
setattr(Matrix, "__mul__", _Matrix__mul__)
Matrix.__mul__.__doc__ = TempDoc
