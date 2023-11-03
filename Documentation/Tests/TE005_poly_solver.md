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

**Test Identifier:** TEST-T-500

**Requirement ID(s)**: REQ-AWM-500

**Verification method:** T

**Test goal:** Proper treatment of the improper argument type by the functions generating Legendre, Chebyshev, Berstein polynomials basis.

**Expected result:** The respective functions raise an exception compatible with TypeError if the passed argument is not an integer number.

**Test steps:** Try to call the concerned functions with an argument of any data type except for the **int** type. Check that the expected exception is raised. Repeat several times with the different data types.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-501

**Requirement ID(s)**: REQ-AWM-501

**Verification method:** T

**Test goal:** Proper treatment of the improper argument value by the functions generating Legendre, Chebyshev, Berstein polynomials basis.

**Expected result:** The respective functions raise an exception compatible with ValueError if the passed argument is a negative integer number.

**Test steps:** Try to call the concerned functions with an arbitrary negative integer number value of the argument. Check that the expected exception is raised. Repeat several times.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-502

**Requirement ID(s)**: REQ-AWM-502

**Verification method:** T

**Test goal:** Proper treatment of the improper argument type by the functions generating a single Legendre or Chebyshev polynomial.

**Expected result:** The respective functions raise an exception compatible with TypeError if the passed argument is not an integer number.

**Test steps:** Try to call the concerned functions with an argument of any data type except for the **int** type. Check that the expected exception is raised. Repeat several times with the different data types.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-503

**Requirement ID(s)**: REQ-AWM-503

**Verification method:** T

**Test goal:** Proper treatment of the improper argument value by the functions generating a single Legendre or Chebyshev polynomial.

**Expected result:** The respective functions raise an exception compatible with ValueError if the passed argument is a negative integer number.

**Test steps:** Try to call the concerned functions with an arbitrary negative integer number value of the argument. Check that the expected exception is raised. Repeat several times.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-504

**Requirement ID(s)**: REQ-AWM-504

**Verification method:** T

**Test goal:** Proper treatment of the improper argument type by the functions generating an interpolating polynomyal (all bases - Lagrange, Legendre, Chebyshev, Bernstein).

**Expected result:** The respective functions raise an exception compatible with TypeError if the passed argument is not a sequence of 2-elements sub-sequences of real numbers.

**Test steps:** Try to call the concerned functions with an argument of any of the impoper data type / structure:

* the argument is not a sequence at all (including a string, bytestring and bytearray types)
* at least, one element is not a sequence itself
* at least, one element is a (sub-) sequence but not of the length 2
* at least, one element is a (sub-) sequence of a length 2, but, at least, one of its (sub-) elements is not a real number

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-505

**Requirement ID(s)**: REQ-AWM-505

**Verification method:** T

**Test goal:** Proper treatment of the improper x-grid definintion by the functions generating an interpolating polynomyal (all bases - Lagrange, Legendre, Chebyshev, Bernstein).

**Expected result:** The respective functions raise an exception compatible with ValueError if the passed argument is a sequence of 2-elements sub-sequence of real numbers, but:

* The length of the sequence is 1 or 0 (empty), OR
* At least, one of the first elements in the pairs (x-value) is not unique

**Test steps:** Try to call the concerned functions with the following argument:

* An empty sequence
* A sequence containing only a single tuple of 2 real numbers
* A sequence containgn 3 2-elements real numbers tuples, but the first elements of two tuples being equal

Check that the expected exception is raised each time.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-510

**Requirement ID(s)**: REQ-FUN-510

**Verification method:** T

**Test goal:** Roots of an arbitrary polynomial are calculated properly.

**Expected result:** For a polynomial of degree N >= 1 (passed as an instance of Polynomial class) the returned value is a list of exactly N real or complex numbers. The polynomial evaluates to zero (within the acceptable error margin) at each value in the list. For the polynomials with the known solutions this list contains all of them, with the roots with multiplicity K > 1 being included into the list exactly K times.

**Test steps:** Pass several polynomials with known real and / or complex roots (including multiple and single roots) into the function being tested. Check that the returned list contains all expected roots counted with their multiplexity. Generate and pass into the function a number of random polynomials; check that the number of the returned roots matches the degree of the passed polynomial, and each value in the list is a close approximation of a root, i.e. the polynomial evaluates to almost zero at this value.

**Test result:** PASS

---

**Test Identifier:** TEST-T-511

**Requirement ID(s)**: REQ-AWM-510

**Verification method:** T

**Test goal:** Treatment of the improper input by the roots finding function.

**Expected result:** An exception compatible with TypeError is raised if the argument is of any data type except being an instance of the class Polynomial.

**Test steps:** Try to call the function with an argument of any data type except for the instance of Polynomial class. Check that the expected exception is raised. Repeat several times with the different data types.

