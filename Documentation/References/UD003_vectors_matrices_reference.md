# Module math_extra_lib.vectors_matrices Reference

## Scope

This document describes the intended usage, design and implementation of the functionality implemented in the module **vectors_matrices** of the library **math\_extra\_lib**. The API reference is also provided.

The functional objects covered in this document are:

* class **Array2D**
* class **Vector**
* class **Column**
* class **Row**
* class **Matrix**
* class **SquareMatrix**

## Intended Use and Functionality

The purpose of this module is to provide classes implementing the fundamentals of the linear algebra (see [design document](../Design/DE003_vectors_matrices.md)): vectors and matrices as well as arithmetic operations between them and real numbers, as given in the table below. Concerning the vectors there are three distinct classes: (generic) **Vector**, **Column** (vector) and **Row** (vector). The generic vector class has nothing to do with matrices. It impements an abstract mathematical concept of a vector as a tuple of real value numbers with the addition (and subtraction) operation between vectors as well as product with (and division by) a scalar value - i.e. *vector space*. This class serves as the prototype / base class for the column and row vectors; it can also be used as the base class for the implementation of the *geometric vectors* in the analitical geometry. Furthermore, it supports *dot product* (inner) and *matrix product* (outer) between to vectors. The row and column vectors are specialized sub-classes, which can be used in the multiplication operation with matrices. Neither row nor column vectors support dot and matrix product between instances of the same class, however, a row vector by a column vector product is supported (as a dot product resulting in a scalar value) as well as a column vector by a row vector product (as an outer product resulting in a matrix). The **Array2D** class serves as a base class for matrices, but it is not a matrix itself, simply a 2-dimensional array of real value numbers; it is used directly only as the result of the outer product of two generic vectors. The **SquareMatrix** sub-classes **Matrix** class specifically for the matrices with the equal width and height, which have additional properties (as mathematical objects) and methods. Thus, a generic matric with equal width and height produced as a result of an arithmetic operation is always converted into an instance of **SquareMatrix**, except for the result of the column by row vectors production, which is a singular matrix even if it is square, thus the added functionality is meaningless.

The supported arithmetics operations between the different data types / classes are listed in the table below. Since these operations are defined via arithmetic operations applied to the elements of the vectors and matrices, specific limitation is applied - equality of the number of elements (size) of the both operands envolved in the operation. All vectors are characterized by a single *Size* (abbreviated to *S*), which is the number of elements. Generic matrices are characterized by both *Width* (number of columns, *W*) and *Height* (number of rows, *H*), whereas for the square matrices width equals height, thus it can be replaced by a single *Size* value (size = number of columns = number of rows, *S*).

