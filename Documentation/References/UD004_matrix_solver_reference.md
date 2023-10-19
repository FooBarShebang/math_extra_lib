# Module math_extra_lib.matrix_solver Reference

## Scope

This document describes the intended usage, design and implementation of the functionality implemented in the module **matrix_solver** of the library **math\_extra\_lib**. The API reference is also provided.

The functional objects covered in this document are:

* function *FindEigenvector*()
* function *SolveLinearSystem*()

## Intended Use and Functionality

This module provides two functions to find a real *eigenvalue* of a real matrix and to solve a *determinate* system of linear equations respectively.

A value $\lambda$ is an *eigenvalue* of a (square) matrix **A** is there exists a *non-zero* vector **v** such that $\mathbf{A}*\mathbf{v} = \lambda * \mathbf{v}$. Note, that the method *getEigenValues*() of the class **SquareMatrix** in the module *math\_extra.vectors\_matrices* attempts to find all eigenvalues of the matrix simultaneosly (see [UD003](./UD003_vectors_matrices_reference.md) document), however it uses the [QR agorithm](https://en.wikipedia.org/wiki/QR_algorithm), which works only for the *diagnonalizable* (not defective) matrices. The function *FindEigenvector*() in this module finds only one real non-zero eigenvalue of a matrix using the [power iteration](https://en.wikipedia.org/wiki/Power_iteration) method, which yields the *dominant* (largest absolute value) *eigenvalue* of the matrix, unless the initial guess was already an *eigenvector* associated with a different *eigenvalue* of the same matrix.

The found eigenvalue can be passed as a keyword argument into the method *getEigenVectors*() of the class **SquareMatrix**, which will attempt to generate an orthonormal vectors basis of the respective eigenspace.

The second function implemented in this module, *SolveLinearSystem*() attempts to solve a system of linear equations, which (for *N* variables and *N* equations) is written as:

$$
\begin{cases}
a_{1,1}*x_1 \; + \; a_{2,1}*x_2  \; + \; \dots \; + \; a_{N-1,1}*x_{N-1} \; + \; a_{N,1}*x_N \; &= \; c_1 \\
a_{1,2}*x_1 \; + \; a_{2,2}*x_2  \; + \; \dots \; + \; a_{N-1,2}*x_{N-1} \; + \; a_{N,2}*x_N \; &= \; c_2 \\
\dots \\
a_{1,N-1}*x_1 \; + \; a_{2,N-1}*x_2  \; + \; \dots \; + \; a_{N-1,N-1}*x_{N-1} \; + \; a_{N,N-1}*x_N \; &= \; c_{N-1} \\
a_{1,N}*x_1 \; + \; a_{2,N}*x_2  \; + \; \dots \; + \; a_{N-1,N}*x_{N-1} \; + \; a_{N,N}*x_N \; &= \; c_N \\
\end{cases}
$$

or in a matrix form

$$
\begin{bmatrix}
a_{1,1} & a_{2,1} & \dots & a_{N-1,1} & a_{N,1} \\
a_{1,1} & a_{2,1} & \dots & a_{N-1,1} & a_{N,1} \\
\vdots & \vdots & \ddots & \vdots & \vdots \\
a_{1,N-1} & a_{2,N-1} & \dots & a_{N-1,N-1} & a_{N,N-1} \\
a_{1,N} & a_{2,N} & \dots & a_{N-1,N} & a_{N,N} \\
\end{bmatrix} * \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{N-1} \\ x_N\end{bmatrix} = \begin{bmatrix} c_1 \\ c_2 \\ \vdots \\ c_{N-1} \\ c_N\end{bmatrix} \Leftrightarrow \mathbf{A} * \mathbf{x} = \mathbf{c}
$$

This system is determinate, i.e. it has a single solution, if $\mathtt{det}(\mathbf{A})\neq0$, in which case the solution is $\mathbf{x} = \mathbf{A}^{-1}*\mathbf{c}$. The class **SquareMatrix** has a method *getInverse*() to find the inverse matrix, however this approach is more prone to the numerical error accumulation and slightly slower than *Gauss-Jordan* elimination and back-substitution method due to larger number of the floating point operations involved.

In the matrix form the Gauss-Jordan elimination is give by the left multiplication with a transformation matrix **T**, which transforms the matrix **A** into an upper-triangular matrix **B** with all non-zero diagonal elements, i.e. $\mathbf{A} \rightarrow \mathbf{B} = \mathbf{T} * \mathbf{A}$. Simultaneous application of the same transformation matrix to the free coefficients column vector **c** transforms it as $\mathbf{c} \rightarrow \mathbf{d} = \mathbf{T} * \mathbf{c}$. Obviously, $\mathbf{T} * \mathbf{A} * \mathbf{x} = \mathbf{T} * \mathbf{c} \Leftrightarrow\mathbf{B} * \mathbf{x} = \mathbf{d}$, hence the initial system is transformed into

$$
\begin{cases}
b_{1,1}*x_1 \; + \; b_{2,1}*x_2  \; + \; \dots \; + \; b_{N-1,1}*x_{N-1} \; + \; b_{N,1}*x_N \; &= \; d_1 \\
b_{2,2}*x_2  \; + \; \dots \; + \; b_{N-1,2}*x_{N-1} \; + \; b_{N,2}*x_N \; &= \; d_2 \\
\dots \\
b_{N-1,N-1}*x_{N-1} \; + \; b_{N,N-1}*x_N \; &= \; d_{N-1} \\
b_{N,N}*x_N \; &= \; d_N \\
\end{cases}
$$

The last variable value is $x_N = \frac{d_N}{b_{N,N}}$, and the values of the rest variables are found using the recursive relation $x_{k<N} = \frac{d_k - \sum_{i=k+1}^N{b_{i,k}*x_i}}{b_{k,k}}$, which is the back-substitution method.

Thus, the function *SolveLinearSystem*() takes the bound coefficients $a_{i,j}$ of the system and the free coefficients $c_j$ and calculates the solution as a sequence of the $x_j$ values using the Gauss-Jordan elimination and back-substitution. The free coefficients can be passed as a flat sequence (**list** or **tuple** Python types) of real numbers (**int** or **float** Python types) or as an instance of the **Column** class (see [UD003](./UD003_vectors_matrices_reference.md) document). The bound coefficients may be passed as:

* an instance of the **SquareMatrix** class (size *N*, i.e. N x N elements)
* a sequence of *N* sub-sequences of *N* real numbers each, e.g. $[[a_{1,1}, \dots, a_{N,1}], \dots, [a_{1, N}, \dots, a_{N,N}]]$
* a flat sequence of $N^2$ real numbers, e.g. $[a_{1,1}, \dots, a_{N,1}, a_{1,2}, \dots, a_{N, N-1}, a_{1, N}, \dots, a_{N,N}]$

Below is an example of usage of the module

```python
from math_extra.matrix_solver import FindEigenvalue, SolveLinearSystem
from math_extra.matrix_solver import SquareMatrix

Matrix = SquareMatrix([[1, 1],[0, 2]])
Eigenvalue = FindEigenvalue(Matrix)
print(Eigenvalue) #>>> 2

#solution of the linear equations system
#+ {  2x + y -  z = 8
#+ { -3x - y + 2z = -11
#+ { -2x + y + 2z = -3
#+
#+ solution is x = 2, y = 3, z = -1

Solution = SolveLinearSystem([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]],
                                [8, -11, -3])
print(Solution) #>>> [2.0, 3.0, -1.0]
```

## Design and Implementation

The essence of the *power iteration method* is in the relation $\mathbf{A} * \mathbf{v} = \lambda * \mathbf{v} \Rightarrow \mathbf{A} * \dots * \mathbf{A} * \mathbf{v} = \mathbf{A}^N * \mathbf{v} = \lambda^N * \mathbf{v}$. Consider a matrix with *K* distinct real eigenvalues sorted by the absolute values $|\lambda_1| > |\lambda_2| > \dots > |\lambda_K|$ and a vector **w**, which is a linear composition of the eigen vectors $\mathbf{v}_i \; : \; \mathbf{A} * \mathbf{v}_i = \lambda_i * \mathbf{v}_i$, i.e. $\mathbf{w} = \sum_{i=1}^K{c_i * \mathbf{v}_i}$. Obviously, after large enough number N of multiplications $\mathbf{A}^N * \mathbf{w} = \sum_{i=1}^K{\lambda_i^N * c_i * \mathbf{v}_i}$ the component aligned with the vector $\mathbf{v}_1$ bound to the eigenvalue $\lambda_1$ dominates, in other words the resulting vector aligns with the $\mathbf{v}_1$, i.e. $\lim_{N\rightarrow \infty}{(\mathbf{A}^N * \mathbf{w})} \parallel \mathbf{v}_1$.

Thus, the power iteration method operates as follows. Generate a random vector $\mathbf{w}_1$ of a unity length, i.e. $||\mathbf{w}_1||=1$. Calculate the product $\mathbf{A}*\mathbf{w}_1$ and normalize it to the unity length. Repeat iteratively $\mathbf{w}_{k+1} = \frac{\mathbf{A}*\mathbf{w}_k}{||\mathbf{A}*\mathbf{w}_k||}$ until the sequence converges with a desired accuracy $\mathbf{w}_{k+1} \approx \mathbf{w}_k \equiv ||\mathbf{w}_{k+1} - \mathbf{w}_k|| < \delta$. In practice, the convergence is judged using the Rayleigh quotient $R_k = \frac{\mathbf{w}_k^T * \mathbf{A} * \mathbf{w}_k}{||\mathbf{w}_k||} = \frac{\mathbf{w}_k^T * \mathbf{w}_{k+1}}{||\mathbf{w}_k||}$, which is the amplitude of the projection of the vector $\mathbf{w}_{k+1}$ onto the vector $\mathbf{w}_k$. Hence, $\lim_{k \rightarrow \infty}(R_k) = \lambda_1$, and the convergence criterium is $|R_{k} - R_{k-1}| < \varepsilon * |R_{k-1}|$.

If a square matrix **A** of the size *N* is *diagonalizable* over the real numbers field any initial guess vector **w** can be decomposed into such linear combination of eigenvectors from one to more eigenspaces (see [this article](https://en.wikipedia.org/wiki/Diagonalizable_matrix) for details), and the method converges *geometrically* with the ratio $|\lambda_2| / |\lambda_1|$. For a *defective* over real numbers matrix the sum of the dimensions of the eigenspaces (over real numbers) is less than the dimension of the matrix, and the initial guess vector may contain a component outside the eigenspaces of the matrix. In this case the method may converge very slowly or do not converge at all.

For example, consider a *shear* matrix $\begin{bmatrix}1 & 1 \\ 0 & 1\end{bmatrix}$, which is not singular and has a single eigenvalue $\lambda = 1$ with algebraic multiplicity of 2 and geometric multiplicity of 1 (i.e. all of the eigenvectors are in the form $\begin{bmatrix}a \\ 0\end{bmatrix}$). On average it takes ~ $10^5$ iterations to achive the error in the eigenvalue approximation $< 10^{-5}$, whereas in the case of the matrix $\begin{bmatrix}1 & 1 \\ 0 & 2\end{bmatrix}$ the method converges to the value $2 + \delta \; : \; \delta <10^{-5}$ in about 20 iterations. Note, that the eigenvalues and eigenvectors in this case are $\lambda_1 = 2 \rightarrow \begin{bmatrix} a \\ a\end{bmatrix}$ and $\lambda_2 = 1 \rightarrow \begin{bmatrix} b \\ 0\end{bmatrix}$. Therefore, a limit on the maximum number of iterations $10^6$ is applied in the function *FindEigenvalue*() in addition to the Rayleigh quotient convergence criterium $\varepsilon = 10^{-12}$. If the desired level of the convergence is not acheived, the function returns **None** value. Also the found eigenvalue is rounded to the nearest integer, if the eigenvalue differs from it by no more than $10^{-4}$.

The singular matrices (det(**A**)=0) pose another potential problem. The sum of all eigenvalues of a matrix **A** (counting with the algebraic multiplicity) is the trace of the matrix, whereas their product is the determinant of the matrix: $\mathtt{tr}(\mathbf{A}) = \sum_{i=1}^K{\gamma_i * \lambda_i}$ and $\mathtt{det}(\mathbf{A}) = \prod_{i=1}^K{\lambda_i^{\gamma_i}}$, where *K* is the numebr of *distinctive* (unique) eigenvalues, and $\gamma_i$ is the algebraic multiplicity of the corresponding eigenvalue. Hence, the zero determinant of a matrix means that one of its eigenvalues is zero, although it may have one or more other non-zero eigenvalues even being real numbers. The same conclusion is also obvious from the equation generating the characteristic polynomial $\mathtt{det}(\mathbf{A} - 0 * \mathbf{I}) = 0 \Rightarrow \mathtt{det}(\mathbf{A}) = 0$. The zero eigenvalue is singular, because the corresponding eigenvector **v** is transformed into the zero vector $\mathbf{A}*\mathbf{v} = 0 * \mathbf{v} = \mathbf{0}$, and the inverse transformation is not possible (undetermined as $1 \rightarrow \infty$), which is the reason why the matrix is not invertible, i.e. $\mathbf{A}^{-1}$ does not exists.

Consider the matrix $\mathbf{A} = \begin{bmatrix}1 & 1 \\ 1 & 1\end{bmatrix}$, with $\det(\mathbf{A})=0$. The characteristic polynomial is $(1-\lambda)^2-1=0$, which has two real solutions $\lambda_1=2$ and $\lambda_2=0$ with the corresponding eigenvectors $\begin{bmatrix}a \\ a \end{bmatrix}$ and $\begin{bmatrix}b \\ -b \end{bmatrix}$. With any initial guess vector $\begin{bmatrix}a \\ b\neq - a \end{bmatrix}$ after the first iteration the algorithm produces $\begin{bmatrix} \frac{a+b}{2|a+b|} \\ \frac{a+b}{2|a+b|} \end{bmatrix}$, thus the algorithm converges just after 2 iterations to $\lambda = 2$. However, if the initial guess is $\begin{bmatrix}a \\ -a \end{bmatrix}$ the product with the matrix results in the zero vector $\begin{bmatrix} 0 \\ 0 \end{bmatrix}$, which cannot be normalized. Since the purpose of the function *FindEigenvalue*() is to find a real non-singular eigenvalue the **None** value is returned. This example is trivial and very unlikely to happen, however in the case of large size matricies a nearly singular vector can be produced in one of the iteration steps, especially considering the accumulation of the numerical error.

Another weakness of the algorithm is related to the Rayleigh quotient. If the matrix represents a rotation with (optional) scaling in N-dimensional space, the said quotient converges after 2 iterations, but not to an eigenvalue. Consider the matrix $\mathbf{A} = \begin{bmatrix}a & -b \\ b & a\end{bmatrix}$, which is 2D vector space' rotation + scalling matrix, with the rotation angle $\phi \; : \; \cos(\phi) = \frac{a}{\sqrt{a^2+b^2}}, \sin(\phi) = \frac{b}{\sqrt{a^2+b^2}}$ and the scaling coefficient $\sqrt{a^2+b^2}$. The characteristic polynomial is $(a-\lambda)^2+b^2=0$, which has only complex roots (not real numbers): $\lambda_1=a -i*b$ and $\lambda_2=a+i*b$. The power iteration algorithm converges to the value of the quotient of $\sqrt{a^2+b^2}$ in a few steps, but $\mathbf{w}_{k+1} \not{\parallel} \mathbf{w}_k \; \forall k$. Therefore, upon the convergence of the quotient the parallelity of the vectors is also checked. If they are not approximately parallel (the ratio of all non-zero components is approximately equal to the value of the quotient) the **None** value is returned.

The function *FindEigenvalue*() employes the matrix x column multiplication and normalization of a vector functionality provided by the module *math\_extra.vectors\_matrices*.

The function *SolveLinearSystem*() relies on the LUP-decomposition method of the class **SquareMatrix** defined in the module *math\_extra.vectors\_matrices*, which returns a lower triangular matrix containing all transformation (rows subtraction) coefficients of the Gauss-Jordan elimination process, an upper triangular matrix containing the transformed bound coefficients (after the elimination) and the columns and rows permutations (pivoting). In a case of a singular matrix the returned upper triangular matrix has one or more bottom most rows with all zero elements (row echelon form), and the system of equations has no solution - the return value of the function is **None**. If the determinant of this upper triangular matrix, which is the product of the main diagonal elements, is non-zero, the system has a single solution, and the rows pivoting was not applied in the process of the LUP-decomposition, thus the rows permutations can be ignored. Further, each i-th column of the returned lower triangular matrix contains the coefficients of the elimination process below the i-th element of the main diagonal, thus the transformed free coefficients' vector can be calculated iteratively using a nested loop without use of the matrix x column multiplication and calculation of the actual transformation matrix.

Thus, the back-substituion algorithm can be applied directly to the returned upper triangular matrix and the calculated transformed free coefficients. However, it does not produce the solution vector directly. Because of the columns pivoting used in the LUP-decomposition for the numerical stability, the elements of the produced vector are shuffled (permutated) with respect to the true solution vector in the same order as the columns of the matrix have been pivoted. Hence, the reverse permutation is applied to the calculated vector, which process produces the true solution vector, which is returned by the function *SolveLinearSystem*().

## API Reference

### Functions

**FindEigenvector**(Matrix)

*Signature*:

**SquareMatrix** -> **int** OR **float** OR **None**

*Args*:

*Matrix*: **SquareMatrix**; instance of the class implementing a square matrix (see module *math\_extra.vectors\_matrices*)

*Returns*:

* **int** OR **float**: the found eigenvalue
* **None**: the matrix has no real number non-zero eigenvalue

*Raises*:

**UT_TypeError**: the passed argument is not an instance of SquareMatrix

*Description*:

Finds a real number eigenvalue of a square matrix using the power iteration method. The found eigenvalue, if exists, is most likely the highest absolute value one. It is possible (but highly unlikely) that the initial guess vector is in the eigenspace of a non-dominant eigenvalue, in which case the found eigenvalue is not the largest by the amplitude.

**SolveLinearSystem**(BoundCoeffs, FreeCoeffs)

*Signature*:

**SquareMatrix** OR **seq**(**seq**(**int** OR **float**)) OR **seq**(**int** OR **float**), **Column** OR **seq**(**int** OR **float**) -> **list**(**int** OR **float**) OR **None**

*Args*:

* *BoundCoeffs*: **SquareMatrix** OR **seq**(**seq**(**int** OR **float**)) OR **seq**(**int** OR **float**) ; the matrix of the bound coefficients of the system in the row-first order (see module *math\_extra.vectors\_matrices*)
* *FreeCoeffs*: **Column** OR **seq**(**int** OR **float**); the free coefficients of the system (see module *math\_extra.vectors\_matrices*)

*Returns*:

* **list**(**int** OR **float**): the found solution of the system
* **None**: the system is undertermined (no solution or multiple solutions)

*Raises*:

* **UT_TypeError**: the first argument is neigther an instance of **SquareMatrix** class nor a flat or nested sequence of real numbers, OR the second argument is neigther an instance of **Column** class nor a flat sequence of real numbers
* **UT_ValueError**: the content of the first argument (as a sequence) is incompatible with the initilization method of **SquareMatrix** class, OR the second argument (as a sequence) has less than 2 elements, OR the size of the free coefficients vector does not match the size of the bound coefficients matrix

*Description*:

Solves a system of linear equations using Gauss-Jordan elimination with rows / columns pivoting (LUP-decomposition) and back-substition.
