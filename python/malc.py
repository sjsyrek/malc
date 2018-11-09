
import sys
import unittest

sys.setrecursionlimit(10000)

# malc - make a lambda calculus
# Python 3
# Steven Syrek

# identity combinator

ID = lambda x: x

# boolean primitives

TRUE = lambda x: lambda y: x

FALSE = lambda x: lambda y: y

# boolean combinators

AND = lambda x: lambda y: x(y)(FALSE)

OR = lambda x: lambda y: x(TRUE)(y)

NOT = lambda x: x(FALSE)(TRUE)

XOR = lambda x: lambda y: x(NOT(y))(y)

# branching

IF_THEN_ELSE = lambda p: lambda x: lambda y: p(x)(y) # IF_THEN_ELSE = ID

# natural numbers

ZERO = lambda f: lambda x: x

ONE = lambda f: lambda x: f(x)

TWO = lambda f: lambda x: f(f(x))

THREE = lambda f: lambda x: f(f(f(x)))

# enumeration

SUCC = lambda n: lambda f: lambda x: f(n(f)(x))

PRED = lambda n: n(lambda p: lambda z: z(SUCC(p(TRUE)))(p(TRUE)))(lambda z: z(ZERO)(ZERO))(FALSE) 

# basic arithmetic

PLUS = lambda n: lambda m: m(SUCC)(n)

MINUS = lambda n: lambda m: m(PRED)(n)

MULT = lambda n: lambda m: m(PLUS(n))(ZERO)

EXP = lambda n: lambda m: m(n)

# more numbers

FOUR = SUCC(THREE)

FIVE = PLUS(TWO)(THREE)

SIX = MULT(TWO)(THREE)

SEVEN = SUCC(SUCC(SUCC(SUCC(SUCC(SUCC(ONE))))))

EIGHT = PRED(MULT(THREE)(THREE))

NINE = EXP(THREE)(TWO)

TEN = MINUS(PLUS(EIGHT)(THREE))(ONE)

# conparison

IS_ZERO = lambda n: n(lambda m: FALSE)(TRUE)

LESS_THAN_OR_EQUAL = lambda n: lambda m: IS_ZERO(MINUS(n)(m))

LESS_THAN = lambda n: lambda m: AND(LESS_THAN_OR_EQUAL(n)(m)) \
                                   (NOT(IS_ZERO(n(PRED)(m))))

EQUALS = lambda n: lambda m: AND(LESS_THAN_OR_EQUAL(n)(m)) \
                                (LESS_THAN_OR_EQUAL(m)(n))

GREATER_THAN_OR_EQUAL = lambda n: lambda m: IS_ZERO(n(PRED)(m))

GREATER_THAN = lambda n: lambda m: AND(GREATER_THAN_OR_EQUAL(n)(m)) \
                                      (NOT(IS_ZERO(MINUS(n)(m))))

MAX = lambda x: lambda y: IF_THEN_ELSE(LESS_THAN_OR_EQUAL(x)(y)) \
                                      (y) \
                                      (x)

MIN = lambda x: lambda y: IF_THEN_ELSE(EQUALS(MAX(x)(y))(x)) \
                                      (y) \
                                      (x)

# function composition

COMPOSE = lambda f: lambda g: lambda x: f(g(x))

# recursion

FIX = lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y)))

# advanced arithmetic

MOD = FIX(lambda Y: lambda n: lambda m: \
    IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n)) \
        (lambda x: Y(MINUS(n)(m))(m)(x)) \
        (n))

DIV = FIX(lambda Y: lambda n: lambda m: \
    IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n)) \
        (lambda x: SUCC(Y(MINUS(n)(m))(m))(x)) \
        (ZERO))

# other combinators

EVEN = lambda n: IS_ZERO(MOD(n)(TWO))

ODD = COMPOSE(NOT)(EVEN)

# pairs

PAIR = lambda x: lambda y: lambda p: p(x)(y)

FIRST = lambda p: p(lambda x: lambda y: x)

SECOND = lambda p: p(lambda x: lambda y: y)

