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

**Test steps:** Analyze the source code of the module [vectors\_matrices](../../vectors_matrices.py) as well as of the unit-test module [/Tests/UT003\_vectors\_matrices](../../Tests/UT003_vectors_matrices.py). Execute the mentioned unit-test module. Also execute the demonstration test [/Tests/DE003\_vectors\_matrices](../../Tests/DT003_vectors_matrices.py).

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

Note that the row x matrix and matrix x column is to be checked in the unit tests for the matrix classes, see TEST-T-30B

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS

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

**Test result:** PASS

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

**Test result:** PASS

---

**Test Identifier:** TEST-T-308

**Requirement ID(s)**: REQ-AWM-304

**Verification method:** T

**Test goal:** Division of a vector by zero

**Expected result:** An exception compatible with ValueError class is raised when any vector class instance (generic, row or column) is divided by a zero (int or float)

**Test steps:** Generate a random vector of the class being tested. Try to divide it by 0 and by 0.0 - check that a sub-class of ValueError exception is raised in the both cases. This test should be applied to each of the vector classes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-309

**Requirement ID(s)**: REQ-FUN-303, REQ-AWM-305, REQ-AWM-306

**Verification method:** T

**Test goal:** Proper implementation of the additional functionality of the vector classes.

**Expected result:** Row and column vector classes implement transposition method, which returns an instance of column (from row) and row (from column) class respectively, with the same elements as the initial instance, which is not modified. All three classes provide a method, which returns a new instance of the same class with the elements being scaled by the geometric length of the initial vector, i.e. the square root of the sum of squares of the elements, whereas the initial instance is not modified. If all elements are zero - the same method should raise ValueError compatible exception. Finally, all three classes provide a class method (no instantiation is required), which generates an instance of the same class, which has only one element set to 1, and all other elements set to 0. For this method both the required size of the vector and the index of the non-zero element must be specified via arguments of the method call. Respectively, exceptions must be raised: TypeError sub-class if either of the arguments is not an integer number; ValueError if the requested size is less than 2, or if the index is negative or equal to or greater then the requested size of the vector.

**Test steps:** Step by step instructions on how to perform the test

* Generate a random row vector, call its method *transpose*(); check that it returns an instance of column vector class with the same elements as the original row vector, also check that the original row vector is not modified
* Generate a random column vector, call its method *transpose*(); check that it returns an instance of row vector class with the same elements as the original column vector, also check that the original column vector is not modified
* Generate a random generic vector, calculate its geometric length, then call its method *normalize*(); check that it returns an instance of the same class, of the same size, and with each element being equal to the respective element of the original vector divided by the calculated geometric length. Perform the same test with column and row vector classes.
* For all three vectror classes - generate an instance of a random size with all zero elements. Try to call its method *normalize*() and check that a sub-class of ValueError exception is raised.
* For all three vector classes:
  * Generate a random integer >= 2 as the required size of a vector and a random integer in the inclusive range from 0 to size - 1. Call the method *generateOrtogonal*() on the class itself without instantiation with the generated numbers as its arguments. Check that it returns an instance of the same class of the requested size, and that all elements except for the requested index one are zeros, whereas the requested index element is 1.
  * Try to call this method with different data types except for an integer number as the first argument - check that sub-class of TypeError exception is raised each time
  * Try to call this method with different data types except for an integer number as the second argument - check that sub-class of TypeError exception is raised each time
  * Try to call this method with values 0, 1 and a random negative integer as the first argument - check that sub-class of ValueError exception is raised each time
  * Try to call this method with the second argument being a random negative integer, an integer being equal to the first argument, and a random integer greater than the first argument - check that sub-class of ValueError exception is raised each time

**Test result:** PASS

---

**Test Identifier:** TEST-T-30A

**Requirement ID(s)**: REQ-FUN-304, REQ-FUN-305

**Verification method:** T

**Test goal:** Instantiation and index access of matices, individual columns and rows access

