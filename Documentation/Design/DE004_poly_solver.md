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

All coefficients of the matrix **A** can be calculated in $O(N^2)$ steps using the obvious recursive relation $a_{i, j+1} = a_{i, j} * x_i \; \forall \; 1 \leq i \leq N, 1 \leq j < N \; : \; a_{i,1} = 1 \; \forall \;  i$. And the system of the linear equations can be solved using Gauss-Jordan elimination and back-substitution, which algorithm has the numerical complexity of $O(N^3)$. The obvious drawback of this method is that the elements of the matrix may differ by many orders of magnitude in amplitude, which results in the accumulation of the floating point error, which can reduce the precision significantly for large degree of the polynomial.

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

Note that the numerical complexity of the iterative calculation $P^{(N+1)}(x) = P^{(N)}(x) * (x - a)$ is $O(N)$, therefore a single basis polynomial $l_i(x)$ of the degree *N-1* is constructed from the roots in $O(N^2)$ steps, and the complete interpolating polynomial $P(x)$ - in $O(N^3)$ steps.

In the case of the repetitive signal processing / observations $\{y_i\}^{(n)}$ on the fixed x-grid $\{x_i\}$ the entire basis can be pre-computed once ($O(N^3)$ complexity) and the interpolating polynomial for each observations set can be computed from the weights $\{y_i\}^{(n)}$ in only $O(N^2)$ steps. Furthermore, in this case the computation can be simplified using the *barycentric form* $P(x) = l(x) * \sum_{i=1}^N{y_i * \frac{w_i}{x-x_i}}$, where $l(x) = \prod_{i=1}^N{(x- x_i)}$ and $w_i = \prod_{j=1,\; j\neq i}^N{(x_i-x_j)^{-1}}$ (barycentric weight of the node). The common polynomial $l(x)$ can be computed once ($O(N^2)$ complexity) for a fixed grid as well as all barycentic weights ($O(N^2)$ together). The barycentric form of the interpolating polynomial at any point *x* is evaluated with $O(N)$ numerical complexity. However, in order to avoid division by zero error the value *x* must be checked. If it is one of the $\{x_i\}$ values (i.e. a node, or a root of $l(x)$ polynomial) the corresponding $y_i$ value must be returned.

## Interpolation using Legendre polynomials

The Legendre polynomials[^2] can also be used in the interpolation. These polynomials are often used in the solution of differential equations, e.g., concerning Laplace's equation or Newtonian potential. They have the following properties:

