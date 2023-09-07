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

**Test result:** PASS

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

**Test Identifier:** TEST-T-30B

**Requirement ID(s)**: REQ-FUN-306, REQ-FUN-320, REQ-FUN-330

**Verification method:** T

**Test goal:** Arithmetic operations with matrices

**Expected result:** Both the general and square matrix classes support the basic arithmetics:

* Two matrices can be added or one matrix can be subtracted from enother if both the widths and heights of the left and the right operands are equal. If one of the operands is a generic matrix but with equal width and height and the second operand is a square matrix the result is a square matrix.

These arithmetical operations do not change the content of the operands.

**Test steps:** Step by step instructions on how to perform the test

* Generate a generic matrix of random width and height with the random values of elements. Generate the second matrix of the same sizes and with also random values of the the elements. Perform the following operations:
  * first + second
  * second + first
  * first - second
  * second - first
* Check that in all cases the result is a matrix of the same class (type) and the dimentions; check that the content of the operands is not changed; check that the values of the elements of the resulting matrix are the sum / difference of the corresponding column / row intersection elements of the operands
* Repeat the previous tests with two square matrices (width = height = size)
* Also try a generic matrix as one of the operands (with width equal to the height) and a square matrix of the same size as the second operand - check that the result is an instance of the square matrix class of the same size and the elements are calculated properly
* Multiply a random matrix (both generic and square) by a random scalar as the right operand (try integer and float) - check that the result is a matrix of the same (sub-) class and of the same sizes, the original matrix is not changed, and each element of the resulting matrix equals the product of the used scalar and the respective (same row and column indexes) element of the original matrix.
* Multiply a random matrix (both generic and square) by a random scalar as the left operand (try integer and float) - check that the result is a matrix of the same (sub-) class and of the same sizes, the original matrix is not changed, and each element of the resulting matrix equals the product of the used scalar and the respective (same row and column indexes) element of the original matrix.
* Divide a random matrix (both generic and square) by a random but non-zero value scalar as the right operand (try integer and float) - check that the result is a matrix of the same (sub-) class and of the same sizes, the original matrix is not changed, and each element of the resulting matrix equals the respective (same row and column indexes) element of the original matrix divided by this scalar value.
* Multiply a random matrix (both generic and square) by a random column vector with the size (length) equal to the matrix width as the right operand. Check that the result is a column vector class instance with the size equal to the matrix height, and each i-th element being the result of the dot product of the i-th row of the matrix and the initial column vector.
* Multiply a random matrix (both generic and square) by a random row vector with the size (length) equal to the matrix jeight as the left operand. Check that the result is a row vector class instacne with the size equal to the matrix width, and each i-th element being the result of the dot product of the initial row vector and i-th column of the matrix.
* Generate a random matrix (try both generic and square) as the left operand and a second matrix with a random width but the height equal to the width of the first matrix (may be square or generic) as the right operand. Multiply them. Check that the result is a matrix class instance with the width of the right operand and height of the left operand, and each element at the intersection of i-th column and j-th row is the dot product of the j-th row of the left operand and i-th column of the right operand. Check that if the width of the resulting matrix equals its height the resulting matrix is also an instance of the square matrix class.

**Test result:** PASS

---

**Test Identifier:** TEST-T-30C

**Requirement ID(s)**: REQ-FUN-307

**Verification method:** T

**Test goal:** Proper implementation of the matrix transposition

**Expected result:** Both the generic and square matrix classes have an instance method, which returns a new instance of the same class with the data of the original matrix being copied and transposed, i.e. each row of the original matrix becomes a column of the transposed matrix, and each column of the original matrix becomes a row of the transposed matrix. In terms of the elements, $\mathbf{A} \rightarrow \mathbf{A}^T \; : \; \mathbf{A}_{i,j} = \mathbf{A}_{j,i}^T \; \forall i,j$

**Test steps:** Step by step instructions on how to perform the test

* Generate a random generic NxM matrix and transpose it. Check that the outcome is an instance of the generic matrix with the sizes MxN. Let **A** be the intial matrix, and **B** - the transposed matrix, check that **A**[i, j] = **B**[j, i] for all indexes.
* Generate a random square matrix with the size N and transpose it. Check that the outcome is an instance of the square matrix with the same size N. Let **A** be the intial matrix, and **B** - the transposed matrix, check that **A**[i, j] = **B**[j, i] for all indexes.
* Check that the content of the intial matrices is not changed in the both cases.
* Repeat these testes several times with the random selection of the sizes and values of the elements.

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

