#usr/bin/python3
"""
Module math_extra_lib.Tests.UT003_vectors_matrices

Implements unit testing of the module math_extra_lib.polynomial, see TE003.
"""

__version__ = "1.0.0.0"
__date__ = "12-01-2023"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import copy
import random

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
        TEST-T-305, TEST-T-306, TEST-T-307, TEST-T-308
    
    Covers requirements: REQ-FUN-301, REQ-FUN-302, REQ-FUN-310, REQ-AWM-300,
        REQ-AWM-301, REQ-AWM-302, REQ-AWM-303, REQ-AWM-304, REQ-AWM-307,
        REQ-AWM-308

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
                Item = objTest[Index]
                self.assertEqual(Item, Elements[Index])
            with self.assertRaises(AttributeError):
                objTest.Data = (10, 10, 10) #read-only property
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
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject + Item
                    with self.assertRaises(TypeError):
                        Temp = Item + self.TestObject
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject + Item
                with self.assertRaises(TypeError):
                    Temp = Item + self.TestObject
        with self.assertRaises(TypeError):
            Temp = self.TestObject + random.random()
        with self.assertRaises(TypeError):
            Temp = self.TestObject + random.randint()
        with self.assertRaises(TypeError):
            Temp = random.random() + self.TestObject
        with self.assertRaises(TypeError):
            Temp = random.randint() + self.TestObject
    
    def test_sub_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject - Item
                    with self.assertRaises(TypeError):
                        Temp = Item - self.TestObject
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject - Item
                with self.assertRaises(TypeError):
                    Temp = Item - self.TestObject
        with self.assertRaises(TypeError):
            Temp = self.TestObject - random.random()
        with self.assertRaises(TypeError):
            Temp = self.TestObject - random.randint()
        with self.assertRaises(TypeError):
            Temp = random.random() - self.TestObject
        with self.assertRaises(TypeError):
            Temp = random.randint() - self.TestObject
    
    def test_add_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
        Other = self.TestClass(*Elements)
        with self.assertRaises(ValueError):
            Temp = self.TestObject + Other
        with self.assertRaises(ValueError):
            Temp = Other + self.TestObject
        del Other
    
    def test_sub_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
        Other = self.TestClass(*Elements)
        with self.assertRaises(ValueError):
            Temp = self.TestObject - Other
        with self.assertRaises(ValueError):
            Temp = Other - self.TestObject
        del Other
    
    def test_add(self):
        """
        Checks the addition of two vectors
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310, REQ-FUN-320, REQ-FUN-330
        """
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
    
    def test_sub(self):
        """
        Checks the subtraction of two vectors
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310, REQ-FUN-320, REQ-FUN-330
        """
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
        
    def test_mul_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject * Item
                with self.assertRaises(TypeError):
                    Temp = Item * self.TestObject
    
    def test_mul_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
        Other = self.TestClass(*Elements)
        with self.assertRaises(ValueError):
            Temp = self.TestObject * Other
        with self.assertRaises(ValueError):
            Temp = Other * self.TestObject
        del Other
    
    def test_mul(self):
        """
        Checks the dot multiplication of two generic vectors and generic
        vector left and right multiplication by a scalar
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
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
    
    def test_matmul_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        for Item in self.NotScalar:
            if isinstance(Item, self.TestClass):
                if not (Item.__class__ is self.TestClass):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject @ Item
                    with self.assertRaises(TypeError):
                        Temp = Item @ self.TestObject
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject @ Item
                with self.assertRaises(TypeError):
                    Temp = Item @ self.TestObject
        for Item in [1, 1.0]:
            with self.assertRaises(TypeError):
                Temp = self.TestObject @ Item
            with self.assertRaises(TypeError):
                Temp = Item @ self.TestObject
    
    def test_matmul(self):
        """
        Checks the implementation of the outer generic vectors product.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        Data = list(self.TestObject.Data)
        Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
        Other = self.TestClass(*Elements)
        Test = self.TestObject @ Other
        self.assertIsInstance(Test, testmodule.Array2D)
        #TODO - check Matrix size and content!
        self.assertListEqual(self.TestObject.Data, Data)
        del Test
        Test = Other @ self.TestObject
        self.assertIsInstance(Test, testmodule.Array2D)
        #TODO - check Matrix size and content!
        self.assertListEqual(self.TestObject.Data, Data)
        del Test
        del Other
        #TODO - also check for the unequal sizes!
    
    def test_div_TypeError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-306
        
        Covers requirements: REQ-AWM-302
        """
        for Item in self.NotScalar:
            with self.assertRaises(TypeError):
                Temp = self.TestObject / Item
            with self.assertRaises(TypeError):
                Temp = Item / self.TestObject
        with self.assertRaises(TypeError):
            Temp = 1 / self.TestObject
        with self.assertRaises(TypeError):
            Temp = 1.0 / self.TestObject
    
    def test_div_ValueError(self):
        """
        Checks treatment of division by zero
        
        Test ID: TEST-T-308
        
        Covers requirements: REQ-AWM-304
        """
        with self.assertRaises(ValueError):
            Temp = self.TestObject / 0
        with self.assertRaises(ValueError):
            Temp = self.TestObject / 0.0
    
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
        New = +self.TestObject
        self.assertIs(New.__class__, self.TestClass)
        self.assertIsNot(New, self.TestObject)
        self.assertEqual(New.Size, self.TestObject.Size)
        self.assertListEqual(New.Data, self.TestObject.Data)
        del New
    
    def test_neg(self):
        """
        Checks the implementation of the unitary plus operation.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        Elements = [-Item for Item in self.TestObject.Data]
        New = -self.TestObject
        self.assertIs(New.__class__, self.TestClass)
        self.assertIsNot(New, self.TestObject)
        self.assertEqual(New.Size, self.TestObject.Size)
        self.assertListEqual(New.Data, Elements)
        del New

