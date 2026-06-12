Title: Setting Up Rustledger for Personal Accounting on Android
Date: 2026-05-19
Author: Gifted
Category: Tech
Tags: finance, android, termux
Slug: setting-up-rustledger-android
Summary: How I set up rustledger for double-entry accounting on Android using proot Debian.

I've been meaning to get serious about personal accounting for a while. I tried beancount about a year ago, got the basics working for both my personal finances and my transport business, then life happened and I stopped updating it. The friction of opening a file, formatting entries correctly, and running checks manually was just too much after a long day.

What changed this time is that I now have an AI agent managing the workflow. But before I get to that — here's how I set up rustledger, which replaced beancount as my ledger engine.

## Why Rustledger

Beancount is Python-based, which means a virtual environment, pip, and a runtime that adds weight to an already constrained Android setup. Rustledger is a Rust implementation of the same double-entry accounting system — fully compatible with beancount's file format, but distributed as a single static binary.

No Python. No venv. No pip. Just download and run.

The other reason: rustledger ships an MCP server. That means my AI agent can query the ledger, run balance reports, and record transactions directly. More on that in a future post.

## Installing on Android (proot Debian)

I run everything inside proot-distro Debian on Termux. Standard ARM64 Linux binaries work fine here, but static builds are more reliable — they don't depend on shared libraries that may or may not exist in the proot environment.

First, find the right release asset:

```bash
curl -s https://api.github.com/repos/rustledger/rustledger/releases/latest \
  | grep "browser_download_url" | grep "aarch64"
```

You'll see four aarch64 options — GNU and musl, for Linux and Darwin. Pick the musl build — it's statically linked and works cleanly in proot:

```bash
curl -L https://github.com/rustledger/rustledger/releases/download/v0.15.0/rustledger-v0.15.0-aarch64-unknown-linux-musl.tar.gz -o rledger.tar.gz
tar xzf rledger.tar.gz
mv rledger /usr/local/bin/
rledger --version
```

That should print `rledger 0.15.0`. Installation done.

## The File Format

Rustledger reads standard beancount format. Every entry is plain text — accounts are opened explicitly, transactions are double-entry, and everything must balance. A minimal personal file looks like this:

```
option "operating_currency" "NGN"

2026-01-01 open Assets:OPay
2026-01-01 open Assets:Cash
2026-01-01 open Expenses:Food
2026-01-01 open Expenses:Transport
2026-01-01 open Income:Salary

2026-05-19 * "Daily expenses"
  Expenses:Transport    2,000.00 NGN
  Expenses:Food         5,000.00 NGN
  Assets:Cash
```

The last line with no amount is the balancing entry — rustledger fills it in automatically.

## Validating the Files

Before doing anything with a ledger file, run the check command:

```bash
rledger check personal_2026.bean
```

Rustledger gives precise error messages with line numbers. Common issues when starting out:

- **Account never opened** — you used an account in a transaction before declaring it with an `open` directive
- **Transaction does not balance** — debits and credits don't add up
- **Wrong currency** — a typo like `NGM` instead of `NGN`

I had all three when cleaning up my 2025 files. The error output is clear enough that fixing them is straightforward.

## My Setup

I maintain two separate files:

**`personal_2026.bean`** — daily personal expenses, salary, passive income, and an envelope budgeting system where I allocate cash to sub-accounts (food, transport, airtime, etc.) at the start of each week.

**`business_2026.bean`** — my Korope transport business. Daily income, fuel, driver salary, repairs, and a weekly profit allocation policy: 40% owner salary, 35% retained earnings, 15% emergency fund, 10% savings.

A third file `main.bean` just includes both:

```
include "personal_2026.bean"
include "business_2026.bean"
```

This is the file the MCP server points to, so the agent can query across both contexts in one call.

## What's Next

The real unlock is connecting rustledger to my AI agent via the MCP server. Instead of manually editing bean files, I tell Joe what I spent during the day and he records it, validates the files, and commits to git. The ledger stays accurate without any manual formatting work on my end.

That setup — and what it actually looks like in practice — is what the next post will cover.