**Test Identifier:** TEST-T-30E

**Requirement ID(s)**: REQ-AWM-302, REQ-AWM-303, REQ-AWM-304

**Verification method:** T

**Test goal:** Exceptions are raised with improper types, sizes or values of the matrix arithmetics operands

**Expected result:** The exception compatible with / sub-class of TypeError is raised if:

* Any other data type except for a matrix instance is used as the second operand in matrix addition or subtraction

The exception compatible with / sub-class of ValueError is raised if:

* Either of the two sizes of the matrix operands of the summation or subtraction are not equal

**Test steps:** Step by step instructions on how to perform the test

* Generate a generic matrix of random width and height with the random values of elements.
* Generate a random generic matrix with the width differing by a random non-zero integer number.
* Try to subtract one matrix from another and add them - check that a sub-class of ValueError exception is raised in the both cases.
* Repeat with mis-matching heights.
* Repeat the tests with the square matrices.
* Check that that a sub-class of ValueError exception is raised when two unequal sized square matrices are added or subtracted.
* Try to add and subtract any data type value from the matrix, except for a matrix instance - check that a sub-class of TypeError exception is raised. Repeat with a number of the different data types.
* Try to add a matrix to and subtract a matrix from any data type value, except for a matrix instance - check that a sub-class of TypeError exception is raised. Repeat with a number of the different data types.
* Generate a (generic or square) marix of width and height with the random values of elements.
* Generate a random column vector of the length not equal to the matrix width. Try to multiply the matrix by this column vector - check that check that a sub-class of ValueError exception is raised.
* Generate a random row vector of the length not equal to the matrix width. Try to multiply this row vector by the matrix - check that check that a sub-class of ValueError exception is raised.
* Generate the second matrix (generic) with an arbutrary width and the height not equal to the width of the first matrix. Try to multiply the first matrix by the second - check that a sub-class of ValueError exception is raised.
* Generate a square with an arbutrary width and the size not equal to the width of the first matrix. Try to multiply the first matrix by the second - check that a sub-class of ValueError exception is raised.
* Try to multiply (right) the matrix by different data types values except for integer, floating point number, matrix (generic or square) class instance and column vector class instance - check that a sub-class of TypeError exception is raised each time.
* Try to multiply (left) the matrix by different data types values except for integer, floating point number, matrix (generic or square) class instance and row vector class instance - check that a sub-class of TypeError exception is raised each time.
* Try to divide the matrix by any data type value, except for an integer or a floating point number. Check that a sub-class of TypeError exception is raised. Repeat several times with the different data types.
* Try to divide the matrix by an integer zero and a floating point zero value. Check that a sub-class of ValueError exception is raised each time.
* Check the multiplication and division related errors with the both generic and square matrix classes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-30F

**Requirement ID(s)**: REQ-AWM-307, REQ-AWM-308

**Verification method:** T

**Test goal:** Treatment of improper element, row or column access index of matrix classes

**Expected result:** The both matrix classes raise a sub-class of TypeError when

* Element index access is done in the form obj\[index\], not in the form obj[col_index, row_index], i.e. with only single index of any data type, including slice
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

**Test Identifier:** TEST-T-340

**Requirement ID(s)**: REQ-FUN-340, REQ-AWM-340

**Verification method:** T

**Test goal:** Proper impementation of the additional functionality of the square matrix class

**Expected result:** The class implements the following class methods:

* Generation of an identity matrix of the given size N
* Generation of the corresponding permutation matrix of size N from the given permutation of numbers 0 to N-1 inclusively, each consequetive element defining the unity (non-zero) element position (column index) in the respective index row

The class inmplements the following instance methods:

* Calculation of the trace (sum of the main diagonal elements) of the matrix
* Calculation of the determinant of the matrix.
* Calculation of the multiplication inverse matrix. If it does not exist (singular matrix, determinant is zero), no exception should be raised, but the meaningful value of None should be returned.
* Calculation of the LUP-decomposition of the matrix, for the singular matrix one or more diagonal elements in the upper-triangular matrix are zeroes.
* Calculation of the LUDP-decomposition of the matrix, for the singular matrix one of more diagonal elements in the diagonal matrix are zeros.
* Calculation of all real eigen values and the respective eigen vectors bound to these eigen values as a dictionary real -> column vector. If all eigen values are complex / imaginary numbers, the returned value is None instead of a dictionary, no exceptions are raised.

