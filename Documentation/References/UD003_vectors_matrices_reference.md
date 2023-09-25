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

Matrix classes are designed to be *immutable* and *atomic* objects, and not a specialized sequence. Therefore, neither *iteration* (as `for element in matrix`) nor *contains check* (as `if element in matrix`) are supported; also the values of the elements can not be changed after instantiation. However, the value if any stored element can be read-out (accessed) using the double index notation (starting from index 0), as `Matrix1[1, 1]` in the example above results in the value of 4. Slice notation is not supported, nor the standard single index notation; instead the classes provide methods to access a single row or column as instances of the respective vector classes. Also, all stored elements can be read-accessed at once via the read-only property *Data*, which returns a list of lists containg the copies of the matrix' elements values, and always in the column-first order.

The both matrix classes support transposition method, which returns a new instance of the same class. Basically, this method simply wraps the class instantiation method into which the stored data content (elements) of the current instance is passed, which is stored internally always in the column-first order, with the explicit switch (keyword argument) *isColumnFirst* = **False**. Thus, an N x M matrix transposed is an M x N matrix, with all columns becoming rows and vice versa, whilst preserving the oder, i.e. $\mathbf{A} \; \rightarrow \; \mathbf{B} = \mathbf{A}^T\; : b_{j,i} = a_{i,j} \; \forall \; 1 \leq i \leq N, \; 1 \leq j \leq M$. In the case of a square matrix the transposition can be visialized as a rotation (flipping) along the main diagonal.

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

A *permutation* of a set (collection of unique items) is a set of the same size produced by reordering of its elements, i.e. a set \{ 2, 1, 3\} is a permutation of the set \{ 1, 2, 3 \} (a.k.a. 1 .. 3 set). A *permutation matrix* **P** of a size *N* is defined by a permutation of 1..*N* set as follows: the value $1 \leq j \leq N$ at the position $1 \leq i \leq N$ in the set permutation means that the *i*-th column of the matrix **P** has non-zero (actually 1) value only at the intersection with the *j*-th row, whereas all other elements of this column are zeroes. Thus, a set permutation \{ 2, 1, 3\} defines the permutation matrix

$$
\begin{bmatrix}
0 & 1 & 0 \\
1 & 0 & 0 \\
0 & 0 & 1 \\
\end{bmatrix}
$$

In a permutation matrix each column and each row has only one element with the value of 1 and all other elements are of the value 0. A permutation matrix is *orthogonal*, i.e. $\mathbf{P}^{-1} = \mathbf{P}^T$, and $\mathtt{det}(\mathbf{P}) = \pm 1$. Basically, a permutation matrix is an identity matrix with two to more columns (or rows) being swapped (pivoted). The left multiplication of a matrix **A** by a permutation matrix (**P \* A**) swaps the columns of the matrix **A**, whereas the right multiplication (**A \* P**) swaps the rows of the matrix **A**.

A *lower-triangular* matrix **L** has all strictly zero elements above the main diagonal, i.e. $l_{i,j>i} = 0$. An *upper-triangular* matrix **U** has all strictly zero elements below the main diagonal, i.e. $u_{i,j<i} = 0$. In the both cases the determinant is the product of all main diagonal elements, i.e. $\mathtt{det}(\mathbf{L}) = \prod_{i=1}^N{l_{i,i}}$ and $\mathtt{det}(\mathbf{U}) = \prod_{i=1}^N{u_{i,i}}$. The *LU-decomposition* of a matrix **A** is a process of finding a lower-triangular matrix **L** and an upper-triangular matrix **U** such that **A** = **L** \* **U**. In practice, considering the numerical stability and singular matrices (det(**A**) =0), the columns and rows pivoting is applied, i.e. $\mathbf{A} \; \rightarrow \; \mathbf{B} = \mathbf{P}_c * \mathbf{A} * \mathbf{P} \; : \; \mathbf{B} = \mathbf{L} * \mathbf{U}$, hence a matrix **A** can be decomposed into a product of permutation matrices, lower- and upper-triangular matrices, which generalized decomposition process is named *LUP-decomposition*. If the process results in all unity main diagonal elements of the lower-diagonal matrix $l_{i,i}=1 \; \forall \; i$, the determinant of the matrix **A** is $\mathtt{det}(\mathbf{A}) = \pm \mathtt{det}(\mathbf{U}) = \pm \prod_{i=1}^N{u_{i,i}}$, with the sign defined by the product of the determinants of the both permutation matrices, which is the product of the signs of the both column and row permutations. Thus, LUP-decomposition is a powerful technique for calculation of the determinant and solution of a system of linear equations (using back-substitution method).

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

