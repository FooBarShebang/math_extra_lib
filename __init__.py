#!/usr/bin/python3
"""
Library math_extra_lib

Implements the necessary tools for the numerical methods in the fields related
to the linear algebra, statistical analysis, regression data fitting and
signal processing.

Modules:
    polynomial: Implements Polynomial class, which supports various arithmetic
        operations and is callable, i.e. it can be evaluated at specific value
        of its argument. Also implementes RationalFunction class required for
        calculation or approximation of several special functions.
    special_functions: Implements a number of special mathematical functions on
        the field of real numbers.
    vectors_matrices: Implements matrices, generic vectors, column and row
        vectors as well as arithmetics involving instances of these classes and
        real number as operands.
    matrix_solver: Implements power iteration method for finding a single
        dominant eigenvalue of a square matrix and solution of a system of
        linear equations.
    poly_solver: Implements finding all complex roots of a real coefficients
        polynomial, generation of Lagrange, Legendre, Chebyshev and Bernstein
        polynomials, and interpolation of univariate real functions using these
        polynomials.
"""

__project__ = 'Linear algebra, special functions, polynomial interpolation'
__version_info__= (1, 0, 0)
__version_suffix__= '-rc1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '29-02-2024'
__status__ = 'Production'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['polynomial', 'special_functions', 'vectors_matrices',
            'matrix_solver', 'poly_solver']