| Operation                   | Requirements / Limitations | Result       |
| --------------------------- | -------------------------- | ------------ |
| Vector + Vector             | S1 = S2                    | Vector       |
| Vector - Vector             | S1 = S2                    | Vector       |
| Vector * scalar             | N.A.                       | Vector       |
| scalar * Vector             | N.A.                       | Vector       |
| Vector / scalar             | scalar <> 0                | Vector       |
| Vector * Vector             | S1 = S2                    | scalar       |
| Vector @ Vector             | N. A.                      | Array2D      |
| Column + Column             | S1 = S2                    | Column       |
| Column - Column             | S1 = S2                    | Column       |
| Column * scalar             | N.A.                       | Column       |
| scalar * Column             | N.A.                       | Column       |
| Column / scalar             | scalar <> 0                | Column       |
| Row * Column                | S1 = S2                    | scalar       |
| Column * Row                | N.A.                       | Matrix       |
| Row + Row                   | S1 = S2                    | Row          |
| Row - Row                   | S1 = S2                    | Row          |
| scalar * Row                | N.A.                       | Row          |
| Row * scalar                | N.A.                       | Row          |
| Row / scalar                | scalar <> 0                | Row          |
| Matrix + Matrix             | W1 = W2 and H1 = H2        | Matrix       |
| Matrix + SquareMatrix       | W1 = H1 = S2               | SquareMatrix |
| SquareMatrix + Matrix       | S1 = W2 = H2               | SquareMatrix |
| Matrix - Matrix             | W1 = W2 and H1 = H2        | Matrix       |
| Matrix - SquareMatrix       | W1 = H1 = S2               | SquareMatrix |
| SquareMatrix - Matrix       | S1 = W2 = H2               | SquareMatrix |
| scalar * Matrix             | N.A.                       | Matrix       |
| Matrix * scalar             | N.A.                       | Matrix       |
| Matrix / scalar             | scalar <> 0                | Matrix       |
| Matrix * Column             | W1 = S2                    | Column       |
| Row * Matrix                | S1 = H2                    | Row          |
| Matrix * Matrix             | W1 = H2 AND H1 <> W1       | Matrix       |
| Matrix * Matrix             | W1 = H2 AND H1 = W1        | SquareMatrix |
| Matrix * SquareMatrix       | W1 = S2 AND H1 <> S2       | Matrix       |
| Matrix * SquareMatrix       | W1 = S2 AND H1 = S2        | SquareMatrix |
| SquareMatrix * Matrix       | S1 = H2 AND S1 <> W2       | Matrix       |
| SquareMatrix * Matrix       | S1 = H2 AND S1 = W2        | SquareMatrix |
| SquareMatrix + SquareMatrix | S1 = S2                    | SquareMatrix |
| SquareMatrix - SquareMatrix | S1 = S2                    | SquareMatrix |
| SquareMatrix * scalar       | N.A.                       | SquareMatrix |
| scalar * SquareMatrix       | N.A.                       | SquareMatrix |
| SquareMatrix / scalar       | scalar <> 0                | SquareMatrix |
| SquareMatrix * Column       | S1 = S2                    | Column       |
| Row * SquareMatrix          | S1 = S2                    | Row          |

**Note** that vectors and matrices objects are designed to be immutable, therefore the *augmented assignement* (like `+=`, `*=`, etc.) is not supported; furthermore a sub-class of **TypeError** is raised in response to an attempted augmented asignment.

The **Vector**, **Column** and **Row** classes must be instantiated with two or more real number value arguments, with the number of the arguments defining the *size* (number of elements) of the respective vector. After instantiation these objects can be used in the standard Python mathematical expressions as given in the table above.

```python
Column1 = Column(1, 2, 3) #size is 3

Column2 = Column(4, 5, 6) #size is 3

Column3 = Column1 + Column2 # (5, 7, 9)

Column3 = Column2 - Column1 # (3, 3, 3)

Column3 = 2 * Column1 + Column3 / 2 # (4, 6.5, 9)
```

Vector classes are designed to be *immutable* and *atomic* objects, and not a specialized sequence. Therefore, neither *iteration* (as `for element in vector`) nor *contains check* (as `if element in vector`) are supported; also the values of the elements can not be changed after instantiation. However, the value if any stored element can be read-out (accessed) using the standard index notation (starting from index 0), as `Column1[1]` in the example above results in the value of 2. Slice notation is not supported. Also, all stored elements can be read-accessed at once via the read-only property *Data*, which returns a list containg the copies of the vector's elements values.

Additionally, instances of these classes can generate *normalized* vectors parallel to themselves, i.e. $\mathbf{x} \rightarrow \tilde{\mathbf{x}} = \frac{\mathbf{x}}{|\mathbf{x}|}$, where the *norm* of a vector $|\mathbf{x}| = \sqrt{\sum_i{x_i^2}}$ is the generalized *geometric (Euclidean) length* of the vector in N-dimensional space. The classes themselves provide *class methods* to generate *orthonormal basis*, specifically - vectors with zero value of all elements but one, and 1 as the value of a single element at the specified index.

The column and row vector class instances also support *transposition* operation, which transforms a column into a row and vice verse preserving the order and values of the elements.

