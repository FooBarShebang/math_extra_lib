# Test Report on the Module math_extra_lib.polynomials

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

## Tests definition (Test)

**Test Identifier:** TEST-T-100

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-102, REQ-FUN-103

**Verification method:** T

**Test goal:** Check instantiation, immutability and evaluation of polynomial.

**Expected result:** The polynomial class can be instantiated with an arbitrary number of real number arguments with non-zero value of the last (zero-th to the highest order). Number of arguments define the degree of the polynomial. The coefficients of the polynomial can be retrieved and compared to be the same with the values of the passed arguments (in the used order). The polynomial evaluates to the correct value at the given value of the variable (argument). Neither operations (arithmetics) not calling methods changes the coefficients of the polynomial, they also cannot be changed directly by assignment.

**Test steps:** Instantiate a polynomial of a random degree (>= 1) with random values of the coefficients (use mixture of integer and floating point numbers). Store the used random values (coefficients values) in a sequence. Check the degree of the created polynomial - should be length of sequence minus 1. Obtain the coefficients of the polynomial from the generated object, compare them with the reference sequence - values and order must be the same.

Use the generated polynomial as left / right operand in all implemented arithmetic operations. After each performed operation check that the degree and coefficients of the polynomial are preserved. If the operation allows another polynomial as the second operand - check that is not changed either.

Call other defined methods of the polynomial - derivative / antiderivative and convolution - with arbitrary but proper arguments. Check that the polynomial is not changed. In the case of the convolution (argument is also a polynomial) check that the second polynomial is not changed either.

Try to assign random value to each of the stored coefficients using index access - check that an exception is raised each time, whereas the coefficients are not changed.

Evaluate the polynomial at several random values. Check that the result is a number with the expected value (calculated manually), whereas the coefficients are not changed.

Repeat these steps multiple times (> 10).

**Test result:** PASS

___

**Test Identifier:** TEST-T-101

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** Not real numbers are not acceptable for the initialization of a polynomial.

**Expected result:** An exception compatible with TypeError is raised if, at least, one of the arguments passed is not a real number.

**Test steps:** Try to instantiate polynomial with varying number 1 - 10 arguments (random) of real number type and 1 argument of some other data type. Try the wrong data type argument at all posible positions. In all cases the expected exception must be raised. Repeat with multiple different data types at the same positions.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-102

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Improper values are not acceptable for the initialization of a polynomial.

**Expected result:** An exception compatible with ValueError is raised if the last positional argument is zero, or there are less than 2 positional real number arguments.

**Test steps:** Try to instantiate polynomial with out arguments, with 1 non-zero real number argument, and an arbitrary number of real number arguments followed by zero (try int and float both) as the last positional argument. In all cases the expected exception must be raised. Repeat the last scenario several time with varying number of positional arguments.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-103

**Requirement ID(s)**: REQ-FUN-101

**Verification method:** T

**Test goal:** Proper construction of a polynomial from its roots.

**Expected result:** An instance of polynomial class can be generated from a sequence of roots (real values) with the degree being equal to the number of the passed root, and the highest power coefficient being 1. The constructed polynomial evaluates to zero (0) at each root value.

**Test steps:** Check that the polynomial with the expected coefficients is created for a number of pre-defined cases with the known roots. Vary the order of the roots during passing into the respective method, the result should not change. Generate an arbitrary sequence of real numbers and create a polynomial from it. Check that it has the expected degree and evaluates to zero at each root value.

**Test result:** PASS

___

**Test Identifier:** TEST-T-104

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** Not real numbers are not acceptable as arguments of 'from roots' method.

**Expected result:** An exception compatible with TypeError is raised if, at least, one of the arguments passed is not a real number.

**Test steps:** Try to call the respective method with the varying number of 0-10 arguments (random) of real number type and 1 argument of some other data type. Try the wrong data type argument at all posible positions. In all cases the expected exception must be raised. Repeat with multiple different data types at the same positions.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-105

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Improper values are not acceptable for the initialization of a polynomial.

**Expected result:** An exception compatible with ValueError is raised if no arguments are passed.

