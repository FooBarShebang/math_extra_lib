# Interpolation of a Function

## Introduction

A certain value  or property **Y** is measured *N* times, for example, at the different locations in space or the different moments in time. The assumption is that the variation in the measured **Y** value reflects its dependence on the measurement position or time **X**, i.e. that **Y** (dependend variable) is a function of **X** (independent variable). Therefore, $\exist \, \mathtt{F} \, : \, \mathbf{X} \overset{F}{\rightarrow} \mathbf{Y} \, \Leftrightarrow \, \mathbf{Y} = \mathtt{F}(\mathbf{X}) \, \Leftrightarrow \, \mathtt{F}(x_i) = y_i \, \forall \, i \in [0, N-1]$. The actual function *F*(*x*) is uknown, we only have a set of *N* pairs of values (*x*, *y*), i.e. $\{(x_0, y0), \, (x_1, y_1),\, \dots , \, (x_{N-1}, y_{N-1})\}$, and we want to find an *approximating* function *f*(*x*) such, that $f(x_i) = F(x_i) \equiv y_i \, \forall \, i \in [0, N-1]$, and the function *f*(*x*) is *continuous* on the entire inteval $[\min{x}, \, \max{x}]$. Therefore, on each interval $[x_i, x_{i+1}] \, \forall \, i \in [0, N-2]$ we can approximate $F(x) \approx f(x) \, \forall \, x \in [x_i, x_{i+1}]$.

One of the ways to achieve it is to define *f*(*x*) as a polynomial, see [DE001](./DE001_polynomials.md). Given *N* unique *x* values and the corresponding *y* values, there is one and only one polynomial of the degree *N-1* (with *N* coefficients), which graph goes exactly through all *N* pairs of (*x*, *y*) points. The *frontal assault* approach requires solution of the system of *N* linear equations of *N* variables, which has computation complexity $\mathtt{O}(N^3)$, see [DE003](./DE003_vectors_matrices.md), and the algorithm is prone to the accumulation of the rounding error. The constructed polynomial of the degree *N-1* can be evaluated as many times as needed at any point $x \in [\min{x}, \, \max{x}]$ with the computation complexity $\mathtt{O}(N)$. The approximating polynomial may also be constructed directly without matrix calculations, e.g. using *Lagrange polynomials*, see [DE004](./DE004_poly_solver.md). $\forall \, i \in [0, N-1]$ one can define a polynomial of degree *N-1*, i.e. $P_{i}^{(N-1)}(x) = \sum_{j=0}^{N-1}{\alpha_j x^j} \, : P_{i}^{(N-1)}(x_k) = 0 \, \forall \, k \neq i \, \mathtt{and} \, P_{i}^{(N-1)}(x_i) = y_i$. Obviously, such a polynomial is constructed as $P_{i}^{(N-1)}(x) = c_i \prod_{j=0, j \neq i}^{N-1}{(x - x_j)}$, with the complete approximating funciton being $f(x) = \sum_{i=0}^{N-1}P_{i}^{(N-1)}(x)$. This algorithm has the computation complexity $\mathtt{O}(N^3)$ as well, but it is generally simpler in the numerical implementation and manual computations, and it is less prone to the numerical instability and error accumulation due to the fact that only $\mathtt{O}(N)$ floating point divisions are involved compared to $\mathtt{O}(N^2)$ of the matrix calculations. Furthermore, if the approximating function value is to be determined only few times, there is no need to contruct this function, instead one only needs to calculate the values of *N* coefficients $c_i$ once (total calculation complexity $\mathtt{O}(N^2)$), and when each time evaluate the values of *N* base polynomials and their sum with the total calculation complexity $\mathtt{O}(N^2)$. However, the high degree polynomial approximation tends to result in the significant oscillation of the approximating function *f*(*x*) between the nodes $x_i$.

The other approach is to use step-wise approximation (interpolation). First, the set of points must be ordered, sorted in ascending values of the independent variables, i.e. $x_{i+1} > x_i \, \forall \, i \in [0, N-2]$. Secondly, on each interval $[x_i, x_{i+1}]$ one must find a function $f_i(x) : f_i(x_i) = y_1 \, \mathtt{and} \, f_i(x_{i+1}) = y_{i+1}$, which automatically ensures that $f_i(x_{i+1}) = f_{i+1}(x_{i+1})$. Then, the complete function is constructed as

