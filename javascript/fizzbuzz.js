// malc - make a lambda calculus
// JavaScript ES2015
// Steven Syrek

// FizzBuzz
// with warm regards to Tom Stuart, Understanding Computation

ZERO = f => x => x

ONE = f => x => f(x)

TWO = f => x => f(f(x))

THREE = f => x => f(f(f(x)))

FOUR = f => x => f(f(f(f(x))))

FIVE = f => x => f(f(f(f(f(x)))))

SIX = f => x => f(f(f(f(f(f(x))))))

SEVEN = f => x => f(f(f(f(f(f(f(x)))))))

EIGHT = f => x => f(f(f(f(f(f(f(f(x))))))))

NINE = f => x => f(f(f(f(f(f(f(f(f(x)))))))))

TEN = f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))

TRUE = x => y => x

FALSE = x => y => y

IF_THEN_ELSE = p => x => y => p(x)(y)

SUCC = n => f => x => f(n(f)(x))

PRED = n => n(p => z => z(SUCC(p(TRUE)))(p(TRUE)))(z => z(ZERO)(ZERO))(FALSE)

PLUS = n => m => m(SUCC)(n)

MINUS = n => m => m(PRED)(n)

MULT = n => m => m(PLUS(n))(ZERO)

FIX = f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y)))

IS_ZERO = n => n(m => FALSE)(TRUE)

LESS_THAN_OR_EQUAL = n => m => IS_ZERO(MINUS(n)(m))

MOD = FIX(Y => n => m =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => Y(MINUS(n)(m))(m)(x))
    (n))

FIFTEEN = PLUS(TEN)(FIVE)

TWENTY = PLUS(TEN)(TEN)

HUNDRED = MULT(TEN)(TEN)

F = MULT(TEN)(SEVEN)

I = PLUS(HUNDRED)(FIVE)

Z = PLUS(HUNDRED)(PLUS(TWENTY)(TWO))

B = PLUS(MULT(TEN)(SIX))(SIX)

U = PLUS(HUNDRED)(PLUS(TEN)(SEVEN))

PAIR = x => y => p => p(x)(y)

FIRST = p => p(x => y => x)

SECOND = p => p(x => y => y)

LIST_ELEMENT = x => xs => PAIR(FALSE)(PAIR(x)(xs))

EMPTY_LIST = PAIR(TRUE)(TRUE)

IS_EMPTY = FIRST

HEAD = xs => FIRST(SECOND(xs))

TAIL = xs => SECOND(SECOND(xs))

RANGE = FIX(Y => m => n =>
  IF_THEN_ELSE(LESS_THAN_OR_EQUAL(m)(n))
    (x => LIST_ELEMENT(m)(Y(SUCC(m))(n))(x))
    (EMPTY_LIST))

FIZZ = LIST_ELEMENT(F)
       (LIST_ELEMENT(I)
       (LIST_ELEMENT(Z)
       (LIST_ELEMENT(Z)
       (EMPTY_LIST))))

BUZZ = LIST_ELEMENT(B)
       (LIST_ELEMENT(U)
       (LIST_ELEMENT(Z)
       (LIST_ELEMENT(Z)
       (EMPTY_LIST))))

FIZZBUZZ = LIST_ELEMENT(F)
          (LIST_ELEMENT(I)
          (LIST_ELEMENT(Z)
          (LIST_ELEMENT(Z)
          (BUZZ))))

FOLD = FIX(Y => f => z => xs =>
  IF_THEN_ELSE(IS_EMPTY(xs))
    (z)
    (x => f(HEAD(xs))(Y(f)(z)(TAIL(xs)))(x)))

MAP = f => FOLD(x => xs => LIST_ELEMENT(f(x))(xs))(EMPTY_LIST)

FIZZBUZZFUNC = MAP(n =>
  IF_THEN_ELSE(IS_ZERO(MOD(n)(FIFTEEN)))
    (FIZZBUZZ)
    (IF_THEN_ELSE(IS_ZERO(MOD(n)(THREE)))
      (FIZZ)
      (IF_THEN_ELSE(IS_ZERO(MOD(n)(FIVE)))
        (BUZZ)
        (n))))

