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

In the both cases the matrix' content is filled in the rows-first order by default. This behaviour can be changed using a keyword argument *isColumnFirst* = **True**, in which case the columns-first order is applied. The rows-first order is chosen for the convenience: in the Indo-European languages ones writes (and reads) a line from left to right and stacks the lines vertically from top to bottom. The same convention is applied to the indexing of the elements of a matrix: the element $a_{i,j}$ of a matrix **A** is at the intersection of the *i*-th column and *j*-th row.

The example below illustrates the rows-first and columns-first ordering:

```python
A = Matrix([[1, 2, 3], [4, 5, 6]]) #rows-first order by the default

B = Matrix([[1, 2, 3], [4, 5, 6]], isColumnsFirst = True) #columns-first order
```

The created matrices are:

$$
\mathbf{A} = \begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6 \\
\end{bmatrix} \; \mathbf{B} = \begin{bmatrix}
1 & 4 \\
2 & 5 \\
3 & 6 \\
\end{bmatrix}
$$

After instantiation these objects can be used in the standard Python mathematical expressions as given in the table above.

```python
Column1 = Column(1, 2, 3) #size is 3

Row1 = Row(1, 2) #size is 2

Matrix1 = Matrix([[1, 3, 5], [2, 4, 6]]) #size is 3(W) x 2(H)

Square1 = SquareMatrix([1, 2, 3, 4]) #size is 2 x 2, as [[1, 2], [3, 4]]

Column2 = Matrix1 * Column1 # result is a column of size 2

Row2 = Row1 * Matrix1 # result is a row of size 3

Martrix2 = Square1 * Matrix1 #result is a matrix of size 3(W) x 2(H)
```

Matrix classes are designed to be *immutable* and *atomic* objects, and not a specialized sequence. Therefore, neither *iteration* (as `for element in matrix`) nor *contains check* (as `if element in matrix`) are supported; also the values of the elements can not be changed after instantiation. However, the value of any stored element can be read-out (accessed) using the double index notation \[column_index, row_index\] (starting from index 0 - programming convention, not the mathematical convention with the starting index 1). For instace, `Matrix1[1, 1]` in the example above results in the value of 4. Slice notation is not supported, nor the standard single index notation; instead the classes provide methods to access a single row or column as instances of the respective vector classes. Also, all stored elements can be read-accessed at once via the read-only property *Data*, which returns a list of lists containg the copies of the matrix' elements values, and always in the rows-first order.

Hence, the element $a_{i,j}$ of a matrix **A** represented by an object (class instance) *A* can be accessed as:

* *A*\[*i*-1, *j*-1\]
* *A.Data*\[*j*-1\]\[*i*-1\]
* *A.getColumn*(*i*-1)\[*j*-1\]
* *A.getRow*(*j*-1)\[*i*-1\]

The both matrix classes support transposition method, which returns a new instance of the same class. Basically, this method simply wraps the class instantiation method into which the stored data content (elements) of the current instance is passed, which is stored internally always in the rows-first order, with the explicit switch (keyword argument) *isColumnFirst* = **True**. Thus, an N x M matrix transposed is an M x N matrix, with all columns becoming rows and vice versa, whilst preserving the oder, i.e. $\mathbf{A} \; \rightarrow \; \mathbf{B} = \mathbf{A}^T\; : b_{j,i} = a_{i,j} \; \forall \; 1 \leq i \leq N, \; 1 \leq j \leq M$. In the case of a square matrix the transposition can be visialized as a rotation (flipping) along the main diagonal.

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

A *diagonal* square matrix **D** has non-zero elements only on the main diagonal (i.e. elements with the equal values of the column and the row indexes $d_{i,i}$), whereas all elements not on the main diagonal are strictly zeroes $d_{i, j \neq i}=0$. Thus, to define such a matrix (N x N) one needs only a flat sequence of N values. The *determinant* of any diagonal matrix is the product of all its main diagonal elements $\mathtt{det}(\mathbf{D}) = \prod_{i=1}^N{d_{i,i}}$.

The *identity* matrix **I** is a special case of a diagonal matrix with all main diagonal elements being 1, i.e. $i_{j,j} = 1, \; i_{j, k \neq j} = 0 \; \forall 1 \leq j \leq N$, which has a special property $\mathbf{I} * \mathbf{A} = \mathbf{A} * \mathbf{I} = \mathbf{A}$ for any square matrix **A** of the same size *N*. Such a matrix is fully defined by the size only. Obviously, $\mathtt{det}(\mathbf{I}) = 1$.

An *inverse* of a (square) matrix **A** is a (square) matrix $\mathbf{A}^{-1}$, such that $\mathbf{A}^{-1} * \mathbf{A} = \mathbf{A} * \mathbf{A}^{-1} = \mathbf{I}$. Note, that not all square matrices have an inverse, but only those with the non-zero determinant.

A *permutation* of a set (collection of unique items) is a set of the same size produced by reordering of its elements, i.e. a set \{ 2, 1, 3\} is a permutation of the set \{ 1, 2, 3 \} (a.k.a. 1 .. 3 set). A *permutation matrix* **P** of a size *N* is defined by a permutation of 1..*N* set as follows: the value $1 \leq j \leq N$ at the position $1 \leq i \leq N$ in the set permutation means that the *i*-th row of the matrix **P** has non-zero (actually 1) value only at the intersection with the *j*-th column, whereas all other elements of this row are zeroes. Thus, a set permutation \{3, 1, 2\} defines the permutation matrix

$$
\begin{bmatrix}
0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 1 & 0 \\
\end{bmatrix}
$$

In a permutation matrix each column and each row has only one element with the value of 1 and all other elements are of the value 0. A permutation matrix is *orthogonal*, i.e. $\mathbf{P}^{-1} = \mathbf{P}^T$, and $\mathtt{det}(\mathbf{P}) = \pm 1$. Basically, a permutation matrix is an identity matrix with two to more columns (or rows) being swapped (pivoted). The left multiplication of a matrix **A** by a permutation matrix (**P \* A**) swaps the rows of the matrix **A**, whereas the right multiplication (**A \* P**) swaps the columns of the matrix **A**. Basically, if *i*-th row of the matrix P has non-zero element at the position *j*, then the *i*-th row of the product (**P \* A**) is $[a_{1,j}, a_{2,j}, \dots, a_{N,j}]$, which is the *j*-th row of the matrix **A**. On the other hand, the *j*-th column of the matrix **P** has non-zero element at the position *i*, then the *j*-th column of the product (**A \* P**) is $[a_{i,1}, a_{i,2}, \dots, a_{i,N}]^T$, which is the *i*-th column of the matrix **A**.

A *lower-triangular* matrix **L** has all strictly zero elements above the main diagonal, i.e. $l_{i,j>i} = 0$. An *upper-triangular* matrix **U** has all strictly zero elements below the main diagonal, i.e. $u_{i,j<i} = 0$. In the both cases the determinant is the product of all main diagonal elements, i.e. $\mathtt{det}(\mathbf{L}) = \prod_{i=1}^N{l_{i,i}}$ and $\mathtt{det}(\mathbf{U}) = \prod_{i=1}^N{u_{i,i}}$. The *LU-decomposition* of a matrix **A** is a process of finding a lower-triangular matrix **L** and an upper-triangular matrix **U** such that **A** = **L** \* **U**. In practice, considering the numerical stability and singular matrices (det(**A**) =0), the columns and rows pivoting is applied, i.e. $\mathbf{A} \; \rightarrow \; \mathbf{B} = \mathbf{P}_r * \mathbf{A} * \mathbf{P}_c \; : \; \mathbf{B} = \mathbf{L} * \mathbf{U}$, hence a matrix **A** can be decomposed into a product of permutation matrices, lower- and upper-triangular matrices, which generalized decomposition process is named *LUP-decomposition*. If the process results in all unity main diagonal elements of the lower-diagonal matrix $l_{i,i}=1 \; \forall \; i$, the determinant of the matrix **A** is $\mathtt{det}(\mathbf{A}) = \pm \mathtt{det}(\mathbf{U}) = \pm \prod_{i=1}^N{u_{i,i}}$, with the sign defined by the product of the determinants of the both permutation matrices, which is the product of the signs of the both column and row permutations. Thus, LUP-decomposition is a powerful technique for calculation of the determinant and solution of a system of linear equations (using back-substitution method).