$$
f(x) = \begin{cases}
f_0(x) & x \in [x_0, x_1) \\
f_1(x) & x \in [x_1, x_2) \\
\dots \\
f_{N-3}(x) & x \in [x_{N-3}, x_{N-2}) \\
f_{N-2} & x \in [x_{N-2}, x_{N-1}]
\end{cases}
$$

This document discusses numerical methods to construct such a function with computational complexity $\mathtt{O}(N)$, and on each interval this function can be evaluated with computational complexity $\mathtt{O}(1)$.

## Linear interpolation

The simplest method is linear interpolation, when on each inteval $[x_i, x_{i+1}] \, \forall \, i \in [0, N-2]$ the approximation is $f(x) = f_i(x)=a_i x + b_i$. The slope of the straigth line between the points $(x_i, y_i)$ and $(x_{i+1}, y_{i+1})$ is $\frac{y_{i+1} - y_i}{x_{i+1} - x_i}$, therefore

$$
f_i(x) = y_i + \frac{y_{i+1} - y_i}{x_{i+1} - x_i} (x-x_i) = y_i \frac{x_{i+1} - x}{x_{i+1} - x_i} + y_{i+1} \frac{x - x_i}{x_{i+1} - x_i}
$$


We can also introduce a normalized variable

$$
t = \frac{x - x_i}{x_{i+1} - x_i} : t \in [0,1] \Rightarrow 1 - t = \frac{x_{i+1} - x}{x_{i+1} - x_i}
$$

and 

$$
f_i(t) = y_i (1-t) + y_{i+1} t
$$

Note that the step-wise linear interpolation function is continuous everywhere, including nodes, i.e. $f(x_{i+1}-0) \equiv f_i(x_{i+1}) = f(x_{i+1}+0) \equiv f_{i+1}(x_{i+1})$, but its derivative is not continuous at the nodes $\frac{df}{dx}(x_{i+1}-0) \equiv \frac{df_i}{dx}(x_{i+1}) \neq \frac{df}{dx}(x_{i+1}+0) \equiv \frac{df_{i+1}}{dx}(x_{i+1}) $.

## Bernstein polynomials

The Bernstein basis polynomial of degree *n* is defined as $b_{i,n}(x) = \binom{n}{i} x^i (1-x)^{n-i}$, see [DE004](./DE004_poly_solver.md), thus for any degree *n* there are exactly *n+1* such polynomials, which form an orthogonal basis on the interval [0, 1], i.e. any polynomial of the degree *n* can be constructed as a linear combination of these basis polynomials:

$$
\forall \, P^{(n)}(x) = \sum_{i=0}^n{a_i x^i} \, \exists \, \alpha_i \, \forall \, i \in [0, n] : P^{(n)}(x) = \sum_{i=0}^n{\alpha_i b_{i,n}(x)} \, \forall \, x \in [0,1] 
$$

Below is not a proof, but an illustration. Consider the first 4 degrees (0 to 3 inclusively).

$$
\begin{aligned}
b_{0,0}(x) &= 1 \\
b_{0,1}(x) &= 1 - x \\
b_{1,1}(x) &= x \\
b_{0,2}(x) &= (1-x)^2 = x^2 - 2 x + 1 \\
b_{1,2}(x) &= 2x(1-x) = -2x^2 + 2x \\
b_{2,2}(x) &= x^2 \\
b_{0,3}(x) &= (1-x)^3 = - x^3 + 3x^2 - 3x + 1 \\
b_{1,3}(x) &= 3x(1-x)^2 = 3x^3 - 6x^2 + 3x \\
b_{2,3}(x) &= 3x^2(1-x) = -3x^3 + 3x^2 \\
b_{3,3}(x) &= x^3
\end{aligned}
$$

Thus,

$$
ax + b = \alpha b_{0,1}(x) + \beta b_{1,1}(x) \Rightarrow \beta - \alpha = a \, \mathtt{and} \, \alpha = b \Rightarrow \beta = a + b
$$