# lists

LIST_ELEMENT = lambda x: lambda xs: PAIR(FALSE)(PAIR(x)(xs))

EMPTY_LIST = PAIR(TRUE)(TRUE)

IS_EMPTY = FIRST

HEAD = lambda xs: FIRST(SECOND(xs))

TAIL = lambda xs: SECOND(SECOND(xs))

# fold/map/filter

FOLD = FIX(lambda r: lambda f: lambda z: lambda xs: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (z) \
        (lambda x: f(HEAD(xs))(r(f)(z)(TAIL(xs)))(x)))

MAP = lambda f: FOLD(lambda x: lambda xs: LIST_ELEMENT(f(x))(xs))(EMPTY_LIST)

FILTER = lambda p: FOLD(lambda x: lambda xs: \
    IF_THEN_ELSE(p(x)) \
        (LIST_ELEMENT(x)(xs)) \
        (xs)) \
    (EMPTY_LIST)

# folds

# implement SUM and stuff

# other list functions

RANGE = FIX(lambda r: lambda m: lambda n: \
    IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n)) \
        (lambda x: LIST_ELEMENT(m)(r(SUCC(m))(n))(x)) \
        (EMPTY_LIST))

INDEX = FIX(lambda r: lambda xs: lambda n: \
    IF_THEN_ELSE(IS_ZERO(n)) \
        (HEAD(xs)) \
        (lambda x: r(TAIL(xs))(PRED(n))(x)))

PUSH = lambda x: lambda xs: FOLD(LIST_ELEMENT)(LIST_ELEMENT(x)(EMPTY_LIST))(xs)

APPEND = FIX(lambda r: lambda xs: lambda ys: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (ys) \
        (lambda x: LIST_ELEMENT(HEAD(xs))(r(TAIL(xs))(ys))(x)))

LENGTH = lambda xs: (FIX(lambda r: lambda xs: lambda n: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
	      (n) \
	      (lambda x: r(TAIL(xs))(SUCC(n))(x)))) \
	      (xs)(ZERO)

REVERSE = lambda xs: (FIX(lambda r: lambda xs: lambda a: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (a) \
        (lambda x: (r(TAIL(xs))(LIST_ELEMENT(HEAD(xs))(a)))(x)))) \
    (xs)(EMPTY_LIST)

TAKE = FIX(lambda r: lambda n: lambda xs: \
    IF_THEN_ELSE(LESS_THAN_OR_EQUAL(n)(ZERO)) \
        (EMPTY_LIST) \
        (IF_THEN_ELSE(IS_EMPTY(xs))) \
            (EMPTY_LIST) \
            (lambda x: LIST_ELEMENT(HEAD(xs))(r(MINUS(n)(ONE))(TAIL(xs)))(x)))

ZIP = FIX(lambda r: lambda xs: lambda ys: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (EMPTY_LIST) \
        (IF_THEN_ELSE(IS_EMPTY(ys)) \
            (EMPTY_LIST) \
            (lambda x: LIST_ELEMENT(PAIR(HEAD(xs))(HEAD(ys)))(r(TAIL(xs))(TAIL(ys)))(x))))

ZIP_WITH = FIX(lambda r: lambda f: lambda xs: lambda ys: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (EMPTY_LIST) \
        (IF_THEN_ELSE(IS_EMPTY(ys)) \
            (EMPTY_LIST) \
            (lambda x: LIST_ELEMENT(f(HEAD(xs))(HEAD(ys)))(r(f)(TAIL(xs))(TAIL(ys)))(x))))

INSERT = FIX(lambda r: lambda n: lambda xs: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (LIST_ELEMENT(n)(EMPTY_LIST)) \
        (IF_THEN_ELSE(GREATER_THAN(n)(HEAD(xs))) \
            (lambda x: LIST_ELEMENT(HEAD(xs))(r(n)(TAIL(xs)))(x)) \
            (LIST_ELEMENT(n)(xs))))

SORT = FOLD(INSERT)(EMPTY_LIST)

# streams