The produced in the process upper-triangular matrix **U** can be decomposed further into a product of a diagonal matrix **D** and another upper-triangular matrix $\hat{\mathbf{U}} \; : \; \hat{u}_{i,i} = 1$ with all main diagonal elements being equal to 1, i.e. $\mathbf{U} = \hat{\mathbf{U}} * \mathbf{D}$. Thus, the *full decomposition* of a matrix **A** is its representation as a product of ermutation matrices, lower- and upper-triangular matrices with all 1s at the main diagonal, and a diagonal matrix.

An *eigenvalue* $\lambda \neq 0$ and the corresponding *eigenvector* **v** of a matrix **A** satisfy the matrix equation $\mathbf{A} * \mathbf{v} = \lambda * \mathbf{v}$. All eigenvalues of a matrix of the size *N* are defined by the polynomial equation $\mathtt{det}(\mathbf{A} - \lambda * \mathbf{I}) = \prod_{i=1}^{1 \leq K \leq N}{(\lambda - \lambda_i)^{\gamma_i}} = 0 \; : \; \sum_{i=1}^K{\gamma_i}=N$, where $\gamma_i$ is the *aritmetic multiplicity* of the eigenvalue $\lambda_i$. For each eigenvaue $\lambda_i$ all eigenvalues bound to this value can be found by solving the *under-defined* system of equations $(\mathbf{A} - \lambda_i * \mathbf{I}) * \mathbf{v}= \mathbf{0}$. The eigenvalue $\lambda_i$ has the *geometric multiplicity* $\mu_i$ if each bound eigenvector can be expressed as a linear combination of $\mu_i$ linearly independent *base* eigenvectors, i.e. it spawns a $\mu_i$-dimensional *eigenspace* within the *N*-dimensional vector space. Obviously, $1 \leq \mu_i \leq \gamma_i \leq N$. For example, any identity matrix **I** of the size *N* has a single eigenvalue $\lambda = 1$ with the arithmetic and geometric multiplicity of *N*.

On the other hand, the matrix

$$
\begin{bmatrix}
1 & 0 & 0 \\
0 & 2 & 0 \\
0 & 0 & 1 \\
\end{bmatrix}
$$

has two eigenvalues: $\lambda_1 = 1$ with $\gamma_1 = \mu_1 = 2$ and $\lambda_2 = 2$ with $\gamma_2 = \mu_2 = 1$. Thereas the 2D-shear matrix

$$
\begin{bmatrix}
1 & 1 \\
0 & 1\\
\end{bmatrix}
$$

has only a single eigenvalue $\lambda = 1$ with the arithmetic multiplicity $\gamma = 2$ bu the geometric multilicity $\mu = 1$. In other words, this matrix is *defect* (*non-diagonalizable*).

In general, even for the all real numbers elements matrices the eigenvalues can be *complex* numbers, thus the eigenvectors can contain *complex numbers* elements. However, this module concerns only the real matrices, vectors and eigenvalues.

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

The second exploit is the 'class patching'. For instance, column x row vectors product results in a matrix, which is defined later in the source code, thus it cannot be used as a return data type yet. Similarly, the matrix x matrix product's result should be converted into a square matrix object when possible, yet the square matrix class is not yet defined. The solution is to implement the functionality in a two-parameters function after definition of all involved classes, then convert this function into a *method* and assign to the respective class attribute, previously declared as a special method. In practice, it is achieved using the standard function *setattr*() applied to the class.

The LUP-decomposition is implemented as the *Gauss-Jordan* elimination with the columns and (optionally) rows pivoting. Consider a matrix **A** with the main diagonal element $a_{i,i}$ at the intersection of the *i*-th column and *i*-th row. If one subtracts the *i*-th row from all the rows below with the scalling coefficients $a_{i,j>i} / a_{i,i}$ all elements in the *i*-th column below the main diagonal become 0, thereas the determinant of the matrix is not changed due to the multi-linearity property of the determinant. This process is equvalent to the matrix multiplication $\mathbf{A} \; \rightarrow \mathbf{L}_i * \mathbf{A} \; :$

$$
\mathbf{L}_i = \begin{bmatrix}
1 & 0 & \dots & 0 & 0 & 0 & \dots & 0 & 0\\
0 & 1 & \dots & 0 & 0 & 0 & \dots & 0 & 0\\
\vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \dots & 1 & 0 & 0 & \dots & 0 & 0\\
0 & 0 & \dots & 0 & 1 & 0 & \dots & 0 & 0\\
0 & 0 & \dots & 0 & -\frac{a_{i, i+1}}{a_{i,i}} & 1 & \dots & 0 & 0\\
0 & 0 & \dots & 0 & -\frac{a_{i, i+2}}{a_{i,i}} & 0 & \dots & 0 & 0\\
\vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \dots & 0 & -\frac{a_{i, N-1}}{a_{i,i}} & 0 & \dots & 1 & 0\\
0 & 0 & \dots & 0 & -\frac{a_{i, N}}{a_{i,i}} & 0 & \dots & 0 & 1\\
\end{bmatrix}
$$

whereas the *inverse* transformation (left multiplication) being

$$
\mathbf{L}_i^{-1} = \begin{bmatrix}
1 & 0 & \dots & 0 & 0 & 0 & \dots & 0 & 0\\
0 & 1 & \dots & 0 & 0 & 0 & \dots & 0 & 0\\
\vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \dots & 1 & 0 & 0 & \dots & 0 & 0\\
0 & 0 & \dots & 0 & 1 & 0 & \dots & 0 & 0\\
0 & 0 & \dots & 0 & \frac{a_{i, i+1}}{a_{i,i}} & 1 & \dots & 0 & 0\\
0 & 0 & \dots & 0 & \frac{a_{i, i+2}}{a_{i,i}} & 0 & \dots & 0 & 0\\
\vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \dots & 0 & \frac{a_{i, N-1}}{a_{i,i}} & 0 & \dots & 1 & 0\\
0 & 0 & \dots & 0 & \frac{a_{i, N}}{a_{i,i}} & 0 & \dots & 0 & 1\\
\end{bmatrix}
$$

In the Gauss-Jordan elimination process one starts from the top-left corner and moves along the main diagonal, such that at each step $1 \leq k \leq N -1$ the matrix is transformed as $\mathbf{A}^{(k-1)} \rightarrow \mathbf{A}^{(k)} = \mathbf{L}_k * \mathbf{A}^{(k-1)} = \mathbf{L}_k * \mathbf{L}_{k-1} * \dots * \mathbf{L}_2 * \mathbf{L}_1 * \mathbf{A}^{(0)} \; : \; \mathbf{A}^{(0)} \equiv \mathbf{A}$. Thus, after *N*-1 steps the matrix **A** is transformed into an upper-triangular matrix **U**, i.e. $\mathbf{A}^{(N-1)} = \mathbf{U} = (\mathbf{L}_{N-1}* \dots *\mathbf{L}_1) * \mathbf{A} = \mathbf{L} * \mathbf{A}$, where the matrix **L** is lower-triangular and invertible, therefore $\mathbf{A} = \mathbf{L}^{-1} * \mathbf{U}$, where the inverse matrix

$$
\mathbf{L}^{-1} = \mathbf{L}_1^{-1} * \dots * \mathbf{L}_{N-1}^{-1}= \begin{bmatrix}
1 & 0 & \dots & 0 & 0 & 0 & \dots & 0 & 0\\
\frac{a_{1, 2}^{(0)}}{a_{1,1}^{(0)}} & 1 & \dots & 0 & 0 & 0 & \dots & 0 & 0\\
\vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
\frac{a_{1, i-1}^{(0)}}{a_{1,1}^{(0)}} & \frac{a_{1, i-1}^{(1)}}{a_{2,2}^{(1)}} & \dots & 1 & 0 & 0 & \dots & 0 & 0\\
\frac{a_{1, i}^{(0)}}{a_{1,1}^{(0)}} & \frac{a_{1, i}^{(1)}}{a_{2,2}^{(1)}} & \dots & \frac{a_{i-1, i}^{(i-2)}}{a_{i-1,i-1}^{(i-2)}} & 1 & 0 & \dots & 0 & 0\\
\frac{a_{1, i+1}^{(0)}}{a_{1,1}^{(0)}} & \frac{a_{1, i+1}^{(1)}}{a_{2,2}^{(1)}} & \dots & \frac{a_{i-1, i+1}^{(i-2)}}{a_{i-1,i-1}^{(i-2)}} & \frac{a_{i, i+1}^{(i-1)}}{a_{i,i}^{(i-1)}} & 1 & \dots & 0 & 0\\
\frac{a_{1, i+2}^{(0)}}{a_{1,1}^{(0)}} & \frac{a_{1, i+2}^{(1)}}{a_{2,2}^{(1)}} & \dots & \frac{a_{i-1, i+2}^{(i-2)}}{a_{i-1,i-1}^{(i-2)}} & \frac{a_{i, i+2}^{(i-1)}}{a_{i,i}^{(i-1)}} & \frac{a_{i+1, i+2}^{(i)}}{a_{i+1,i+1}^{(i)}} & \dots & 0 & 0\\
\vdots & \vdots & \ddots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
\frac{a_{1, N-1}^{(0)}}{a_{1,1}^{(0)}} & \frac{a_{2, N-1}^{(1)}}{a_{2,2}^{(1)}} & \dots & \frac{a_{i-1, N-1}^{(i-2)}}{a_{i-1,i-1}^{(i-2)}} & \frac{a_{i, N-1}^{(i-1)}}{a_{i,i}^{(i-1)}} & \frac{a_{i+1, N-1}^{(i)}}{a_{i+1,i+1}^{(i)}} & \dots & 1 & 0\\
\frac{a_{1, N}^{(0)}}{a_{1,1}^{(0)}} & \frac{a_{2, N}^{(1)}}{a_{2,2}^{(1)}} & \dots & \frac{a_{i-1, N}^{(i-2)}}{a_{i-1,i-1}^{(i-2)}} & \frac{a_{i, N}^{(i-1)}}{a_{i,i}^{(i-1)}} & \frac{a_{i+1, N}^{(i)}}{a_{i+1,i+1}^{(i)}} & \dots & \frac{a_{N-1, N}^{(N-1)}}{a_{N-1,N-1}^{(N-1)}} & 1\\
\end{bmatrix}
$$

