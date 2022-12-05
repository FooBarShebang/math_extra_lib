#usr/bin/python3
"""
Module math_extra_lib.Tests.UT001_polynomial

Implements unit testing of the module math_extra_lib.polynomial, see TE001.
"""

__version__ = "1.0.0.0"
__date__ = "05-12-2022"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import copy

from random import randint, random, sample

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.polynomial as testmodule

#classes

#+ test cases

class Test_Polynomial(unittest.TestCase):
    """
    Test cases for the class math_extra_lib.polynomial.Polynomial
    
    Implements tests: TEST-T-100 to TEST-T-10B.
    
    Covers the requirements: REQ-FUN-100 to REQ-FUN-108 and REQ-AWM-100 to
    REQ-AWM-103.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.Polynomial
    
    def setUp(self):
        """
        Single test preparation. Performed before each test case.
        """
        self.NDegree = randint(3, 6)
        self.CheckCoefficients = []
        for Index in range(self.NDegree + 1):
            Value = randint(-5, 5)
            bFloat = random()
            if bFloat >= 0.5:
                Value += random()
            self.CheckCoefficients.append(Value)
        if not self.CheckCoefficients[-1]:
            self.CheckCoefficients[-1] = 1.0
        self.TestObject = self.TestClass(*self.CheckCoefficients)
    
    def tearDown(self):
        """
        Clean-up after each test case.
        """
        del self.TestObject
        del self.CheckCoefficients
        del self.NDegree
    
    def test_initialization(self):
        """
        Tests intialization, immutability and evaluation of a polynomial.
        
        Test ID: TEST-T-100
        Requirements: REQ-FUN-100, REQ-FUN-102, REQ-FUN-103
        """
        def CheckClosure(strMsg):
            TestCoefficients = self.TestObject.getCoefficients()
            for Index, Value in enumerate(self.CheckCoefficients):
                self.assertEqual(self.TestObject.Degree, self.NDegree,
                            msg = 'degree of polynomial - {}'.format(strMsg))
                self.assertEqual(TestCoefficients[Index], Value,
                        msg = 'getCoefficients() - index {} - {}'.format(Index,
                                                                        strMsg))
                self.assertEqual(self.TestObject[Index], Value,
                        msg = 'direct - index {} - {}'.format(Index, strMsg))
            
        for _ in range(20):
            CheckClosure('initialization')
            Other = self.TestClass(1,1,1)
            Temp = +self.TestObject
            CheckClosure('identity')
            Temp = -self.TestObject
            CheckClosure('negation')
            Temp = self.TestObject + 1
            CheckClosure('right scalar addition')
            Temp = self.TestObject + Other
            CheckClosure('polynomial addition')
            Temp = 1.0 + self.TestObject
            CheckClosure('left scalar addition')
            Temp = self.TestObject - 1.0
            CheckClosure('right scalar substraction')
            Temp = self.TestObject - Other
            CheckClosure('polynomial substraction')
            Temp = 1.0 - self.TestObject
            CheckClosure('left scalar substraction')
            Temp = self.TestObject * 2
            CheckClosure('right scalar multiplication')
            Temp = self.TestObject * Other
            CheckClosure('polynomial multiplication')
            Temp = 1.5 * self.TestObject
            CheckClosure('left scalar multiplication')
            Temp = self.TestObject / 2
            CheckClosure('scalar division')
            Temp = self.TestObject ** 2
            CheckClosure('exponentiation')
            Temp = pow(self.TestObject, 2)
            CheckClosure('functional exponentiation')
            Temp = self.TestObject // Other
            CheckClosure('polynomial division quotient')
            Temp = self.TestObject % Other
            CheckClosure('polynomial division remainder')
            Temp = divmod(self.TestObject, 2)
            CheckClosure('divmod()')
            Temp = self.TestObject.getAntiderivative()
            CheckClosure('antiderivative')
            Temp = self.TestObject.getDerivative()
            CheckClosure('the first derivative')
            Temp = self.TestObject.getDerivative(2)
            CheckClosure('the second derivative')
            Temp = self.TestObject.getConvolution(Other)
            CheckClosure('convolution')
            for Index in range(self.TestObject.Degree + 1):
                with self.assertRaises(Exception):
                    self.TestObject[Index] = 1
            CheckClosure('index assignment')
            Test = self.TestObject(0)
            self.assertEqual(Test, self.TestObject[0], msg ='evaluation at 0')
            Check = sum(Item for Item in self.TestObject.getCoefficients())
            Test = self.TestObject(1)
            self.assertAlmostEqual(Test, Check, delta = abs(0.0001 * Check),
                                                        msg ='evaluation at 1')
            for _ in range(10):
                Value = randint(-5, 5)
                bFloat = random()
                if bFloat >= 0.5:
                    Value += random()
                Check = sum(Item * pow(Value, Index) for Index, Item in
                                enumerate(self.TestObject.getCoefficients()))
                Test = self.TestObject(Value)
                self.assertAlmostEqual(Test, Check, delta = abs(0.0001 * Check),
                                        msg ='evaluation at {}'.format(Value))
            self.tearDown()
            self.setUp()
    
    def test_FromRoots(self):
        """
        Checks creation of a polynomial from its roots.
        
        Test ID: TEST-T-103
        Covers requirements: REQ-FUN-101
        """
        TestObject = self.TestClass.fromRoots(1)
        # x-1
        self.assertTupleEqual((-1,1), TestObject.getCoefficients())
        self.assertAlmostEqual(0, TestObject(1))
        self.assertNotEqual(0, TestObject(2))
        del TestObject
        TestObject = self.TestClass.fromRoots(1, -1)
        # x^2 - 1
        self.assertTupleEqual((-1, 0, 1), TestObject.getCoefficients())
        self.assertAlmostEqual(0, TestObject(1))
        self.assertAlmostEqual(0, TestObject(-1))
        self.assertNotEqual(0, TestObject(2))
        del TestObject
        TestObject = self.TestClass.fromRoots(-1, 1)
        # x^2 -1
        self.assertTupleEqual((-1, 0, 1), TestObject.getCoefficients())
        del TestObject
        TestObject = self.TestClass.fromRoots(1, 1)
        # (x-1)^2 = x^2 - 2*x + 1
        self.assertTupleEqual((1, -2, 1), TestObject.getCoefficients())
        self.assertAlmostEqual(0, TestObject(1))
        self.assertNotEqual(0, TestObject(2))
        del TestObject
        TestObject = self.TestClass.fromRoots(1, -1, 0.5)
        # x^3 -0.5*x^2 - x + 0.5
        self.assertTupleEqual((0.5, -1, -0.5, 1), TestObject.getCoefficients())
        self.assertAlmostEqual(0, TestObject(1))
        self.assertAlmostEqual(0, TestObject(-1))
        self.assertAlmostEqual(0, TestObject(0.5))
        self.assertNotEqual(0, TestObject(2))
        del TestObject
        TestObject = self.TestClass.fromRoots(-1, 0.5, 1)
        # x^3 -0.5*x^2 - x + 0.5
        self.assertTupleEqual((0.5, -1, -0.5, 1), TestObject.getCoefficients())
        del TestObject
        for _ in range(20):
            NDegree = randint(1, 6)
            Roots = []
            for _ in range(NDegree):
                Value = randint(-5, 5)
                bFloat = random()
                if bFloat >= 0.5:
                    Value += random()
                Roots.append(Value)
            TestObject = self.TestClass.fromRoots(*Roots)
            CheckCoefficients = TestObject.getCoefficients()
            self.assertEqual(1, CheckCoefficients[-1])
            for Root in Roots:
                self.assertAlmostEqual(0, TestObject(Root))
            while True:
                Value = randint(-5, 5) + random()
                if not (Value in Roots):
                    break
            self.assertNotEqual(0, TestObject(Value))
            del TestObject
            for _ in range(10):
                NewRoots = sample(Roots, k=len(Roots))
                TestObject = self.TestClass.fromRoots(*NewRoots)
                NewCoefficients = TestObject.getCoefficients()
                for Index, Value in enumerate(CheckCoefficients):
                    self.assertAlmostEqual(Value, NewCoefficients[Index])
                del TestObject
    
    def test_addScalar(self):
        """
        Checks right scalar addition.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        for _ in range(10):
            iValue = randint(-5, 5)
            fValue = randint(-5, 5) + random()
            Test = self.TestObject + iValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            self.assertAlmostEqual(Coefficients[0],
                                            self.CheckCoefficients[0] + iValue)
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], Value)
            del Test
            Test = self.TestObject + fValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            self.assertAlmostEqual(Coefficients[0],
                                            self.CheckCoefficients[0] + fValue)
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], Value)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_subScalar(self):
        """
        Checks right scalar subtraction.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        for _ in range(10):
            iValue = randint(-5, 5)
            fValue = randint(-5, 5) + random()
            Test = self.TestObject - iValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            self.assertAlmostEqual(Coefficients[0],
                                            self.CheckCoefficients[0] - iValue)
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], Value)
            del Test
            Test = self.TestObject - fValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            self.assertAlmostEqual(Coefficients[0],
                                            self.CheckCoefficients[0] - fValue)
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], Value)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_raddScalar(self):
        """
        Checks left scalar addition.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        for _ in range(10):
            iValue = randint(-5, 5)
            fValue = randint(-5, 5) + random()
            Test = self.TestObject + iValue
            self.assertIsInstance(Test, self.TestClass)
            Coefficients = Test.getCoefficients()
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            self.assertAlmostEqual(Coefficients[0],
                                            self.CheckCoefficients[0] + iValue)
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], Value)
            del Test
            Test = self.TestObject + fValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            self.assertAlmostEqual(Coefficients[0],
                                            self.CheckCoefficients[0] + fValue)
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], Value)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_rsubScalar(self):
        """
        Checks left scalar subtraction.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        for _ in range(10):
            iValue = randint(-5, 5)
            fValue = randint(-5, 5) + random()
            Test = iValue - self.TestObject
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            self.assertAlmostEqual(Coefficients[0],
                                            iValue - self.CheckCoefficients[0])
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], -Value)
            del Test
            Test = fValue - self.TestObject
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            self.assertAlmostEqual(Coefficients[0],
                                            fValue - self.CheckCoefficients[0])
            for Index, Value in enumerate(self.CheckCoefficients[1:]):
                self.assertAlmostEqual(Coefficients[Index + 1], -Value)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_mulScalar(self):
        """
        Checks right scalar multiplication.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        for _ in range(10):
            while True:
                iValue = randint(-5, 5)
                if iValue:
                    break
            while True:
                fValue = randint(-5, 5) + random()
                if fValue:
                    break
            Test = self.TestObject * iValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            for Index, Value in enumerate(self.CheckCoefficients):
                self.assertAlmostEqual(Coefficients[Index], Value * iValue)
            del Test
            Test = self.TestObject * fValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            for Index, Value in enumerate(self.CheckCoefficients):
                self.assertAlmostEqual(Coefficients[Index], Value * fValue)
            del Test
            Test = self.TestObject * 0
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            del Test
            Test = self.TestObject * 0.0
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_rmulScalar(self):
        """
        Checks left scalar multiplication.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        for _ in range(10):
            while True:
                iValue = randint(-5, 5)
                if iValue:
                    break
            while True:
                fValue = randint(-5, 5) + random()
                if fValue:
                    break
            Test = iValue * self.TestObject
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            for Index, Value in enumerate(self.CheckCoefficients):
                self.assertAlmostEqual(Coefficients[Index], Value * iValue)
            del Test
            Test = fValue * self.TestObject
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            for Index, Value in enumerate(self.CheckCoefficients):
                self.assertAlmostEqual(Coefficients[Index], Value * fValue)
            del Test
            Test = 0 * self.TestObject
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            del Test
            Test = 0.0 * self.TestObject
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_truediv(self):
        """
        Checks the division by a scalar.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        for _ in range(10):
            while True:
                iValue = randint(-5, 5)
                if iValue:
                    break
            while True:
                fValue = randint(-5, 5) + random()
                if fValue:
                    break
            Test = self.TestObject / iValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            for Index, Value in enumerate(self.CheckCoefficients):
                self.assertAlmostEqual(Coefficients[Index], Value / iValue)
            del Test
            Test = self.TestObject / fValue
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.TestObject.Degree)
            Coefficients = Test.getCoefficients()
            for Index, Value in enumerate(self.CheckCoefficients):
                self.assertAlmostEqual(Coefficients[Index], Value / fValue)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_copy(self):
        """
        Tests the shallow copying of a polynomial.
        """
        Test = copy.copy(self.TestObject)
        self.assertIsNot(Test, self.TestObject)
        self.assertIsInstance(Test, self.TestClass)
        self.assertEqual(Test.Degree, self.TestObject.Degree)
        TestCoefficients = Test.getCoefficients()
        for Index, Value in enumerate(self.CheckCoefficients):
            self.assertEqual(TestCoefficients[Index], Value)
        del Test
    
    def test_pos(self):
        """
        Tests the unary plus - identity operation of a polynomial.
        """
        Test = +self.TestObject
        self.assertIsNot(Test, self.TestObject)
        self.assertIsInstance(Test, self.TestClass)
        self.assertEqual(Test.Degree, self.TestObject.Degree)
        TestCoefficients = Test.getCoefficients()
        for Index, Value in enumerate(self.CheckCoefficients):
            self.assertEqual(TestCoefficients[Index], Value)
        del Test
    
    def test_neg(self):
        """
        Tests the unary minus - negation of a polynomial.
        """
        Test = -self.TestObject
        self.assertIsInstance(Test, self.TestClass)
        self.assertEqual(Test.Degree, self.TestObject.Degree)
        TestCoefficients = Test.getCoefficients()
        for Index, Value in enumerate(self.CheckCoefficients):
            self.assertEqual(TestCoefficients[Index], -Value)
        del Test
    
    def test_pow(self):
        """
        Checks the exponentiation.
        
        Test ID: TEST-T-106
        Covers requirements: REQ-FUN-104
        """
        MyPoly = self.TestClass(1, 1)
        Test = MyPoly**1
        self.assertIsNot(Test, MyPoly)
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1,1))
        del Test
        Test = MyPoly**2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 2, 1))
        del Test
        Test = MyPoly**3
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 3, 3, 1))
        del Test
        Test = MyPoly**4
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 4, 6, 4, 1))
        del Test
        Test = MyPoly**5
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 5, 10, 10, 5, 1))
        del Test
        MyPoly = self.TestClass(1, 1, 1)
        Test = MyPoly**1
        self.assertIsNot(Test, MyPoly)
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 1, 1))
        del Test
        Test = MyPoly**2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 2, 3, 2, 1))
        del Test
        Test = MyPoly**3
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 3, 6, 7, 6, 3, 1))
        del Test
        del MyPoly
        for _ in range(10):
            for _ in range(10):
                Power = randint(1, 5)
                iValue = randint(-5,5)
                CheckValue = (self.TestObject(iValue))**Power
                RelPrecision = 0.0001*abs(CheckValue)
                Test = self.TestObject**Power
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(iValue)
                self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                del Test
                Test = pow(self.TestObject, Power)
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(iValue)
                self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                del Test
                fValue = randint(-5,5) + random()
                CheckValue = (self.TestObject(fValue))**Power
                RelPrecision = 0.0001*abs(CheckValue)
                Test = self.TestObject**Power
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(fValue)
                self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                del Test
                Test = pow(self.TestObject, Power)
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(fValue)
                self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                del Test

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Polynomial)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, ])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting math_extra_lib.polynomial module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)