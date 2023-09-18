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

The purpose of this module is to provide classes implementing the fundamentals of the linear algebra: vectors and matrices as well as arithmetic operations between them and real numbers, as given in the table below. Concerning the vectors there are three distinct classes: (generic) **Vector**, **Column** (vector) and **Row** (vector). The generic vector class has nothing to do with matrices. It impements an abstract mathematical concept of a vector as a tuple of real value numbers with the addition (and subtraction) operation between vectors as well as product with (and division by) a scalar value - i.e. *vector space*. This class serves as the prototype / base class for the column and row vectors; it can also be used as the base class for the implementation of the *geometric vectors* in the analitical geometry. Furthermore, it supports *dot product* (inner) and *matrix product* (outer) between to vectors. The row and column vectors are specialized sub-classes, which can be used in the multiplication operation with matrices. Neither row nor column vectors support dot and matrix product between instances of the same class, however, a row vector by a column vector product is supported (as a dot product resulting in a scalar value) as well as a column vector by a row vector product (as an outer product resulting in a matrix). The **Array2D** class serves as a base class for matrices, but it is not a matrix itself, simply a 2-dimensional array of real value numbers; it is used directly only as the result of the outer product of two generic vectors. The **SquareMatrix** sub-classes **Matrix** class specifically for the matrices with the equal width and height, which have additional properties (as mathematical objects) and methods. Thus, a generic matric with equal width and height produced as a result of an arithmetic operation is always converted into an instance of **SquareMatrix**, except for the result of the column by row vectors production, which is a singular matrix even if it is square, thus the added functionality is meaningless.

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

Vector classes are designed to be *immutable* and *atomic* objects, and not a specialized sequence. Therefore, neither *iteration* (as `for element in vector`) nor *contains check* (as `if element in vector`) are supported; neither the values of the elements can be changed after instantiation. However, the value if any stored element can be read-out (accessed) using the standard index notation (starting from index 0), as `Column1[1]` in the example above results in the value of 2. Slice notation is not supported. Also, all stored elements can be read-accessed at once via the read-only property *Data*, which returns a list containg the copies of the vector's elements values.

Additionally, instances of these classes can generate *normalized* vectors parallel to themselves, i.e. $\mathbf{x} \rightarrow \tilde{\mathbf{x}} = \frac{\mathbf{x}}{|\mathbf{x}|}$, where the *norm* of a vector $|\mathbf{x}| = \sqrt{\sum_i{x_i^2}}$ is the generalized *geometric (Eucledian) length* of the vector in N-dimensional space. The classes themselves provide *class methods* to generate *orthonormal basis*, specifically - vectors with zero value of all elements but one, and 1 as the value of a single element at the specified index.

The column and row vector class instances also support *transposition* operation, which transforms a column into a row and vice verse preserving the order and values of the elements.

## Design and Implementation

![Class diagram](..\UML\vectors_matrices\vectors_matrices_classes.png)

## API Reference

### Class Array2D

### Class Vector

### Class Column

### Class Row

### Class Matrix

### Class SquareMatrix
