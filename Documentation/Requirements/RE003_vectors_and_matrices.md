# Requirements for the Module math_extra_lib.vector_matrices

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Description / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requirement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-300

**Title:** Content of the module

**Description:** The module implements the following classes

* A generic (abstract) vector of an arbitrary length / number of elements
* A specific vector subclass representing columns of matrices and column vectors
* A specific vector subclass representing rows of matrices and rows vectors
* A generic matrix of the arbitrary N x M dimensions
* A square matrix of an arbitrary N x N size

**Verification Method:** A

---

**Requirement ID:** REQ-FUN-301

**Title:** Vector data type

**Description:** All three vector classes are, in essence, immutable sequences of real number elements, but they must be considered to be not sequences in 'IS A' type checks. Functionally, they should:

* Support read-only access to the individual elements via integer indexing, but not slices
* Do not support iterator protocol and 'value in' checks
* Be able to 'serialize' all their elements' values into a standard Python sequence

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-302

**Title:** Instantiation of the vector classes

**Description:** All three vector classes must be instantiated with any non-zero number of real number typed arguments, where the number of arguments defines the dimensions / length of the respective vector.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-303

**Title:** Additional functionality of the vector classes

**Description:** All three vector classes must provide the additional functionality:

* Generation of the orthogonal vectors set in the respective N-dimensional vector space
* Generation of the normalized vector (unit length) parallel to the current instance
* Both column and row vectors also support transposition, which transforms a column vector into the same length row vector with the same elements, and vice versa

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-304

**Title:** Matrix data type

**Description:** The both matrix classes are, in essence, immutable sequences of immutable sequences of equal number of real number elements, but they must be considered to be not sequences in 'IS A' type checks. Functionally, they should:

* Support read-only access to any individual element using two indexes as *obj[i,j]* - inner (left) for the column and outer (right) for the row
* Do not support iterator protocol and 'value in' checks
* Be able to 'serialize' all their elements' values into a standard Python nested sequence
* Provide read-only access to own individual columns and rows as instances of the column and row vectors respectively

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-305

**Title:** Instantiation of the matrix classes

**Description:** The both matrix classes could be instantiated with

* A (nested) sequence of the equal length sequences of real numbers; for the square matrices the number of the nested sequences must be equal to the length of each nested sequuence
* A plain (flat) sequence of real numbers of the length not less than the width x height of the matrix elements; for a non-square matrix both the width and the height must be explicitely specified, for the square matrices - the both sizes are equal and must be specified explicitely using a single argument

In the both cases (nested and flat sequences) the default interpretation of the data should be 'rows first', i.e. each nested sub-sequence is a single row of a matrix; the reverse 'columns first' order must be explicitely specified via an optional argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-306

**Title:** Matrix arithmetics

**Description:** The both matrix classes should support the following arithmetical operations:

* Multpilication by a real number (as both right and left operand), resulting in the same size matrix
* Division by a real, non-zero number, resulting in the same size matrix
* Addition of two equal sizes (both width and height) matrices, resulting in the same size matrix
* Subtraction of a matrix from the equal sized (both width and height) matrix, resulting in the same size matrix
* Multiplication of the matrix (as the left argument) by a column vector, if the width of the matrix equals the length of the column vector; resulting in a column vector of the length equal to the height of the matrix
* Multiplication of the matrix (as the right argument) by a row vector, if the height of the matrix equals the length of the row vector; resulting in a row vector of the length equal to width of the matrix
* Multiplication of two matrices such that the width of the left matrix (N x K) equals the height of the righ matrix (M x N), which results in a matrix of the size M x K

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-307

**Title:** Additional functionality of the matrix classes

**Description:** The both matrix classes should support the following be able to generate a transposition of themselves, i.e. a N x M matrix transposed is a matrix of M x N with each column becoming a row in the transposed matrix, and each row -> column.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-310

**Title:** Generic vectors arithmetics

**Description:** The generic vector class should support the following arithmetic operations:

