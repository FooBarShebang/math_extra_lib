#usr/bin/python3
"""
Module math_extra_lib.Tests.UT003_vectors_matrices

Implements unit testing of the module math_extra_lib.vectors_matrices, see TE003
"""

__version__ = "1.0.0.0"
__date__ = "24-03-2023"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import copy
import random
from math import sqrt

from collections.abc import Sequence

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import math_extra_lib.vectors_matrices as testmodule

#classes

#+ test cases

class Test_Vector(unittest.TestCase):
    """
    Unit tests for the generic vector class.
    
    Test IDs: TEST-T-300, TEST-T-301, TEST-T-302, TEST-T-303, TEST-T-304,
        TEST-T-305, TEST-T-306, TEST-T-307, TEST-T-308, TEST-T-309
    
    Covers requirements: REQ-FUN-301, REQ-FUN-302, REQ-FUN-303, REQ-FUN-310,
        REQ-AWM-300, REQ-AWM-301, REQ-AWM-302, REQ-AWM-303, REQ-AWM-304,
        REQ-AWM-305, REQ-AWM-306, REQ-AWM-307, REQ-AWM-308

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.Vector
        cls.NotScalar = (int, float, '1', testmodule.Vector(1,1),
                            testmodule.Column(1,1), testmodule.Row(1,1),
                            testmodule.Matrix(((1,1),(1,1))),
                            testmodule.SquareMatrix(((1,1),(1,1))),
                            [1,1], (1,1), {1:1, 1:1}, {1, 2})
    
    def setUp(self) -> None:
        """
        Preparation of each individual unit test.
        """
        Length = random.randint(3, 10)
        Elements = list()
        for _ in range(Length):
            Item = random.randint(-100, 100)
            if random.random() >= 0.5:
                Item += random.random()
            Elements.append(Item)
        self.TestObject = self.TestClass(*Elements)
    
    def tearDown(self) -> None:
        """
        Cleaning up after each individual unit test.
        """
        del self.TestObject
    
    def test_init(self):
        """
        Checks instantiation of a vector class from a random number of numeric
        argumemts. Checks the Size property and elements read access via an
        integer index.
        
        Test ID: TEST-T-300
        
        Covers requirements: REQ-FUN-301, REQ-FUN-302
        """
        for _ in range(10):
            Length = random.randint(2, 10)
            Elements = list()
            for _ in range(Length):
                Item = random.randint(-100, 100)
                if random.random() >= 0.5:
                    Item += random.random()
                Elements.append(Item)
            objTest = self.TestClass(*Elements) #instantiation check
            self.assertNotIsInstance(objTest, Sequence)
            Size = objTest.Size #dimenstions / length / size property check
            self.assertIsInstance(Size, int)
            self.assertEqual(Size, Length)
            with self.assertRaises(AttributeError):
                objTest.Size = 10 #read-only property
            self.assertEqual(objTest.Size, Size)
            for Index in range(-Length, Length): #index read access
                Item = objTest[Index]
                self.assertIsInstance(Item, (int, float))
                self.assertEqual(Item, Elements[Index])
                with self.assertRaises(TypeError):
                    objTest[Index] = random.random()
            AsList = objTest.Data #serialization check
            self.assertIsInstance(AsList, list)
            self.assertListEqual(AsList, Elements)
            for Index in range(Length): #immurability check
                AsList[Index] = random.random()
            for Index in range(Length):
                self.assertEqual(objTest[Index], Elements[Index])
            self.assertListEqual(objTest.Data, Elements)
            with self.assertRaises(AttributeError):
                objTest.Data = (10, 10, 10) #read-only property
            self.assertListEqual(objTest.Data, Elements)
            del objTest
    
    def test_Iteration(self):
        """
        Checks that a vector does not support iteration protocol.
        
        Test ID: TEST-T-300
        
        Covers requirements: REQ-FUN-301
        """
        with self.assertRaises(TypeError):
            for Item in self.TestObject:
                pass
    
    def test_Contains(self):
        """
        Checks that a vector does not support contains check protocol.
        
        Test ID: TEST-T-300
        
        Covers requirements: REQ-FUN-301
        """
        with self.assertRaises(TypeError):
            if 1 in self.TestObject:
                pass
    
    def test_index_TypeError(self):
        """
        Checks that only integer indexing is allowed.
        
        Test ID: TEST-T-301
        
        Covers requirements: REQ-AWM-307
        """
        for Index in [1.0, int, float, '1']:
            with self.assertRaises(TypeError):
                Temp  = self.TestObject[Index]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[0:]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[:2]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[0:2]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[:]
    
    def test_index_ValueError(self):
        """
        Checks that only integer indexing within the range is allowed.
        
        Test ID: TEST-T-302
        
        Covers requirements: REQ-AWM-308
        """
        Size = self.TestObject.Size
        with self.assertRaises(ValueError):
            Temp = self.TestObject[-Size - 1]
        with self.assertRaises(ValueError):
            Temp = self.TestObject[Size]
        for _ in range(10):
            Shift = random.randint(1, 10)
            with self.assertRaises(ValueError):
                Temp = self.TestObject[-Size - 1 - Shift]
            with self.assertRaises(ValueError):
                Temp = self.TestObject[Size + Shift]
    
    def test_init_TypeError(self):
        """
        Checks that only real number arguments are allowed as arguments of the
        initialization method.
        
        Test ID: TEST-T-303
        
        Covers requirements: REQ-AWM-300
        """
        for Item in self.NotScalar:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Item, 1)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Item, 1, 1)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(1, Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(1, Item, 1)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(1, 1, Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(1, 1, Item, 1)
    
    def test_init_ValueError(self):
        """
        Checks that, at least, 2 real number arguments are required for
        instantiation.
        
        Test ID: TEST-T-304
        
        Covers requirements: REQ-AWM-301
        """
        with self.assertRaises(ValueError):
            Temp = self.TestClass()
        with self.assertRaises(ValueError):
            Temp = self.TestClass(1)
    
    def test_copy(self):
        """
        Testing the shallow copy of a vector.
        """
        New = copy.copy(self.TestObject)
        self.assertIs(New.__class__, self.TestClass)
        self.assertIsNot(New, self.TestObject)
        self.assertEqual(New.Size, self.TestObject.Size)
        self.assertListEqual(New.Data, self.TestObject.Data)
        del New
    
    def test_add_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject + Item
                    self.assertListEqual(self.TestObject.Data, Data)
                    with self.assertRaises(TypeError):
                        Temp = Item + self.TestObject
                    self.assertListEqual(self.TestObject.Data, Data)
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject + Item
                self.assertListEqual(self.TestObject.Data, Data)
                with self.assertRaises(TypeError):
                    Temp = Item + self.TestObject
                self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = self.TestObject + random.random()
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = self.TestObject + random.randint()
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = random.random() + self.TestObject
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = random.randint() + self.TestObject
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_sub_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject - Item
                    self.assertListEqual(self.TestObject.Data, Data)
                    with self.assertRaises(TypeError):
                        Temp = Item - self.TestObject
                    self.assertListEqual(self.TestObject.Data, Data)
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject - Item
                self.assertListEqual(self.TestObject.Data, Data)
                with self.assertRaises(TypeError):
                    Temp = Item - self.TestObject
                self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = self.TestObject - random.random()
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = self.TestObject - random.randint()
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = random.random() - self.TestObject
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = random.randint() - self.TestObject
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_add_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
            Other = self.TestClass(*Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject + Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(ValueError):
                Temp = Other + self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.tearDown()
            self.setUp()
    
    def test_sub_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
            Other = self.TestClass(*Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject - Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(ValueError):
                Temp = Other - self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.tearDown()
            self.setUp()
    
    def test_add(self):
        """
        Checks the addition of two vectors
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310, REQ-FUN-320, REQ-FUN-330
        """
        for _ in range(10):
            Elements = [random.random() for _ in range(self.TestObject.Size)]
            Other = self.TestClass(*Elements)
            TestCheck = [self.TestObject[Index] + Item
                                        for Index, Item in enumerate(Elements)]
            Data = list(self.TestObject.Data)
            Temp = self.TestObject + Other
            self.assertIsInstance(Temp, self.TestClass)
            self.assertIs(Temp.__class__, self.TestClass)
            self.assertListEqual(Temp.Data, TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            self.assertListEqual(Other.Data, Elements)
            del Temp
            Temp = Other + self.TestObject
            self.assertIsInstance(Temp, self.TestClass)
            self.assertIs(Temp.__class__, self.TestClass)
            self.assertListEqual(Temp.Data, TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            self.assertListEqual(Other.Data, Elements)
            del Temp
            del Other
            self.tearDown()
            self.setUp()
    
    def test_sub(self):
        """
        Checks the subtraction of two vectors
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310, REQ-FUN-320, REQ-FUN-330
        """
        for _ in range(10):
            Elements = [random.random() for _ in range(self.TestObject.Size)]
            Other = self.TestClass(*Elements)
            TestCheck = [self.TestObject[Index] - Item
                                        for Index, Item in enumerate(Elements)]
            TestCheck2 = [-Item for Item in TestCheck]
            Data = list(self.TestObject.Data)
            Temp = self.TestObject - Other
            self.assertIsInstance(Temp, self.TestClass)
            self.assertIs(Temp.__class__, self.TestClass)
            self.assertListEqual(Temp.Data, TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            self.assertListEqual(Other.Data, Elements)
            del Temp
            Temp = Other - self.TestObject
            self.assertIsInstance(Temp, self.TestClass)
            self.assertIs(Temp.__class__, self.TestClass)
            self.assertListEqual(Temp.Data, TestCheck2)
            self.assertListEqual(self.TestObject.Data, Data)
            self.assertListEqual(Other.Data, Elements)
            del Temp
            del Other
            self.tearDown()
            self.setUp()
        
    def test_mul_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                    self.assertListEqual(self.TestObject.Data, Data)
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
                    self.assertListEqual(self.TestObject.Data, Data)
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject * Item
                self.assertListEqual(self.TestObject.Data, Data)
                with self.assertRaises(TypeError):
                    Temp = Item * self.TestObject
                self.assertListEqual(self.TestObject.Data, Data)
    
    def test_mul_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
            Other = self.TestClass(*Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject * Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(ValueError):
                Temp = Other * self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.tearDown()
            self.setUp()
    
    def test_mul(self):
        """
        Checks the dot multiplication of two generic vectors and generic
        vector left and right multiplication by a scalar
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Other = random.random()
            Elements = [Item * Other for Item in self.TestObject.Data]
            TestCheck = self.TestObject * Other
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            TestCheck = Other * self.TestObject
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            Other = random.randint(-10, 10)
            Elements = [Item * Other for Item in self.TestObject.Data]
            TestCheck = self.TestObject * Other
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            TestCheck = Other * self.TestObject
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
            Other = self.TestClass(*Elements)
            TestCheck = sum(Item * self.TestObject[Index]
                                        for Index, Item in enumerate(Elements))
            Test = self.TestObject * Other
            self.assertIsInstance(Test, (int, float))
            self.assertAlmostEqual(Test, TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            Test = Other * self.TestObject
            self.assertIsInstance(Test, (int, float))
            self.assertAlmostEqual(Test, TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.tearDown()
            self.setUp()
    
    def test_matmul_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject @ Item
                    self.assertListEqual(self.TestObject.Data, Data)
                    with self.assertRaises(TypeError):
                        Temp = Item @ self.TestObject
                    self.assertListEqual(self.TestObject.Data, Data)
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject @ Item
                self.assertListEqual(self.TestObject.Data, Data)
                with self.assertRaises(TypeError):
                    Temp = Item @ self.TestObject
                self.assertListEqual(self.TestObject.Data, Data)
        for Item in [1, 1.0]:
            with self.assertRaises(TypeError):
                Temp = self.TestObject @ Item
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                Temp = Item @ self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
    
    def test_matmul(self):
        """
        Checks the implementation of the outer generic vectors product.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random() + random.randint(-10, 10)
                    for _ in range(self.TestObject.Size + random.randint(0, 3))]
            Other = self.TestClass(*Elements)
            SizeSelf = len(Data)
            SizeOther = len(Elements)
            Test = self.TestObject @ Other
            self.assertIsInstance(Test, testmodule.Array2D)
            self.assertEqual(Test.Width, SizeOther)
            self.assertEqual(Test.Height, SizeSelf)
            for Row in range(SizeSelf):
                for Col in range(SizeOther):
                    self.assertAlmostEqual(Test[Col, Row],
                                                    Elements[Col] * Data[Row])
            self.assertListEqual(self.TestObject.Data, Data)
            del Test
            Test = Other @ self.TestObject
            self.assertIsInstance(Test, testmodule.Array2D)
            self.assertEqual(Test.Width, SizeSelf)
            self.assertEqual(Test.Height, SizeOther)
            for Row in range(SizeOther):
                for Col in range(SizeSelf):
                    self.assertAlmostEqual(Test[Col, Row],
                                                    Elements[Row] * Data[Col])
            self.assertListEqual(self.TestObject.Data, Data)
            del Test
            del Other
            self.tearDown()
            self.setUp()
    
    def test_div_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotScalar:
            with self.assertRaises(TypeError):
                Temp = self.TestObject / Item
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                Temp = Item / self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = 1 / self.TestObject
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Temp = 1.0 / self.TestObject
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_div_ValueError(self):
        """
        Checks treatment of division by zero
        
        Test ID: TEST-T-308
        
        Covers requirements: REQ-AWM-304
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            with self.assertRaises(ValueError):
                Temp = self.TestObject / 0
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(ValueError):
                Temp = self.TestObject / 0.0
            self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_div(self):
        """
        Checks the implementation of the division of a vector by a scalar.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Other = random.random()
            if not Other:
                Other = 0.1
            Test = self.TestObject / Other
            self.assertIsInstance(Test, self.TestClass)
            self.assertIs(Test.__class__, self.TestClass)
            self.assertEqual(Test.Size, self.TestObject.Size)
            for Index, Item in enumerate(Data):
                self.assertAlmostEqual(Test[Index], Item / Other)
            del Test
            Other += random.randint(-10, 10)
            Test = self.TestObject / Other
            self.assertIsInstance(Test, self.TestClass)
            self.assertIs(Test.__class__, self.TestClass)
            self.assertEqual(Test.Size, self.TestObject.Size)
            for Index, Item in enumerate(Data):
                self.assertAlmostEqual(Test[Index], Item / Other)
            del Test
            self.tearDown()
            self.setUp()
    
    def test_pos(self):
        """
        Checks the implementation of the unitary plus operation.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            New = +self.TestObject
            self.assertIs(New.__class__, self.TestClass)
            self.assertIsNot(New, self.TestObject)
            self.assertEqual(New.Size, self.TestObject.Size)
            self.assertListEqual(New.Data, self.TestObject.Data)
            self.assertListEqual(self.TestObject.Data, Data)
            del New
            self.tearDown()
            self.setUp()
    
    def test_neg(self):
        """
        Checks the implementation of the unitary plus operation.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [-Item for Item in self.TestObject.Data]
            New = -self.TestObject
            self.assertIs(New.__class__, self.TestClass)
            self.assertIsNot(New, self.TestObject)
            self.assertEqual(New.Size, self.TestObject.Size)
            self.assertListEqual(New.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del New
            self.tearDown()
            self.setUp()
    
    def test_augmentedAssignment(self):
        """
        Checks that the in-place modification via augmented assignment is not
        supported. This is an additional test.
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
            Other = self.TestClass(*Elements)
            with self.assertRaises(TypeError):
                self.TestObject += Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject -= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject *= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject @= Other
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            Other = random.randint(1, 10)
            with self.assertRaises(TypeError):
                self.TestObject *= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject /= Other
            self.assertListEqual(self.TestObject.Data, Data)
            Other += random.random()
            with self.assertRaises(TypeError):
                self.TestObject *= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject /= Other
            self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_normalize(self):
        """
        Checks generation of a normalized vector from an existing one.
        
        Test ID: TEST-T-309
        
        Covers requirements: REQ-FUN-303
        """
        for _ in range(10):
            Length = sqrt(sum(Item*Item for Item in self.TestObject.Data))
            while not Length:
                self.tearDown()
                self.setUp()
                Length = sqrt(sum(Item*Item for Item in self.TestObject.Data))
            Data = list(self.TestObject.Data)
            Test = self.TestObject.normalize()
            self.assertListEqual(self.TestObject.Data, Data)
            self.assertIsInstance(Test, self.TestClass)
            self.assertIs(Test.__class__, self.TestClass)
            self.assertEqual(Test.Size, self.TestObject.Size)
            for Index, Element in enumerate(self.TestObject.Data):
                self.assertAlmostEqual(Test[Index], Element / Length)
            del Test
            Size = random.randint(2, 10)
            Elements = [0 for _ in range(Size)]
            Test = self.TestClass(*Elements)
            with self.assertRaises(ValueError):
                Temp = Test.normalize()
            del Test
            self.tearDown()
            self.setUp()
    
    def test_generateOrtogonal(self):
        """
        Checks generation of a unity orthogonal vectors set.
        
        Test ID: TEST-T-309
        
        Covers requirements: REQ-FUN-303
        """
        for _ in range(10):
            Size = random.randint(2, 10)
            for Index in range(Size):
                Test = self.TestClass.generateOrtogonal(Size, Index)
                self.assertIsInstance(Test, self.TestClass)
                self.assertIs(Test.__class__, self.TestClass)
                self.assertEqual(Test.Size, Size)
                for Second in range(Size):
                    if Second == Index:
                        self.assertEqual(Test[Second], 1)
                    else:
                        self.assertEqual(Test[Second], 0)
                del Test
            self.tearDown()
            self.setUp()
    
    def test_generateOrtogonal_TypeError(self):
        """
        Checks generation of a unity orthogonal vectors set - input data types.
        
        Test ID: TEST-T-309
        
        Covers requirements: REQ-FUN-303
        """
        Data = list(self.TestObject.Data)
        Size = random.randint(2, 10)
        Index = random.randint(0, Size - 1)
        for Item in self.NotScalar:
            with self.assertRaises(TypeError):
                self.TestClass.generateOrtogonal(Item, Index)
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestClass.generateOrtogonal(Size, Item)
            self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            self.TestClass.generateOrtogonal(3.0, Index)
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            self.TestClass.generateOrtogonal(Size, 1.0)
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_generateOrtogonal_ValueError(self):
        """
        Checks generation of a unity orthogonal vectors set - input data values.
        
        Test ID: TEST-T-309
        
        Covers requirements: REQ-FUN-303
        """
        Data = list(self.TestObject.Data)
        with self.assertRaises(ValueError):
            self.TestClass.generateOrtogonal(0, 1)
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(ValueError):
            self.TestClass.generateOrtogonal(1, 1)
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(ValueError):
            self.TestClass.generateOrtogonal(random.randint(-10, -1), 1)
        self.assertListEqual(self.TestObject.Data, Data)
        Size = random.randint(2, 10)
        with self.assertRaises(ValueError):
            self.TestClass.generateOrtogonal(Size, random.randint(-10, -1))
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(ValueError):
            self.TestClass.generateOrtogonal(Size, Size)
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(ValueError):
            self.TestClass.generateOrtogonal(Size, Size + random.randint(1, 10))
        self.assertListEqual(self.TestObject.Data, Data)

class Test_Column(Test_Vector):
    """
    Unit tests for the column vector class.
    
    Test IDs: TEST-T-300, TEST-T-301, TEST-T-302, TEST-T-303, TEST-T-304,
        TEST-T-305, TEST-T-306, TEST-T-307, TEST-T-308, TEST-T-309
    
    Covers requirements: REQ-FUN-301, REQ-FUN-302, REQ-FUN-303, REQ-FUN-320,
        REQ-AWM-300, REQ-AWM-301, REQ-AWM-302, REQ-AWM-303, REQ-AWM-304,
        REQ-AWM-305, REQ-AWM-306, REQ-AWM-307, REQ-AWM-308

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = testmodule.Column
    
    def test_mul_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotScalar:
            if isinstance(Item, testmodule.Vector):
                if not (Item.__class__ is testmodule.Row):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                    self.assertListEqual(self.TestObject.Data, Data)
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
                    self.assertListEqual(self.TestObject.Data, Data)
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject * Item
                self.assertListEqual(self.TestObject.Data, Data)
                if not isinstance(Item, testmodule.Matrix):
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
                    self.assertListEqual(self.TestObject.Data, Data)
    
    def test_mul_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
            Other = testmodule.Row(*Elements)
            with self.assertRaises(ValueError):
                Temp = Other * self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.tearDown()
            self.setUp()
    
    def test_mul(self):
        """
        Checks the column vector left and right multiplication by a scalar
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-320
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Other = random.random()
            Elements = [Item * Other for Item in self.TestObject.Data]
            TestCheck = self.TestObject * Other
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            TestCheck = Other * self.TestObject
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            Other = random.randint(-10, 10)
            Elements = [Item * Other for Item in self.TestObject.Data]
            TestCheck = self.TestObject * Other
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            TestCheck = Other * self.TestObject
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            self.tearDown()
            self.setUp()
    
    def test_matmul(self):
        """
        Checks that the outer product is not defined for the column vectors.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
            Other = self.TestClass(*Elements)
            with self.assertRaises(TypeError):
                Test = self.TestObject @ Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                Test = Other @ self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.tearDown()
            self.setUp()
    
    def test_transpose(self):
        """
        Checks the transposition method.
        
        Test ID: TEST-T-309
        
        Covers requirements: REQ-FUN-303
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Test = self.TestObject.transpose()
            self.assertIsInstance(Test, testmodule.Row)
            self.assertIs(Test.__class__, testmodule.Row)
            self.assertListEqual(Test.Data, Data)
            self.assertListEqual(self.TestObject.Data, Data)
            del Test
            self.tearDown()
            self.setUp()

class Test_Row(Test_Vector):
    """
    Unit tests for the row vector class.
    
    Test IDs: TEST-T-300, TEST-T-301, TEST-T-302, TEST-T-303, TEST-T-304,
        TEST-T-305, TEST-T-306, TEST-T-307, TEST-T-308, TEST-T-309
    
    Covers requirements: REQ-FUN-301, REQ-FUN-302, REQ-FUN-303, REQ-FUN-330,
        REQ-AWM-300, REQ-AWM-301, REQ-AWM-302, REQ-AWM-303, REQ-AWM-304,
        REQ-AWM-305, REQ-AWM-306, REQ-AWM-307, REQ-AWM-308

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = testmodule.Row
    
    def test_mul_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotScalar:
            if isinstance(Item, testmodule.Vector):
                if not (Item.__class__ is testmodule.Column):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                    self.assertListEqual(self.TestObject.Data, Data)
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
                    self.assertListEqual(self.TestObject.Data, Data)
            else:
                if not isinstance(Item, testmodule.Matrix):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                    self.assertListEqual(self.TestObject.Data, Data)
                with self.assertRaises(TypeError):
                    Temp = Item * self.TestObject
                self.assertListEqual(self.TestObject.Data, Data)
    
    def test_mul_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
            Other = testmodule.Column(*Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject * Other
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.tearDown()
            self.setUp()
    
    def test_mul(self):
        """
        Checks the row vector left and right multiplication by a scalar, and
        row x column and column x row vector multiplications.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-320, REQ-FUN-330
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Other = random.random()
            Elements = [Item * Other for Item in self.TestObject.Data]
            TestCheck = self.TestObject * Other
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            TestCheck = Other * self.TestObject
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            Other = random.randint(-10, 10)
            Elements = [Item * Other for Item in self.TestObject.Data]
            TestCheck = self.TestObject * Other
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            TestCheck = Other * self.TestObject
            self.assertIsInstance(TestCheck, self.TestClass)
            self.assertIs(TestCheck.__class__, self.TestClass)
            self.assertListEqual(TestCheck.Data, Elements)
            self.assertListEqual(self.TestObject.Data, Data)
            del TestCheck
            Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
            Other = testmodule.Column(*Elements)
            TestCheck = sum(Item * self.TestObject[Index]
                                        for Index, Item in enumerate(Elements))
            Test = self.TestObject * Other
            self.assertIsInstance(Test, (int, float))
            self.assertAlmostEqual(Test, TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            NewSize = self.TestObject.Size + random.randint(0, 3)
            Elements = [random.random() + random.randint(-10, 10)
                                                    for _ in range(NewSize)]
            Other = testmodule.Column(*Elements)
            Test = Other * self.TestObject
            self.assertIsInstance(Test, testmodule.Matrix)
            self.assertEqual(Test.Width, self.TestObject.Size)
            self.assertEqual(Test.Height, Other.Size)
            for Row in range(Other.Size):
                for Col in range(self.TestObject.Size):
                    TestCheck = Other[Row] * self.TestObject[Col]
                    self.assertAlmostEqual(Test[Col, Row], TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            del Test
            del Other
            NewSize = self.TestObject.Size - random.randint(0, 3)
            NewSize = max(2, NewSize)
            Elements = [random.random() + random.randint(-10, 10)
                                                    for _ in range(NewSize)]
            Other = testmodule.Column(*Elements)
            Test = Other * self.TestObject
            self.assertIsInstance(Test, testmodule.Matrix)
            self.assertEqual(Test.Width, self.TestObject.Size)
            self.assertEqual(Test.Height, Other.Size)
            for Row in range(Other.Size):
                for Col in range(self.TestObject.Size):
                    TestCheck = Other[Row] * self.TestObject[Col]
                    self.assertAlmostEqual(Test[Col, Row], TestCheck)
            self.assertListEqual(self.TestObject.Data, Data)
            del Test
            del Other
            self.tearDown()
            self.setUp()
    
    def test_matmul(self):
        """
        Checks that the outer product is not defined for the row vectors.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
            Other = self.TestClass(*Elements)
            with self.assertRaises(TypeError):
                Test = self.TestObject @ Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                Test = Other @ self.TestObject
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
        
    def test_transpose(self):
        """
        Checks the transposition method.
        
        Test ID: TEST-T-309
        
        Covers requirements: REQ-FUN-303
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Test = self.TestObject.transpose()
            self.assertIsInstance(Test, testmodule.Column)
            self.assertIs(Test.__class__, testmodule.Column)
            self.assertListEqual(Test.Data, Data)
            self.assertListEqual(self.TestObject.Data, Data)
            del Test
            self.tearDown()
            self.setUp()

class Test_Array2D(unittest.TestCase):
    """
    Set of unit tests for the class Array2D. These tests are not part of the
    test plan, however, this class is the prototype for the both generic and
    square matrices, which already implements part of their functionality.
    
    Implements tests: TEST-T-30A, TEST-T-30D and TEST-T-30F
    
    Covers requirements: REQ-FUN-304, REQ-FUN-305, REQ-AWM-300, REQ-AWM-301,
    REQ-AWM-307 and REQ-AWM-308
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.Array2D
        cls.NotBool = [1, 1.0, [1, 1], (1, 1), {1, 1}, "1", {1 : 1}, int,
                        float, bool, testmodule.Vector(1, 1),
                        testmodule.Column(1, 1), testmodule.Row(1, 1),
                        testmodule.Array2D([[1, 1], [1, 1]])]
        cls.NotInt = [1.0, [1, 1], (1, 1), {1, 1}, "1", {1 : 1}, int, float,
                        bool, testmodule.Vector(1, 1), testmodule.Column(1, 1),
                        testmodule.Row(1, 1),
                        testmodule.Array2D([[1, 1], [1, 1]])]
        cls.NotScalar = [[1, 1], (1, 1), {1, 1}, "1", {1 : 1}, int, float,
                        bool, testmodule.Vector(1, 1), testmodule.Column(1, 1),
                        testmodule.Row(1, 1),
                        testmodule.Array2D([[1, 1], [1, 1]])]
        cls.NotSequence = [1, 1.0, "1", {1 : 1}, int, float, bool,
                            testmodule.Vector(1, 1), testmodule.Column(1, 1),
                            testmodule.Row(1, 1),
                            testmodule.Array2D([[1, 1], [1, 1]])]
    
    def setUp(self) -> None:
        """
        Preparation for each individual unit test.
        """
        Width = random.randint(2, 5)
        Height = random.randint(2, 5)
        Elements = list()
        for _ in range(Height):
            Row = list()
            for _ in range(Width):
                Value = random.randint(-5, 5)
                if random.random() > 0.5:
                    Value += random.random()
                Row.append(Value)
            Elements.append(Row)
        self.TestObject = self.TestClass(Elements)
    
    def tearDown(self) -> None:
        """
        Cleaning up after each individual unit test
        """
        del self.TestObject
        self.TestObject = None
    
    def test_init(self):
        """
        Checks the different instantiation options and per element access.
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304, REQ-FUN-305
        """
        Width = random.randint(2, 5)
        Height = random.randint(2, 5)
        Elements = list()
        for _ in range(Width*Height + 1):
            Value = random.randint(-5, 5)
            if random.random() > 0.5:
                Value += random.random()
            Elements.append(Value)
        ElementsRows = [[Elements[Width*Row + Column]
                        for Column in range(Width)] for Row in range(Height)]
        ElementsCols = [[Elements[Width*Row + Column]
                        for Row in range(Height)] for Column in range(Width)]
        Test = self.TestClass(Elements, Width = Width)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Width = Width, isColumnsFirst = False)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Width = Height, isColumnsFirst = True)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Height)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Width)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsCols)
        for Row in range(Width):
            for Col in range(Height):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsCols[Row][Col])
        del Test
        Test = self.TestClass(Elements, Height = Height)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Height = Height, isColumnsFirst = False)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Height = Width, isColumnsFirst = True)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Height)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Width)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsCols)
        for Row in range(Width):
            for Col in range(Height):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsCols[Row][Col])
        del Test
        Test = self.TestClass(Elements, Width = Width, Height = Height)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Width = Width, Height = Height,
                                                        isColumnsFirst = False)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Width = Height, Height = Width,
                                                        isColumnsFirst = True)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Height)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Width)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsCols)
        for Row in range(Width):
            for Col in range(Height):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsCols[Row][Col])
        del Test
        MaxSize = max(Width, Height)
        NewSize = random.randint(MaxSize + 1, 2 * MaxSize)
        Test = self.TestClass(ElementsRows)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, isColumnsFirst = False)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsCols, isColumnsFirst = True)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, Width = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, isColumnsFirst = False,
                                                                Width = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsCols, isColumnsFirst = True,
                                                                Width = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, Height = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, isColumnsFirst = False,
                                                            Height = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsCols, isColumnsFirst = True,
                                                            Height = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, Height = NewSize, Width = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, isColumnsFirst = False,
                                            Width = NewSize, Height = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsCols, isColumnsFirst = True,
                                            Width = NewSize, Height = NewSize)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Width)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Height)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Height):
            for Col in range(Width):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
    
    def test_init_TypeError(self):
        """
        Checks the treatment of the improper data types of the arguments of the
        initialization method.
        
        Test ID: TEST-T-30D
        
        Covers requirements: REQ-AWM-300
        """
        Width = self.TestObject.Width
        Height = self.TestObject.Height
        Data = list(self.TestObject.Data)
        DataFlat = list()
        for Item in Data:
            DataFlat.extend(Item)
        # column / row order argument
        for Item in self.NotBool:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Width = Width,
                                                        isColumnsFirst = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Width = Width, Height = Height,
                                                        isColumnsFirst = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Height = Height,
                                                        isColumnsFirst = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Data, isColumnsFirst = Item)
        # width argument
        for Item in self.NotInt:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Width = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Width = Item, Height = Height)
            #that should be ignored as the argument
            Temp = self.TestClass(Data, Width = Item)
            del Temp
        # height argument
        for Item in self.NotInt:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Height = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Height = Item, Width = Width)
            #that should be ignored as the argument
            Temp = self.TestClass(Data, Height = Item)
            del Temp
        # mandatory data argument
        for Item in self.NotSequence:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Item, Width = Width, Height = Height)
        for Item in self.NotScalar:
            Elements = [1 for _ in range(random.randint(4, 10))]
            Index = random.randint(0, len(Elements) - 1)
            Elements[Index] = Item
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Elements, Width = 2, Height = 2)
            Elements = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
            IndexX = random.randint(0, 2)
            IndexY = random.randint(0, 2)
            Elements[IndexX][IndexY] = Item
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Elements)
    
    def test_init_ValueError(self):
        """
        Checks the treatment of the improper data types of the arguments of the
        initialization method.
        
        Test ID: TEST-T-30D
        
        Covers requirements: REQ-AWM-301
        """
        Width = self.TestObject.Width
        Height = self.TestObject.Height
        Data = list()
        for Item in self.TestObject.Data:
            Data.extend(Item)
        with self.assertRaises(ValueError):
            Temp = self.TestClass(Data) #no width and height!
        for Value in [0, 1, Width + 1, random.randint(-10, -1)]:
            with self.assertRaises(ValueError):
                Temp = self.TestClass(Data, Width = Value, Height = Height)
        for Value in [0, 1, Height + 1, random.randint(-10, -1)]:
            with self.assertRaises(ValueError):
                Temp = self.TestClass(Data, Width = Width, Height = Value)
        for Value in [0, 1, max(Width, Height) + 1, random.randint(-10, -1)]:
            with self.assertRaises(ValueError):
                Temp = self.TestClass(Data, Width = Value, Height = Value)
        with self.assertRaises(ValueError):
            Temp = self.TestClass(Data, Width = Width + 1, Height = Height + 1)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([1, 1, 1], Width = 2)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([1, 1, 1, 1, 1], Width = 3)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([1, 1, 1], Height = 2)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([1, 1, 1, 1, 1], Height = 3)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1], [1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1], [1, 1 ,1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1, 1, 1], [1, 1 ,1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1, 1], [1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]])
    
    def test_index_TypeError(self):
        """
        Checks treatment of the improper data type of the index access.
        
        Test ID: TEST-T-30F
        
        Covers requirements: REQ-AWM-307
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotInt:
            with self.assertRaises(TypeError):
                Temp = self.TestObject[1, Item]
            with self.assertRaises(TypeError):
                Temp = self.TestObject[Item, 1]
            with self.assertRaises(TypeError):
                Temp = self.TestObject[Item, Item]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[0, 0 : 1]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[0 : 1, 0]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[0 : 1, 0 : 1]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[1]
        with self.assertRaises(TypeError):
            Temp = self.TestObject[0:1]
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_index_ValueError(self):
        """
        Checks treatment of the improper values of the index access.
        
        Test ID: TEST-T-30F
        
        Covers requirements: REQ-AWM-308
        """
        Width = self.TestObject.Width
        Height = self.TestObject.Height
        Data = list(self.TestObject.Data)
        with self.assertRaises(ValueError):
            Temp = self.TestObject[1, 1, 1]
        for Col in [-Width - random.randint(2, 10), -Width -1, Width,
                                                Width + random.randint(1, 10)]:
            with self.assertRaises(ValueError):
                Temp = self.TestObject[Col, 0]
        for Row in [-Height - random.randint(2, 10), -Height -1, Height,
                                                Height + random.randint(1, 10)]:
            with self.assertRaises(ValueError):
                Temp = self.TestObject[0, Row]
        #those should be ok - no exceptions
        for Col in range(-Width, Width):
            for Row in range(-Height, Height):
                Temp = self.TestObject[Col, Row]
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_NotSequence(self):
        """
        Checks that 'IS A' check against sequence type returns False.
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304
        """
        self.assertNotIsInstance(self.TestObject, Sequence)
    
    def test_NotIterator(self):
        """
        Checks that 'for x in y' construct cannot be used with arrays and
        matrices, i.e. they are not iterable.
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304
        """
        with self.assertRaises(TypeError):
            for Item in self.TestObject:
                pass
    
    def test_NotContains(self):
        """
        Checks that 'if x in y' construct cannot be used with arrays and
        matrices, i.e. the 'contains' check is not supported.
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304
        """
        with self.assertRaises(TypeError):
            if 1 in self.TestObject:
                pass
    
    def test_Immutable(self):
        """
        Checks that arrays and matrices are not mutable, and their property
        attributes are read-only. Also, index access is read-only.
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304
        """
        Data = list(self.TestObject.Data)
        with self.assertRaises(AttributeError):
            self.TestObject.Width = 5
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(AttributeError):
            self.TestObject.Height = 5
        self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(AttributeError):
            self.TestObject.Data = [[1, 1], [1, 1]]
        self.assertListEqual(self.TestObject.Data, Data)
        Width = self.TestObject.Width
        Height = self.TestObject.Height
        for Col in range(Width):
            for Row in range(Height):
                with self.assertRaises(TypeError):
                    self.TestObject[Col, Row] = 5
                self.assertListEqual(self.TestObject.Data, Data)
    
class Test_Matrix(Test_Array2D):
    """
    Set of unit tests for the class Matrix.
    
    Implements tests: TEST-T-30A, TEST-T-30B, TEST-T-30D, TEST-T-30E
    and TEST-T-30F
    
    Covers requirements: REQ-FUN-304, REQ-FUN-305, REQ-FUN-306, REQ-FUN-320,
    REQ-FUN-330, REQ-AWM-300, REQ-AWM-301, REQ-AWM-302, REQ-AWM-303,
    REQ-AWM-304, REQ-AWM-307 and REQ-AWM-308
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.NotMatrix = [1, 2.0, True, int, float, bool, [1], (1.0, 1), {1:1},
                            {1, 2}, list, tuple, dict, set, testmodule.Matrix,
                            testmodule.SquareMatrix, testmodule.Vector,
                            testmodule.Column, testmodule.Row,
                            testmodule.Vector(1, 2, 3), testmodule.Row(1, 2, 3),
                            testmodule.Column(1, 2, 3)]
        cls.BadTypeRight = [int, float, bool, [1], (1.0, 1), {1:1},
                            {1, 2}, list, tuple, dict, set, testmodule.Matrix,
                            testmodule.SquareMatrix, testmodule.Vector,
                            testmodule.Column, testmodule.Row,
                            testmodule.Vector(1, 2, 3), testmodule.Row(1, 2, 3),
                            ]
        cls.BadTypeLeft = [int, float, bool, [1], (1.0, 1), {1:1},
                            {1, 2}, list, tuple, dict, set, testmodule.Matrix,
                            testmodule.SquareMatrix, testmodule.Vector,
                            testmodule.Column, testmodule.Row,
                            testmodule.Vector(1, 2, 3),
                            testmodule.Column(1, 2, 3)]
        cls.NotScalar = [int, float, bool, [1, 2], (1.0, 1), {1:1},
                            {1, 2}, list, tuple, dict, set, testmodule.Matrix,
                            testmodule.SquareMatrix, testmodule.Vector,
                            testmodule.Column, testmodule.Row,
                            testmodule.Vector(1, 2, 3), testmodule.Row(1, 2, 3),
                            testmodule.Column(1, 2, 3),
                            testmodule.Matrix(((1, 1), (2, 3))),
                            testmodule.SquareMatrix(((1, 1), (2, 3)))]
        cls.TestClass = testmodule.Matrix
    
    def test_getRow(self):
        """
        Checks the access to a single row
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304
        """
        for _ in range(10):
            Height = self.TestObject.Height
            Data = list(self.TestObject.Data)
            for Index in range(-Height, Height):
                Test = self.TestObject.getRow(Index)
                self.assertIsInstance(Test, testmodule.Row)
                self.assertListEqual(Test.Data, Data[Index])
                del Test
            self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_getColumn(self):
        """
        Checks the access to a single column
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304
        """
        for _ in range(10):
            Width = self.TestObject.Width
            Data = list(self.TestObject.Data)
            for Index in range(-Width, Width):
                TestCheck = [Row[Index] for Row in Data]
                Test = self.TestObject.getColumn(Index)
                self.assertIsInstance(Test, testmodule.Column)
                self.assertListEqual(Test.Data, TestCheck)
                del Test
            self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_getRow_TypeError(self):
        """
        Checks treatment of the improper indexing (per row) access data types.
        
        Test ID: TEST-T-30F
        
        Covers requirements: REQ-AWM-307
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotInt:
            with self.assertRaises(TypeError):
                Row = self.TestObject.getRow(Item)
            self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Row = self.TestObject.getRow(slice(0,1))
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_getColumn_TypeError(self):
        """
        Checks treatment of the improper indexing (per column) access data types
        
        Test ID: TEST-T-30F
        
        Covers requirements: REQ-AWM-307
        """
        Data = list(self.TestObject.Data)
        for Item in self.NotInt:
            with self.assertRaises(TypeError):
                Col = self.TestObject.getColumn(Item)
            self.assertListEqual(self.TestObject.Data, Data)
        with self.assertRaises(TypeError):
            Col = self.TestObject.getColumn(slice(0,1))
        self.assertListEqual(self.TestObject.Data, Data)
    
    def test_getRow_ValueError(self):
        """
        Checks treatment of the improper indexing (per row) access data types.
        
        Test ID: TEST-T-30F
        
        Covers requirements: REQ-AWM-308
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Height = self.TestObject.Height
            for Row in [-Height - random.randint(2, 10), -Height -1, Height,
                                                Height + random.randint(1, 10)]:
                with self.assertRaises(ValueError):
                    Temp = self.TestObject.getRow(Row)
                self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_getColumn_ValueError(self):
        """
        Checks treatment of the improper indexing (per column) access data types
        
        Test ID: TEST-T-30F
        
        Covers requirements: REQ-AWM-308
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Width = self.TestObject.Width
            for Col in [-Width - random.randint(2, 10), -Width -1, Width,
                                                Width + random.randint(1, 10)]:
                with self.assertRaises(ValueError):
                    Temp = self.TestObject.getColumn(Col)
                self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_augmentedAssignment(self):
        """
        Checks that the in-place modification via augmented assignment is not
        supported. This is an additional test.
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            Elements = [[random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Width)]
                                        for _ in range(self.TestObject.Height)]
            Other = self.TestClass(Elements)
            with self.assertRaises(TypeError):
                self.TestObject += Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject -= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject *= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject @= Other
            self.assertListEqual(self.TestObject.Data, Data)
            del Other
            Other = random.randint(1, 10)
            with self.assertRaises(TypeError):
                self.TestObject *= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject /= Other
            self.assertListEqual(self.TestObject.Data, Data)
            Other += random.random()
            with self.assertRaises(TypeError):
                self.TestObject *= Other
            self.assertListEqual(self.TestObject.Data, Data)
            with self.assertRaises(TypeError):
                self.TestObject /= Other
            self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_add(self):
        """
        Checks the implementation of the matrix summation.

        Test ID: TEST-T-30B

        Covers requirements: REQ-FUN-306
        """
        for _ in range (10):
            Width = self.TestObject.Width
            Height = self.TestObject.Height
            Data = list(self.TestObject.Data)
            Elements = list()
            for _ in range(Height):
                Row = list()
                for _ in range(Width):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = self.TestClass(Elements)
            objTest = self.TestObject + Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] +
                                                                Other[Col, Row])
            del objTest
            objTest = Other + self.TestObject
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] +
                                                                Other[Col, Row])
            del objTest
            del Other
            self.tearDown()
            self.setUp()
    
    def test_sub(self):
        """
        Checks the implementation of the matrix subtraction.

        Test ID: TEST-T-30B

        Covers requirements: REQ-FUN-306
        """
        for _ in range (10):
            Width = self.TestObject.Width
            Height = self.TestObject.Height
            Data = list(self.TestObject.Data)
            Elements = list()
            for _ in range(Height):
                Row = list()
                for _ in range(Width):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = self.TestClass(Elements)
            objTest = self.TestObject - Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] -
                                                                Other[Col, Row])
            del objTest
            objTest = Other - self.TestObject
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, - self.TestObject[Col, Row] +
                                                                Other[Col, Row])
            del objTest
            del Other
            self.tearDown()
            self.setUp()
    
    def test_add_ValueError(self):
        """
        Checks the implementation of the matrix summation - unequal sizes.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Width = self.TestObject.Width
            Height = self.TestObject.Height
            NewWidth = Width + random.randint(1, 5)
            NewHeight = Height + random.randint(1, 5)
            Elements = list()
            for _ in range(Height):
                Row = list()
                for _ in range(NewWidth):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject + Other
            with self.assertRaises(ValueError):
                Temp = Other + self.TestObject
            del Other
            Elements = list()
            for _ in range(NewHeight):
                Row = list()
                for _ in range(Width):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject + Other
            with self.assertRaises(ValueError):
                Temp = Other + self.TestObject
            del Other
            Size = max(Width, Height) + random.randint(1, 5)
            Elements = list()
            for _ in range(Size):
                Row = list()
                for _ in range(Size):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.SquareMatrix(Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject + Other
            with self.assertRaises(ValueError):
                Temp = Other + self.TestObject
            del Other
            self.tearDown()
            self.setUp()
    
    def test_sub_ValueError(self):
        """
        Checks the implementation of the matrix subtraction - unequal sizes.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Width = self.TestObject.Width
            Height = self.TestObject.Height
            NewWidth = Width + random.randint(1, 5)
            NewHeight = Height + random.randint(1, 5)
            Elements = list()
            for _ in range(Height):
                Row = list()
                for _ in range(NewWidth):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            self.assertNotEqual(Other.Width, self.TestObject.Width)
            self.assertEqual(Other.Height, self.TestObject.Height)
            with self.assertRaises(ValueError):
                Temp = self.TestObject - Other
            with self.assertRaises(ValueError):
                Temp = Other - self.TestObject
            del Other
            Elements = list()
            for _ in range(NewHeight):
                Row = list()
                for _ in range(Width):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject - Other
            with self.assertRaises(ValueError):
                Temp = Other - self.TestObject
            del Other
            Size = max(Width, Height) + random.randint(1, 5)
            Elements = list()
            for _ in range(Size):
                Row = list()
                for _ in range(Size):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.SquareMatrix(Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject - Other
            with self.assertRaises(ValueError):
                Temp = Other - self.TestObject
            del Other
            self.tearDown()
            self.setUp()
    
    def test_add_TypeError(self):
        """
        Checks the implementation of the matrix summation - improper types.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-302
        """
        for _ in range(10):
            for Item in self.NotMatrix:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject + Item
                with self.assertRaises(TypeError):
                    Temp = Item + self.TestObject
            self.tearDown()
            self.setUp()
    
    def test_sub_TypeError(self):
        """
        Checks the implementation of the matrix subtraction - improper types.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-302
        """
        for _ in range(10):
            for Item in self.NotMatrix:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject + Item
                with self.assertRaises(TypeError):
                    Temp = Item + self.TestObject
            self.tearDown()
            self.setUp()
    
    def test_mul(self):
        """
        Checks the implementation of the matrix multiplication, including by
        scalar, column, row and another matrix.

        Test ID: TEST-T-30B

        Covers requirements: REQ-FUN-306
        """
        for _ in range (10):
            Width = self.TestObject.Width
            Height = self.TestObject.Height
            Data = list(self.TestObject.Data)
            #by scalar (left and right)
            Scalar = random.randint(-10, 10)
            objTest = self.TestObject * Scalar
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] * Scalar)
            del objTest
            objTest = Scalar * self.TestObject
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] * Scalar)
            del objTest
            Scalar += random.random()
            objTest = self.TestObject * Scalar
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] * Scalar)
            del objTest
            objTest = Scalar * self.TestObject
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] * Scalar)
            del objTest
            #by row vector (left)
            Elements = [random.random() + random.randint(-10, 10)
                                                        for _ in range(Height)]
            Other = testmodule.Row(*Elements)
            objTest = Other * self.TestObject
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertListEqual(list(Other.Data), Elements)
            self.assertIsInstance(objTest, testmodule.Row)
            self.assertEqual(objTest.Size, Width)
            for Index, Item in enumerate(objTest.Data):
                self.assertIsInstance(Item, (int, float))
                self.assertAlmostEqual(Item,
                                    Other * self.TestObject.getColumn(Index))
            del Other
            del objTest
            #by column vector (right)
            Elements = [random.random() + random.randint(-10, 10)
                                                        for _ in range(Width)]
            Other = testmodule.Column(*Elements)
            objTest = self.TestObject * Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertListEqual(list(Other.Data), Elements)
            self.assertIsInstance(objTest, testmodule.Column)
            self.assertEqual(objTest.Size, Height)
            for Index, Item in enumerate(objTest.Data):
                self.assertIsInstance(Item, (int, float))
                self.assertAlmostEqual(Item,
                                    self.TestObject.getRow(Index) * Other)
            del Other
            del objTest
            #by generic matrix (right)
            NewWidth = Height + random.randint(1, 3)
            Elements = list()
            for _ in range(Width):
                Row = list()
                for _ in range(NewWidth):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            objTest = self.TestObject * Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertListEqual(list(Other.Data), Elements)
            self.assertIsInstance(objTest, testmodule.Matrix)
            self.assertEqual(objTest.Width, NewWidth)
            self.assertEqual(objTest.Height, Height)
            if Height == NewWidth:
                self.assertIsInstance(objTest, testmodule.SquareMatrix)
            else:
                self.assertNotIsInstance(objTest, testmodule.SquareMatrix)
            for Row in range(Height):
                for Col in range(NewWidth):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject.getRow(Row) *
                                                        Other.getColumn(Col))
            del Other
            del objTest
            NewWidth = max(2, Height - random.randint(1, 3))
            Elements = list()
            for _ in range(Width):
                Row = list()
                for _ in range(NewWidth):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            objTest = self.TestObject * Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertListEqual(list(Other.Data), Elements)
            self.assertIsInstance(objTest, testmodule.Matrix)
            self.assertEqual(objTest.Width, NewWidth)
            self.assertEqual(objTest.Height, Height)
            if Height == NewWidth:
                self.assertIsInstance(objTest, testmodule.SquareMatrix)
            else:
                self.assertNotIsInstance(objTest, testmodule.SquareMatrix)
            for Row in range(Height):
                for Col in range(NewWidth):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject.getRow(Row) *
                                                        Other.getColumn(Col))
            del Other
            del objTest
            #+ expected square matrix!
            Elements = list()
            for _ in range(Width):
                Row = list()
                for _ in range(Height):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            objTest = self.TestObject * Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertListEqual(list(Other.Data), Elements)
            self.assertIsInstance(objTest, testmodule.SquareMatrix)
            self.assertEqual(objTest.Size, Height)
            for Row in range(Height):
                for Col in range(Height):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject.getRow(Row) *
                                                        Other.getColumn(Col))
            del Other
            del objTest
            #by square matrix (right)
            Elements = list()
            for _ in range(Width):
                Row = list()
                for _ in range(Width):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.SquareMatrix(Elements)
            objTest = self.TestObject * Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertListEqual(list(Other.Data), Elements)
            self.assertIsInstance(objTest, testmodule.Matrix)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            if Width == Height:
                self.assertIsInstance(objTest, testmodule.SquareMatrix)
            else:
                self.assertNotIsInstance(objTest, testmodule.SquareMatrix)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject.getRow(Row) *
                                                        Other.getColumn(Col))
            del Other
            del objTest
            self.tearDown()
            self.setUp()
    
    def test_mul_TypeError(self):
        """
        Checks the implementation of the matrix multiplication - improper types.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-302
        """
        for _ in range(10):
            for Item in self.BadTypeRight:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject * Item
            for Item in self.BadTypeLeft:
                with self.assertRaises(TypeError):
                    Temp = Item * self.TestObject
            self.tearDown()
            self.setUp()
    
    def test_mul_ValueError(self):
        """
        Checks the implementation of the matrix multiplication - mismatching
        sizes.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            Width = self.TestObject.Width
            Height = self.TestObject.Height
            Elements = [1 for _ in range(Width + random.randint(1, 3))]
            Other = testmodule.Column(*Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject * Other
            del Other
            if Width > 2:
                Elements = [1 for _ in
                                range(max(2, Width - random.randint(1, 3)))]
                Other = testmodule.Column(*Elements)
                with self.assertRaises(ValueError):
                    Temp = self.TestObject * Other
                del Other
            Elements = [1 for _ in range(Height + random.randint(1, 3))]
            Other = testmodule.Row(*Elements)
            with self.assertRaises(ValueError):
                Temp = Other * self.TestObject
            del Other
            if Height > 2:
                Elements = [1 for _ in
                                range(max(2, Height - random.randint(1, 3)))]
                Other = testmodule.Row(*Elements)
                with self.assertRaises(ValueError):
                    Temp = Other * self.TestObject
                del Other
            Elements = [[1 for _ in range(3)]
                                for _ in range(Width + random.randint(1, 3))]
            Other = testmodule.Matrix(Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject * Other
            del Other
            if Width > 2:
                Elements = [[1 for _ in range(3)] for _ in range(
                                        max(2, Width - random.randint(1, 3)))]
                Other = testmodule.Matrix(Elements)
                with self.assertRaises(ValueError):
                    Temp = self.TestObject * Other
                del Other
            Size = Width + random.randint(1, 3)
            Elements = [[1 for _ in range(Size)] for _ in range(Size)]
            Other = testmodule.SquareMatrix(Elements)
            with self.assertRaises(ValueError):
                Temp = self.TestObject * Other
            del Other
            if Width > 2:
                Size = max(2, Width - random.randint(1, 3))
                Elements = [[1 for _ in range(Size)] for _ in range(Size)]
                Other = testmodule.SquareMatrix(Elements)
                with self.assertRaises(ValueError):
                    Temp = self.TestObject * Other
                del Other
            self.tearDown()
            self.setUp()
    
    def test_div(self):
        """
        Checks the implementation of the matrix division by a scalar.

        Test ID: TEST-T-30B

        Covers requirements: REQ-FUN-306
        """
        for _ in range (10):
            Width = self.TestObject.Width
            Height = self.TestObject.Height
            Data = list(self.TestObject.Data)
            #by scalar (left and right)
            Scalar = random.randint(-10, 10)
            if not Scalar:
                Scalar = 2
            objTest = self.TestObject / Scalar
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] / Scalar)
            del objTest
            Scalar += random.random()
            objTest = self.TestObject / Scalar
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, Width)
            self.assertEqual(objTest.Height, Height)
            for Row in range(Height):
                for Col in range(Width):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] / Scalar)
            del objTest
    
    def test_div_ValueError(self):
        """
        Checks the implementation of the matrix division by zero.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-304
        """
        for _ in range(10):
            for Item in self.NotScalar:
                with self.assertRaises(ValueError):
                    Temp = self.TestObject / 0
            for Item in self.NotScalar:
                with self.assertRaises(ValueError):
                    Temp = self.TestObject / 0.0
            self.tearDown()
            self.setUp()
    
    def test_div_TypeError(self):
        """
        Checks the implementation of the matrix division - improper types.

        Test ID: TEST-T-30E

        Covers requirements: REQ-AWM-303
        """
        for _ in range(10):
            for Item in self.NotScalar:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject / Item
            self.tearDown()
            self.setUp()
    
    def test_transpose(self):
        """
        Checks the implementation of the matrix transposition.

        Test ID: TEST-T-30C

        Covers requirements: REQ-FUN-307
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            objTest = self.TestObject.transpose()
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Width, self.TestObject.Height)
            self.assertEqual(objTest.Height, self.TestObject.Width)
            for RowIndex in range(self.TestObject.Height):
                for ColIndex in range(self.TestObject.Width):
                    Item = objTest[RowIndex, ColIndex]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[ColIndex, RowIndex])
            del objTest
            self.tearDown()
            self.setUp()

class Test_SquareMatrix(Test_Matrix):
    """
    Set of unit tests for the class SquareMatrix.
    
    Implements tests: TEST-T-30A, TEST-T-30B, TEST-T-30D, TEST-T-30E
    and TEST-T-30F, TEST-T-340, TEST-T-341, TEST-T-342
    
    Covers requirements: REQ-FUN-304, REQ-FUN-305, REQ-FUN-306, REQ-FUN-320,
    REQ-FUN-330, REQ-AWM-300, REQ-AWM-301, REQ-AWM-302, REQ-AWM-303,
    REQ-AWM-304, REQ-AWM-307, REQ-AWM-308, REQ-AWM-340, REQ-AWM-341 and
    REQ-AWM-342
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = testmodule.SquareMatrix
    
    def setUp(self) -> None:
        """
        Preparation for each individual unit test.
        """
        Size = random.randint(2, 5)
        Elements = list()
        for _ in range(Size):
            Row = list()
            for _ in range(Size):
                Value = random.randint(-5, 5)
                if random.random() > 0.5:
                    Value += random.random()
                Row.append(Value)
            Elements.append(Row)
        self.TestObject = self.TestClass(Elements)
    
    def tearDown(self) -> None:
        """
        Cleaning up after each individual unit test
        """
        del self.TestObject
        self.TestObject = None
    
    def test_init(self):
        """
        Checks the different instantiation options and per element access.
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304, REQ-FUN-305
        """
        Size = random.randint(2, 5)
        Elements = list()
        for _ in range(Size*Size + 1):
            Value = random.randint(-5, 5)
            if random.random() > 0.5:
                Value += random.random()
            Elements.append(Value)
        ElementsRows = [[Elements[Size*Row + Column]
                        for Column in range(Size)] for Row in range(Size)]
        ElementsCols = [[Elements[Size*Row + Column]
                        for Row in range(Size)] for Column in range(Size)]
        Test = self.TestClass(Elements, Size = Size)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Size = Size, isColumnsFirst = False)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, isColumnsFirst = False)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(Elements, Size = Size, isColumnsFirst = True)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsCols)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsCols[Row][Col])
        del Test
        Test = self.TestClass(Elements, isColumnsFirst = True)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsCols)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsCols[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, isColumnsFirst = False)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsCols, isColumnsFirst = True)
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, isColumnsFirst = False,
                                            Size = Size + random.randint(1, 5))
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsRows, Size = Size + random.randint(1, 5))
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
        Test = self.TestClass(ElementsCols, isColumnsFirst = True,
                                            Size = Size + random.randint(1, 5))
        self.assertIsInstance(Test.Width, int)
        self.assertEqual(Test.Width, Size)
        self.assertIsInstance(Test.Height, int)
        self.assertEqual(Test.Height, Size)
        self.assertIsInstance(Test.Size, int)
        self.assertEqual(Test.Size, Size)
        self.assertIsInstance(Test.Data, list)
        self.assertListEqual(Test.Data, ElementsRows)
        for Row in range(Size):
            for Col in range(Size):
                Temp = Test[Col, Row]
                self.assertIsInstance(Temp, (int, float))
                self.assertEqual(Temp, ElementsRows[Row][Col])
        del Test
    
    def test_init_TypeError(self):
        """
        Checks the treatment of the improper data types of the arguments of the
        initialization method.
        
        Test ID: TEST-T-30D
        
        Covers requirements: REQ-AWM-300
        """
        Size = self.TestObject.Size
        Data = list(self.TestObject.Data)
        DataFlat = list()
        for Item in Data:
            DataFlat.extend(Item)
        # column / row order argument
        for Item in self.NotBool:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Size = Size,
                                                        isColumnsFirst = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, isColumnsFirst = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Data, isColumnsFirst = Item)
        # Size argument
        for Item in self.NotInt:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Size = Item)
            with self.assertRaises(TypeError):
                Temp = self.TestClass(DataFlat, Size = Item,
                                                        isColumnsFirst = True)
            #that should be ignored as the argument
            Temp = self.TestClass(Data, Size = Item)
            del Temp
        # mandatory data argument
        for Item in self.NotSequence:
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Item, Size = Size)
        for Item in self.NotScalar:
            Elements = [1 for _ in range(random.randint(4, 10))]
            Index = random.randint(0, len(Elements) - 1)
            Elements[Index] = Item
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Elements)
            Elements = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
            IndexX = random.randint(0, 2)
            IndexY = random.randint(0, 2)
            Elements[IndexX][IndexY] = Item
            with self.assertRaises(TypeError):
                Temp = self.TestClass(Elements)
    
    def test_init_ValueError(self):
        """
        Checks the treatment of the improper data types of the arguments of the
        initialization method.
        
        Test ID: TEST-T-30D
        
        Covers requirements: REQ-AWM-301
        """
        Size = self.TestObject.Size
        Data = list()
        for Item in self.TestObject.Data:
            Data.extend(Item)
        for Value in [0, 1, Size + 1, random.randint(-10, -1)]:
            with self.assertRaises(ValueError):
                Temp = self.TestClass(Data, Size = Value)
            with self.assertRaises(ValueError):
                Temp = self.TestClass(Data, Size = Value, isColumnsFirst = True)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([1, 1, 1], Size = 2)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([1, 1, 1])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([1, 1, 1, 1, 1], Size = 3)
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1], [1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1], [1, 1 ,1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1, 1, 1], [1, 1 ,1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1, 1], [1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1, 1], [1, 1, 1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1, 1], [1, 1, 1]])
        with self.assertRaises(ValueError):
            Temp = self.TestClass([[1, 1], [1, 1], [1, 1]])
    
    def test_SizeImmutable(self):
        """
        Checks that arrays and matrices are not mutable, and their property
        attributes are read-only. Also, index access is read-only.
        
        Test ID: TEST-T-30A
        
        Covers requirements: REQ-FUN-304
        """
        for _ in range(10):
            Data = list(self.TestObject.Data)
            with self.assertRaises(AttributeError):
                self.TestObject.Size = 2 + random.randint(0, 5)
            self.assertListEqual(self.TestObject.Data, Data)
            self.tearDown()
            self.setUp()
    
    def test_add(self):
        """
        Checks the implementation of the matrix summation.

        Test ID: TEST-T-30B

        Covers requirements: REQ-FUN-306
        """
        super().test_add()
        for _ in range (10):
            Size = self.TestObject.Size
            Data = list(self.TestObject.Data)
            Elements = list()
            for _ in range(Size):
                Row = list()
                for _ in range(Size):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            objTest = self.TestObject + Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Size, Size)
            for Row in range(Size):
                for Col in range(Size):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] +
                                                                Other[Col, Row])
            del objTest
            objTest = Other + self.TestObject
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Size, Size)
            for Row in range(Size):
                for Col in range(Size):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] +
                                                                Other[Col, Row])
            del objTest
            del Other
            self.tearDown()
            self.setUp()
    
    def test_sub(self):
        """
        Checks the implementation of the matrix subtraction.

        Test ID: TEST-T-30B

        Covers requirements: REQ-FUN-306
        """
        super().test_sub()
        for _ in range(10):
            Size = self.TestObject.Size
            Data = list(self.TestObject.Data)
            Elements = list()
            for _ in range(Size):
                Row = list()
                for _ in range(Size):
                    Value = random.randint(-5, 5)
                    if random.random() > 0.5:
                        Value += random.random()
                    Row.append(Value)
                Elements.append(Row)
            Other = testmodule.Matrix(Elements)
            objTest = self.TestObject - Other
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Size, Size)
            for Row in range(Size):
                for Col in range(Size):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, self.TestObject[Col, Row] -
                                                                Other[Col, Row])
            del objTest
            objTest = Other - self.TestObject
            self.assertListEqual(list(self.TestObject.Data), Data)
            self.assertIsInstance(objTest, self.TestClass)
            self.assertIs(objTest.__class__, self.TestClass)
            self.assertEqual(objTest.Size, Size)
            for Row in range(Size):
                for Col in range(Size):
                    Item = objTest[Col, Row]
                    self.assertIsInstance(Item, (int, float))
                    self.assertEqual(Item, - self.TestObject[Col, Row] +
                                                                Other[Col, Row])
            del objTest
            del Other
            self.tearDown()
            self.setUp()
    
    def test_generateIdentity_TypeError(self):
        """
        Checks improper input data type treatment.

        Test ID: TEST-T-341

        Covers requirements: REQ-AMW-341
        """
        for Item in self.NotScalar:
            with self.assertRaises(TypeError):
                Temp = self.TestClass.generateIdentity(Item)
        with self.assertRaises(TypeError):
            Temp = self.TestClass.generateIdentity(random.random())
    
    def test_generateIdentity_ValueError(self):
        """
        Checks improper input data value treatment.

        Test ID: TEST-T-342

        Covers requirements: REQ-AMW-342
        """
        with self.assertRaises(ValueError):
            Temp = self.TestClass.generateIdentity(1)
        with self.assertRaises(ValueError):
            Temp = self.TestClass.generateIdentity(0)
        for _ in range(100):
            with self.assertRaises(ValueError):
                Temp = self.TestClass.generateIdentity(random.randint(-100, 0))
    
    def test_generatePermutation_TypeError(self):
        """
        Checks improper input data type treatment.

        Test ID: TEST-T-341

        Covers requirements: REQ-AMW-341
        """
        for Item in self.NotSequence:
            with self.assertRaises(TypeError):
                Temp = self.TestClass.generatePermutation(Item)
        for Item in self.NotScalar:
            Args = list([Item for Item in range(random.randint(0, 2))])
            Args.append(Item)
            Args.extend([Item + 3 for Item in range(random.randint(1, 2))])
            with self.assertRaises(TypeError):
                Temp = self.TestClass.generatePermutation(Args)
        Args = list([Item for Item in range(random.randint(0, 2))])
        Args.append(random.random())
        Args.extend([Item + 3 for Item in range(random.randint(1, 2))])
        with self.assertRaises(TypeError):
            Temp = self.TestClass.generatePermutation(Args)
    
    def test_generatePermutation_ValueError(self):
        """
        Checks improper input data value treatment.

        Test ID: TEST-T-342

        Covers requirements: REQ-AMW-342
        """
        with self.assertRaises(ValueError):
            Temp = self.TestClass.generatePermutation([])
        with self.assertRaises(ValueError):
            Temp = self.TestClass.generatePermutation([0])
        for _ in range(100):
            Data = [Item for Item in range(random.randint(3, 10))]
            random.shuffle(Data)
            Size = len(Data)
            if Data[-1] == Size - 1:
                Test = Data[1:]
            else:
                Test = Data[:-1]
            with self.assertRaises(ValueError):
                Temp = self.TestClass.generatePermutation(Test)
            Position = random.randint(0, Size - 1)
            Test = list(Data)
            Test[Position] = - Data[Position] - 1
            with self.assertRaises(ValueError):
                Temp = self.TestClass.generatePermutation(Test)
            Test[Position] = Size
            with self.assertRaises(ValueError):
                Temp = self.TestClass.generatePermutation(Test)
            Test[Position] = Size + random.randint(1, 10)
            with self.assertRaises(ValueError):
                Temp = self.TestClass.generatePermutation(Test)
            Position1 = random.randint(0, Size - 2)
            Position2 = random.randint(Position1 + 1, Size - 1)
            Test = list(Data)
            Test[Position2] = Data[Position1]
            with self.assertRaises(ValueError):
                Temp = self.TestClass.generatePermutation(Test)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Vector)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_Column)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_Row)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_Array2D)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_Matrix)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_SquareMatrix)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting math_extra_lib.vectors_matrices module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
