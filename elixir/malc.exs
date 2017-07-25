# malc - make a lambda calculus
# Elixir
# Steven Syrek

# identity combinator

id = fn x -> x end

# id = &(&1)

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

# pairs

pair = fn x -> fn y -> fn p -> p.(x).(y) end end end

first = fn p -> p.(fn x -> fn y -> x end end) end

second = fn p -> p.(fn x -> fn y -> y end end) end

# lists

list_element = fn x -> fn xs -> pair.(false_).(pair.(x).(xs)) end end

empty_list = pair.(true_).(true_)

is_empty = first

head = fn xs -> first.(second.(xs)) end

tail = fn xs -> second.(second.(xs)) end

# utility functions

to_bool = fn b -> if_then_else.(b).(true).(false) end

from_bool = fn b -> if b, do: true_, else: false_ end

to_int = fn n -> n.(fn x -> x + 1 end).(0) end

defmodule Malc do 

  def from_int(n), do: if n == 0, do: fn f -> fn x -> x end end, else: fn f -> fn x -> f.(from_int(n - 1).(f).(x)) end end

  def to_array(xs), do: quote do: [] ++ if unquote(to_bool.(is_empty.(xs)), do: [], else: [head.(xs)] ++ to_array(tail.(xs)))

  def from_array(xs), do: quote do: if length xs === 0, do: unquote(empty_list, else: list_element.(List.first(xs))(from_array(List.delete_at(xs, 0))))

  def to_array_int(xs), do: quote do: [] ++ if unquote(to_bool.(is_empty.(xs)), do: [], else: [to_int(head.(xs))] ++ to_array_int(tail.(xs)))

  def from_array_int(xs), do: quote do: if length xs === 0, do: unquote(empty_list, else: list_element.(from_int(List.first(xs)))(from_array_int(List.delete_at(xs, 0))))

end

from_int = &Malc.from_int/1

to_array = &Malc.to_array/1

from_array = &Malc.from_array/1

to_array_int = &Malc.to_array_int/1

from_array_int = &Malc.from_array_int/1

array = list_element.(one).(list_element.(two).(list_element.(three).(empty_list)))
