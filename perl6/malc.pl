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

# utility functions

my $To_Bool = -> $b { $IF_THEN_ELSE($b)(True)(False) }

my $From_Bool = -> $b { $b ?? $TRUE !! $FALSE }

my $To_Int = -> $n { $n(-> $x { $x + 1 })(0) }

my $From_Int = -> $n { $n == 0 ?? -> $f { -> $x { $x } } !! -> $f { -> $x { $f($From_Int($n - 1)($f)($x)) } } }

my $To_Array = -> $xs { [].concat($To_Bool($IS_EMPTY($xs)) ?? [] !! [$HEAD($xs)].concat($To_Array($TAIL($xs)))) }

my $From_Array = -> $xs { $xs.length == 0 ?? $EMPTY_LIST !! $LIST_ELEMENT($xs(0))($From_Array($xs.drop(1))) }

my $To_Array_Int = -> $xs { [].concat($To_Bool($IS_EMPTY($xs)) ?? [] !! [$To_Int($HEAD($xs))].concat($To_Array_Int($TAIL($xs)))) }

my $From_Array_Int = -> $xs { $xs.length == 0 ?? $EMPTY_LIST !! $LIST_ELEMENT($From_Int($xs(0)))($From_Array_Int($xs.drop(1))) }

my $To_String = -> $str { $To_Array_Int($str).map( -> $n { $n.chr }).join() }

my $From_String = -> $str { $str.length == 0 ?? $EMPTY_LIST !! $LIST_ELEMENT($From_Int($str(0).ord))($From_String($str(1, $str.length))) }

my $To_FizzBuzz = -> $fb { $To_Array($fb).map( -> $x { $To_String($x) == "" ?? $To_Int($x) !! $To_String($x) }) }