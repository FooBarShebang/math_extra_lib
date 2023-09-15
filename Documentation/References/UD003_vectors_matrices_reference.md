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

## Design and Implementation

![Class diagram](..\UML\vectors_matrices\vectors_matrices_classes.png)

## API Reference

### Class Array2D

### Class Vector

### Class Column

### Class Row

### Class Matrix

### Class SquareMatrix
