# malc - make a lambda calculus
# Perl 6
# Steven Syrek

# identity combinator

my $ID = -> $x { $x }

# boolean primitives

my $TRUE = -> $x { -> $y { $x } }

my $FALSE = -> $x { -> $y { $y } }

# boolean combinators

my $AND = -> $x { -> $y { $x($y)($FALSE) } }

my $OR = -> $x { -> $y { $x($TRUE)($y) } }

my $NOT = -> $x { $x($FALSE)($TRUE) }

my $XOR = -> $x { -> $y { $AND($OR($x)($y))($NOT($AND($x)($y))) } }

# branching

my $IF_THEN_ELSE = -> $p { -> $x { -> $y { $p($x)($y) } } } # $IF_THEN_ELSE = $ID

# natural numbers

my $ZERO = -> $f { -> $x { $x } }

my $ONE = -> $f { -> $x { $f($x) } }

my $TWO = -> $f { -> $x { $f($f($x)) } }

my $THREE = -> $f { -> $x { $f($f($f($x))) } }

# enumeration

my $SUCC = -> $n { -> $f { -> $x { $f($n($f)($x)) } } }

my $PRED = -> $n { $n(-> $p { -> $z { $z($SUCC($p($TRUE)))($p($TRUE)) } })(-> $z { $z($ZERO)($ZERO) })($FALSE) }

# basic arithmetic

my $PLUS = -> $n { -> $m { $m($SUCC)($n) } }

my $MINUS = -> $n { -> $m { $m($PRED)($n) } }

my $MULT = -> $n { -> $m { $m($PLUS($n))($ZERO) } }

my $EXP = -> $n { -> $m { $m($n) } }

# more numbers

my $FOUR = $SUCC($THREE);

my $FIVE = $PLUS($TWO)($THREE);

my $SIX = $MULT($TWO)($THREE);

my $SEVEN = $SUCC($SUCC($SUCC($SUCC($SUCC($SUCC($ONE))))));

my $EIGHT = $PRED($MULT($THREE)($THREE));

my $NINE = $EXP($THREE)($TWO);

my $TEN = $MINUS($PLUS($EIGHT)($THREE))($ONE);

# comparison

my $IS_ZERO = -> $n { $n(-> $m { $FALSE })($TRUE) }

my $LESS_THAN_OR_EQUAL = -> $n { -> $m { $IS_ZERO($MINUS($n)($m)) } }

my $LESS_THAN = -> $n { -> $m { $AND($LESS_THAN_OR_EQUAL($n)($m))\
                             ($NOT($IS_ZERO($n($PRED)($m)))) } }

my $EQUALS = -> $n { -> $m { $AND($LESS_THAN_OR_EQUAL($n)($m))\
                          ($LESS_THAN_OR_EQUAL($m)($n)) } }

my $GREATER_THAN_OR_EQUAL = -> $n { -> $m { $IS_ZERO($n($PRED)($m)) } }

my $GREATER_THAN = -> $n { -> $m { $AND($GREATER_THAN_OR_EQUAL($n)($m))\
                                ($NOT($IS_ZERO($MINUS($n)($m)))) } }

my $MAX = -> $x { -> $y { \
  $IF_THEN_ELSE($LESS_THAN_OR_EQUAL($x)($y))\
    ($y)\
    ($x)\
  }\
}

my $MIN = -> $x { -> $y {\
  $IF_THEN_ELSE($EQUALS($MAX($x)($y))($x))\
    ($y)\
    ($x)\
  }\
}

# function composition

my $COMPOSE = -> $f { -> $g { -> $x { $f($g($x)) } } }

# recursion

my $FIX = -> $f { -> $x { $f(-> $y { $x($x)($y) }) }(-> $x { $f(-> $y { $x($x)($y) }) }) } 

# advanced arithmetic

my $MOD = $FIX(-> $r { -> $n { -> $m {\
  $IF_THEN_ELSE($LESS_THAN_OR_EQUAL($m)($n))\
    (-> $x { $r($MINUS($n)($m))($m)($x) })\
    ($n)\
  } } }\
); 

my $DIV = $FIX(-> $r { -> $n { -> $m {\
  $IF_THEN_ELSE($LESS_THAN_OR_EQUAL($m)($n))\
    (-> $x { $SUCC($r($MINUS($n)($m))($m))($x) })\
    ($ZERO)\
  } } }\
);

# other combinators

my $EVEN = -> $n { $IS_ZERO($MOD($n)($TWO)) }

my $ODD = $COMPOSE($NOT)($EVEN);

# pairs

my $PAIR = -> $x { -> $y { -> $p { $p($x)($y) } } }

my $FIRST = -> $p { $p(-> $x { -> $y { $x } }) }

my $SECOND = -> $p { $p(-> $x { -> $y { $y } }) }

# lists

