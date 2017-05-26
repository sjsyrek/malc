// malc - make a lambda calculus
// JavaScript ES2015
// Steven Syrek

// identity combinator

ID = x => x

// boolean primitives

TRUE = x => y => x

FALSE = x => y => y

// boolean combinators

AND = x => y => x(y)(FALSE)

OR = x => y => x(TRUE)(y)

NOT = x => x(FALSE)(TRUE)

XOR = x => y => AND(OR(x)(y))(NOT(AND(x)(y)))

// branching

IF_THEN_ELSE = p => x => y => p(x)(y) // IF_THEN_ELSE = ID

// natural numbers

ZERO = f => x => x

ONE = f => x => f(x)

TWO = f => x => f(f(x))

THREE = f => x => f(f(f(x)))

// enumeration

SUCC = n => f => x => f(n(f)(x))

PRED = n => n(p => z => z(SUCC(p(TRUE)))(p(TRUE)))(z => z(ZERO)(ZERO))(FALSE)

// basic arithmetic

PLUS = n => m => m(SUCC)(n)

MINUS = n => m => m(PRED)(n)

MULT = n => m => m(PLUS(n))(ZERO)

EXP = n => m => m(n)

// more numbers

FOUR = SUCC(THREE)

FIVE = PLUS(TWO)(THREE)

SIX = MULT(TWO)(THREE)

SEVEN = SUCC(SUCC(SUCC(SUCC(SUCC(SUCC(ONE))))))

EIGHT = PRED(MULT(THREE)(THREE))

NINE = EXP(THREE)(TWO)

TEN = MINUS(PLUS(EIGHT)(THREE))(ONE)

// comparison

IS_ZERO = n => n(m => FALSE)(TRUE)

LESS_THAN_OR_EQUAL = n => m => IS_ZERO(MINUS(n)(m))

LESS_THAN = n => m => AND(LESS_THAN_OR_EQUAL(n)(m))
                         (NOT(IS_ZERO(n(PRED)(m))))

EQUALS = n => m => AND(LESS_THAN_OR_EQUAL(n)(m))
                      (LESS_THAN_OR_EQUAL(m)(n))

GREATER_THAN_OR_EQUAL = n => m => IS_ZERO(n(PRED)(m))

GREATER_THAN = n => m => AND(GREATER_THAN_OR_EQUAL(n)(m))
                            (NOT(IS_ZERO(MINUS(n)(m))))

MAX = x => y =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(x)(y))
    (y)
    (x)

MIN = x => y =>
  IF_THEN_ELSE(EQUALS(MAX(x)(y))(x))
    (y)
    (x)

// function composition

COMPOSE = f => g => x => f(g(x))

// recursion

FIX = f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y)))

// advanced arithmetic

MOD = FIX(r => n => m =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => r(MINUS(n)(m))(m)(x))
    (n))

DIV = FIX(r => n => m =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => SUCC(r(MINUS(n)(m))(m))(x))
    (ZERO))

// other combinators

EVEN = n => IS_ZERO(MOD(n)(TWO))

ODD = COMPOSE(NOT)(EVEN)

// pairs

PAIR = x => y => p => p(x)(y)

FIRST = p => p(x => y => x)

SECOND = p => p(x => y => y)

// lists

LIST_ELEMENT = x => xs => PAIR(FALSE)(PAIR(x)(xs))

EMPTY_LIST = PAIR(TRUE)(TRUE)

IS_EMPTY = FIRST

HEAD = xs => FIRST(SECOND(xs))

TAIL = xs => SECOND(SECOND(xs))

// fold/map/filter

FOLD = FIX(r => f => z => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (z)
    (x => f(HEAD(xs))(r(f)(z)(TAIL(xs)))(x)))

MAP = f => FOLD(x => xs => LIST_ELEMENT(f(x))(xs))(EMPTY_LIST)

FILTER = p => FOLD(x => xs =>
  IF_THEN_ELSE(p(x))
    (LIST_ELEMENT(x)(xs))
    (xs))
  (EMPTY_LIST)

// other list functions

RANGE = FIX(r => m => n =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => LIST_ELEMENT(m)(r(SUCC(m))(n))(x))
    (EMPTY_LIST))

INDEX = FIX(r => xs => n =>
  IF_THEN_ELSE(IS_ZERO(n))
    (HEAD(xs))
    (x => r(TAIL(xs))(PRED(n))(x)))

PUSH = x => xs => FOLD(LIST_ELEMENT)(LIST_ELEMENT(x)(EMPTY_LIST))(xs)

APPEND = FIX(r => xs => ys =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (ys)
    (x => LIST_ELEMENT(HEAD(xs))(r(TAIL(xs))(ys))(x)))

LENGTH = xs => (FIX(r => xs => n =>
	IF_THEN_ELSE(IS_EMPTY(xs))
	  (n)
	  (x => r(TAIL(xs))(SUCC(n))(x))))
	  (xs)(ZERO)

REVERSE = xs => (FIX(r => xs => a =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (a)
    (x => (r(TAIL(xs))(LIST_ELEMENT(HEAD(xs))(a)))(x))))
  (xs)(EMPTY_LIST)

TAKE = FIX(r => n => xs =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(n)(ZERO))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(xs)))
      (EMPTY_LIST)
      (x => LIST_ELEMENT(HEAD(xs))(r(MINUS(n)(ONE))(TAIL(xs)))(x)))

ZIP = FIX(r => xs => ys =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(ys))
      (EMPTY_LIST)
      (x => LIST_ELEMENT(PAIR(HEAD(xs))(HEAD(ys)))(r(TAIL(xs))(TAIL(ys)))(x))))

