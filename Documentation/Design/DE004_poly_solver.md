# Polynomial interpolation of a function of a single variable and numerical method of finding all roots of a polynomial

## Background information - polynomial interpolation

Consider a real function of a single real variable $f(x)$ and the graphic of this function on the x-y plane $y=f(x)$. A *grid* or *mesh* of the x-values is an ordered set of *N* (unique) x-values $\{x_i\} \; : \; x_{i+1} > x_i \; \forall \; 1 \leq (i \in \mathbb{N})< N$. The mesh is *equidistant* (or uniform) if $\Delta x_i = x_{i+1} - x_i = \mathtt{const} \; \forall \; i$, and it is non-equidistant (not uniform) otherwise. On this mesh the function evaluates to the values $\{y_i\} \; : \; y_i = f(x_i) \; \forall \; i$. When one observes (measures) an output of some system at the several levels (values) of the input, or measures some signal at the various moments in time, the entire observation data can be represented as a set of pairs of the independent and dependent variables $\{(x_i, y_i)\}$. The actual function $f(x)$ describing the system response or the temporal evolution of the singal may be unknown or simply to complex / costly for practical calculations, in which case the actual function can be *interpolated* by another known and / or simpler function $F(x) \; : \; F(x_i) = f(x_i) = y_i \; \forall \; i$. Thus, the actual but unknown value of the function $f(x)$ at any value of the independent variable not being a *node* of the mesh $x\not\in\{x_i\}$ is approximated by the value of the interpolating function. Usually, those x-values lay between the nodes of the mesh (hence the name - interpolation), however the values of the interpolating function can be evaluated at the x-values outside the mesh (i.e. $x < x_1$ or $x > x_N$), although with a lesser degree of confidence, i.e. with a higher possible error. The second use case is called *extrapolation*.

For *N* observed pairs $\{(x_i, y_i)\}$ the interpolating function can be chosen as a polynomial of the *N-1* degree (see [DE001](./DE001_polynomials.md) document) $P^{N-1}(x) = \sum_{i=0}^{N-1}{a_i * x^i} = a_0 + a_1 * x + a_2 * x^2 + \dots a_{N-1}*x^{N-1}$, which has exactly *N* coefficients, which are found by solving a system of *N* linear equations $P^{N-1}(x_j) = y_j$ generated on the observed pairs $\{(x_j, y_j)\}$. In the matrix form (see [DE003](./DE003_vectors_matrices.md) document) this system is written as:

$$
\begin{bmatrix}
1 & x_1 & x_1^2 & \dots & x_1^{N-1} \\
1 & x_2 & x_2^2 & \dots & x_2^{N-1} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & x_N & x_N^2 & \dots & x_N^{N-1}
\end{bmatrix} * \begin{bmatrix} a_0 \\ a_1 \\ \vdots \\ a_{N-1} \end{bmatrix} =
\begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_N \end{bmatrix} \equiv \mathbf{A} * \mathbf{a} = \mathbf{y}
$$

All coefficients of the matrix **A** can be calculated in $O(N^2)$ steps using the obvious recursive relation $a_{i, j+1} = a_{i, j} * x_i \; \forall \; 1 \leq i \leq N, 1 \leq j < N \; : \; a_{i,1} = 1 \; \forall \;  i$. And the system of the linear equations can be solved using Gauss-Jordan elimination and back-substitution, which algorithm has the numerical complexity of $O(N^2)$ as well. The obvious drawback of this method is that the elements of the matrix may differ by many orders of magnitude in amplitude, which results in the accumulation of the floating point error, which can reduce the precision significantly for large degree of the polynomial.

Note, that depending on the nature of the underlying function $f(x)$, thus the set of the observed values $\{y_i\}$, the values of one or more highest power coefficients of the interpolating polynomial can be zeroes, resulting in the degree of the polynomial being $K < N -1$. For example, if the underlying function itself is a polynomial of degree $K < N -1$, i.e. $f(x) = P^K(x)$, all the coefficients $a_j = 0 \; \forall \; K < j < N$ in the solution of the system, and the interpolating polynomial is the $P^K(x)$ itself, i.e. $F(x) \equiv f(x)$. In general, for any observations set $\{(x_i, y_i)\}$ with the unique x-values ($x_i \neq x_j \; \forall \; i \neq j$) there is one and only one polynomial $P^{K}(x)$ of the degree $0 \leq K \leq N-1$, which goes through all N points.

