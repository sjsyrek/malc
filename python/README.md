# Python 3

`lambda`, `lambda` everywhere...

Load into your Python REPL:
```py
python3 -i malc.py
```

## How to convert JavaScript lambdas to Python

Using the regular expression `(\w+){1}\s=>\s`, replace all matches with `lambda \1: `. Add a `\` at the end of each line that does not comprise a complete expression, and indent appropriately (four spaces is typical for Python).