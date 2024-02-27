# Module math_extra_lib.special_functions Reference

## Scope

This document describes the intended usage, design and implementation of the functionality implemented in the module **poly_solver** of the library **math\_extra\__lib**. The API reference is also provided.

The concerted functional elements are functions:

* *FindRoots*
* *GetLagrangePolynomial*
* *GetLagrangeBasis*
* *InterpolateLagrange*
* *GetLegendrePolynomial*
* *GetLegendreBasis*
* *InterpolateLegendre*
* *GetChebyshevPolynomial*
* *GetChebyshevBasis*
* *InterpolateChebyshev*
* *GetBernsteinPolynomial*
* *GetBernsteinBasis*
* *InterpolateBernstein*

## Intended Use and Functionality

The main purpose of this module is to enable:

* Calculation of the (complex) roots of an arbitrary polynomial with real coefficients, and
* Polynomial interpolation of a univariate function on the real numbers field

## Design and Implementation

![Library components](..\UML\poly_solver\poly_solver_components.png)

## API Reference

### Functions

**FindRoots**(Poly)

*Signature*:

Polynomial -> list(int OR float OR complex)

*Args*:

*Poly*: **Polynomial**; instance of the class, the polynomial, which roots are to be found

*Returns*:

**list**(**int** OR **float** OR **complex**): the found roots of the polynomial

*Raises*:

**UT_TypeError**: argument is not an instance of Polynomial class

*Description*:

Calculates all roots of a polynomial passed as an instance of **Polynomial** class using Alberth method, and returns them as a list of real or complex numbers. Each root with multiplicity K is included exactly K times; thus for a polynomial of the degree N the length of the list is exactly N.

**GetLagrangePolynomial**(Node, Roots)

*Signature*:

int OR float, seq(int OR float) -> Polynomial

*Args*:

* *Node*: **int** OR **float**; the x-value, at which the polynomial evaluates to 1
* *Roots*: **seq**(**int** OR **float**); sequence of real numbers (x-values), at which the polynomial evaluates to 0

*Returns*:

**Polynomial**: instance of, a polynomial of degree N, where N is the number of the roots

*Raises*:

* **UT_TypeError**: the first argument is not a real number, OR the second argument is not a sequence of real numbers
* **UT_ValueError**: roots sequence is empty, OR it contains, at least, 2 equal elements

*Description*:

Calculates a single base Lagrange polynomial, which evaluates to 1 at the provided node x-value and to 0 at all passed N roots (x-values).

**GetLagrangeBasis**(XGrid)

*Signature*:

seq(int OR float) -> list(Polynomial)

*Args*:

*XGrid*: **seq**(**int** OR **float**); sequence of unique real numbers

*Returns*:

**list**(**Polynomial**): list of N instances of Polynomial class - the base Lagrange polynomials - each of the degree N-1, where N is the number of points

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence of real numbers
* **UT_ValueError**: the passed sequence contains less than 2 elements, OR, at least, two elements are equal

*Description*:

Calculates N base Lagrange base polynomials of the degree N-1 for the passed N unique x-values (nodes).

**InterpolateLagrange**(XYGrid)

*Signature*:

seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float

*Args*:

*XYGrid*: **seq**(**seq**(**int** OR **float**, **int** OR **float**)); a sequence of 2-elements sub-sequences of real numbers, representing the X-Y values pairs of the function to be interpolated

*Returns*:

* **Polynomial**: instance of, interpolating polynomial of degree 1 or higher
* **int** OR **float**: interpolating function is constant (0-th degree)

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a sequence (nested) of real numbers (int or float), OR a length of any of the sub-sequence is not 2
* **UT_ValueError**: the passed argument is empty or contains only 1 element, OR any of the X values is not unique (first element of the sub-sequences)

*Description*:

Calculates an interpolatig polynomial of degree <= N - 1, where N is the number of (X,Y) data points provided. The calculated polynomial goes (almost) exactly through each of the provided data points. A constant function (0-th degree polynomial) is represented by a real number, higher degrees - by an instance of the **math\_extra\_lib.polynomial.Polynomial** class. Lagrange polynomial basis is used in the calculations.

**GetLegendrePolynomial**(Degree)

*Signature*:

int >= 0 -> Polynomial OR int

*Args*:

*Degree*: **int** >= 0; the requested degree of the polynomial

*Returns*:

* **Polynomial**: instance of, degree > 0
* **int**: value = 1, degree is 0

*Raises*:

* **UT_TypeError**: the passed argument is not an integer number
* **UT_ValueError**: the passed argument is a negative integer number

*Description*:

Calculates a single Legendre polynomial of degree N >= 0.

**GetLegendreBasis**(Degree)

*Signature*:

int >= 0 -> list(Polynomial OR int)

*Args*:

*Degree*: **int** >= 0; the requested degree of the basis

*Returns*:

**list**(**Polynomial** OR **int**): the basis, where the first element is always 1, and each subsequent element is an instance of polynomial class of the degree equal to the element index

*Raises*:

* **UT_TypeError**: the passed argument is not an integer number
* **UT_ValueError**: the passed argument is a negative integer number

*Description*:

Calculates a complete Legendre polynomial base of degree N >= 0.

**InterpolateLegendre**(XYGrid)

*Signature*:

seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float

*Args*:

*XYGrid*: **seq**(**seq**(**int** OR **float**, **int** OR **float**)); a sequence of 2-elements sub-sequences of real numbers, representing the X-Y values pairs of the function to be interpolated

