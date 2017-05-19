# malc - Make a Lambda Calculus

## About

Malc is a guide and specification for implementing an untyped [lambda calculus](https://en.wikipedia.org/wiki/Lambda_calculus) in any programming language that supports [higher-order functions](https://en.wikipedia.org/wiki/Higher-order_function). Contributions that generally follow the specification below, as well as clever or more ambitious extensions of it in the spirit of this project, are welcome.

Inspired by the [Make a Lisp](https://github.com/kanaka/mal) project.

## Implementations

* [JavaScript ES2015](/javascript/README.md)
* [Python 3](/python/README.md)

## Specification

This is only a partial list of functions that each implementation should provide. For other examples, read the code.

```
ID = λx. x
```

Identity combinator. Returns `x`.

***

```
TRUE = λx. λy. x
FALSE = λx. λy. y
```

Boolean true and false.

***

```
AND = λx. λy. x y FALSE
OR = λx. λy. x TRUE y
NOT = λx. x FALSE TRUE
XOR = λx. λy. NOT(AND x y)
```

Boolean combinators.

***

```
IF_THEN_ELSE = λp. λx. λy. p x y
```

Conditional branching. Note that `IF_THEN_ELSE` is identical in value to `ID`.

***

```
ZERO = λf. λx. x
ONE = λf. λx. f x
TWO = λf. λx. f(f(x))
THREE = λf. λx. f(f(f(x)))
```

Natural numbers.

***

```
SUCC = λn. λf. λx. f(n f x)
```

Given a number, return the following number.

***

```
PRED = λn. n(λp. λz. z(SUCC(p TRUE))(p TRUE))(λz. z ZERO ZERO) FALSE
```

Given a number, return the preceding number down to `ZERO`.

***

```
PLUS = λn. λm. m SUCC n
```

Add two numbers.

***

```
MINUS = λn. λm. m PRED n
```

Subtract one number from another, down to `ZERO`.

***

```
MULT = λn. λm. m(PLUS n) ZERO
```

Multiply two numbers.

***

```
EXP = λn. λm. m n
```

Exponentiation. Returns n^m.

***

```
IS_ZERO = λn. n(λm. FALSE) TRUE
```

Check whether a number is equal to `ZERO`.

***

```
LESS_THAN_OR_EQUAL = λn. λm. IS_ZERO(MINUS n m)
LESS_THAN = λn. λm. AND(LESS_THAN_OR_EQUAL n m)(NOT IS_ZERO(n(PRED m)))
EQUALS = λn. λm. AND(LESS_THAN_OR_EQUAL n m)(LESS_THAN_OR_EQUAL m n)
GREATER_THAN_OR_EQUAL = λn. λm. IS_ZERO(n(PRED m))
GREATER_THAN = λn. λm. AND(GREATER_THAN_OR_EQUAL n m)(NOT(IS_ZERO(MINUS n m)))
```

General predicates for comparing the ordering of numbers.

***

```
COMPOSE = λf. λg. λx. f(g x)
```

Function composition.

***

```
FIX = λy. (λx. y(x x))(λx. y(x x))
```

The fixpoint "Z" combinator, for defining recursive functions (see above).

***

```
PAIR = λx. λy. λp. p x y
```

Create a pair (2-tuple) out of two numbers.

***

```
FIRST = λp. p(λx. λy. x)
SECOND = λp. p(λx. λy. y)
```

First and second projections on a pair. Return the first or second value, respectively.

***

```
LIST_ELEMENT = λx. λxs. PAIR FALSE (PAIR x xs)
```

Prepend an element `x` onto the front of a list `xs`. Use `EMPTY_LIST` for `xs` when creating a new list.

***

```
EMPTY_LIST = PAIR TRUE TRUE
```

The empty list.

***

```
IS_EMPTY = FIRST
```

Check whether a list is `EMPTY_LIST`.

***

```
HEAD = λxs. FIRST (SECOND xs)
```

Return the first element of a list.

***

```
TAIL = λxs. SECOND(SECOND xs)
```

Return the rest of a list after and not including the first element.

***

```
FACT = FIX(λr. λn. IS_ZERO n ONE)(λx. MULT n (r(PRED n)) x)
```

Return the factorial of `n`.

***

```
FIB = FIX(λr. λn. IS_ZERO n ZERO(IF_THEN_ELSE(EQUALS n ONE)(λx. PLUS(r(MINUS n ONE))(r(MINUS n TWO)) x)))
```

Return the `n`th Fibonacci number after `ZERO`.