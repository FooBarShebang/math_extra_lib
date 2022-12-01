# Test Report on the Module statistics_lib.polynomials

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

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-102

**Verification method:** T

**Test goal:** Check instantiation, immutability and evaluation of polynomial.

**Expected result:** The polynomial class can be instantiated with an arbitrary number of real number arguments with non-zero value of the last (zero-th to the highest order). Number of arguments define the degree of the polynomial. The coefficients of the polynomial can be retrieved and compared to be the same with the values of the passed arguments (in the used order). The polynomial evaluates to the correct value at the given value of the variable (argument). Neither operations (arithmetics) not calling methods changes the coefficients of the polynomial, they also cannot be changed directly by assignment.

**Test steps:** Instantiate a polynomial of a random degree (>= 1) with random values of the coefficients (use mixture of integer and floating point numbers). Store the used random values (coefficients values) in a sequence. Check the degree of the created polynomial - should be length of sequence minus 1. Obtain the coefficients of the polynomial from the generated object, compare them with the reference sequence - values and order must be the same.

Use the generated polynomial as left / right operand in all implemented arithmetic operations. After each performed operation check that the degree and coefficients of the polynomial are preserved. If the operation allows another polynomial as the second operand - check that is not changed either.

Call other defined methods of the polynomial - derivative / antiderivative and convolution - with arbitrary but proper arguments. Check that the polynomial is not changed. In the case of the convolution (argument is also a polynomial) check that the second polynomial is not changed either.

Repeat these steps multiple times (> 10).

**Test result:** PASS / FAIL

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

**Test result:** PASS / FAIL

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

**Test result:** PASS / FAIL

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

**Test goal:** ?

**Expected result:** ?

**Test steps:** ?

**Test result:** PASS / FAIL

___

**Test Identifier:** TEST-T-10B

**Requirement ID(s)**: REQ-AWM-103

**Verification method:** T

**Test goal:** ?

**Expected result:** ?

**Test steps:** ?

**Test result:** PASS / FAIL
___

**Test Identifier:** TEST-T-100

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-102

**Verification method:** T

**Test goal:** ?

**Expected result:** ?

**Test steps:** ?

**Test result:** PASS / FAIL

___