Similarly

$$
ax^2 + bx + c = \alpha b_{0,2}(x) + \beta b_{1,2}(x) + \gamma b_{2,2}(x) \Rightarrow \\
\begin{cases}
\alpha -2 \beta + \gamma &= a  \\
-2 \alpha + 2 \beta &= b \\
\alpha &= c
\end{cases} \Rightarrow
\begin{cases}
\alpha &= c \\
\beta &= c + b / 2 \\
\gamma &= a + b + c
\end{cases}
$$

And

$$
ax^3 + bx^2 + cx + d = \alpha b_{0,3}(x) + \beta b_{1,3}(x) + \gamma b_{2,3}(x) + \delta b_{3,3}(x) \Rightarrow \\
\begin{cases}
- \alpha + 3 \beta - 3 \gamma  + \delta&= a  \\
3 \alpha - 6 \beta + 3 \gamma &= b \\
-3 \alpha + 3 \beta &= c \\
\alpha  &= d
\end{cases} \Rightarrow
\begin{cases}
\alpha &= d \\
\beta &= d + c / 3 \\
\gamma &= d + 2c/3 + b/3 \\
\delta &= a + b + c + d
\end{cases}
$$

The important consequence is that:

$$
\forall \, P^{(2)}(x) : P^{(2)}(0)= P^{(2)}(1) = 0 \Rightarrow P^{(2)}(x) = a * b_{1,2}(x) \\
\forall \, P^{(3)}(x) : P^{(3)}(0)= P^{(3)}(1) = 0 \Rightarrow P^{(3)}(x) = a * b_{1,3}(x) + b * b_{2,3}(x)
$$

which is obvious from the following considerations $b_{1,2}(0) = b_{1,2}(1) = 0$, whereas $b_{0,2}(0) = 1$ and $b_{0,2}(1) = 0$ and $b_{2,2}(0) = 0$ and $b_{2,2}(1) = 1$; similarly $b_{1,3}(0) = b_{1,3}(1) = b_{2,3}(0) = b_{2,3}(1) = 0$, whereas $b_{0,3}(0) = 1$ and $b_{0,3}(1) = 0$ and $b_{3,3}(0) = 0$ and $b_{3,3}(1) = 1$.

For example, $B_1(x) = x^3 - x = - \frac{1}{3} (b_{1,3}(x) + 2 b_{2,3}(x))$, and $B_2(x) = (1- x)^3 - (1 - x) \equiv B_1(1 - x) = - \frac{1}{3} (2 b_{1,3}(x) +  b_{2,3}(x))$. These two polynomials can also be used as the basis for construction of an arbitrary degree 3 polynomial with the roots at 0 and 1, i.e.


$$
\forall \, P^{(3)}(x) : P^{(3)}(0)= P^{(3)}(1) = 0 \Rightarrow P^{(3)}(x) = a * b_{1,3}(x) + b * b_{2,3}(x) = \alpha B_1(x) + \beta B_2(x)
$$

where

$$
\begin{cases}
a &= - \frac{\alpha + 2 \beta}{3} \\
b &= - \frac{2 \alpha + \beta}{3}
\end{cases} \Leftrightarrow 
\begin{cases}
\alpha &= a - 2 b \\
\beta &= b - 2a
\end{cases}
$$

## Quadratic spline interpolation

In order to ensure not only continuity of the approximation function, i.e. $f_i(x_{i+1}) = f_{i+1}(x_{i+1})$, but also of its first derivative (smoth function) $\frac{df_i}{dx}(x_{i+1}) = \frac{df_{i+1}}{dx}(x_{i+1})$, one should use the polynomials of degree 2 or higher.

For *N* nodes (thus *N-1* intervals) and the interval polynomials $f_i(x) = a_i x^2 + b_i x + c_i$, there are *3N -3* variables. The equality to $y_i$ value at the $x_i$ node conditions yield *2N-2* equations, whereas the continuity of the derivative at *N-2* internal nodes yeild *N-2* additional equations, with the total of *3N-4* equations. One extra equation can be produced by specifying the value of the function's derivative at one of the edges, i.e. $\frac{df_0}{dx}(x_{0})$ or $\frac{df_{N-2}}{dx}(x_{N-1})$.

