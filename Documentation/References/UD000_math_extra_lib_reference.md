# Library math_extra_lib Reference

## Scope

This document provides reference information on the libary *math\_extra\_lib*, which includes the following modules:

* *special_functions*
* *polynomial*
* *poly_solver*
* *vector_matrices*
* *matrix_solver*

## Installation

This library can be check-out from the GitHub [repository https://github.com/FooBarShebang/math_extra_lib](https://github.com/FooBarShebang/math_extra_lib). The recommended manner of use is within a *virtual environment*. The recommended location is *Lib/site_packages* within the virtual environments.

**Important**! Do not forget to check-out the dependencies into the same location side by side with *math\_extra\_lib*:

* [introspection_lib](https://github.com/FooBarShebang/introspection_lib)

## Intended Use and Functionality

The purpose of this library is to provide the necessary tools for the numerical methods in the fields related to the *linear algebra*, *statistical analysis*, *regression data fitting* and *signal processing*. This is a *light-weight pure Python code* replacement for NumPy / SciPy in the situations when only a limited, specific functionality is required, and the calculation speed is not an issue.

Furthermore, the library implements vigorous input data sanity checks: the data types and values of the call arguments of functions and methods are checked, and the wrong or unexpected data types or values are rejected by raising custom exceptions from the *introspection\_lib* library. This approach separates **TypeError** and **ValueError** exceptions originating from a bad code (programming error) and custom exceptions of the compatible types originating from the bad data input. Furthermore, these custom exceptions provide the built-in trace analysis and customization options.

The library includes a number of classes and functions implementing the following functionality:

* Special mathematical functions (beta, gamma, standard error function, etc.) commonly used in the statistical analysis (continuous distributions)
* Polynomial evaluation and arithmetics on the field of the *rational* numbers (only integer and floating point types are supported)
* Finding all *complex* roots of a polynomial with the *rational* coefficients
* Polynomial interpolation of a real function of a single real argument (only integer and floating point types are supported)
* Construction of an orthogonal polynomial basis (Legendre, Chebyshev of the first kind, Bernstein)
* Matrix and vectors (row and column) arithmetics on the field of the rational numbers (only integer and floating point types are supported)
* Calculation of the trace, the determinant, the inverse matrix, the LUP and LDUP decomposition, and the *real* eigenvalues / eigenvectors of a square matrix
* Solution of a system of linear equations

This library is not desinged for the symbolic calculations, but to simplify the numerical calculations. For example, using polynomials

```python
from math_extra_lib.polynomial import Polynomial
from math_extra_lib.poly_extra import FindRoots

A = Polynomial(0, 1, 1) #x^2 + x
B = Polynomial(1, 1) #x + 1
C = A + B # (x^2 + x) + (x + 1) = x^2+2x+1 = (x+1)^2
print(C(2)) #evaluates to 9, which value is printed
print(FindRoots(C)) #-1 is a single unique root with multiplicity 2 -> [-1, -1]
```

or using matrices and vectors

```python
from math_extra_lib.vectors_matrices import SquareMatrix, Column

A = SquareMatrix([[1, 1],[-1, 2]])
# ( 1 1)
# (-1 2)
B = Column(1, 1)
C = Column(1, -3)
D = 2 * A * B + C #which is a column vector (5, -1)

print(A.getTrace()) #1 + 2 = 3, which is printed
print(A.getDeterminant()) # 1*2 - (1 * -1) = 3, which is printed
```

Solution of a system of linear equations is also simple

```python
from math_extra_lib.matrix_solver import SolveLinearSystem

# x + 2y = 5
# x -  y = -1

print(SolveLinearSystem([[1, 2], [1, -1]], [5, -1])) #prints [1, 2]
```

Note, that the bound coefficients can also be passed as an instance of **SquareMatrix** class, whereas the free coefficients - as instance of **Column** class.

Polynomial interpolation has simple interface as well

```python
from math_extra_lib.poly_solver import InterpolateLegendre

XGrid = [1, 2, 3]
YGrid = [3, 1, 2]
XYGrid = zip(XGrid, YGrid)

Poly = InterpolateLegendre(XYGrid) #returns an instance of Polynomial class

print(Poly) # 1.5x^2-6.5x+8
print(Poly(0)) # evaluates to 8
print(Poly(1.5)) # evaluates to 1.625
```

## Design and Implementation

The components diagram of the library is shown below.

![Library components](../UML/library_components.png)

Polynomials are implemented as callable and immutable class instances, i.e. the coefficients of a polynomial and its degree are defined during instantiation, and they cannot be changed afterwards. Calling an instance of a **Polynomial** class with a single real number argument evaluates this polynomial at the passed value of the argument. The polynomial class supports addition, subtraction and multiplication operation with both right or left operand being either a real number (integer or floating point) or another polynomial. A polynomial can be raised to a positive integer power and divided by a non-zero real number. The polynomial class also supports floor division and remainder (modulo) of floor division by another polynomial. The augmented assignments are not supported.

Matrices and vectors (generic, column and row vectors) are implemented as immutable class instances, which, however, support a variety of the arithmetic operations with the mixed operands (matrix, vector or real number), but not the augmented assignments. These classes are not callable.

The input data sanity checks raise either **UT\_TypeError** or **UT\_ValueError** defined in the module *base\_exceptions* of the library *introspection\_lib*.

## API Reference

The reference documentation on the specific modules, including design and implementation specifics and API is provided in the separate files - see links below.

* Module [polynomial](./UD001_polynomial_reference.md)
* Module [special_functions](./UD002_special_functions.md)
* Module [vectors_matrices](./UD003_vectors_matrices_reference.md)
* Module [matrix_solver](./UD004_matrix_solver_reference.md)
* Module [poly_solver](./UD005_poly_solver_reference.md)

Note that class **Polynomial** can also be imported from the module *poly\_solver*, whereas the classes **SquareMatrix** and **Column** can also be imported from the module *matrix\_solver*.
