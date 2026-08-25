Title: Python Data Structures: Choosing the Right Tool for the Job
Date: 2026-08-25
Tags: python, data structures, programming
Slug: python-data-structures
Summary: A practical guide to Python's built-in data structures — lists, tuples, sets, and dictionaries — when to use each, their time-complexity trade-offs, and when to reach for the collections module.

## Built-In Data Structures in Python

Every Python program leans on a handful of built-in data structures. They are the vocabulary of everyday code, so knowing their strengths — and their costs — pays off almost immediately. Python gives you four core built-in types: **lists**, **tuples**, **sets**, and **dictionaries**. Each is optimized for a different job.

The question to ask yourself is not "which one can hold my data" (they all can) but **"how will I access it, and what operations matter most?"** The wrong choice turns a fast program into a slow one, and a readable program into a confusing one.

## Lists: The Ordered, Mutable Sequence

A list is an ordered, mutable, heterogeneous sequence. Lists are what you reach for by default when you have a collection of items and the order matters:

```python
# collecting things in order
primes = [2, 3, 5, 7, 11]
mixed = ["title", 42, 3.14, True]

# append adds to the end
primes.append(13)
# extend merges another iterable
primes.extend([17, 19])
```

### How lists actually work

Under the hood a Python list is a **dynamic array**, not a linked list. The list object holds a pointer to an array of references, plus a length and a reserved capacity. When the array fills up, Python allocates a new, larger block and copies everything over. The growth factor smooths this out, so although a single `append` can trigger a copy, the **amortized** cost across many appends is O(1).

That has consequences for the time complexity of the operations you actually call:

| Operation | Average | Worst-case | Notes |
|-----------|---------|------------|-------|
| `list[i]` | O(1) | O(1) | random access by index |
| `list.append(x)` | O(1) amortized | O(n) | occasional resize/copy |
| `list.insert(0, x)` | O(n) | O(n) | every element must shift |
| `x in list` | O(n) | O(n) | linear scan |
| `list.pop()` | O(1) amortized | O(1) | pops the end |
| `list.pop(0)` | O(n) | O(n) | shifts every element |

### When to use a list

Use a list when:

- Order matters and you iterate or index by position.
- You append mostly at the end (the common case).
- Items may be heterogeneous or mixed types.
- You need slicing (`list[2:5]`).

Do **not** use a list when:

- You need fast membership tests (`x in list` is O(n)). Use a set.
- You need to pop from the front repeatedly. Use a `deque` from the `collections` module.
- You mostly need key/value lookup. Use a dict.

```python
# Good: sequential append + indexed access
def running_totals(values):
    totals = []
    running = 0
    for v in values:
        running += v
        totals.append(running)
    return totals

# Bad: membership test on a list — becomes slow as it grows
banned = ["spam", "eggs", "ham", "sausage"]
# ... thousands of entries later ...
if word in banned:  # O(n) per check
    pass
```

## Tuples: The Immutable Sequence

A tuple is an ordered, **immutable**, heterogeneous sequence. The defining feature is immutability — you cannot add, remove, or reassign elements after creation:

```python
point = (3, 4)
# point[0] = 5  # TypeError: 'tuple' object does not support item assignment

# a tuple of one element needs a trailing comma
single = (42,)
```

Because tuples are immutable and do not over-allocate capacity like lists, they are slightly more memory-efficient and can be faster to iterate. More importantly, **only immutable types can be hashable**, and tuples inherit hashability from their elements — so a tuple is a valid dict key or set member, while a list is not:

```python
cache = {}
cache[(2026, "en")] = "cache miss"  # tuple keys are fine

# cache[[2026, "en"]] = "..."  # TypeError: unhashable type: 'list'
```

### When to use a tuple

Use a tuple when:

- The sequence represents a fixed record or coordinate: `("Alice", 30, "engineer")`.
- You want the data to be immutable by contract — it signals "this collection should not change."
- You need a hashable container, such as a dict key or set member.
- You want named fields (use a named-tuple or dataclass instead of raw indexing).

Avoid tuples when you need to grow or shrink the collection — use a list.

## Sets: The Unordered, Unique Collection

A set is an unordered collection of **unique** hashable elements. Sets are built on hash tables (the same data structure backing dicts), which gives them their signature property: **membership testing in O(1) average time**.

```python
primes = {2, 3, 5, 7, 11}
primes.add(13)
primes.add(2)  # duplicates are ignored

# set comprehension
evens = {x for x in range(10) if x % 2 == 0}
```

### How sets work: hash tables

