Title: Understanding the Linux File System — Part 1: Structure Walkthrough
Date: 2026-09-23
Time: 09:17
Author: Gifted
Tags: linux, filesystem, tutorial
Slug: understanding-linux-file-system-part-1-structure-walkthrough
Summary: A hands-on walkthrough of the Linux filesystem hierarchy — what lives where, why it matters, and how to explore it yourself.

# Understanding the Linux File System — Part 1: Structure Walkthrough

Linux keeps everything under one root — `/`. No drive letters, no `C:` or `D:`. Every storage device, every file, every configuration lives somewhere under this single tree. Once you get the layout, navigating any Linux system feels obvious.

## The Root Directory `/`

Everything starts here. `/` is not your home directory — it's the top of the entire filesystem. Disks, partitions, and virtual filesystems all branch off from here.

```bash
ls /
```

You'll see the standard directories that make up the Filesystem Hierarchy Standard (FHS). Each one below.

## `/bin` — Essential User Commands

Binaries every user needs, even in single-user mode. `ls`, `cp`, `mv`, `cat`, `grep`, `bash` — all here. Statically linked or depending only on `/lib`, so they work even if other filesystems aren't mounted.

```bash
ls /bin | head -20
# cat /bin/bash     # don't do this, it's binary
```

## `/etc` — Configuration

"Et cetera" — and that's roughly what lives here. Network settings (`/etc/network/`), user accounts (`/etc/passwd`, `/etc/shadow`), cron jobs (`/etc/crontab`), hostname (`/etc/hostname`).

```bash
cat /etc/hostname
cat /etc/passwd | head -5
```

> ⚠️ `/etc/passwd` is world-readable. Password hashes live in `/etc/shadow`, root-only. I still get nervous `cat`-ing it on production boxes.

## `/home` — User Directories

Each non-root user gets a folder here: `/home/gifted`, `/home/alice`, etc. Personal files, dotfiles (`.bashrc`, `.vimrc`), local configs. Backing up `/home` is the #1 rule — it's the only part most users care about. I learned this the hard way.

```bash
ls /home
du -sh /home/*     # disk usage per user
```

## `/var` — Variable Data

Things that grow: logs (`/var/log/`), mail queues (`/var/mail/`), package caches (`/var/cache/`), www roots (`/var/www/`). Disk full? Check `/var/log` first — syslog silently eats gigabytes. Happened to me more times than I'd like to admit.

```bash
du -sh /var/log/* | sort -h | tail -10
journalctl --disk-usage    # systemd log size
```

## `/proc` — Process & Kernel Info

Not a real filesystem — virtual, maintained by the kernel. Each process gets a numeric directory: `/proc/1234/` holds status, open files, memory map, cmdline.

```bash
ls /proc | grep '^[0-9]' | head -10   # list PIDs
cat /proc/1/cmdline                   # PID 1's command
cat /proc/meminfo                     # memory stats
cat /proc/cpuinfo                     # CPU details
```

## `/sys` — Device & Kernel Parameters

Also virtual. Kernel data about hardware: USB devices, block devices, power management. A device tree you can browse.

```bash
ls /sys/block/          # block devices
ls /sys/class/net/      # network interfaces
cat /sys/class/net/eth0/address   # MAC address
```

## `/dev` — Device Files

Everything is a file — including hardware. `/dev/sda` is your first disk, `/dev/tty` is your terminal, `/dev/urandom` gives random bytes, `/dev/null` discards anything written to it.

```bash
ls /dev/sd*            # storage devices
ls /dev/tty*           # terminals
echo "hello" > /dev/null   # silently discards
```

## The Big Picture

```
/
├── bin/          → essential commands
├── etc/          → system config
├── home/         → user data
├── var/          → logs, caches, queues
├── proc/         → process & kernel info (virtual)
├── sys/          → device & hardware info (virtual)
├── dev/          → device files
├── tmp/          → temporary files (cleared on reboot)
├── usr/          → installed software, libraries, docs
├── opt/          → optional third-party software
├── boot/         → kernel, initramfs, bootloader
├── lib/          → shared libraries
├── sbin/         → admin binaries (root-only)
├── root/         → root user's home
├── run/          → runtime data (PIDs, sockets)
└── mnt/ / media/ → mount points for removable media
```

## Personal Note

Coming from Android/Termux, the `/` tree feels familiar in spirit — Termux has its own isolated filesystem at `/data/data/com.termux/files/home/` — but the full Linux hierarchy is a different beast. `/proc` and `/sys` are windows into the kernel, not real storage. That mental model explains why `cat /proc/meminfo` works even when your disk is full.

Part 2 tomorrow: inodes, hard vs soft links, permissions (`rwx`), and the FHS in depth.