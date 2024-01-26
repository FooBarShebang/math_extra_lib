#usr/bin/python3
"""
Module math_extra_lib.Tests.UT004_poly_solver

Implements unit testing of the module math_extra_lib.poly_solver, see TE005.
"""

__version__ = "1.0.0.0"
__date__ = "26-01-2024"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import random

from math import sqrt, sin

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.poly_solver as testmodule

from math_extra_lib.polynomial import Polynomial

#classes

#+ test cases

class Test_HelperFunctions(unittest.TestCase):
    """
    Unit tests for the helper functions. Not part of the test plan TE005.
    
    Version 1.0.0.0
    """
    
    def test_GenerateBinomialCoefficients(self):
        """
        Checks the proper generation of the binomial coefficients, i.e. the
        helper function _GenerateBinomialCoefficients().
        """
        Expected = {
            0: [1],
            1: [1, 1],
            2: [1, 2, 1],
            3: [1, 3, 3, 1],
            4: [1, 4, 6, 4, 1],
            5: [1, 5, 10, 10, 5, 1],
            6: [1, 6, 15, 20, 15, 6, 1],
            7: [1, 7, 21, 35, 35, 21, 7, 1],
            8: [1, 8, 28, 56, 70, 56, 28, 8, 1]
        }
        for Key, Value in Expected.items():
            Test = testmodule._GenerateBinomialCoefficients(Key)
            self.assertListEqual(Test, Value)
    
    def test_GetDerivative(self):
        """
        Checks the proper calculation of the coefficients of a derivative
        polynomial.
        """
        Base = [
            [1, 1], # x + 1
            [-1, -2, 1], # x^2 - 2x - 1
            [0, 0, 2, 4], # 4x^3 + 2x^2
            [1, 1, 0, complex(3, 1), 2], # 2x^4 + (3+i)*x^3 + x + 1
            [1, 1, 0, complex(3, 1), 2, complex(1, -0.5)]
            # (1 -0.5i)*x^5 + 2x^4 + (3+i)*x^3 + x + 1
        ]
        Derivative = [
            [1],
            [-2, 2],
            [0, 4, 12],
            [1, 0, complex(9, 3), 8],
            [1, 0, complex(9, 3), 8, complex(5, -2.5)]
        ]
        for Test, Check in zip(Base, Derivative):
            Result = testmodule._GetDerivative(Test)
            self.assertIsInstance(Result, list)
            self.assertEqual(len(Result), len(Check))
            for TestValue, CheckValue in zip(Result, Check):
                self.assertEqual(TestValue, CheckValue)
    
    def test_EvaluatePolynomial(self):
        """
        Checks the implementation of the polynomial implementation.
        """
        #benchmark - real coefficients and real argument
        for _ in range(10):
            Power = random.randint(1, 5)
            Coefficients = [random.randint(-3, 3) for _ in range(Power)]
            Coefficients.append(1)
            CheckPolynomial = Polynomial(*Coefficients)
            for _ in range(10):
                Value = random.randint(-3, 3)
                Check = CheckPolynomial(Value)
                Test = testmodule._EvaluatePolynomial(Coefficients, Value)
                self.assertIsInstance(Test, int)
                self.assertEqual(Test, Check)
                Value += random.random()
                Check = CheckPolynomial(Value)
                Test = testmodule._EvaluatePolynomial(Coefficients, Value)
                self.assertIsInstance(Test, (int, float))
                self.assertAlmostEqual(Test, Check)
            del CheckPolynomial
        #pre-computed on complex numbers
        Polynomials = [
            [1, 1], # x + 1
            [-1, -2, 1], # x^2 - 2x - 1
            [0, 0, 2, 4], # 4x^3 + 2x^2
            [1, 1, 0, complex(3, 1), 2], # 2x^4 + (3+i)*x^3 + x + 1
            [1, 1, 0, complex(3, 1), 2, complex(1, -0.5)]
            # (1 -0.5i)*x^5 + 2x^4 + (3+i)*x^3 + x + 1
        ]
        Cases = {
            0: [1, -1, 0, 1, 1],
            1: [2, -2, 6, complex(7, 1), complex(8, 0.5)],
            -1: [0, 2, -2, complex(-1, -1), complex(-2, -0.5)],
            complex(0,1): [complex(1, 1), complex(-2, -2), complex(-2, -4),
                           complex(4, -2), complex(4.5, -1)]
        }
        for Value, CheckValues in Cases.items():
            for Poly, Check in zip(Polynomials, CheckValues):
                Test = testmodule._EvaluatePolynomial(Poly, Value)
                self.assertIsInstance(Test, (int, float, complex))
                self.assertEqual(Test, Check)
        #edge cases
        #+ rounding and complex -> real conversion
        Test = testmodule._EvaluatePolynomial([1, 1], 1 + 1.0E-14)
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 2)
        Test = testmodule._EvaluatePolynomial([1, 1],
                                              complex(1 + 1.0E-14, 1.0E-14))
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 2)
        Test = testmodule._EvaluatePolynomial([1, 0, 1],
                                              complex(0, 1 + 1.0E-14))
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 0)
        Test = testmodule._EvaluatePolynomial([1, 1, 1],
                                              complex(1.0E-14, 1 + 1.0E-14))
        self.assertIsInstance(Test, complex)
        self.assertEqual(Test, complex(0,1))
    
    def test_ReduceByRoot(self):
        """
        Checks the implementation of the polynomial root reduction.
        """
        Poly = [-1, 0, 1] #x^2 - 1 = (x-1)*(x+1)
        Test = testmodule._ReduceByRoot(Poly, 1)
        self.assertListEqual(Test, [1, 1])
        Test = testmodule._ReduceByRoot(Poly, -1)
        self.assertListEqual(Test, [-1, 1])
        Poly = [1, 0, 1] #x^2 + 1 = (x-i)*(x+i)
        Test = testmodule._ReduceByRoot(Poly, complex(1.0E-14, 1))
        self.assertListEqual(Test, [complex(0, 1), 1])
        Test = testmodule._ReduceByRoot(Poly, complex(1.0E-14, -1 + 1.0E-14))
        self.assertListEqual(Test, [complex(0, -1) , 1])
        Poly = [1, -2, 1] #x^2 - 2x + 1 = (x-1)^2
        Test = testmodule._ReduceByRoot(Poly, 1)
        self.assertListEqual(Test, [-1, 1])
        Poly = [1, 2, 1] #x^2 + 2x + 1 = (x+1)^2
        Test = testmodule._ReduceByRoot(Poly, -1)
        self.assertListEqual(Test, [1, 1])
        Poly = [-1, 3, -3, 1] #x^3 -3x^2 + 3x - 1 = (x-1)^3
        Test = testmodule._ReduceByRoot(Poly, 1)
        self.assertListEqual(Test, [1, -2, 1])
        Poly = [1, 3, 3, 1] #x^3 + 3x^2 + 3x + 1 = (x+1)^3
        Test = testmodule._ReduceByRoot(Poly, -1)
        self.assertListEqual(Test, [1, 2, 1])
        Poly = [-1, -1, 1, 1] #x^3 + x^2 - x - 1 = (x+1)^2 * (x-1)
        Test = testmodule._ReduceByRoot(Poly, -1)
        self.assertListEqual(Test, [-1, 0, 1])
        Test = testmodule._ReduceByRoot(Poly, 1)
        self.assertListEqual(Test, [1, 2, 1])
        Poly = [6, 11, 6, 1] #x^3 + 6x^2 + 11x + 6 = (x + 1) * (x + 2) * (x + 3)
        Test = testmodule._ReduceByRoot(Poly, -1)
        self.assertListEqual(Test, [6, 5, 1])
        Test = testmodule._ReduceByRoot(Poly, -2)
        self.assertListEqual(Test, [3, 4, 1])
        Test = testmodule._ReduceByRoot(Poly, -3)
        self.assertListEqual(Test, [2, 3, 1])
    
    def test_FindAllRoots(self):
        """
        Checks implementation of roots finding algorithm.
        
        May occasionally fail due to floating point error accumulation, when
        a polynomial of high degree (>= 5) has a pair of complex conjugated
        roots.
        """
        #1st degree
        for _ in range(10):
            FreeCoefficient = random.randint(-5, 5) + random.random()
            Test = testmodule._FindAllRoots([FreeCoefficient, 1])
            self.assertIsInstance(Test, list)
            self.assertListEqual(Test, [-FreeCoefficient])
        #2nd degree
        #+ x^2 + 2x + 1
        Test = testmodule._FindAllRoots([1, 2, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [-1, -1])
        #+ x^2 - 2x + 1
        Test = testmodule._FindAllRoots([1, -2, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1, 1])
        #+ x^2 - 1
        Test = testmodule._FindAllRoots([-1, 0, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1, -1])
        #+ x^2 + 1
        Test = testmodule._FindAllRoots([1, 0, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [complex(0, 1), complex(0, -1)])
        #+ x^2
        Test = testmodule._FindAllRoots([0, 0, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [0, 0])
        for _ in range(20):
            Poly = [random.randint(-5, 5) + random.random(),
                                    random.randint(-5, 5) + random.random(), 1]
            Test = testmodule._FindAllRoots(Poly)
            self.assertIsInstance(Test, list)
            self.assertEqual(len(Test), 2)
            for Root in Test:
                Check = testmodule._EvaluatePolynomial(Poly, Root)
                self.assertEqual(Check, 0)
        #3rd degree
        #x^3 - 3x^2 + 3x - 1
        Test = testmodule._FindAllRoots([-1, 3, -3, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1, 1, 1])
        #x^3 + 3x^2 + 3x + 1
        Test = testmodule._FindAllRoots([1, 3, 3, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [-1, -1, -1])
        #x^3
        Test = testmodule._FindAllRoots([0, 0, 0, 1])
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [0, 0, 0])
        #x^3 + 6x^2 + 11x + 6 = (x + 1) * (x + 2) * (x + 3)
        Poly = [6, 11, 6, 1]
        Test = testmodule._FindAllRoots(Poly)
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        for Root in [-1, -2, -3]:
            self.assertIn(Root, Test)
        #x^3 + x^2 - x - 1 = (x+1)^2 * (x-1)
        Poly = [-1, -1, 1, 1]
        Test = testmodule._FindAllRoots(Poly)
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        self.assertCountEqual(Test, [-1, -1, 1])
        #x^3 - 1
        Test = testmodule._FindAllRoots([-1, 0, 0, 1])
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        self.assertEqual(len(set(Test)), 3) #all roots are unique
        for Root in Test:
            if isinstance(Root, complex):
                self.assertAlmostEqual(Root.real, -0.5)
                self.assertAlmostEqual(abs(Root.imag), 0.5*sqrt(3))
            else:
                self.assertEqual(Root, 1)
        #x^3 + 1
        Test = testmodule._FindAllRoots([1, 0, 0, 1])
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        self.assertEqual(len(set(Test)), 3) #all roots are unique
        for Root in Test:
            if isinstance(Root, complex):
                self.assertAlmostEqual(Root.real, 0.5)
                self.assertAlmostEqual(abs(Root.imag), 0.5*sqrt(3))
            else:
                self.assertEqual(Root, -1)
        for _ in range(100):
            Degree = random.randint(3, 7)
            Poly= [random.randint(-3, 3)+random.random() for _ in range(Degree)]
            Poly.append(1)
            Test = testmodule._FindAllRoots(Poly)
            self.assertIsInstance(Test, list)
            self.assertEqual(len(Test), Degree)
            for Root in Test:
                #may occasionally fail due to floating point error accumulation
                self.assertAlmostEqual(
                                abs(testmodule._EvaluatePolynomial(Poly, Root)),
                                0, msg=f'{Poly}, {Test}, {Root}', delta = 0.001)

class Test_FindRoots(unittest.TestCase):
    """
    Unit tests for the function FindRoots().
    
    Test IDs: TEST-T-510 and TEST-T-511
    
    Covers requirements: REQ-FUN-510 and REQ-AWM-510
    
    Version 1.0.0.0
    """
    
    def test_TypeError(self):
        """
        Test ID: TEST-T-511
        
        Requirements: REQ-AWM-510
        """
        for Item in [1, 1.0, int, float, True, bool, list, tuple, [1, 1.0],
                                (1, 2), dict, {1: 1}, {1, 2, 3}, Polynomial]:
            with self.assertRaises(TypeError):
                Roots = testmodule.FindRoots(Item)
    
    def test_Calculation(self):
        """
        Test ID: TEST-T-511
        
        Requirements: REQ-AWM-510
        """
        #1st degree
        for _ in range(10):
            FreeCoefficient = random.randint(-5, 5) + random.random()
            Test = testmodule.FindRoots(Polynomial(FreeCoefficient, 1))
            self.assertIsInstance(Test, list)
            self.assertListEqual(Test, [-FreeCoefficient])
        #2nd degree
        #+ x^2 + 2x + 1
        Test = testmodule.FindRoots(Polynomial(1, 2, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [-1, -1])
        #+ x^2 - 2x + 1
        Test = testmodule.FindRoots(Polynomial(1, -2, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1, 1])
        #+ x^2 - 1
        Test = testmodule.FindRoots(Polynomial(-1, 0, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1, -1])
        #+ x^2 + 1
        Test = testmodule.FindRoots(Polynomial(1, 0, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [complex(0, 1), complex(0, -1)])
        #+ x^2
        Test = testmodule.FindRoots(Polynomial(0, 0, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [0, 0])
        #3rd degree
        #x^3 - 3x^2 + 3x - 1
        Test = testmodule.FindRoots(Polynomial(-1, 3, -3, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1, 1, 1])
        #x^3 + 3x^2 + 3x + 1
        Test = testmodule.FindRoots(Polynomial(1, 3, 3, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [-1, -1, -1])
        #x^3
        Test = testmodule.FindRoots(Polynomial(0, 0, 0, 1))
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [0, 0, 0])
        #x^3 + 6x^2 + 11x + 6 = (x + 1) * (x + 2) * (x + 3)
        Test = testmodule.FindRoots(Polynomial(6, 11, 6, 1))
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        for Root in [-1, -2, -3]:
            self.assertIn(Root, Test)
        #x^3 + x^2 - x - 1 = (x+1)^2 * (x-1)
        Test = testmodule.FindRoots(Polynomial(-1, -1, 1, 1))
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        self.assertCountEqual(Test, [-1, -1, 1])
        #x^3 - 1
        Test = testmodule.FindRoots(Polynomial(-1, 0, 0, 1))
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        self.assertEqual(len(set(Test)), 3) #all roots are unique
        for Root in Test:
            if isinstance(Root, complex):
                self.assertAlmostEqual(Root.real, -0.5)
                self.assertAlmostEqual(abs(Root.imag), 0.5*sqrt(3))
            else:
                self.assertEqual(Root, 1)
        #x^3 + 1
        Test = testmodule.FindRoots(Polynomial(1, 0, 0, 1))
        self.assertIsInstance(Test, list)
        self.assertEqual(len(Test), 3)
        self.assertEqual(len(set(Test)), 3) #all roots are unique
        for Root in Test:
            if isinstance(Root, complex):
                self.assertAlmostEqual(Root.real, 0.5)
                self.assertAlmostEqual(abs(Root.imag), 0.5*sqrt(3))
            else:
                self.assertEqual(Root, -1)
        for _ in range(100):
            Degree = random.randint(2, 7)
            Poly= [random.randint(-3, 3)+random.random() for _ in range(Degree)]
            Poly.append(1)
            Check = testmodule._FindAllRoots(Poly)
            Coefficent = random.randint(-3, 3)+random.random()
            if not Coefficent:
                Coefficent = 1
            Poly = [Item * Coefficent for Item in Poly]
            Test = testmodule.FindRoots(Polynomial(*Poly))
            self.assertEqual(len(Check), len(Test))
            for CheckValue in Check:
                self.assertTrue(any(map(
                            lambda x: abs(x - CheckValue) < 0.000001, Test)))
            for CheckValue in Test:
                self.assertTrue(any(map(
                            lambda x: abs(x - CheckValue) < 0.000001, Check)))

class Test_GetLagrangePolynomial(unittest.TestCase):
    """
    Unit tests for the function GetLagrangePolynomial().
    
    Not part of the test plan, but the internal quality check.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetLagrangePolynomial)
    
    def test_TypeError(self):
        """
        Checks the response to the bad input data types.
        """
        BadMesh = [
            '1, 2, 3', 1, 2.0, int , float, list, tuple, set, dict, bool, True,
            [1, '2', 3], {1 : 1, 2 : 2}, [[1, ], [2, ], [3, ]],
            [1, complex(1, 0)], b'121', bytearray([1, 2, 3])]
        NotRealNumber = [
            '1, 2, 3', [1, 2], int , float, list, tuple, set, dict, bool, True,
            [1, '2', 3], {1 : 1, 2 : 2}, [[1, ], [2, ], [3, ]],
            [1, complex(1, 0)], complex(1, 0)]
        for Item in BadMesh:
            with self.assertRaises(TypeError):
                Test = self.TestFunc(1, Item)
        for Item in NotRealNumber:
            with self.assertRaises(TypeError):
                Test = self.TestFunc(Item, [1, 2, 3])
    
    def test_ValueError(self):
        """
        Checks the response to the improper values of the arguments.
        """
        with self.assertRaises(ValueError):
            Test = self.TestFunc(1, []) #at least, 1 root is required!
        with self.assertRaises(ValueError):
            Test = self.TestFunc(1, [2.0, 3, 2.0]) #all roots must be unique
        with self.assertRaises(ValueError):
            Test = self.TestFunc(3, [1.0, 3, 2.0]) #node <> root!
    
    def test_Performance(self):
        """
        Test ID: TEST-T-520
        
        Requirement ID: REQ-FUN-520
        """
        Roots = []
        Node = 1.5
        for NewRoot in [1, 2, 3.0, 0.5, -1.0]:
            Roots.append(NewRoot)
            Test = self.TestFunc(Node, Roots)
            self.assertIsInstance(Test, Polynomial)
            self.assertEqual(Test.Degree, len(Roots))
            for Value in Roots:
                self.assertAlmostEqual(Test(Value), 0)
            self.assertAlmostEqual(Test(Node), 1)

class Test_GetLagrangeBasis(unittest.TestCase):
    """
    Unit tests for the function GetLagrangeBasis().
    
    Test IDs: TEST-T-520, TEST-T-521 and TEST-T-522
    
    Covers requirements: REQ-FUN-520, REQ-AWM-520 and REQ-AWM-521
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetLagrangeBasis)
    
    def test_TypeError(self):
        """
        Test ID: TEST-T-521
        
        Requirement ID: REQ-AWM-520
        """
        BadMesh = [
            '1, 2, 3', 1, 2.0, int , float, list, tuple, set, dict, bool, True,
            [1, '2', 3], {1 : 1, 2 : 2}, [[1, ], [2, ], [3, ]],
            [1, complex(1, 0)], b'121', bytearray([1, 2, 3])]
        for Item in BadMesh:
            with self.assertRaises(TypeError):
                Test = self.TestFunc(Item)
    
    def test_ValueError(self):
        """
        Test ID: TEST-T-522
        
        Requirement ID: REQ-AWM-521
        """
        with self.assertRaises(ValueError):
            Test = self.TestFunc([]) #at least, 2 roots are required!
        with self.assertRaises(ValueError):
            Test = self.TestFunc([1]) #at least, 2 roots are required!
        with self.assertRaises(ValueError):
            Test = self.TestFunc([2.0, 3, 2.0]) #all roots must be unique
    
    def test_Performance(self):
        """
        Test ID: TEST-T-520
        
        Requirement ID: REQ-FUN-520
        """
        Roots = [1.0]
        for Degree in range(2, 7):
            Roots.append(Roots[-1] + 0.1 + random.random())
            Test = self.TestFunc(Roots)
            self.assertIsInstance(Test, list)
            self.assertEqual(len(Test), Degree)
            for Index, Node in enumerate(Roots):
                Check = Test[Index]
                self.assertIsInstance(Check, Polynomial)
                self.assertEqual(Check.Degree, Degree - 1)
                if not Index:
                    Zeroes = Roots[1 : ]
                elif Index == Degree - 1:
                    Zeroes = Roots[ : -1]
                else:
                    Zeroes = Roots[ : Index]
                    Zeroes.extend(Roots[Index + 1 : ])
                self.assertAlmostEqual(Check(Node), 1)
                for Root in Zeroes:
                    self.assertAlmostEqual(Check(Root), 0)

class Test_InterpolateLagrange(unittest.TestCase):
    """
    Unit tests for the function InterpolateLagrange().
    
    Test IDs: TEST-T-530, TEST-T-504 and TEST-T-505
    
    Covers requirements: REQ-FUN-530, REQ-AWM-504 and REQ-AWM-505
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.InterpolateLagrange)
        cls.XGrid = [Index + 0.25 * random.random() for Index in range(6)]
    
    def test_TypeError(self):
        """
        Test ID: TEST-T-504
        
        Requirement ID: REQ-AWM-504
        """
        BadMesh = [
            '1, 2, 3', 1, 2.0, int , float, list, tuple, set, dict, bool, True,
            [1, '2', 3], {1 : 1, 2 : 2}, [[1, ], [2, 1], [3, 1]],
            [1, complex(1, 0)], [[1, 2, 0], [2, 1], [3, 1]],]
        for Item in BadMesh:
            with self.assertRaises(TypeError):
                Test = self.TestFunc(Item)
    
    def test_ValueError(self):
        """
        Test ID: TEST-T-505
        
        Requirement ID: REQ-AWM-505
        """
        with self.assertRaises(ValueError):
            Test = self.TestFunc([])
        with self.assertRaises(ValueError):
            Test = self.TestFunc([[1, 2]])
        with self.assertRaises(ValueError):
            Test = self.TestFunc([[2.0, 1], [3, 2], [2.0, 3]])
    
    def test_Constant(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        Coefficient = random.randint(1, 3) + random.random()
        YGrid = [Coefficient for _ in self.XGrid]
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        if isinstance(Test, (int, float)):
            self.assertAlmostEqual(Test, Coefficient)
        else:
            self.assertIsInstance(Test, Polynomial)
            self.assertLessEqual(Test.Degree, 5)
            for XValue in self.XGrid:
                Check = Test(XValue)
                self.assertAlmostEqual(Check, Coefficient)
            del Test
    
    def test_Linear(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        Coefficients= [random.randint(1, 3) + random.random() for _ in range(2)]
        Generator = Polynomial(*Coefficients)
        YGrid = [Generator(XValue) for XValue in self.XGrid]
        del Generator
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        self.assertIsInstance(Test, Polynomial)
        self.assertLessEqual(Test.Degree, 5)
        for XValue in self.XGrid:
            Check = Test(XValue)
            self.assertAlmostEqual(Check, YGrid)
        del Test
    
    def test_Quadratic(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        Coefficients= [random.randint(1, 3) + random.random() for _ in range(3)]
        Generator = Polynomial(*Coefficients)
        YGrid = [Generator(XValue) for XValue in self.XGrid]
        del Generator
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        self.assertIsInstance(Test, Polynomial)
        self.assertLessEqual(Test.Degree, 5)
        for XValue in self.XGrid:
            Check = Test(XValue)
            self.assertAlmostEqual(Check, YGrid)
        del Test
    
    def test_Cubic(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        Coefficients= [random.randint(1, 3) + random.random() for _ in range(4)]
        Generator = Polynomial(*Coefficients)
        YGrid = [Generator(XValue) for XValue in self.XGrid]
        del Generator
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        self.assertIsInstance(Test, Polynomial)
        self.assertLessEqual(Test.Degree, 5)
        for XValue in self.XGrid:
            Check = Test(XValue)
            self.assertAlmostEqual(Check, YGrid)
        del Test
    
    def test_FourthDegree(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        Coefficients= [random.randint(1, 3) + random.random() for _ in range(5)]
        Generator = Polynomial(*Coefficients)
        YGrid = [Generator(XValue) for XValue in self.XGrid]
        del Generator
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        self.assertIsInstance(Test, Polynomial)
        self.assertLessEqual(Test.Degree, 5)
        for XValue in self.XGrid:
            Check = Test(XValue)
            self.assertAlmostEqual(Check, YGrid)
        del Test
    
    def test_FifthDegree(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        Coefficients= [random.randint(1, 3) + random.random() for _ in range(6)]
        Generator = Polynomial(*Coefficients)
        YGrid = [Generator(XValue) for XValue in self.XGrid]
        del Generator
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        self.assertIsInstance(Test, Polynomial)
        self.assertLessEqual(Test.Degree, 5)
        for XValue in self.XGrid:
            Check = Test(XValue)
            self.assertAlmostEqual(Check, YGrid)
        del Test
    
    def test_Sine(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        YGrid = [sin(XValue) for XValue in self.XGrid]
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        self.assertIsInstance(Test, Polynomial)
        self.assertLessEqual(Test.Degree, 5)
        for XValue in self.XGrid:
            Check = Test(XValue)
            self.assertAlmostEqual(Check, YGrid)
        del Test
    
    def test_Sqrt(self):
        """
        Test ID: TEST-T-530, TEST-T-550, TEST-T-570, TEST-T-590
        
        Requirement ID: REQ-FUN-530, REQ-FUN-550, REQ-FUN-570, REQ-FUN-590
        """
        YGrid = [sqrt(XValue) for XValue in self.XGrid]
        XYGrid = list(zip(self.XGrid, YGrid))
        Test = self.TestFunc(XYGrid)
        self.assertIsInstance(Test, Polynomial)
        self.assertLessEqual(Test.Degree, 5)
        for XValue in self.XGrid:
            Check = Test(XValue)
            self.assertAlmostEqual(Check, YGrid)
        del Test

class Test_GetLegendrePolynomial(unittest.TestCase):
    """
    Unit tests for the function GetLegendrePolynomial().
    
    Test IDs: TEST-T-541, TEST-T-502 and TEST-T-503
    
    Covers requirements: REQ_FUN-541, REQ-AWM-502 and REQ-AWM-503
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetLegendrePolynomial)
        cls.Check = {
            1 : [0, 1],
            2 : [-0.5, 0, 1.5],
            3 : [0, -1.5, 0, 2.5],
            4 : [0.375, 0, -3.75, 0, 4.375],
            5 : [0, 1.875, 0, -8.75, 0, 7.875],
            6 : [-0.3125, 0, 6.5625, 0, -19.6875, 0, 14.4375],
            7 : [0, -2.1875, 0, 19.6875, 0, 43.3125, 0, 26.8125],
            8 : [0.2734, 0, -9.8438, 0, 54.1406, 0, -93.8437, 0, 50.2734],
            9 : [0, 2.4609, 0, -36.0937, 0, 140.7656, 0, -201.0937, 0, 94.9609],
            10 : [-0.2461, 0, 13.5352, 0, -117.3047, 0, 351.9141, 0,
                                                        -427.3242, 0, 180.4258]
        }
    
    def test_TypeError(self):
        """
        Test ID: TEST-T-502
        
        Requirement ID: REQ-AWM-502
        """
        WrongTypes = ['1', int, float, [1], (1, 2), {1, 2}, {1:2}, True, bool]
        for Item in WrongTypes:
            with self.assertRaises(TypeError):
                Test = self.TestFunc(Item)
    
    def test_ValueError(self):
        """
        Test ID: TEST-T-503
        
        Requirement ID: REQ-AWM-503
        """
        for _ in range(100):
            Degree = random.randint(1, 20)
            with self.assertRaises(ValueError):
                Test = self.TestFunc(-Degree)
    
    def test_Performance(self):
        """
        Test ID: TEST-T-541
        
        Requirement ID: REQ-FUN-541
        """
        Test = self.TestFunc(0)
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 1)
        for Degree in range(1, 11):
            Test = self.TestFunc(Degree)
            self.assertIsInstance(Test, Polynomial)
            self.assertEqual(Test.Degree, Degree)
            Coefficients = Test.getCoefficients()
            del Test
            self.assertEqual(len(Coefficients), Degree + 1)
            for TestValue, CheckValue in zip(Coefficients, self.Check[Degree]):
                self.assertAlmostEqual(TestValue, CheckValue)

class Test_GetLegendreBasis(unittest.TestCase):
    """
    Unit tests for the function GetLegendrePolynomial().
    
    Test IDs: TEST-T-500 and TEST-T-501
    
    Covers requirements: REQ-AWM-500 and REQ-AWM-501
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetLegendreBasis)
    
    def test_TypeError(self):
        """
        Test ID: TEST-T-500
        
        Requirement ID: REQ-AWM-500
        """
        WrongTypes = ['1', int, float, [1], (1, 2), {1, 2}, {1:2}, True, bool]
        for Item in WrongTypes:
            with self.assertRaises(TypeError):
                Test = self.TestFunc(Item)
    
    def test_ValueError(self):
        """
        Test ID: TEST-T-501
        
        Requirement ID: REQ-AWM-501
        """
        for _ in range(100):
            Degree = random.randint(1, 20)
            with self.assertRaises(ValueError):
                Test = self.TestFunc(-Degree)
    
    def test_Performance(self):
        """
        Test ID: TEST-T-540
        
        Requirement ID: REQ-FUN-540
        """
        Test = self.TestFunc(0)
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1])
        for Degree in range(1, 11):
            Test = self.TestFunc(Degree)
            self.assertIsInstance(Test, list)
            self.assertEqual(len(Test), Degree + 1)
            for Index, Item in enumerate(Test):
                if not Index:
                    self.assertIsInstance(Item, int)
                    self.assertEqual(Item, 1)
                else:
                    self.assertIsInstance(Item, Polynomial)
                    self.assertEqual(Item.Degree, Index)
                    Check = testmodule.GetChebyshevPolynomial(Degree)
                    CheckTuple = Check.getCoefficients()
                    del Check
                    TestTuple = Item.getCoefficients()
                    self.assertEqual(len(TestTuple), len(CheckTuple))
                    for TestValue, CheckValue in zip(TestTuple, CheckTuple):
                        self.assertAlmostEqual(TestValue, CheckValue)

class Test_InterpolateLegendre(Test_InterpolateLagrange):
    """
    Unit tests for the function InterpolateLegendre().
    
    Test IDs: TEST-T-550, TEST-T-504 and TEST-T-505
    
    Covers requirements: REQ-FUN-550, REQ-AWM-504 and REQ-AWM-505
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.InterpolateLegendre)
        cls.XGrid = [Index + 0.25 * random.random() for Index in range(6)]

class Test_GetChebyshevPolynomial(Test_GetLegendrePolynomial):
    """
    Unit tests for the function GetChebyshevPolynomial().
    
    Test IDs: TEST-T-561, TEST-T-502 and TEST-T-503
    
    Covers requirements: REQ-FUN-561, REQ-AWM-502 and REQ-AWM-503
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetChebyshevPolynomial)
        cls.Check = {
            1 : [0, 1],
            2 : [-1, 0, 2],
            3 : [0, -3, 0, 4],
            4 : [1, 0, -8, 0, 8],
            5 : [0, 5, 0, -20, 0, 16],
            6 : [-1, 0, 18, 0, -48, 0, 32],
            7 : [0, -7, 0, 56, 0, -112, 0, 64],
            8 : [1, 0, -32, 0, 160, 0, -256, 0, 128],
            9 : [0, 9, 0, -120, 0, 432, 0 -576, 0, 256],
            10 : [-1, 0, 50, 0, -400, 0, 1120, 0, -1280, 0, 512]
        }
    
    def test_Performance(self):
        """
        Test ID: TEST-T-561
        
        Requirement ID: REQ-FUN-561
        """
        Test = self.TestFunc(0)
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 1)
        for Degree in range(1, 11):
            Test = self.TestFunc(Degree)
            self.assertIsInstance(Test, Polynomial)
            self.assertEqual(Test.Degree, Degree)
            Coefficients = list(Test.getCoefficients())
            del Test
            self.assertListEqual(Coefficients, self.Check[Degree])

class Test_GetChebyshevBasis(Test_GetLegendreBasis):
    """
    Unit tests for the function GetChebyshevBasis().
    
    Test IDs: TEST-T-560, TEST-T-500 and TEST-T-501
    
    Covers requirements: REQ-FUN-560, REQ-AWM-500 and REQ-AWM-501
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetChebyshevBasis)
    
    def test_Performance(self):
        """
        Test ID: TEST-T-560
        
        Requirement ID: REQ-FUN-560
        """
        Test = self.TestFunc(0)
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1])
        for Degree in range(1, 11):
            Test = self.TestFunc(Degree)
            self.assertIsInstance(Test, list)
            self.assertEqual(len(Test), Degree + 1)
            for Index, Item in enumerate(Test):
                if not Index:
                    self.assertIsInstance(Item, int)
                    self.assertEqual(Item, 1)
                else:
                    self.assertIsInstance(Item, Polynomial)
                    self.assertEqual(Item.Degree, Index)
                    Check = testmodule.GetChebyshevPolynomial(Degree)
                    self.assertTupleEqual(Item.getCoefficients(),
                                                        Check.getCoefficients())
                    del Check

