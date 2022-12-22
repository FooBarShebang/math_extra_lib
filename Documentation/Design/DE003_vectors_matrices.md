# Design of the implementation of the vector and matrix classes

## Generic / abstract vector

On the basic level a *vector* is a quantity, which cannot be expressed by a single number (a *scalar*), by a combination of such scalar values. Thus, conceptually, a vector is an *ordered finite collection* of elements (i.e. a *finite sequence*, like a *tuple* or an *array* of fixed length). The number *N* of the elements constituting an array is its *size* or *length*.

Thus, an N-vector **v** is defined by its elements $\mathbf{v} = (v_1, v_2, \dots, v_N)$. All possible N-vectors form an infinite *set* $V_N$. Within this set a binary operation of *addition* (or *sum*) can be defined, which produces a vector in $V_N$ from any two vectors in the same set, i.e. $\forall \; \mathbf{v}, \mathbf{w} \in V_N \; \exists \; \mathbf{u} \in V_N \; : \; \mathbf{v} + \mathbf{w} = \mathbf{u}$. In relation to a scalar *field F* (e.g. real numbers) a binary operation of *scalar multiplication* can be defined, which produces a vector in $V_N$ from any vector in the same set and a scalar from the field *F*, i.e. $\forall \; a \in F, \; \mathbf{v} \in V_N \; \exists \; \mathbf{u} \in V_N \; : a * \mathbf{v} = \mathbf{u}$.

A *vector space* over a field *F* is a set $V_N$ with these two binary operations if they satisfy the following 8 axioms:

* *Associativity* of vector addition $\mathbf{u} + (\mathbf{v} + \mathbf{w}) = (\mathbf{u} + \mathbf{v}) + \mathbf{w}$
* *Commutativity* of vector addition $\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}$
* Existance of *identity element* (zero vector) of vector addition $\exists \; \mathbf{0} \in V_N \; : \mathbf{v} + \mathbf{0} = \mathbf{v} \; \forall \; \mathbf{v} \in V_N$
* Existance of *inverse element* of vector addition $\forall \; \mathbf{v} \in V_N \; \exists \; -\mathbf{v} \in V_N \; : \; \mathbf{v} + (- \mathbf{v}) = \mathbf{0}$
* Compatibility of scalar multiplication with field multiplication $a * (b * \mathbf{v}) = (a * b) * \mathbf{v}$
* Multiplicative identity *1* in *F* is also the *identity element* of scalar multiplication $\mathit{1} * \mathbf{v} = \mathbf{v}$
* *Distributivity* of scalar multiplication with respect to vector addition $a * (\mathbf{v} + \mathbf{u}) = a * \mathbf{v} + a * \mathbf{u}$
* *Distributivity* of scalar multiplication with respect to field addition $(a + b) * \mathbf{v} = a * \mathbf{v} + b * \mathbf{v}$

The direct consequences of these requirements are:

* Vector subtraction operation definition is $\mathbf{v} - \mathbf{w} = \mathbf{v} + (- \mathbf{w})$
* $\mathit{0} * \mathbf{v} = \mathbf{0} \; \forall \; \mathbf{v} \in V_N$, where *0* is the identity element of field addition ($a + \mathit{0} = a \; \forall \; a \in F$)
* $a * \mathbf{0} = \mathbf{0} \; \forall \; a \in F$
* $-\mathbf{v} = (-\mathit{1}) * \mathbf{v}$

Considering the field of *real number* the *per element* definitions of the vector addition and scalar multiplication as given below apparently satisfy these requirements:

* $\mathbf{v} + \mathbf{u} = (v_1, v_2, \dots, v_N) + (u_1, u_2, \dots, u_N) = (v_1 + u_1, v_2 + u_2, \dots, v_N + u_N)$
* $a * \mathbf{v} = a * (v_1, v_2, \dots, v_N) = (a * v_1, a * v_2, \dots, a * v_N)$

with the zero vector being $\mathbf{0} = (0, 0, \dots, 0)$. Hence, the commutativity of the scalar multiplication can be postulated *ad hoc*, i.e. $a * \mathbf{v} \equiv \mathbf{v} * a$, and division of a vector by a scalar can be defined as $\mathbf{v} / a = \frac{1}{a} * \mathbf{v} \; \forall \; a \neq 0$.

Furthermore, two additional binary operations can be defined: *inner product* (or *dot product*) and *outer product* - which are not part of the vector space.