**Test steps:** Step by step instructions on how to perform the test

* Try to generate using the class itself (no instantiation is required) a number of different sizes identity matrices. In each case check that an instance of a square matrix of the expected size is returned, with all main diagonal elements being 1s and all other elements - zeroes.
* Try to generate using the class itself (no instantiation is required) a number of different sizes permutation matrices using various 0..N-1 permutations (Python Standard Library, random.sample() or random.shuffle() functions). In each case check that an instance of a square matrix of the expected size is returned, with each i-th row containing only a single values of 1 at the position j with all other values being zeroes, where j is the value of i-th element of the permutation sequence.
* Generate a random square matrix. Calculate its trace using the respective instance method. 'Manually' calculate the sum of the main diagonal elements. Check that the returned trace values is the same. Repeat several times with a new matrix each time.
* Generate a random square matrix. Calculate its determinant using the respective methods. Check that a real number is returned. Repeat several times. Also check using several pre-computed examples with the known determinant values.
* Manually calculate LUP- and LUDP-decompositions of several example matrices. Check that the respective methods return the expected results.
* For the LUP-decomposition method: generate a random square matrix and call the respective method. Check that
  * The L-matrix is an instance of the square matrix class with all main diagonal elements being 1s, and all elements above - zeroes
  * The U-matrix is an instance of the square matrix class with all zero elements below the main diagonal
  * The product of all main diagonal elements of the U-matrix times the returned sign value (which is +1 or -1) equals the determinant of the original matrix
  * The P - permutation - is an integer sequence containing a proper 0..N-1 permutation, and the respective permutation matrix can be generated from it
  * The original matrix can be re-constructed as the product of L \* U \* P-matrix
* For the LUDP-decomposition method: generate a random square matrix and call the respective method. Check that
  * The L-matrix is an instance of the square matrix class with all main diagonal elements being 1s, and all elements above - zeroes
  * The U-matrix is an instance of the square matrix class with all zero elements below the main diagonal and 1s on the main diagonal
  * The D - component is a squence of real number of the length N with the product of all elements times the returned sign value (which is +1 or -1) being equal to the determinant of the original matrix
  * The P - permutation - is an integer sequence containing a proper 0..N-1 permutation, and the respective permutation matrix can be generated from it
  * The original matrix can be re-constructed as the product of L \* U \* D-matrix * P-matrix, where the D-matrix is a diagonal matrix constructed by the D - component values.
* Check the calculation of the inverse matrix using several pre-calculated cases. Also check using several random generated square matrices:
  * If the determinant of the original matrix is not zero, check that an instance of a square matrix is returned by the inverse matrix method (and of the same size), and the product of the inverse and original matrices results in an identity matrix
  * Otherwise, check that None value is returned by this method and no exception is raised.
* Check the calculation of the eigen values and eigen vectors using several pre-computed cases, including all simple eigen values (N) and one or more multiple eigen values (more than a single eigen vector per eigen value) and no real value eigen values (None as the return value, no exceptions).
  * Check that each eigen vector is normalized to the unity length and is an instance of column vector class.
  * Check that the product of the original matrix and an eigen vector results in the same vector scaled by the respective eigen value.
  * For the multiple eigen value (more than a single eigen vector bound to the same eigen value) - all vectors are othogonal, i.e. their dot product is always zero.
  * The total number of eigen values and the total number of eigen vectors do not exceed the size of the matrix.
  * All eigen values and all elements of all eigen values are real numbers.
  * Generate several random normalized and linearly independed column vectors (determinant of the matrix **V** formed from them is non zero), also generate random non-zero eigen values. Construct a diagonal matrix **M** from these eigen values. Then, construct a matrix **A** = **V** \* **M** \* **V**^-1. Check that the method calculates eigen values of the matrix **A** close to the expected (generated) values. Check that the returned vectors are indeed eigenvectors of unity length, they are linearly independent and for the same eigenvalue are orthogonal.

**Test result:** PASS

---

**Test Identifier:** TEST-T-341

**Requirement ID(s)**: REQ-AWM-341

**Verification method:** T

**Test goal:** Treatment of the improper data type of the arguments of the square matrix class methods (constructors / generators)

