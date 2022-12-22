# Requirements for the Module math_extra_lib.polynomials

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

**Requirement ID:** REQ-FUN-100

**Title:** Polynomials instantiation.

**Description:** A generic polynomial should be implemented as a class, with the coefficients being defined during instantiation. They should be passed as (unpacked) sequence of real numbers in the either descending order from the highest to the lowest (zero) power coefficient, or in the ascending oreder of the coefficients - from the free to the N-th power coefficient. The actual power of the polynomial is defined by the highest power non-zero coefficient.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-101

**Title:** Polynomials creatation from the roots.

**Description:** A polynomial of the power N could be created from N known roots (treating all muptiple roots as individual but equal roots) with the highest power coefficient being 1.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-102

**Title:** Immutability of polynomial.

**Description:** Upon definition of the polynomial's coefficients during the instantiation they cannot be further altered neither by assignment, nor as a result of an arithmetic operations.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-103

**Title:** Evaluation of polynomial.

**Description:** A polynomial should be able to evaluate itself, i.e. calculate  own value, at a given value of its argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-104

**Title:** Arithmetic operations with real numbers.

**Description:** The polynomials should support the following arithmetic operations:

* Left and right addition of a real number to a polynomial
* Substraction of a polynomial from a real number
* Substraction of a real number from a polynomial
* Left and right multiplication of a polynomial by a real number
* Division of a polynomial by a real number
* Exponentiation of a polynomial to a positive integer power

Unary '+' (identity) and '-' (negation) operations are equivalent to addition / substraction of a polynomial to / from zero.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-105

**Title:** Arithmetic operations with two polynomials.

**Description:** The polynomials should support the following arithmetic operations:

* Addition of two polynomials
* Substraction of a polynomial from another polynomial
* Multiplication of two polynomials
* Division of a polynomial by another polynomial, which results in a tuple of two objects: quotient and remainder - with both or either being a real number or a polynomial

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-106

**Title:** Derivative of polynomial.

**Description:** A polynomial should be able to produce own derivative of any positive integer power N.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-107

**Title:** Antiderivative of polynomial.

**Description:** A polynomial should be able to produce own antiderivative up to a constant (free, zero power coefficient), which should be set to zero.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-108

**Title:** Convolution of polynomials.

**Description:** A polynomial should be able to produce a convolution with another polynomial: P(x) = sum(a\_i \* x^i), Q(x) = sum(b\_j \* x^j) => P(Q(x)) = sum(a\_i \* (Q(x))^i) = sum(c_k * x^k).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-110

**Title:** Rational function instantiation.

**Description:** A generic rational function should be implemented as a class, with the coefficients of the both divident and divisor polynomials being defined during instantiation. They should be passed as two (unpacked) sequence of real numbers in the order from the highest to the lowest (zero) power coefficient. The actual power of the created polynomial is defined by the first non-zero coefficient position, and it may be less than the length of the passed sequence minus 1, but the power cannot be below 1. Alternatively, either of the polynomials can be passed directly as a polynomial object.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-111

**Title:** Immutability of a rational function.

**Description:** Upon definition of the polynomials' coefficients during the instantiation they cannot be further altered.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-112

**Title:** Evaluation of a rational function.

**Description:** A rational function should be able to evaluate itself, i.e. calculate  own value, at a given value of its argument. If both the divident and divisor are evaluated to zero the conflict should be resolved with the L'Hospital's / Bernoulli's rule using derivatives, until either of or both terms as non-zero.

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-100

**Title:** TypeError - polynomials instantiation

**Description:** An exception compatible to the standard TypeError should be raised by the initialization method and the construction from roots method if any of the passed arguments is not a real number.

**Verification Method:** T

**Requirement ID:** REQ-AWM-101

**Title:** ValueError - polynomials instantiation

**Description:** An exception compatible to the standard ValueError should be raised by the initialization method if it recieves less than 2 positional arguments, or the last argument is zero. The construction from roots method should also raise such exception is it called without arguments.

**Verification Method:** T

**Requirement ID:** REQ-AWM-102

**Title:** TypeError - polynomials arithmetics and calculus

**Description:** An exception compatible to the standard TypeError should be raised by using any data type except real numbers and polynomials (when allowed) as the second operand of arithmetics with a polynomial. The same exception must be raised in the following situations:

* not an integer power in exponentiation operation
* not integer argument for the derivative method
* not polynomial argument for the convolution method
* not a real number as an argument for evaluation method

**Verification Method:** T

**Requirement ID:** REQ-AWM-103

**Title:** ValueError - polynomials arithmetics and calculus

**Description:** An exception compatible to the standard ValueError should be raised  in the following situations:

* zero scalar divisor in the division operation
* not positive power in the exponentiation operation
* not positive argument of the derivative method

**Verification Method:** T

**Requirement ID:** REQ-AWM-110

**Title:** TypeError - fractional function instantiation

**Description:** An exception compatible to the standard TypeError should be raised  in the following situations:

* at least one argument of the initialization method is neither polynomial nor a sequence (but not a string!)
* an element of a sequence type argument is not a real number

**Verification Method:** T

**Requirement ID:** REQ-AWM-111

**Title:** ValueError - fractional function instantiation

**Description:** An exception compatible to the standard ValueError should be raised if the last element of a sequence type argument is zero

**Verification Method:** T

**Requirement ID:** REQ-AWM-112

**Title:** TypeError - fractional function evaluation

**Description:** An exception compatible to the standard TypeError should be raised  if anything but a real number is passed as the argument of the evaluation method.

**Verification Method:** T

**Requirement ID:** REQ-AWM-113

**Title:** ValueError - fractional function evaluation

**Description:** An exception compatible to the standard ValueError should be raised if the passed argument results in the division by zero situation with non-zero divident.

**Verification Method:** T