my $LIST_ELEMENT = -> $x { -> $xs { $PAIR($FALSE)($PAIR($x)($xs)) } }

my $EMPTY_LIST = $PAIR($TRUE)($TRUE);

my $IS_EMPTY = $FIRST;

my $HEAD = -> $xs { $FIRST($SECOND($xs)) }

my $TAIL = -> $xs { $SECOND($SECOND($xs)) }

# fold/map/filter

my $FOLD = $FIX(-> $r { -> $f { -> $z { -> $xs {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($z)\
    (-> $x { $f($HEAD($xs))($r($f)($z)($TAIL($xs)))($x) })\
  } } } }\
);

my $MAP = -> $f {\
  $FOLD(-> $x { -> $xs {\
    $LIST_ELEMENT($f($x))($xs)\
  } })\
  ($EMPTY_LIST)\
} 

my $FILTER = -> $p {\
  $FOLD(-> $x { -> $xs {\
    $IF_THEN_ELSE($p($x))\
      ($LIST_ELEMENT($x)($xs))\
      ($xs)\
  } })\
  ($EMPTY_LIST)\
}

# other list functions

my $RANGE = $FIX(-> $r { -> $m { -> $n {\
  $IF_THEN_ELSE($LESS_THAN_OR_EQUAL($m)($n))\
    (-> $x { $LIST_ELEMENT($m)($r($SUCC($m))($n))($x) })\
    ($EMPTY_LIST)\
  } } }\
);

my $INDEX = $FIX(-> $r { -> $xs { -> $n {\
  $IF_THEN_ELSE($IS_ZERO($n))\
    ($HEAD($xs))\
    (-> $x { $r($TAIL($xs))($PRED($n))($x) })\
  } } }\
);

my $PUSH = -> $x { -> $xs { $FOLD($LIST_ELEMENT)($LIST_ELEMENT($x)($EMPTY_LIST))($xs) } }

my $APPEND = $FIX(-> $r { -> $xs { -> $ys {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($ys)\
    (-> $x { $LIST_ELEMENT($HEAD($xs))($r($TAIL($xs))($ys))($x) })\
  } } }\
);

my $LENGTH = -> $xs { ($FIX(-> $r { -> $xs { -> $n {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($n)\
    (-> $x { $r($TAIL($xs))($SUCC($n))($x) })\
  } } }\
))($xs)($ZERO) }

my $REVERSE = -> $xs { ($FIX(-> $r { -> $xs { -> $a {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($a)\
    (-> $x { ($r($TAIL($xs))($LIST_ELEMENT($HEAD($xs))($a)))($x) })\
  } } }\
))($xs)($EMPTY_LIST) }

my $TAKE = $FIX(-> $r { -> $n { -> $xs {\
  $IF_THEN_ELSE($LESS_THAN_OR_EQUAL($n)($ZERO))\
    ($EMPTY_LIST)\
    ($IF_THEN_ELSE($IS_EMPTY($xs)))\
      ($EMPTY_LIST)\
      (-> $x { $LIST_ELEMENT($HEAD($xs))($r($MINUS($n)($ONE))($TAIL($xs)))($x) })\
  } } }\
);

my $ZIP = $FIX(-> $r { -> $xs { -> $ys {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($EMPTY_LIST)\
    ($IF_THEN_ELSE($IS_EMPTY($ys))\
      ($EMPTY_LIST)\
      (-> $x { $LIST_ELEMENT($PAIR($HEAD($xs))($HEAD($ys)))($r($TAIL($xs))($TAIL($ys)))($x) }))\
  } } }\
);

my $ZIP_WITH = $FIX(-> $r { -> $f { -> $xs { -> $ys {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($EMPTY_LIST)\
    ($IF_THEN_ELSE($IS_EMPTY($ys))\
      ($EMPTY_LIST)\
      (-> $x { $LIST_ELEMENT($f($HEAD($xs))($HEAD($ys)))($r($f)($TAIL($xs))($TAIL($ys)))($x) }))\
  } } } }\
);

my $INSERT = $FIX(-> $r { -> $n { -> $xs {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($LIST_ELEMENT($n)($EMPTY_LIST))\
    ($IF_THEN_ELSE($GREATER_THAN($n)($HEAD($xs)))\
      (-> $x { $LIST_ELEMENT($HEAD($xs))($r($n)($TAIL($xs)))($x) })\
      ($LIST_ELEMENT($n)($xs)))\
  } } }\
);

my $SORT = $FOLD($INSERT)($EMPTY_LIST);

# streams

my $ZEROS = $FIX(-> $r { $LIST_ELEMENT($ZERO)($r) });

my $REPEAT = -> $x { $FIX(-> $r { $LIST_ELEMENT($x)($r) }) }

# functional structures (list implementations)

# monoid

my $MEMPTY = $EMPTY_LIST;

my $MAPPEND = $APPEND;

# functor

