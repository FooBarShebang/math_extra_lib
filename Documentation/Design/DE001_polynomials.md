# Design of the module math_extra_lib.polynomials

## Background and definitions

Polynomial $P(x)$ of degree $N \geq 1$ is a function of a single variable x, which is a sum of powers of *x* less than or equal to *N* multiplied by respective coefficients, whith the highest power in the sum being exactly *N*, for instance:

* $2*x^3$ is a polynomial of the degree 3
* $x+1$ is a polynomial of the degree 1
* $x^2 + 2 * x + 1 = (x+1)^2$ and $x^2 - 2 * x + 3 = (x-1)^2 + 2$ and $x^2 - 1 = (x-1)*(x+1)$ are all polynomials of the degree 2

The generic form of a polynomial can be expressed as $P(x) = a_0 + a_1*x + a_2*x^2 + \dots + a_n*x^N = \sum_{i=0}^N{a_i*x^i} \; : \; a_N \neq 0 \; \Rightarrow \; deg(P(x)) = N$. Thus, the rules of the arithmetic operations between polynomials and scalars can be defined using the *commutativity*, *associativity* and *distributivity* properties of the respective scalar arithmetic operators.

For two polynomals $P_1(x) = \sum_{i=0}^{N_1}{a_i*x^i}, \; deg(P_1(x)) = N_1$ and $P_2(x) = \sum_{i=0}^{N_2}{b_i*x^i}, \; deg(P_2(x)) = N_2$, and a scalar $c$ the basic rules are:

* $c + P_1(x) = P_1(x) + c = c + \sum_{i=0}^{N_1}{a_i*x^i} = (a_0+c) + \sum_{i=1}^{N_1}{a_i*x^i}$
* $P_1(x) - c = \left( \sum_{i=0}^{N_1}{a_i*x^i} \right) - c = (a_0-c) + \sum_{i=1}^{N_1}{a_i*x^i}$
* $c - P_1(x) = c - \sum_{i=0}^{N_1}{a_i*x^i} = (c - a_0) - \sum_{i=1}^{N_1}{a_i*x^i} = (c + (- a_0)) + \sum_{i=1}^{N_1}{(-a_i)*x^i}$
* $c * P_1(x) = P_1(x) * c = c * \sum_{i=0}^{N_1}{a_i*x^i} = \sum_{i=1}^{N_1}{(c*a_i)*x^i}$
* $P_1(x) / c = \left( \sum_{i=0}^{N_1}{a_i*x^i} \right) / c = \sum_{i=1}^{N_1}{(a_i/c)*x^i}$
* $P_1(x) + P_2(x) = P_2(x) + P_1(x) = \sum_{i=0}^{N_1}{a_i*x^i} + \sum_{i=0}^{N_2}{b_i*x^i} = $
  * $\sum_{i=0}^{N}{(a_i+b_i)*x^i}$ if $N_1 = N_2 = N$
  * $\sum_{i=0}^{N_1}{(a_i+b_i)*x^i} + \sum_{i=N_1+1}^{N_2}{b_i*x^i}$ if $N_1 < N_2$
  * $\sum_{i=0}^{N_2}{(a_i+b_i)*x^i} + \sum_{i=N_2+1}^{N_1}{a_i*x^i}$ if $N_1 > N_2$
* $P_1(x) - P_2(x) = \sum_{i=0}^{N_1}{a_i*x^i} - \sum_{i=0}^{N_2}{b_i*x^i} = $
  * $\sum_{i=0}^{N}{(a_i-b_i)*x^i}$ if $N_1 = N_2 = N$
  * $\sum_{i=0}^{N_1}{(a_i-b_i)*x^i} + \sum_{i=N_1+1}^{N_2}{(-b_i)*x^i}$ if $N_1 < N_2$
  * $\sum_{i=0}^{N_2}{(a_i-b_i)*x^i} + \sum_{i=N_2+1}^{N_1}{a_i*x^i}$ if $N_1 > N_2$
* $P_1(x) * P_2(x) = P_2(x) * P_1(x) = \left( \sum_{i=0}^{N_1}{a_i*x^i} \right) * \left( \sum_{i=0}^{N_2}{b_i*x^i} \right) = \sum_{i=0}^{N_1}{\left( a_i*x^i * \sum_{j=0}^{N_2}{b_j*x^j}\right)} = \sum_{i=0}^{N_1}{\sum_{j=0}^{N_2}{a_i * b_j * x^{i+j}}} = \sum_{i=0}^{N_1 + N_2}{c_i*x^i} \Rightarrow deg(P_1(x) * P_2(x)) = deg(P_1(x))+ deg(P_2(x))$
* for a positive integer *c*: $\left( P_1(x)\right)^c = P_1(x) * P_1(x) * \dots * P_1(x) = \prod^c{P_1(x)} \Rightarrow deg(\left( P_1(x)\right)^c) = c * deg(P_1(x))$