The solution of the problem is to express the polynominals in the terms of the normalized variable *t* at each interval as

$$
f_i(t) = y_i (1-t) + y_{i+1} t + a_i * b_{1,2}(t) = y_i (1-t) + y_{i+1} t + 2 * a_i * t * (1-t)
$$

which, obviously, reduces the number of free variables from $3N-3$ to $N-1$, whilst it satisfies the boundary conditions $f_i(0) = y_i$ and $f_i(1) = y_{i+1}$, and its derivative (over t) is $\frac{df_i}{dt} (t) = y_{i+1} - y_i - 4 a_i t + 2 a_i$, hence $\frac{df_i}{dt} (0) = y_{i+1} - y_i + 2 a_i$ and $\frac{df_i}{dt} (1) = y_{i+1} - y_i - 2 a_i$. Considering that $\frac{df}{dx}(t(x)) = \frac{df}{dt} * \frac{dt}{dx} = \frac{df}{dt} * \frac{1}{x_{i+1} - x_i}$, the continuity of the derivate at the inner nodes condition yeilds *N-2* equations in the form

$$
\frac{y_{i+1} - y_i}{x_{i+1} - x_i} - 2 * \frac{\alpha_i}{x_{i+1} - x_i} = \frac{y_{i+2} - y_{i+1}}{x_{i+2} - x_{i+1}} + 2 * \frac{\alpha_{x+1}}{x_{i+2} - x_{i+1}} 
$$

Basically, by specifiyng the value of the derivative $\frac{df}{dx}(x_0)$ at the left-most mode the value of the coefficient $\alpha_0$ is defined, and the rest of the coefficients are calculates directly in *N-2* steps, since each $\alpha_{i+1}$ coefficient is fully defined by the mesh function (ponts pairs) $\{(x_i, y_i)\}$ and the value of the coeffient at the previous interval $\alpha_i$. Alternatively one can start from the value of the derivative at the right-most point $x_{N-1}$, thus defining the $\alpha_{N-2}$ value and moving in the reverse direction towards $\alpha_0$.

Effectively, a single boundary condition defines the entire solution of the system of equations. However, it also leads to strong oscillation of the approximation function between the nodes, which is amplified by the drastic change of the average internode slope $\frac{y_{i+1} - y_i}{x_{i+1} - x_i}$ in the adjacent intervals. This is the reason, why quadratic spline interpolation is never used in practice.

## Cubic spline interpolation

With a cubic (3rd degree) polynomial used at each of the *N-1* intervals, the number of free variables is increaded to *4N-4*. The equality to $y_i$ value at the $x_i$ node conditions yield *2N-2* equations, whereas the continuity of the derivative at *N-2* internal nodes yeild *N-2* additional equations, with the total of *3N-4* equations. We can also apply restriction on the continuity of the second derivative $\frac{d^2f_i}{dx^2}(x_{i+1}) = \frac{d^2f_{i+1}}{dx^2}(x_{i+1})$, which yields *N-2* extra equations, with the total of *4N-6*. Two more equations can be obtained from the boundary conditions:

* Values of the first derivative at each of the end nodes
* OR, values of the second derivative at each of the end nodes
* OR, value of the first derivatice at one end node and of the second derivative at the same or the opposite end node

The most common case is to set $\frac{d^2f}{dx^2}(x_0) \equiv \frac{d^2f_0}{dx^2}(x_0) = 0$ and $\frac{d^2f}{dx^2}(x_{N-1}) \equiv \frac{d^2f_{N-2}}{dx^2}(x_{N-1}) = 0$, i.e. the approximation funcitons becomes a straight line (zero curvature) and the both ends of the definition interval. This is called *natural cubic spline* because it is the shape, which a flexible ruler with N fixation points takes[^1].

The task is reduced to *2N-2* free variables in this form:

$$
\begin{aligned}
f_i(t) &= y_i (1-t) + y_{i+1} t + a_i * B_1(t) + b_i * B_2(t)\\
& = y_i (1-t) + y_{i+1} t + a_i * (t^3 - t) + b_i * ((1-t)^3 - (1-t))
\end{aligned}
$$