**Expected result:** The following modes of instantiation are supported:

* A (nested) sequence of equal length sub-sequences of real numbersm in which case the values of the optional keyword arguments for width and height (or size for the square matrices) are ignored. Each nested sub-sequence represents a single row / column (depending on the value of the optional keyword argument defining the treatment of the row / column first order), whereas the number of those nested sub-sequences defines the value of the second dimension
  * For the square matrices the number of the nested sub-sequences must be equal to the length of any of these sub-sequences
* A flat sequence of real numbers
  * For generic matrices the following combination of the optional keyword arguments is supported:
    * Both the width and the height are supplied as integer values >= 2, in which case the length of the sequence must be equal to or greater than width * height
    * The width is specified as an integer >= 2, the height is not specified or None - the length of the sequence must be, at least, 2 x width; the height is defined automaticaly as the integer floor of division of the length by the width
    * The height is specified as an integer >= 2, the width is not specified or None - the length of the sequence must be, at least, 2 x height; the width is defined automaticaly as the integer floor of division of the length by the height
  * For square matrices:
    * Size argument is provided as an integer >= 2 - the length of the sequence must be, at least, size * size
    * Size argument is not passed or None - the size is defined automatically as integer floor of the square root of the length of the sequence
* For the both flat and nested sequences the optional keyword argument defines the order of the data filling of NxM matrix as:
  * Rows first means that the matrix' elements are assigned as: 0-th row 0-th column, 0-th row 1-st column, ..., 0-th row N-th (last) column, than 1-st row, than 2-nd row, etc.
  * Columns first means that the matrix' elements are assigned as: 0-th row 0-th column, 1-st row 0-th column, ..., M-th (last) row 0-th column, than 1-st column, than 2-nd column, etc.

Any matrix (generic or square) is not a sub-class of generic sequence ('IS A' check against *collections.abc.Sequence*). It does not support iteration ('for x in object') nor 'contains' check ('if x in object').

Any matrix (generic or square) supports read-only double index access to the individual elements as 'obj[i,j]' with the inner index refering to a column, and the outer (second, right) - to a row. A whole column or row of a matrix can be read-out as an instance of the column or row vector class respectively.

Any matrix (generic or square) has a method or read-only property to read-out all elements at once as a nested list of lists of real numbers in the rows first order.

**Test steps:** Step by step instructions on how to perform the test

* Generate a random integer >= 2 as width (N) and a random integer >= 2 as height (M); for the square matrices use only the first number as the size (M=N)
* Generate a random list of a mixture of random integers and random floating point numbers of the length width \* height + 1 (size \* size + 1)
* Create two nested test lists:
  * Length M, each element is a list of length N, constructed as
    * 0, 1, ... N-1 index elements of the generated sequence
    * N, N+1, ..., 2*N-1 index elements of the generated sequence
    * etc.
  * Length N, each element is a list of length M, constructed as
    * 0, N, ..., N * (M-1) index elements of the generated sequence
    * 1, N+1, ..., N * (M-1)+1 index elements of the generated sequence
    * etc.
* For the both classes - instantiate the class with the **first** nested test list using the following options for the keyword arguments:
  * no keyword arguments
  * isColumnsFirst = False
  * isColumnsFirst = False, Width and Height / Size are random integers > max(N, M)
  * Width and Height / Size are random integers > max(N, M)
* For the both classes - instantiate the class with the **second** nested test list using the following options for the keyword arguments:
  * isColumnsFirst = True
  * isColumnsFirst = True, Width and Height / Size are random integers > max(N, M)
* For the both classes - instantiate the class with the generated **flat** list using the following options for the keyword arguments
  * For the generic matrix:
    * Width = N
    * Height = M
    * Width = N, Height = M
  * For the square matrix Size = N
