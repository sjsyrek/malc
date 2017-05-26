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

XOR = lambda x: lambda y: AND(OR(x)(y))(NOT(AND(x)(y)))


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

# factorial

FACT = FIX(lambda r: lambda n:
  IS_ZERO(n)
    (ONE)
    (lambda x: MULT(n)(r(PRED(n)))(x)))

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