# Test Report on the libarary math_extra_lib (global requirements)

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

## Tests definition (Inspection)

**Test Identifier:** TEST-I-000

**Requirement ID(s)**: REQ-INT-000

**Verification method:** I

**Test goal:** Reliable dependencies

**Expected result:** The library does not contain any outdated, not maintained software or software of suspicious origin as dependencies.

**Test steps:** Inspect the source code and the declared list of dependencies. **NOTE** - the analysis shows that the library has no 3rd party dependencies; it uses only the standard Python library and another library by the same developer, which is not deprecated.

**Test result:** PASS

---

**Test Identifier:** TEST-I-001

**Requirement ID(s)**: REQ-UDR-000

**Verification method:** I

**Test goal:** Completeness of the documentation

**Expected result:** For each module the corresponding requirements, test report and user reference documentation; design documentation is provided as well if the implemented functionality is non-trivial and requires additional background information, or the used numerical method or model is non-trivial and requires extensive explanation. All declared functionality is implemented, tested against the formulated requirements, and comprensively explained / documented.

**Test steps:** Inspect the documentation bundled with the library. Check that all requirements are implemented and tested. Check that user reference documentation provides comprehensive description of the functionality and complete API reference.

**Test result:** PASS

## Tests definition (Test)

**Test Identifier:** TEST-T-000

**Requirement ID(s)**: REQ-FUN-000

**Verification method:** T

**Test goal:** Check that the polynomials and rational functions are implemented as *callable* objects, and they provide all required functionality.

**Expected result:** The implementation of polynomials and rational functions meets all requirements defined in the document [RE001](../Requirements/RE001_polynomials_requirements.md), with the implemented support for the arithmetic operations conforming the [DE001](../Design/DE001_polynomials.md) document.

**Test steps:** Perform all unit and demonstration tests defined in [TE001](./TE001_polynomials.md) document, and implemented as [UT001](../../Tests/UT001_polynomial.py) and [DT001](../../Tests/DT001_polynomial.py) test modules.

**Test result:** PASS

---

**Test Identifier:** TEST-T-001

**Requirement ID(s)**: REQ-FUN-001

**Verification method:** T

**Test goal:** Check that all required special mathematical functions are implemented as *callable* objects, which perform correct calculations and provides required API

**Expected result:** All special functions defined in the [DE002](../Design/DE002_special_functions.md) document are implemented, their API (call signature, return types, exceptions being raised, etc.) conforms the requirements [RE002](../Requirements/RE002_special_functions.md) document.

**Test steps:** Perform all unit and demonstration tests defined in [TE002](./TE002_special_functions.md) document, and implemented as [UT002](../../Tests/UT002_special_functions.py) and [DT002](../../Tests/DT002_special_functions.py) test modules.

**Test result:** PASS

---

**Test Identifier:** TEST-T-002

**Requirement ID(s)**: REQ-FUN-002, REQ-FUN-003, REQ-FUN-004

**Verification method:** T

**Test goal:** Proper implementation of the vectors (including column and row vectors) and matrix classes, which support the mixed scalar - vector - matrix arithmetics. The square matrices also provide all required methods.

**Expected result:** All required classes are implemented, and support the arithmetical operations as defined in the [DE003](../Design/DE003_vectors_matrices.md) document. The class implementing square matrix provides all required additional methods (calculation of determinant, trace, inverse matrix, decomposition, eignevalues and eigenvectors) following the same design document. The signature and return types of these methods conform the requirements [RE003](../Requirements/RE003_vectors_and_matrices.md). The handling of the improper arguments and operands conforms the same requirements document. Additionally, the calculation of an eigenvalue of a defect matrix is implemented according the requirements document [RE004](../Requirements/RE004_matrix_solver.md).

**Test steps:** Perfrom all unit and demonstration tests defined in [TE003](./TE003_vectors_matrices.md) document, and implemented as [UT003](../../Tests/UT003_vectors_matrices.py) and [DT003](../../Tests/DT003_vectors_matrices.py) test modules. Additionally, perform the tests defined for the eigenvalue functionality in the document [TE004](./TE004_matrix_solver.md), and implemented in the test modules [DT004](../../Tests/DT004_matrix_solver.py) and [UT004](../../Tests/UT004_matrix_solver.py).

**Test result:** PASS

---

**Test Identifier:** TEST-T-003

**Requirement ID(s)**: REQ-FUN-005

**Verification method:** T

**Test goal:** Proper implementation of the function to solve a system of the linear equations

**Expected result:** A system of N linear equations of N variables has a single solution (single value of each of the N varibles) if the N x N square matrix formed by all bound coefficients is not singular, i.e. its determinant is non-zero. In this case the function should return such a solution. If matrix is singular, the return value should be **None**. The call signature and the return value type as well as handling of the improper arguments conform the requirements document [RE004](../Requirements/RE004_matrix_solver.md).

**Test steps:** Perform the corresponding unit and demonstration tests defined in the [TE004](./TE004_matrix_solver.md) document, and implemented in the test modules [DT004](../../Tests/DT004_matrix_solver.py) and [UT004](../../Tests/UT004_matrix_solver.py).

**Test result:** PASS

---

**Test Identifier:** TEST-T-004

**Requirement ID(s)**: REQ-FUN-006

**Verification method:** T

