# JavaScript ES2015

Arrow functions make this nicer.

Load the `malc.html` page into your browser and test the functions in your JavaScript console. Or use [node](https://nodejs.org/en/). For the separate FizzBuzz implementation, load `fizzbuzz.html`. Loading both at once seems to cause browser stack death.

## How to write a recursive function using lambdas in JavaScript

1. Write the function as you normally would without a fixpoint combinator:
    ```js
    FACT = n =>
      IS_ZERO(n)
        (ONE)
        (MULT(n)(FACT(PRED(n))))
    ```

2. Wrap the whole thing in `FIX`, add a parameter to the front of the definition, and replace all recursive function calls with that parameter:
    ```js
    FACT = FIX(Y => n =>
      IS_ZERO(n)
        (ONE)
        (MULT(n)(Y(PRED(n)))))
    ```

3. Wrap the recursive branch of your function in a dummy closure by adding a parameter to the front of that branch and applying the last function in that branch to the same parameter:
    ```js
    FACT = FIX(Y => n =>
      IS_ZERO(n)
        (ONE)
        (x => MULT(n)(Y(PRED(n)))(x)))
    ```

With this method, you can easily convert, e.g. Haskell functions, into JavaScript lambdas that work with malc:

```hs
(!!) :: [a] -> Int -> a
(x:_)  !! 0 = x
(_:xs) !! n = xs !! (n-1)
```
```js
INDEX = FIX(Y => xs => n =>
  IF_THEN_ELSE(IS_ZERO(n))
    (HEAD(xs))
    (x => Y(TAIL(xs))(PRED(n))(x)))
```

## Function documentation

```js
ID = x => x
```

Identity combinator. Returns `x`.

***

```js
TRUE = x => y => x
FALSE = x => y => y
```

Boolean true and false.

***

```js
AND = x => y => x(y)(FALSE)
OR = x => y => x(TRUE)(y)
NOT = x => x(FALSE)(TRUE)
XOR = x => y => NOT(AND(x)(y))
```

Boolean combinators.

***

```js
IF_THEN_ELSE = p => x => y => p(x)(y)
```

Conditional branching. Note that `IF_THEN_ELSE` is identical in value to `ID`.

***

```js
ZERO = f => x => x
ONE = f => x => f(x)
TWO = f => x => f(f(x))
THREE = f => x => f(f(f(x))) // etc.
```

Natural numbers.

***

```js
SUCC = n => f => x => f(n(f)(x))
```

Given a number, return the following number.

***

```js
PRED = n => n(p => z => z(SUCC(p(TRUE)))(p(TRUE)))(z => z(ZERO)(ZERO))(FALSE)
```

Given a number, return the preceding number down to `ZERO`.

***

```js
PLUS = n => m => m(SUCC)(n)
```

Add two numbers.

***

```js
MINUS = n => m => m(PRED)(n)
```

Subtract one number from another, down to `ZERO`.

***

```js
MULT = n => m => m(PLUS(n))(ZERO)
```

Multiply two numbers.

***

```js
EXP = n => m => m(n)
```

Exponentiation. Returns n^m (equivalent to `n**m`).

***

```js
IS_ZERO = n => n(m => FALSE)(TRUE)
```

Check whether a number is equal to `ZERO`.

***

```js
LESS_THAN_OR_EQUAL = n => m => IS_ZERO(MINUS(n)(m))
LESS_THAN = n => m => AND(LESS_THAN_OR_EQUAL(n)(m))(NOT(IS_ZERO(n(PRED)(m))))
EQUALS = n => m => AND(LESS_THAN_OR_EQUAL(n)(m))(LESS_THAN_OR_EQUAL(m)(n))
GREATER_THAN_OR_EQUAL = n => m => IS_ZERO(n(PRED)(m))
GREATER_THAN = n => m => AND(GREATER_THAN_OR_EQUAL(n)(m))(NOT(IS_ZERO(MINUS(n)(m))))
```

General predicates for comparing the ordering of numbers.

***

```js
MAX = x => y => IF_THEN_ELSE(LESS_THAN_OR_EQUAL(x)(y))(y)(x)
MIN = x => y => IF_THEN_ELSE(EQUALS(MAX(x)(y))(x))(y)(x)
```

Return the greater or lesser of two numbers, respectively.

***

```js
COMPOSE = f => g => x => f(g(x))
```

Function composition.

***

```js
FIX = f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y)))
```

The fixpoint "Z" combinator, for defining recursive functions (see above).

***

```js
MOD = FIX(Y => n => m =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => Y(MINUS(n)(m))(m)(x))
    (n))
```

Modulus of two numbers.
	
***

```js
DIV = FIX(Y => n => m =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => SUCC(Y(MINUS(n)(m))(m))(x))
    (ZERO))
```

Divide two numbers.

***

```js
EVEN = n => IS_ZERO(MOD(n)(TWO))
ODD = COMPOSE(NOT)(EVEN)
```

Check whether a number is even or odd, respectively.

***

```js
PAIR = x => y => p => p(x)(y)
```

Create a pair (2-tuple) out of two numbers.

***

```js
FIRST = p => p(x => y => x)
SECOND = p => p(x => y => y)
```

First and second projections on a pair. Return the first or second value, respectively.

***

```js
LIST_ELEMENT = x => xs => PAIR(FALSE)(PAIR(x)(xs))
```

Prepend an element `x` onto the front of a list `xs`. Use `EMPTY_LIST` for `xs` when creating a new list, i.e. `LIST_ELEMENT(ONE)(LIST_ELEMENT(TWO)(LIST_ELEMENT(THREE)(EMPTY_LIST)))`.

***

```js
EMPTY_LIST = PAIR(TRUE)(TRUE)
```

The empty list.

***

```js
IS_EMPTY = FIRST
```

Check whether a list is `EMPTY_LIST`.

***

```js
HEAD = xs => FIRST(SECOND(xs))
```

Return the first element of a list.

***

```js
TAIL = xs => SECOND(SECOND(xs))
```

Return the rest of a list after and not including the first element.

***

```js
FOLD = FIX(Y => f => z => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (z)
    (x => f(HEAD(xs))(Y(f)(z)(TAIL(xs)))(x)))
```
Fold a binary function `f` with accumulator `z` over a list `xs` and return the result.

***

```js
MAP = f => FOLD(x => xs => LIST_ELEMENT(f(x))(xs))(EMPTY_LIST)
```

Apply a function `f` to every element in a list `xs`.

***

```js
FILTER = p => FOLD(x => xs =>
  IF_THEN_ELSE(p(x))
    (LIST_ELEMENT(x)(xs))
    (xs))
   (EMPTY_LIST)
```
Given a predicate function `p` and list `xs`, return a new list of only those elements of `xs` for which `p` returns `TRUE`.

***

```js
RANGE = FIX(Y => m => n =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => LIST_ELEMENT(m)(Y(SUCC(m))(n))(x))
    (EMPTY_LIST))
```

Create a new list within a specified range, i.e. `RANGE(ONE)(TEN)` for a list of consecutive values from `ONE` to `TEN`.

***

```js
INDEX = FIX(Y => xs => n =>
  IF_THEN_ELSE(IS_ZERO(n))
    (HEAD(xs))
    (x => Y(TAIL(xs))(PRED(n))(x)))
```

Return the value at index `n` of list `xs`.

***

```js
PUSH = x => xs => FOLD(LIST_ELEMENT)(LIST_ELEMENT(x)(EMPTY_LIST))(xs)
```

Append the value `x` to the end of the list `xs`.

***

```js
APPEND = FIX(Y => xs => ys =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (ys)
    (x => LIST_ELEMENT(HEAD(xs))(Y(TAIL(xs))(ys))(x)))
```

Append a list `ys` onto the end of a list `xs`.

***

```js
LENGTH = xs => (FIX(Y => xs => n =>
	IF_THEN_ELSE(IS_EMPTY(xs))
	  (n)
	  (x => Y(TAIL(xs))(SUCC(n))(x))))
	  (xs)(ZERO)
```

Return the length of a list `xs`.

***

```js
REVERSE = xs => (FIX(Y => xs => a =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (a)
    (x => (Y(TAIL(xs))(LIST_ELEMENT(HEAD(xs))(a)))(x))))
  (xs)(EMPTY_LIST)
```

Return a list with the elements of a list `xs` in reverse order.

***

```js
TAKE = FIX(Y => n => xs =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(n)(ZERO))
	   (EMPTY_LIST)
	   (IF_THEN_ELSE(IS_EMPTY(xs)))
	     (EMPTY_LIST)
	     (x => LIST_ELEMENT(HEAD(xs))(Y(MINUS(n)(ONE))(TAIL(xs)))(x)))
```

Return a list comprised of the first `n` elements of a list `xs`.

***

```js
ZIP = FIX(Y => xs => ys =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(ys))
      (EMPTY_LIST)
      (x => LIST_ELEMENT(PAIR(HEAD(xs))(HEAD(ys)))(Y(TAIL(xs))(TAIL(ys)))(x))))
```

Zip two lists together into a new list of pairs.

***

```js
ZIP_WITH = FIX(Y => f => xs => ys =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(ys))
      (EMPTY_LIST)
      (x => LIST_ELEMENT(f(HEAD(xs))(HEAD(ys)))(Y(f)(TAIL(xs))(TAIL(ys)))(x))))
```

Zip two list together using a custom, binary function.

***

```js
INSERT = FIX(Y => n => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (LIST_ELEMENT(n)(EMPTY_LIST))
    (IF_THEN_ELSE(GREATER_THAN(n)(HEAD(xs)))
      (x => LIST_ELEMENT(HEAD(xs))(Y(n)(TAIL(xs)))(x))
      (LIST_ELEMENT(n)(xs))))
```

Insert a number `n` into a list of numbers at the first position where it is less than or equal to the next number.

***

```js
SORT = FOLD(INSERT)(EMPTY_LIST)
```

Sort a list in ascending order.

***

```js
ZEROS = FIX(Y => LIST_ELEMENT(ZERO)(Y))
```

Return an infinite list in which every element is `ZERO`.

***

```js
REPEAT = x => FIX(Y => LIST_ELEMENT(x)(Y))
```

Return an infinite list in which every element is `x`.

***

**Monoid**	

```js
MEMPTY = EMPTY_LIST
```

Identity of lists.

```js
MAPPEND = APPEND
```

Associative operation for lists.

***

**Functor**

```js
FMAP = MAP
```

Function mapping for lists.

***

**Applicative**

```js
PURE = x => LIST_ELEMENT(x)(EMPTY_LIST)
```

Identity for applicative list.

```js
AP = FIX(Y => fs => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(fs))(EMPTY_LIST)
      (x => MAPPEND(MAP(HEAD(fs))(xs))(Y(TAIL(fs))(xs))(x))))
```

Applicative operation for lists. Applies every function in `fs` to every element in `xs` and returns the result in a new list.

Example:
```js
LIST = RANGE(ONE)(THREE)
FUNC_LIST = MAP(PLUS)(LIST)
AP_LIST = AP(FUNC_LIST)(LIST)
// toArrayInt(AP_LIST) = [2,3,4,3,4,5,4,5,6]
```

***

```js
AP_ZIP_LIST = fs => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(fs))(EMPTY_LIST)
      (ZIP_WITH(ID)(fs)(xs)))
```

Applicative operation for zip lists. Applies each function in `fs` to each parallel element in `xs` and returns the result in a new list.

Example:
```js
LIST = RANGE(ONE)(THREE)
FUNC_LIST = MAP(PLUS)(LIST)
ZIP_LIST = AP_ZIP_LIST(FUNC_LIST)(REVERSE(LIST))
// toArrayInt(ZIP_LIST) = [4,4,4]
```

***

**Monad**

```js
RETURN = PURE
```

Identity for monadic list.

```js
BIND = FIX(Y => xs => f =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (x => MAPPEND(f(HEAD(xs)))(Y(TAIL(xs))(f))(x)))
```

Binding operation (or "flat map") for lists.

Example:
```js
LIST = RANGE(ONE)(THREE)
BIND_SQUARE = x => RETURN(EXP(x)(TWO))
BIND_CUBE = x => RETURN(EXP(x)(THREE))
BIND_LIST = BIND(BIND(LIST)(BIND_SQUARE))(BIND_CUBE)
// toArrayInt(BIND_LIST) = [1,64,729]
```

***

**Factorial**

```js
FACT = FIX(Y => n =>
  IS_ZERO(n)
    (ONE)
    (x => MULT(n)(Y(PRED(n)))(x)))
```
Return the factorial of `n`.

```js
F = f => n => IS_ZERO(n)(ONE)(x => MULT(n)(f(PRED(n)))(x))

FACT = FIX(F)

AND_EQUALS_TWO = COMPOSE(AND)(EQUALS(TWO))

ALL_TWOS = FOLD(AND_EQUALS_TWO)(TRUE)

FACT_CHECK = ALL_TWOS(
  LIST_ELEMENT(
    FACT(TWO)
  )(LIST_ELEMENT(
    FIX(F)(TWO)
  )(LIST_ELEMENT(
    (Y => (x => Y(y => x(x)(y)))(x => Y(y => x(x)(y))))(F)(TWO)
  )(LIST_ELEMENT(
    (x => F(y => x(x)(y)))(x => F(y => x(x)(y)))(TWO)
  )(LIST_ELEMENT(
    F(y => (x => F(y => x(x)(y)))(x => F(y => x(x)(y)))(y))(TWO)
  )(LIST_ELEMENT(
    F(FIX(F))(TWO)
  )(LIST_ELEMENT(
    (f => n => IS_ZERO(n)(ONE)(x => MULT(n)(f(PRED(n)))(x)))(FIX(F))(TWO)
  )(LIST_ELEMENT(
    (n => IS_ZERO(n)(ONE)(x => MULT(n)(FIX(F)(PRED(n)))(x)))(TWO)
  )(LIST_ELEMENT(
    IS_ZERO(TWO)(ONE)(x => MULT(TWO)(FIX(F)(PRED(TWO)))(x))
  )(LIST_ELEMENT(
    x => MULT(TWO)(FIX(F)(PRED(TWO)))(x)
  )(LIST_ELEMENT(
    x => MULT(TWO)(FIX(F)(ONE))(x)
  )(LIST_ELEMENT(
    x => MULT(TWO)(FACT(ONE))(x)
  )(LIST_ELEMENT(
    x => MULT(TWO)(ONE)(x)
  )(LIST_ELEMENT(
    MULT(TWO)(ONE)
  )(LIST_ELEMENT(
    TWO
  )(EMPTY_LIST)))))))))))))))
)
```

Proof that the reduction steps for `FACT` are isomorphic to one another.

`FACT_EXP = (f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(f => n => (n => n(x => x => y => y)(x => y => x))(n)(f => x => f(x))(x => (n => m => m((n => m => m(n => f => x => f(n(f)(x)))(n))(n))(f => x => x))(n)(f((n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n)))(x)))`

Expansion of `FACT` into un-abstracted function calls.

***

**Fibonacci**

```js
FIB = FIX(Y => n =>
  IS_ZERO(n)
    (ZERO)
    (IF_THEN_ELSE(EQUALS(n)(ONE))
      (ONE)
      (x => PLUS(Y(MINUS(n)(ONE)))(Y(MINUS(n)(TWO)))(x))))
```
Return the `n`th Fibonacci number after `ZERO`.

`FIB_EXP = (f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(f => n => (n => n(x => (x => y => y))(x => y => x))(n)(f => x => x)((x => x)((n => m => (x => y => x(y)(x => y => y))((n => m => (n => n(x => (x => y => y))(x => y => x))((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(m)))(n)(m))((n => m => (n => n(x => (x => y => y))(x => y => x))((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(m)))(m)(n)))(n)(f => x => f(x)))(f => x => f(x))(x => (n => m => m(n => f => x => f(n(f)(x)))(n))(f((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(f => x => f(x))))(f((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(f => x => f(f(x)))))(x))))`

Expansion of `FIB` into un-abstracted function calls.

***

**FizzBuzz**

_Inspired by Tom Stuart, [Understanding Computation](https://www.amazon.co.uk/gp/product/1449329276/ref=as_li_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=1449329276&linkCode=as2&tag=computationclub-21&linkId=Y33MSPW2C4U3YVP5) and [Programming with Nothing](https://speakerdeck.com/tomstuart/programming-with-nothing)_

```js
FIZZBUZZFUNC = MAP(n =>
  IF_THEN_ELSE(IS_ZERO(MOD(n)(FIFTEEN)))
    (FIZZBUZZ)
    (IF_THEN_ELSE(IS_ZERO(MOD(n)(THREE)))
      (FIZZ)
      (IF_THEN_ELSE(IS_ZERO(MOD(n)(FIVE)))
        (BUZZ)
        (n))))
```
Apply the FizzBuzz test to a list of numbers. Long lists are likely to make your browser freeze.

Example:
```js
LIST = RANGE(ONE)(FIFTEEN)
FB = FIZZBUZZFUNC(LIST)
// toFizzBuzz(FB) = [1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]
```

[Expansion](FizzBuzz.md) of `FIZZBUZZFUNC` into un-abstracted function calls.

***

**Utility functions**

```js
toBool = b => IF_THEN_ELSE(b)(true)(false)
```

Boolean conversion from lambdas to native.

***

```js
fromBool = b => b ? TRUE : FALSE
```

Boolean conversion from native to lambdas.

***

```js
toInt = n => n(x => x + 1)(0)
```

Integer conversion from lambdas to native.

***

```js
fromInt = n => n == 0 ? f => x => x : f => x => f(fromInt(n - 1)(f)(x))
```
Integer conversion from native to lambdas.

***

```js
toArray = xs => [].concat(toBool(IS_EMPTY(xs)) ? [] : [HEAD(xs)].concat(toArray(TAIL(xs))))
```

Array conversion from lambdas to native. Does not convert elements.

***

```js
fromArray = xs => xs.length === 0 ? EMPTY_LIST : LIST_ELEMENT(xs.slice(0,1))(fromArray(xs.slice(1)))
```

Array conversion from native to lambdas. Does not convert elements.

***

```js
toArrayInt = xs => [].concat(toBool(IS_EMPTY(xs)) ? [] : [toInt(HEAD(xs))].concat(toArrayInt(TAIL(xs))))
```

Convert a list of lambda numbers into a native array of integers.

***

```js
fromArrayInt = xs => xs.length === 0 ? EMPTY_LIST : LIST_ELEMENT(fromInt(xs.slice(0,1)))(fromArrayInt(xs.slice(1)))
```

Convert a native array of integers into a list of lambda numbers.

***

```js
toPair = p => {
  return {fst: FIRST(p), snd: SECOND(p)}
}
```

Convert a lambda pair into a native object.

***

```js
toPairInt = p => {
  return {fst: (toInt(FIRST(p))), snd: (toInt(SECOND(p)))}
}
```

Convert a pair of lambda numbers into a native object.

***

```js
toString = str => toArrayInt(str).map(n => String.fromCharCode(n)).join("")
```

Convert a list of lambda numbers into a native string.

***

```js
fromString = str => str.length === 0 ? EMPTY_LIST : LIST_ELEMENT(fromInt(str.charCodeAt(str.substr(0,1))))(fromString(str.substr(1)))
```

Convert a native string into a list of lambda numbers.

***

```js
toFizzBuzz = fb => toArray(fb).map(x => toString(x) === "" ? toInt(x) : toString(x))
```

Convert the output of `FIZZBUZZFUNC` into a native array.

***

```js
toLambda = x => {
  if (Number.isInteger(x)) return fromInt(x)
  if (typeof x === "boolean") return fromBool(x)
  if (typeof x === 'string') return fromString(x)
  if (Array.isArray(x)) return fromArray(x.map(y => toLambda(y)))
  return x
}
```

Convert any native object into corresponding lambdas, if possible.

***

**Tests**

```js
p = PAIR(ONE)(TWO)
l = RANGE(ONE)(THREE)

tests = {
  id: ID(1) === 1,
  true: TRUE(1)(0) === 1,
  false: FALSE(1)(0) === 0,
  and: toBool(AND(FALSE)(TRUE)) === false,
  or: toBool(OR(FALSE)(TRUE)) === true,
  not: toBool(NOT(TRUE)) === false,
  xor: toBool(XOR(TRUE)(TRUE)) === false,
  ifThenElse: toBool(IF_THEN_ELSE(IS_ZERO(ZERO))(TRUE)(FALSE)) === true,
  zero: toInt(ZERO) === 0,
  one: toInt(ONE) === 1,
  two: toInt(TWO) === 2,
  three: toInt(THREE) === 3,
  four: toInt(FOUR) === 4,
  five: toInt(FIVE) === 5,
  six: toInt(SIX) === 6,
  seven: toInt(SEVEN) === 7,
  eight: toInt(EIGHT) === 8,
  nine: toInt(NINE) === 9,
  ten: toInt(TEN) === 10,
  succ: toInt(SUCC(ONE)) === 2,
  pred: toInt(PRED(ONE)) === 0,
  plus: toInt(PLUS(TWO)(TWO)) === 4,
  minus: toInt(MINUS(TWO)(ONE)) === 1,
  mult: toInt(MULT(TWO)(THREE)) === 6,
  exp: toInt(EXP(TWO)(THREE)) === 8,
  isZero: toBool(IS_ZERO(ZERO)) === true,
  lessThanOrEqual: toBool(LESS_THAN_OR_EQUAL(ZERO)(ZERO)) === true,
  lessThan: toBool(LESS_THAN(ZERO)(ONE)) === true,
  equals: toBool(EQUALS(ONE)(ONE)) === true,
  greaterThanOrEqual: toBool(GREATER_THAN_OR_EQUAL(ONE)(ZERO)) === true,
  greaterThan: toBool(GREATER_THAN(ONE)(ZERO)) === true,
  max: toInt(MAX(ONE)(TWO)) === 2,
  min: toInt(MIN(ONE)(TWO)) === 1,
  compose: COMPOSE(ID)(ID)(1) === ID(ID(1)),
  mod: toInt(MOD(TEN)(TWO)) === 0,
  div: toInt(DIV(TEN)(TWO)) === 5,
  even: toBool(EVEN(TWO)) === true,
  odd: toBool(ODD(TWO)) === false,
  pair: toPairInt(p).fst === 1 && toPairInt(p).snd === 2,
  first: toInt(FIRST(p)) === 1,
  second: toInt(SECOND(p)) === 2,
  emptyList: toBool(AND(FIRST(EMPTY_LIST))(SECOND(EMPTY_LIST))) === true,
  isEmpty: toBool(AND(IS_EMPTY(EMPTY_LIST))(NOT(IS_EMPTY(l)))) === true,
  head: toInt(HEAD(l)) === 1,
  tail: toArrayInt(TAIL(l)).every((e,i) => e === [2,3][i]),
  fold: toInt(FOLD(PLUS)(ZERO)(l)) === 6,
  map: toArrayInt(MAP(PLUS(ONE))(l)).every((e,i) => e === [2,3,4][i]),
  filter: toInt(HEAD(FILTER(EVEN)(l))) === 2,
  range: toArrayInt(l).every((e,i) => e === [1,2,3][i]),
  index: toInt(INDEX(l)(ZERO)) === 1,
  push: toArrayInt(PUSH(FOUR)(l)).every((e,i) => e === [1,2,3,4][i]),
  append: toArrayInt(APPEND(l)(l)).every((e,i) => e === [1,2,3,1,2,3][i]),
  length: toInt(LENGTH(l)) === 3,
  reverse: toArrayInt(REVERSE(l)).every((e,i) => e === [3,2,1][i]),
  take: toArrayInt(TAKE(TWO)(l)).every((e,i) => e === [1,2][i]),
  zip: toArray(ZIP(l)(l)).map(x => toPairInt(x)).every((e,i) => e.fst === i+1 && e.snd === i+1),
  zipWith: toArrayInt(ZIP_WITH(PLUS)(l)(REVERSE(l))).every((e,i) => e === [4,4,4][i]),
  insert: toArrayInt(INSERT(ZERO)(l)).every((e,i) => e === [0,1,2,3][i]),
  sort: toArrayInt(SORT(REVERSE(l))).every((e,i) => e === toArrayInt(l)[i]),
  zeros: toArrayInt(TAKE(THREE)(ZEROS)).every((e,i) => e === [0,0,0][i]),
  repeat: toArrayInt(TAKE(THREE)(REPEAT(ONE))).every((e,i) => e === [1,1,1][i]),
  pure: toArrayInt(PURE(ONE))[0] === 1,
  ap: toArrayInt(AP(MAP(PLUS)(l))(l)).every((e,i) => e === [2,3,4,3,4,5,4,5,6][i]),
  apZipList: toArrayInt(AP_ZIP_LIST(MAP(PLUS)(l))(REVERSE(l))).every((e,i) => e === [4,4,4][i]),
  bind: toArrayInt(BIND(l)(RETURN(x => RETURN(PLUS(x)(ONE))))).every((e,i) => e === [2,3,4][i]),
  fact: toInt(FACT(TWO)) === 2,
  factCheck: toBool(FACT_CHECK),
  factExp: toInt(FACT_EXP(TWO)) === 2,
  fib: toInt(FIB(SIX)) === 8,
  fibExp: toInt(FIB_EXP(SIX)) === 8
}

allTests = () => Object.values(tests).reduce((x, y) => x && y)
```

`allTests()` should return `true` if every element in `tests` is `true`.