* Check, that in all cases (three previous points):
  * The *Width* and *Height* / *Size* properties return the expected generated N and M values (respectively)
  * The property *Data* returns a list equal to the first nested test list
  * Assignment to these properties is not allowed (AttributeError is raised)
  * The method *getRow*(0 <= j < M) returns an instance of Row class, with the elements being equal to the j-th element of the first nested test list
  * The method *getColumn*(0 <= i < N) returns an instance of Column class, with the elements being equal to the i-th element of the second nested test list
  * The index access object[i, j] returns a real number value equal to the i-th element of the j-th element of the first nested test list
  * Assignment to an element as object[i, j] = something results in the AttributeError exception
* For the generic matrix - instantiate the class with the generated **flat** list, and the keyword arguments:
  * Width = M, isColumnsFirst = True
  * Height = N, isColumnsFirst = True
  * Width = M, Height = N, isColumnsFirst = True
* Check that:
  * The *Width* and *Height* properties return the expected generated M and N values respectively
  * The property *Data* returns a list equal to the second nested test list
* For the square matrix - instantiate the class with the generated **flat** list, and the keyword arguments Size = N, isColumnsFirst = True. Check that:
  * The *Size* property returns N
  * The property *Data* returns a list equal to the second nested test list
* For the both classes:
  * Generate a random instance using any of the allowed instantiation signature
  * Check that being used in the construction 'for x in y' (iteration) the instance throws TypeError sub-class exception
  * Check that being used in the construction 'if x in y' (contains check) the instance throws TypeError sub-class exception

**Test result:** PASS

---

**Test Identifier:** TEST-T-30D

**Requirement ID(s)**: REQ-AWM-300, REQ-AWM-301

**Verification method:** T

**Test goal:** Treatment of improper arguments of initialization method of matrix classes

**Expected result:** The matrix classes raise a sub-class of TypeError when

* Both classes: isColumnsFirst optional keyword argument is not a boolean type value
* Both classes: the mandatory first argument - the elements data - is neither a flat sequence of real numbers nor a nested sequence of sequences of real numbers
* Generic matrix class: the data argument is flat sequence, whereas either Width or Height optional keyword argument is neither None nor an integer number

The matrix classes raise a sub-class of ValueError when

* Both classes
  * The data argument is a nested sequence of less than 2 elements at the top level
  * The data argument is a nested sequence with a length of, at least, one sub-sequence element being less than 2
  * The data argument is a nested sequence with the different lengths of its sub-sequence elements
* Generic matrix
  * The data argument is a flat sequence and neither width nor height is specified
  * The data argument is a flat sequence with only width optional argument specified (not height), but the width value is less than 2
  * The data argument is a flat sequence with only width optional argument specified (not height), but the length of the data sequence is less than 2 * width
  * The data argument is a flat sequence with only height optional argument specified (not width), but the height value is less than 2
  * The data argument is a flat sequence with only height optional argument specified (not width), but the length of the data sequence is less than 2 * height
  * The data argument is a flat sequence with the both width and height arguments specified, but either of these optional arguments is less the 2
  * The data argument is a flat sequence with the both width and height arguments specified, but the length of the data sequenc is less than width * height
* Square matrix:
  * The data argument is a flat sequence and the size optional argument is not provided, and the length of the data sequence is less than 4
  * The data argument is a flat sequence and the size optional argument is provided, but the specified size is less than 2
  * The data argument is a flat sequence and the size optional argument is provided, but the length of the data sequence is less than size * size
  * The data argument is a nested sequence with a length of a sub-sequence element being unequal to the number of the sub-sequence elements

**Test steps:** Try to instantiate the class being tested with one or several arguments of the different improper data types, whereas the other arguments being of the proper data type, or not provided (for the optional ones). Check that a sub-class of TypeError exception is raised in each case. Make sure that all described violation cases are covered.

Try to instantiate the class being tested with the one or more arguments being of the proper type but of a value expected to result in ValueError sub-class exception (see above). Make sure that all described violation cases are covered, and the expected exception is raised in the each case.