The polynomial division can be defined as follows. Consider the case $N_1=N_2=N$, then $\exists \; c \neq 0 \; : a_N = c * b_N$, then the substraction $P_1(x) - c * P_2(x)$ eliminates, at least, the highest power term, therefore $P_1(x) - c * P_2(x)= const \; | \; P_3(x) \; : \; 1 \leq deg(P_3(x)) < N$. For the case of $N_1 > N_2$ the same logic is applicable $\exists \; c \neq 0 \; : a_{N_1} = c * b_{N_2}$, then $P_1(x) - c * x^{N_1-N_2} * P_2(x)= const \; | \; P_3(x) \; : \; 1 \leq deg(P_3(x)) < N_1$. Such procedure can be applied recursively to the resulting polynomial $P_3(x)$ (difference) as long as its degree exceeds $N_2$.

Thus, $P_1(x) / P_2(x) = c_1 | Q(x) + (c_2 | R(x))/P_2(x) \; : \; 1 \leq deg(R(x)) < N_2 \; AND \; deg(Q(x)) = N_1 - N_2 > 1$, where $Q(x)$ (or some scalar) is the *quotient* and $R(x)$ (or some scalar) is *remainder* - same meaning as in the integer division by modulo. Note, that the *remainder* is zero only if $\exists \; Q(x) \; : \; Q(x)*P_2(x) = P_1(x)$, whereas the *quotient* is zero if $N_1 < N_2$, in which case $R(x) = P_1(x)$.

A *root* of a polynomial is the value of its argument (variable), at which the value of the polynomial is zero, i.e. $\tilde{x} \; : \; P(x = \tilde{x}) = 0$. On the field of *complex* numbers *Z* a polynomial of degree *N* always has exactly *N* roots, although some roots may have the same value, in which case such a value is a root with *multiplicity* $> 1$, whereas all distinct, non-repeative values are *simple* roots. Thus, $P(x) = \sum_{i=0}^{N}{a_i*x^i} = a_N * \prod_{i=0}^N{(x - z_i)} = a_N * \prod_{j=0}^K{(x - z_j)^{k_j}} : \sum_{j=0}^K{k_j} = N \;  AND \; z_i \in Z \; \forall \; i$.

On the field of the *real* numbers *R* a polynomial of the degree *N* may have any non-negative integer number of roots from 0 to *N*, with the sum of the multiplicities of all roots not exceeding *N*. For example, $x^2 - 1 = (x-1)*(x+1)$ has exactly two simple real roots 1 and -1, $x^2 + 2 * x + 1 = (x+1)^2$ has a single real root -1 of multiplicity 2, $x^2+1$ has no real roots (but two *imaginary* roots *i* and -*i*), whereas $x^3 - x^2 + x - 1 =(x-1)*(x^2+1)$ has a single simple real root 1.

On other hand, given *N* real roots (treating the roots with multiplicity *k* as *k* individual roots) it is always possible to construct a respective polynomial up to a scaling factor (highest power coefficient) in the form $P(x) = \prod_{i=0}^N{(x - x_i)} = a_0 + a_1 * x + a_2 * x^2 + \dots + a_{N-1}*x^{N-1} + x^N$.

For a polynomial $P(x) = \sum_{i=0}^{N}{a_i*x^i}$ the *first derivative* is $\frac{dP(x)}{dx} = \sum_{i=1}^{N}{a_i*i*x^{i-1}}$. Recursively, the K-th derivative $(K<N)$ is $\frac{d^K P(x)}{dx^K} = \sum_{i=K}^{N}{\left( a_i*x^{i-K} * \prod_{j=0}^{K-1}{(i-j)}\right)}$. Finally, the first anti-derivative is $\int{P(x)} = const + \sum_{i=0}^{N}{\frac{a_i}{i+1}*x^{i+1}}$, where the constant of the indefinte integral becomes a new free coefficient (zero-th power), and it can be chosen arbitrary, even being zero.

## Design of the implementation

The described arithmetics can be implemented using the standard Python arithmetics operators by implementing the *magical* methods of a class representing a polynomial:

* '+' (addition)
  * '\_\_add\_\_()' for the right addition of a scalar or another polynomial
  * '\_\_radd\_\_()' for the left addition of a scalar