However, it is possible to produce the zero value at the main diagonal after some *k*-1 steps $a_{k,k}^{(k-1)} = 0$ even if the matrix **A** is not *singular* (i.e. $\mathtt{det}(\mathbf{A}) \neq 0$, or all rows of the matrix are linearly independent). If the matrix is not singular, there must be, at least, one element in the *k*-th row, which is not yet zeroed, i.e., $\exists \; i>k \; : \; a_{i,k}^{(k-1)} \neq 0$. Hence, one can swap the *k*-th and *i*-th columns (columns pivoting process) to get a non-zero value at the main diagonal. Such pivoting is described by the matrix multiplication $\mathbf{P}_k * \mathbf{A}^{(k-1)}$, with the permutation matrix $\mathbf{P}_k$ being generated by the $\{1, 2, \dots, k-1, i, k+1, \dots, i-1, k, i+1, \dots, N-1, N \}$ permutation of the 1..*N* set. Because of the strict relation $i > k$ this process does not affect the already calculated values of the $\mathbf{L}^{-1}$ matrix, thus it can be applied to the original matrix even before the first step of the elimination process, i.e., $\mathbf{A}^{(k-1)} \rightarrow \mathbf{A}^{(k)} = \mathbf{L}_k * (\mathbf{P}_k * \mathbf{A}^{(k-1)}) = \mathbf{L}_k * (\mathbf{P}_k * (\mathbf{L}_{k-1} * \dots * \mathbf{L}_2 * \mathbf{L}_1 * \mathbf{A}^{(0)})) = \mathbf{L}_k * \mathbf{L}_{k-1} * \dots * \mathbf{L}_2 * \mathbf{L}_1 * (\mathbf{P}_k * \mathbf{A}^{(0)})$. Basically, all required columns pivotings can be applied to the matrix beforehand and defined as a single permutation matrix: $\mathbf{A} \rightarrow \mathbf{B} = \mathbf{P}_c * \mathbf{A} = \mathbf{L}^{-1} * \mathbf{U} \; \Rightarrow \; \mathbf{A} = \mathbf{P}_c^{-1} * \mathbf{L}^{-1} * \mathbf{U}$, where $\mathbf{P}_c^{-1} = \mathbf{P}_c^T$.

Note, that $\mathtt{det}(\mathbf{P}_c^{-1}) = \pm 1$, with each columns pivoting inverting the sign of the determinant of the resulting matrix **U**.

In the numerical implementation of the method the columns pivoting can be applied at each step, even if the value of the diagonal elements is not zero. Basically, at each step the column is selected with the highest *absolute* value of an element at the intersection with the current *k*-th row, and the current *k*-th column is swapped with the selected column. This approach is beneficial for the numerical stability, since at each step tha maximum possible absolute value of the divider in the scaling coefficient is chosen. In practice, there is no need to physically swap elements of a matrix. Instead, the columns pivoting can be traced using *N*-sized vector / array, instantiated with 1 .. *N* set values, and the current *k*-th and *i*-th elements being swapped when *k*-*i* columns pivoting has to be applied. This vector / array is used as a *look-up* table for the column index resolution. Also, there is no practical reason to generate and return the corresponding matrix. thus the generated columns permutation array is returned instead. Also, the permutation sign is traced, starting with +1, and the sign is flipped (+1 to -1 and vice versa) with each pivoting applied (unless the current diagonal element is the maximum absolute value in the row, in which case the pivoting is not applied).

In a case of a singular matrix a *k*-th row becomes all-zeroes at the *k*-th step. Unless it is the last row, and there, at least, one row below, which contains, at least, one non-zero element, the rows pivoting must be applied, i.e. swap of two rows - the current and one below it. As with the columns pivoting, the rows pivoting is implemented via cloumns permutation vector / array look-up table. However, physical swapping of the already calculated elements of the $\mathbf{L}^{-1}$ matrix must be applied concerning the respective *k*-th and *i*-th rows (*i* > *k*), but only the elements at the intersection with the columns from the 1-st to the (*k*-1)-th. Also, the produced matrix **U** is not strictly upper-triangular matrix (with all non-zero elements on the main diagonal), but is in the *row echelon* form, with the non-zero elements only at or above the main diagonal, but with one or more rows at the bottom containing only zeroes.

Thus, in the general case, both the columns and rows pivoting is applied, i.e. $\mathbf{A} \rightarrow \mathbf{B} = \mathbf{P}_c * \mathbf{A} * \mathbf{P}_r= \mathbf{L}^{-1} * \mathbf{U} \; \Rightarrow \; \mathbf{A} = \mathbf{P}_c^{-1} * \mathbf{L}^{-1} * \mathbf{U} * \mathbf{P}_r^{-1}$, which is the implemented LUP-decomposition method. **Note**, that for a non-singular (invertible) matrix the rows pivoting is not applied, hence $\mathbf{P}_r = \mathbf{P}_r^{-1} = \mathbf{I}$, unless det(**A**) = 0.

For a non-singular matrix **A** the produced upper-triangular matrix **U** can be decomposed further into a product of an upper-triangular matrix with all 1s at the main diagonal and a diagonal matrix **D** as $\mathbf{U} = \hat{\mathbf{U}}^{-1} * \mathbf{D}$, i.e. $\mathbf{A} = \mathbf{P}_c^{-1} * \mathbf{L}^{-1} * \hat{\mathbf{U}}^{-1} * \mathbf{D}$, where matrix $\hat{\mathbf{U}}$ describes the secondary elimination (*k*-th row is subtracted from each row above with a specific coefficient, thus zeroing all elements above the diagonal in the *k*-th column). **Note**, that in the case of a singular matrix this *full decomposition* fails to produce a diagonal matrix **D**: one or more left-most columns will (or may) contain non-zero elements above the main diagonal. However, the major application of such full decomposition is the calculation of the inverse matrix, in which case the matrix must be non-singular.

## API Reference

### Class Array2D

### Class Vector

### Class Column

### Class Row

### Class Matrix

### Class SquareMatrix
