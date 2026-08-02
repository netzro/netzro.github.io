Title: Globbing in Python, Part 1
Date: 2026-08-02
Time: 05:13
Author: Gifted
Tags: python, globbing, programming, tutorial
Slug: globbing-in-python
Summary: A beginner-friendly look at how glob patterns work in Python — `*`, `?`, `[...]`, and the `glob` module.

## What globbing is

Globbing is pattern matching for file paths. Instead of listing every file by name, you describe a shape and the system finds the matches.

```
*.py        → all Python files
data_?.csv  → data_1.csv, data_A.csv, but not data_10.csv
[abc].txt   → a.txt, b.txt, or c.txt
```

Python has a built-in `glob` module that does exactly this. No pip install needed.

## The basics: `*` and `?`

The two most common patterns:

- `*` matches any number of characters (including zero)
- `?` matches exactly one character

```python
import glob

# All Python files in the current directory
for f in glob.glob("*.py"):
    print(f)

# Files like data_1.csv, data_X.csv — but not data_10.csv
for f in glob.glob("data_?.csv"):
    print(f)
```

`*` is greedy. `*.py` matches `setup.py`, `my_script.py`, even `.py` (an empty name with an extension). If you want non-hidden files only, combine it:

```python
# Hidden files (starting with .) are NOT matched by *
glob.glob("*.py")    # finds app.py, not .hidden.py
```

## Character classes: `[...]`

Square brackets match one character from a set:

```python
# Exactly one character from the set a, b, or c
glob.glob("[abc].txt")   # a.txt, b.txt, c.txt — not ab.txt

# Ranges work too
glob.glob("file[0-9].log")  # file0.log, file1.log, ... file9.log

# Negation with ^ or !
glob.glob("file[^0-9].log")  # fileX.log, fileA.log — not file1.log
```

## Recursive glob with `**`

Python 3.5+ supports recursive globbing with `**`. This is the most useful pattern for real work:

```python
import glob

# All Python files in current dir and every subdirectory
for f in glob.glob("**/*.py", recursive=True):
    print(f)

# All markdown files anywhere under content/
for f in glob.glob("content/**/*.md", recursive=True):
    print(f)
```

Without `recursive=True`, `**` is treated like `*` — it does NOT descend into subdirectories.

## `glob` vs `os.scandir` vs `pathlib.Path.glob`

Python gives you three ways to glob. Use each when:

| Method | Best for |
|--------|----------|
| `glob.glob()` | Quick one-liners, shell-like patterns |
| `pathlib.Path.glob()` | Object-oriented workflows, chaining with other path ops |
| `os.scandir()` | When you need fine control (filter by stat, avoid recursion) |

```python
from pathlib import Path

# Same as glob.glob("**/*.py", recursive=True)
for f in Path(".").glob("**/*.py"):
    print(f)

# Filter by something else
for f in Path(".").glob("**/*.py"):
    if f.stat().st_size > 1000:
        print(f"{f} ({f.stat().st_size} bytes)")
```

`pathlib` is the modern choice. It returns `Path` objects (not strings), so you can call `.read_text()`, `.rename()`, `.stem`, `.suffix` directly.

## Common pitfalls

1. **Hidden files are invisible to `*`** — files starting with `.` are skipped by default. If you need them, use `glob.glob(".*")` explicitly.

2. **`**` without `recursive=True` is a no-op for recursion** — it acts like `*` and only matches the current directory.

3. **Glob returns strings, not sorted** — the order is filesystem-dependent. If you need sorted results, wrap it: `sorted(glob.glob("*.py"))`.

4. **No match returns an empty list, not an error** — always handle the empty case if the result drives further logic.

```python
files = glob.glob("nonexistent/*.py")
if not files:
    print("No matches — check the directory and pattern.")
```

## Try it yourself

Open a Python REPL and try:

```python
import glob
glob.glob("**/*.md", recursive=True)
```

See how many markdown files exist under your current directory. Then try `glob.glob("content/posts/**/*.md", recursive=True)` to list every blog post.

In **Part 2**, we'll go further — `fnmatch` for string-only matching, brace expansion, writing a custom glob engine, and globbing across remote filesystems.