* '-' (substraction)
  * '\_\_sub\_\_()' for the substraction of a scalar or another polynomial from the current one
  * '\_\_rsub\_\_()' for the substraction of a polynomial (current) from a scalar
* '*' (multiplication)
  * '\_\_mul\_\_()' for the right multiplication by a scalar or another polynomial
  * '\_\_rmul\_\_()' for the left multiplication by a scalar
* '\\' (true division) '\_\_truediv\_\_()' for the division by a scalar
* '\\\\' (integer division) '\_\_floordiv\_\_()' for the division of a polynomial by another polynomial returning the *quotient* of the division
* '%' (mod division) '\_\_mod\_\_()' for the division of a polynomial by another polynomial returning the *remainder* of the division
* '^' (exponentiation) to raise a polynomial to a positive integer power; note, that this method also hooks the call of the built-in function **pow**()

In addition, the call to the built-in function **divmod**() is hooked by the magic method '\_\_divmod\_\_()', which should return a tuple of both *quotient* and *remainder* of the division of a polynomial by another polynomial.

Finally, the implementation of the magic method '\_\_call\_\_()' makes an instance of the class *callable*, i.e., in essence, a function, as below

```python
class SomeClass
    def __init__(self, *args):
        #do some stuff

    def __call__(self, Argument):
        #do some calculations here
        return SomeValue

MyObject = SomeClass(1, 4, 2)
Result = MyObject(4) #functional call, uses __call__() magic method
print(Result)
```

The calculus functions, i.e. derivative(s) and anti-derivative must be implemented as *instance methods*, whereas creation of a polynomial from its N roots must be a *class method* returning a new instance of the class.

The values of the coefficients of a polynomial should be passed into the initialization (instantiation) method, by preference in the order from the free coefficient to the highest power coefficient, in which case the last argument must be non-zero. These values are then stored in the internal hidden / private attribute (field) in a form of an (immutable) sequence, which length is the degree of the polynomial plus 1. Then, all arithmetics and described calculus operations can be easily performed using left / right padding of a sequence and per-element sequence manipulations.

Using the same definitions for the polynomials $P_1(x) = \sum_{i=0}^{N_1}{a_i*x^i}$ and $P_2(x) = \sum_{i=0}^{N_2}{b_i*x^i}$ their internal representations are $(a_0, a_1, \dots, a_{N_1})$ and $(b_0, b_1, \dots, b_{N_2})$. Then, the left and right addition of a scalar is $P_1(x)+c=c+P_1(x) \rightarrow (a_0 + c, a_1, a_2, \dots, a_{N_1})$. Substraction of a scalar is $P_1(x)-c \rightarrow (a_0 - c, a_1, a_2, \dots, a_{N_1})$, whereas the substraction from a scalar is $c- P_1(x) \rightarrow (c - a_0, -a_1, -a_2, \dots, -a_{N_1})$. The left and right multiplication by a scalar also has a simple form expression $P_1(x)*c=c*P_1(x) \rightarrow (a_0 * c, a_1 * c, a_2 * c, \dots, a_{N_1} * c)$, as well as the division by a scalar $P_1(x)/c \rightarrow (a_0 / c, a_1 / c, a_2 / c, \dots, a_{N_1} / c)$.

Conserning the addition and substraction of polynomials the shortest sequence must be first padded with zeroes from the right to match the length of the second sequence, and then the per-element addition or substraction must be applied for the same index elements:

* Equal length / polynomial degree $N_1 = N_2 = N$
  * $P_1(x) + P_2(x) \rightarrow (a_0 + b_0, a_1 + b_1, \dots, a_N + b_N)$
  * $P_1(x) - P_2(x) \rightarrow (a_0 - b_0, a_1 - b_1, \dots, a_N - b_N)$
* $N_1 > N_2$
  * $P_1(x) + P_2(x) \rightarrow (a_0 + b_0, a_1 + b_1, \dots, a_{N_2} + b_{N_2}, a_{N_2+1} + 0, \dots, a_{N_1} + 0)$
  * $P_1(x) - P_2(x) \rightarrow (a_0 - b_0, a_1 - b_1, \dots, a_{N_2} - b_{N_2}, a_{N_2+1} - 0, \dots, a_{N_1} - 0)$