where $a_{i,j}^{(k)}$ is the value of the element at the intersection of the *i*-th column and *j*-th row after *k* transformation steps. The prooof is outside the scope of this document. In the practical implementation it means that at each *k*-th step the *k*-th column of the inverse matrix $\mathbf{L}^{-1}$ can be calculated directly from the current state of the matrix, and then the matrix is transformed as:

* $a_{k, j>k}^{(k-1)} \rightarrow a_{k, j>k}^{(k)} = 0$ - all elements in the *k*-th column below the main diagonal are set to zero
* $a_{i>k, j>k}^{(k-1)} \rightarrow a_{i>k, j>k}^{(k)} = a_{i>k, j>k}^{(k-1)} - a_{i>k, k}^{(k-1)} * \frac{a_{k, j>k}^{(k-1)}}{a_{k,k}^{(k-1)}}$ - rows subtraction ignoring the already zeroed columns

Obviously, $\mathtt{det}(\mathbf{L}^{-1})=1 \; \Rightarrow \; \mathtt{det}(\mathbf{A}) = \mathtt{det}(\mathbf{U})=\mathtt{det}(\mathbf{A}^{(N-1)}) = \prod_{i=1}^N{a_{i,i}^{(N-1)}}$, i.e. the determinant of a matrix can be calculated as the product of all main diagonal elements in the upper-triangular matrix produced by the Gauss-Jordan elimination process.

However, it is possible to produce the zero value at the main diagonal after some *k*-1 steps $a_{k,k}^{(k-1)} = 0$ even if the matrix **A** is not *singular* (i.e. $\mathtt{det}(\mathbf{A}) \neq 0$, or all rows of the matrix are linearly independent). If the matrix is not singular, there must be, at least, one element in the *k*-th row, which is not yet zeroed, i.e., $\exists \; i>k \; : \; a_{i,k}^{(k-1)} \neq 0$. Hence, one can swap the *k*-th and *i*-th columns (columns pivoting process) to get a non-zero value at the main diagonal. Such pivoting is described by the matrix multiplication $\mathbf{A}^{(k-1)} * \mathbf{P}_k$, with the permutation matrix $\mathbf{P}_k$ being generated by the $\{1, 2, \dots, k-1, i, k+1, \dots, i-1, k, i+1, \dots, N-1, N \}$ permutation of the 1..*N* set. Because of the strict relation $i > k$ this process does not affect the already calculated values of the $\mathbf{L}^{-1}$ matrix, thus it can be applied to the original matrix even before the first step of the elimination process, i.e., $\mathbf{A}^{(k-1)} \rightarrow \mathbf{A}^{(k)} = \mathbf{L}_k * (\mathbf{A}^{(k-1)}*\mathbf{P}_k) = \mathbf{L}_k  * ((\mathbf{L}_{k-1} * \dots * \mathbf{L}_2 * \mathbf{L}_1 * \mathbf{A}^{(0)}) * \mathbf{P}_k) = (\mathbf{L}_k * \mathbf{L}_{k-1} * \dots * \mathbf{L}_2 * \mathbf{L}_1) * (\mathbf{A}^{(0)} * \mathbf{P}_k)$. Basically, all required columns pivotings can be applied to the matrix beforehand and defined as a single permutation matrix: $\mathbf{A} \rightarrow \mathbf{B} = \mathbf{A} * \mathbf{P}_c= \mathbf{L}^{-1} * \mathbf{U} \; \Rightarrow \; \mathbf{A} = \mathbf{L}^{-1} * \mathbf{U} * \mathbf{P}_c^{-1}$, where $\mathbf{P}_c^{-1} = \mathbf{P}_c^T$.

Note, that $\mathtt{det}(\mathbf{P}_c^{-1}) = \pm 1$, with each columns pivoting inverting the sign of the determinant of the resulting matrix **U**.

In the numerical implementation of the method the columns pivoting can be applied at each step, even if the value of the diagonal elements is not zero. Basically, at each step the column is selected with the highest *absolute* value of an element at the intersection with the current *k*-th row, and the current *k*-th column is swapped with the selected column. This approach is beneficial for the numerical stability, since at each step tha maximum possible absolute value of the divider in the scaling coefficient is chosen. In practice, there is no need to physically swap elements of a matrix. Instead, the columns pivoting can be traced using *N*-sized vector / array, instantiated with 1 .. *N* set values, and the current *k*-th and *i*-th elements being swapped when *k*-*i* columns pivoting has to be applied. This vector / array is used as a *look-up* table for the column index resolution. Also, there is no practical reason to generate and return the corresponding matrix. thus the generated columns permutation array is returned instead. Also, the permutation sign is traced, starting with +1, and the sign is flipped (+1 to -1 and vice versa) with each pivoting applied (unless the current diagonal element is the maximum absolute value in the row, in which case the pivoting is not applied).

In a case of a singular matrix a *k*-th row becomes all-zeroes at the *k*-th step. Unless it is the last row, and there, at least, one row below, which contains, at least, one non-zero element, the rows pivoting must be applied, i.e. swap of two rows - the current and one below it. As with the columns pivoting, the rows pivoting is implemented via cloumns permutation vector / array look-up table. However, physical swapping of the already calculated elements of the $\mathbf{L}^{-1}$ matrix must be applied concerning the respective *k*-th and *i*-th rows (*i* > *k*), but only the elements at the intersection with the columns from the 1-st to the (*k*-1)-th. Also, the produced matrix **U** is not strictly upper-triangular matrix (with all non-zero elements on the main diagonal), but is in the *row echelon* form, with the non-zero elements only at or above the main diagonal, but with one or more rows at the bottom containing only zeroes.

Thus, in the general case, both the columns and rows pivoting is applied, i.e. $\mathbf{A} \rightarrow \mathbf{B} = \mathbf{P}_r * \mathbf{A} * \mathbf{P}_c = \mathbf{L}^{-1} * \mathbf{U} \; \Rightarrow \; \mathbf{A} = \mathbf{P}_r^{-1} * \mathbf{L}^{-1} * \mathbf{U} * \mathbf{P}_c^{-1}$, which is the implemented LUP-decomposition method. **Note**, that for a non-singular (invertible) matrix the rows pivoting is not applied, hence $\mathbf{P}_r = \mathbf{P}_r^{-1} = \mathbf{I}$, unless det(**A**) = 0. Also note, that the numerical complexity of this top-down elimination process is $O(n^3)$: ~ $n^2$ operations for each row, and *n*-1 row to be eliminated.

