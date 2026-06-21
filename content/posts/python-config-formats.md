Title: Config File Formats in Python: A Practical Guide
Date: 2026-06-21
Author: Gifted
Tags: python, configuration, yaml, toml, json, ini, best-practices
Slug: python-config-formats
Summary: A hands-on look at every config format Python projects actually use — INI, JSON, YAML, TOML, and env files — with real code examples and when each one makes sense.

---

Every Python project needs configuration at some point. Database credentials, feature flags, API keys, logging levels — something has to live outside your code. The question is: what format do you put it in?

There's no single right answer. There are, however, clear trade-offs. Here's what I've learned from using all of them.

## The Contenders

Python projects typically use one of these formats:

| Format | Standard Library Support | Human-Friendly | Comments | Data Types |
|--------|-------------------------|----------------|----------|------------|
| INI / CFG | `configparser` (built-in) | Yes | Yes | Strings only |
| JSON | `json` (built-in) | Moderate | No | Full |
| YAML | `PyYAML` (third-party) | Very | Yes | Full |
| TOML | `tomllib` (3.11+ built-in) | Very | Yes | Full |
| .env | `python-dotenv` (third-party) | Yes | Yes | Strings only |
| Python files | Nothing needed | Yes | Yes | Anything |

Let's walk through each one.

## INI: The Old Reliable

INI files have been around since MS-DOS. Python's `configparser` module handles them natively.

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

db_host = config['database']['host']
db_port = config.getint('database', 'port')
```

```ini
# config.ini
[database]
host = localhost
port = 5432
name = myapp

[logging]
level = INFO
file = /var/log/myapp.log
```

**When to use it:** Legacy projects, simple key-value configs, or when you want zero dependencies. INI is readable, supports sections, and everyone understands it immediately.

**When to skip it:** Everything is a string. No native support for lists, booleans, or nested structures. If your config has any complexity, you'll end up writing parsing code on top of `configparser`.

## JSON: The Universal Language

JSON is everywhere. Python's `json` module is built in.

```python
import json

with open('config.json') as f:
    config = json.load(f)

api_key = config['api']['key']
debug = config['debug']
```

```json
{
  "debug": true,
  "api": {
    "key": "abc123",
    "timeout": 30
  },
  "features": ["auth", "billing", "notifications"]
}
```

**When to use it:** Machine-generated configs, API responses, or when your config is produced/consumed by other systems. JSON is the lingua franca of web services.

**When to skip it:** No comments. Trailing commas cause errors. Humans editing JSON by hand will make mistakes. If people need to maintain the file directly, JSON fights you.

## YAML: The Human-First Format

YAML is designed to be readable. It supports comments, anchors, aliases, and complex nesting.

```python
import yaml  # pip install pyyaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

db = config['database']
print(db['host'], db['port'])
```

```yaml
# config.yaml
database:
  host: localhost
  port: 5432
  credentials:
    username: admin
    password: ${DB_PASSWORD}  # substituted at runtime

logging:
  level: INFO
  handlers:
    - console
    - file
```

**When to use it:** Complex configs with deep nesting, or when non-developers need to edit the file. Docker Compose, Ansible, and GitHub Actions all use YAML for this reason.

**When to skip it:** PyYAML is a third-party dependency. YAML's flexibility is a double-edged sword — indentation errors, unexpected type coercion (`yes` becomes `True`), and the infamous [Norway problem](https://hitchdev.com/strictyaml/why/implicit-typing-removed/). Always use `safe_load()`, never `load()`.

## TOML: The Modern Default

TOML was created specifically as a better INI. Python 3.11+ includes `tomllib` in the standard library.

```python
import tomllib

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)

title = config['project']['title']
version = config['project']['version']
```

```toml
# config.toml
[project]
title = "My App"
version = "1.2.0"

[database]
host = "localhost"
port = 5432

[logging]
level = "INFO"
```

**When to use it:** New Python projects. `pyproject.toml` is already the standard for Python packaging, so your team already knows TOML. It supports comments, has clear syntax, and handles types properly.

**When to skip it:** If you need to support Python < 3.11, you'll need the `tomli` backport package. Also, deeply nested TOML gets verbose — the `[a.b.c.d]` header syntax doesn't scale as gracefully as YAML's indentation.

## .env Files: Secrets and Environment

`.env` files aren't a config format so much as a convention. Each line is a key-value pair.

```python
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env into os.environ

db_url = os.environ['DATABASE_URL']
secret_key = os.environ['SECRET_KEY']
```

```env
# .env
DATABASE_URL=postgresql://user:pass@localhost/myapp
SECRET_KEY=super-secret-value
DEBUG=true
```

**When to use it:** Environment-specific secrets and variables. The 12-factor app methodology recommends storing config in the environment, and `.env` files are the local development equivalent.

**When to skip it:** Everything is a string. No nesting, no lists, no structure. `.env` files work best for a flat set of variables, not complex configuration. And never commit them to version control.

## Python Files: Just Use Code

Some projects skip config files entirely and use a Python module.

```python
# config.py
DEBUG = True
DATABASE = {
    'host': 'localhost',
    'port': 5432,
    'name': 'myapp',
}
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

```python
from config import DEBUG, DATABASE
```

**When to use it:** When your config needs logic, or when you want IDE autocompletion and type checking. Django's `settings.py` is the canonical example.

**When to skip it:** Now you're executing untrusted code. If anyone can modify the config file, they can run arbitrary Python. This also makes it harder to generate or validate config programmatically.

## What I Actually Use

For new Python projects, my default stack is:

- **`pyproject.toml`** — project metadata and tool configuration (already standard)
- **`.env`** — secrets and environment-specific values (loaded via `python-dotenv`)
- **`config.yaml`** or **`config.toml`** — application-level configuration that humans edit

I avoid INI unless I'm maintaining something old. I avoid JSON for anything humans write. I avoid Python config files unless the project already uses that pattern.

## The Real Rule

The best config format is the one your team will actually maintain correctly. A perfectly structured YAML file that nobody wants to edit is worse than a simple `.env` file people understand.

Pick the simplest format that handles your actual requirements. Add complexity only when the config demands it — not because a format is popular.
