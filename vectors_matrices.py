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
__date__ = '20-12-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
#import math

import collections.abc as c_abc

from typing import Sequence, Union, Tuple, Any, List, Optional, Dict

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
    """
    pass

def _ChechIfSequenceRealSequence(Value: Any) -> None:
    """
    """
    pass

#classes

class Array2D:
    """
    """
    
    #special methods
    
    def __init__(self, seqValues, *, Width : Optional[int] = None,
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
    
    def __getitem__(self, Indexes : Tuple[int, int]) -> TReal:
        """
        """
        pass
    
    def __list__(self) -> List[List[TReal]]:
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

class Vector:
    """
    """
    
    #special methods
    
    def __init__(self, *args) -> None:
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
    
    def __getitem__(self, Index: int) -> TReal:
        """
        """
        pass
    
    def __list__(self) -> List[TReal]:
        """
        """
        pass
    
    def __add__(self, Other: TVector) -> TVector:
        """
        """
        pass
    
    def __sub__(self, Other: TVector) -> TVector:
        """
        """
        pass
    
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
        """
        pass
    
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

    def __mul__(self, Other: TReal) -> TColumn:
        """
        """
        pass
    
    def __rmul__(self, Other: TReal) -> TColumn:
        """
        """
        pass

class Row(Vector):
    """
    """
    pass

    #special methods

    def __mul__(self, Other: Union[TReal, TColumn]) -> Union[TRow, TReal]:
        """
        """
        pass
    
    def __rmul__(self, Other: TReal) -> TRow:
        """
        """
        pass

class Matrix(Array2D):
    """
    """
    
    #special methods
    
    def __add__(self, Other: TMatrix) -> TMatrix:
        """
        """
        pass
    
    def __sub__(self, Other: TMatrix) -> TMatrix:
        """
        """
        pass
    
    def __mul__(self, Other: Union[TReal, TColumn, TMatrix]
                                                ) -> Union[TColumn, TMatrix]:
        """
        """
        pass
    
    def __rmul__(self, Other: Union[TReal, TRow]) -> Union[TRow, TMatrix]:
        """
        """
        pass
    
    def __truediv__(self, Other: TReal) -> TMatrix:
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
    
    #public methods
    
    def transpose(self) -> TMatrix:
        """
        """
        pass
    
    def getColumn(self, Index: int) -> TColumn:
        """
        """
        pass
    
    def getRow(self, Index: int) -> TRow:
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
    
    def __init__(self, seqValues, *, Size : int = None,
                                        isColumnsFirst : bool = True) -> None:
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

#Do dynamic binding to implment column x row -> matrix multiplication