**Test steps:** Try to call the respective method without arguments or using unpacked empty sequence as the argument. In the both cases the expected exception is raised.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-106

**Requirement ID(s)**: REQ-FUN-104

**Verification method:** T

**Test goal:** Proper implementation of scalar - polynomial arithmetics.

**Expected result:** An instance of polynomial class supports the following arithmetical operations using the standard Python syntax:

* Left and right addition of a real number to a polynomial
* Substraction of a polynomial from a real number
* Substraction of a real number from a polynomial
* Left and right multiplication of a polynomial by a real number
* Division of a polynomial by a real number
* Exponentiation of a polynomial to a positive integer power

The results of the operations conform the definitions made in the respective design document [DE001](../Design/DE001_polynomials.md).

**Test steps:** Create an arbitrary polynomial (random degree and coeffiecients values). Generate a random integer and a random floating point numbers. Use these numbers as left and right addition operand and right substraction operand. Check that the result is a polynomial of the same degree, and all coefficients except the free one are the same as of the original polynomial, whereas the free coefficient has the expected different value. Use the same numbers as the left operand in substraction. Check that the result is a polynomial of the same degree, and all coefficients except the free one are the same absolute values as of the original polynomial but the opposite sign, whereas the free coefficient has the expected different value. Use the same numbers as left and right operands in multiplication and right operand in division (unless zero). Check that the result is a polynomial of the same degree and all coefficients are scaled as expected. Repeat several time with the different polynomials.

Check exponentiation in the following steps:

* Create a simple binomial (x - a) and raise it to a number of powers - e.g. 2, 3, 5 - for which the coefficients have known expression (see Newtown binomial)
* Pre-calculate 2nd and 3rd powers of some simple polynomials (2nd - 3rd power) manually and compare with the implemented exponentiation operator
* Generate a random polynomial and raise it to an arbitrary postive integer power > 1 - check that its degree is as expected; evaluate the first polynomial at some random value and raise this value to the same power, evaluate the value of the raised to power polynomial at the same argument / variable and compare to the previous value - should be (almost) equal; repeat several times at the different values of argument.

**Test result:** PASS

___

**Test Identifier:** TEST-T-107

**Requirement ID(s)**: REQ-FUN-104, REQ-FUN-105

**Verification method:** T

**Test goal:** Proper implementation of the polynomial - polynomial arithmetics.

**Expected result:** An instance of polynomial class supports the following arithmetical operations using the standard Python syntax:

* Addition of two polynomials
* Substraction of a polynomial from another polynomial
* Multiplication of two polynomials
* Division of a polynomial by another polynomial, which results in a tuple of two objects: quotient and remainder - with both or either being a real number or a polynomial

**Test steps:** Check the operations using few pre-computed (manually) examples, including addition and substraction of equal and unequal degree polynomials, as well as the case of the cancelation of the highest power coefficient(s). Check the generated results against the pre-computed ones.

For the addition, substraction and multiplication - generate a number of pairs of random polynomials. Additionally verify using evaluation check. Sum / difference / product of two polynomials must evaluate to the same value at the same argument's value as the sum / difference / product of the evaluations of the original polynomials at the same value of the argument.

Finally, generate a random polynomial of degree > 2. Mutliply it by itself 2, 3 and 4 times and compare the result with the explicit expontiation.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-108

**Requirement ID(s)**: REQ-FUN-106, REQ-FUN-107

**Verification method:** T

**Test goal:** Proper calculation of derivatives and anti-derivative.

**Expected result:** An instance of polynomial class of degree N can calculate own antiderivate (also polynomial) as well as an arbitrary degree K derivative of itself (polynomial K < N - scalar K >= N).

**Test steps:** Generate a random polynomial of degree N >= 2. Calculate its first derivative, compare it to the expected polynomial (see design documentation). Calculate a random K-th derivative where 1 < K < N - compare to the expected polynomial. Calculate the N-th derivative - it must be N! * a_N. Calculate N+1-th derivative - it must be 0. Calculate a random K > N+1 derivative - it must be zero. Calculate its first anti-derivative, compare it to the expected polynomial (see design documentation) - check that the free coefficient is zero.