which is the solution for the 'going though the nodes' restriction.

Note, that

$$
\begin{aligned}
\frac{dB_1}{dt} &= 3t^2 - 1 \Rightarrow \frac{dB_1}{dt}(0) = -1, \, \frac{dB_1}{dt}(1) = 2 \\
\frac{dB_2}{dt} &= -3(1-t)^2 + 1 \Rightarrow \frac{dB_2}{dt}(0) = -2, \, \frac{dB_2}{dt}(1) = 1 \\
\frac{d^2B_1}{dt^2} &= 6t \Rightarrow \frac{d^2B_1}{dt^2}(0) = 0, \, \frac{d^2B_1}{dt^2}(1) = 6 \\
\frac{d^2B_2}{dt^2} &= 6(1-t) \Rightarrow \frac{d^2B_2}{dt^2}(0) = 6, \, \frac{d^2B_2}{dt^2}(1) = 0
\end{aligned}
$$

Therefore, at the node $x_{i+1} \, \forall \, 0 \leq i < N-2$ the first derivate continuiity is expressed as

$$
\frac{y_{i+1} - y_i}{x_{i+1} - x_i} + \frac{2 a_i}{x_{i+1} - x_i} + \frac{b_i}{x_{i+1} - x_i} = \frac{y_{i+2} - y_{i-1}}{x_{i+2} - x_{i+1}} - \frac{a_{i+1}}{x_{i+2} - x_{i+1}} - \frac{2 b_{i+1}}{x_{i+2} - x_{x+1}}
$$

Since $\frac{d^2f}{dx^2} = \frac{d}{dt}(\frac{df}{dx}) * \frac{dt}{dx} = \frac{d^2f}{dt^2} * \left( \frac{dt}{dx}\right)^2$, the continuity of the second derivative is expessed as

$$
\frac{6 a_i}{(x_{i+1} - x_i)^2} = \frac{6 b_{i+1}}{(x_{i+2} - x_{i+1})^2} = y_{i+1}''
$$

where $y_{i+1}''$ is yet unknown value of the second derivative at the point $x_{i+1}$. Therefore, the continuuity of the first derivative is transformed into

$$
y_i'' * \frac{x_{i+1} - x_i}{6} + y_{i+1}'' * \frac{x_{x+2} - x_i}{3} + y_{i+2}'' * \frac{x_{x+2} - x_{i+1}}{6} = \frac{y_{i+2} - y_{i-1}}{x_{i+2} - x_{i+1}} - \frac{y_{i+1} - y_i}{x_{i+1} - x_i}
$$

which can be further refactored into

$$
y_i'' * \frac{x_{i+1} - x_i}{2 (x_{x+2} - x_i)} + y_{i+1}''  + y_{i+2}'' * \frac{x_{x+2} - x_{i+1}}{2 (x_{x+2} - x_i)} = \frac{3}{x_{x+2} - x_i} * \left( \frac{y_{i+2} - y_{i-1}}{x_{i+2} - x_{i+1}} - \frac{y_{i+1} - y_i}{x_{i+1} - x_i} \right)
$$

with the boundary conditions $y_0'' = 0$ and $y_{N-1}'' = 0$. This system of the linear equations is represented by a tri-diagonal matrix, and it can be solved in $\mathtt{O}(N)$ steps (see the next section). The approximation polygon on each interval is defined as

$$
\begin{aligned}
f_i(t) &= y_i (1-t) + y_{i+1} t + y_{i+1}'' * (t^3 - t) * \frac{(x_{i+1} - x_i)^2}{6}\\
&+ y_i'' * ((1-t)^3 - (1-t)) * \frac{(x_{i+1} - x_i)^2}{6}
\end{aligned}
$$

## Tri-diagonal matrices and Thomas algorithm

As defined in previous section, one need to solve the linear system of *N-2* equations for *N-2* variables, with each equation including only 3 variables - values of the second derivative at three adjacent nodes: 

$$
a_i x_{i-1} + b_i x_i + c_i x_{i+1} = d_i \, \forall \, 1 \leq i \leq n
$$

with $a_1 = c_n = 0$. Such system of equations forms a tri-diagonal matrix:

$$
\begin{bmatrix}
b_1 & c_1 & 0 & 0 & \dots & 0 & 0 & 0 \\
a_2 & b_2 & c_2 & 0 & \dots & 0 & 0 & 0 \\
0 & a_3 & b_3 & c_3 & \dots & 0 & 0 & 0 \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \vdots \\
0 & 0 & 0 & 0 & \dots & a_{n-1} & b_{n-1} & c_{n-1} \\
0 & 0 & 0 & 0 & \dots & 0 & a_n & b_n \\
\end{bmatrix} \times
\begin{bmatrix}
x_1 \\ x_2 \\ x_3 \\ \vdots \\ x_{n-1} \\ x_n
\end{bmatrix} =
\begin{bmatrix}
d_1 \\ d_2 \\ d_3 \\ \vdots \\ d_{n-1} \\ d_n
\end{bmatrix}
$$

which can be solved in $\mathtt{O}(N)$ steps. For each column *i* we need to eliminate only a single element $a_{i+1}$ under the main diagonal element $b_i$, which process also affects the next diagonal element $b_{i+1}$ and the 'free' vector coeffient $d_{i+1}$. After elimination of the $a_2$ element $b_2 \rightarrow b_2' = b_2 - c_1 * \frac{a_2}{b_1}$ and $d_2 \rightarrow d_2' = d_2 - d_1 * \frac{a_2}{b_1}$. After elimination of the $a_2$ element $b_3 \rightarrow b_3' = b_3 - c_2 * \frac{a_2}{b_2'}$ and $d_3 \rightarrow d_3' = d_3 - d_2 * \frac{a_2}{b_2'}$. Etc. After reaching the *n*-th column, $x_n = \frac{d_n'}{b_n'}$, and the rest of elements is found by back-substitution traveling upward along the main diagonal: $x_{n-1} = \frac{d_{n-1}' - c_{n-1} * x_n}{b_{n-1}'}$, $x_{n-2} = \frac{d_{n-2}' - c_{n-2} * x_{n-1}}{b_{n-2}'}$, etc.

This special, simplified form of Gaussian elimination, also knows as Thomas algorithm[^2] can be expressed as the forward sweep

$$
c_i' = \begin{cases}
\frac{c_i}{b_i} & i =1 \\
\frac{c_i}{b_i - a_i c_{i-1}'} & i=2, 3, \dots, n-1
\end{cases}
$$

and 

$$
d_i' = \begin{cases}
\frac{d_i}{b_i} & i =1 \\
\frac{d_i - a_i d_{i-1}'}{b_i - a_i c_{i-1}'} & i=2, 3, \dots, n-1
\end{cases}
$$

with the back substitution (solution)

$$
\begin{aligned}
x_n &= d_n', \\
x_i &= d_i' - c_i' x_{i+1}, \, i = n-1, n-2, \dots, 1
\end{aligned}
$$

This algorithm is, in general, not numerically stable, however it is guaranteed to be stable in the case of the cubic spline interpolation. Indeed, concerning the system of equations for the second derivaties in its normalized form. Obviously, that all diagonal elements $b_i = 1 \, \forall \, i$ and $0 < a_i < 1/2$ and $0 < c_i < 1/2$. In the special case of the equidistant $\{x_i\}$ mesh $a_i = c_i = 1/ 4 \, \forall \, i$. Therefore, $b_2' = b_2 - a_2 * c_1 / b_1 > 3/4 > 1 / 2$, since $b_1 = b_2 = 1$ and $0 < c_1 < 1/2$ and $0 < a_2 < 1/2$. As long as $b_i' > 1/2$ it is quaranteed that $b_{i+1}' = 1 - c_i * \frac{a_{i+1}}{b_i'} > 1/2$. Therefore, a zero value element never occurs at the main diagonal, which is equivalent to to $b_i - a_i c_i' > 0 \, \forall \, i$, and the division by zero never occurs.

## References

[^1]: [Wikipedia: Spline interpolation](https://en.wikipedia.org/wiki/Spline_interpolation)

[^2]: [Wikipedia: Tridiagonal matrix algorithm](https://en.wikipedia.org/wiki/Tridiagonal_matrix_algorithm)