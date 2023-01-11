# Test Report on the Module math_extra_lib.vectors_matrices

## Conventions

Each test is defined following the same format. Each test receives a unique test identifier and a reference to the ID(s) of the requirements it covers (if applicable). The goal of the test is described to clarify what is to be tested. The test steps are described in brief but clear instructions. For each test it is defined what the expected results are for the test to pass. Finally, the test result is given, this can be only pass or fail.

The test format is as follows:

**Test Identifier:** TEST-\[I/A/D/T\]-XYZ

**Requirement ID(s)**: REQ-uvw-xyz

**Verification method:** I/A/D/T

**Test goal:** Description of what is to be tested

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

The test ID starts with the fixed prefix 'TEST'. The prefix is followed by a single letter, which defines the test type / verification method. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the test ordering number for this object. E.g. 'TEST-T-112'. Each test type has its own counter, thus 'TEST-T-112' and 'TEST-A-112' tests are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Tests definition (Analysis)

**Test Identifier:** TEST-A-300

**Requirement ID(s)**: REQ-FUN-300

**Verification method:** A

**Test goal:** All required functionality is implemented and performs correctly.

**Expected result:** The required special functions are present and perform as expected, i.e. all TEST-T-3xy tests defined in this document are passed.

**Test steps:** Analyze the source code of the module [vectors\_matrices](../../vectors_matrices.py) as well as of the unit-test module [/Tests/UT003\_vectors\_matrices](../../Tests/UT003_vectors_matrices.py). Execute the mentioned unit-test module.

**Test result:** PASS / FAIL

## Tests definition (Test)

**Test Identifier:** TEST-T-300

**Requirement ID(s)**: REQ-FUN-301, REQ-FUN-302

**Verification method:** T

**Test goal:** Instantiation and behaviour of vector classes as immutable, not itterable sequences

**Expected result:** Any of the vector classes can be instantiated with an arbitrary (>= 2) number of numeric type arguments, which define the size of the vector and values of its elements. The individual elements are read-accessible using integer indexing, but cannot be assigned to. All elements can be read-out at once as a list. The class does not support iteration ('for item in object') nor the contains element check ('if item in object').

**Test steps:** Step by step instructions on how to perform the test

* Generate a list of an arbitrary length >= 2 with each element being a random integer or floating point number (random mix)
* Instantiate the tested class with this list in the unpacked form - no exception should be raised
* Check that the created instance is not a generic sequence ('is a' check)
* Check that it has property *Size*, which is an integer number equal to the length of the generated list
* Check that the *Size* property is read-only, AttributeError should be raised upon assignment
* Check that the instance of the tested class supports index read access using integer numbers in the range [-Size, Size-1] inclusively, and the returned values are the respective elements of the generated list
* Check that the assignment to an element using the same index access results in the TypeError exception
* Check that the instance of the tested class has property *Data*, which should be a list of the same elements as the generated list
* Check that the *Data* property is read-only, AttributeError should be raised upon assignment to this property
* Randomly modify the elements of the list returned by the property *Data*, check that the elements of the vector are not modified - using index access
* Check that the instance of the tested class does not support iteration - construction 'for x in y' should result in TypeError, where 'y' is the said instance
* Check that the instance of the tested class does not support 'contains check' - construction 'if x in y' should result in TypeError, where 'y' is the said instance

Repeat the test several times.

**Test result:** PASS

---

**Test Identifier:** TEST-T-301

**Requirement ID(s)**: REQ-AWM-307

**Verification method:** T

**Test goal:** Improper data type of vector indexing.

**Expected result:** An exception compatible with TypeError is raised if any data type except for an integer number is used for indexing, including slicing.

**Test steps:** Step by step instructions on how to perform the test

* Generate an random vector
* Try to access an element of the vector using different improper data types - a sub-class of TypeError should be raised each time

This test should be applied to all vector classes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-302

**Requirement ID(s)**: REQ-AWM-308