When you ask `x in some_set`, Python hashes `x`, uses that hash to jump straight to a bucket, and checks only the few items in that bucket. That is why `x in set` is O(1) on average and `x in list` is O(n) — the list has no index at all and must scan every element.

| Operation | Average | Worst-case |
|-----------|---------|------------|
| `x in set` | O(1) | O(n) |
| `set.add(x)` | O(1) | O(n) |
| `set.discard(x)` | O(1) | O(n) |
| `set.pop()` | O(1) | O(1) |
| `set | other` (union) | O(len(set)) | O(len(set)) |
| `set & other` (intersection) | O(min(len(set), len(other))) | O(min(len(set), len(other))) |

The worst case is O(n) when many elements hash to the same bucket — but this is rare in practice unless you feed Python a pathological input.

### When to use a set

Use a set when:

- You need **fast membership tests** (`item in collection` happens a lot).
- You need to **deduplicate** a sequence.
- You need **set math**: unions, intersections, differences.
- You do not care about order.

```python
# Deduplicating while preserving nothing about order
emails = ["a@example.com", "b@example.com", "a@example.com"]
unique_emails = set(emails)

# Fast membership test instead of scanning a list
stop_words = {"the", "a", "an", "in", "on", "at"}
tokens = text.split()
filtered = [t for t in tokens if t.lower() not in stop_words]  # O(1) per check
```

Avoid sets when:

- You need to preserve insertion order or access by index. Use a list.
- Your elements are unhashable (lists, dicts). Convert them to tuples first, or use a different structure.

## Dictionaries: The Key-to-Value Map

A dictionary maps **keys** to **values**. In modern Python (3.7+) dicts also preserve **insertion order**, which makes them more useful than they used to be. Like sets, dicts are backed by hash tables, so lookup is O(1) on average:

```python
config = {"host": "localhost", "port": 8080, "debug": True}
config["port"] = 9090
# .get() avoids KeyError
timeout = config.get("timeout", 30)
```

### Time complexity

| Operation | Average | Worst-case |
|-----------|---------|------------|
| `d[key]` | O(1) | O(n) |
| `d.get(key)` | O(1) | O(n) |
| `key in d` | O(1) | O(n) |
| `d[key] = value` | O(1) amortized | O(n) |
| `del d[key]` | O(1) amortized | O(n) |

### When to use a dict

Use a dict when:

- You need to **look up** a value by a key.
- You need **counting** or grouping by category.
- You want to map one set of values to another (translation tables, configs, objects).
- You are counting frequencies, caching results, or attaching metadata to records.

```python
# Counting word frequency — the classic dict pattern
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1

# Or, more cleanly, with defaultdict or Counter (below)
```

Avoid dicts when you need order-only operations without keys (use a list), when you need uniqueness without values (use a set), or when your keys are unhashable.

## Choosing at a Glance

The decision mostly comes down to three questions:

| Decision tree | Result |
|---------------|--------|
| Do I need **unique** elements and fast membership? | **set** |
| Do I need to look up values by **key**? | **dict** |
| Do I need to **modify** the collection? | **list** (mutable) |
| Is the collection fixed and small, used as a record or key? | **tuple** (immutable) |

A quick reference for the most common patterns:

- **Stack**: `list.append` / `list.pop` — O(1), built-in.
- **Queue**: `collections.deque` with `append` / `popleft` — O(1). A list's `pop(0)` is O(n).
- **Ordered unique collection**: a `dict` (as an ordered set): `dict.fromkeys(items)`.
- **Fast "have I seen this?"**: `set`.
- **Counts or tallies**: `collections.Counter`.

## The `collections` Module: Specialized Tools

The `collections` module ships with Python and provides tuned replacements for the built-ins when you need something more specific.

### `deque`: Fast appends and pops from both ends

A `deque` (double-ended queue) is a doubly-linked list of blocks. Appending and popping from **either end** is O(1):

```python
from collections import deque

q = deque([1, 2, 3])
q.append(4)      # [1, 2, 3, 4]
q.popleft()      # 1, q is now [2, 3, 4]

# A deque is also bounded — great for a sliding-window buffer
window = deque(maxlen=3)
for x in range(10):
    window.append(x)
    print(window)  # only the last 3 values are kept
```

Use a `deque` when you need a queue (FIFO) or a sliding window. For pure end-of-list stacks, a plain `list` is fine and simpler.

### `Counter`: A dict built for counting

`Counter` is a `dict` subclass where missing keys default to `0`. Perfect for tallying:

```python
from collections import Counter

words = ["apple", "banana", "apple", "orange", "banana", "apple"]
counts = Counter(words)
# Counter({'apple': 3, 'banana': 2, 'orange': 1})

# most_common returns the top N
print(counts.most_common(2))  # [('apple', 3), ('banana', 2)]

# Counter supports arithmetic: combining two tallies
extra = Counter(["apple", "kiwi"])
total = counts + extra
```

Use a `Counter` whenever you are counting occurrences of hashable items. Replacing the manual `d[key] = d.get(key, 0) + 1` loop with a `Counter` is one of the cleanest wins in Python.

### `defaultdict`: A dict that never says KeyError

A `defaultdict` auto-creates missing entries using a factory you specify:

```python
from collections import defaultdict

# group items by a key without checking membership each time
groups = defaultdict(list)
for item in records:
    groups[item.category].append(item)

# default_factory can be any zero-argument callable
counts = defaultdict(int)
counts["hits"] += 1  # starts at 0 automatically
```

Use a `defaultdict` when you are accumulating into a collection (list, set, int) and the repeated `if key not in d` boilerplate clutters your code. It is a readability win over plain dicts for grouping and tallying. If you also need counts and ordering, `Counter` is usually the better fit.

### `OrderedDict`: When order matters and you want explicit control

Before Python 3.7, dicts did not guarantee insertion order, so `OrderedDict` existed to fill that gap. Since 3.7, regular dicts preserve order, so for most use cases a plain dict is enough. `OrderedDict` still has one edge: its `==` comparison is **order-sensitive** (unlike dict), and it provides `move_to_end()`:

```python
from collections import OrderedDict

cache = OrderedDict()
cache["a"] = 1
cache["b"] = 2
cache.move_to_end("a")  # "a" is now the most recently used
```

Use `OrderedDict` when you need order-sensitive equality, LRU-style reordering, or you support Python 3.6 and earlier. Otherwise, stick with plain `dict`.

## A Worked Example: Log Analysis

Here is a small program that puts several of these structures together. It reads a log file, finds the top request paths, keeps a sliding window of recent status codes, and groups errors by path:

```python
from collections import Counter, defaultdict, deque

def analyze_log(lines):
    # Count how often each path appears
    path_counts = Counter()

    # Keep only the last 100 status codes seen (sliding window)
    recent_statuses = deque(maxlen=100)

    # Group error messages by path
    errors_by_path = defaultdict(list)

    for line in lines:
        parts = line.split()
        if len(parts) < 9:
            continue
        path = parts[6]
        status = parts[8]

        path_counts[path] += 1
        recent_statuses.append(status)

        if status.startswith("5"):  # server error
            errors_by_path[path].append(line.strip())

    # Top 5 most-requested paths
    top_paths = path_counts.most_common(5)

    # 404 paths: those in the log but not in the top list
    top_set = {p for p, _ in top_paths}
    low_traffic = {p for p in path_counts if p not in top_set}

    return top_paths, dict(recent_statuses), errors_by_path, low_traffic

# Simulated log lines
sample = [
    '127.0.0.1 - - [01/Jan/2026:12:00:00] "GET /index.html" 200 1024',
    '127.0.0.1 - - [01/Jan/2026:12:00:01] "GET /about" 200 512',
    '127.0.0.1 - - [01/Jan/2026:12:00:02] "GET /index.html" 200 1024',
    '127.0.0.1 - - [01/Jan/2026:12:00:03] "GET /missing" 404 128',
    '127.0.0.1 - - [01/Jan/2026:12:00:04] "GET /index.html" 500 0',
]

top, statuses, errors, low = analyze_log(sample)
print("Top paths:", top)
print("Recent statuses:", statuses)
print("Errors by path:", errors)
print("Low-traffic paths:", low)
```

This shows the structures cooperating rather than competing: `Counter` for tallying, `deque` for the bounded window, `defaultdict` for grouping, and `set` comprehensions for the membership math.

## Bottom Line

Start with the built-in that matches your access pattern:

- **Membership testing** → `set`
- **Key/value lookup** → `dict`
- **Ordered, mutable collection** → `list`
- **Ordered, immutable record or key** → `tuple`

When the built-in falls short on complexity or ergonomics, the `collections` module usually has a tuned specialist: `deque` for queues, `Counter` for tallies, `defaultdict` for grouping. Reach for them when they remove real boilerplate — not because they are "more advanced." The best data structure is the one whose complexity you do not pay for, and whose clarity saves more time than you spend learning it.
