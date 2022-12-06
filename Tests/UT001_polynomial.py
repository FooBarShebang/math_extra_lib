#usr/bin/python3
"""
Module math_extra_lib.Tests.UT001_polynomial

Implements unit testing of the module math_extra_lib.polynomial, see TE001.
"""

__version__ = "1.0.0.0"
__date__ = "06-12-2022"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import copy

from random import randint, random, sample

from math import factorial

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
        for _ in range(self.NDegree + 1):
            Value = randint(-5, 5)
            bFloat = random()
            if bFloat >= 0.5:
                Value += random()
            self.CheckCoefficients.append(Value)
        if not self.CheckCoefficients[-1]:
            self.CheckCoefficients[-1] = 1.0
        self.TestObject = self.TestClass(*self.CheckCoefficients)
        self.NSecond = randint(2, 6)
        self.SecondCoefficients = []
        for _ in range(self.NSecond + 1):
            Value = randint(-5, 5)
            bFloat = random()
            if bFloat >= 0.5:
                Value += random()
            self.SecondCoefficients.append(Value)
        if not self.SecondCoefficients[-1]:
            self.SecondCoefficients[-1] = 1.0
        self.SecondObject = self.TestClass(*self.SecondCoefficients)
    
    def tearDown(self):
        """
        Clean-up after each test case.
        """
        del self.TestObject
        del self.CheckCoefficients
        del self.NDegree
        del self.SecondObject
        del self.SecondCoefficients
        del self.NSecond
    
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
            Temp = divmod(self.TestObject, Other)
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
                if abs(CheckValue) > 1000:
                    RelPrecision = 0.01*abs(CheckValue)
                else:
                    RelPrecision = 0.001*abs(CheckValue)
                Test = self.TestObject**Power
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(iValue)
                if abs(CheckValue) > 0.001:
                    self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                else:
                    self.assertAlmostEqual(TestValue - CheckValue, 0, places= 5)
                del Test
                Test = pow(self.TestObject, Power)
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(iValue)
                if abs(CheckValue) > 0.001:
                    self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                else:
                    self.assertAlmostEqual(TestValue - CheckValue, 0, places= 5)
                del Test
                fValue = randint(-5,5) + random()
                CheckValue = (self.TestObject(fValue))**Power
                if abs(CheckValue) > 1000:
                    RelPrecision = 0.01*abs(CheckValue)
                else:
                    RelPrecision = 0.001*abs(CheckValue)
                Test = self.TestObject**Power
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(fValue)
                if abs(CheckValue) > 0.001:
                    self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                else:
                    self.assertAlmostEqual(TestValue - CheckValue, 0, places= 5)
                del Test
                Test = pow(self.TestObject, Power)
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree * Power)
                TestValue = Test(fValue)
                if abs(CheckValue) > 0.001:
                    self.assertAlmostEqual(TestValue, CheckValue,
                                                            delta= RelPrecision)
                else:
                    self.assertAlmostEqual(TestValue - CheckValue, 0, places= 5)
                del Test
    
    def test_mulPoly(self):
        """
        Checks polynomial multiplication.
        
        Test ID: TEST-T-107
        Covers requirements: REQ-FUN-104, REQ-FUN-105
        """
        Poly1 = self.TestClass(-1, 1)
        Poly2 = self.TestClass(1, 1)
        Check = Poly1 * Poly2
        self.assertIsInstance(Check, self.TestClass)
        self.assertTupleEqual(Check.getCoefficients(), (-1, 0, 1))
        del Poly1
        del Poly2
        Check2 = Check * self.TestClass(-0.5, 1)
        del Check
        self.assertIsInstance(Check2, self.TestClass)
        self.assertTupleEqual(Check2.getCoefficients(), (0.5, -1, -0.5, 1))
        del Check2
        Poly1 = self.TestClass(1, 2, 1)
        Poly2 = self.TestClass(1, 3, 3, 1)
        Check = Poly1 * Poly2
        self.assertIsInstance(Check, self.TestClass)
        self.assertTupleEqual(Check.getCoefficients(), (1, 5, 10, 10, 5, 1))
        del Poly1
        del Poly2
        del Check
        Check = self.TestObject * self.TestObject
        Check1 = self.TestObject**2
        self.assertIsInstance(Check, self.TestClass)
        for Index, Value in enumerate(Check.getCoefficients()):
            self.assertAlmostEqual(Value, Check1[Index])
        del Check1
        Check1 = Check * self.TestObject
        del Check
        Check = self.TestObject**3
        for Index, Value in enumerate(Check.getCoefficients()):
            self.assertAlmostEqual(Value, Check1[Index])
        del Check1
        Check1 = Check * self.TestObject
        del Check
        Check = self.TestObject**4
        self.assertEqual(Check.Degree, Check1.Degree)
        for Index, Value in enumerate(Check.getCoefficients()):
            self.assertAlmostEqual(Value, Check1[Index])
        del Check
        del Check1
        for _ in range(10):
            Test = self.TestObject * self.SecondObject
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.NDegree + self.NSecond)
            for _ in range(100):
                Value = randint(-5, 5)
                if random() > 0.5:
                    Value += random()
                Value1 = self.TestObject(Value)
                Value2 = self.SecondObject(Value)
                Value3 = Test(Value)
                if abs(Value3) > 1000:
                    RelPrecision = 0.01*abs(Value3)
                else:
                    RelPrecision = 0.001*abs(Value3)
                if abs(Value1 * Value2) > RelPrecision:
                    self.assertAlmostEqual(Value3, Value1 * Value2,
                                                        delta = RelPrecision)
                else:
                    self.assertAlmostEqual(0, Value3)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_addPoly(self):
        """
        Checks polynomial addition.
        
        Test ID: TEST-T-107
        Covers requirements: REQ-FUN-105
        """
        Poly1 = self.TestClass(1, 2, 3, 1)
        Poly2 = self.TestClass(0, 1, -1)
        Test = Poly1 + Poly2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 3, 2, 1))
        del Test
        Test = Poly2 + Poly1
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 3, 2, 1))
        del Test
        del Poly2
        Poly2 = self.TestClass(0, 1, -1, -1)
        Test = Poly1 + Poly2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 3, 2))
        del Test
        del Poly2
        Poly2 = self.TestClass(0, 1, -3, -1)
        Test = Poly1 + Poly2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 3))
        del Test
        del Poly2
        Poly2 = self.TestClass(0, -2, -3, -1)
        Test = Poly1 + Poly2
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 1)
        del Test
        for _ in range(10):
            Temp = - self.TestObject
            Test = self.TestObject + Temp
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            del Temp
            del Test
            if ((self.NDegree == self.NSecond) and
                    (self.CheckCoefficients[-1]==-self.SecondCoefficients[-1])):
                continue
            Test = self.TestObject + self.SecondObject
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, max(self.NDegree, self.NSecond))
            for _ in range(100):
                Value = randint(-5, 5)
                if random() > 0.5:
                    Value += random()
                Value1 = self.TestObject(Value)
                Value2 = self.SecondObject(Value)
                Value3 = Test(Value)
                RelPrecision = 0.00001 * abs(Value3)
                self.assertAlmostEqual(Value3, Value1 + Value2,
                                                        delta = RelPrecision)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_subPoly(self):
        """
        Checks polynomial subtraction.
        
        Test ID: TEST-T-107
        Covers requirements: REQ-FUN-105
        """
        Poly1 = self.TestClass(1, 2, 3, 1)
        Poly2 = self.TestClass(0, 1, -1)
        Test = Poly1 - Poly2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 1, 4, 1))
        del Test
        Test = Poly2 - Poly1
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (-1, -1, -4, -1))
        del Test
        del Poly2
        Poly2 = self.TestClass(0, 1, -1, 1)
        Test = Poly1 - Poly2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 1, 4))
        del Test
        del Poly2
        Poly2 = self.TestClass(0, 1, 3, 1)
        Test = Poly1 - Poly2
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (1, 1))
        del Test
        del Poly2
        Poly2 = self.TestClass(0, 2, 3, 1)
        Test = Poly1 - Poly2
        self.assertIsInstance(Test, int)
        self.assertEqual(Test, 1)
        del Test
        for _ in range(10):
            Test = self.TestObject - self.TestObject
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            del Test
            if ((self.NDegree == self.NSecond) and
                    (self.CheckCoefficients[-1]== self.SecondCoefficients[-1])):
                continue
            Test = self.TestObject - self.SecondObject
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, max(self.NDegree, self.NSecond))
            for _ in range(100):
                Value = randint(-5, 5)
                if random() > 0.5:
                    Value += random()
                Value1 = self.TestObject(Value)
                Value2 = self.SecondObject(Value)
                Value3 = Test(Value)
                RelPrecision = 0.00001 * abs(Value3)
                self.assertAlmostEqual(Value3, Value1 - Value2,
                                                        delta = RelPrecision)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_divPoly(self):
        """
        Checks polynomial division.
        
        Test ID: TEST-T-107
        Covers requirements: REQ-FUN-105
        """
        Divident = self.TestClass(1, 0, -2, 0, 1)
        Divisor = self.TestClass(-1, 0, 1)
        Quot, Rem = divmod(Divident, Divisor)
        self.assertIsInstance(Quot, self.TestClass)
        self.assertTupleEqual(Quot.getCoefficients(), (-1, 0, 1))
        self.assertIsInstance(Rem, int)
        self.assertEqual(Rem, 0)
        del Quot
        Quot = Divident // Divisor
        Rem = Divident % Divisor
        self.assertIsInstance(Quot, self.TestClass)
        self.assertTupleEqual(Quot.getCoefficients(), (-1, 0, 1))
        self.assertIsInstance(Rem, int)
        self.assertEqual(Rem, 0)
        del Quot
        del Divisor
        Divisor = self.TestClass(-1, 1)
        Quot, Rem = divmod(Divident, Divisor)
        self.assertIsInstance(Quot, self.TestClass)
        self.assertTupleEqual(Quot.getCoefficients(), (-1, -1, 1, 1))
        self.assertIsInstance(Rem, int)
        self.assertEqual(Rem, 0)
        del Quot
        Quot = Divident // Divisor
        Rem = Divident % Divisor
        self.assertIsInstance(Quot, self.TestClass)
        self.assertTupleEqual(Quot.getCoefficients(), (-1, -1, 1, 1))
        self.assertIsInstance(Rem, int)
        self.assertEqual(Rem, 0)
        del Quot
        del Divisor
        Divisor = self.TestClass(1, 1)
        Quot, Rem = divmod(Divident, Divisor)
        self.assertIsInstance(Quot, self.TestClass)
        self.assertTupleEqual(Quot.getCoefficients(), (1, -1, -1, 1))
        self.assertIsInstance(Rem, int)
        self.assertEqual(Rem, 0)
        del Quot
        Quot = Divident // Divisor
        Rem = Divident % Divisor
        self.assertIsInstance(Quot, self.TestClass)
        self.assertTupleEqual(Quot.getCoefficients(), (1, -1, -1, 1))
        self.assertIsInstance(Rem, int)
        self.assertEqual(Rem, 0)
        del Quot
        del Divisor
        for _ in range(10):
            Quot, Rem = divmod(self.TestObject, self.TestObject)
            self.assertIsInstance(Quot, (int, float))
            self.assertEqual(Quot, 1)
            self.assertIsInstance(Rem, int)
            self.assertEqual(Rem, 0)
            Quot = self.TestObject // self.TestObject
            Rem = self.TestObject % self.TestObject
            self.assertIsInstance(Quot, (int, float))
            self.assertEqual(Quot, 1)
            self.assertIsInstance(Rem, int)
            self.assertEqual(Rem, 0)
            Quot, Rem = divmod(self.TestObject, self.SecondObject)
            Quot1 = self.TestObject // self.SecondObject
            Rem1 = self.TestObject % self.SecondObject
            if self.NDegree < self.NSecond:
                self.assertIsInstance(Quot, int)
                self.assertIsInstance(Quot1, int)
                self.assertEqual(Quot, 0)
                self.assertEqual(Quot1, 0)
                self.assertIsInstance(Rem, self.TestClass)
                self.assertIsInstance(Rem1, self.TestClass)
                Coefficients = Rem.getCoefficients()
                for Index, Value in enumerate(self.CheckCoefficients):
                    self.assertAlmostEqual(Value, Coefficients[Index])
                Coefficients = Rem1.getCoefficients()
                for Index, Value in enumerate(self.CheckCoefficients):
                    self.assertAlmostEqual(Value, Coefficients[Index])
            elif self.NDegree == self.NSecond:
                self.assertIsInstance(Quot, (int, float))
                self.assertIsInstance(Quot1, (int, float))
                TestValue=self.CheckCoefficients[-1]/self.SecondCoefficients[-1]
                self.assertAlmostEqual(Quot, TestValue)
                self.assertAlmostEqual(Quot1, TestValue)
                if isinstance(Rem, (int, float)):
                    self.assertIsInstance(Rem1, (int, float))
                    self.assertAlmostEqual(Rem, Rem1)
                else:
                    self.assertIsInstance(Rem, self.TestClass)
                    self.assertIsInstance(Rem1, self.TestClass)
                    self.assertLessEqual(Rem.Degree, self.NSecond)
                    self.assertTupleEqual(Rem.getCoefficients(),
                                                        Rem1.getCoefficients())
            else:
                self.assertIsInstance(Quot, self.TestClass)
                self.assertIsInstance(Quot1, self.TestClass)
                self.assertEqual(Quot.Degree, self.NDegree - self.NSecond)
                self.assertTupleEqual(Quot.getCoefficients(),
                                                        Quot1.getCoefficients())
                if isinstance(Rem, (int, float)):
                    self.assertIsInstance(Rem1, (int, float))
                    self.assertAlmostEqual(Rem, Rem1)
                else:
                    self.assertIsInstance(Rem, self.TestClass)
                    self.assertIsInstance(Rem1, self.TestClass)
                    self.assertLessEqual(Rem.Degree, self.NSecond)
                    self.assertTupleEqual(Rem.getCoefficients(),
                                                        Rem1.getCoefficients())
            for _ in range(100):
                Value = randint(-5, 5) + random()
                DtValue = self.TestObject(Value)
                DrValue =  self.SecondObject(Value)
                if not DrValue:
                    CheckValue = DtValue / DrValue
                    if isinstance(Quot, self.TestClass):
                        QuotValue = Quot(Value)
                    else:
                        QuotValue = Quot
                    if isinstance(Rem, self.TestClass):
                        RemValue = Rem(Value) / DrValue
                    else:
                        RemValue = Rem / DrValue
                    TestValue = QuotValue + RemValue
                    self.assertAlmostEqual(TestValue, CheckValue)
            if isinstance(Quot, self.TestClass):
                del Quot
                del Quot1
            if isinstance(Rem, self.TestClass):
                del Rem
                del Rem1
            self.tearDown()
            self.setUp()
    
    def test_antiderivative(self):
        """
        Checks polynomial anti-derivative calculation.
        
        Test ID: TEST-T-108
        Covers requirements: REQ-FUN-107
        """
        for _ in range(10):
            Test = self.TestObject.getAntiderivative()
            self.assertIsInstance(Test, self.TestClass)
            self.assertEqual(Test.Degree, self.NDegree + 1)
            self.assertEqual(Test[0], 0)
            for Index in range(1, self.NDegree + 2):
                self.assertAlmostEqual(Test[Index],
                                    self.CheckCoefficients[Index - 1] / Index)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_derivative(self):
        """
        Checks polynomial anti-derivative calculation.
        
        Test ID: TEST-T-108
        Covers requirements: REQ-FUN-106
        """
        for _ in range(10):
            Test = self.TestObject.getDerivative()
            self.assertEqual(Test.Degree, self.NDegree - 1)
            for Index, Value in enumerate(Test.getCoefficients()):
                CheckValue = self.CheckCoefficients[Index + 1] * (Index + 1)
                self.assertAlmostEqual(Value, CheckValue)
            del Test
            for Power in range(1, self.NDegree):
                Test = self.TestObject.getDerivative(Degree = Power)
                self.assertIsInstance(Test, self.TestClass)
                self.assertEqual(Test.Degree, self.NDegree - Power)
                for Index, Value in enumerate(Test.getCoefficients()):
                    CheckValue = self.CheckCoefficients[Index + Power]
                    CheckValue *= factorial(Index + Power)
                    CheckValue /= factorial(Index)
                    self.assertAlmostEqual(Value, CheckValue)
                del Test
            Test = self.TestObject.getDerivative(Degree = self.NDegree)
            self.assertIsInstance(Test, (int, float))
            self.assertEqual(Test,
                        factorial(self.NDegree) * self.CheckCoefficients[-1])
            Test = self.TestObject.getDerivative(Degree = self.NDegree + 1)
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            Test = self.TestObject.getDerivative(
                                        Degree = self.NDegree + randint(2, 5))
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
            Test = self.TestObject.getDerivative(
                                        Degree = self.NDegree + randint(5, 10))
            self.assertIsInstance(Test, int)
            self.assertEqual(Test, 0)
    
    def test_convolution(self):
        """
        Checks polynomials convolution calculation.
        
        Test ID: TEST-T-109
        Covers requirements: REQ-FUN-108
        """
        Poly1 = self.TestClass(1, 1, 1)
        Poly2 = self.TestClass(-1, 0, 1)
        Test = Poly2.getConvolution(Poly1)
        self.assertIsInstance(Test, self.TestClass)
        self.assertTupleEqual(Test.getCoefficients(), (0, 2, 3, 2, 1))
        del Test
        del Poly1
        del Poly2
        Poly1 = self.TestClass(randint(0, 5), randint(0, 5) + random(),
                                        randint(0, 5) + random(), randint(1, 5))
        Poly2 = self.TestClass(randint(0, 5), randint(0, 5) + random(),
                                                                randint(1, 5))
        Test = Poly2.getConvolution(Poly1)
        self.assertEqual(Test.Degree, 6)
        self.assertIsInstance(Test, self.TestClass)
        Test2 = Poly2[0] + Poly2[1] * Poly1 + Poly2[2] * (Poly1**2)
        for Index, Value in enumerate(Test2.getCoefficients()):
            self.assertAlmostEqual(Test[Index], Value)
        del Test2
        del Test
        del Poly2
        del Poly1