class Test_InterpolateChebyshev(Test_InterpolateLagrange):
    """
    Unit tests for the function InterpolateChebyshev().
    
    Test IDs: TEST-T-570, TEST-T-504 and TEST-T-505
    
    Covers requirements: REQ-FUN-570, REQ-AWM-504 and REQ-AWM-505
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.InterpolateChebyshev)
        cls.XGrid = [Index + 0.25 * random.random() for Index in range(6)]

class Test_GetBernsteinPolynomial(unittest.TestCase):
    """
    Unit tests for the function GetBernsteinPolynomial().
    
    Test IDs: TEST-T-581, TEST-T-582 and TEST-T-583
    
    Covers requirements: REQ-FUN-581, REQ-AWM-580 and REQ-AWM-581
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetBernsteinPolynomial)
        cls.Check = {
            1 : {
                0: [1, -1],
                1: [0, 1]
            },
            2: {
                0: [1, -2, 1],
                1: [0, 2, - 2],
                2: [0, 0, 1]
            },
            3: {
                0: [1, -3, 3, -1],
                1: [0, 3, -6, 3],
                2: [0, 0, 3, -3],
                3: [0, 0, 0, 1]
            },
            4: {
                0: [1, -4, 6, -4, 1],
                1: [0, 4, -12, 12, -4],
                2: [0, 0, 6, -12, 6],
                3: [0, 0, 0, 4, -4],
                4: [0, 0, 0, 0, 1]
            },
            5: {
                0: [1, -5, 10, -10, 5, -1],
                1: [0, 5, -20, 30, -20, 5],
                2: [0, 0, 10, -30, 30, -10],
                3: [0, 0, 0, 10, -20, 10],
                4: [0, 0, 0, 0, 5, -5],
                5: [0, 0, 0, 0, 0, 1]
            }
        }
    
    def test_TypeError(self):
        """
        Test ID: TEST-T-582
        
        Requirement ID: REQ-AWM-580
        """
        WrongTypes = ['1', int, float, [1], (1, 2), {1, 2}, {1:2}, True, bool]
        for Item in WrongTypes:
            with self.assertRaises(TypeError):
                Test = self.TestFunc(Item, 1)
            with self.assertRaises(TypeError):
                Test = self.TestFunc(1, Item)
            with self.assertRaises(TypeError):
                Test = self.TestFunc(Item, Item)
    
    def test_ValueError(self):
        """
        Test ID: TEST-T-583
        
        Requirement ID: REQ-AWM-581
        """
        for _ in range(100):
            Degree = random.randint(1, 20)
            with self.assertRaises(ValueError):
                Test = self.TestFunc(-Degree, 1)
            with self.assertRaises(ValueError):
                Test = self.TestFunc(1, -Degree)
            with self.assertRaises(ValueError):
                Test = self.TestFunc(-Degree, -Degree)
            BaseDegree = random.randint(0, 20)
            with self.assertRaises(ValueError):
                Test = self.TestFunc(BaseDegree, BaseDegree + Degree)
    
    def test_Performance(self):
        """
        Test ID: TEST-T-581
        
        Requirement ID: REQ-FUN-581
        """
        Test = self.TestFunc(0, 0)
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 1)
        for Degree in range(1, 6):
            for Index in range(Degree + 1):
                Test = self.TestFunc(Degree, Index)
                self.assertIsInstance(Test, Polynomial)
                self.assertEqual(Test.Degree, Degree)
                Coefficients = list(Test.getCoefficients())
                del Test
                self.assertListEqual(Coefficients, self.Check[Degree][Index])

