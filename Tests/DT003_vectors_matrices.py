#usr/bin/python3
"""
Module math_extra_lib.Tests.DT003_vectors_matrices

Implements demonstration testing of the module math_extra_lib.vectors_matrices
- specifically the exceptions generation, which are auxilary to the functional
unit tests see TE00 and TE003 documents, and arithmetics.
"""

__version__ = "1.0.0.0"
__date__ = "18-01-2023"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.vectors_matrices as testmodule

#helper functions

def PrintError(Error: Exception) -> None:
    print(Error.__class__.__name__, ':', Error)
    if hasattr(Error, 'Traceback'):
        print(Error.Traceback.Info)

#test area

if __name__=='__main__':
    print('Generic vectors arithmetics...')
    Vector1 = testmodule.Vector(1, 2, 3)
    Vector2 = testmodule.Vector(4, 5, 6)
    Vector3 = testmodule.Vector(7, 8)
    print('Vector1=', Vector1, 'which is', repr(Vector1))
    print('Vector2=', Vector2, 'which is', repr(Vector2))
    print('Vector3=', Vector3, 'which is', repr(Vector3))
    Test = Vector1 + Vector2
    print('Vector1 + Vector2=', Test, 'which is', repr(Test))
    del Test
    Test = Vector1 - Vector2
    print('Vector1 - Vector2=', Test, 'which is', repr(Test))
    del Test
    Test = Vector1 * Vector2
    print('Inner product Vector1 * Vector2=', Test)
    del Test
    Test = Vector1 @ Vector3
    print('Outer product Vector1 @ Vector3=', Test, 'which is', repr(Test))
    del Test
    Test = Vector3 @ Vector1
    print('Outer product Vector3 @ Vector1=', Test, 'which is', repr(Test))
    del Test
    Test = Vector1 * 0.5
    print('Vector1 * 0.5=', Test, 'which is', repr(Test))
    del Test
    Test = 0.25 * Vector1
    print('0.25 * Vector1=', Test, 'which is', repr(Test))
    del Test
    Test = Vector1 / 0.5
    print('Vector1 / 0.5=', Test, 'which is', repr(Test))
    del Test
    input('Press Enter...')
    Column1 = testmodule.Column(1,2,3)
    Column2 = testmodule.Column(4,5,6)
    Column3 = testmodule.Column(7,8)
    print('Column1=', Column1, 'which is', repr(Column1))
    print('Column2=', Column2, 'which is', repr(Column2))
    print('Column3=', Column3, 'which is', repr(Column3))
    Test = Column1 + Column2
    print('Column1 + Column2=', Test, 'which is', repr(Test))
    del Test
    Test = Column1 - Column2
    print('Column1 - Column2=', Test, 'which is', repr(Test))
    del Test
    Test = Column1 * 1.5
    print('Column1 * 1.5=', Test, 'which is', repr(Test))
    del Test
    Test = 0.5 * Column1
    print('0.5 * Column1', Test, 'which is', repr(Test))
    del Test
    Test = Column1 / 2.1
    print('Column1 / 2.1=', Test, 'which is', repr(Test))
    del Test
    input('Press Enter...')
    Row1 = testmodule.Row(1,2,3)
    Row2 = testmodule.Row(4,5,6)
    Row3 = testmodule.Row(7,8)
    print('Row1=', Row1, 'which is', repr(Row1))
    print('Row2=', Row2, 'which is', repr(Row2))
    print('Row3=', Row3, 'which is', repr(Row3))
    Test = Row1 + Row2
    print('Row1 + Row2=', Test, 'which is', repr(Test))
    del Test
    Test = Row1 - Row2
    print('Row1 - Row2=', Test, 'which is', repr(Test))
    del Test
    Test = Row1 * 1.5
    print('Row1 * 1.5=', Test, 'which is', repr(Test))
    del Test
    Test = 0.5 * Row1
    print('0.5 * Row1', Test, 'which is', repr(Test))
    del Test
    Test = Row1 / 2.1
    print('Row1 / 2.1=', Test, 'which is', repr(Test))
    del Test
    input('Press Enter...')
    print('Row1 * Column1=', Row1 * Column1)
    print('Row3 * Column3=', Row3 * Column3)
    Test = Column3 * Row1
    print('Column3 * Row1=', Test, 'which is', repr(Test))
    del Test
    Test = Column1 * Row3
    print('Column1 * Row3=', Test, 'which is', repr(Test))
    del Test
    input('Press Enter...')
    Matrix1 = testmodule.Matrix(((1, 2, 3), (3, 4, 5)))
    Matrix2 = testmodule.Matrix(((6, 7, 8), (9, -1, -2)))
    Matrix3 = testmodule.Matrix(((-3, -4), (-5, -6), (-7, -8)))
    SMatrix1 = testmodule.SquareMatrix(((1, 2), (3, 4)))
    SMatrix2 = testmodule.SquareMatrix(((5, 6), (7, 8)))
    SMatrix3 = testmodule.SquareMatrix(((9, -1, -2), (-3, -4, -5), (-6, -7, -8)))
    print('Matrix1=', Matrix1, 'which is', repr(Matrix1))
    print('Matrix2=', Matrix2, 'which is', repr(Matrix2))
    print('Matrix3=', Matrix3, 'which is', repr(Matrix3))
    input('Press Enter...')
    print('SMatrix1=', SMatrix1, 'which is', repr(SMatrix1))
    print('SMatrix2=', SMatrix2, 'which is', repr(SMatrix2))
    print('SMatrix3=', SMatrix3, 'which is', repr(SMatrix3))
    input('Press Enter...')
    print('Demonstration of sanity checks and exceptions...')
    print('Generic vector instantiation')
    try:
        testmodule.Vector(1)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Vector(1, 'a', 0.1)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    print('Column vector instantiation')
    try:
        testmodule.Column(1)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Column(1, 'a', 0.1)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    print('Row vector instantiation')
    try:
        testmodule.Row(1)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Row(1, 'a', 0.1)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    print('Generic matrix instantiation')
    try:
        testmodule.Matrix(1)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix([1, 'a', 0.1])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix(((1, 'a'), (0.1, 1)))
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    try:
        testmodule.Matrix([1, 1, 1])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix([1, 1, 1], Width = 1)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix([1, 1, 1], Height = 1)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    try:
        testmodule.Matrix([1, 1, 1, 1], Width = 2, Height = 3)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix([1, 1, 1], Width = 2)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix([1, 1, 1], Height = 2)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    try:
        testmodule.Matrix([[1], [1, 1, 1]])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix([[1, 1], [1, 1, 1]])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.Matrix([[1, 1, 1, 1, 1]])
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.Matrix([1, 1, 1, 1], Height = 2, isColumnsFirst=1)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    print('Square matrix instantiation')
    try:
        testmodule.SquareMatrix(1)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SquareMatrix([1, 'a', 0.1])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SquareMatrix(((1, 'a'), (0.1, 1)))
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    try:
        testmodule.SquareMatrix([1, 1, 1])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SquareMatrix([1, 1, 1], Size = 1)
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SquareMatrix([1, 1, 1], Size = 3)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    try:
        testmodule.SquareMatrix([[1], [1, 1, 1]])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SquareMatrix([[1, 1], [1, 1, 1]])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SquareMatrix([[1, 1, 1, 1, 1]])
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        testmodule.SquareMatrix([[1, 1], [1, 1], [1, 1]])
    except Exception as err:
        PrintError(err)
    try:
        testmodule.SquareMatrix([1, 1, 1, 1], isColumnsFirst=1)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    print('Improper arguments of vector classes methods')
    try:
        Vector1.generateOrtogonal(1, 1)
    except Exception as err:
        PrintError(err)
    try:
        Column1.generateOrtogonal(3, 4)
    except Exception as err:
        PrintError(err)
    try:
        Row1.generateOrtogonal(3, -1)
    except Exception as err:
        PrintError(err)
    input('Press Enter...')
    print('Vectors indexing')
    try:
        Vector1[0: 1]
    except Exception as err:
        PrintError(err)
    try:
        Column1[3]
    except Exception as err:
        PrintError(err)
    try:
        Row1[-4]
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Vectors indexing')
    try:
        Matrix1[0: 1]
    except Exception as err:
        PrintError(err)
    try:
        Matrix1[3, -4]
    except Exception as err:
        PrintError(err)
    try:
        SMatrix1[-1, -1, 1]
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    print('Vector arithmetics')
    try:
        Vector1 - 1
    except Exception as err:
        PrintError(err)
    try:
        2 + Column1
    except Exception as err:
        PrintError(err)
    try:
        Vector1 * Row1
    except Exception as err:
        PrintError(err)
    input('Press Enter')
    try:
        Row1 - Vector1
    except Exception as err:
        PrintError(err)
    try:
        Column1 * Vector1
    except Exception as err:
        PrintError(err)
    try:
        Vector1 @ Row1
    except Exception as err:
        PrintError(err)
    print('Press Enter')
    try:
        1 @ Vector1
    except Exception as err:
        PrintError(err)
    try:
        Column1 @ Column1
    except Exception as err:
        PrintError(err)
    try:
        Row3 @ Row1
    except Exception as err:
        PrintError(err)
    print('Press Enter')
    del Vector1
    del Vector2
    del Vector3
    del Column1
    del Column2
    del Column3
    del Row1
    del Row2
    del Row3
    del Matrix1
    del Matrix2
    del Matrix3
    del SMatrix1
    del SMatrix2
    del SMatrix3