**Test result:** PASS

---

**Test Identifier:** TEST-T-30F

**Requirement ID(s)**: REQ-AWM-307, REQ-AWM-308

**Verification method:** T

**Test goal:** Treatment of improper element, row or column access index of matrix classes

**Expected result:** The both matrix classes raise a sub-class of TypeError when

* Element index access is done in the form obj[index], not in the form obj[col_index, row_index], i.e. with only single index of any data type, including slice
* Element is accessed in the form obj[col_index, row_index], but either column or row index is of any data type except for an integer number, including slice
* Column (method getColum(index)) or row (method getRow(index)) is accessed using any data type argument except for an integer number, including slice

The both matrix classes raise a sub-class of ValueError when

* The column (first) index in the element access obj[col_index, row_index] is an integer but either less than - Width or greater than Width - 1, where Width is the matrix width
* The row (second) index in the element access obj[col_index, row_index] is an integer but either less than - Height or greater than Height - 1, where Height is the matrix height
* The argument of the method getColumn() method is an integer but either less than - Width or greater than Width - 1, where Width is the matrix width
* The argument of the method getRow() is an integer but either less than - Height or greater than Height - 1, where Height is the matrix height

**Test steps:** Instantiate a random matrix of the class being tested. Try to access an element using only index of an integer and slice data types; check that a sub-class of TypeError exception is raised in the both cases. Try to access an element using different improper (not integer) data types as the first, the second and both indexes, check that a sub-class of TypeError exception is raised in all cases. Try to call the methods getColumn() and getRow() with different improper (not integer) data types as the argument, check that a sub-class of TypeError exception is raised in all cases.

Try to access an element using two integer index values, with one or both being outside the allowed ranges [-Width, Width -1] and [-Height, Height - 1] respectively; check that a sub-class ValueError exception is raised in each case with the different improper values. Try to call method getColumn() with an integer argument with the value outside the allowed range [-Width, Width -1]; check that a sub-class ValueError exception is raised in each case with the different improper values. Try to call method getRow() with an integer argument with the value outside the allowed range [-Height, Height -1]; check that a sub-class ValueError exception is raised in each case with the different improper values.

**Test result:** PASS

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
| REQ-FUN-303        | TEST-T-309                                                   | YES                      |
| REQ-FUN-304        | TEST-T-30A                                                   | YES                      |
| REQ-FUN-305        | TEST-T-30A                                                   | YES                      |
| REQ-FUN-306        | TEST-T-30B                                                   | NO                       |
| REQ-FUN-307        | TEST-T-30C                                                   | NO                       |
| REQ-FUN-310        | TEST-T-305                                                   | YES                      |
| REQ-FUN-320        | TEST-T-305, TEST-T-30B                                       | NO                       |
| REQ-FUN-330        | TEST-T-305, TEST-T-30B                                       | NO                       |
| REQ-FUN-340        |                                                              | NO                       |
| REQ-AWM-300        | TEST-T-303, TEST-T-30D                                       | YES                      |
| REQ-AWM-301        | TEST-T-304, TEST-T-30D                                       | YES                      |
| REQ-AWM-302        | TEST-T-306, TEST-T-30E                                       | NO                       |
| REQ-AWM-303        | TEST-T-307, TEST-T-30E                                       | NO                       |
| REQ-AWM-304        | TEST-T-308, TEST-T-30E                                       | NO                       |
| REQ-AWM-305        | TEST-T-309                                                   | YES                      |
| REQ-AWM-306        | TEST-T-309                                                   | YES                      |
| REQ-AWM-307        | TEST-T-301, TEST-T-30F                                       | YES                      |
| REQ-AWM-308        | TEST-T-302, TEST-T-30F                                       | YES                      |
| REQ-AWM-340        |                                                              | NO                       |
| REQ-AWM-341        |                                                              | NO                       |
| REQ-AWM-342        |                                                              | NO                       |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| NO                                           | Under development    |
