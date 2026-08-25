Title: Python Data Classes: Cleaner Code with Less Boilerplate
Date: 2026-08-25
Tags: python, programming
Slug: python-data-classes
Summary: A practical guide to data classes, why they replace hand-rolled classes for data containers, and the features that make them worth reaching for.

## What Are Data Classes?

The `dataclass` decorator (introduced in Python 3.7 via the standard-library `dataclasses` module) is a way to declare classes whose **primary purpose is to store data**. You write annotations for the fields you want, and the decorator generates the boring parts for you: `__init__`, `__repr__`, `__eq__`, and others.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

That single block is equivalent to a plain class that manually writes out an `__init__` taking `x` and `y`, a `__repr__` showing `Point(x=..., y=...)`, and an `__eq__` comparing both fields. The decorator does the typing and the ceremony so you do not have to.

## Why Reach for Them?

There is nothing you can do with a data class that you cannot do by hand — the value is in what you get rid of.

**vs plain classes.** A classic `class Point:` with a hand-written `__init__`, `__repr__`, and `__eq__` is easy to get slightly wrong (forgetting a field in `__eq__`, swapping order in `__init__`). Data classes keep the definition and the generated methods in sync automatically.

**vs tuples.** Tuples are compact and fast, but they are positional. `p[0]` is opaque until you remember it is `x`. A data class reads `p.x` and still lets you unpack `x, y = p` when you need to.

**vs dicts.** A dict like `{"x": 1.0, "y": 2.0}` is flexible, but it has no type hints, no validation, and no attribute access. A data class gives you `point.x` plus static typing without losing the lightweight feel.

The trade-off is worth it whenever a type is mostly "a bag of named, typed values" — configuration, records, DTOs, results returned from a function, rows mapped from a database.

## The `@dataclass` Decorator

Decorating a class with `@dataclass` inspects its annotations and, by default, generates `__init__`, `__repr__`, and `__eq__`. The fields are inferred from annotated class attributes:

```python
from dataclasses import dataclass

@dataclass
class InventoryItem:
    name: str
    quantity: int
    price: float
```

You do not need to import `field` here; plain annotations on `str`, `int`, `float` are enough.

## What Gets Generated

`dataclass()` accepts parameters that toggle which dunder methods it synthesizes. The common ones:

- **`init=True`** (default) — generates `__init__(self, name, quantity, price)`. Pass `init=False` for a field that should never be set by the constructor.
- **`repr=True`** (default) — generates `__repr__` showing each field by name. Handy for debugging and logging.
- **`eq=True`** (default) — generates `__eq__` comparing tuples of fields. Two `InventoryItem` instances are equal iff `name`, `quantity`, and `price` all match.
- **`frozen=False`** (default) — when `True`, generates `__setattr__`/`__delattr__` that raise `FrozenInstanceError`. This makes instances **hashable** and immutable, so they become safe to use as dict keys or set members. Note that a plain (non-frozen) data class is unhashable by default, mirroring a normal mutable class.
- **`order=True`** — generates `__lt__`, `__le__`, `__gt__`, `__ge__` ordering the instance by a tuple of its fields. Useful when you need to `sort()` or `min()`/`max()` them. Implies `eq=True` and a consistent field order, so the fields must be orderable among themselves.

```python
from dataclasses import dataclass

@dataclass(order=True)
class Score:
    player: str
    points: int

scores = [Score("Ada", 7), Score("Linus", 10), Score("Grace", 7)]
for s in sorted(scores):
    print(s)
```

`order` here sorts on `player` first, then `points`. Be deliberate about field order when you use it.

## Default Values

You can give any field a default value, and the generated `__init__` will use it when the caller omits the argument:

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    flags: list[str] = field(default_factory=list)
```

Rules to remember:

- Mutable default values (a bare `list`, `dict`, or a custom object) are shared across instances, which is almost never what you want. `dataclasses` raises `ValueError` if you try `flags: list = []` to protect you.
- For mutable defaults, use `field(default_factory=...)`. A factory is called once per instance with no arguments, so `default_factory=list` gives each instance its own list. This also works for your own types: `default_factory=MyConfig.from_env`.
- Fields with defaults must come after fields without defaults, just like regular function parameters. `dataclasses` enforces this and raises `TypeError` if you get it wrong.

## Field Control with `field()`

Not every attribute should be a constructor parameter or part of the generated repr. `field()` lets you opt out:

```python
from dataclasses import dataclass, field

