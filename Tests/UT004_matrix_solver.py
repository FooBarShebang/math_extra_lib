#usr/bin/python3
"""
Module math_extra_lib.Tests.UT004_matrix_solver

Implements unit testing of the module math_extra_lib.matrix_solver, see TE004.
"""

__version__ = "1.0.0.0"
__date__ = "12-10-2023"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import random
from math import sqrt

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.matrix_solver as testmodule

from math_extra_lib.vectors_matrices import Column, SquareMatrix, Matrix, Row

#classes

#+ test cases

class Test_FindEigenvalue(unittest.TestCase):
    """
    Unit tests for the function FindEigenvalue.
    
    Test IDs: TEST-T-410, TEST-T-411, TEST-T-412
    
    Covers requirements: REQ-FUN-410, REQ-AWM-410
    
    Version 1.0.0.0
    """
    
    def test_TypeError(self):
        """
        Checks that only SquareMatrix instance can be used as the argument.
        
        Test ID: TEST-T-412
        
        Covers requirements: REQ-AWM-410
        """
        WrongArgs = [1, 2.0, int, float, True, None, [1, 2], [(1, 2), (1, 2)],
                    (1, 2, 3, 4), Column(1, 2, 3), Matrix([(1, 2), (1, 2)]),
                    "1", str]
        for Arg in WrongArgs:
            with self.assertRaises(TypeError):
                Test = testmodule.FindEigenvector(Arg)
    
    def test_Eigenvalue_OK(self):
        """
        Checks that a proper eigenvalue is returned, if exists.
        
        Test ID: TEST-T-410
        
        Covers requirements: REQ-FUN-410
        """
        Matrices = [[[1, 1], [0, 1]], #2D shear
            [[1, 0, 1], [0, 1, 1], [0, 0, 2]], #x-y shear + z-scaling
            [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 3, 0], [0, 0, 0, 4]],
            [[5, 0, 0 ,0, 0], [1, 1, 0, 0, 0], [1, 0, 1, 0, 0],
            [1, 1, 0, 1, 0], [0, 0, 0, 0, 1]]]
        Values = [ [1], [1, 2], [1, 2, 3, 4], [1, 5]]
        for Arg, Eigenvalues in zip(Matrices, Values):
            TestMatrix = SquareMatrix(Arg)
            TestResult = testmodule.FindEigenvector(TestMatrix)
            self.assertIsInstance(TestResult, (int, float), msg=f"{Arg}")
            self.assertIn(TestResult, Eigenvalues)
            del TestMatrix
    
    def test_Eigenvalue_NOK(self):
        """
        Checks that None is returned if no real eigenvalue exists.
        
        Test ID: TEST-T-411
        
        Covers requirements: REQ-FUN-410
        """
        WrongMatrices = [[[0.8, -0.6], [0.6, 0.8]], #2D rotation
                        [[0, 0, 0], [0, 0, 0], [0, 0, 0]], #all zeroes
                        [[0, 0, 0, 2], [0, 0, 1, 0], [0, 1, 0, 0],
                        [1, 0, 0, 0]], #non-main diagonal only
                        [[0.8, -0.6, 0, 0, 0, 0], [0.6, 0.8, 0, 0, 0, 0],
                        [0, 0, 0.8, -0.6, 0, 0], [0, 0, 0.6, 0.8, 0, 0],
                        [0, 0, 0, 0, 0.8, -0.6], [0, 0, 0, 0, 0.6, 0.8]]
                        #2D rotation repeated x3 - block-matrix
                        ]
        for Arg in WrongMatrices:
            TestMatrix = SquareMatrix(Arg)
            TestResult = testmodule.FindEigenvector(TestMatrix)
            self.assertIsNone(TestResult, msg=f"{Arg}")
            del TestMatrix