ZEROS = FIX(lambda r: LIST_ELEMENT(ZERO)(r))

REPEAT = lambda x: FIX(lambda r: LIST_ELEMENT(x)(r))

# functional structures (list implementations)

# monoid

MEMPTY = EMPTY_LIST

MAPPEND = APPEND

# functor

FMAP = MAP

# applicative

PURE = lambda x: LIST_ELEMENT(x)(EMPTY_LIST)

AP = FIX(lambda r: lambda fs: lambda xs: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (EMPTY_LIST) \
        (IF_THEN_ELSE(IS_EMPTY(fs))(EMPTY_LIST) \
            (lambda x: MAPPEND(MAP(HEAD(fs))(xs))(r(TAIL(fs))(xs))(x))))

AP_ZIP_LIST = lambda fs: lambda xs: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (EMPTY_LIST) \
        (IF_THEN_ELSE(IS_EMPTY(fs))(EMPTY_LIST) \
            (ZIP_WITH(ID)(fs)(xs)))

# monad

RETURN = PURE

BIND = FIX(lambda r: lambda xs: lambda f: \
    IF_THEN_ELSE(IS_EMPTY(xs)) \
        (EMPTY_LIST) \
        (lambda x: MAPPEND(f(HEAD(xs)))(r(TAIL(xs))(f))(x)))

# factorial

F = lambda f: lambda n: IS_ZERO(n)(ONE)(lambda x: MULT(n)(f(PRED(n)))(x))

FACT = FIX(F)

FACT = FIX(lambda r: lambda n: \
    IS_ZERO(n) \
        (ONE) \
        (lambda x: MULT(n)(r(PRED(n)))(x)))

AND_EQUALS_TWO = COMPOSE(AND)(EQUALS(TWO))

ALL_TWOS = FOLD(AND_EQUALS_TWO)(TRUE)

FACT_CHECK = ALL_TWOS( \
    LIST_ELEMENT( \
        FACT(TWO) \
    )(LIST_ELEMENT( \
        FIX(F)(TWO) \
    )(LIST_ELEMENT( \
        (lambda r: (lambda x: r(lambda y: x(x)(y)))(lambda x: r(lambda y: x(x)(y))))(F)(TWO) \
    )(LIST_ELEMENT( \
        (lambda x: F(lambda y: x(x)(y)))(lambda x: F(lambda y: x(x)(y)))(TWO) \
    )(LIST_ELEMENT( \
        F(lambda y: (lambda x: F(lambda y: x(x)(y)))(lambda x: F(lambda y: x(x)(y)))(y))(TWO) \
    )(LIST_ELEMENT( \
        F(FIX(F))(TWO) \
    )(LIST_ELEMENT( \
        (lambda f: lambda n: IS_ZERO(n)(ONE)(lambda x: MULT(n)(f(PRED(n)))(x)))(FIX(F))(TWO) \
    )(LIST_ELEMENT( \
        (lambda n: IS_ZERO(n)(ONE)(lambda x: MULT(n)(FIX(F)(PRED(n)))(x)))(TWO) \
    )(LIST_ELEMENT( \
        IS_ZERO(TWO)(ONE)(lambda x: MULT(TWO)(FIX(F)(PRED(TWO)))(x)) \
    )(LIST_ELEMENT( \
        lambda x: MULT(TWO)(FIX(F)(PRED(TWO)))(x) \
    )(LIST_ELEMENT( \
        lambda x: MULT(TWO)(FIX(F)(ONE))(x) \
    )(LIST_ELEMENT( \
        lambda x: MULT(TWO)(FACT(ONE))(x) \
    )(LIST_ELEMENT( \
        lambda x: MULT(TWO)(ONE)(x) \
    )(LIST_ELEMENT( \
        MULT(TWO)(ONE) \
    )(LIST_ELEMENT( \
        TWO \
    )(EMPTY_LIST)))))))))))))))
)