@dataclass
class Session:
    user: str
    token: str = field(repr=False, compare=True)
    created_at: float = field(default_factory=lambda: __import__("time").time())
```

Key `field()` arguments:

- `default` / `default_factory` — the value sources described above.
- `repr=False` — hides a field from the generated `__repr__` (good for secrets or noisy values).
- `compare=False` — excludes a field from `__eq__`/`__ne__`/`order` comparisons.
- `init=False` — the field exists on the instance but is not accepted by `__init__`; you typically set it inside `field(default=...)` or in `__post_init__`.
- `init=False, default=...` — a way to attach a class-level constant that is the same for every instance but excluded from the constructor signature.

## `__post_init__`

`__post_init__` runs once, right after the generated `__init__` finishes assigning each field. It is the intended place to compute derived values, validate, or normalize:

```python
from dataclasses import dataclass, field

@dataclass
class Temperature:
    celsius: float
    _kelvin: float = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.celsius < -273.15:
            raise ValueError("temperature below absolute zero")
        self._kelvin = self.celsius + 273.15
```

Here `_kelvin` is excluded from `__init__` (`init=False`) and from the repr, then populated in `__post_init__` from `celsius`. The public constructor `Temperature(celsius=...)` still behaves like a normal parameterised class.

## Inheritance

Data classes inherit normally, with the usual caveat that field order matters. A base data class that defines some fields can be subclassed, and fields from the parent come first in the generated `__init__`:

```python
from dataclasses import dataclass

@dataclass
class Contact:
    name: str
    email: str = ""

@dataclass
class Customer(Contact):
    account_id: str = ""
    balance: float = 0.0
```

`Customer("Ada", "ada@example.com", "C-123", 250.0)` works because the parameter list is `(name, email, account_id, balance)` — parent fields first, then child fields. The one thing to avoid is redefining a field that exists in the base class; that changes the slot ordering and raises `TypeError`, so extend rather than override.

## A Practical Example

Putting it together: a tiny inventory model where items arrive from JSON, are compared and sorted, and cached behind an immutable snapshot.

```python
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Product:
    sku: str
    name: str
    quantity: int = 0
    price: float = 0.0
    tags: list[str] = field(default_factory=list)

    # runs after __init__ assigns every field above
    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("price must be non-negative")
        self.sku = self.sku.upper()

    # convenience: build one Product from a raw dict
    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Product:
        return cls(
            sku=row.get("sku", ""),
            name=row.get("name", ""),
            quantity=int(row.get("quantity", 0)),
            price=float(row.get("price", 0.0)),
            tags=list(row.get("tags", [])),
        )

@dataclass(order=True, frozen=True)
class Snapshot:
    # `order=True` lets us sort snapshots by total value.
    # the first field below acts as the sort key via the `field` wrapper:
    total_value: float = field(compare=True)
    products: tuple[Product, ...] = field(compare=False, default=())

# ---- simulate rows from a database or CSV -----
rows = [
    {"sku": "abc", "name": "Widget", "quantity": 3, "price": "4.50", "tags": ["tool", "new"]},
    {"sku": "XYZ", "name": "Gadget", "quantity": 2, "price": "12.00", "tags": ["tool"]},
    {"sku": "def", "name": "Widget Pro", "quantity": 1, "price": "19.99", "tags": ["new"]},
]

products = [Product.from_row(r) for r in rows]
print(products[0])
# Product(sku='ABC', name='Widget', quantity=3, price=4.5, tags=['tool', 'new'])

# sort by unit price
for p in sorted(products, key=lambda x: x.price):
    print(p.name, p.price)

# an immutable, hashable snapshot we could use as a dict key
snap = Snapshot(
    total_value=sum(p.quantity * p.price for p in products),
    products=tuple(sorted(products, key=lambda x: x.sku)),
)
print(asdict(snap))
```

The `Product` class is mutable and comparison-friendly (so `sort`, `==`, and `__repr__` work out of the box), while `Snapshot` is frozen and ordered — the right shape for a value you store, deduplicate, or pass between threads without worrying about it changing underneath you.

## When to Stop Using Them

Data classes are not a replacement for every class. If your object owns expensive resources, has invariants you must protect, or needs `__slots__` for memory savings across millions of instances, a hand-rolled class is still the right tool. Reach for `@dataclass` when the question you are answering is "what data lives here, and how should it compare?", not "how do I hide state behind an abstraction?".