The **Matrix** and **SquareMatrix** classes must be instantiated with a mandatory sequence argument, which can be either a flat sequence of integers or floating point numbers, or a (nested) sequence of same length (sub-) sequences of integers or floating point numbers.

In the first case, the matrix dimensions must be provided explicitely for a generic matrix using two keyword arguments *Width* and *Height* - if only one value is specified, the second value is determined automatically as the result of the floor division of the size of the sequence by the specified dimension. For a square matrix the size (width = height) can be determined automatically as rounding down the square root of the length of the passed sequence, or it can be specified explicitely using the keyword argument *Size*. The following rules are applied:

* Any specified dimension must be an integer >= 2
* The product of width x height (or size^2) cannot exceed the length of the passed sequence
* Only the first width x height elements of the passed sequence are used, the tailing rest of the elements is ignored

In the second case all sub-sequences must be of the same length, which defines one of the dimensions, whereas the number of the sub-sequences define the second; for a square matrix the number of sub-sequences must be equal to the length of a sub-sequence.

In the both cases the matrix' content is filled in the column-first order by default. This behaviour can be changed using a keyword argument *isColumnFirst* = **False**, in which case the row-first order is applied.

After instantiation these objects can be used in the standard Python mathematical expressions as given in the table above.

```python
Column1 = Column(1, 2, 3) #size is 3

Row1 = Row(1, 2) #size is 2

Matrix1 = Matrix([[1, 2], [3, 4], [5, 6]]) #size is 3(W) x 2(H)

Square1 = SquareMatrix([1, 2, 3, 4]) #size is 2 x 2, as [[1, 2], [3, 4]]

Column2 = Matrix1 * Column1 # result is a column of size 2

Row2 = Row1 * Matrix1 # result is a row of size 3

Martrix2 = Square1 * Matrix1 #result is a matrix of size 3(W) x 2(H)
```

Matrix classes are designed to be *immutable* and *atomic* objects, and not a specialized sequence. Therefore, neither *iteration* (as `for element in vector`) nor *contains check* (as `if element in vector`) are supported; also the values of the elements can not be changed after instantiation. However, the value if any stored element can be read-out (accessed) using the double index notation (starting from index 0), as `Matrix1[1, 1]` in the example above results in the value of 4. Slice notation is not supported, nor the standard single index notation; instead the classes provide methods to access a single row or column as instances of the respective vector classes. Also, all stored elements can be read-accessed at once via the read-only property *Data*, which returns a list of lists containg the copies of the matrix' elements values, and always in the column-first order.

The both matrix classes support transposition method, which returns a new instance of the same class.

The **SquareMatrix** class also implements a number of additional methods:

* class method *generateIdentity*(), which generates an identity matrix of the specified size
* class method *generatePermutation*(), which generates orthogonal permutation matrix (columns / rows pivoted identity matrix) from a provided permutation of the [1..N] set, passed a sequence
* class method *generateDiagonal*(), which generates a diagonal matrix with the elements on the main diagonal defined by the passed sequence argument
* method *getTrace*(), which calculates the trace of the matrix - sum of all elements on the main diagonal
* method *getLUPdecomposition*(), which calculates decomposition of a matrix into a product of column permutation matrix, lower triangular matrix with all elements at the main diagonal being 1, upper triangular matrix (or row echelon for a singular matrix) and rows permutation matrix
* method *getFullDecomposition*(), which calculates decomposition of a matrix into a product of column permutation matrix, lower triangular matrix with all elements at the main diagonal being 1, upper triangular matrix with all elements at the main diagonal being 1, a diagonal matrix (unless original matrix is singular) and rows permutation matrix
* method *getDeterminant*(), which calculates the determinant of the matrix
* method *getInverse*(), which calculates the multiplicative reciprocal (inverse) matrix for a non-singular matrix
* method *getEigenValues*(), which calculates all eigenvalues of a *diagonalizable* matrix
* method *getEigenVectors*(), which can calculate all eigenvalues and associated orthonormal base eigenvectors for a diagonalizable matrix; or just the orthonormal base eigenvectors for a given eigenvalue, which works also for the *defective* (not diagonalizable) matrices

