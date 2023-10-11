# Test Report on the Module math_extra_lib.poly_solver

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

**Test Identifier:** TEST-A-500

**Requirement ID(s)**: REQ-FUN-500

**Verification method:** A

**Test goal:** All required functionality is implemented and performs correctly.

**Expected result:** The required functions are present and perform as expected, i.e. all TEST-T-5xy tests defined in this document are passed.

**Test steps:** Analyze the source code of the module [poly_solver](../../poly_solver.py) as well as of the unit-test module [/Tests/UT005_poly_solver](../../Tests/UT005_poly_solver.py). Execute the mentioned unit-test module. Also execute the demonstration test [/Tests/DE005_poly_solver](../../Tests/DT005_poly_sover.py).

**Test result:** PASS / FAIL

## Tests definition (Test)

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                       | **Verified \[YES/NO\]** |
| :----------------- | :----------------------------------------------------------- | :---------------------- |
| REQ-FUN-500        | TEST-A-500                                                   | NO                      |
| REQ-FUN-510        |                                                              | NO                      |
| REQ-FUN-520        |                                                              | NO                      |
| REQ-FUN-530        |                                                              | NO                      |
| REQ-FUN-540        |                                                              | NO                      |
| REQ-FUN-541        |                                                              | NO                      |
| REQ-FUN-550        |                                                              | NO                      |
| REQ-FUN-560        |                                                              | NO                      |
| REQ-FUN-561        |                                                              | NO                      |
| REQ-FUN-570        |                                                              | NO                      |
| REQ-FUN-580        |                                                              | NO                      |
| REQ-FUN-581        |                                                              | NO                      |
| REQ-FUN-590        |                                                              | NO                      |
| REQ-AWM-500        |                                                              | NO                      |
| REQ-AWM-501        |                                                              | NO                      |
| REQ-AWM-502        |                                                              | NO                      |
| REQ-AWM-503        |                                                              | NO                      |
| REQ-AWM-504        |                                                              | NO                      |
| REQ-AWM-505        |                                                              | NO                      |
| REQ-AWM-510        |                                                              | NO                      |
| REQ-AWM-520        |                                                              | NO                      |
| REQ-AWM-521        |                                                              | NO                      |
| REQ-AWM-580        |                                                              | NO                      |
| REQ-AWM-581        |                                                              | NO                      |
| REQ-AWM-590        |                                                              | NO                      |
| REQ-AWM-591        |                                                              | NO                      |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| NO                                           | Under development    |