class Test_Rational(unittest.TestCase):
    """
    Test cases for the class math_extra_lib.polynomial.RationalFunction
    
    Implements tests: TEST-T-110 to TEST-T-114.
    
    Covers the requirements: REQ-FUN-110 to REQ-FUN-112 and REQ-AWM-110 to
    REQ-AWM-113.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.RationalFunction
    
    def test_init(self):
        """
        Checks the instantiation of a rational function.
        
        Test ID: TEST-T-110
        Covers requirements: REQ-FUN-110
        """
        for _ in range(10):
            Degree1 = randint(1, 5)
            Degree2 = randint(1, 5)
            Coefficients1 = [randint(-5, 5) + random() for _ in range(Degree1)]
            Coefficients2 = [randint(-5, 5) + random() for _ in range(Degree2)]
            Coefficients1.append(randint(1, 5))
            Coefficients2.append(randint(1, 5))
            Coefficients1 = tuple(Coefficients1)
            Coefficients2 = tuple(Coefficients2)
            TestObject = self.TestClass(Coefficients1, Coefficients2)
            self.assertIsInstance(TestObject, self.TestClass)
            Check = TestObject.getCoefficients()
            self.assertIsInstance(Check, tuple)
            self.assertEqual(len(Check),2)
            self.assertIsInstance(Check[0], tuple)
            self.assertTupleEqual(Check[0], Coefficients1)
            self.assertIsInstance(Check[1], tuple)
            self.assertTupleEqual(Check[1], Coefficients2)
            del TestObject
            TestObject = self.TestClass(testmodule.Polynomial(*Coefficients1),
                                                                Coefficients2)
            self.assertIsInstance(TestObject, self.TestClass)
            Check = TestObject.getCoefficients()
            self.assertIsInstance(Check, tuple)
            self.assertEqual(len(Check),2)
            self.assertIsInstance(Check[0], tuple)
            self.assertTupleEqual(Check[0], Coefficients1)
            self.assertIsInstance(Check[1], tuple)
            self.assertTupleEqual(Check[1], Coefficients2)
            del TestObject
            TestObject = self.TestClass(Coefficients1,
                                        testmodule.Polynomial(*Coefficients2))
            self.assertIsInstance(TestObject, self.TestClass)
            Check = TestObject.getCoefficients()
            self.assertIsInstance(Check, tuple)
            self.assertEqual(len(Check),2)
            self.assertIsInstance(Check[0], tuple)
            self.assertTupleEqual(Check[0], Coefficients1)
            self.assertIsInstance(Check[1], tuple)
            self.assertTupleEqual(Check[1], Coefficients2)
            del TestObject
            TestObject = self.TestClass(testmodule.Polynomial(*Coefficients1),
                                        testmodule.Polynomial(*Coefficients2))
            self.assertIsInstance(TestObject, self.TestClass)
            Check = TestObject.getCoefficients()
            self.assertIsInstance(Check, tuple)
            self.assertEqual(len(Check),2)
            self.assertIsInstance(Check[0], tuple)
            self.assertTupleEqual(Check[0], Coefficients1)
            self.assertIsInstance(Check[1], tuple)
            self.assertTupleEqual(Check[1], Coefficients2)
            del TestObject
    
    def test_evaluate(self):
        """
        Checks the instantiation of a rational function.
        
        Test ID: TEST-T-110
        Covers requirements: REQ-FUN-111, REQ-FUN-112
        """
        Poly1 = testmodule.Polynomial(1,1)**3
        Poly2 = testmodule.Polynomial(1,1)**3
        TestObject = self.TestClass(Poly1, Poly2)
        Check = TestObject(-1)
        self.assertIsInstance(Check, (int, float))
        self.assertAlmostEqual(Check, 1)
        del Poly2
        del TestObject
        Poly2 = testmodule.Polynomial(1,1)**2
        TestObject = self.TestClass(Poly1, Poly2)
        Check = TestObject(-1)
        self.assertIsInstance(Check, (int, float))
        self.assertEqual(Check, 0)
        del Poly2
        del TestObject
        Poly2 = testmodule.Polynomial(1,1)**4
        TestObject = self.TestClass(Poly1, Poly2)
        #Check = TestObject(-1) - check for singularity
        del Poly2
        del TestObject
        for _ in range(10):
            Degree1 = randint(1, 5)
            Degree2 = randint(1, 5)
            Coefficients1 = [randint(-5, 5) + random() for _ in range(Degree1)]
            Coefficients2 = [randint(-5, 5) + random() for _ in range(Degree2)]
            Coefficients1.append(randint(1, 5))
            Coefficients2.append(randint(1, 5))
            TestObject = self.TestClass(Coefficients1, Coefficients2)
            Divident = testmodule.Polynomial(*Coefficients1)
            Divisor = testmodule.Polynomial(*Coefficients2)
            Values = list()
            while len(Values) < 10:
                Value = randint(-5, 5) + random()
                if Divisor(Value):
                    Values.append(Value)
            RootValue = None
            for Value in Values:
                CheckValue = Divident(Value) / Divisor(Value)
                TestValue = TestObject(Value)
                self.assertIsInstance(TestValue, (int, float))
                self.assertAlmostEqual(CheckValue, TestValue)
                if TestValue:
                    RootValue = Value
            del TestObject
            ExtraPoly = testmodule.Polynomial(-RootValue,1)
            self.assertAlmostEqual(ExtraPoly(RootValue), 0)
            CheckValue = Divident(RootValue) / Divisor(RootValue)
            TestObject = self.TestClass(Divident*ExtraPoly, Divisor*ExtraPoly)
            TestValue = TestObject(RootValue)
            self.assertIsInstance(TestValue, (int, float))
            self.assertAlmostEqual(CheckValue, TestValue)
            del TestObject
            TestObject = self.TestClass(Divident*ExtraPoly*ExtraPoly,
                                                    Divisor*ExtraPoly*ExtraPoly)
            TestValue = TestObject(RootValue)
            self.assertIsInstance(TestValue, (int, float))
            self.assertAlmostEqual(CheckValue, TestValue)
            del TestObject
            TestObject = self.TestClass(Divident*ExtraPoly*ExtraPoly*ExtraPoly,
                                        Divisor*ExtraPoly*ExtraPoly*ExtraPoly)
            TestValue = TestObject(RootValue)
            self.assertIsInstance(TestValue, (int, float))
            self.assertAlmostEqual(CheckValue, TestValue)
            del TestObject

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Polynomial)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_Rational)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting math_extra_lib.polynomial module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)