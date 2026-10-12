Title: Understanding the Linux File System — Part 2: Inodes, Links, and Permissions
Date: 2026-10-12
Time: 10:00
Author: Gifted
Tags: linux, filesystem, tutorial
Slug: understanding-linux-file-system-part-2-inodes-links-permissions
Summary: Inodes, hard vs soft links, and the rwx permission model — the parts of the Linux filesystem that Part 1 only walked past.
---

# Understanding the Linux File System — Part 2: Inodes, Links, and Permissions

In [Part 1](https://netzro.github.io/posts/2026/Sep/23/understanding-linux-file-system-part-1-structure-walkthrough/) I walked the directory tree: what lives in `/etc`, why `/proc` isn't real storage, where your logs go. This part goes underneath the tree.

Because the tree is a lie of convenience. A directory is not a container holding your files. It's a list of names mapped to numbers, and those numbers point somewhere else entirely. Once that clicks, links and permissions stop being trivia and start being obvious.

## What an inode actually is

Every file on a Linux filesystem has an **inode**: a numbered record holding everything about the file except its name and its contents.

```bash
$ ls -li demo.txt
4033239 -rw-------. 1 u0_a362 u0_a362 6 Oct 11 09:21 demo.txt
```

That leading `4033239` is the inode number. Ask for it directly:

```bash
$ stat -c '%n inode=%i links=%h type=%F' demo.txt
demo.txt inode=4033239 links=1 type=regular file
```

The inode stores the file's size, owner, group, permission bits, timestamps, and the pointers to where the actual data blocks live on disk. What it does **not** store is the filename. The name lives in the directory, as an entry pointing at the inode.

So the mental model is:

```
directory entry  ──►  inode  ──►  data blocks
   "demo.txt"         4033239       (on disk)
```

That separation is the whole reason links exist, and the whole reason `rm` doesn't always delete your data.

## Hard links: two names, one inode

A hard link is a second directory entry pointing at the same inode. On a normal Linux system:

```bash
$ ln demo.txt hardlink.txt
$ ls -li demo.txt hardlink.txt
4033239 -rw-------. 2 u0_a362 u0_a362 6 Oct 11 09:21 demo.txt
4033239 -rw-------. 2 u0_a362 u0_a362 6 Oct 11 09:21 hardlink.txt
```

Same inode number. Same data. The link count went from 1 to 2, which is what that third column means.

This is why deleting a hard-linked file doesn't destroy the data:

```bash
$ rm demo.txt
$ cat hardlink.txt
hello
```

`rm` removed one *name*. The inode still has a link count of 1, so the data stays. The kernel only frees the blocks when the link count hits zero and nothing has the file open.

Two consequences worth knowing: hard links can't cross filesystems, because an inode number is only unique within its own filesystem. And you generally can't hard-link a directory, because that would let you build a loop in the tree.

**A caveat on that block above.** I couldn't run it on the machine I write these posts from. Termux on Android returns `Permission denied` for `ln` without `-s`, because app storage here is f2fs under SELinux, which blocks hard links for app processes. The behaviour I've described is standard Linux and it's what you'll see on any normal distro, but that transcript is from the manual, not from this phone. I'd rather flag it than let it pass as something I ran.

## Soft links: a name pointing at a name

A symbolic link (symlink) is a different animal. It's its own file, with its own inode, whose *contents* are a path.

```bash
$ ln -s demo.txt symlink.txt
$ ls -li demo.txt symlink.txt
4033239 -rw-------. 1 u0_a362 u0_a362 6 Oct 11 09:21 demo.txt
4033289 lrwxrwxrwx. 1 u0_a362 u0_a362 8 Oct 11 09:21 symlink.txt -> demo.txt
```

Different inode. The `l` at the start of the permissions marks it as a link, and the `->` shows where it points.

The practical difference: a symlink stores a *path*, not an inode. So it can cross filesystems, and it can point at something that doesn't exist. That second property is what makes broken links possible:

```bash
$ ln -sf /nonexistent/target broken.lnk
$ cat broken.lnk
cat: broken.lnk: No such file or directory
```

The link itself is perfectly valid. It just points nowhere. `ls -l` still shows it:

```bash
$ ls -l broken.lnk
lrwxrwxrwx. 1 u0_a362 u0_a362 19 Oct 11 09:22 broken.lnk -> /nonexistent/target
```

Symlinks also chain. Point a link at a link and reading it follows the whole path:

```bash
$ ln -s orig.txt link1
$ ln -s link1 link2
$ cat link2
data
$ rm orig.txt
$ cat link2
cat: link2: No such file or directory
```

Remove the real file and the entire chain collapses, because every link in it is just a path that no longer resolves.

## Permissions: who can do what

Every inode carries nine permission bits, in three groups of three:

```
-rwxr-xr-x
 │││ │││ │││
 │││ │││ └┴┴── others
 │││ └┴┴───── group
 └┴┴──────── owner
```

Each group is `r` (read), `w` (write), `x` (execute). For files, `x` means "can be run as a program." For directories, it means something different: **`x` is the right to traverse into the directory.** A directory you can read but not traverse lets you list names and nothing else.

Each group is really a three-bit number, which is where the octal notation comes from. Here's the table, verified on this machine:

```bash
$ for m in 777 755 644 600 400; do printf 'x' > p.tmp; chmod $m p.tmp
    printf "  %s -> %s\n" "$m" "$(stat -c '%A' p.tmp)"; done
  777 -> -rwxrwxrwx
  755 -> -rwxr-xr-x
  644 -> -rw-r--r--
  600 -> -rw-------
  400 -> -r--------
```

The four you'll actually type:

- **755** — owner can read, write, execute; everyone else can read and execute. Directories, scripts, anything executable.
- **644** — owner reads and writes; everyone else only reads. Documents, configs, most files.
- **600** — owner only. Private keys, tokens, anything secret.
- **400** — read-only, even for the owner. Rare, but it's the "don't touch this" bit.

The execute bit is not decoration. Watch what happens without it:

```bash
$ chmod 644 e.sh
$ ./e.sh
bash: ./e.sh: Permission denied
$ chmod 755 e.sh
$ ./e.sh
ran
```

A file with `rw` and no `x` is just text. You can read it all day, but the kernel won't execute it. That's the entire difference between a script and a document.

## Where new file permissions come from

When you create a file, the permissions aren't chosen by the app — they're the result of a mask called `umask`:

```bash
$ umask
0077
```

`umask` lists the bits to *remove* from the default. On this machine it's `0077`, so group and others get nothing, and every new file lands at `600`. On a typical desktop `umask` is `022`, giving new files `644` and new directories `755`.

That's why the same script behaves differently on two machines: the code is identical, but `umask` decided what the file could do when it was created.

## Why inodes can run out

Disk space and inodes are counted separately. A filesystem has a fixed number of inodes, set when it was created, and a file consumes one regardless of its size.

```bash
$ df -i /data
Filesystem         Inodes   IUsed   IFree IUse% Mounted on
/dev/block/dm-59 12354048 9128412 3225636   74% /data/user/0
```

74% of the inodes on this device are gone while there's still free space. That's normal here — Android app storage is millions of tiny files — but it's the classic failure mode elsewhere: a mail queue or a cache directory fills up with millions of empty files, `df -h` reports plenty of room, and every write fails with "no space left on device." The space isn't the problem. The inode table is.

## Personal Note

Part 1 was about navigating the tree. This part is about what the tree is made of, and it changed how I read `ls -l` output. That leading inode number used to be noise. Now it's the first thing I check when two files look identical but behave differently, because identical-looking names with different inodes are two different files, and identical inodes are two names for one file.

The filename is not the file. The name is a label in a directory pointing at a numbered record, and almost every surprising thing about Linux file behaviour follows from that one fact.

*Go back to [Part 1](https://netzro.github.io/posts/2026/Sep/23/understanding-linux-file-system-part-1-structure-walkthrough/) for the directory tree walkthrough.*
