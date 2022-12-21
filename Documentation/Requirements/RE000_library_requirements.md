# Requirements for the Library math_extra_lib

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Descriprion / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requiement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-000

**Title:** Polynomials

**Description:** The library should provide *callable* objects capable of evaluation of the value of a polynomial and a rational function (ratio of two polynomials) at the given value of their real number argument. The polynomial implementation should support the field of the real numbers in terms of its coefficients and arithmetical operations. See document [RE001](./RE001_polynomials_requirements.md).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-001

**Title:** Special functions

**Description:** The library should provide *callable* objects capable of evaluation of the value of a number of special mathematical functions (such as beta, gamma functions and their incomplete variants, as well as inverse error function, etc.). See document [RE002](./RE002_special_functions.md).

---

**Requirement ID:** REQ-FUN-002

**Title:** Vectors

**Description:** The library should implement a generic vector of length N (with real coefficients) supporting arithmetics on the field of real numbers, as well as inner and outer vector products. See document [RE003](./RE003_vectors_and_matrices.md).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-003

**Title:** Matrices

**Description:** The library should implement column and row vectors, and matrices, supporting the corresponding vector-matrix and matrix-matrix arithmetics. See document [RE003](./RE003_vectors_and_matrices.md).

**Verification Method:** T

## Interfaces

**Requirement ID:** REQ-INT-000

**Title:** Reliable dependencies

**Description:** The library should be based either solely on the Standard Python Library, or it should use only widely accepted / used and well maintained 3rd party libraries / packages.

**Verification Method:** I

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-000

**Title:** Comprehensive error messaging / treatment

**Description:** An exception should be raised with the informative description if inappropriate value / type of the arguments is passed, or an arithmetic error occurs in the process. The exception must provide clear and informative explanation.

**Verification Method:** D

## Installation and acceptance requirements

**Requirement ID:** REQ-IAR-000

**Title:** Python interpreter version

**Description:** The library should be used with Python 3 interpreter. The minimum version requirement is Python v3.6.

**Verification Method:** T

---

**Requirement ID:** REQ-IAR-001

**Title:** Operational system

**Description:** The library should work, at least, under MS Windows and GNU Linux operational systems. Ideally, it should not utilize any platform-specific functionality, therefore it should work under any OS, for which Python 3 interpreter is available.

**Verification Method:** T

---

**Requirement ID:** REQ-IAR-002

**Title:** System requirements check

**Description:** The library should provide a module / script to check if all system requirements are met, i.e. the Python interpreter version, other required libraries / packages presence as well as their versions. This module / script should report the missing requriements.

**Verification Method:** T

## User documentation requirements

**Requirement ID:** REQ-UDR-000

**Title:** The library is thoroughly documented.

**Description:** The library should be documented, including:

* Design documents
* Requirements documents
* Test reports
* User and API references

The reference documentation should provide sufficient data on the implementation for the future maintenance and modification as well as clear and comprehensive usage instructions and examples.

**Verification Method:** I