class Test_Column(Test_Vector):
    """
    Unit tests for the column vector class.
    
    Test IDs: TEST-T-300, TEST-T-301, TEST-T-302, TEST-T-303, TEST-T-304,
        TEST-T-305, TEST-T-306, TEST-T-307, TEST-T-308
    
    Covers requirements: REQ-FUN-301, REQ-FUN-302, REQ-FUN-320, REQ-AWM-300,
        REQ-AWM-301, REQ-AWM-302, REQ-AWM-303, REQ-AWM-304, REQ-AWM-307,
        REQ-AWM-308

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
        for Item in self.NotScalar:
            if isinstance(Item, testmodule.Vector):
                if not (Item.__class__ is testmodule.Row):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
            else:
                with self.assertRaises(TypeError):
                    Temp = self.TestObject * Item
                if not isinstance(Item, testmodule.Matrix):
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
    
    def test_mul_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
        Other = testmodule.Row(*Elements)
        with self.assertRaises(ValueError):
            Temp = Other * self.TestObject
        del Other
    
    def test_mul(self):
        """
        Checks the column vector left and right multiplication by a scalar
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-320
        """
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
    
    def test_matmul(self):
        """
        Checks that the outer product is not defined for the column vectors.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        Data = list(self.TestObject.Data)
        Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
        Other = self.TestClass(*Elements)
        with self.assertRaises(TypeError):
            Test = self.TestObject @ Other
        with self.assertRaises(TypeError):
            Test = Other @ self.TestObject
        del Other

class Test_Row(Test_Vector):
    """
    Unit tests for the row vector class.
    
    Test IDs: TEST-T-300, TEST-T-301, TEST-T-302, TEST-T-303, TEST-T-304,
        TEST-T-305, TEST-T-306, TEST-T-307, TEST-T-308
    
    Covers requirements: REQ-FUN-301, REQ-FUN-302, REQ-FUN-320, REQ-FUN-330,
        REQ-AWM-300, REQ-AWM-301, REQ-AWM-302, REQ-AWM-303, REQ-AWM-304,
        REQ-AWM-307, REQ-AWM-308

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
        for Item in self.NotScalar:
            if isinstance(Item, testmodule.Vector):
                if not (Item.__class__ is testmodule.Column):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                    with self.assertRaises(TypeError):
                        Temp = Item * self.TestObject
            else:
                if not isinstance(Item, testmodule.Matrix):
                    with self.assertRaises(TypeError):
                        Temp = self.TestObject * Item
                with self.assertRaises(TypeError):
                    Temp = Item * self.TestObject
    
    def test_mul_ValueError(self):
        """
        Checks treatment of operands incompatibility
        
        Test ID: TEST-T-307
        
        Covers requirements: REQ-AWM-303
        """
        Elements = [random.random()
                for _ in range(self.TestObject.Size + random.randint(1, 10))]
        Other = testmodule.Column(*Elements)
        with self.assertRaises(ValueError):
            Temp = self.TestObject * Other
        del Other
    
    def test_mul(self):
        """
        Checks the row vector left and right multiplication by a scalar, and
        row x column and column x row vector multiplications.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-320, REQ-FUN-330
        """
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
        Test = Other * self.TestObject
        self.assertIsInstance(Test, testmodule.SquareMatrix)
        #TODO - check Matrix size and content!
        self.assertListEqual(self.TestObject.Data, Data)
        del Test
        del Other
        #TODO - also check for the unequal sizes!
    
    def test_matmul(self):
        """
        Checks that the outer product is not defined for the row vectors.
        
        Test ID: TEST-T-305
        
        Covers requirements: REQ-FUN-310
        """
        Data = list(self.TestObject.Data)
        Elements = [random.random() + random.randint(-10, 10)
                                        for _ in range(self.TestObject.Size)]
        Other = self.TestClass(*Elements)
        with self.assertRaises(TypeError):
            Test = self.TestObject @ Other
        with self.assertRaises(TypeError):
            Test = Other @ self.TestObject
        del Other

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Vector)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_Column)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_Row)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting math_extra_lib.vectors_matrices module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