**Expected result:** An exception of a sub-class of TypeError is raised if:

* The identity matrix generator class method receives an argument of non-integer data type
* The permutation matrix generator class method receives an argument, which is any data type except for a sequence of integers

**Test steps:** Step by step instructions on how to perform the test

* Use the class itself, no instantiation is required
* Try to generate an identity matrix using different non-integer data types values (except for an integer) - check that sub-class of TypeError exception is raised each time
* Try to generate a permutation matrix using different data types except for sequences - check that sub-class of TypeError exception is raised each time. Also try strings and sequences containg different non-integer elements.

**Test result:** PASS

---

**Test Identifier:** TEST-T-342

**Requirement ID(s)**: REQ-AWM-342

**Verification method:** T

**Test goal:** Treatment of the imporper values of the arguments of the square matrix class methods (constructors / generators)

**Expected result:** An exception of a sub-class of TypeError is raised if:

* The identity matrix generator class method receives an argument, which is 1, zero or negative value integer
* The permutation matrix generator class method receives an argument, which is a sequence of integers with:
  * the length of the sequence is less than 2
  * for the length of the sequence N > 1 any of the elements is < 0 or >= N, or
  * there are, at least, two repetative values (not unique elements)

**Test steps:** Step by step instructions on how to perform the test

* Use the class itself, no instantiation is required
* Try to generate an identity matrix using values 1, 0 and several random negative  - check that sub-class of ValueError exception is raised each time
* Generate a random 0..N-1 numbers permutation (Python Standard Library, random.sample() or random.shuffle() functions). Try to generate a permutation matrix using different modifications of the this permutation - check that sub-class of ValueError exception is raised each time:
  * Remove one or more elements
  * Replace one or more elements with duplicating values
  * Replace one or more elements with negative integer values
  * Replace one or more elements with values >= N

**Test result:** PASS

---

**Test Identifier:** TEST-T-343

**Requirement ID(s)**: REQ-AWM-343

**Verification method:** T

**Test goal:** Treatment of the imporper type optional argument of the eigenvector method

**Expected result:** An exception of a sub-class of TypeError is raised if an argument of any type except int, float or None is passed.

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                       | **Verified \[YES/NO\]** |
| :----------------- | :----------------------------------------------------------- | :---------------------- |
| REQ-FUN-300        | TEST-A-300                                                   | YES                     |
| REQ-FUN-301        | TEST-T-300                                                   | YES                     |
| REQ-FUN-302        | TEST-T-300                                                   | YES                     |
| REQ-FUN-303        | TEST-T-309                                                   | YES                     |
| REQ-FUN-304        | TEST-T-30A                                                   | YES                     |
| REQ-FUN-305        | TEST-T-30A                                                   | YES                     |
| REQ-FUN-306        | TEST-T-30B                                                   | YES                     |
| REQ-FUN-307        | TEST-T-30C                                                   | YES                     |
| REQ-FUN-310        | TEST-T-305                                                   | YES                     |
| REQ-FUN-320        | TEST-T-305, TEST-T-30B                                       | YES                     |
| REQ-FUN-330        | TEST-T-305, TEST-T-30B                                       | YES                     |
| REQ-FUN-340        | TEST-T-340                                                   | YES                     |
| REQ-AWM-300        | TEST-T-303, TEST-T-30D                                       | YES                     |
| REQ-AWM-301        | TEST-T-304, TEST-T-30D                                       | YES                     |
| REQ-AWM-302        | TEST-T-306, TEST-T-30E                                       | YES                     |
| REQ-AWM-303        | TEST-T-307, TEST-T-30E                                       | YES                     |
| REQ-AWM-304        | TEST-T-308, TEST-T-30E                                       | YES                     |
| REQ-AWM-305        | TEST-T-309                                                   | YES                     |
| REQ-AWM-306        | TEST-T-309                                                   | YES                     |
| REQ-AWM-307        | TEST-T-301, TEST-T-30F                                       | YES                     |
| REQ-AWM-308        | TEST-T-302, TEST-T-30F                                       | YES                     |
| REQ-AWM-340        | TEST-T-340                                                   | YES                     |
| REQ-AWM-341        | TEST-T-341                                                   | YES                     |
| REQ-AWM-342        | TEST-T-342                                                   | YES                     |
| REQ-AWM-343        | TEST-T-343                                                   | YES                     |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| YES                                          | All tests are passed |