The LUP-decomposition is used for calculation of the *determinant*. Obviously, $\mathbf{A} = \mathbf{P}_r^{-1} * \mathbf{L}^{-1} * \mathbf{U} * \mathbf{P}_c^{-1} \; \Rightarrow \; \mathtt{det}(\mathbf{A}) = \mathtt{det}(\mathbf{P}_r^{-1}) * \mathtt{det}(\mathbf{L}^{-1}) * \mathtt{det}(\mathbf{U}) * \mathtt{det}(\mathbf{P}_c^{-1})$. However, $\mathtt{det}(\mathbf{L}^{-1})=\mathtt{det}(\mathbf{L}) = 1$ because they are both lower-triangular with all 1s at the main diagonal. For the non-singular matrices the rows permutation is not applied, i.e. $\mathbf{P}_r = \mathbf{P}_r^{-1} = \mathbf{I}$ and it can be ignored. For the singular matrices $\mathtt{det}(\mathbf{U})=0$, since it contains at least one all 0s row at the bottom. Thus, $\mathtt{det}(\mathbf{A}) = \mathtt{sign}(\mathtt{det}(\mathbf{P}_c^{-1})) * \mathtt{det}(\mathbf{U}) = (-1)^K * \prod_{i=1}^N{u_{i,i}}$, where $K$ is the number of the colums pivoting applied in the process. The numerical complexity of this method is $O(n^3)$, as opposed to the $O(n!)$ complexity of *Leibniz* formula for the determinant (direct) or *Laplace expansion* formula (recursive).

For a non-singular matrix **A** the produced upper-triangular matrix **U** can be decomposed further into a product of an upper-triangular matrix with all 1s at the main diagonal and a diagonal matrix **D** as $\mathbf{U} = \hat{\mathbf{U}}^{-1} * \mathbf{D}$, i.e. $\mathbf{A} = \mathbf{L}^{-1} * \hat{\mathbf{U}}^{-1} * \mathbf{D} * \mathbf{P}_c^{-1}$, where matrix $\hat{\mathbf{U}}$ describes the secondary elimination (*k*-th row is subtracted from each row above with a specific coefficient, thus zeroing all elements above the diagonal in the *k*-th column). **Note**, that in the case of a singular matrix this *full decomposition* fails to produce a diagonal matrix **D**: one or more left-most columns will (or may) contain non-zero elements above the main diagonal. However, the major application of such full decomposition is the calculation of the inverse matrix, in which case the matrix must be non-singular.

The elements of the inverse matrix $\hat{\mathbf{U}}^{-1}$ are defined directly by the coefficients used in the bottom-up elemination, same as with the top-down elimination $\mathbf{L}^{-1}$, thus without any matrix multiplication. Hence, the numerical complexity of the bottom-up elimination is also $O(n^3)$, so is the numerical complexity of the total process of full decomposition.

The inverse matrix is calculated using the full decomposition. $\mathbf{A} = \mathbf{L}^{-1} * \hat{\mathbf{U}}^{-1} * \mathbf{D} * \mathbf{P}_c^{-1} \; \Rightarrow \; \mathbf{A}^{-1} = \mathbf{P}_c * \mathbf{D}^{-1} * \hat{\mathbf{U}} * \mathbf{L} \; \Leftrightarrow (\mathbf{A} * \mathbf{P}_c)^{-1} = \mathbf{D}^{-1} * \hat{\mathbf{U}} * \mathbf{L}$. The numerical algorithm, however, does not use any direct matrix multiplication; instead it relies on the rows addition and multiplication of a row by a scalar.

First, the matrix **L** is calculated from the identity matrix by subtracting *i*-th row from each *j*-th row (*j* > *i*) with the coefficient defined by the element of the $\mathbf{L}^{-1}$ matrix at the intesection of the *i*-th column and *j*-th row, starting from the first raw and iterating top-down.

Then, the *i*-th row of the calculated **L** matrix is subtracted from each *j*-th row (*j* < *i*) with the coefficient defined by the element of the $\hat{\mathbf{U}}^{-1}$ matrix at the intesection of the *i*-th column and *j*-th row, starting from the last raw and iterating bottom-up. This process produces the $\hat{\mathbf{U}} * \mathbf{L}$ matrix.

Since **D** is a diagonal matrix with the diagonal elements being $d_{i,i}$, the inverse matrix $\mathbf{D}^{-1}$ is also diagonal with the values of the main diagonal elements being $\frac{1}{d_{i,i}}$. Furthermore, the left multiplication by a diagonal matrix is simply the multilication of all elements in the *i*-th row of the right operand matrix by the \[*i*, *i*\] element of the left operand (diagonal matrix).

Thus, the matrix product $\mathbf{D}^{-1} * \hat{\mathbf{U}} * \mathbf{L}$ is already calculated, which is the inverse of the matrix **A** with permuted columns, which is $(\mathbf{A} * \mathbf{P}_c)^{-1} = \mathbf{P}_c^{-1} * \mathbf{A}^{-1}$, i.e., the calculated $\mathbf{D}^{-1} * \hat{\mathbf{U}} * \mathbf{L}$ product differs from the inverse matrix $\mathbf{A}^{-1}$ by rows permutation, which can be found as follows. Let $\mathbf{P}c$ columns permutation matrix be defined by the permutation $[p_1,p_2,\dots,p_N]$ of the 1 .. *N* set. Consider the pairs (tuples) $(p_i, i)$ and sort them in the ascending order of the values of the first element: $(p_i=1, i), (p_j=2, j), \dots, (p_k=N, k)$. Then the sequence of the second elements $i, j, \dots, k$ is the rows indeces look-up table for the required rows permutation.

Mathematically this algorithm of calculation of the inverse matrix is described in terms of the *augmented* block matrix (2N x N). If a transformation *T* of a matrix **A** performed as a series of left matrix products transforms it into an identity matrix, i.e. $\mathbf{A} \xrightarrow{T} \mathbf{I}$, then considering the block matrix constructed from **A** and **I**: $[\mathbf{A}|\mathbf{I}] \xrightarrow{T} [\mathbf{I}|\mathbf{A}^{-1}]$. Since this algorithm is, in essence, top-down and bottom-up eliminations applied two times to a NxN matrix, thus its numerical complexity is also $O(n^3)$, which is the same as of a matrix product. However, the direct calculation of the **L** and $\hat{\mathbf{U}}$ matrices has the numerical complexity of $O(n^4)$, since it requires *N*-2 products of the matrices representing single row elimination: $\mathbf{L} = \mathbf{L}_{N-1} * \mathbf{L}_{N-2} * \dots * \mathbf{L}_2 * \mathbf{L}_1$, and the same for the bottom-up elimination. Thus, the augmented matrix transformation method is faster and less prone to the numerical error accumulation.

Calculation of the inverse matrix is often required in the matrix-based calculations. For example, a system of linear equations can be expressed in a matrix form as **A** \* **x** = **y**, where column vector **y** represents the free coefficients, matrix **A** represents all bound coefficients, and the column vector **x** represents the solution of the system, i.e. the values of all unknown variables, which must be defined. If the system has one and only one solution, it is $\mathbf{x} = \mathbf{A}^{-1} * \mathbf{y}$. However, if matrix **A** is singular (thus, there is no inverse matrix), the respective system may have no solution or an infinite number of solutions. LUP-decomposition can be used to solve the system in the both cases.

First, simultaneous pivoting of the rows in the matrix **A** and respective elements of the free coefficients vector **y** does not change the solution, which is obvious since $\mathbf{P}* (\mathbf{A} * \mathbf{x}) = \mathbf{P} * \mathbf{y} = (\mathbf{P} * \mathbf{A}) * \mathbf{x}$, which is valid for any matrix **P**, not only the rows permutation matrix. Secondly, pivoting of the columns in the matrix **A** re-arranges the elements of the solution vector respectively: $(\mathbf{A} * \mathbf{P}_c) * (\mathbf{x}^T * \mathbf{P}_c)^T = \mathbf{A} * (\mathbf{P}_c * \mathbf{P}_c^T) * \mathbf{x} = \mathbf{A} * (\mathbf{P}_c * \mathbf{P}_c^{-1}) * \mathbf{x} = \mathbf{A} * \mathbf{x}$. Then, considering $\mathbf{A} = \mathbf{P}_r^{-1} * \mathbf{L}^{-1} * \mathbf{U} * \mathbf{P}_c^{-1}$ decomposition, the solution of the system of equations is found using the folowing steps:

* Calculate the pivoted free coefficients vector $\mathbf{v} = \mathbf{P}_r * \mathbf{y}$, which is achieved by swapping the elements of the vector **y** without actual multiplication
* Solve the system $\mathbf{L}^{-1} * \mathbf{U} * \mathbf{w} = \mathbf{v} \; \Rightarrow \; \mathbf{U} * \mathbf{w} = \mathbf{L} * \mathbf{v}$, which is achieved in two steps:
  * the vector $\mathbf{z} = \mathbf{L} * \mathbf{v}$ is calculated by subtracting elements of the vector **v** from the elements below (with higher indexes) with the multiplicative coefficients defined by the elements of the matrix $\mathbf{L}^{-1}$, i.e. the augmented matrix transformation $[\mathbf{A} * \mathbf{P}_c | \mathbf{v}] \rightarrow [\mathbf{U} | \mathbf{L} * \mathbf{v}]$
  * the vector **w** as the solution of the system $\mathbf{U} * \mathbf{w} = \mathbf{z}$ is found using the bottom-up back-stubstituion
