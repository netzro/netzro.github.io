Title: Python Functions in Functional Programming, Part 2: Intermediate Techniques
Date: 2026-07-25
Time: 07:36
Author: Gifted
Tags: python, functional-programming, programming, tutorial
Slug: python-functions-functional-intermediate
Summary: Going past the basics: functools.partial and lru_cache, closures, recursion, and a real refactor of imperative code into a functional shape.

## Where Part 1 left us

In [Part 1](https://netzro.github.io/posts/2026/Jul/24/python-functions-functional-beginner/) we treated functions as ordinary values, kept the core of our logic pure, and transformed data by producing new data instead of mutating old data. That mindset is most of the battle.

Now we go a level deeper. The tools here are `functools`, closures, and recursion: the ones I reach for when a script starts to sprawl. None of them are exotic. They're just ways to make small functions do more without getting noisy.

## functools.partial: freezing arguments

`partial` takes a function and some of its arguments, and hands you back a new function with those arguments already filled in. It's like saying "I want this function, but with this one thing pre-set."

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))   # 25
print(cube(5))     # 125
```

Why bother? Because once you have `square`, you can pass it to `map` exactly like any other function. `partial` turns a two-argument function into a one-argument function that fits a slot built for one. It's a small thing that removes a lot of `lambda x: power(x, 2)` clutter.

## functools.lru_cache: memoization for free

`lru_cache` caches a function's return values so repeated calls with the same arguments skip the work. "LRU" means least-recently-used: when the cache is full, the oldest entries get evicted.

```python
from functools import lru_cache

@lru_cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))   # 12586269025, computed instantly
```

Without the cache, `fib(50)` recomputes the same smaller fibs millions of times and crawls. With it, each value is computed once. This is the practical payoff of pure functions: a function with no side effects can be cached safely, because the answer only depends on its inputs.

One caveat about `lru_cache`: it checks arguments for equality and hashability. Passing a list won't work; pass a tuple. And clear the cache (`fib.cache_clear()`) if you're measuring performance across runs.

## Closures: functions that remember

A closure is a function defined inside another function that captures variables from its enclosing scope. The inner function "remembers" those variables even after the outer function has returned.

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor   # factor is captured from the enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(10))   # 20
print(triple(10))   # 30
```

This looks a lot like `partial`, and that's no accident. `partial` is essentially a closure you don't have to write by hand. Closures shine when the captured logic is more involved than a single fixed argument. They're also the machinery behind decorators, which are just higher-order functions that wrap other functions.

## Higher-order functions, revisited

Part 1 showed `apply_twice`. A decorator is the same idea with nicer syntax:

```python
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__} with {args}")
        return func(*args, **kwargs)
    return wrapper

@debug
def add(a, b):
    return a + b
```

`debug` takes a function and returns a new one that logs before delegating. That's a higher-order function doing real work: it wraps behavior instead of replacing it.

## Recursion: solving by shrinking

Some problems are naturally self-similar: a directory and its sub-directories, a tree and its branches, a list and its tail. Recursion handles these by solving the small case directly and reducing the bigger case to a smaller one.

```python
def sum_list(items):
    if not items:
        return 0
    return items[0] + sum_list(items[1:])

print(sum_list([1, 2, 3, 4]))   # 10
```

This is elegant but allocates a new slice on every call, which is wasteful. For real list work, a loop or `reduce` is usually better. Recursion earns its place with genuinely recursive data, trees and nested structures, where the shape of the problem is recursive whether you like it or not.

Python has no tail-call optimization, so deep recursion will hit a limit. Keep recursion for problems that are shallow or structurally recursive, not for iterating over long flat sequences.

## Avoiding side effects when you refactor

Here's a messy imperative loop that mutates state as it goes:

```python
# imperative
def normalize(numbers):
    result = []
    for n in numbers:
        result.append(n / max(numbers))
    return result
```

It scans `numbers` twice and builds `result` by mutation. The functional version makes the transformation explicit and stateless:

```python
# functional
def normalize(numbers):
    peak = max(numbers)
    return [n / peak for n in numbers]
```

No list being appended to in a loop, no hidden state. The function still reads `max(numbers)` twice in spirit but now it's one clear step. More importantly, the output depends only on the input. That's the property that lets `lru_cache` and parallel execution work later.

When you refactor imperative code this way, look for three smells: a list you append to inside a loop, a counter you increment by hand, and a variable you reassign to track "the current best." Each one usually becomes a comprehension, a `reduce`, or a recursive call.

## Where this leaves you

The through-line of both parts is simple: small pure functions, composed into bigger behavior, with side effects pushed to the edges. `partial` and `lru_cache` make those functions cheaper to build and run. Closures and decorators let them carry context. Recursion handles the problems that are recursive at heart.

If Part 1 was "functions are values," Part 2 is "and here's what you can build once you really believe it." Open a recent script and find one `for` loop that appends to a list, then rewrite it as a comprehension, then as a `map`. The code gets shorter, and the intent gets clearer. That's the whole point.

---

*Go back to [Part 1](https://netzro.github.io/posts/2026/Jul/24/python-functions-functional-beginner/) if you need to revisit the foundations.*