*Returns*:

* **Polynomial**: instance of, interpolating polynomial of degree 1 or higher
* **int** OR **float**: interpolating function is constant (0-th degree)

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a sequence (nested) of real numbers (int or float), OR a length of any of the sub-sequence is not 2
* **UT_ValueError**: the passed argument is empty or contains only 1 element, OR any of the X values is not unique (first element of the sub-sequences)

*Description*:

Calculates an interpolatig polynomial of degree <= N - 1, where N is the number of (X,Y) data points provided. The calculated polynomial goes (almost) exactly through each of the provided data points. A constant function (0-th degree polynomial) is represented by a real number, higher degrees - by an instance of the **math\_extra\_lib.polynomial.Polynomial** class. Legendre polynomial basis is used in the calculations.

**GetChebyshevPolynomial**(Degree)

*Signature*:

int >= 0 -> Polynomial OR int

*Args*:

*Degree*: **int** >= 0; the requested degree of the basis

*Returns*:

* **Polynomial**: instance of, degree > 0
* **int**: value = 1, degree is 0

*Raises*:

* **UT_TypeError**: the passed argument is not an integer number
* **UT_ValueError**: the passed argument is a negative integer number

*Description*:

Calculates a single Chebyshev polynomial (of the 1st kind) of degree N >= 0.

**GetChebyshevBasis**(Degree)

*Signature*:

int >= 0 -> list(Polynomial OR int)

*Args*:

*Degree*: **int** >= 0; the requested degree of the basis

*Returns*:

**list**(**Polynomial** OR **int**): the basis, where the first element is always 1, and each subsequent element is an instance of polynomial class of the degree equal to the element index

*Raises*:

* **UT_TypeError**: the passed argument is not an integer number
* **UT_ValueError**: the passed argument is a negative integer number

*Description*:

Calculates a complete Chebyshev polynomial base of degree N >= 0 (of the 1st kind).

**InterpolateChebyshev**(XYGrid)

*Signature*:

seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float

*Args*:

*XYGrid*: **seq**(**seq**(**int** OR **float**, **int** OR **float**)); a sequence of 2-elements sub-sequences of real numbers, representing the X-Y values pairs of the function to be interpolated

*Returns*:

* **Polynomial**: instance of, interpolating polynomial of degree 1 or higher
* **int** OR **float**: interpolating function is constant (0-th degree)

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a sequence (nested) of real numbers (int or float), OR a length of any of the sub-sequence is not 2
* **UT_ValueError**: the passed argument is empty or contains only 1 element, OR any of the X values is not unique (first element of the sub-sequences)

*Description*:

Calculates an interpolatig polynomial of degree <= N - 1, where N is the number of (X,Y) data points provided. The calculated polynomial goes (almost) exactly through each of the provided data points. A constant function (0-th degree polynomial) is represented by a real number, higher degrees - by an instance of the **math\_extra\_lib.polynomial.Polynomial** class. Chebyshev polynomial basis (of the first kind) is used in the calculations.

**GetBernsteinPolynomial**(Degree, Index)

*Signature*:

int >= 0, int >= 0 -> Polynomial OR int

*Args*:

*Degree*: **int** >= 0; the requested degree of the polynomial (basis degree)
*Index*: **int** >= 0; the requested index of the polynomial whithin the basis

*Returns*:

* **Polynomial**: instance of, degree > 0
* **int**: value = 1, degree is 0

*Raises*:

* **UT_TypeError**: the first passed argument is not an integer number, OR the second passed argument is not an integer number
* **UT_ValueError**: the first passed argument is a negative integer number, OR the second passed argument is not an integer number, OR the second argument is larger than the first

*Description*:

Calculates a single Bernstein polynomial of degree N >= 0 and index K, where 0 <= K <= N.

**GetBernsteinBasis**(Degree)

*Signature*:

int >= 0 -> list(Polynomial) OR list(int)

*Args*:

*Degree*: **int** >= 0; the requested degree of the basis

*Returns*:

**list**(**Polynomial** OR **int**): the basis, for the *Degree* = 0 it is [1], otherwise it contains N = *Degree* **Polynomial**-class instances, each being a polynomial of degree = *Degree*

*Raises*:

* **UT_TypeError**: the passed argument is not an integer number
* **UT_ValueError**: the passed argument is a negative integer number

*Description*:

Calculates a complete Bernstein polynomial base of degree N >= 0.

**InterpolateBernstein**(XYGrid)

*Signature*:

seq(seq(int OR float, int OR float)) -> Polynomial OR int OR float

*Args*:

*XYGrid*: **seq**(**seq**(**int** OR **float**, **int** OR **float**)); a sequence of 2-elements sub-sequences of real numbers, representing the X-Y values pairs of the function to be interpolated

*Returns*:

* **Polynomial**: instance of, interpolating polynomial of degree 1 or higher
* **int** OR **float**: interpolating function is constant (0-th degree)

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a sequence (nested) of real numbers (int or float), OR a length of any of the sub-sequence is not 2
* **UT_ValueError**: the passed argument is empty or contains only 1 element, OR any of the X values is not unique (first element of the sub-sequences)

*Description*:

Calculates an interpolatig polynomial of degree <= N - 1, where N is the number of (X,Y) data points provided. The calculated polynomial goes (almost) exactly through each of the provided data points. A constant function (0-th degree polynomial) is represented by a real number, higher degrees - by an instance of the **math\_extra\_lib.polynomial.Polynomial** class. Legendre polynomial basis is used in the calculations.