ZIP_WITH = FIX(r => f => xs => ys =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(ys))
      (EMPTY_LIST)
      (x => LIST_ELEMENT(f(HEAD(xs))(HEAD(ys)))(r(f)(TAIL(xs))(TAIL(ys)))(x))))

INSERT = FIX(r => n => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (LIST_ELEMENT(n)(EMPTY_LIST))
    (IF_THEN_ELSE(GREATER_THAN(n)(HEAD(xs)))
      (x => LIST_ELEMENT(HEAD(xs))(r(n)(TAIL(xs)))(x))
      (LIST_ELEMENT(n)(xs))))

SORT = FOLD(INSERT)(EMPTY_LIST)

// streams

ZEROS = FIX(r => LIST_ELEMENT(ZERO)(r))

REPEAT = x => FIX(r => LIST_ELEMENT(x)(r))

// functional structures (list implementations)

// monoid

MEMPTY = EMPTY_LIST

MAPPEND = APPEND

// functor

FMAP = MAP

// applicative

PURE = x => LIST_ELEMENT(x)(EMPTY_LIST)

AP = FIX(r => fs => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(fs))(EMPTY_LIST)
      (x => MAPPEND(MAP(HEAD(fs))(xs))(r(TAIL(fs))(xs))(x))))

AP_ZIP_LIST = fs => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (IF_THEN_ELSE(IS_EMPTY(fs))(EMPTY_LIST)
      (ZIP_WITH(ID)(fs)(xs)))

// monad

RETURN = PURE

BIND = FIX(r => xs => f =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (EMPTY_LIST)
    (x => MAPPEND(f(HEAD(xs)))(r(TAIL(xs))(f))(x)))

// factorial

F = f => n => IS_ZERO(n)(ONE)(x => MULT(n)(f(PRED(n)))(x))

FACT = FIX(F)

FACT = FIX(r => n =>
  IS_ZERO(n)
    (ONE)
    (x => MULT(n)(r(PRED(n)))(x)))

AND_EQUALS_TWO = COMPOSE(AND)(EQUALS(TWO))

ALL_TWOS = FOLD(AND_EQUALS_TWO)(TRUE)

FACT_CHECK = ALL_TWOS(
  LIST_ELEMENT(
    FACT(TWO)
  )(LIST_ELEMENT(
    FIX(F)(TWO)
  )(LIST_ELEMENT(
    (r => (x => r(y => x(x)(y)))(x => r(y => x(x)(y))))(F)(TWO)
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

FACT_EXP = (f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(f => n => (n => n(x => x => y => y)(x => y => x))(n)(f => x => f(x))(x => (n => m => m((n => m => m(n => f => x => f(n(f)(x)))(n))(n))(f => x => x))(n)(f((n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n)))(x)))

// fibonacci

FIB = FIX(r => n =>
  IS_ZERO(n)
    (ZERO)
    (IF_THEN_ELSE(EQUALS(n)(ONE))
      (ONE)
      (x => PLUS(r(MINUS(n)(ONE)))(r(MINUS(n)(TWO)))(x))))

FIB_EXP = (f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(f => n => (n => n(x => (x => y => y))(x => y => x))(n)(f => x => x)((x => x)((n => m => (x => y => x(y)(x => y => y))((n => m => (n => n(x => (x => y => y))(x => y => x))((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(m)))(n)(m))((n => m => (n => n(x => (x => y => y))(x => y => x))((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(m)))(m)(n)))(n)(f => x => f(x)))(f => x => f(x))(x => (n => m => m(n => f => x => f(n(f)(x)))(n))(f((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(f => x => f(x))))(f((n => m => m(n => n(p => z => z((n => f => x => f(n(f)(x)))(p(x => y => x)))(p(x => y => x)))(z => z(f => x => x)(f => x => x))(x => y => y))(n))(n)(f => x => f(f(x)))))(x))))

// utility functions

toBool = b => IF_THEN_ELSE(b)(true)(false)

fromBool = b => b ? TRUE : FALSE

toInt = n => n(x => x + 1)(0)

fromInt = n => n == 0 ? f => x => x : f => x => f(fromInt(n - 1)(f)(x))

toArray = xs => [].concat(toBool(IS_EMPTY(xs)) ? [] : [HEAD(xs)].concat(toArray(TAIL(xs))))

fromArray = xs => xs.length === 0 ? EMPTY_LIST : LIST_ELEMENT(xs[0])(fromArray(xs.slice(1)))

toArrayInt = xs => [].concat(toBool(IS_EMPTY(xs)) ? [] : [toInt(HEAD(xs))].concat(toArrayInt(TAIL(xs))))

fromArrayInt = xs => xs.length === 0 ? EMPTY_LIST : LIST_ELEMENT(fromInt(xs[0]))(fromArrayInt(xs.slice(1)))

toPair = p => {
  return {fst: FIRST(p), snd: SECOND(p)}
}

toPairInt = p => {
  return {fst: (toInt(FIRST(p))), snd: (toInt(SECOND(p)))}
}

toString = str => toArrayInt(str).map(n => String.fromCharCode(n)).join("")

fromString = str => str.length === 0 ? EMPTY_LIST : LIST_ELEMENT(fromInt(str.charCodeAt(str[0])))(fromString(str.substr(1)))

toFizzBuzz = fb => toArray(fb).map(x => toString(x) === "" ? toInt(x) : toString(x))

toLambda = x => {
  if (Number.isInteger(x)) return fromInt(x)
  if (typeof x === "boolean") return fromBool(x)
  if (typeof x === 'string') return fromString(x)
  if (Array.isArray(x)) return fromArray(x.map(y => toLambda(y)))
  return x
}

// tests

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
console.log(allTests() ? "All tests passed." : "Tests failed.")