FACT_EXP = (lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda f: lambda n: (lambda n: n(lambda x: lambda x: lambda y: y)(lambda x: lambda y: x))(n)(lambda f: lambda x: f(x))(lambda x: (lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(n)(f((lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n)))(x)))

# fibonacci

FIB = FIX(lambda r: lambda n: \
    IS_ZERO(n) \
        (ZERO) \
        (IF_THEN_ELSE(EQUALS(n)(ONE)) \
            (ONE) \
            (lambda x: PLUS(r(MINUS(n)(ONE)))(r(MINUS(n)(TWO)))(x))))

FIB_EXP = (lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda f: lambda n: (lambda n: n(lambda x: (lambda x: lambda y: y))(lambda x: lambda y: x))(n)(lambda f: lambda x: x)((lambda x: x)((lambda n: lambda m: (lambda x: lambda y: x(y)(lambda x: lambda y: y))((lambda n: lambda m: (lambda n: n(lambda x: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda n: lambda m: m(lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n))(n)(m)))(n)(m))((lambda n: lambda m: (lambda n: n(lambda x: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda n: lambda m: m(lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n))(n)(m)))(m)(n)))(n)(lambda f: lambda x: f(x)))(lambda f: lambda x: f(x))(lambda x: (lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(f((lambda n: lambda m: m(lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n))(n)(lambda f: lambda x: f(x))))(f((lambda n: lambda m: m(lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n))(n)(lambda f: lambda x: f(f(x)))))(x))))

# FizzBuzz

FIFTEEN = PLUS(TEN)(FIVE)

TWENTY = PLUS(TEN)(TEN)

HUNDRED = MULT(TEN)(TEN)

F = MULT(TEN)(SEVEN)

I = PLUS(HUNDRED)(FIVE)

Z = PLUS(HUNDRED)(PLUS(TWENTY)(TWO))

B = PLUS(MULT(TEN)(SIX))(SIX)

U = PLUS(HUNDRED)(PLUS(TEN)(SEVEN))

FIZZ = LIST_ELEMENT(F) \
      (LIST_ELEMENT(I) \
      (LIST_ELEMENT(Z) \
      (LIST_ELEMENT(Z) \
      (EMPTY_LIST))))

BUZZ = LIST_ELEMENT(B) \
      (LIST_ELEMENT(U) \
      (LIST_ELEMENT(Z) \
      (LIST_ELEMENT(Z) \
      (EMPTY_LIST))))

FIZZBUZZ = LIST_ELEMENT(F) \
          (LIST_ELEMENT(I) \
          (LIST_ELEMENT(Z) \
          (LIST_ELEMENT(Z) \
          (BUZZ))))

FIZZBUZZFUNC = MAP(lambda n: \
    IF_THEN_ELSE(IS_ZERO(MOD(n)(FIFTEEN))) \
        (FIZZBUZZ) \
        (IF_THEN_ELSE(IS_ZERO(MOD(n)(THREE))) \
            (FIZZ) \
            (IF_THEN_ELSE(IS_ZERO(MOD(n)(FIVE))) \
                (BUZZ) \
                (n))))

FIZZBUZZFUNC_EXP = (lambda f: ((lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda r: lambda f: lambda z: lambda xs: (lambda p: lambda x: lambda y: p(x)(y))((lambda p: p(lambda x: lambda y: x))(xs))(z)(lambda x: f((lambda xs: (lambda p: p(lambda x: lambda y: x))((lambda p: p(lambda x: lambda y: y))(xs)))(xs))(r(f)(z)((lambda xs: (lambda p: p(lambda x: lambda y: y))((lambda p: p(lambda x: lambda y: y))(xs)))(xs)))(x))))(lambda x: lambda xs: (lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))(f(x))(xs))((lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: x)(lambda x: lambda y: x)))(lambda n: (lambda p: lambda x: lambda y: p(x)(y))((lambda n: n(lambda m: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda r: lambda n: lambda m: (lambda p: lambda x: lambda y: p(x)(y))((lambda n: lambda m: (lambda n: n(lambda m: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda n: lambda m: m(lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n))(n)(m)))(m)(n))(lambda x: r((lambda n: lambda m: m((lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y)))(n))(n)(m))(m)(x))(n))(n)((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(x)))))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(x)))))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(f(f(f(x)))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))(((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(x))))))))(lambda f: lambda x: f(f(f(f(f(f(x))))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))(U)((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))((lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: x)(lambda x: lambda y: x)))))))))))((lambda p: lambda x: lambda y: p(x)(y))((lambda n: n(lambda m: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda r: lambda n: lambda m: (lambda p: lambda x: lambda y: p(x)(y))((lambda n: lambda m: (lambda n: n(lambda m: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda n: lambda m: m(lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n))(n)(m)))(m)(n))(lambda x: r((lambda n: lambda m: m((lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y)))(n))(n)(m))(m)(x))(n))(n)(lambda f: lambda x: f(f(f(x))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(x)))))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(f(f(f(x)))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))((lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: x)(lambda x: lambda y: x))))))((lambda p: lambda x: lambda y: p(x)(y))((lambda n: n(lambda m: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y))))(lambda r: lambda n: lambda m: (lambda p: lambda x: lambda y: p(x)(y))((lambda n: lambda m: (lambda n: n(lambda m: (lambda x: lambda y: y))(lambda x: lambda y: x))((lambda n: lambda m: m(lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y))(n))(n)(m)))(m)(n))(lambda x: r((lambda n: lambda m: m((lambda n: n(lambda p: lambda z: z((lambda n: lambda f: lambda x: f(n(f)(x)))(p(lambda x: lambda y: x)))(p(lambda x: lambda y: x)))(lambda z: z(lambda f: lambda x: x)(lambda f: lambda x: x))(lambda x: lambda y: y)))(n))(n)(m))(m)(x))(n))(n)(lambda f: lambda x: f(f(f(f(f(x))))))))(((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(x))))))))(lambda f: lambda x: f(f(f(f(f(f(x))))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(x))))))))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))((lambda x: lambda xs: (lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: y)((lambda x: lambda y: lambda p: p(x)(y))(x)(xs)))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(n))(lambda f: lambda x: x))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))((lambda n: lambda m: m(lambda n: lambda f: lambda x: f(n(f)(x)))(n))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x)))))))))))(lambda f: lambda x: f(f(f(f(f(f(f(f(f(f(x))))))))))))(lambda f: lambda x: f(f(x)))))((lambda x: lambda y: lambda p: p(x)(y))(lambda x: lambda y: x)(lambda x: lambda y: x)))))))(n))))

