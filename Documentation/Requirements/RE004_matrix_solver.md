# Requirements for the module math_extra_lib.matrix_solver

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

**Requirement ID:** REQ-FUN-400

**Title:** Content of the module

**Description:** The module implements the following functions

* Calculation of a single eigenvalue of a square matrix using power iteration method
* Solution of a system of linear equations, formulated in a matrix form, but only if there exists a single solution

**Verification Method:** A

---

**Requirement ID:** REQ-FUN-410

**Title:** Eigenvalue calculation

**Description:** The module implements a function, which

* Accepts a single argument, which must be an instance of **SquareMatrix** class with all real value elements
* Calculates a real value eigenvalue using the power iteration method
* Returns the found eigenvalue as an integer or floating point number
* If such real eigenvalue does not exists - the return value is **None**

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-420

**Title:** Solution of a system of linear equations

**Description:** The module implements a function, which

* Accepts two mandatory arguments:
  * All bound coefficients of the system passed either as an instance of **SquareMatrix** class, or as a flat or nested sequence of real numbers, compatible with the initialization method of the **SquareMatrix** class
  * All free coefficients of the system passed either as an instance of **Column** class, or as a flat sequence of real numbers
* Calculates the solution of the system (as a column vector)
* Returns the found solution a flat sequence (list) of real numbers
* If such solution does not exists - the return value is **None**

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AMW-410

**Title:** Eigenvalue calculation - improper argument type

**Description:** The function calculating eigenvalue raises an exception compatible with TypeError if the passed argument is not an instance of **SquareMatrix** class

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-420

**Title:** Linear equation system - improper argument(s) type

**Description:** The function calculating eigenvalue raises an exception compatible with TypeError if

* the first passed argument is not an instance of **SquareMatrix** class or flat / nested sequence of real numbers compatible with the initialization method of that class
* the second passed argument is not an instance of **Column** class or flat sequence of real numbers

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-421

**Title:** Linear equation system - mismatching sizes

**Description:** The function calculating eigenvalue raises an exception compatible with TypeError if

* the first passed argument as a flat sequence of real numbers has less than 4 elements
* the first argument as a nested sequence of real numbers has, at least, one elements (sub-sequence) of the length unequal to the length of other elements
* the number of the elements (sub-sequences) of the first argument as a nested sequence of real numbers does not equal the size of each element (sub-sequence)
* the second passed argument as flat sequence of real numbers has less than 2 elements
* the number of the free coefficients (column vector size) does not equal the size of the matrix of the bound coefficients

**Verification Method:** T