class Test_GetBernsteinBasis(Test_GetLegendreBasis):
    """
    Unit tests for the function GetBernsteinBasis().
    
    Test IDs: TEST-T-580, TEST-T-500 and TEST-T-501
    
    Covers requirements: REQ-FUN-580, REQ-AWM-500 and REQ-AWM-501
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.GetBernsteinBasis)
    
    def test_Performance(self):
        """
        Test ID: TEST-T-580
        
        Requirement ID: REQ-FUN-580
        """
        Test = self.TestFunc(0)
        self.assertIsInstance(Test, list)
        self.assertListEqual(Test, [1])
        for Degree in range(1, 6):
            Test = self.TestFunc(Degree)
            self.assertIsInstance(Test, list)
            self.assertEqual(len(Test), Degree + 1)
            for Index, Item in enumerate(Test):
                self.assertIsInstance(Item, Polynomial)
                self.assertEqual(Item.Degree, Degree)
                Check = testmodule.GetBernsteinPolynomial(Degree, Index)
                self.assertTupleEqual(Item.getCoefficients(),
                                                        Check.getCoefficients())
                del Check

class Test_InterpolateBernstein(Test_InterpolateLagrange):
    """
    Unit tests for the function InterpolateBernstein().
    
    Test IDs: TEST-T-590, TEST-T-504 and TEST-T-505
    
    Covers requirements: REQ-FUN-590, REQ-AWM-504 and REQ-AWM-505
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparations. Called only once.
        """
        cls.TestFunc = staticmethod(testmodule.InterpolateBernstein)
        cls.XGrid = [Index + 0.25 * random.random() for Index in range(6)]

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_HelperFunctions)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_FindRoots)

TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetLagrangePolynomial)

TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetLagrangeBasis)

TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_InterpolateLagrange)

TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetLegendrePolynomial)

TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetLegendreBasis)

TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_InterpolateLegendre)

TestSuite9 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetChebyshevPolynomial)

TestSuite10 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetChebyshevBasis)

TestSuite11 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_InterpolateChebyshev)

TestSuite12 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetBernsteinPolynomial)

TestSuite13 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetBernsteinBasis)

TestSuite14 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_InterpolateBernstein)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6, TestSuite7, TestSuite8, TestSuite9, TestSuite10,
                    TestSuite11, TestSuite12, TestSuite13, TestSuite14])

if __name__ == "__main__":
    sys.stdout.write("Conducting math_extra_lib.poly_solver module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)