The dot product is a scalar value defined as $\mathbf{v} \cdot \mathbf{u} = v_1 * u_1 + v_2 * u_2 + \dots + v_N * u_N$ - i.e. the sum of products of the same index / position elements of the both vectors. Apparently, the both vectors must be of the same length, i.e. belong to the same vector space.

The outer product yields a 2-dimensional array (or a matrix) and is applicable to any two vectors, even from the different vector spaces, i.e. of the different length. The (i, j)-th element of the resulting array, i.e. the element at the intersection of the i-th column and j-th row being a product of the j-th element of the left operand and the i-th element of the right operand, $(\mathbf{u} \otimes \mathbf{v})_{i,j} = u_j * v_i$. In the full form for $\mathbf{u} \in V_M$ and $\mathbf{v} \in V_N$ it is given as:

$$
\mathbf{u} \otimes \mathbf{v} = \begin{bmatrix}
u_1 v_1 & u_1 v_2 & \dots & u_1 v_N \\
u_2 v_1 & u_2 v_2 & \dots & u_2 v_N \\
\vdots & \vdots & \ddots & \vdots \\
u_M v_1 & u_M v_2 & \dots & u_M v_N
\end{bmatrix} = \begin{bmatrix}
u_1 * \begin{bmatrix} v_1 & v_2 & \dots & v_N \end{bmatrix} \\
u_2 * \begin{bmatrix} v_1 & v_2 & \dots & v_N \end{bmatrix} \\
\vdots \\
u_M * \begin{bmatrix} v_1 & v_2 & \dots & v_N \end{bmatrix}
\end{bmatrix} = \\
\begin{bmatrix}
v_1 * \begin{bmatrix} u_1 \\ u_2 \\ \vdots \\ u_M\end{bmatrix} &
v_2 * \begin{bmatrix} u_1 \\ u_2 \\ \vdots \\ u_M\end{bmatrix} &
\dots &
v_N * \begin{bmatrix} u_1 \\ u_2 \\ \vdots \\ u_M\end{bmatrix}
\end{bmatrix}
$$

Given those properties, a generic / abstract vectors can be implemented as a *hybrid* class, combining some properties and functionality of the both *immutable sequence* and *numeric types* in Python, thus supporting the standard indexing and arithmetics notation as is summarized in the table below.

| Operation          | Notation | 'Magic' method    |
| ------------------ | -------- | ----------------- |
| element access     | a[i]     | \_\_getitem\_\_() |
| vector addition    | a + b    | \_\_add\_\_()     |
| vector subtraction | a - b    | \_\_sub\_\_()     |
| scalar x vector    | a * b    | \_\_rmul\_\_()    |
| vector x scalar    | a * b    | \_\_mul\_\_()     |
| vector / scalar    | a / b    | \_\_truediv\_\_() |
| dot product        | a * b    | \_\_mul\_\_()     |
| outer product      | a @ b    | \_\_matprod\_\_() |

Note, that neither the iterator protocol (as in `for a in b`) nor the element presence check protocol (as in `if a in b`) are required, since a vector is supposed to be treated as a single entity, with the 'read-only' element access being provided only for convenience.

Such generic / abstract vectors are the basis, the foundation for the specialized classes like *column* and *row vector*, as well as *geometric vectors*, which represent quantities with both magnitude and direction both in geometry and physics.

## Column and row vectors

The *column* and *row vectors* are specific cases of the generic vectors, representing columns and rows of matrices respectively, as well as vector elements from some vector spaces, for which some matrix defines *linear mapping* onto the same or another vector space.

A column vector is (visually) represented as

$$
\mathbf{v} = \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_N \end{bmatrix}
$$

whereas a row vector as

$$
\mathbf{v}^T = \begin{bmatrix} v_1 & v_2 & \dots & v_N \end{bmatrix}
$$

Considering the column and row vectors of the same length N, they form two identical but separate vector spaces $V_N$ and $V_N^T$, which are related to each by the operation of *tansposition*, i.e. $\forall \; \mathbf{v} \in V_N \; \exists \; \hat{\mathbf{w}} = \mathbf{v}^T \in V_N^T \; : \; \hat{w}_i = v_i \; \forall \; 1 \leq i \leq N$. Therefore

$$
\mathbf{v} = \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_N \end{bmatrix} = {\begin{bmatrix} v_1 & v_2 & \dots & v_N \end{bmatrix}}^T = (\mathbf{v}^T)^T
$$

The addition and subtraction is allowed (defined) only within the respective vector space (between two column vectors of the same length, or between two row vectors of the same length, but not mixing them up). The inner and outer products do not have a lot of sense or application with respect to a single vector space concerning column and row vectors, but can be used for implementation of column x row and row x column vector multiplication as $\mathbf{v}^T * \mathbf{u} = \mathbf{v} \cdot \mathbf{u}$ and $\mathbf{u} * \mathbf{v}^T = \mathbf{u} \otimes \mathbf{v}$.