**Verification method:** T

**Test goal:** Integer index for vector is out of the range.

**Expected result:** An exception compatible with ValueError is raised if the integer index is not in the inclusive range [-Size, Size-1], where Size is the length of the vector.

**Test steps:** Step by step instructions on how to perform the test

* Generate an random vector, get its size as Size
* Try to access the following indexes elements:
  * -Size -1
  * Size
  * -Size - some random integer number > 1
  * Size + some random integer > 0
* A sub-class of ValueError should be raised each time

This test should be applied to all vector classes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-303

**Requirement ID(s)**: REQ-AWM-300

**Verification method:** T

**Test goal:** Vector instantiation with a non-numeric argument.

**Expected result:** An exception compatible with TypeError is raised if, at least, one of the arguments passed into instantiation method is neither integer nor floating point number.

**Test steps:** Step by step instructions on how to perform the test

* Try to instantiate the tested class with any improper data type as the first positional argument with total number of argyments being 1, 2 and 3
* Try to instantiate the tested class with any improper data type as the second positional argument with total number of argyments being 2 and 3
* Try to instantiate the tested class with any improper data type as the third positional argument with total number of argyments being 3 and 4
* A sub-class of TypeError exception should be raised each time
* Repeat with the different improper data types.

This test should be applied to all vector classes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-304

**Requirement ID(s)**: REQ-AWM-301

**Verification method:** T

**Test goal:** Too little arguments of vector instantiation.

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

* Try to instantiate the tested class without arguments - check that sub-class of ValueError exception is raised
* Try to instantiate the tested class with a single real number - check that sub-class of ValueError exception is raised

This test should be applied to all vector classes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-305

**Requirement ID(s)**: REQ-FUN-310, REQ-FUN-320, REQ-FUN-330

**Verification method:** T

**Test goal:** Vector - vector and vector - scalar arithmetics

**Expected result:** The following arithmetic operations are supported

* Left and right multiplication by a scalar - resulting in an instance of the same class (generic, column or row) with the same size as the first vector, and elements being product of the respective element and the scalar
* Division by a non-zero scalar - resulting in an instance of the same class (generic, column or row) with the same size as the first vector, and elements being the respective element divided by the scalar
* Addition and subtraction of two vectors of the same type and length - resulting in an instance of the same class (generic, column or row) with the same size as the both vectors, with the elements being sum / difference of the respective elements of the operands
* Scalar (dot, inner) product of two generic vectors of the same length results in a real number (scalar) equal to the sum of the products of the same index elements of the both vectors
* Outer product of two generic vectors of the sizes N and M results in a 2D array class instance of the M x N size, with each i-th column being the left vector multiplied by the i-th element of the right vector
* Product of the row and column vectors of the same size results in a real number (scalar) equal to the sum of the products of the same index elements of the both vectors
* Product of the column (size N) and row vector (size M) results in a matrix class instance of the M x N size, with each i-th column being the left vector multiplied by the i-th element of the right vector

The elements of the involved vector operands are not changed in the process.

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-306

**Requirement ID(s)**: REQ-AWM-302

**Verification method:** T

**Test goal:** Incompatible type of the second operand in the vector-vector and vector-scalar arithmetics

**Expected result:** An exception compatible with TypeError is raised if the second operand (left or right) is not comparible with the instance of the class being tested

* For generic vectors (see REQ-FUN-310)
  * Multiplication - the second operand is neither scalar nor another generic vector (dot product)
  * Division - right operand is not a scalar (vector can be only the left operand!)
  * Addition and subtraction - only between general vectors is allowed
  * Outer product - only between the general vectors is allowed
* For column vectors (see REQ-FUN-320)
  * Multiplication
    * Left operand is neither a scalar nor a row vector (dot product) nor a matrix
    * Right operand is neither scalar nor a row vector (outer product)
  * Division - right operand is not a scalar (vector can be only the left operand!)
  * Addition and subtraction - only between column vectors is allowed