class Test_SolveLinearSystem(unittest.TestCase):
    """
    Unit tests for the function SolveLinearSystem.
    
    Test IDs: TEST-T-420, TEST-T-421, TEST-T-422, TEST-T-423
    
    Covers requirements: REQ-FUN-420, REQ-AWM-420, REQ-AWM-421
    
    Version 1.0.0.0
    """
    
    def test_TypeError(self):
        """
        Checks that only proper type arguments can be passed.
        
        Test ID: TEST-T-422
        
        Covers requirements: REQ-AWM-420
        """
        WrongArgs = [1, 2.0, int, float, True, None, [1, "2"],
                    [(1, "2"), (1, 2)], [(1, 2), 1],
                    (1, "2", 3, 4), Column(1, 2, 3), Matrix([(1, 2), (1, 2)]),
                    "1", str]
        for Arg in WrongArgs:
            with self.assertRaises(TypeError):
                Test = testmodule.SolveLinearSystem(Arg, [1, 2])
        WrongArgs = [1, 2.0, int, float, True, None, [1, "2"],
                    [(1, 2), (1, 2)], (1, "2", 3, 4), Row(1, 2, 3),
                    Matrix([(1, 2), (1, 2)]), SquareMatrix([(1, 2), (1, 2)]),
                    "1", str]
        for Arg in WrongArgs:
            with self.assertRaises(TypeError):
                Test = testmodule.SolveLinearSystem(
                                            SquareMatrix([[1, 2], (1, 2)]), Arg)
    
    def test_ValueError(self):
        """
        Checks that the sizes of matrix and column vector must match.
        
        Test ID: TEST-T-423
        
        Covers requirements: REQ-AWM-421
        """
        WrongArgs = [
            [1, 2, 3], #too little elements for a SquareMatrix
            [[1, 2]], [[1,2], [3,3], [3,4]], #height != width
            [[1, 2], [3]], [[1, 2], [3, 4, 5]], #different rows length
        ]
        for Arg in WrongArgs:
            with self.assertRaises(ValueError):
                Test = testmodule.SolveLinearSystem(Arg, [1, 2])
        WrongArgs = [[], [1], [1, 2, 3]]
        for Arg in WrongArgs:
            with self.assertRaises(ValueError):
                Test = testmodule.SolveLinearSystem([[1, 0], [0, 1]], Arg)
    
    def test_System_NOK(self):
        """
        Checks that None is returned if the system does not have a single
        solution.
        
        Test ID: TEST-T-421
        
        Covers requirements: REQ-FUN-420
        """
        WrongMatrices = [[[0.8, -0.6], [0.8, -0.6]], #same row
                        [[1, 2, 3], [4, 5, 6], [3, 3, 3]], #linear dependence
                        [[1, 2, 3, 0], [2, 3, 1, 0], [3, 5, 5, 0],
                        [9, 8, 7, 0]], #zero column
                        [[1, 2, 3, 0, 1], [2, 3, 1, 0, 1], [3, 5, 5, 2, 1],
                        [-1, 2, -3, 1, -1], [0, 0, 0, 0, 0]] #zero row
                        ]
        for Arg in WrongMatrices:
            FreeCoeffs = [1 for _ in Arg]
            TestResult = testmodule.SolveLinearSystem(Arg, FreeCoeffs)
            self.assertIsNone(TestResult)
    
    def test_System_OK(self):
        """
        Checks that the system is solved correctly
        
        Test ID: TEST-T-420
        
        Covers requirements: REQ-FUN-420
        """
        def _GenerateRandom():
            Result=random.randint(-3, 3) + random.randint(0, 1)*random.random()
            return Result 
        print('Testing sizes 2 to 5 inclusively')
        for Size in range(2, 6):
            print(f'Size {Size}:', end = '')
            while True:
                print('.', end = '')
                Bound = [[_GenerateRandom() for _ in range(Size)]
                                                        for _ in range(Size)]
                _Matrix = SquareMatrix(Bound)
                Determinant = _Matrix.getDeterminant()
                if Determinant:
                    break
            print()
            Free = [_GenerateRandom() for _ in range(Size)]
            Result = testmodule.SolveLinearSystem(_Matrix, Free)
            self.assertIsInstance(Result, list)
            self.assertEqual(len(Result), Size)
            Solution = Column(*Result)
            Check = (_Matrix * Solution).Data
            for FreeCoeff, CheckValue in zip(Free, Check):
                self.assertAlmostEqual(FreeCoeff, CheckValue)
            del _Matrix
            _Matrix = list(Bound)
            Result = testmodule.SolveLinearSystem(_Matrix, Free)
            self.assertIsInstance(Result, list)
            self.assertEqual(len(Result), Size)
            for SolutionElement, CheckValue in zip(Solution.Data, Result):
                self.assertAlmostEqual(SolutionElement, CheckValue)
            _Matrix = []
            for Row in Bound:
                _Matrix.extend(Row)
            Result = testmodule.SolveLinearSystem(_Matrix, Column(*Free))
            self.assertIsInstance(Result, list)
            self.assertEqual(len(Result), Size)
            for SolutionElement, CheckValue in zip(Solution.Data, Result):
                self.assertAlmostEqual(SolutionElement, CheckValue)
            del Solution

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_FindEigenvalue)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_SolveLinearSystem)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting math_extra_lib.matrix_solver module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)