* Orthogonality and normalization $\int_{-1}^1{P^{(m)}(x)P^{(n)}(x)dx} = \frac{2}{2n+1}\delta_{mn}$
* Recursive definition (Bonnet's formula)
  * $P^{(0)}(x) = 1$
  * $P^{(1)}(x) = x$
  * $P^{(n+1)}(x) = \frac{2n+1}{n+1}xP^{(n)}(x) - \frac{n}{n+1}P^{(n-1)}(x)$
* Any polynomial of the degree *N* on the interval [-1, 1] can be decomposed into $\sum_{i=0}^N{\alpha_i*P^{(i)}(x)}$

The advantage of using Legende polynomial base is that it is independent on the actual values of the $\{x_i\}$ set, but it is fully defined by the number of the observation points *N*, which means that the basis is formed by exactly *N* polynomials $P^{(0)}(x)$ to $P^{(N-1)}(x)$, which can be pre-computed in about $O(N^2)$ steps all together, and re-used regardless of the specific observations set $\{(x_i, y_i)\}$ as long as the number of points remains constant.

However, the x-coordinates must be rescaled $[\min(\{x_i\}), \max(\{x_i\})] = [x_1, x_N] \rightarrow [-1, 1]$, which is achived by the linear transformation $x \rightarrow z = \frac{2x-(x_N+x_1)}{x_N - x_1}$. Then the observations set $\{(x_i, y_i)\}$ is interpolated by the polynomial $P(z) = \sum_{i=0}^{N-1}{a_i*P^{(i)}(z)}$, where the weigth coefficients are calculated as

$$
\begin{bmatrix}
P^{(0)}(z_1) & P^{(1)}(z_1) & \dots & P^{(N-1)}(z_1) \\
P^{(0)}(z_2) & P^{(1)}(z_2) & \dots & P^{(N-1)}(z_2) \\
\vdots & \vdots & \ddots & \vdots \\
P^{(0)}(z_N) & P^{(1)}(z_N) & \dots & P^{(N-1)}(z_N) \\
\end{bmatrix} * \begin{bmatrix} a_0 \\ a_1 \\ \vdots \\ a_{N-1}\end{bmatrix} =
\begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_N\end{bmatrix}
$$

Note that the Bonnet's recursive formula can be used for the sequential evaluation of all basis polynomials at the given value of *z*, thus all coefficients of the matrix can be computed in $O(N^2)$ steps. Furthermore, with the known weighting coefficients the entire interpolating polynomial can be evaluated in $O(N)$ steps without the neccessity to construct the polynomial itself.

If required, the constructed $P(z)$ polynomial can be transformed into a polynomial on the x-space by convolution $P(z) \rightarrow \hat{P}(x) = P(\frac{x_N-x_1}{2}z + \frac{x_N+x_1}{2})$.

## Interpolation using Chebyshev polynomials

The Chebyshev polynomials[^3] of the first kind are another example of orthogonal polynomials basis, which can be used in the interpolation. These polynomials are often used in the approximation of a function applications and signal processing due to their close relation to the Fourier cosine series. They have the following properties:

* Orthogonality and normalization $\int_{-1}^1{T^{(m)}(x)T^{(n)}(x)\frac{dx}{\sqrt{1-x^2}}} = \begin{cases}
0 & \mathtt{if} \; n \neq m \\
\pi & \mathtt{if} \; n=m=0 \\
\frac{\pi}{2} & \mathtt{if} \; n=m \neq 0
\end{cases}$
* Relation to the cosine function $T^{(n)}(\cos(\phi)) = \cos(n \phi)$
* Recursive definition
  * $T^{(0)}(x) = 1$
  * $T^{(1)}(x) = x$
  * $T^{(n+1)}(x) = 2xT^{(n)}(x) - T^{(n-1)}(x)$
* Any polynomial of the degree *N* on the interval [-1, 1] can be decomposed into $\sum_{i=0}^N{\alpha_i*T^{(i)}(x)}$

Their usage for the interpolation purposes is identical to the Legendre basis.

## Interpolation using Bernstein polynomials

The Bernstein polynomials[^4] can also be effectively used in the interpolation. Most often they are used to calculate a Bezier curve. These polynomials have the following properties:

* The *N+1* basis polynomials of degree *N* are defined as $b_{i,N} = {n \choose i} x^i (1-x)^{n-i}$
* $\sum_{i=0}^N{b_{i,N}(x)} = 1$
* $b_{0,N}(0) = b_{N,N}(1) = 1$ and $b_{i>0,N}(0) = b_{i<N, N}(1) = 0$
* Any polynomial of the degree *N* on the interval [0, 1] can be decomposed into $\sum_{i=0}^N{\alpha_i*b_{i,N}(x)}$

The entire basis can be effectively generated in $O(N^2)$ steps using the following relations:

* $(1-x)^n = \sum_{i=0}^n{(-1)^i{n \choose i} x^i}$
* ${n \choose i} = {n \choose n-i}$
* ${n \choose i} = \frac{n-i+1}{i} {n \choose i-1}$

However, the x-coordinates must be rescaled $[\min(\{x_i\}), \max(\{x_i\})] = [x_1, x_N] \rightarrow [0, 1]$, which is achived by the linear transformation $x \rightarrow z = \frac{x-x_1}{x_N - x_1}$. Then the observations set $\{(x_i, y_i)\}$ is interpolated by the polynomial $P(z) = \sum_{i=0}^{N-1}{a_i*b_{i, N-1}(z)}$, where the weigth coefficients are calculated as

$$
\begin{bmatrix}
b_{0, N-1}(z_1) & b_{1, N-1}(z_1) & \dots & b_{N-1, N-1}(z_1) \\
b_{0, N-1}(z_2) & b_{1, N-1}(z_2) & \dots & b_{N-1, N-1}(z_2)  \\
\vdots & \vdots & \ddots & \vdots \\
b_{0, N-1}(z_N) & b_{1, N-1}(z_N) & \dots & b_{N-1, N-1}(z_N)  \\
\end{bmatrix} * \begin{bmatrix} a_0 \\ a_1 \\ \vdots \\ a_{N-1}\end{bmatrix} =
\begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_N\end{bmatrix}
$$

However, this system of equations (N equations of N variables) can be reduced to N-2 equations of N-2 variables because $a_0 = y_1$ and $a_{N-1} = y_N$ due to properties of Bernstein polynomials. Therefore, the actual system to be solved is

$$
\begin{bmatrix}
b_{1, N-1}(z_1) & b_{2, N-1}(z_1) & \dots & b_{N-2, N-1}(z_1) \\
b_{1, N-1}(z_2) & b_{2, N-1}(z_2) & \dots & b_{N-2, N-1}(z_2)  \\
\vdots & \vdots & \ddots & \vdots \\
b_{1, N-1}(z_N) & b_{2, N-1}(z_N) & \dots & b_{N-2, N-1}(z_N)  \\
\end{bmatrix} * \begin{bmatrix} a_1 \\ a_2 \\ \vdots \\ a_{N-2}\end{bmatrix} =
\begin{bmatrix} y_2 - y_1 * (1-z_1)^{N-1} - y_N * z_1^{N-1}\\ y_3 - y_1 * (1-z_2)^{N-1} - y_N * z_2^{N-1} \\ \vdots \\ y_{N-1} - y_1 * (1-z_{N-1})^{N-1} - y_N * z_{N-1}^{N-1}\end{bmatrix}
$$

The constructed $P(z)$ polynomial can be transformed into a polynomial on the x-space by convolution $P(z) \rightarrow \hat{P}(x) = P((x_N-x_1)z + x_1)$.

## Finding all complex roots of a polynomial

A numerical method of finding all complex roots of a polynomial[^5] is, basically, based on the gradient descend. A polynomial of degree N can be factorized as $P^{(N)}(x) = \sum_{i=0}^N{a_i x^i} = a_N \prod_{j=1}^K{(x-z_j)^{\gamma_j}}$, where $z_j$ is a root with the multiplicity $\gamma_j$, and $\sum_{j=1}^K{\gamma_j} = N$. Assuming that all roots have multiplicity of 1 (N unique roots), the initial guess of the values $z_1, \; z_2, \; \dots \; z_N$ can be selected randomly within a circle on the complex plane with the radius $r = |z| = 1 + \max\{|\frac{a_{N-1}}{a_N}|, |\frac{a_{N-2}}{a_N}|, \dots, |\frac{a_0}{a_N}|\}$ - Cauchy's bound[^6]. Then, for each $z_k$ and offset is calculated as

$$
w_k = \frac{\frac{P(z_k)}{P'(z_k)}}{1 - \frac{P(z_k)}{P'(z_k)} * \sum_{i=1, i \neq k}^N{\frac{1}{z_k-z_i}}}
$$

where $P'(z_k)$ is the derivative of the polynomial evaluated at the point $z_k$. Then the guess is updated as $z_k \rightarrow z_k - w_k \; \forall \; k$, and the process is repeated iteratevely untill sufficient convergence is achieved.

Apparently, the polynomial can be normalized first by dividing by the value of the $a_N$, which does not change the values of the roots, but simplifies the calculations.

Also, there are two possible numerical problems with the algorithm:

* At a certain iteration step one of the 'guess' $z_k$ values coincides with a (local) extremum of the polynomial function, but it is not a root, i.e. $P(z_k) \neq 0$ but $P'(z_k) = 0$. In this case the offset $w_k$ can be chosen arbitrary just to move out of the extremum
* The polynomial has root(s) with multplicity > 1, and $z_k$ converges to such a root

In the second case both $P(z_k) = 0$ but $P'(z_k) = 0$. Indeed, considering multiplicity of a root $z_k$ being $\gamma_k > 1$, the initial polynomial of degree N can be factorized as $P^{(N)}(x) = (x-z_k)^{\gamma_k}*P^{(N-\gamma_k)}(x)$, where $P^{(N-\gamma_k)}(z_k) \neq 0$. Therefore,

$$
\frac{d}{dx}P^{(N)}(x) = \gamma_k (x-z_k)^{\gamma_k-1} * P^{(N-\gamma_k)}(x) + (x-z_k)^{\gamma_k}*\frac{d}{dx}P^{(N-\gamma_k)}(x) \Rightarrow \frac{d}{dx}P^{(N)}(z_k) = 0
$$

However, in this situation the original polynomial $P(x)$ must be divisible by $(x-z_k)$ and even by $(x-z_k)^{\gamma_k}$. Thus, the solution is to apply the transformation $P(x) \rightarrow P(x) / (x-z_k)$ iteratively as long as the reduced polynomial evaluates to 0 at $z_k$. Doing so the multiplicity of the $z_k$ root is defined. The remaining roots of the original polynomial $P^{(N)}(x)$ are the roots of the reduced polynomial $P^{(N-\gamma_k)}(x)$, which can be found using recursive call of the same function. This approach also eliminates the possible devision by zero problem concerning the $\frac{1}{z_k - z_i}$ terms.

Note, that the $\frac{1}{z_k - z_i}$ terms introduce 'repulsion' between the attractors of the algorithm (roots of the polynomial), which reduces the convergence speed of the algorithm in the case of presence of root(s) with multiplicity > 1 but also prevents the situation described above, unless the initial guess was 'lucky' to hit the multiple root.

Also for the large degrees ($N \geq 5$) and presence of the complex conjugated pair of roots ($a+b*i$ and $a-b*i$), i.e. factorization of the polynomial on the real numbers contains term $x^2 \pm 2ax + a^2 + b^2$, the algorithm results in significantly higher uncertainty / error of the estimation for this conjugated roots pair than for the other roots.

## References

[^1]: [Wikipedia: Lagrange polynomials](https://en.wikipedia.org/wiki/Lagrange_polynomial)

[^2]: [Wikipedia: Legendre polynomials](https://en.wikipedia.org/wiki/Legendre_polynomials)

[^3]: [Wikipedia: Chebyshev polynomials](https://en.wikipedia.org/wiki/Chebyshev_polynomials)

[^4]: [Wikipedia: Bernstein polynomials](https://en.wikipedia.org/wiki/Bernstein_polynomial)

[^5]: [Wikipedia: Aberth-Ehrlich method](https://en.wikipedia.org/wiki/Aberth_method)

[^6]: [Wikipedia: Geometrical properties of polynomial roots](https://en.wikipedia.org/wiki/Geometrical_properties_of_polynomial_roots)
