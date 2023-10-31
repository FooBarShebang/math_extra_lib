# Requirements for the module math_extra_lib.poly_solver

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Descriprion / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requiement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-500

**Title:** Content of the module

**Description:** The module implements the following functions

* Calculation of all complex number roots of a polynomial
* Calculation of the base Lagrange polynomials for the given x-values grid, which can be not equidistant
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Lagrange base, x-grid may be not equidistant
* Calculation of a Legendre polynomial of an arbitrary degree N >= 0 and of the complete base set of polynomials up to the N-th degree
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Legendre base, x-grid may be not equidistant
* Calculation of a Chebyshev polynomial of the first kind of an arbitrary degree N >= 0  and of the complete base set of polynomials up to the N-th degree
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Chebyshev base, x-grid may be not equidistant
* Calculation of all Berstein polynomials (N+1 polynomials forming a base) of an arbitrary degree N >= 0
* Calculation of the interpolating polynomial for a set of (x,y) pairs using Berstein base, x-grid may be not equidistant

**Verification Method:** A

---

**Requirement ID:** REQ-FUN-510

**Title:** Roots of a polynomial

**Description:** The function calculating roots of a polynomial should

* Accept only a single argument - instance of **Polynomial** class
* Calculate all roots of the polynomial, including those of multiplicity greater than 1, thus for a polynomial of the degree N there are exactly N real or complex number roots, although the number of unque value roots is 1 <= K <= N
* Return all roots as a list of integer, floating point or complex number, with each root of multiplicity K > 1 being repeated K times in the list

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-520

**Title:** Lagrange base polynomials

**Description:** The function genrating Lagrange base polynomials should

* Accept only a single argument - a flat sequence of unique real number values of the length N > 1 as the x-coordinates grid $\{x_i\}$
* Calculate N polynomials of the degree N-1 such, that each i-th polynomial $l_i(x_i) = 1$ and $l_i(x_j) = 0 \; \forall \; j \neq i$
* Return calculated polynomials as a list of instances of the **Polynomial** class, preserving the order

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-530

**Title:** Lagrange polynomials interpolation

**Description:** The function generating Lagrange base polynomials interpolation should

* Accept only a single argument - a sequence of pairs of $(x_i, y_i)$ (values of a function at the respective points of the x-coordinates grid $\{x_i\}$), which is represented a sequence of 2-element sub-sequences of real numbers
* Calculate the interpolating polynomial of the degree $0 \leq K \leq N-1$ using Lagrange base as $\sum_{i=1}^N{y_i * l_i(x)}$, where *N* is the number of the points
* Return calculated polynomial as an instance of the **Polynomial** class for *K* > 0 and as a real number for *K* = 0

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-540

**Title:** Legendre base polynomials

**Description:** The function generating Legendre base polynomials should

* Accept only a single non-negative integer argument $N \geq 0$
* Calculate N + 1 polynomials of the increasing degree from 0 (constant) to N such, that each i-th polynomial $P_i(x)$ is the i-th degree Legendre polynomial ($0 \leq i \leq N$)
* Return calculated polynomials as a list of instances on the **Polynomial** class, preserving the order
* Calculation of each individual K-th power polynomial shold be delegated to a separate function

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-541

**Title:** Legendre N-th degree polynomial

**Description:** The function generating a single Legendre polynomial should

* Accept only a single non-negative integer argument $N \geq 0$
* Calculate a single Legendre polynomial of the the requested degree *N*
* Return calculated polynomial as an instance on the **Polynomial** class, except for the 0-th degree, in which case it is **int** type

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-550

**Title:** Legendre polynomials interpolation

**Description:** The function generating Legendre base polynomials interpolation should

* Accept only a single argument - a sequence of pairs of $(x_i, y_i)$ (values of a function at the respective points of the x-coordinates grid $\{x_i\}$), which is represented a sequence of 2-element sub-sequences of real numbers
* Calculate the interpolating polynomial of the degree $0 \leq K \leq N-1$ using Legendre base as $\sum_{i=0}^{N-1}{\alpha_i * P_i(Q(x))}$, where *N* is the number of the points, where $Q(x)$ is the 1-st degree (linear) polynomial describing the mapping of the interval $[\mathtt{min}(\{x_i\}), \mathtt{max}(\{x_i\})] \rightarrow [-1, 1]$, and the weighting coefficients $\alpha_i$ are defined by solving the linear equation system generated by the condition $\sum_{i=0}^{N-1}{\alpha_i * P_i(\varepsilon_j)} = y_j$, where $\varepsilon_j = Q(x_j)$
* Return calculated polynomial as an instance of the **Polynomial** class for *K* > 0 and as a real number for *K* = 0

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-560

**Title:** Chebyshev base polynomials

**Description:** The function generating Chebyshev base polynomials should

* Accept only a single non-negative integer argument $N \geq 0$
* Calculate N + 1 polynomials of the increasing degree from 0 (constant) to N such, that each i-th polynomial $T_i(x)$ is the i-th degree Chebyshev polynomial of the first kind ($0 \leq i \leq N$)
* Return calculated polynomials as a list of instances on the **Polynomial** class, preserving the order
* Calculation of each individual K-th power polynomial shold be delegated to a separate function

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-561

**Title:** Chebyshev N-th degree polynomial

**Description:** The function generating a single Chebyshev polynomial should

* Accept only a single non-negative integer argument $N \geq 0$
* Calculate a single Chebyshev polynomial of the first kind of the the requested degree *N*
* Return calculated polynomial as an instance on the **Polynomial** class, except for the 0-th degree, in which case it is **int** type

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-570

**Title:** Chebyshev polynomials interpolation

**Description:** The function generating Chebyshev base polynomials interpolation should