## Design and Implementation

The class diagram of the module is given below.

![Class diagram](..\UML\vectors_matrices\vectors_matrices_classes.png)

The immutability of the vectors and matrices classes is achieved by combining the following techniques:

* The parent classes **Vector** and **Array2D** are nor derived from any standard Python sequence type, nor from the respective ABC, instead they are implemented as general classes, which include instance of tuple / nested tuple to store the actual data as an instance attribute (field) *\_Elements*
* The said field *\_Elements* is interfaced by a *read-only* property *Data*, which returns a copy of the stored data, not a reference to the same object
* The single underscore prefix naming convention only indicates that the field is designed to be treated as a *private* attribute, but does not provide a true *encapsulation*. However, this field is itself a (nested) immutable sequence, which elements cannot be changed. The field can be still re-referenced (re-assigned) to a different object, which cannot be prevented without mingling with the attribute resolution scheme
* Only the read-only indexing elements access method *\_\_getitem\_\_*() is implemented, but not the modification methods *\_\_setitem\_\_*() and *\_\_delitem\_\_*(), which are not present in a general class by default
* The Python data model and methods resolution automatically implements augmented assignments like `+=`, etc. if the respective binary operation is implemented. In order to negate this default behaviour the special methods hooking augmented assignments `+=`, `-=`, `*=` and `/=` (i.e., *\_\_iadd\_\_*(), etc.) are implemented explicititely. These methods simply raise an exception sub-classing the standard **TypeError**

Neither iterator nor membership check protocol special methods *\_\_iter\_\_*() and *\_\_contains\_\_*() are implemented by default in a general class. However, the standard Python method resolution scheme provides a fallback for the not implemented membership check protocol via the iterator protocol, which is the [documented default behaviour](https://docs.python.org/3/reference/datamodel.html). However, there is also *not documented* fallback for the iterator protocol as well, if the class implements indexing element access: basically, the index is incremented from zero untill **IndexError** exception is raised. Therefore, the *\_\_iter\_\_*() method is explicitely implemented to raise sub-class of **TypeError** exception.

The special methods implementing the arithmetical operations (like *\_\_add\_\_*(), etc.) rely heavily on the 'IS A' type checking in order to: A) ensure that only allowed data types / classes can be used as the second operand - sub-class of **TypeError** exception, B) properly choose the calculation method and the result data type / class depending on the type / class of the second operand, C) avoid circular referencing or referencing a not yet defined class.

The last functionality is achieved by exploiting the Python method resolution model. Basically, the statement `A+B` is resolved into the method call `A.__add__(B)`; however if the **NotImplemented** value is returned, another method call is made `B.__radd__(A)`. For example, the left and the right multiplication of a column / row vector by a scalar is implemented already in the parent **Vector** class' methods *\_\_mul\_\_*() and *\_\_rmul\_\_*(), but it is re-defined (implemented) separately in the classes **Column** and **Row** because of the different set of the allowed second operand types. Yet, the row x matrix and matrix x column multiplication is not implemented in these classes, but delegated to the **Matrix** class using the described **NotImplemented** fallback behaviour.

The second exploit is the 'class patching'. For instance, column x row vectors product results in a matrix, which is defined later in the source code, thus it cannot be used as a return data type yet. Similarly, the matrix x matrix product's result should be converted into a square matrix object when possible, yet the square matrix class is not yet defined. The solution is to implement the functionality in a two-parameters function after definition of all involved classes, then convert this function into a *method* and assign to the respective class attribute, previously declared as a special method.

## API Reference

### Class Array2D

### Class Vector

### Class Column

### Class Row

### Class Matrix

### Class SquareMatrix
