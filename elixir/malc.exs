# malc - make a lambda calculus
# Elixir
# Steven Syrek

# identity combinator

id = fn x -> x end

# boolean primitives

true_ = fn x -> fn y -> x end end

false_ = fn x -> fn y -> y end end

# boolean combinators

and_ = fn x -> fn y -> x.(y).(false_) end end

or_ = fn x -> fn y -> x.(true_).(y) end end

not_ = fn x -> x.(false_).(true_) end

xor = fn x -> fn y -> and_.(or_.(x).(y)).(not_.(and_.(x).(y))) end end

# branching

if_then_else = id

# natural numbers

zero = fn f -> fn x -> x end end

one = fn f -> fn x -> f.(x) end end

two = fn f -> fn x -> f.(f.(x)) end end

three = fn f -> fn x -> f.(f.(f.(x))) end end

# utility functions

to_bool = fn b -> if_then_else.(b).(true).(false) end

from_bool = fn b -> if b, do: true_, else: false_ end

to_int = fn n -> n.(fn x -> x + 1 end).(0) end

defmodule Utils do
  def from_int(n) do if n == 0, do: fn f -> fn x -> x end end, else: fn f -> fn x -> f.(from_int(n - 1).(f).(x)) end end end
end
