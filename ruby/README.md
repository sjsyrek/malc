# Ruby

For some reason, Ruby calls them procs even though the language also has lambdas. And blocks. I don't really know the difference, and I don't really care. I'm not a Rubyist, so please don't email me about this.

Load the code into irb:
```
irb -W0 -r ./malc.rb
```
And then test to your heart's content. Rubyists love testing, right? Note the `-W0` option, which suppresses annoying warnings you don't need to worry about.

## How to write a recursive function using procs in Ruby

1. Write the function as you normally would without a fixpoint combinator:
```ruby
FACT = -> n { \
  IS_ZERO[n] \
    [ONE] \
    [MULT[n][r[PRED[n]]]] \
  }
```

2. Wrap the whole thing in `FIX`, add a parameter (e.g. `r`) to the front of the definition, and replace all recursive function calls with that parameter:
```ruby
FACT = FIX[-> r { -> n { \
  IS_ZERO[n] \
    [ONE] \
    [MULT[n][r[PRED[n]]]] \
  } } \
]
```

3. Wrap the recursive branch of your function in a dummy closure by adding a parameter (e.g. `x`) to the front of that branch and applying the last function in that branch to the same parameter:
```ruby
FACT = FIX[-> r { -> n { \
  IS_ZERO[n] \
    [ONE] \
    [-> x { MULT[n][r[PRED[n]]][x] }] \
  } } \
]
```

With this method, you can easily convert, e.g. Haskell functions, into Ruby procs that work with malc:

```hs
(!!) :: [a] -> Int -> a
(x:_)  !! 0 = x
(_:xs) !! n = xs !! (n-1)
```

Becomes:

```ruby
INDEX = FIX[-> r { -> xs { -> n { \
  IF_THEN_ELSE[IS_ZERO[n]] \
    [HEAD[xs]] \
    [-> x { r[TAIL[xs]][PRED[n]][x] }] \
  } } } \
]
```

## FizzBuzz

_Inspired by Tom Stuart, [Understanding Computation](https://www.amazon.co.uk/gp/product/1449329276/ref=as_li_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=1449329276&linkCode=as2&tag=computationclub-21&linkId=Y33MSPW2C4U3YVP5) and [Programming with Nothing](https://speakerdeck.com/tomstuart/programming-with-nothing)_

```ruby
FIZZBUZZFUNC = MAP[-> n { \
  IF_THEN_ELSE[IS_ZERO[MOD[n][FIFTEEN]]] \
    [FIZZBUZZ] \
    [IF_THEN_ELSE[IS_ZERO[MOD[n][THREE]]] \
      [FIZZ] \
      [IF_THEN_ELSE[IS_ZERO[MOD[n][FIVE]]] \
        [BUZZ] \
        [n] \
    ]] \
}]
```

`FIZZBUZZFUNC_EXP` is the same expression [expanded into un-abstracted function calls](fizzbuzz_ruby.md).

Test the FizzBuzz functions as follows:

```ruby
To_FizzBuzz[FIZZBUZZFUNC[RANGE[ONE][FIFTEEN]]]

To_FizzBuzz[FIZZBUZZFUNC_EXP[RANGE[ONE][FIFTEEN]]]
```

You should get the following output for both:

```ruby
[1, 2, "Fizz", 4, "Buzz", "Fizz", 7, 8, "Fizz", "Buzz", 11, "Fizz", 13, 14, "FizzBuzz"]
```