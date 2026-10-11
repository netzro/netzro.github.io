---
Title: Exit Codes: The Numbers Your Terminal Won't Show You
Date: 2026-10-11
Time: 06:35
Author: Gifted
Tags: bash, linux, python, programming, tutorial
Slug: exit-codes
Summary: A practical guide to exit codes — what 0, 1, 2, 126, 127 and 128+N actually mean, why 75 and 78 matter, and how to use them in your own scripts.
---

# Exit Codes: The Numbers Your Terminal Won't Show You

Every command you run ends by handing your shell a number. Almost nobody looks at it, which is a shame, because when something fails silently that number is usually the only witness.

## The one rule everything follows

Zero means success. Anything else means failure.

That convention is backwards from how most languages treat numbers. In C, `0` is false; here, `0` means everything is fine.

You've been seeing this number all along, whether you noticed it or not. It lives in a shell variable called `$?`:

```bash
$ true
$ echo $?
0
$ false
$ echo $?
1
```

`$?` only holds the last command's status. It gets overwritten by the very next thing you run, including the `echo` you used to print it. That's why you save it immediately if you need it:

```bash
$ ls /nonexistent
ls: cannot access '/nonexistent': No such file or directory
$ code=$?
$ echo "exit was $code"
exit was 2
```

## The codes you'll actually meet

Here's what I see day to day, all verified on this machine:

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | General error, the catch-all |
| `2` | Misuse of a shell builtin (bad option, missing argument) |
| `126` | Command found, but not executable |
| `127` | Command not found |
| `130` | Terminated by Ctrl-C |
| `128+N` | Killed by signal N |

The difference between 126 and 127 is worth internalising:

```bash
$ nonexistent-command-xyz
sh: nonexistent-command-xyz: not found
$ echo $?
127

$ printf '#!/bin/sh\necho hi\n' > script.sh
$ chmod 644 script.sh      # readable, but not executable
$ ./script.sh
sh: ./script.sh: Permission denied
$ echo $?
126
```

127 means "I couldn't find it." 126 means "I found it, but it won't run." If a script works for you and fails on a server, that distinction is often the whole answer. A file that lost its execute bit during a copy gives you 126, not 127.

## 128+N: the signal convention

When a process is killed by a signal rather than exiting on its own, the shell reports `128 + signal_number`. The three you'll meet most:

- `130` = 128 + 2, SIGINT. You pressed Ctrl-C.
- `143` = 128 + 15, SIGTERM. Something asked it to stop politely.
- `137` = 128 + 9, SIGKILL. Something killed it outright.

That last one matters if you've ever had a process vanish on a small machine. 137 usually means the kernel's out-of-memory killer decided your process was the problem.

There's a trap here. Python reports signals differently. Where the shell says 143, Python's `subprocess` says `-15`:

```python
>>> import subprocess
>>> r = subprocess.run(['sh', '-c', 'kill -TERM $$'])
>>> r.returncode
-15          # shell would have shown 143
```

A negative value means "died from signal N." If you're checking for a signal death in Python and comparing against 143, you'll never match it.

## Going past 255, or not

An exit code is a single byte. The range is 0 to 255, and anything outside wraps around modulo 256:

```bash
$ sh -c 'exit 256'
$ echo $?
0            # 256 % 256 = 0
$ sh -c 'exit 257'
$ echo $?
1            # 257 % 256 = 1
```

Python behaves the same way, which is a genuine footgun:

```bash
$ python3 -c "import sys; sys.exit(300)"
$ echo $?
44           # 300 % 256
$ python3 -c "import sys; sys.exit(-1)"
$ echo $?
255
```

So `sys.exit(-1)` doesn't mean "error" in any special sense. It means 255. If you want a distinguishable failure code, pick a small positive number.

## The convention most people never hear about

There's an older, more expressive set of codes from BSD's `sysexits.h`. Almost nothing uses them by default, but they earn their keep when you're writing something a supervisor will restart, because they let you say why it failed and whether retrying could possibly help.

I use them in a trading bot I've been building. Four codes cover everything it needs to communicate:

```python
EX_OK     = 0    # success
EX_ERROR  = 1    # crash / repeated errors: restart with backoff
EX_LOCKED = 75   # another instance holds the lock: do NOT thrash
EX_CONFIG = 78   # bad config / secrets / corrupt state: restarting cannot help
```

The two interesting ones are 75 and 78.

75 (EX_TEMPFAIL) means "temporary failure, try again later." When my bot starts a second time while the first is still running, it exits 75. The supervisor reads that and knows not to hammer it, because another instance is already alive and restarting is pointless.

78 (EX_CONFIG) means the configuration is wrong. A missing API key, an unreadable state file, a typo in a config option. This one is the most valuable of the lot, because it tells the supervisor to stop trying. Restarting a process with a broken config produces the same failure in a loop, forever, burning resources and filling logs.

If a supervisor is going to restart your program, your exit codes are how you tell it whether that's a good idea. Zero and a generic 1 don't carry that information. 75 and 78 do.

## Using them in your own scripts

In bash, `exit N` sets the code. In Python, `sys.exit(N)` raises `SystemExit`, which the interpreter turns into the process code:

```bash
$ python3 -c "import sys; sys.exit(75)"
$ echo $?
75
```

`SystemExit` with a string is a special case. It prints the message and exits 1, not the number:

```bash
$ python3 -c "raise SystemExit('something went wrong')"
something went wrong
$ echo $?
1
```

If you want a specific code, pass an integer. If you want a message on stderr, print it yourself and then exit with the code.

One more habit worth adopting:

```bash
#!/bin/bash
set -euo pipefail
```

`-e` makes the script exit the moment any command fails, using that command's code. Without it, a failing step in the middle gets ignored and the script reports success at the end. That's the worst outcome, because it looks like it worked.

## Wrapping up

Exit codes are a small, boring, useful protocol. Zero is success, everything else is a reason. The signal range starts at 128. The range is one byte, so it wraps. And the sysexits values, particularly 75 and 78, are how a program explains itself to whatever is supervising it.

Next time a script fails without saying why, check `$?` before you change anything. It's probably already told you.
