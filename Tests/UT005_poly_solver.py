#usr/bin/python3
"""
Module math_extra_lib.Tests.UT004_poly_solver

Implements unit testing of the module math_extra_lib.poly_solver, see TE005.
"""

__version__ = "1.0.0.0"
__date__ = "02-11-2023"
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

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_HelperFunctions)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1])

if __name__ == "__main__":
    sys.stdout.write("Conducting math_extra_lib.poly_solver module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)