**Test result:** PASS

---

**Test Identifier:** TEST-T-520

**Requirement ID(s)**: REQ-FUN-520

**Verification method:** T

**Test goal:** Proper generation of Lagrange polynomial basis

**Expected result:** For N unique x-values exactly N polynomials of the degree N-1 are generated. A polynomial corresponding i-th x-point evaluates to 1 at this point and to 0 at all other points.

**Test steps:** Generate a random x-grid of 6 points. Generate the polynomial basis. Check that there are 6 polynomials in it, and each is of the degree 5. Check that a polynomial corresponding i-th x-point evaluates to 1 at this point and to 0 at all other points.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-521

**Requirement ID(s)**: REQ-AWM-520

**Verification method:** T

**Test goal:** Proper treatment of the improper argument type by the function generating Lagrange polynomial basis.

**Expected result:** The respective function raises an exception compatible with TypeError if the passed argument is not a sequence of real numbers.

**Test steps:** Try to call the concerned functions with an argument of any of the impoper data type / structure:

* the argument is not a sequence at all (including a string, bytestring and bytearray types)
* at least, one element is not a a real number

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-522

**Requirement ID(s)**: REQ-AWM-521

**Verification method:** T

**Test goal:** Proper treatment of the improper x-grid definintion by the function generating Lagrange polynomial basis.

**Expected result:** Try to call the concerned functions with the following argument:

* An empty sequence
* A sequence containing only a single real number
* A sequence containgn 3 real numbers, but two of them being equal

Check that the expected exception is raised each time.

**Test steps:** Try to call the concerned functions with an arbitrary negative integer number value of the argument. Check that the expected exception is raised. Repeat several times.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-530

**Requirement ID(s)**: REQ-FUN-530

**Verification method:** T

**Test goal:** Proper interpolation using Lagrange basis

**Expected result:** For N unique x-values and corresponding N y-values passed as sequence of (x,y) pairs the corresponding function generates a polynomial of degree K not greater then N-1, which evaluates to y_i value at each corresponding x_i point. If all y-values are the same (constant function) the polynomial can be of 0 degree (a real number) - expected case, or a polynomial of the degree K < N if the numerical error accumulation prevents complete cancelation of the higer power terms.

**Test steps:** Generate a random x-grid of 6 points. Calculate the corresponding y-values using one of the test functions. Form the (x,y) pairs grid and passed into the function being tested. Check that the returned value is either a real number (only if all y values are the same) or a polynomial of the degree K <= 5. Check that this polynomial evaluates to y_i value at each corresponding x_i point. Try with the following check functions:

* a constant function y = const
* a linear function y = a * x + b
* a parabolic function y = a \* x^2 + b \* x + c
* a cubic function - 3rd degree polynomial
* a 4th degree polynomial
* a 5th degree polynomial
* a sine function y = a \* sin(b\*x + c) + d

The values of the coefficients can be chosen arbitrary

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-540

**Requirement ID(s)**: REQ-FUN-540

**Verification method:** T

**Test goal:** Proper calculation of the Legendre polynomial basis

**Expected result:** For the given degree N the basis consists of N+1 elements, the first being a constant value 1 (integer) and each 1 <= K <= N position the corresponding element is the K-th degree Legendre polynomial.