# utility functions

to_bool = lambda b: IF_THEN_ELSE(b)(True)(False)

from_bool = lambda b: TRUE if b is True else FALSE

to_int = lambda n: n(lambda x: x + 1)(0)

from_int = lambda n: (lambda f: lambda x: x) if n == 0 else lambda f: lambda x: f(from_int(n - 1)(f)(x))

to_list = lambda xs: [] if to_bool(IS_EMPTY(xs)) else [] + [HEAD(xs)] + to_list(TAIL(xs))

from_list = lambda xs: EMPTY_LIST if len(xs) == 0 else LIST_ELEMENT(xs[0:1])(from_list(xs[1:]))

to_list_int = lambda xs: [] if to_bool(IS_EMPTY(xs)) else [] + [to_int(HEAD(xs))] + to_list_int(TAIL(xs))

from_list_int = lambda xs: EMPTY_LIST if len(xs) == 0 else LIST_ELEMENT(from_int(xs[0:1][0]))(from_list_int(xs[1:]))

to_pair = lambda p: {'fst': FIRST(p), 'snd': SECOND(p)}

to_pair_int = lambda p: {'fst': to_int(FIRST(p)), 'snd': to_int(SECOND(p))}

to_string = lambda str: "".join(map(lambda n: chr(n), to_list_int(str)))

from_string = lambda str: EMPTY_LIST if len(str) == 0 else LIST_ELEMENT(from_int(ord(str[0])))(from_string(str[1:]))

to_fizzbuzz = lambda fb: list(map(lambda x: to_int(x) if to_string(x) == "" else to_string(x), to_list(fb)))