* The calculated vector $\mathbf{w} = \mathbf{P}_c^{-1} * \mathbf{x} \; \Rightarrow \; \mathbf{x} = \mathbf{P}_c * \mathbf{w}$, which is calcualted by re-arranging the elements of the vector **w** using the $(p_i, i)$ tuples sorting technique to generate the indeces look-up table

If matrix **A** is invertible all main diagonal elements in the matrix **U** are non-zero, and there is only single solution vector **w**. Otherwise, $K \geq 1$ last rows in the matrix **U** are all zeroes, i.e. it can be written in the block form as

$$
\mathbf{U} = \begin{bmatrix}
\mathbf{U}_{(N-K)*(N-K)} & \mathbf{B}_{K * (N-K)} \\
\mathbf{0}_{(N-K)*K} & \mathbf{0}_{K*K}
\end{bmatrix}
$$

If, at least, one of the last *K* elements of the vector **z** is non-zero, the system has no solutions. Otherwise, any vector $\mathbf{w} = [w_1^{(1)}, \dots, w_{N-K}^{(1)}, c_1, 0, \dots, 0]^T + [w_1^{(2)}, \dots, w_{N-K}^{(2)}, 0, c-2, \dots, 0]^T + \dots + [w_1^{(K)}, \dots, w_{N-K}^{(K)}, 0, 0, \dots, c_K]^T$ is a solution of the system, where each vector $\mathbf{w}^{(j)}$ is the solution of the matrix equation $\mathbf{U}_{(N-K)*(N-K)} * \mathbf{w}^{(j)} = [z_1, z_2, \dots, z_{N-K}]^T - c_j * \mathbf{b}^{(j)}$, where $\mathbf{b}^{(j)}$ is the *j*-th column of the $\mathbf{B}_{K * (N-K)}$ sub-matrix. In the matrix form any solution of the system is $\mathbf{w} = \mathbf{U}_{(N-K)*(N-K)}^{-1}*([z_1, z_2, \dots, z_{N-K}]^T - \mathbf{B}_{K * (N-K)} * [c_1, c_2, \dots, c_K]^T)$.

This algorithm is used to find the *eigenvectors* of a matrix by the method *getEigenVectors*(). For an (optionally) provided eigenvalue $\lambda$ each bound eigenvector **x** must satisfy the matrix equation $(\mathbf{A} - \lambda * \mathbf{I}) * \mathbf{x} = \mathbf{0}$. If the eigenvalue has the *geometric multiplicity* K, the last K rows in the generated matrix **U** are all-zeroes. The lower-triangular matrix $\mathbf{L}^{-1}$ and the rows permutation matrix $\mathbf{P}_r$ can be simply ignored, since the free coefficients are all zeroes, hence the vector **z** is always all-zeroes. Then any solution (before final elements pivoting) as a linear composition of K linearly indendent solutions $\mathbf{w} = c_1 * [w_1^{(1)}, \dots, w_{N-K}^{(1)}, 1, 0, \dots, 0]^T + c_2 * [w_1^{(2)}, \dots, w_{N-K}^{(2)}, 0, 1, \dots, 0]^T + \dots + c_K * [w_1^{(K)}, \dots, w_{N-K}^{(K)}, 0, 0, \dots, 1]^T$, where $\mathbf{w}^{(j)} = \mathbf{U}_{(N-K)*(N-K)}^{-1} * \mathbf{b}^{(j)}$. Hence K linearly independent eigen vectors $\mathbf{x}_1 = \mathbf{P}_c * [w_1^{(1)}, \dots, w_{N-K}^{(1)}, 1, 0, \dots, 0]$ to $\mathbf{x}_K = \mathbf{P}_c * [w_1^{(K)}, \dots, w_{N-K}^{(K)}, 0, 0, \dots, 1]$ form one of the possible eigenbasis in the eigenspace generated by the eigenvalue $\lambda$. Since they are linearly independent, an *orthonormal* eigenbasis can be generated from them using [Gram-Schmidt algorithm](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process), which generates K vectors in the same eigenspace with each vector haiving a unity length (||**x**|| = 1) and being orthogonal to others. Such orthonormal eigenbasis is returned by convention to avoid ambiguity.