Repeat this test multiple times.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-109

**Requirement ID(s)**: REQ-FUN-108

**Verification method:** T

**Test goal:** Proper calculation of convolution of polynomials.

**Expected result:** An instance of polynomial class has a method, which accepts another instance of polynomial class as its argument and returns another polynomial, which is a convolution of these two. I.e. P(x) and Q(x) are two polynomials. Then, at any value of argument x the second polynomial evaluates to Q(x) -> y. The first polynomial evaluates to P(x = y) -> z. So, the polynomial R(x) which is a convolution P(Q(x)) must evaluate to the same value z at the same value x, for any arbitrary chosen value x.

**Test steps:** Check the method using few manually pre-computed examples.

Then, generate two random 2-nd and / or 3-rd degree polynomials. Calculate their convolution 'manually' using the coefficients of the 'outer' polynomial and the already tested multiplication, addition and exponentiation operations on the 'inner' polynomial. Calculate the convolution using the respective methode of the 'outer' polynomial and the 'inner' polynomial as the argument. Compare the two calculated polynomials per coefficient - must be the same. Also evaluate the convolution at a number of random values of argument / variable, and compare them with the results of the step-wise evaluation P(x = Q(x)) - must be the same.

Repeat the random testing approach several times.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-10A

**Requirement ID(s)**: REQ-AWM-102

**Verification method:** T

**Test goal:** Improper data types as operands (arithmetics) or arguments of methods are rejected.

**Expected result:** An exception compatible with TypeError is raised in the following cases:

* Right operand of multiplication, substraction or addition is neither real number nor an instance of polynomial
* Left operand of multiplication, substraction or addition is not a real number
* Right operand of the true division is not a real number
* Right operand of the integer or mod division is not a polynomial
* Right operand of exponentiation is not an integer number
* Argument of convolution or divmod method is not a polynomial
* Optional argument (order) of the derivative method is not an integer number

**Test steps:** Instantiate a random polynomial. Try to use different data types except for the allowed as the respective (left or right) second operand in all described arithmetical operations, as well as the argument of the respective methods. Check that the expected exception is raised in each case.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-10B

**Requirement ID(s)**: REQ-AWM-103

**Verification method:** T

**Test goal:** Improper values (of the proper data types) as operands (arithmetics) or arguments of methods are rejected.

**Expected result:** An exception compatible with ValueError is raised in the following cases:

* Zero or negative integer is used as the power in the exponentiation operation
* Zero or negative integer is passed as the required order of the derivative
* Zero value (integer or floating point) is used as the right operand of the true division operations

**Test steps:** Instantiate a random polynomial. Try to raise it to 0-th power, and few negative (random) integer powers. Try to divide this polynomial by zero integer and zero floating point. Try to call the derivate method with zero, and few negative integer values as its argument. Check that the expected exception is raised in each case.

**Test result:** PASS / FAIL
___

**Test Identifier:** TEST-T-110

**Requirement ID(s)**: REQ-FUN-110, REQ-FUN-111, REQ-FUN-112

**Verification method:** T

**Test goal:** Instantiation and evaluation of rational function.

**Expected result:** An instance of rational function class can be instantiated with two arguments, each of these can be either an instance of polynomial class or a sequence of real numbers with the last element being non-zero. 

**Test steps:** Generate two random sequences of real numbers, both of the length 2 or more elements, with the last element in each sequence being non-zero. Instantiate two polynomials - one from the first sequence, and the second polynomials - from the second sequence. Generate a number of random real numbers, check that none of them is a root of the second polynomial - remove all roots from the sequence. Instantiate a fractional function from two original sequence and evaluate it at each of the generated real numbers. Check that in each case the function evaluated to the same value as the ratio of the values of the respective polynomials at the same value of the argument. Repeat test using instantiation with two polynomials, sequence + polynomial and polinomial + sequence combination of the arguments.