# test_fizzbuzz = to_fizzbuzz(FIZZBUZZFUNC(RANGE(ONE)(FIFTEEN))) == [1,2,"Fizz",4,"Buzz","Fizz",7,8,"Fizz","Buzz",11,"Fizz",13,14,"FizzBuzz"]


class Testing(unittest.TestCase):
    p = PAIR(ONE)(TWO)
    l = RANGE(ONE)(THREE)
    
    def test_combinators(self):
        self.assertEqual(ID(1), 1)
        self.assertEqual(COMPOSE(ID)(ID)(1), ID(ID(1)))
        
    def test_booleans(self):
        self.assertEqual(TRUE(1)(0), 1)
        self.assertEqual(FALSE(1)(0), 0)
        self.assertEqual(to_bool(AND(FALSE)(TRUE)), False)
        self.assertEqual(to_bool(OR(FALSE)(TRUE)), True)
        self.assertEqual(to_bool(NOT(TRUE)), False)
        self.assertEqual(to_bool(XOR(TRUE)(TRUE)), False)
        self.assertEqual(to_bool(IF_THEN_ELSE(IS_ZERO(ZERO))(TRUE)(FALSE)), True)
        
    def test_numeric(self):
        self.assertEqual(to_int(ZERO), 0)
        self.assertEqual(to_int(ONE), 1)
        self.assertEqual(to_int(TWO), 2)
        self.assertEqual(to_int(THREE), 3)
        self.assertEqual(to_int(SUCC(ONE)), 2)
        self.assertEqual(to_int(PRED(ONE)), 0)
        self.assertEqual(to_int(PLUS(TWO)(TWO)), 4)
        self.assertEqual(to_int(MINUS(TWO)(ONE)), 1)
        self.assertEqual(to_int(MULT(TWO)(THREE)), 6)
        self.assertEqual(to_int(EXP(TWO)(THREE)), 8)
        
    def test_bool_functions(self):
        self.assertEqual(to_bool(IS_ZERO(ZERO)), True)
        self.assertEqual(to_bool(IS_ZERO(THREE)), False)
        self.assertEqual(to_bool(LESS_THAN_OR_EQUAL(ZERO)(ZERO)), True)
        self.assertEqual(to_bool(LESS_THAN_OR_EQUAL(ONE)(ZERO)), False)
        self.assertEqual(to_bool(LESS_THAN(ZERO)(ONE)), True)
        self.assertEqual(to_bool(LESS_THAN(ZERO)(ZERO)), False)
        self.assertEqual(to_bool(EQUALS(ONE)(ONE)), True)
        self.assertEqual(to_bool(GREATER_THAN(ZERO)(ZERO)), False)
        self.assertEqual(to_bool(GREATER_THAN(ONE)(ZERO)), True)
        self.assertEqual(to_bool(GREATER_THAN_OR_EQUAL(ZERO)(ZERO)), True)
        self.assertEqual(to_bool(GREATER_THAN_OR_EQUAL(ONE)(ZERO)), True)
        self.assertEqual(to_bool(GREATER_THAN_OR_EQUAL(ZERO)(ONE)), False)
        self.assertEqual(to_bool(EVEN(TWO)), True)
        self.assertEqual(to_bool(ODD(ONE)), True)
        self.assertEqual(to_bool(ODD(TWO)), False)
        
    def test_numeric_functions(self):
        self.assertEqual(to_int(MAX(ONE)(TWO)), 2)
        self.assertEqual(to_int(MIN(ONE)(TWO)), 1)
        self.assertEqual(to_int(MOD(FIVE)(TWO)), 1)
        self.assertEqual(to_int(DIV(FOUR)(TWO)), 2)
        
    def test_data_structures(self):
        self.assertEqual(to_int(FIRST(Testing.p)), 1)
        self.assertEqual(to_int(SECOND(Testing.p)), 2)
        self.assertEqual(to_bool(AND(FIRST(EMPTY_LIST))(SECOND(EMPTY_LIST))), True)
        self.assertEqual(to_bool(AND(IS_EMPTY(EMPTY_LIST))(NOT(IS_EMPTY(Testing.l)))), True)
        self.assertEqual(to_int(HEAD(Testing.l)), 1)
        self.assertEqual(to_list_int(TAIL(Testing.l)), [2, 3])
        self.assertEqual(to_int(FOLD(PLUS)(ZERO)(Testing.l)), 6)
        self.assertEqual(to_list_int(MAP(PLUS(ONE))(Testing.l)), [2, 3, 4])
        self.assertEqual(to_int(HEAD(FILTER(EVEN)(Testing.l))), 2)
        self.assertEqual(to_list_int(Testing.l), [1, 2, 3])
        self.assertEqual(to_int(INDEX(Testing.l)(ZERO)), 1)
        self.assertEqual(to_list_int(PUSH(FOUR)(Testing.l)), [1, 2, 3, 4])
        self.assertEqual(to_list_int(APPEND(Testing.l)(Testing.l)), [1, 2, 3, 1, 2, 3])
        self.assertEqual(to_int(LENGTH(Testing.l)), 3)
        self.assertEqual(to_list_int(REVERSE(Testing.l)), [3, 2, 1])
        self.assertEqual(to_list_int(TAKE(TWO)(Testing.l)), [1, 2])
        self.assertEqual(list(map(lambda x: to_pair_int(x), to_list(ZIP(Testing.l)(Testing.l)))), [{'fst': 1, 'snd': 1}, {'fst': 2, 'snd': 2}, {'fst': 3, 'snd': 3}])
        self.assertEqual(to_list_int(ZIP_WITH(PLUS)(Testing.l)(REVERSE(Testing.l))), [4, 4, 4])
        self.assertEqual(to_list_int(INSERT(ZERO)(Testing.l)), [0, 1, 2, 3])
        self.assertEqual(to_list_int(SORT(REVERSE(Testing.l))), to_list_int(Testing.l))
        self.assertEqual(to_list_int(TAKE(THREE)(ZEROS)), [0, 0, 0])
        self.assertEqual(to_list_int(TAKE(THREE)(REPEAT(ONE))), [1, 1, 1])
    def test_higher_order(self):
        self.assertEqual(0, 0) # not implemented as of yet, SUM, FOLDS, etc.
    
    def test_applicative(self):
        self.assertEqual(to_list_int(PURE(ONE))[0], 1)
        self.assertEqual(to_list_int(AP(MAP(PLUS)(Testing.l))(Testing.l)), [2, 3, 4, 3, 4, 5, 4, 5, 6])
        self.assertEqual(to_list_int(AP_ZIP_LIST(MAP(PLUS)(Testing.l))(REVERSE(Testing.l))), [4, 4, 4])
#         self.assertEqual(to_list_int(BIND(Testing.l)(RETURN(lambda x : RETURN(PLUS(x)(ONE))))), [2, 3, 4])
        
    def test_factorial(self):
        self.assertEqual(to_int(FACT(THREE)), 6)
        self.assertEqual(to_int(FACT_EXP(THREE)), 6)
#         self.assertEqual(to_bool(FACT_CHECK), True)

    def test_fibonacci(self):
        self.assertEqual(to_int(FIB(SIX)), 8)
        self.assertEqual(to_int(FIB_EXP(SIX)), 8)
        
    def test_fizzbuzz(self):
        self.assertEqual(to_fizzbuzz(FIZZBUZZFUNC(RANGE(ONE)(FIFTEEN))), [1,2,"Fizz",4,"Buzz","Fizz",7,8,"Fizz","Buzz",11,"Fizz",13,14,"FizzBuzz"])
        self.assertEqual(to_fizzbuzz(FIZZBUZZFUNC_EXP(RANGE(ONE)(FIFTEEN))), [1,2,"Fizz",4,"Buzz","Fizz",7,8,"Fizz","Buzz",11,"Fizz",13,14,"FizzBuzz"])

unittest.main(argv=['first-arg-is-ignored'], exit=False)