Note that the eigenvalues can be found analytically in many cases: for example, the main diagonal elements of any diagonal, upper- or lower-triangular matrix are its eigenvalues, the eigenvalues can be easily guessed sometimes, especially for the sparse matrices (many zero-valued elements) with integer values of the elements. There are several numerical methods to find, at least, one eigenvalue of a matrix, e.g. [power iteration](https://en.wikipedia.org/wiki/Power_iteration), or even all eigenvalues of a matrix at once. If an eigenvalue is not passed into the method *getEigenVectors*(), another method of the class *getEigenValues*() is called automatically to find all eigenvalues, and then the associated orthonormal eigenbasis is found for each found eigenvalue.

Note that the method *getEigenValues*() implements [QR agorithm](https://en.wikipedia.org/wiki/QR_algorithm), which works only for the *diagnonalizable* (not defective) matrices, but returns all eigenvalues at once. Furthermore, for such matrices the geometric multiplicity of each eigenvalue equals its arithmetic multiplicity, hence for a matrix of the size N exactly N linearly independent eigenvectors can be calculated, forming one or more orthonormal eigenbases depending on the number of the unique eigenvalues.

This algorithm does not converge in the case of a defective matrix, thus the maximum number of iterations threshold of 100 000 is used to terminate the calculations when algorithm does not converge. Furthermore, the convergence of the algorithm is judged by proximity of the **Q** matrix generated at each step to the identity matrix **I**: each main diagonal element must differ from 1 by no more than $\varepsilon=10^{-14}$, whereas the values of all non-diagonal elements must be almost zero, i.e. in the open range $(-\varepsilon, \varepsilon)$. In order to reduce accumulation of the numerical error all almost-zero elements of a normalized vector are rounded to 0, whereas elements being in the $\varepsilon$ vicinity of the values +1 or -1 are rounded to them. Basically, the vectors mostly or truly parallel to one of the *standard basis* vectors is normalized to the respective vector. This approach is also taken in the implementation of the Gram-Schmidt algorithm.

Each found eigenvalue is rounded to the nearest integer number, if the absolute difference with this integer is less than $N^3 * \varepsilon$, where *N* is the matrix size. An eigenvalue $\lambda_2$ is considered different from a previously found eigenvalue $\lambda_1$ if $\mathtt{abs}\left( \frac{\lambda_2 - \lambda_1}{\lambda_1} \right) > \varepsilon$. Otherwise, the two eigenvalues are considered to be the same (multiplicity > 1), and the $\lambda_2$ values is not added to the result.

Also, for a given eigenvalue the method *getEigenVectors*() determines its geometric multiplicty by the number of zero values in the main diagonal of the matrix **U** in the LUP-decomposition. Because of the rows and columns pivoting used in the LUP-decomposition algorithm such zero-valued diagonal elements can occur only in the lowest rows, which must be all-zeroes. However, due to accumulation of the numerical error (floating point operations) the algorithm may fail to zero one or more elements in the linearly dependent rows. Therefore, the value of the last diagonal element is compared to zero using $N^3 * \varepsilon$ proximity threshold. For the rest of the diagonal elements a more stricted proximity threshold of $N^2 * \varepsilon$ is used due to the forced columns pivoting and explicit zeroing of the elements below the diagonal used in the LUP-decomposition algorithm.

These measures improve the numerical stability and precision of the eigenvalues and eigenvectors calculation, especially in the case of the integer values matrices. However, the same measures may backfire and produce wrong results in the case of large matrices with large dynamic range of the absolute values of the elements, especially floating point values.

## API Reference

### Class Array2D

A prototype class for the generic and square matrices, implementing the data storage and read-access in the form of a 2-D array.

The data is stored and returned (property Data) as a sequence of the nested equal length sub-sequences of real numbers, each sub-sequence representing a single row of the array, i.e. in the rows-first order.

The instances of this class are immutable objects, and are not considered to be sequences, thus not supporting iteration and 'contains' check. But the entire stored data can be copied into a mutable Python sequence (list) using the property *Data*. Individual element can be read-only accessed using double indexing as *obj*[col_index, row_index]. Slice notation is not supported.

Can be instantiated either from a flat sequence of real number, when either width or height or both must be specified; or from a nested sequence, in which case the width and height arguments are ignored even if provided. The default parsing order is rows-first, which can be switched to columns-first using a boolean keyword argument *isColumnsFirst*, which defaults to **False**.

Thus, the supported instantiation call signatures are:

* **Array2D**(list(int OR float), *Width* = int >= 2)
* **Array2D**(list(int OR float), *Height* = int >= 2)
* **Array2D**(list(int OR float), *Width* = int >= 2, *Height* = int >= 2)
* **Array2D**(list(int OR float), *Width* = int >= 2, *isColumnsFirst* = True)
* **Array2D**(list(int OR float), *Height* = int >= 2, *isColumnsFirst* = True)
* **Array2D**(list(int OR float), *Width* = int >= 2, *Height* = int >= 2, *isColumnsFirst* = True)
* **Array2D**(list(list(int OR float)))
* **Array2D**(list(list(int OR float)), *isColumnsFirst* = True)

***Properties***:

* *Width*: (read-only) **int** >= 2
* *Height*: (read-only) **int** >= 2
* *Data*: (read-only) **list**(**list**(**int** OR **float**))

***Instantiation***:

\_\_**int**\_\_(seqValues, *, Width = None, Height = None, isColumnsFirst = False)

*Signature*:

seq(int OR float) OR seq(seq(int OR float))/, int >= 2 OR None, int >= 2 OR None, bool/ -> None

*Args*:

* *seqValues*: **seq**(**int** OR **float**) OR **seq**(**seq**(**int** OR **float**)); elements of the array / matrix, in the flat form the total number of elements must be equal to or greater than 2 * *Width* if only width is specified, or 2 * *Height* if only height is specified, or *Width* \* *Height* if both are specified
* *Width*: (keyword) **int** >= 2 OR **None**; required width of the array or matrix, defaults to None meaning automatic definition based on the number of elements and the specified required height, at least one of the dimensions (width and / or height) must be specified if the data is passed as a flat sequence, this argument is ignored if the data is passed as a nested sequence
* *Height*: (keyword) **int** >= 2 OR **None**; required height of the array or matrix, defaults to None meaning automatic definition based on the number of elements and the specified required width, at least one of the dimensions (width and / or height) must be specified if the data is passed as a flat sequence, this argument is ignored if the data is passed as a nested sequence
* *isColumnsFirst*: (keyword) **bool**; flag if the passed data to parsed in the columns-first order, defaults to False, i.e. rows-first order when each consequitive slice of a flat sequence or sub-sequence element of a nested sequence is treated as the representation of a single row of the array or matrix

*Raises*:

* **UT_TypeError**: mandatory argument is neither a flat sequence of real numbers nor a nested sequence of sequences of real numbers, OR optional keyword argument *isColumnsFirst* is not boolean, OR optional keyword arguments *Width* or *Height* are neither **None** nor integer numbers
* **UT_ValueError**: either *Width* or *Height* argument is an integer < 2, OR the both arguments are **None** when the mandatory argument is a flat sequence of real numbers, OR the length of a flat sequence as the mandatory argument is too short for the given values of *Width* and / or *Height*, OR a nested sequence as the mandatory argument has less than 2 elements, OR the length of an sub-sequence element is less than 2, OR the sub-sequence elements differ in length.

*Description*:

Parses the passed data sequence and packs it into the internally stored nested tuple structure representing a 2D array or a matrix, with each tuple element representing a single row of that array or matrix.

### Class Vector

Implementation of a generic, abstract vector. Must be instantiated with 2 or more real number typed arguments, with the number of the arguments defining the size / dimensions of the vector. Individual elements can be read-only accessed using integer indexing as *obj*\[index\], slicing is not supported.

The instances of this class are immutable objects, and are not considered to be sequences, thus not supporting iteration and 'contains' check. But the entire stored data can be copied into a mutable Python sequence (list) using the property *Data*.

Supports the following artihmetics:

* Addition and subtraction of two generic vectors of equal length
* Left and right mutliplication by a real number
* Division by non-zero real number
* Inner (dot) product of two equal length generic vectors -> real number
* Outer product of two generic vectors -> **Array2D**

Additionally, supports generation of orthogonal unity vectors of the specified dimensions and a normalized (unity geometric length) vector parallel to the one represented by the current instance.

***Properties***:

* *Size*: (read-only) **int** >= 2
* *Data*: (read-only) **list**(**int** OR **float**)

***Instantiation***:

\_\_**init**\_\_(*args)

*Signature*:

*seq(int OR float) -> None

*Args*:

*\*args*: **\*seq**(**int** OR **float**); any number of integer or floating point arguments as the elements of the vector

*Raises*:

* **UT_TypeError**: any of the arguments is neither integer nor floating point number
* **UT_ValueError**: number of arguments is less than 2

*Description*:

The passed numerical arguments are taken as the elements of a vector to be created.

***Class methods***:

**generateOrthogonal**(Length, Index)

*Signature*:

int >= 2, int >= 0 -> Vector

*Args*:

* *Length*: **int** >= 2;
* *Index*: **int** >= 2;

*Returns*:

**Vector**: an instance of the same class

*Raises*:

* **UT_TypeError**: either of the arguments in not an integer number
* **UT_ValueError**: the first argument is less than 2, OR the second argument is negative or equal to or greater than the first one

*Description*:

Class method to generate a vector from the unity orthogonal set such, that only a single element is 1, thereas all other elements are 0 - i.e. one of the *standard basis* vectors.

***Methods***:

**normalize**()

*Signature*:

None -> Vector

*Returns*:

**Vector*: a new instance of the same class - the normalized vector

*Raises*:

**UT_ValueError**: all elements of the original vector are zeroes

*Description*:

Generates a new instance of the same class of the same length, but with all elements being scaled (divided by) a square root of the sum of all elements of the original vector squared.

### Class Column

Implementation of a column vector. Must be instantiated with 2 or more real number typed arguments, with the number of the arguments defining the size / dimensions of the vector. Individual elements can be read-only accessed using integer indexing as *obj*\[index\], slicing is not supported.

The instances of this class are immutable objects, and are not considered to be sequences, thus not supporting iteration and 'contains' check. But the entire stored data can be copied into a mutable Python sequence (list) using the property *Data*.

Supports the following artihmetics:

* Addition and subtraction of two column vectors of equal length
* Left and right mutliplication by a real number
* Division by non-zero real number
* Right multiplication by a row vector -> **Matrix**
* Left multiplication by a row vector of the same size -> real number

Outer product is not supported. Multiplication with a matrix is delegated to the Matrix class.

Additionally, supports generation of orthogonal unity vectors of the specified dimensions and a normalized (unity geometric length) vector parallel to the one represented by the current instance. Also implements transposition **Column** -> **Row**.

Sub-classes **Vector**.

***Properties***:

* *Size*: (read-only) **int** >= 2
* *Data*: (read-only) **list**(**int** OR **float**)

***Instantiation***:

\_\_**init**\_\_(*args)

*Signature*:

*seq(int OR float) -> None

*Args*:

*\*args*: **\*seq**(**int** OR **float**); any number of integer or floating point arguments as the elements of the vector

*Raises*:

* **UT_TypeError**: any of the arguments is neither integer nor floating point number
* **UT_ValueError**: number of arguments is less than 2

*Description*:

The passed numerical arguments are taken as the elements of a vector to be created.

***Class methods***:

**generateOrthogonal**(Length, Index)

int >= 2, int >= 0 -> Column

Inherited from the class **Vector**.

***Methods***:

**normalize**()

None -> Column

Inherited from the class **Vector**.

**transpose**()

*Signature*:

None -> Row

*Description*:

Transposes the current column vector into a row vector (**Row** class instance) preserving the elements.

### Class Row

Implementation of a row vector. Must be instantiated with 2 or more real number typed arguments, with the number of the arguments defining the size / dimensions of the vector. Individual elements can be read-only accessed using integer indexing as *obj*\[index\], slicing is not supported.

The instances of this class are immutable objects, and are not considered to be sequences, thus not supporting iteration and 'contains' check. But the entire stored data can be copied into a mutable Python sequence (list) using the property Data.

Supports the following artihmetics:

* Addition and subtraction of two row vectors of equal length
* Left and right mutliplication by a real number
* Division by non-zero real number
* Left multiplication by a column vector -> **Matrix**
* Right multiplication by a same size column vector -> real number

Outer product is not supported. Multiplication with a matrix is delegated to the **Matrix** class.

Additionally, supports generation of orthogonal unity vectors of the specified dimensions and a normalized (unity geometric length) vector parallel to the one represented by the current instance. Also implements transposition **Row** -> **Column**.

Sub-classes **Vector**.

***Properties***:

* *Size*: (read-only) **int** >= 2
* *Data*: (read-only) **list**(**int** OR **float**)

***Instantiation***:

\_\_**init**\_\_(*args)

*Signature*:

*seq(int OR float) -> None

*Args*:

*\*args*: **\*seq**(**int** OR **float**); any number of integer or floating point arguments as the elements of the vector

*Raises*:

* **UT_TypeError**: any of the arguments is neither integer nor floating point number
* **UT_ValueError**: number of arguments is less than 2

*Description*:

The passed numerical arguments are taken as the elements of a vector to be created.

***Class methods***:

**generateOrthogonal**(Length, Index)

int >= 2, int >= 0 -> Row

Inherited from the class **Vector**.

***Methods***:

**normalize**()

None -> Row

Inherited from the class **Vector**

**transpose**()

*Signature*:

None -> Column

*Description*:

Transposes the current row vector into a column vector (**Column** class instance) preserving the elements.

### Class Matrix

Implementation of a generic matrix.

The data is stored and returned (property *Data*) as a sequence of the nested equal length sub-sequences of real numbers, each sub-sequence representing a single row of the matrix, i.e. in the rows-first order.

The instances of this class are immutable objects, and are not considered to be sequences, thus not supporting iteration and 'contains' check. But the entire stored data can be copied into a mutable Python sequence (list) using the property *Data*. Individual element can be read-only accessed using double indexing as *obj*\[col_index, row_index\].

Can be instantiated either from a flat sequence of real number, when either width or height or both must be specified; or from a nested sequence, in which case the width and height arguments are ignored even if provided. The default parsing order is rows-first, which can be switched to columns-first using a boolean keyword argument *isColumnsFirst*, which defaults to **False**.

Thus, the supported instantiation call signatures are:

* **Matrix**(list(int OR float), *Width* = int >= 2)
* **Matrix**(list(int OR float), *Height* = int >= 2)
* **Matrix**(list(int OR float), *Width* = int >= 2, *Height* = int >= 2)
* **Matrix**(list(int OR float), *Width* = int >= 2, *isColumnsFirst* = True)
* **Matrix**(list(int OR float), *Height* = int >= 2, *isColumnsFirst* = True)
* **Matrix**(list(int OR float), *Width* = int >= 2, *Height* = int >= 2, *isColumnsFirst* = True)
* **Matrix**(list(list(int OR float)))
* **Matrix**(list(list(int OR float)), *isColumnsFirst* = True)

Sub-classes **Array2D** and adds support for arithmetics between a matrices, column and row vectors, and scalars. Also adds transposition, columns and rows access methods.

***Properties***:

* *Width*: (read-only) **int** >= 2
* *Height*: (read-only) **int** >= 2
* *Data*: (read-only) **list**(**list**(**int** OR **float**))

***Instantiation***:

\_\_**int**\_\_(seqValues, *, Width = None, Height = None, isColumnsFirst = False)

*Signature*:

seq(int OR float) OR seq(seq(int OR float))/, int >= 2 OR None, int >= 2 OR None, bool/ -> None

*Args*:

* *seqValues*: **seq**(**int** OR **float**) OR **seq**(**seq**(**int** OR **float**)); elements of the array / matrix, in the flat form the total number of elements must be equal to or greater than 2 * *Width* if only width is specified, or 2 * *Height* if only height is specified, or *Width* \* *Height* if both are specified
* *Width*: (keyword) **int** >= 2 OR **None**; required width of the array or matrix, defaults to None meaning automatic definition based on the number of elements and the specified required height, at least one of the dimensions (width and / or height) must be specified if the data is passed as a flat sequence, this argument is ignored if the data is passed as a nested sequence
* *Height*: (keyword) **int** >= 2 OR **None**; required height of the array or matrix, defaults to None meaning automatic definition based on the number of elements and the specified required width, at least one of the dimensions (width and / or height) must be specified if the data is passed as a flat sequence, this argument is ignored if the data is passed as a nested sequence
* *isColumnsFirst*: (keyword) **bool**; flag if the passed data to parsed in the columns-first order, defaults to False, i.e. rows-first order when each consequitive slice of a flat sequence or sub-sequence element of a nested sequence is treated as the representation of a single row of the array or matrix

*Raises*:

* **UT_TypeError**: mandatory argument is neither a flat sequence of real numbers nor a nested sequence of sequences of real numbers, OR optional keyword argument *isColumnsFirst* is not boolean, OR optional keyword arguments *Width* or *Height* are neither **None** nor integer numbers
* **UT_ValueError**: either *Width* or *Height* argument is an integer < 2, OR the both arguments are **None** when the mandatory argument is a flat sequence of real numbers, OR the length of a flat sequence as the mandatory argument is too short for the given values of *Width* and / or *Height*, OR a nested sequence as the mandatory argument has less than 2 elements, OR the length of an sub-sequence element is less than 2, OR the sub-sequence elements differ in length.

*Description*:

Creates an instance of the class and fills the values of its elements using the passed data.

***Methods***:

**transpose**()

*Signature*:

None -> Matrix

*Description*:

Method to generate a transposition of the current matrix (new instance of the same class). Each row becomes a column and vice versa preserving the rows / columns order.

**getColumn**(Index)

*Signature*:

int -> Column

*Args*:

*Index*: **int**; the required column index

*Raises*:

* **UT_TypeError**: argument is not an integer number
* **UT_ValueError**: argument value is not in the inclusive range [-*Width*, *Width* - 1]

*Description*:

Method to access a specific column of a matrix in the form of a column vector.

**getRow**(Index)

*Signature*:

int -> Row

*Args*:

*Index*: **int**; the required row index

*Raises*:

* **UT_TypeError**: argument is not an integer number
* **UT_ValueError**: argument value is not in the inclusive range [-*Height*, *Height* - 1]

*Description*:

Method to access a specific row of a matrix in the form of a row vector.

### Class SquareMatrix

Implementation of a square matrix, for which width equals height, and is referred to as simply size.

The data is stored and returned (property *Data*) as a sequence of the nested equal length sub-sequences of real numbers, each sub-sequence representing a single row of the matrix, i.e. in the rows-first order.

The instances of this class are immutable objects, and are not considered to be sequences, thus not supporting iteration and 'contains' check. But the entire stored data can be copied into a mutable Python sequence (list) using the property *Data*. Individual element can be read-only accessed using double indexing as *obj*[col_index, row_index].

Can be instantiated either from a flat sequence of real number, when the required size may be specified via a keyword argument, or it may auto-deducted; or from a nested sequence, in which case the size arguments is ignored even if provided. The default parsing order is rows-first, which can be switched to columns-first using a boolean keyword argument *isColumnsFirst*, which defaults to False.

Thus, the supported instantiation call signatures are:

* **SquareMatrix**(list(int OR float))
* **SquareMatrix**(list(int OR float), *isColumnsFirst* = True)
* **SquareMatrix**(list(int OR float), *Size* = int >= 2)
* **SquareMatrix**(list(int OR float), *Size* = int >= 2, *isColumnsFirst* = True)
* **SquareMatrix**(list(list(int OR float)))
* **SquareMatrix**(list(list(int OR float)), *isColumnsFirst* = True)

Sub-classes **Matrix** and supports for arithmetics between a matrices, column and row vectors, and scalars as well as transposition, columns and rows access methods. Also adds adds a number of class and instance methods specific for the square matrices:

* calculation of the trace and determinant
* LUP and LUDP (full) decomposition
* Generation of the multuplicative inverse matrix
* Calculation of eigenvalues and eigenvectors

***Properties***:

* *Width*: (read-only) **int** >= 2
* *Height*: (read-only) **int** >= 2
* *Size*: (read-only) **int** >= 2
* *Data*: (read-only) **list**(**list**(**int** OR **float**))

***Instantiation***:

\_\_**init**\_\_(seqValues, *, Size = None, isColumnsFirst = False)

*Signature*:

seq(int OR float) OR seq(seq(int OR float))/, int >= 2 OR None, bool/ -> None

*Args*:

* *seqValues*: **seq**(**int** OR **float**) OR **seq**(**seq**(**int** OR **float**)); elements of the array / matrix, in the flat form the total number of elements must be equal to or greater than *Size* \* *Size* if it is specified, or > 4 if *Size* is not specified or **None**, in the nested form the length of each element must be equal to their count
* *Size*: (keyword) **int** >= 2 OR **None**; required size = width = height of the matrix, defaults to **None** meaning automatic definition based on the length of the flat sequence argument
* *isColumnsFirst*: (keyword) **bool**; flag if the passed data to parsed in the columns-first order, defaults to **False**, i.e. rows-first order when each consequitive slice of a flat sequence or sub-sequence element of a nested sequence is treated as the representation of a single row of the array or matrix

*Raises*:

* **UT_TypeError**: mandatory argument is neither a flat sequence of real numbers nor a nested sequence of sequences of real numbers, OR optional keyword argument *isColumnsFirst* is not boolean, OR optional keyword arguments *Size* is neither None nor an integer number
* **UT_ValueError**: *Size* argument is an integer < 2, OR the length of a flat sequence as the mandatory argument is too short for the given values of *Size*, OR a nested sequence as the mandatory argument has less than 2 elements, OR the length of an sub-sequence element is less than 2, OR the sub-sequence elements differ in length, OR length of the sub-sequence element is not equal to their number

*Description*:

Parses the passed data sequence and packs it into the internally stored nested tuple structure representing a matrix, with each tuple element representing a single row of that matrix.

***Class methods***:

**generateIdentity**(Size)

*Signature*:

int >= 2 -> SquareMatrix

*Args*:

*Size*: **int** > 1; the requested size of the identity matrix

*Returns*:

* **SquareMatrix**: a new instance of the class

*Raises*:

* **UT_TypeError**: the passed argument is not an integer number
* **UT_ValueError**: the passed argument is an integer, but less than 2

*Description*:

Creates a new instance of a square matrix with all elements on the main diagonal being equal to 1, and all other elements being zeroes.

**generatePermutation**(Permutation)

*Signature*:

seq(int >= 0) -> SquareMatrix

*Args*:

*Permutation*: **seq**(**int** >= 0);  proper 0..N-1 permutation sequence

*Returns*:

**SquareMatrix**: a new instance of the class

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence of integer numbers
* **UT_ValueError**: the sequence is shorter that 2 elements, OR any of the elements is negative OR equal to or greater than the sequence length, OR any of the elements is not unique.

*Description*:

Generates a permutation matrix of the size N from the passed 0..N-1 numbers permutation sequence. Basically, the identity matrix with some columns (or rows) shufled. The value j at the index i of the passed sequence encodes 1 at the intersection of i-th row and j-th column.

**generateDiagonal**(Elements)

*Signature*:

seq(int OR float) -> SquareMatrix

*Args*:

*Elements*: **seq**(**int** OR **float**); the main diagonal elements

*Returns*:

**SquareMatrix**: a new instance of the class

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence of integer or floating point numbers
* **UT_ValueError**: the sequence is shorter that 2 elements

*Description*:

Generates a square diagonal matrix with the elements on the main diagonal defined by the passed real numbers sequence argument.

***Methods***:

**transpose**()

None -> SquareMatrix

Inherited from the **Matrix** class.

**getColumn**(Index)

int -> Column

Inherited from the **Matrix** class.

**getRow**(Index)

int -> Row

Inherited from the **Matrix** class.

**getTrace**()

*Signature*:

None -> int OR float

*Description*:

Calculates the trace of a square matrix, i.e. the sum of all main diagonal elements.

**getLUPdecomposition**()

*Signature*:

None -> SquareMatrix, SquareMatrix, tuple(int), tuple(int), int

*Returns*:

**SquareMatrix**, **SquareMatrix**, **tuple**(**int**), **tuple**(**int**), **int**: unpacked tuple of two square matrices of the same size (lower- and upper triangular respectively), followed by the permutation tuple representing the swapping of the columns (the actual permutation matrix can be generated from it directly), followed by (tuple) permutation of rows, followed by +1 or -1 number as the permutation sign.

*Description*:

Calculates the decomposion of a matrix into a product of four matrices: the rows permutation matrix (which is identity unless some rows are not linear independent), the lower-triangular (with all main diagonal elements being 1), the upper-triangular matrix and the rows and columns permutation matrices. Uses Gauss-Jordan elimination algorithm with full pivoting.

Note that the rows pivoting occurs only if a row becomes all zeroes in the elimination process, which means, that the determinant is zero and the matrix is singular. Therefore, the rows permutations can be usually ignored. The columns permutations are used for the numerical stability even if no zeroes appear on the main diagonal during elimination.

Naming the initial matrix A, lower-triangular L, upper-triangular U, columns permutation Pc and rows permutation matrix Pr, for any non-singular matrix A = L * U * Pc, with Pr == I - identity matrix. Even for a singular matrix A = Pr * L * U * Pc with U being the row echelon form with all zeroes rows at the bottom.

**getFullDecomposition**()

*Signature*:

None -> SquareMatrix, SquareMatrix, tuple(int OR float), tuple(int), tuple(int), int

*Returns*:

**SquareMatrix**, **SquareMatrix**, **tuple**(**int** OR **float**), **tuple**(**int**), **tuple**(**int**), **int**: unpacked tuple of two square matrices of the same size (lower- and upper-triangular respectively), followed by the tuple or real numbers representing the main diagonal elements of the diagonal matrix (can be generated directly from it), followed by the permutation tuple representing the swapping of the columns (the actual permutation matrix can be generated from it directly), followed by the rows permutation tuple, followed by +1 or -1 number as the permutation sign.

*Description*:

Calculates the decomposion of a matrix into a product of five matrices: the rows permutation matrix (which is identity unless some rows are not linear independent), the lower-triangular (with all main diagonal elements being 1), the upper-triangular matrix (with all main diagonal elements being 1), a diagonal matrix (all non-zero elements only on the main diagonal) and the permutation matrices. Uses Gauss-Jordan elimination algorithm with full pivoting to calculate the LUP-decomposition first, then decomposes the upper- traingular matrix into a diagonal and upper-triangular with onses at the main diagonal using Gauss elimination algorithm.

Note that the rows pivoting occurs only if a row becomes all zeroes in the elimination process, which means, that the determinant is zero and the matrix is singular. Therefore, the rows permutations can be usually ignored. The columns permutations are used for the numerical stability even if no zeroes appear on the main diagonal during elimination.

Naming the initial matrix A, lower-triangular L, upper-triangular U, diagonal matrix D, columns permutation Pc and rows permutation matrix Pr, for the non-singular matrix A = L * U * D * Pc, with Pr == I being the identity matrix.

**Note**: for a singular matrix det(A) = 0, A != Pr * L * U * D * Pc, since the Gauss elimination method fails to eliminate all non-diagonal elements, thus D is not, actually, diagonal, but it is treated as one.

**getDeterminant**()

*Signature*:

None -> int OR float

*Description*:

Calculates the determinant of a square matrix using LUP-decomposition for large (Size > 3) matrices, and the direct analytical expression for 2 x 2 and 3 x 3 matrices for speed.

**getInverse**()

*Signature*:

None -> SquareMatrix OR None

*Returns*:

* **SquareMatrix**: the inverse of the current square matrix, unless the current matrix is singular (determinant is zero)
* **None**: the matrix is singular, so the inverse does not exists

*Description*:

Calculates the inverse matrix if one exists using full (LUDP) decomposition.

**getEigenValues**()

*Signature*:

None -> tuple(int OR float) OR None

*Returns*:

* **tuple**(**int** OR **float**): all unique real number valued eigenvalues
* **None**: no real number valued eigenvalues are found

*Description*:

Calculates the real number valued eigenvalues. Based on the Francis QR-algorithm with Gram-Schmidt orthogonalization method. Works only for the diagonalizable (not defect) matrices.

**getEigneVectors**(*, Eigenvalue = None)

*Signature*:

/int OR float OR None/ -> dict(int OR float -> tuple(Column) OR None) OR None

*Args*:

*Eigenvalue*: (keyword) **int** OR **float**; an a priori known eigenvalue of the matrix, for which the eigenvectors are to be found. Defaults to **None**, in which case the method attemts to calculate all eigenvalues first.

*Returns*:

* **dict**(**int** OR **float** -> **tuple**(**Column**) OR **None**): dictionary mapping all unique real number valued eigenvalues to the respective orthonormal set of eigenvectors as a tuple of column vector class instances, if it is not possible to calculate, at least, one eigenvector for a given eigenvalue (due to rounding errors) the value of the corresponding key is set to **None**
* **None**: no real number valued eigenvalues are found, OR the passed value is not an eigenvalue of the matrix

*Raises*:

**UT_TypeError**: the passed optional value is not a real number

*Description*:

Calculates the real number valued eigenvalues and the respective eigen vectors, which form orthonormal basis for each eigenvalue. Based on the Francis QR-algorithm with Gram-Schmidt orthogonalization method.
