# Test Report on the Module math_extra_lib.matrix_solver

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

**Test Identifier:** TEST-A-400

**Requirement ID(s)**: REQ-FUN-400

**Verification method:** A

**Test goal:** All required functionality is implemented and performs correctly.

**Expected result:** The required functions are present and perform as expected, i.e. all TEST-T-5xy tests defined in this document are passed.

**Test steps:** Analyze the source code of the module [matrix_solver](../../matrix_solver.py) as well as of the unit-test module [/Tests/UT004_matrix_solver](../../Tests/UT004_matrix_solver.py). Execute the mentioned unit-test module. Also execute the demonstration test [/Tests/DE004_matrix_solver](../../Tests/DT004_matrix_solver.py).

**Test result:** PASS / FAIL

## Tests definition (Test)

**Test Identifier:** TEST-T-410

**Requirement ID(s)**: REQ-FUN-410

**Verification method:** T

**Test goal:** Eigenvalue calculation - performance

**Expected result:** The function calculates a real eigenvalue of any real matrix, if such exists; even if the matrix is defective (non-diagonalizable) but not singular (determinant is not zero), for instance, shear matrix, etc.

**Test steps:** Generate a number of square matrices with the size varying from 2 to 5 inclusively, for which the eigenvalues are known, including defective matrices. Pass each of the generated matrices into the function being tested. Check that the function returns a real value (**int** or **float** type), which is one of the eigenvalues of the corresponding matrix.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-411

**Requirement ID(s)**: REQ-FUN-410

**Verification method:** T

**Test goal:** Eigenvalue calculation - no real eigenvalues situation treatment

**Expected result:** The function returns **None** value if there is no real eigenvalue.

**Test steps:** Generate a number of square matrices with the size varying from 2 to 5 inclusively, which are either singular or known to have no real eigenvalues (e.g. 2D rotation matrix or 3D rotation matrix with, at least, 2-axes rotation). Pass each of the generated matrices into the function being tested. Check that the function returns **None** value, and does not raise any exceptions.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-412

**Requirement ID(s)**: REQ-AWM-410

**Verification method:** T

**Test goal:** Eigenvalue calculation - treatement of improper argument type

**Expected result:** An exception compatible with TypeError is raised if the passed argument is not an instance of **SquareMatrix** class.

**Test steps:** Try to call the function being tested with the argument of any data type, except for being instance of the **SquareMatrix** class. Check that the expected exception is raised. Repeat several times with the different improper types of the argument.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-420

**Requirement ID(s)**: REQ-FUN-420

**Verification method:** T

**Test goal:** Linear system solution - performance

**Expected result:** The function returns **None** value if there is no real eigenvalue.

**Test steps:** Check the correctness of the solver function on few examples with the known solutions. Generate a number random non-singular matrices of the size 2 to 5 inclusively, and random non-zero column vectors of the corresponding size. Calculate the solution for each pair, create a column vector from it, and verify that this is a solution using matrix x column multiplication. Try to pass the same matrices as 2D and 1D arrays, and check that the result is the same. Try to pass the free coefficients column vector as flat sequence - check that the result is the same.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-421

**Requirement ID(s)**: REQ-FUN-420

**Verification method:** T

**Test goal:** Linear system solution - single solution does not exist case

**Expected result:** The function returns **None** value if there is single solution of the system (determinant is zero).

**Test steps:** Generate a random square matrix of size 2 to 5 inclusively, with two equal rows, and a random column vector of the corresponding size. Pass these objects as the arguments of the function being tested. Check that no exceptions are raised, and the return value is **None**. Repeat several times.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-422

**Requirement ID(s)**: REQ-AWM-420

**Verification method:** T

**Test goal:** Linear system solution - treatement of improper argument type

**Expected result:** An exception compatible with TypeError is raised if:

* the first passed argument is not an instance of **SquareMatrix** class or flat / nested sequence of real numbers compatible with the initialization method of that class
* the second passed argument is not an instance of **Column** class or flat sequence of real numbers

**Test steps:** Try to call the function being tested with one or both argument of any data type not matching the declared signature. Check that the expected exception is raised. Repeat several times with the different improper types of the argument(s).

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-423

**Requirement ID(s)**: REQ-AWM-421

**Verification method:** T

**Test goal:** Linear system solution - treatement of the mismatching sizes

**Expected result:** An exception compatible with ValueError is raised if:

* the first passed argument as a flat sequence of real numbers has less than 4 elements - square matrix must have size >= 2, i.e., at least 4 elements
* the first argument as a nested sequence of real numbers has, at least, one elements (sub-sequence) of the length unequal to the length of other elements - the matrix must be square
* the number of the elements (sub-sequences) of the first argument as a nested sequence of real numbers does not equal the size of each element (sub-sequence) - each row must contain exactly the same number of elements
* the second passed argument as flat sequence of real numbers has less than 2 elements - column vector must be of the size 2, at least
* the number of the free coefficients (column vector size) does not equal the size of the matrix of the bound coefficients - the size of the matrix and size of the column vector must be equal

**Test steps:** Try to call the function being tested with arguments implementing one of the described above violations. Check that the expected exception is raised. Check each of the violation cases.

**Test result:** PASS/FAIL

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                       | **Verified \[YES/NO\]** |
| :----------------- | :----------------------------------------------------------- | :---------------------- |
| REQ-FUN-400        | TEST-A-400                                                   | NO                      |
| REQ-FUN-410        | TEST-T-410, TEST-T-411                                       | NO                      |
| REQ-FUN-420        | TEST-T-420, TEST-T-421                                       | NO                      |
| REQ-AWM-410        | TEST-T-412                                                   | NO                      |
| REQ-AWM-420        | TEST-T-422                                                   | NO                      |
| REQ-AWM-421        | TEST-T-423                                                   | NO                      |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| NO                                           | Under development    |