**Test goal:** Proper implementation of the polynomial interpolation of a real function of a single real variable.

**Expected result:** All models (different polynomials basis) defined in the [DE005](../Design/DE005_poly_solver.md) design and  [RE005](../Requirements/RE005_poly_solver.md) requirements documents are implemented, and the polynomials generated by these methods are correct, i.e. their values at the nodes (x-values) are the same as of the function being interpolated. The call signature and the return types of the corresponding functions as well as the improper arguments treatment conform the same requirements document.

**Test steps:** Perform the corresponding unit and demonstration tests defined in the [TE005](./TE005_poly_solver.md) document, and implemented in the test modules [UT005](../../Tests/UT005_poly_solver.py) and [DT005](../../Tests/DT005_poly_solver.py).

**Test result:** PASS

---

**Test Identifier:** TEST-T-005

**Requirement ID(s)**: REQ-FUN-007

**Verification method:** T

**Test goal:** Proper implementation of calculation of the roots of a polynomial.

**Expected result:** The function properly calculates **all** real or complex roots of a polynomial, including the multiple roots, i.e. the polynomial evaluates to the zero (up to rounding error) at each value, and there are exactly N such values (accounting for the roots multiplicity) for a polynomial of the degree N. The call signature, return type and handling of the improper argument(s) conform the [RE005](../Requirements/RE005_poly_solver.md) requirements document.

**Test steps:** Perform the corresponding unit and demonstration tests defined in the [TE005](./TE005_poly_solver.md) document, and implemented in the test modules [UT005](../../Tests/UT005_poly_solver.py) and [DT005](../../Tests/DT005_poly_solver.py).

**Test result:** PASS

---

**Test Identifier:** TEST-T-006

**Requirement ID(s)**: REQ-IAR-000, REQ-IAR-002

**Verification method:** T

**Test goal:** The system requirements are properly checked, including the Python interpreter version.

**Expected result:** The library includes a special script to check the system requirements: version of the Python interpreter, presence and version of each declared dependency. This script reports the results onto the console. If no problems are reported, any module of the library can be used without import errors. Furthermore, the library can be installed using *pip* tool (wheel-format distrubition model), which checks for presence and fetches the dependencies automatically when required. By design, the *pip* tool installs the version of wheel-distribution compatible with the local Python interpreter version.

**Test steps:** Install the library using *pip* tool or clone it from the Git repository on any system with Python 3.6+ interpreter. Check the console output, control that all declared dependencies are automatically fetched (if not yet present). Check that the installed library includes a special Python script for the dependencies check. Execute this script and analyze the console output. Execute all demonstration tests modules, chech that import related exceptions are not raised, and the modules behave as expected.

**Test result:** PASS

---

**Test Identifier:** TEST-T-007

**Requirement ID(s)**: REQ-IAR-001

**Verification method:** T

**Test goal:** Check that the library is cross-platform.

**Expected result:** Can be used whith any operational system and hardware configuration supporting Python 3 interpreter; at least, under MS Windows and Linux OS of various version on different IBM PC-compatible computers.

**Test steps:** Intall the library on the different machines, run the demonstration tests. See [tested OS](./tested_OS.md) document for the description of the tested hardware + OS + Python version combinations.

**Test result:** PASS

## Tests definition (Demonstration)

**Test Identifier:** TEST-D-000

**Requirement ID(s)**: REQ-AWM-000

**Verification method:** D

**Test goal:** Check that raised exceptions are informative and correct

**Expected result:** The type (class) of an exception matches the encoutered error situation; TypeError-compatible for the improper types of the input, ValueError - for a proper type but inacceptable value, etc. The raised exceptions contain informative and correct description of the problem as well as provide traceback capability for the detailed analysis.

**Test steps:** Analyze the source code, run the demonstration tests, which demonstrate the exceptions handling; specifically, the test modules [DT001](../../Tests/DT001_polynomial.py), [DT002](../../Tests/DT002_special_functions.py), [DT003](../../Tests/DT003_vectors_matrices.py), [DT004](../../Tests/DT004_matrix_solver.py) and [DT005](../../Tests/DT005_poly_solver.py).

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                       | **Verified \[YES/NO\]** |
| :----------------- | :----------------------------------------------------------- | :---------------------- |
| REQ-FUN-000        | TEST-T-000                                                   | YES                     |
| REQ-FUN-001        | TEST-T-001                                                   | YES                     |
| REQ-FUN-002        | TEST-T-002                                                   | YES                     |
| REQ-FUN-003        | TEST-T-002                                                   | YES                     |
| REQ-FUN-004        | TEST-T-002                                                   | YES                     |
| REQ-FUN-005        | TEST-T-003                                                   | YES                     |
| REQ-FUN-006        | TEST-T-004                                                   | YES                     |
| REQ-FUN-007        | TEST-T-005                                                   | YES                     |
| REQ-INT-000        | TEST-I-000                                                   | YES                     |
| REQ-AWM-000        | TEST-D-000                                                   | YES                     |
| REQ-IAR-000        | TEST-T-006                                                   | YES                     |
| REQ-IAR-001        | TEST-T-007                                                   | YES                     |
| REQ-IAR-002        | TEST-T-006                                                   | YES                     |
| REQ-UDR-000        | TEST-I-001                                                   | YES                     |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| YES                                          | All tests are passed |
