# malc - make a lambda calculus
# Perl 6
# Steven Syrek

# identity combinator

my $ID = -> $x { $x }

my $TRUE = -> $x { -> $y { $x } }

my $FALSE = -> $x { -> $y { $y } }