**Test steps:** Try to generate the basis for the degree from N = 0 to 10 inclusively. Check that a list of N+1 elements is generated, with its elements forming the sequence of the first N Legendre polynomials - compare their coefficients to the [Wikipedia](https://en.wikipedia.org/wiki/Legendre_polynomials) table.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-541

**Requirement ID(s)**: REQ-FUN-541

**Verification method:** T

**Test goal:** Proper generation of a single Legendre polynomial

**Expected result:** For the given degree N >= 1 a polynomial of the degree N is generated, and for the degree 0 - the constant integer value of 1 is generated. Each generated polynomial is the corresponding degree Legendre polynomial.

**Test steps:** Try to generate ta base polynomial of the degree from N = 0 to 10 inclusively. Check that for N=0 the **int** value of 1 is returned, and for the higher degrees a corresponding Legendre polynomial of the same degree is returned - compare the coefficients to the [Wikipedia](https://en.wikipedia.org/wiki/Legendre_polynomials) table.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-550

**Requirement ID(s)**: REQ-FUN-550

**Verification method:** T

**Test goal:** Proper interpolation using Legendre basis

**Expected result:** For N unique x-values and corresponding N y-values passed as sequence of (x,y) pairs the corresponding function generates a polynomial of degree K not greater then N-1, which evaluates to y_i value at each corresponding x_i point. If all y-values are the same (constant function) the polynomial can be of 0 degree (a real number) - expected case, or a polynomial of the degree K < N if the numerical error accumulation prevents complete cancelation of the higer power terms.

**Test steps:** Generate a random x-grid of 6 points. Calculate the corresponding y-values using one of the test functions. Form the (x,y) pairs grid and passed into the function being tested. Check that the returned value is either a real number (only if all y values are the same) or a polynomial of the degree K <= 5. Check that this polynomial evaluates to y_i value at each corresponding x_i point. Try with the following check functions:

* a constant function y = const
* a linear function y = a * x + b
* a parabolic function y = a \* x^2 + b \* x + c
* a cubic function - 3rd degree polynomial
* a 4th degree polynomial
* a 5th degree polynomial
* a sine function y = a \* sin(b\*x + c) + d

The values of the coefficients can be chosen arbitrary

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-560

**Requirement ID(s)**: REQ-FUN-560

**Verification method:** T

**Test goal:** Proper calculation of the Chebyshev polynomial basis

**Expected result:** For the given degree N the basis consists of N+1 elements, the first being a constant value 1 (integer) and each 1 <= K <= N position the corresponding element is the K-th degree Chebyshev polynomial of the first kind

**Test steps:** Try to generate the basis for the degree from N = 0 to 10 inclusively. Check that a list of N+1 elements is generated, with its elements forming the sequence of the first N Chebyshev polynomials - compare their coefficients to the [Wikipedia](https://en.wikipedia.org/wiki/Chebyshev_polynomials) table.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-561

**Requirement ID(s)**: REQ-FUN-561

**Verification method:** T

**Test goal:** Proper generation of a single Chebyshev polynomial

**Expected result:** For the given degree N >= 1 a polynomial of the degree N is generated, and for the degree 0 - the constant integer value of 1 is generated. Each generated polynomial is the corresponding degree Chebyshev polynomial of the first kind.

**Test steps:** Try to generate ta base polynomial of the degree from N = 0 to 10 inclusively. Check that for N=0 the **int** value of 1 is returned, and for the higher degrees a corresponding Chebyshev polynomial of the same degree is returned - compare the coefficients to the [Wikipedia](https://en.wikipedia.org/wiki/Chebyshev_polynomials) table.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-570

**Requirement ID(s)**: REQ-FUN-570

**Verification method:** T

**Test goal:** Proper interpolation using Chebyshev basis

**Expected result:** For N unique x-values and corresponding N y-values passed as sequence of (x,y) pairs the corresponding function generates a polynomial of degree K not greater then N-1, which evaluates to y_i value at each corresponding x_i point. If all y-values are the same (constant function) the polynomial can be of 0 degree (a real number) - expected case, or a polynomial of the degree K < N if the numerical error accumulation prevents complete cancelation of the higer power terms.

**Test steps:** Generate a random x-grid of 6 points. Calculate the corresponding y-values using one of the test functions. Form the (x,y) pairs grid and passed into the function being tested. Check that the returned value is either a real number (only if all y values are the same) or a polynomial of the degree K <= 5. Check that this polynomial evaluates to y_i value at each corresponding x_i point. Try with the following check functions:

* a constant function y = const
* a linear function y = a * x + b
* a parabolic function y = a \* x^2 + b \* x + c
* a cubic function - 3rd degree polynomial
* a 4th degree polynomial
* a 5th degree polynomial
* a sine function y = a \* sin(b\*x + c) + d

The values of the coefficients can be chosen arbitrary

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-580

**Requirement ID(s)**: REQ-FUN-580

**Verification method:** T

**Test goal:** Proper calculation of the Bernstein polynomial basis

**Expected result:** For the given degree N the basis consists of N+1 elements, each being a polynomial of N-th degree, except for N=0, in which case the basis is a single constant value 1.

**Test steps:** Try to generate the basis for the degree from N = 0 to 5 inclusively. Check that a list of N+1 elements is generated, with its elements forming the sequence of the $b_{0,N}(x)$ to $b_{N,N}(x)$ Bernstein polynomials - compare their coefficients to the [Wikipedia](https://en.wikipedia.org/wiki/Bernstein_polynomial) page.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-581

**Requirement ID(s)**: REQ-FUN-581

**Verification method:** T

**Test goal:** Proper generation of a single Bernstein polynomial

**Expected result:** For the given degree N >= 1 and the index 0 <= K <= N a polynomial of the degree N is generated, and for the degree 0 (and index 0) - the constant integer value of 1 is generated. Each generated polynomial is the corresponding $b_{K,N}(x)$ Bernstein polynomial.

**Test steps:** Try to generate ta base polynomial of the degree from N = 0 to 5 inclusively and for all corresponding indexes 0 <= K <= N. Check that for N=0 the **int** value of 1 is returned, and for the higher degrees a corresponding Bernstein polynomial of the same degree (and corresponding index) is returned - compare the coefficients to the [Wikipedia](https://en.wikipedia.org/wiki/Bernstein_polynomial) page.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-582

**Requirement ID(s)**: REQ-AWM-580

**Verification method:** T

**Test goal:** Non-integer argument(s) of a function generating a Bernstein polynomial

**Expected result:** The function raises an exception compatible with TypeError if:

* the first argument (degree) is not of the **int** type
* the second argument (index) is not of the **int** type

**Test steps:** Check the following cases:

* The first argument is any type but **int** and the second argument is a positive integer number
* The first argument is a positive integer number and the second argument is any type but **int**
* The both argument are of any type but **int**

Check that the expected exception is raised each time. Repeat several times with the different improper data types.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-583

**Requirement ID(s)**: REQ-AWM-581

**Verification method:** T

**Test goal:** Integer but of improper value argument(s) of a function generating a Bernstein polynomial

**Expected result:** The function raises an exception compatible with ValueError if:

* the first argument (degree) is negative
* the second argument (index) is negative
* the second argument is larger than the first

**Test steps:** Check the following cases:

* The first argument is a negative integer number and the second argument is a positive integer number
* The first argument is a positive integer number and the second argument is a negative integer number
* The both argument are negative integer numbers
* The both arguments are non-negative integer numbers, but the second arguments has a larger value than the first

Check that the expected exception is raised each time.

**Test result:** PASS / FAIL

---

**Test Identifier:** TEST-T-590

**Requirement ID(s)**: REQ-FUN-590

**Verification method:** T

**Test goal:** Proper interpolation using Bernstein basis

**Expected result:** For N unique x-values and corresponding N y-values passed as sequence of (x,y) pairs the corresponding function generates a polynomial of degree K not greater then N-1, which evaluates to y_i value at each corresponding x_i point. If all y-values are the same (constant function) the polynomial can be of 0 degree (a real number) - expected case, or a polynomial of the degree K < N if the numerical error accumulation prevents complete cancelation of the higer power terms.

**Test steps:** Generate a random x-grid of 6 points. Calculate the corresponding y-values using one of the test functions. Form the (x,y) pairs grid and passed into the function being tested. Check that the returned value is either a real number (only if all y values are the same) or a polynomial of the degree K <= 5. Check that this polynomial evaluates to y_i value at each corresponding x_i point. Try with the following check functions:

* a constant function y = const
* a linear function y = a * x + b
* a parabolic function y = a \* x^2 + b \* x + c
* a cubic function - 3rd degree polynomial
* a 4th degree polynomial
* a 5th degree polynomial
* a sine function y = a \* sin(b\*x + c) + d

The values of the coefficients can be chosen arbitrary

**Test result:** PASS / FAIL

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                       | **Verified \[YES/NO\]** |
| :----------------- | :----------------------------------------------------------- | :---------------------- |
| REQ-FUN-500        | TEST-A-500                                                   | NO                      |
| REQ-FUN-510        | TEST-T-510                                                   | YES                     |
| REQ-FUN-520        | TEST-T-520                                                   | NO                      |
| REQ-FUN-530        | TEST-T-530                                                   | NO                      |
| REQ-FUN-540        | TEST-T-540                                                   | NO                      |
| REQ-FUN-541        | TEST-T-541                                                   | NO                      |
| REQ-FUN-550        | TEST-T-550                                                   | NO                      |
| REQ-FUN-560        | TEST-T-560                                                   | NO                      |
| REQ-FUN-561        | TEST-T-561                                                   | NO                      |
| REQ-FUN-570        | TEST-T-570                                                   | NO                      |
| REQ-FUN-580        | TEST-T-580                                                   | NO                      |
| REQ-FUN-581        | TEST-T-581                                                   | NO                      |
| REQ-FUN-590        | TEST-T-590                                                   | NO                      |
| REQ-AWM-500        | TEST-T-500                                                   | NO                      |
| REQ-AWM-501        | TEST-T-501                                                   | NO                      |
| REQ-AWM-502        | TEST-T-502                                                   | NO                      |
| REQ-AWM-503        | TEST-T-503                                                   | NO                      |
| REQ-AWM-504        | TEST-T-504                                                   | NO                      |
| REQ-AWM-505        | TEST-T-505                                                   | NO                      |
| REQ-AWM-510        | TEST-T-511                                                   | YES                     |
| REQ-AWM-520        | TEST-T-521                                                   | NO                      |
| REQ-AWM-521        | TEST-T-523                                                   | NO                      |
| REQ-AWM-580        | TEST-T-582                                                   | NO                      |
| REQ-AWM-581        | TEST-T-583                                                   | NO                      |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| NO                                           | Under development    |
