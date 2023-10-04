# Requirements for the module math_extra_lib.poly_solver

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

**Requirement ID:** REQ-FUN-500

**Title:** Content of the module

**Description:** The module implements the following functions

* Calculation of all complex number roots of a polynomial
* Calculation of the base Lagrange polynomials for the given x-values grid, which can be not equidistant
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Lagrange base, x-grid may be not equidistant
* Calculation of a Legendre polynomial of an arbitrary degree N >= 0
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Legendre base, x-grid may be not equidistant
* Calculation of a Chebyshev polynomial of the first kind of an arbitrary degree N >= 0
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Chebyshev base, x-grid may be not equidistant
* Calculation of all Berstein polynomials (N+1 polynomials forming a base) of an arbitrary degree N >= 0
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Chebyshev base, x-grid must be equidistant

**Verification Method:** A

---

## Alarms, warnings and operator messages