* Multpilication by a real number (as both right and left operand), resulting in a vector of the same length
* Division by a real, non-zero number, resulting in a vector of the same length
* Addition of two vectors of the equal length, resulting in a vector of the same length
* Subtraction of one vector from another vector of the same length, resulting in a vector of the same length
* Dot (inner) product of two vectors of equal length, resulting in a real number, scalar value
* Outer (matrix) product of two vectors (lengths can differ, e.g. N of the left operand and M of the right operand), which results in a 2D array of the M x N size, with each i-th column being the left vector multiplied by the i-th element of the right vector

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-320

**Title:** Column vectors arithmetics

**Description:** The column vector class should support the following arithmetic operations:

* Multpilication by a real number (as both right and left operand), resulting in a column vector of the same length
* Division by a real, non-zero number, resulting in a column vector of the same length
* Addition of two column vectors of the equal length, resulting in a column vector of the same length
* Subtraction of one column vector from another column vector of the same length, resulting in a column vector of the same length
* Multiplication of a row vector (as the left operand) by a column vector of the same length (as the right operand), resulting in a real number, scalar value
* Multiplication of a column vector (as the left operand) of length N by a row vector (as the right operand) of length M, resulting in a matrix of the M x N size, with each i-th column being the left (column) vector multiplied by the i-th element of the right (row) vector

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-330

**Title:** Row vectors arithmetics

**Description:** The row vector class should support the following arithmetic operations:

* Multpilication by a real number (as both right and left operand), resulting in a row vector of the same length
* Division by a real, non-zero number, resulting in a row vector of the same length
* Addition of two row vectors of the equal length, resulting in a row vector of the same length
* Subtraction of one row vector from another row vector of the same length, resulting in a row vector of the same length
* Multiplication of a row vector (as the left operand) by a column vector of the same length (as the right operand), resulting in a real number, scalar value
* Multiplication of a column vector (as the left operand) of length N by a row vector (as the right operand) of length M, resulting in a matrix of the M x N size, with each i-th column being the left (column) vector multiplied by the i-th element of the right (row) vector

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-340

**Title:** Additional functionality of the square matrix class

**Description:** The square matrix class should implement the following additional functionality:

* Generation of an identity matrix of an arbitrary size N (N x N)
* Generation of a permutation matrix of an arbitrary size N (N x N) from a given N-permutation sequence
* Calculate the trace of a matrix
* Calculate the determinant of a matrix
* Generate an inverse matrix (unless determinant is zero)
* Calculate the LUP-decomposition, i.e. representation of the current matrix as a product of lower- and upper-triagonal matrices and a permutation matrix
* Calculate the full decomposition of a matrix into a product of a lower-triagonal, upper-triagonal, diagonal and permutation matrices
* Calculate (if such exist) all real eigen values of a matrix and the respective eigen vectors, forming an orthogonal basis

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-300

**Title:** Instantiation of the classes with improper type arguments

**Description:** An exception compatible with TypeError should be raised in the following cases:

* At least, one mandatory positional argument of the instantation / initialization of any vector classes is not a real number (int or float type)
* The mandatory argument of the instantation / initialization of any matrix class is neither a flat sequence of real numbers nor a sequence of nested sequences of real numbers
* Any optional, keyword argument of the instantation / initialization of any matrix class describing the size(s) of a matrix is not an integer number

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-301

**Title:** Instantiation of the classes with improper valued arguments

**Description:** An exception compatible with ValueError should be raised in the following cases:

* Any optional, keyword argument of the instantation / initialization of any matrix class describing the size(s) of a matrix is an integer number but not positive
* The total number of the flat or nested sequence argument of the same method is less than required number defined by the declared size of the matrix
* Number of arguments in vector instantiation is less then 2

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-302

**Title:** Improper data type of an operand

**Description:** An exception compatible with TypeError should be raised in the second operand is of the type not compatible with the class of the first operand:

* For matrices (see REQ-FUN-306):
  * Multiplication
    * Left operand is neither row vector nor scalar nor matrix
    * Right operand is neither column vector nor scalar nor matrix
  * Division - right operand is not a scalar (matrix can be only the left operand!)
  * Addition and subtraction - only between matrices is allowed
* For generic vectors (see REQ-FUN-310)
  * Multiplication
    * Left operand is not a scalar
    * Right operand is neither scalar nor another generic vector (dot product)
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

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-303

**Title:** Mismatching size of an operand

**Description:** An exception compatible with ValueError should be raised in the second operand is of the type compatible with the class of the first operand, but its size (length, width or height) does not match the size of the first operand:

* Matrix addition and subtraction - either widths or heights are not equal
* Matrix x matrix multiplication - width of the left matrix is not equal to the height of the right matrix
* Matrix x column vector multiplication - width of the matrix is not equal to the length of the vector
* Row vector x matrix multiplication - height of the matrix is not equal to the length of the vector
* Row vector x column vector multiplication - unequal length of the vectors
* Generic vector dot product with another generic vector product - unequal length of the vectors
* Any vectors addition or subtraction - unequal length of the vectors

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-304

**Title:** Division by zero

**Description:** An exception compatible with ValueError should be raised when a matrix or any vector is divided by zero scalar value, instead of ZeroDivisionError

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-305

**Title:** Improper argument type for orthogonal base vector generator

**Description:** An exception compatible with TypeError should be raised the respective method of a vector class receives any other type than an integer as any of its two arguments - length of the vector and / or index of the unity, non-zero element.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-306

**Title:** Improper argument value for orthogonal base vector generator

**Description:** An exception compatible with ValueError should be raised by the respective method if:

* The requested length of a vector is zero or negative
* The requested index of the non-zero, unity element is:
  * Negative, OR
  * Greater than the requested length - 1

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-307

**Title:** Improper argument type used for indexing

**Description:** An exception compatible with TypeError should be raised if:

* Any other data type except the integer is used in the index access to a vector's element, as in *obj[i]*; as well as to entire column or row of a matrix access
* Any other data type except of two integers (unpacked tuple of integers with 2 elements) is used in the index access to an element of a matrix, as in *obj[i,j]*

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-308

**Title:** Improper argument value used for indexing

**Description:** An exception compatible with IndexError should be raised:

* The integer index in accessing an element of a vector of length N is not in the (inclusive) range [-N, N-1]; as well as to entire column or row of a matrix access
* In the index access to an element of a matrix of N x M dimentions
  * The first (inner) integer index - for column - is not in the (inclusive) range [-N, N-1]
  * The second (outer) integer index - for row - is not in the (inclusive) range [-M, M-1]

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-340

**Title:** Singular square matrix or square matrix with a complex (not real number) eigenvalue

**Description:** No exceptions should be raised but the inability to complete the task should be indicated by returning None value in the following situations:

* The square matrix is singular (determinant is zero), thus inverse matrix does not exist
* At least one of the eigen values of the matrix is not a real number, but a complex one - thus the eigen values - eigen vectors combinations cannot be computed properly on the field of the real numbers

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-341

**Title:** Square matrix generator methods - improper argument(s) type

**Description:** An exception compatible with TypeError should be raised when:

* A non-integer argument is passed into the method of generation of an identity matrix
* The argument of the method to generate a permutation matrix is not a sequence of integer numbers

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-342

**Title:** Square matrix generator methods - improper argument(s) values

**Description:** An exception compatible with ValueError should be raised when:

* The argument of the method to generate an identity matrix is zero or negative
* Any element of the argument of the method to generate a permutation matrix is:
  * Negative, OR
  * Greater than the length of the permutation sequence - 1, OR
  * Non-unique, i.e. the same number has been used already

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-343

**Title:** Eigenvectors method - improper argument(s) type

**Description:** An exception compatible with TypeError should be raised when the method receives as the optional argument any value except integer, floating point or None type.

**Verification Method:** T