* For row vectors (see REQ-FUN-330)
  * Multiplication
    * Left operand is neither a scalar nor a column vector (outer product)
    * Right operand is neither scalar nor a column vector (dot product) nor a matrix
  * Division - right operand is not a scalar (vector can be only the left operand!)
  * Addition and subtraction - only between row vectors is allowed

**Test steps:** Generate a random instance of the class being tested. Try all defined arithmetical operations with various improper data types of the second operand. Check that a sub-class of TypeError exception is raised each time.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-307

**Requirement ID(s)**: REQ-AWM-303

**Verification method:** T

**Test goal:** Mismatching lengths of the vectors in vector-vector arithmetic

**Expected result:** An exception compatible with ValueError class is raised when the lengths (sizes) of the operand vectors are not equal in the operations:

* Row vector x column vector multiplication
* Generic vector dot product with another generic vector product
* Any vectors addition or subtraction

**Test steps:** Step by step instructions on how to perform the test

* Generate a random vector of the tested class (for all three classes)
* For all three classes - generate a second random vector of the same class, but of a different size. Try to add and subtract these two vectors - check that a sub-class of ValueError exception is raised in each case
* For row vector class - generate a random column vector of a different size. Try row x column multiplication - check the ValueError sub-class exception is raised
* For generic vector - generate a second random vector of the same class. Try to multiply them - check that the ValueError sub-class exception is raised. Repeat with the reverese order of operands - check that ValueError sub-class exception is raised.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-308

**Requirement ID(s)**: REQ-AWM-304

**Verification method:** T

**Test goal:** Division of a vector by zero

**Expected result:** An exception compatible with ValueError class is raised when any vector class instance (generic, row or column) is divided by a zero (int or float)

**Test steps:** Generate a random vector of the class being tested. Try to divide it by 0 and by 0.0 - check that a sub-class of ValueError exception is raised in the both cases. This test should be applied to each of the vector classes.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-301

**Requirement ID(s)**: REQ-???-3??

**Verification method:** T

**Test goal:** Description of what is to be tested

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

---

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                       | **Verified \[YES/NO\]**) |
| :----------------- | :----------------------------------------------------------- | :----------------------- |
| REQ-FUN-300        | TEST-A-300                                                   | NO                       |
| REQ-FUN-301        | TEST-T-300                                                   | YES                      |
| REQ-FUN-302        | TEST-T-300                                                   | YES                      |
| REQ-FUN-303        |                                                              | NO                       |
| REQ-FUN-304        |                                                              | NO                       |
| REQ-FUN-305        |                                                              | NO                       |
| REQ-FUN-306        |                                                              | NO                       |
| REQ-FUN-307        |                                                              | NO                       |
| REQ-FUN-310        | TEST-T-305                                                   | NO                       |
| REQ-FUN-320        | TEST-T-305                                                   | NO                       |
| REQ-FUN-330        | TEST-T-305                                                   | NO                       |
| REQ-FUN-340        |                                                              | NO                       |
| REQ-AWM-300        | TEST-T-303                                                   | NO                       |
| REQ-AWM-301        | TEST-T-304                                                   | NO                       |
| REQ-AWM-302        | TEST-T-306                                                   | NO                       |
| REQ-AWM-303        | TEST-T-307                                                   | NO                       |
| REQ-AWM-304        | TEST-T-308                                                   | NO                       |
| REQ-AWM-305        |                                                              | NO                       |
| REQ-AWM-306        |                                                              | NO                       |
| REQ-AWM-307        | TEST-T-301                                                   | NO                       |
| REQ-AWM-308        | TEST-T-302                                                   | NO                       |
| REQ-AWM-340        |                                                              | NO                       |
| REQ-AWM-341        |                                                              | NO                       |
| REQ-AWM-342        |                                                              | NO                       |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| NO                                           | Under development    |