* $N_1 < N_2$
  * $P_1(x) + P_2(x) \rightarrow (a_0 + b_0, a_1 + b_1, \dots, a_{N_1} + b_{N_1}, 0 + b_{N_1+1} , \dots, 0 + b_{N_2})$
  * $P_1(x) - P_2(x) \rightarrow (a_0 - b_0, a_1 - b_1, \dots, a_{N_1} - b_{N_1}, 0 - b_{N_1+1}, \dots, 0 - b_{N_2})$

Instead of padding of the sequences the same result can be achived using slices and if / else branching.

Concerning a product of two polynomials, first note that mutiplication of a polynomial P(x) by $x^K$ increases the power of each term by *K*, i.e. $x^K * P(x) \rightarrow \sum_{i=0}^N{a_i*x^{i+K}}$, which is equivalent by left padding of the sequence representation by *K* zeroes. Therefore, the product $P_1(x) * P_2(x)$ can be calculated as per-element sum of $N_2$ sequences of the length $N_1 + N_2$ each as $(0, \dots, 0, b_{N_2} * a_0, \dots, b_{N_2} * a_{N_1}) + (0, \dots, 0, b_{N_2-1} * a_0, \dots, b_{N_2-1} * a_{N_1}, 0) + \dots + (b_0 * a_0, \dots, b_0 * a_{N-1}, 0, \dots, 0)$.

The exponentiation / raise to a positive integer power N can thus be calculated as N-1 products directly. Alternatively, especially for large N, a special trick can be applied, which logarithmically reduces the number of products. First, K > 0 should be found such $2^K \leq N < 2^{K+1}$, hence $N = 2^K + M$, where $0 \leq M < 2^K$. So the required power can be calculated as K squaring followed by M multiplication as $((P(x)^2)^2 \dots )^2*P(x)*\dots*P(x)$.

Construction of a polynomial from its roots is, in essence, N-1 multiplications, however each step is reduced to a single per-element summation. Indeed, consider the already calculated part, which is a polynomial of degree N (starting from $x-x_1 \rightarrow (-x_1, 1)$ term, expressing the first passed root) $P(x)*(x-x_{N+1}) \rightarrow (-x_{N+1} * a_0, a_0 - x_{N+1} * a_1, a_1 - x_{N+1} * a_2, \dots, a_{N-1} - x_{N+1} * a_N, a_N)$, where $a_N = 1$ at each step.

Considering the polynomial division, the quotient should be calculated only if the degree of the divident is greater than or equal to the degree of the divisor. First, the coefficient $c = a_{N_1} /  b_{N_2}$ is calculated, which is the coefficient of the $N_1 -N_2$ power term of the quotient (highest). Then the difference is calculated $P_1(x) - x^{N_1-N_2}*P_2(x) \rightarrow (a_0, \dots, a_{N_1-N_2 - 1}, a_{N_1-N_2} - c * b_0, \dots, a_{N_1-1} - c * b_{N_2-1})$ (length $N_1 - 1$). Then the procedure is repeated recursively with substitution of the $P_1(x)$ by the reuslt of the previous step and respective adjustment of the degree $N_1$. The process continues until the length of the sequence resulting from the substraction reaches $N_2 -1$. All right-side consecutive zero values are removed, and the remaining sequence represents the residuals, whereas all accumulated coefficients *c* (in each respected step) are the coefficients of the quotient (in the reverse order!). **Note**, that a sequence of only one element (including zero value) is not a polynomial, but a scalar (numeric) value.

Calculation of the first derivative and anti-derivative are also straight forward per-element sequence manipulations: $\frac{dP(x)}{dx} \rightarrow (a_1, 2 * a_2, \dots, N*a_N)$ and $\int{P(x)} \rightarrow (0, a_0, a_1 / 2, \dots, a_N /(N+1))$, with the free coeffient (integration constant) being chosen as zero. The generic K-th derivative $(K \leq N)$ can be calculated recursively or directly using either the looped correction factors calculation (as in the definition) or the factorial expressions as $\frac{d^KP(x)}{dx^K} \rightarrow (K! * a_K, (K+1)! * a_{K+1}, \frac{(K+2)!}{2!} * a_{K+2}, \dots, \frac{N!}{K!} * a_N)$, where $0!=1!=1$. And for $K > N$ the derivative is zero.

Finally, considering the evaluation of a polynomial it is possible to calculate the sum of power directly, however, an alternative algorithm is preferable, which is based on the following expression

$$
P(x) = a_0 + a_1 * x + a_2 * x^2 + ... + a_N * x^N = \newline
= a_0 + x * (a_1 + x * (a_2 + x * (...(a_{N-1} + x * a_N) )))
$$

Apparently, this algorithm can be implemented iteratively given the sequence representation of the polynomial.