Therefore, both the column vectors and the row vectors can be implemented as sub-classes of the generic vector with minor modifications (polymorthism) of the 'magic' methods for the multiplication. Specifically

| Operation       | Notation | 'Magic' method                 | Result |
| --------------- | -------- | ------------------------------ | ------ |
| column + column | a + b    | \_\_add\_\_()                  | column |
| column - column | a - b    | \_\_sub\_\_()                  | column |
| row + row       | a + b    | \_\_add\_\_()                  | row    |
| row - row       | a - b    | \_\_sub\_\_()                  | row    |
| column x row    | a * b    | \_\_mul\_\_() / \_\_rmul\_\_() | matrix |
| row x column    | a * b    | \_\_mul\_\_() / \_\_rmul\_\_() | scalar |
| column x scalar | a * b    | \_\_mul\_\_()                  | column |
| scalar x column | a * b    | \_\_rmul\_\_()                 | column |
| column / scalar | a / b    | \_\_div\_\_()                  | column |
| scalar x row    | a * b    | \_\_rmul\_\_()                 | row    |
| row x scalar    | a * b    | \_\_mul\_\_()                  | row    |
| row / scalar    | a / b    | \_\_div\_\_()                  | row    |

whereas neither of the column and row vector classes should support multiplication (left or right) by a generic vector. The *explicit* outer product (via Python @ operator) can be preserved, accepting any type vectors as the both operands.

## Matrix

Conceptually, a matrix of the size N x K is a table consisting of N columns and K rows, which can also be represented as a column of K elements, each being row N-vector, or as a row of N elements, each being column K-vector.

$$
\mathbf{A} = \begin{bmatrix}
a_{1,1} & a_{2,1} & \dots & a_{N,1} \\
a_{1,2} & a_{2,2} & \dots & a_{N,2} \\
\vdots & \vdots & \ddots & \vdots \\
a_{1,K} & a_{2,K} & \dots & a_{N,K} \\
\end{bmatrix} = \begin{bmatrix}
\begin{bmatrix} a_{1,1} & a_{2,1} & \dots & a_{N,1} \end{bmatrix} \\
\begin{bmatrix} a_{1,2} & a_{2,2} & \dots & a_{N,2}  \end{bmatrix} \\
\vdots \\
\begin{bmatrix} a_{1,K} & a_{2,K} & \dots & a_{N,K} \end{bmatrix} \\
\end{bmatrix} = \begin{bmatrix}
\mathbf{a}_{\cdot, 1} \\ \mathbf{a}_{\cdot, 2} \\ \vdots \\ \mathbf{a}_{\cdot, K}
\end{bmatrix} = \\
\begin{bmatrix}
\begin{bmatrix} a_{1,1} \\ a_{1,2} \\ \vdots \\ a_{1, K} \end{bmatrix} &
\begin{bmatrix} a_{2,1} \\ a_{2,2} \\ \vdots \\ a_{2, K} \end{bmatrix} &
\dots &
\begin{bmatrix} a_{N,1} \\ a_{N,2} \\ \vdots \\ a_{N, K} \end{bmatrix}
\end{bmatrix} = \begin{bmatrix} \mathbf{a}_{1,\cdot}^T & \mathbf{a}_{2,\cdot}^T & \dots \mathbf{a}_{N,\cdot}^T \end{bmatrix}
$$

However, unlike simle tables, matrices can be manipulated as single entities in arithmetic operations.

Scalar multiplication

$$
b * \mathbf{A} = \mathbf{A} * b= \begin{bmatrix}
b * a_{1,1} & b * a_{2,1} & \dots & b * a_{N,1} \\
b * a_{1,2} & b * a_{2,2} & \dots & b * a_{N,2} \\
\vdots & \vdots & \ddots & \vdots \\
b * a_{1,K} & b * a_{2,K} & \dots & b * a_{N,K} \\
\end{bmatrix}
$$

hence, a division of a matrix by a scalar can be defined via multiplication as $\mathbf{A} / b = \frac{1}{b} * \mathbf{A}$.

Addition can be performed only between two matrices of the same size N x K as

