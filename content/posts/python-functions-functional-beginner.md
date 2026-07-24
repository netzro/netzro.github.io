Title: Python Functions in Functional Programming, Part 1: The Basics
Date: 2026-07-09
Time: 09:30
Author: Gifted
Tags: python, functional-programming, programming, tutorial
Slug: python-functions-functional-beginner
Summary: A beginner-friendly look at how functions work in Python when you treat them the functional-programming way — first-class objects, pure functions, and the map/filter/reduce trio.

## What "functional" even means in Python

Python isn't a pure functional language like Haskell. You can mutate state, use classes, loop with `for`. But Python *borrows* a lot from functional programming, and the result is a style that's often cleaner and easier to reason about than the imperative alternative.

Functional programming comes down to three ideas:

1. Functions are **values** you can pass around.
2. Functions should avoid **side effects** when possible.
3. You build behavior by **composing** small functions.

That's it. No monads required for the basics. Let's see what each looks like in Python.

## Functions are first-class objects

In Python, a function is just another object. You can assign it to a variable, store it in a list, return it from another function, and pass it as an argument.

```python
def greet(name):
    return f"Hello, {name}!"

say = greet          # no parentheses — we're passing the function, not calling it
print(say("Ada"))    # Hello, Ada!
```

This is the foundation of everything functional in Python. Because functions are values, you can write functions that *take other functions* as input.

```python
def apply_twice(func, value):
    return func(func(value))

def add_five(x):
    return x + 5

print(apply_twice(add_five, 10))   # 20
```

A function that takes or returns another function is called a **higher-order function**. You'll meet these constantly.

## Pure functions and why they matter

A *pure* function has two properties:

- It always returns the same output for the same input.
- It doesn't change anything outside itself (no global state, no file writes, no `print` side effects).

```python
# Pure
def square(x):
    return x * x

# Impure — depends on outside state and mutates it
total = 0
def add_to_total(x):
    global total
    total += x
    return total
```

Why care? Pure functions are predictable. You can test them without setup, run them in any order, and cache their results. When a bug appears, a pure function has far fewer places to hide it.

That doesn't mean you never write impure code — printing to a screen or saving a file has to happen somewhere. The functional style is about *pushing* side effects to the edges of your program and keeping the core logic pure.

## The map / filter / reduce trio

These three are the workhorses of functional Python.

**map** applies a function to every item in an iterable:

```python
numbers = [1, 2, 3, 4]
squared = list(map(square, numbers))
print(squared)   # [1, 4, 9, 16]
```

**filter** keeps only the items that pass a test:

```python
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)     # [2, 4]
```

**reduce** collapses an iterable into a single value:

```python
from functools import reduce

product = reduce(lambda a, b: a * b, numbers)
print(product)   # 24
```

Notice the `lambda` in `filter` and `reduce`. A lambda is just a tiny anonymous function — useful when you don't need a full `def`.

```python
# These are the same
def is_even(x):
    return x % 2 == 0

is_even = lambda x: x % 2 == 0
```

## A note on list comprehensions

Python gives you list comprehensions, which often read better than `map` and `filter`:

```python
squared = [x * x for x in numbers]
evens = [x for x in numbers if x % 2 == 0]
```

Functional purists sometimes prefer `map`/`filter`, but in real Python code, comprehensions are idiomatic and fast. The functional *mindset* — transforming data without mutating it — matters more than which syntax you pick.

## Immutability: a gentle start

Functional programming favors data you don't change. Instead of editing a list, you make a new one.

```python
original = [1, 2, 3]
updated = original + [4]     # new list, original untouched
```

Tuples are immutable by default, which makes them a safe choice for data that shouldn't change:

```python
point = (3, 4)    # can't be reassigned element-wise
```

## Where this leaves you

If you take nothing else: treat functions as ordinary values, keep the core of your logic pure, and transform data by producing new data rather than mutating old data. Those habits alone will make your Python clearer.

In **Part 2**, we'll go further — `functools` (`partial`, `lru_cache`), closures, recursion, and how to refactor messy imperative code into a functional shape.

## Try it yourself

Open a Python REPL and rewrite a small `for` loop you've written recently using `map` or a comprehension. Feel how the code shrinks. That's the functional style clicking into place.