* Accept only a single argument - a sequence of pairs of $(x_i, y_i)$ (values of a function at the respective points of the x-coordinates grid $\{x_i\}$), which is represented a sequence of 2-element sub-sequences of real numbers
* Calculate the interpolating polynomial of the degree $0 \leq K \leq N-1$ using Chebyshev base as $\sum_{i=0}^{N-1}{\alpha_i * T_i(Q(x))}$, where *N* is the number of the points, where $Q(x)$ is the 1-st degree (linear) polynomial describing the mapping of the interval $[\mathtt{min}(\{x_i\}), \mathtt{max}(\{x_i\})] \rightarrow [-1, 1]$, and the weighting coefficients $\alpha_i$ are defined by solving the linear equation system generated by the condition $\sum_{i=0}^{N-1}{\alpha_i * T_i(\varepsilon_j)} = y_j$, where $\varepsilon_j = Q(x_j)$
* Return calculated polynomial as an instance of the **Polynomial** class for *K* > 0 and as a real number for *K* = 0

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-580

**Title:** Berstein base polynomials

**Description:** The function generating Berstein base polynomials should

* Accept only a single non-negative integer argument $N \geq 0$
* Calculate N + 1 polynomials of the N-th degree $b_{i,N}(x)$ is the N-th degree Berstein polynomial ($0 \leq i \leq N$)
* Return calculated polynomials as a list of instances on the **Polynomial** class, preserving the order
* Calculation of each individual K-th power polynomial shold be delegated to a separate function

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-581

**Title:** Berstein N-th degree polynomial

**Description:** The function generating a single Berstein polynomial should

* Accept two non-negative integer arguments $N \geq 0$ (degree) and $0 \leq i \leq N$ (index within the Berstein basis)
* Calculate a single Berstein polynomial $b_{i,N}(x)$
* Return calculated polynomial as an instance on the **Polynomial** class, except for the 0-th degree, in which case it is **int** type

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-590

**Title:** Berstein polynomials interpolation

**Description:** The function generating Berstein base polynomials interpolation should

* Accept only a single argument - a sequence of pairs of $(x_i, y_i)$ (values of a function at the respective points of the x-coordinates grid $\{x_i\}$), which is represented a sequence of 2-element sub-sequences of real numbers
* Calculate the interpolating polynomial of the degree $0 \leq K \leq N-1$ using Bernstein base as $\sum_{i=0}^{N-1}{\alpha_i * b_{i, N-1}(Q(x))}$, where *N* is the number of the points, where $Q(x)$ is the 1-st degree (linear) polynomial describing the mapping of the interval $[\mathtt{min}(\{x_i\}), \mathtt{max}(\{x_i\})] \rightarrow [0, 1]$, and the weighting coefficients $\alpha_i$ are defined by solving the linear equation system generated by the condition $\sum_{i=0}^{N-1}{\alpha_i * b_{i,N-1}(\varepsilon_j)} = y_j$, where $\varepsilon_j = Q(x_j)$
* Return calculated polynomial as an instance of the **Polynomial** class for *K* > 0 and as a real number for *K* = 0

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AMW-500

**Title:** Polynomials basis generation - improper argument type

**Description:** The functions generating polynomials basis (Legendre, Chebyshev, Berstein) raise an exception compatible with TypeError if the passed argument is not of the **int** type

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-501

**Title:** Polynomials basis generation - improper argument value

**Description:** The functions generating polynomials basis (Legendre, Chebyshev, Berstein) raise an exception compatible with ValueError if the passed argument is negative

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-502

**Title:** Base polynomial generation - improper argument type

**Description:** The functions generating base polynomial of degree N (Legendre, Chebyshev) raise an exception compatible with TypeError if the passed argument is not of the **int** type

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-503

**Title:** Base polynomial generation - improper argument value

**Description:** The functions generating base polynomial of degree N (Legendre, Chebyshev) raise an exception compatible with ValueError if the passed argument is negative

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-504

**Title:** Interpolation polynomial - improper argument type

**Description:** The functions generating interpolation polynomial on an arbitrary x-grid (Lagrange, Legendre, Chebyshev, Bernstein) raise an exception compatible with TypeError if the passed argument is not a sequence of 2-element sub-sequences of real numbers

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-505

**Title:** Interpolation polynomial - improper x-grid values

**Description:** The functions generating interpolation polynomial on an arbitrary x-grid (Lagrange, Legendre, Chebyshev, Bernstein) raise an exception compatible with ValueError if there is, at least, 1 not unique value amongst the first elements of the sub-sequences (x-grid with non-unique values)

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-510

**Title:** Polynomial's roots - improper argument type

**Description:** The function calculating the roots of a polynomial raises an exception compatible with TypeError if the passed argument is not an instance of **Polynomial** class

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-520

**Title:** Lagrange base - improper argument type

**Description:** The function calculating the Lagrange base polynomials raises an exception compatible with TypeError if the passed argument is not a sequence or any of its element is nor a real number

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-521

**Title:** Lagrange base - improper x-grid

**Description:** The function calculating the Lagrange base polynomials raises an exception compatible with ValueError if:

* the passed sequence of real numbers contains less than 2 elements
* the passed sequence contains, at least, one non-unique value (repetition of the values)

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-580

**Title:** Berstein polynomial generation - improper argument type

**Description:** The function generating Bersteing polynomial raises an exception compatible with TypeError if:

* the first argument (degree) is not of the **int** type
* the second argument (index) is not of the **int** type

**Verification Method:** T

---

**Requirement ID:** REQ-AMW-581

**Title:** Berstein polynomial generation - improper argument value

The function generating Bersteing polynomial raises an exception compatible with ValueError if:

* the first argument (degree) is negative
* the second argument (index) is negative
* the second argument is larger than the first

**Verification Method:** T
