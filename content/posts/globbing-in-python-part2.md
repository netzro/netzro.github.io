Title: Globbing in Python, Part 2: Beyond the Basics
Date: 2026-09-08
Time: 08:00
Author: Gifted
Tags: python, globbing, programming, tutorial
Slug: globbing-in-python-part2
Summary: Going past the basics: fnmatch for string-only matching, brace expansion, writing a custom glob engine, and globbing across remote filesystems.

## Where Part 1 left us

In [Part 1](https://netzro.github.io/posts/2026/Aug/02/globbing-in-python/) we covered the essentials: `*`, `?`, `[...]`, `**`, and the `glob` module. We also looked at `pathlib.Path.glob()` as the modern alternative.

Now we go further. The tools here are `fnmatch`, brace expansion, and a peek under the hood at how globbing actually works. None of them are exotic — they're just ways to match patterns when `glob` alone isn't enough.

## fnmatch: pattern matching for strings

`glob` matches against file paths. `fnmatch` matches against *any string*. It uses the same wildcards (`*`, `?`, `[...]`) but works on plain text, not the filesystem.

```python
import fnmatch

# Filter a list of strings
names = ["alice", "bob", "charlie", "dave"]
fnmatch.filter(names, "a*")        # ['alice']
fnmatch.filter(names, "?ob")       # ['bob']
fnmatch.filter(names, "[c-d]*")    # ['charlie', 'dave']
```

This is useful when you already have a list of strings and want to filter them without touching the filesystem. Configuration files, log parsing, user input validation — anywhere you need "does this string match this pattern?"

```python
# Case-insensitive matching
fnmatch.fnmatchcase("Hello", "hello")   # False (case-sensitive)
fnmatch.fnmatch("Hello", "hello")       # True on some platforms, False on others

# Use fnmatchcase for reliable case-insensitive matching
fnmatch.fnmatchcase("Hello".lower(), "hello")  # True
```

One gotcha: `fnmatch.fnmatch` is case-sensitive on Linux but case-insensitive on Windows. Use `fnmatchcase` when you need consistent behavior across platforms.

## Brace expansion: matching multiple patterns

Standard glob doesn't support brace expansion. You can't do `*.{py,md,txt}` with `glob.glob()`. But you can build it yourself:

```python
import glob
import re

def brace_expand(pattern):
    """Expand brace patterns like *.{py,md} into multiple glob patterns."""
    # Find the first {a,b,c} group
    match = re.search(r'\{([^}]+)\}', pattern)
    if not match:
        return [pattern]
    
    prefix = pattern[:match.start()]
    suffix = pattern[match.end():]
    options = match.group(1).split(',')
    
    results = []
    for opt in options:
        # Recursively expand nested braces
        results.extend(brace_expand(prefix + opt + suffix))
    return results

# Usage
patterns = brace_expand("*.{py,md}")
print(patterns)  # ['*.py', '*.md']

# Now glob each one
files = []
for p in patterns:
    files.extend(glob.glob(p))
```

This is a simplified version. Real brace expansion handles nested braces and escaped characters, but this covers 90% of use cases.

## Writing a custom glob engine

Understanding how globbing works internally makes you better at using it. Here's a minimal recursive glob engine:

```python
import os
import re

def glob_to_regex(pattern):
    """Convert a glob pattern to a regex pattern."""
    regex = []
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == '*':
            # Check for ** (recursive)
            if i + 1 < len(pattern) and pattern[i + 1] == '*':
                regex.append('.*')
                i += 2
            else:
                regex.append('[^/]*')
                i += 1
        elif char == '?':
            regex.append('.')
            i += 1
        elif char == '[':
            # Find closing bracket
            j = pattern.index(']', i)
            regex.append(pattern[i:j+1])
            i = j + 1
        else:
            regex.append(re.escape(char))
            i += 1
    return '^' + ''.join(regex) + '$'

def custom_glob(pattern, root='.'):
    """A minimal recursive glob implementation."""
    regex = re.compile(glob_to_regex(pattern))
    matches = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        for name in filenames + dirnames:
            full_path = os.path.join(dirpath, name)
            if regex.match(full_path):
                matches.append(full_path)
    
    return matches

# Usage
custom_glob("*.py")           # All .py files recursively
custom_glob("src/*.md")       # Markdown files in src/
```

This is intentionally simple. Python's `glob` module handles edge cases (hidden files, sorting, escaping) that this doesn't. But it shows the core idea: glob patterns are just regex in disguise.

## Globbing across remote filesystems

Sometimes you need to glob files that aren't on your local machine. A few approaches:

**1. SSH + glob**

```python
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('example.com', username='user')

sftp = ssh.open_sftp()
# List files matching a pattern remotely
files = sftp.listdir('/var/log/')
logs = [f for f in files if f.endswith('.log')]
```

**2. Cloud storage (S3, GCS)**

```python
import boto3

s3 = boto3.client('s3')
# S3 doesn't support glob natively — you list and filter
response = s3.list_objects_v2(Bucket='my-bucket', Prefix='data/')
files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.csv')]
```

**3. HTTP/HTTPS**

```python
import requests
from bs4 import BeautifulSoup

# Parse an index page and filter links
resp = requests.get('https://example.com/files/')
soup = BeautifulSoup(resp.text, 'html.parser')
pdfs = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.pdf')]
```

The pattern is the same everywhere: list, then filter. The glob syntax changes, but the idea doesn't.

## Performance considerations

When globbing large directories, a few things matter:

1. **Avoid `**` when you know the depth** — `glob.glob("src/**/*.py")` walks every subdirectory. `glob.glob("src/*/*.py")` is faster if you know the structure.

2. **Use `os.scandir()` for filtering** — it's faster than `os.listdir()` because it returns `DirEntry` objects with cached `stat` info.

3. **Cache results** — if you're globbing the same pattern repeatedly, cache the result. Filesystems don't change that often.

```python
from functools import lru_cache
import glob

@lru_cache(maxsize=128)
def cached_glob(pattern):
    return glob.glob(pattern, recursive=True)
```

## Where this leaves you

The through-line of both parts is simple: globbing is pattern matching for paths. `glob` and `pathlib` handle the filesystem. `fnmatch` handles strings. Brace expansion and custom engines handle the edge cases. And when files are remote, you list and filter.

If Part 1 was "here's how to find files," Part 2 is "here's how to find files when the built-in tools aren't enough." Open a recent script and find one place where you manually filter a list of filenames — replace it with `fnmatch` or a custom pattern. The code gets shorter, and the intent gets clearer.

---

*Go back to [Part 1](https://netzro.github.io/posts/2026/Aug/02/globbing-in-python/) if you need to revisit the foundations.*
