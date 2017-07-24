# Perl 6

The syntax is remarkably similar to Ruby, or Ruby is remarkably similar to Perl. Or Perl 6 is remarkably similar to Ruby, which is remarkably similar to Perl 5, 4, 3, 2, 1. Except everything looks like money, the error messages are completely unhelpful, and you can use parens instead of brackets in your function calls.

Fire up the Perl 6 "REPL" and evaluate the code as follows:
```
EVALFILE 'malc.pl'
```
Or test directly from the command line:
```
perl6 malc.pl
```
You will have to test it using `say` statements in the original file since this isn't a proper REPL. Supposedly, there is a way to import the code as a module, and you may feel free to submit a pull request to make it so.

## How to write a recursive function using anonymous functions in Perl 6

1. Write the function as you normally would without a fixpoint combinator:
```perl
my $FACT = -> $n {\
  $IS_ZERO($n)\
    ($ONE)\
    ($MULT($n)($r($PRED($n)))($x))\
  }
```

2. Wrap the whole thing in `FIX`, add a parameter (e.g. `r`) to the front of the definition, and replace all recursive function calls with that parameter:
```perl
my $FACT = $FIX(-> $r { -> $n {\
  $IS_ZERO($n)\
    ($ONE)\
    ($MULT($n)($r($PRED($n)))($x))\
  } }\
);
```

3. Wrap the recursive branch of your function in a dummy closure by adding a parameter (e.g. `x`) to the front of that branch and applying the last function in that branch to the same parameter:
```perl
my $FACT = $FIX(-> $r { -> $n {\
  $IS_ZERO($n)\
    ($ONE)\
    (-> $x { $MULT($n)($r($PRED($n)))($x) })\
  } }\
);
```

With this method, you can easily convert, e.g. Haskell functions, into Perl 6 anonymous functions that work with malc:

```hs
(!!) :: [a] -> Int -> a
(x:_)  !! 0 = x
(_:xs) !! n = xs !! (n-1)
```

Becomes:

```perl
my $INDEX = $FIX(-> $r { -> $xs { -> $n {\
  $IF_THEN_ELSE($IS_ZERO($n))\
    ($HEAD($xs))\
    (-> $x { $r($TAIL($xs))($PRED($n))($x) })\
  } } }\
);
```

## FizzBuzz

_Inspired by Tom Stuart, [Understanding Computation](https://www.amazon.co.uk/gp/product/1449329276/ref=as_li_tl?ie=UTF8&camp=1634&creative=19450&creativeASIN=1449329276&linkCode=as2&tag=computationclub-21&linkId=Y33MSPW2C4U3YVP5) and [Programming with Nothing](https://speakerdeck.com/tomstuart/programming-with-nothing)_

```perl
my $FIZZBUZZFUNC = $MAP(-> $n {\
  $IF_THEN_ELSE($IS_ZERO($MOD($n)($FIFTEEN)))\
    ($FIZZBUZZ)\
    ($IF_THEN_ELSE($IS_ZERO($MOD($n)($THREE)))\
      ($FIZZ)\
      ($IF_THEN_ELSE($IS_ZERO($MOD($n)($FIVE)))\
        ($BUZZ)\
        ($n)\
    ))\
});
```

Test the FizzBuzz function by inserting the following line of code into the `malc.pl` file:

```perl
say $To_FizzBuzz($FIZZBUZZFUNC($RANGE($ONE)($FIFTEEN)));
```

When you evaluate the file, you should get the following output:

```perl
(1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz)
```