$$
\mathbf{A} + \mathbf{B} = \begin{bmatrix}
a_{1,1} + b_{1,1} & a_{2,1} + b_{2,1} & \dots & a_{N,1} + b_{N,1} \\
a_{1,2} + b_{1,2} & a_{2,2} + b_{2, 2} & \dots & a_{N,2} + b_{N,2} \\
\vdots & \vdots & \ddots & \vdots \\
a_{1,K} + b_{1, K} & a_{2,K} + b_{2,K} & \dots & a_{N,K} + b_{N,K} \\
\end{bmatrix}
$$

Then, the same properties of arithmetics exist as for vectors:

* *Associativity* of matrix addition $\mathbf{A} + (\mathbf{B} + \mathbf{C}) = (\mathbf{A} + \mathbf{B}) + \mathbf{C}$
* *Commutativity* of matrix addition $\mathbf{A} + \mathbf{B} = \mathbf{B} + \mathbf{A}$
* Existance of *identity element* (zero matrix) of matrix addition $\exists \; \mathbf{0}_{NK} \; : \mathbf{A} + \mathbf{0}_{NK} = \mathbf{A}$, in which all elements are zeroes
* Existance of *inverse element* of matrix addition $\forall \; \mathbf{A} \; \exists \; -\mathbf{A} = (-1) * \mathbf{A} \; : \; \mathbf{A} + (- \mathbf{A}) = \mathbf{0}_{NK}$
* Compatibility of scalar multiplication with numbers multiplication $a * (b * \mathbf{A}) = (a * b) * \mathbf{A}$
* Existance of *identity element* of scalar multiplication $1 * \mathbf{A} = \mathbf{A}$
* *Distributivity* of scalar multiplication with respect to matrix addition $a * (\mathbf{A} + \mathbf{B}) = a * \mathbf{A} + a * \mathbf{B}$
* *Distributivity* of scalar multiplication with respect to numbers addition $(a + b) * \mathbf{A} = a * \mathbf{A} + b * \mathbf{A}$

The direct consequences of these requirements are:

* Matrix subtraction operation definition is $\mathbf{A} - \mathbf{B} = \mathbf{A} + (- \mathbf{B})$
* $0 * \mathbf{A} = \mathbf{0}_{NK}$
* $a * \mathbf{0}_{NK} = \mathbf{0}_{NK} \; \forall \; a$

However, additional operations are also defined.

Multiplication of N x K matrix by column K-vector results in a column N-vector as

$$
\mathbf{A} * \mathbf{v} = \begin{bmatrix}
a_{1,1} & a_{2,1} & \dots & a_{N,1} \\
a_{1,2} & a_{2,2} & \dots & a_{N,2} \\
\vdots & \vdots & \ddots & \vdots \\
a_{1,K} & a_{2,K} & \dots & a_{N,K} \\
\end{bmatrix} * \begin{bmatrix} v_1 \\ v_2 \\ \vdots \\ v_N\end{bmatrix} = \begin{bmatrix}
a_{1,1} * v_1 + a_{2,1} * v_2 + \dots + a_{N,1} * v_N \\
a_{1,2} * v_1 + a_{2,2} * v_2 + \dots + a_{N,2} * v_N \\
\vdots \\
a_{1,K} * v_1 + a_{2,K} * v_2 + \dots + a_{N,K} * v_N
\end{bmatrix}
$$

Multiplication of row K-vector by N x K matrix results in a row N-vector as

$$
\mathbf{v}^T * \mathbf{A} = \begin{bmatrix} v_1 & v_2 & \dots & v_k\end{bmatrix} * \begin{bmatrix}
a_{1,1} & a_{2,1} & \dots & a_{N,1} \\
a_{1,2} & a_{2,2} & \dots & a_{N,2} \\
\vdots & \vdots & \ddots & \vdots \\
a_{1,K} & a_{2,K} & \dots & a_{N,K} \\
\end{bmatrix} = \\
\begin{bmatrix}
(v_1 * a_{1,1} + \dots + v_K * a_{1,K}) & (v_1 * a_{2,1} + \dots + v_K * a_{2,K}) & \dots & (v_1 * a_{N,1} + \dots + v_K * a_{N,K})
\end{bmatrix}
$$

Finally, multiplication of matrix **A** (size N x K) by a matrix **B** (size M x N) is defined only if the width of the left operand is equal to the height of the rigth operand, and it results in M x K matrix, with the following per element defintion

$$
\mathbf{A}_{NK} * \mathbf{B}_{MN} = \mathbf{C}_{MK} \; : \; c_{i,j} = a_{1,j} * b_{i,1} + a_{2,j} * b_{i,2} + \dots + a_{N,j} * b_{i,N} \; \forall \; 1 \leq i \leq M, 1 \leq j \leq K
$$
