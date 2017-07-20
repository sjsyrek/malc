# JavaScript ES2015

Arrow functions make this nicer.

Load the `malc.html` page into your browser and test the functions in your JavaScript console (which should report that the included tests have passed). Or use [node](https://nodejs.org/en/). For the separate FizzBuzz implementation, load `fizzbuzz.html`. Loading both at once may cause browser stack death.

## How to write a recursive function using lambdas in JavaScript

1. Write the function as you normally would without a fixpoint combinator:
```js
FACT = n =>
  IS_ZERO(n)
    (ONE)
    (MULT(n)(FACT(PRED(n))))
```

2. Wrap the whole thing in `FIX`, add a parameter (e.g. `r`) to the front of the definition, and replace all recursive function calls with that parameter:
```js
FACT = FIX(r => n =>
  IS_ZERO(n)
    (ONE)
    (MULT(n)(r(PRED(n)))))
```

3. Wrap the recursive branch of your function in a dummy closure by adding a parameter (e.g. `x`) to the front of that branch and applying the last function in that branch to the same parameter:
```js
FACT = FIX(r => n =>
  IS_ZERO(n)
    (ONE)
    (x => MULT(n)(r(PRED(n)))(x)))
```

With this method, you can easily convert, e.g. Haskell functions, into JavaScript lambdas that work with malc:

```hs
(!!) :: [a] -> Int -> a
(x:_)  !! 0 = x
(_:xs) !! n = xs !! (n-1)
```

Becomes:

```js
INDEX = FIX(r => xs => n =>
  IF_THEN_ELSE(IS_ZERO(n))
    (HEAD(xs))
    (x => r(TAIL(xs))(PRED(n))(x)))
```

## FizzBuzz

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

`FIZZBUZZFUNC_EXP` is the same expression [expanded into un-abstracted function calls](fizzbuzz_javascript.md).

Test the FizzBuzz functions as follows:

`toFizzBuzz(FIZZBUZZFUNC(RANGE(ONE)(FIFTEEN)))`
`toFizzBuzz(FIZZBUZZFUNC_EXP(RANGE(ONE)(FIFTEEN)))`

You should get the following output for both:

```js
[1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]
```