FIZZBUZZFUNC_EXP = (f => ((f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(Y => f => z => xs => (p => x => y => p(x)(y))(((p => p(x => y => x)))(xs)) (z) (x => f((xs => (p => p(x => y => x))((p => p(x => y => y))(xs)))(xs))(Y(f)(z)((xs => (p => p(x => y => y))((p => p(x => y => y))(xs)))(xs)))(x))))(x => xs => (x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(f(x))(xs))(((x => y => p => p(x)(y))((x => y => x))((x => y => x)))))(n => (p => x => y => p(x)(y))((n => n(m => (x => y => y))((x => y => x)))(((f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(Y => n => m => (p => x => y => p(x)(y))((n => m => (n => n(m => (x => y => y))((x => y => x)))((n => m => m((n => n(p => z => z((n => f => x => f(n(f)(x)))(p((x => y => x))))(p((x => y => x))))(z => z((f => x => x))((f => x => x)))((x => y => y))))(n))(n)(m)))(m)(n)) (x => Y((n => m => m((n => n(p => z => z((n => f => x => f(n(f)(x)))(p((x => y => x))))(p((x => y => x))))(z => z((f => x => x))((f => x => x)))((x => y => y))))(n))(n)(m))(m)(x)) (n)))(n)(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(x))))))))))) (((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(x))))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(x))))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) (((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(x)))))))))((f => x => f(f(f(f(f(f(x)))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(x)))))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) (((x => y => p => p(x)(y))((x => y => x))((x => y => x)))))))))))))) ((p => x => y => p(x)(y))((n => n(m => (x => y => y))((x => y => x)))(((f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(Y => n => m => (p => x => y => p(x)(y))((n => m => (n => n(m => (x => y => y))((x => y => x)))((n => m => m((n => n(p => z => z((n => f => x => f(n(f)(x)))(p((x => y => x))))(p((x => y => x))))(z => z((f => x => x))((f => x => x)))((x => y => y))))(n))(n)(m)))(m)(n)) (x => Y((n => m => m((n => n(p => z => z((n => f => x => f(n(f)(x)))(p((x => y => x))))(p((x => y => x))))(z => z((f => x => x))((f => x => x)))((x => y => y))))(n))(n)(m))(m)(x)) (n)))(n)((f => x => f(f(f(x))))))) (((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(x))))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(x))))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) (((x => y => p => p(x)(y))((x => y => x))((x => y => x))))))))) ((p => x => y => p(x)(y))((n => n(m => (x => y => y))((x => y => x)))(((f => (x => f(y => x(x)(y)))(x => f(y => x(x)(y))))(Y => n => m => (p => x => y => p(x)(y))((n => m => (n => n(m => (x => y => y))((x => y => x)))((n => m => m((n => n(p => z => z((n => f => x => f(n(f)(x)))(p((x => y => x))))(p((x => y => x))))(z => z((f => x => x))((f => x => x)))((x => y => y))))(n))(n)(m)))(m)(n)) (x => Y((n => m => m((n => n(p => z => z((n => f => x => f(n(f)(x)))(p((x => y => x))))(p((x => y => x))))(z => z((f => x => x))((f => x => x)))((x => y => y))))(n))(n)(m))(m)(x)) (n)))(n)((f => x => f(f(f(f(f(x))))))))) (((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(x)))))))))((f => x => f(f(f(f(f(f(x)))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(x)))))))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) ((x => xs => (x => y => p => p(x)(y))((x => y => y))((x => y => p => p(x)(y))(x)(xs)))(((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => m => m((n => f => x => f(n(f)(x))))(n))(n))((f => x => x)))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((n => m => m((n => f => x => f(n(f)(x))))(n))(((n => m => m((n => f => x => f(n(f)(x))))(n))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))((f => x => f(f(f(f(f(f(f(f(f(f(x))))))))))))))((f => x => f(f(x))))))) (((x => y => p => p(x)(y))((x => y => x))((x => y => x))))))))) (n))))

toBool = b => IF_THEN_ELSE(b)(true)(false)

toInt = n => n(x => x + 1)(0)

toArray = xs => [].concat(toBool(IS_EMPTY(xs)) ? [] : [HEAD(xs)].concat(toArray(TAIL(xs))))

toArrayInt = xs => [].concat(toBool(IS_EMPTY(xs)) ? [] : [toInt(HEAD(xs))].concat(toArrayInt(TAIL(xs))))

toString = str => toArrayInt(str).map(n => String.fromCharCode(n)).join("")

toFizzBuzz = fb => toArray(fb).map(x => toString(x) === "" ? toInt(x) : toString(x))

testFizzBuzz = () => (toFizzBuzz(FIZZBUZZFUNC(RANGE(ONE)(FIFTEEN))).every((e,i) => e === [1,2,"Fizz",4,"Buzz","Fizz",7,8,"Fizz","Buzz",11,"Fizz",13,14,"FizzBuzz"][i]))