In the practical applications, such as signal processing, the $\{x_i\}$ mesh is often fixed, thus the matrix **A** and its *inverse* $\mathbf{A}^{-1}$ can be pre-calculated in advance, hence the coefficients of a polynomial can be calculated for each set of the observed values $\{y_i\}$ in $O(N^2)$ steps as $\mathbf{a} = \mathbf{A}^{-1} * \mathbf{y}$ without necessity to compute the matrix and solve the system of the equations separately for each set of the observations.

The *naive* evalutation of a polynomial using the direct formula has the numerical complexity of $O(N^2)$; indeed, separate calculation of each K-th power of the variable requires *K-1* multiplications. Since all concerned powers are positive integer, the complexity of the algorithm can be reduced to $O(N*\log(N))$ using the recursive calculation method: $x^{2*k+1} = x^k * x^k *x$ for the odd powers and $x^{2*k} = x^k * x^k$ for the even powers. Still, the terms of the sum can differ by many orders of magnitude, which reduces the precision due to the accumulation of the floating point error.

However, the value of a polynomial can be evaluated in $O(N)$ steps using caching of the previously calculated terms:

* Evaluate $x$ as (1) and $a_0 + a_1 * x = a_0 + (1) * a_1$ as (1')
* Evaluate $x^2 = (1) * x$ as (2) and $a_0 + a_1 *x + a_2 * x^2 = (1') + (2) * a_2$ as (2')
* Evaluate $x^3 = (2) * x$ as (3) and $a_0 + a_1 *x + a_2 * x^2 + a_3 * x^3= (2') + (3) * a_3$ as (3')
* Iterate until the complete sum is calculated

In practice, a similar approach is taken for the numerical evaluation of a polynomial, but starting from the highest power term as given by the equation below.

$$
a_0 + a_1 * x + a_2 * x^2 + ... + a_N * x^{N-1} = a_0 + x * (a_1 + x * (a_2 + x * (...(a_{N-2} + x * a_{N-1}) )))
$$

This algorithm has the numerical complexity of $O(N)$ as well, and it minimizes the floating point error accumulation.

## Interpolation using Lagrange polynomials

Instead of solving the sytem above directly, the interpolating polynomial can be found using the *Lagrange polynomial basis*[^1] as $P(x) = \sum_{i=1}^{N}{y_i*l_i(x)}$, where $l_i(x_j) = \delta_{i,j}$, where $\delta_{i,j}$ is *Kronecker delta*, i.e. $l_i(x_j) = 0 \; \forall \; i \neq j$ and $l_i(x_i) = 1$. Basically, each $x_j \neq x_i$ is a *root* of the polynomial $l_i(x)$, whereas at $x_i$ the polynomial $l_i(x)$ evaluates to 1. Thus, each base polynomial is of the degree *N-1* exactly, and their sum is of the degree $0 \leq K \leq N-1$. These base polynomials are defined as

$$
l_i(x) = \prod_{1 \leq j \leq N, \; j \neq i}{\frac{x - x_j}{x_i - x_j}} = \frac{x - x_1}{x_i - x_1} * \dots * \frac{(x - x_{i-1})*(x - x_{i+1})}{(x_i - x_{i-1})*(x_i - x_{i+1})} * \dots * \frac{x - x_N}{x_i - x_N} 
$$

For the *hand computations* this algorithm is much simpler than the direct calculations using the solution of a linear equations system (see above).

In the frame of this library, the Lagrange interpolation can be easily implemented using the functionality of the module *polynomials* (see [UD001](../References/UD001_polynomial_reference.md)); specifically, the class method *fromRoots*() of the class **Polynomial** as follows:

* For *N* observations $\{(x_i, y_i)\}$ *N* sub-sets $\{x_{j \neq i}\}$ are generated by removing *i*-th point from the total grid $\{x_j\}$ for each *i*
* The polynomial basis is generated as:
  * Creating a polynomial $P_i(x)$ from *N-1* roots $\{x_{j \neq i}\}$
  * Calculating the correction coefficient $c_i$ by evaluating this polynomial at $x_i$, i.e. $c_i = P_i(x_i)$
  * Normalizing the polynomial by the calculated correction factor, i.e. $l_i(x) = P_i(x) / c_i$
* Calculating the interpolating polynomial as $P(x) = \sum_{i=1}^N{y_i * P_i(x)}$

## Interpolation using Legendre polynomials

???[^2]

## References

[^1]: [Wikipedia: Lagrange polynomial](https://en.wikipedia.org/wiki/Lagrange_polynomial)

[^2]: [Wikipedia: Legendre polynomial](https://en.wikipedia.org/wiki/Legendre_polynomials)