my $FMAP = $MAP;

# applicative

my $PURE = -> $x { $LIST_ELEMENT($x)($EMPTY_LIST) }

my $AP = $FIX(-> $r { -> $fs { -> $xs {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($EMPTY_LIST)\
    ($IF_THEN_ELSE($IS_EMPTY($fs))($EMPTY_LIST)\
      (-> $x { $MAPPEND($MAP($HEAD($fs))($xs))($r($TAIL($fs))($xs))($x) }))\
  } } }\
);

my $AP_ZIP_LIST = -> $fs { -> $xs {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($EMPTY_LIST)\
    ($IF_THEN_ELSE($IS_EMPTY($fs))($EMPTY_LIST)\
      ($ZIP_WITH($ID)($fs)($xs)))\
  } }

# monad

my $RETURN = $PURE;

my $BIND = $FIX(-> $r { -> $xs { -> $f {\
  $IF_THEN_ELSE($IS_EMPTY($xs))\
    ($EMPTY_LIST)\
    (-> $x { $MAPPEND($f($HEAD($xs)))($r($TAIL($xs))($f))($x) })\
  } } }\
);

# factorial

my $FACT = $FIX(-> $r { -> $n {\
  $IS_ZERO($n)\
    ($ONE)\
    (-> $x { $MULT($n)($r($PRED($n)))($x) })\
  } }\
);

# fibonacci

my $FIB = $FIX(-> $r { -> $n {\
  $IS_ZERO($n)\
    ($ZERO)\
    ($IF_THEN_ELSE($EQUALS($n)($ONE))\
      ($ONE)\
      (-> $x { $PLUS($r($MINUS($n)($ONE)))($r($MINUS($n)($TWO)))($x) })\
    )\
  } }\
);

# FizzBuzz

my $FIFTEEN = $PLUS($TEN)($FIVE);

my $TWENTY = $PLUS($TEN)($TEN);

my $HUNDRED = $MULT($TEN)($TEN);

my $F = $MULT($TEN)($SEVEN);

my $I = $PLUS($HUNDRED)($FIVE);

my $Z = $PLUS($HUNDRED)($PLUS($TWENTY)($TWO));

my $B = $PLUS($MULT($TEN)($SIX))($SIX);

my $U = $PLUS($HUNDRED)($PLUS($TEN)($SEVEN));

my $FIZZ = $LIST_ELEMENT($F)\
      ($LIST_ELEMENT($I)\
      ($LIST_ELEMENT($Z)\
      ($LIST_ELEMENT($Z)\
      ($EMPTY_LIST))));

my $BUZZ = $LIST_ELEMENT($B)\
      ($LIST_ELEMENT($U)\
      ($LIST_ELEMENT($Z)\
      ($LIST_ELEMENT($Z)\
      ($EMPTY_LIST))));

my $FIZZBUZZ = $LIST_ELEMENT($F)\
          ($LIST_ELEMENT($I)\
          ($LIST_ELEMENT($Z)\
          ($LIST_ELEMENT($Z)\
          ($BUZZ))));

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

# utility functions

my $To_Bool = -> $b { $IF_THEN_ELSE($b)(True)(False) }

my $From_Bool = -> $b { $b ?? $TRUE !! $FALSE }

my $To_Int = -> $n { $n(-> $x { $x + 1 })(0) }

my $From_Int = -> $n { $n == 0 ?? -> $f { -> $x { $x } } !! -> $f { -> $x { $f($From_Int($n - 1)($f)($x)) } } }

my $To_Array = -> $xs { [].append($To_Bool($IS_EMPTY($xs)) ?? [] !! [$HEAD($xs)].append($To_Array($TAIL($xs)))) }

my $From_Array = -> $xs { $xs.elems == 0 ?? $EMPTY_LIST !! $LIST_ELEMENT($xs[0])($From_Array($xs.splice(1))) }

my $To_Array_Int = -> $xs { [].append($To_Bool($IS_EMPTY($xs)) ?? [] !! [$To_Int($HEAD($xs))].append($To_Array_Int($TAIL($xs)))) }

my $From_Array_Int = -> $xs { $xs.elems == 0 ?? $EMPTY_LIST !! $LIST_ELEMENT($From_Int($xs[0]))($From_Array_Int($xs.splice(1))) }

my $To_String = -> $str { $To_Array_Int($str).map(-> $n { $n.chr }).join() }

my $From_String = -> $str { $str.chars == 0 ?? $EMPTY_LIST !! $LIST_ELEMENT($From_Int($str.substr(0,1).ord))($From_String($str.substr(1, $str.chars))) }

my $To_FizzBuzz = -> $fb { $To_Array($fb).map(-> $x { !$To_String($x) ?? $To_Int($x) !! $To_String($x) }) }

say $To_FizzBuzz($FIZZBUZZFUNC($RANGE($ONE)($FIFTEEN)));