Select one of the values - $x_r$ - from the check sequence of numbers, at which the just tested rational function evaluates to a non-zero value *y*. Multiply the both polynomials by $(x-x_r)$ polynomial and use the returned polynomials for the instantiation of a new rational function. Evaluate the new function at $x_r$ - it should return *y* value. Repeat using $(x-x_r)^2$ and $(x-x_r)^3$ multipliers of the original polynomials.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-111

**Requirement ID(s)**: REQ-AWM-110

**Verification method:** T

**Test goal:** Improper type of an argument of the initialization method of the rational function class is rejected.

**Expected result:** An exception compatible with TypeError is raised if, at least, one of the arguments of the initialization method is neither a sequence of real numbers nor an instance of polynomial class.

**Test steps:** Generate a random sequence of real numbers with the last element being non-zero. Try to instantiate a rational function class using this sequence as the first argument, and a number of improper data types for the second argument. Check that the expected exception is raised in each case. Repeat the test using the reversed order of the arguments (first is improper, the second if the generated numbers sequence). Also try both arguments being of improper data type.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-112

**Requirement ID(s)**: REQ-AWM-111

**Verification method:** T

**Test goal:** Improper definition of either divident or divisor polynomial is rejected.

**Expected result:** An exception compatible with ValueError is raised if, at least, one of the initialization method arguments is a sequence of real numbers with the last element being zero.

**Test steps:** Generate a random sequence of real numbers with the last element being non-zero, and the second random sequence of real numbers with the last element being zero. Try to intantiate the rational function class using the first and the second sequence as its arguments. Check that the expected exception is raised. Swap the arguments and repeat. Also try using the second sequence (zero as the last element) for the both arguments.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-113

**Requirement ID(s)**: REQ-AWM-112

**Verification method:** T

**Test goal:** Only real numbers are accepted as the arguments of the rational function evaluation method.

**Expected result:** An exception compatible with TypeError is raised when a rational function's evaluation method receives an argument of any data type except for a real number.

**Test steps:** Instantiate a random rational function. Try to call its evaluation method with an argument of an improper data type, e.g. string, list, tuple, etc. Check that the expected exception is raised. Try with a number of improper data types.

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-114

**Requirement ID(s)**: REQ-AWM-113

**Verification method:** T

**Test goal:** Treatement of singularity point by rational function.

**Expected result:** An exception compatible with ValueError is raised (instead of ZeroDivision) if the argument passed into the evaluation method of a rational function is a root of the divisor but not the divident polynomial, i.e. this value is a singularity point of the rational function.

**Test steps:** Intantiate a rational function with two polynomials, with known real roots, at least - one known root for the divisor polynomial, at which the divident is not zero. Try to evaluate the rational function at this value (divisor's root). Check that the expected exception is raised.

**Test result:** PASS / FAIL

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-100        | TEST-T-100             | YES                      |
| REQ-FUN-101        | TEST-T-103             | YES                      |
| REQ-FUN-102        | TEST-T-100             | YES                      |
| REQ-FUN-103        | TEST-T-100             | YES                      |
| REQ-FUN-104        | TEST-T-106, TEST-T-107 | NO                       |
| REQ-FUN-105        | TEST-T-107             | NO                       |
| REQ-FUN-106        | TEST-T-108             | NO                       |
| REQ-FUN-107        | TEST-T-108             | NO                       |
| REQ-FUN-108        | TEST-T-109             | NO                       |
| REQ-AWM-100        | TEST-T-101, TEST-T-104 | NO                       |
| REQ-AWM-101        | TEST-T-102, TEST-T-105 | NO                       |
| REQ-AWM-102        | TEST-T-10A             | NO                       |
| REQ-AWM-103        | TEST-T-10B             | NO                       |
| REQ-FUN-110        | TEST-T-110             | NO                       |
| REQ-FUN-111        | TEST-T-110             | NO                       |
| REQ-FUN-112        | TEST-T-110             | NO                       |
| REQ-AWM-110        | TEST-T-111             | NO                       |
| REQ-AWM-111        | TEST-T-112             | NO                       |
| REQ-AWM-112        | TEST-T-113             | NO                       |
| REQ-AWM-113        | TEST-T-114             | NO                       |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
