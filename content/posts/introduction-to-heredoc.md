---
Title: Introduction to Heredoc
Date: 2026-09-14
Time: 14:11
Author: Gifted
Tags: bash, python, programming, tutorial
Slug: introduction-to-heredoc
Summary: Learn the basics of heredoc and nowdoc in Bash and Python — syntax, differences, and common use cases.
---

# Introduction to Heredoc

Heredoc is a way to pass multi-line input to a command or language without fussing over escaping or newline characters. It's one of those quiet tools that saves you a surprising amount of time once you understand the mechanics.

I'll cover the basics of heredoc, the distinction between heredoc and nowdoc, where they shine in practice, and how they work in Bash and Python.

## The basic idea

At its core, heredoc lets you embed a block of text directly in your script or command line. You choose a delimiter — any word you like — and everything until that word appears on a line by itself becomes the input.

```bash
cat << EOF
Hello, world!
This is line two.
EOF
```

The shell reads everything between the opening `<< EOF` and the closing `EOF` as the standard input to `cat`. No need to quote, escape, or concatenate strings.

## Heredoc vs nowdoc

Not all heredocs are the same. The key distinction is **variable interpolation** — whether placeholders inside the block get expanded or left as literal text.

**Heredoc** (Bash, PHP, Ruby) expands variables inside the block:

```bash
name="Gifted"
cat << EOF
Hello, $name
Today is $(date +%A)
EOF
```

Output:
```
Hello, Gifted
Today is Monday
```

**Nowdoc** (PHP, and conceptually in Python with raw strings) treats the block as literal — no variable expansion happens. In PHP, you quote the delimiter:

```php
$name = "Gifted";
echo <<<'EOF'
Hello, $name
This stays exactly as typed.
EOF;
```

The distinction matters when you need to preserve dollar signs, backticks, or template literals as-is — configuration files, SQL strings, or code generation.

## Common use cases

Heredocs excel anywhere you'd otherwise reach for `echo` chains or messy quoting:

1. **Generating config files** — Write entire configs inline instead of editing them separately.
2. **Running SQL queries** — Pass multi-line SQL to `mysql`, `psql`, or `sqlite3` without escaping.
3. **Here documents in tests** — Embed expected output or fixture data directly in test files.
4. **Sending emails** — Compose email bodies inline for `sendmail` or `mail`.
5. **Embedding templates** — Build HTML, Markdown, or other structured text from variables.

## Python's take

Python doesn't have a built-in heredoc operator, but achieves the same result with **triple-quoted strings**:

```python
import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

query = """
    SELECT id, name, email
    FROM users
    WHERE active = 1
    ORDER BY name;
"""

cur.execute(query)
```

Triple quotes (`"""` or `'''`) preserve newlines and indentation naturally. Use `'''` (or `r"""`) when you need a raw string — Python's equivalent of nowdoc — to avoid escaping backslashes or dollar signs.

You can also combine this with `textwrap.dedent()` to strip leading whitespace from indented blocks:

```python
from textwrap import dedent

config = dedent("""
    [database]
    host = localhost
    port = 5432
    name = myapp
""").strip()
```

## Bash deep dive

Bash heredoc has a couple of useful variants. The standard form:

```bash
cat << EOF
Some text here
EOF
```

**Stripping leading tabs** — Prefix the delimiter with `-` to remove leading tab characters (not spaces). This keeps your heredoc indented in a script without adding tabs to the output:

```bash
if true; then
    cat <<- EOF
        This has no leading tabs
    EOF
fi
```

**Quoting the delimiter** — `'EOF'` turns off variable expansion, giving you nowdoc-like behavior:

```bash
price='$100'
cat << 'EOF'
The price is $price
EOF
# Output: The price is $price
```

Without the quotes, `$price` would expand to `100`.

## When to reach for heredoc

Use heredoc when the text you're passing is long enough that inline quotes become unwieldy, or when the content itself contains quotes, newlines, or special characters that would be painful to escape.

If the text is short and simple, a quoted string is still cleaner. Heredoc is a tool, not a default — but when the situation calls for it, nothing else feels as natural.

I reach for it constantly in scripts that generate configs, seed databases, or compose structured text. Once you internalize the syntax, you'll spot the use cases everywhere.
