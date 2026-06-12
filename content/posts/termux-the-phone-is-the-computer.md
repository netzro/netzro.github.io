Title: Termux — The Phone Is The Computer
Date: 2026-06-12
Author: Gifted
Category: Technology
Tags: termux, android, linux, development, mobile
Slug: termux-the-phone-is-the-computer
Summary: How I run a full development environment from an Android phone — and why you might want to.

---

I do not own a laptop. Everything I build — agents, portfolio trackers, blog pipelines, cron jobs — runs from a phone. Not a "phone as a thin client" setup. The phone is the computer.

The tool that makes this possible is [Termux](https://termux.dev).

## What Termux Is

Termux is a Linux terminal emulator for Android. Not a VM. Not a chroot running in the background. It gives you a real shell, a real package manager (`apt`), and a real filesystem — all running directly on the Android kernel.

No root required. No USB debugging. No developer mode. Install from F-Droid, open the app, and you have a Debian-like environment in your pocket.

That is the pitch. The reality is even better.

## What I Run on It

My daily stack looks like this:

- **Hermes Agent** — my personal AI agent, serving a WebUI and Telegram bot
- **OmniRoute** — routing Claude Sonnet 4.5 through free API tiers
- **ngx-portfolio** — a CLI and MCP server tracking my NGX stock portfolio
- **Cron jobs** — daily backups, price refreshes, document organization
- **Python tooling** — managed entirely through `uv` with `UV_LINK_MODE=copy`
- **Git** — pushing to private GitHub repos over SSH

All of this runs on a device I bought for NGN 85,000.

## The Setup That Matters

Termux out of the box is bare. The magic is in the configuration.

First, the essentials:

```bash
pkg update && pkg upgrade
pkg install git python openssh curl wget
```

Then `uv`, which I use instead of pip:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

I set `UV_LINK_MODE=copy` in my `.bashrc` because symlinks behave oddly on Android's filesystem:

```bash
echo 'export UV_LINK_MODE=copy' >> ~/.bashrc
```

For my work, I also run a proot Debian environment. This gives me a full Debian filesystem without root:

```bash
pkg install proot-distro
proot-distro install debian
proot-distro login debian
```

Inside proot, it is a standard Debian system. `apt install` works. `systemctl` does not (no systemd without root), but everything else does. I keep my projects at `/root/projects` inside proot, which maps to `~/projects` in Termux.

SSH access is critical. I use it to push to GitHub, pull configs, and occasionally tunnel into other services. Setting up keys is the first thing I do on any fresh install:

```bash
ssh-keygen -t ed25519 -C "termux"
cat ~/.ssh/id_ed25519.pub
```

That public key goes straight into GitHub, and then the phone is a first-class git citizen.

## Why Not Just Buy a Laptop?

I get this question often. The answer is simple: constraints drive creativity.

A laptop gives you 16 GB of RAM, a full desktop environment, and zero battery anxiety. It also gives you excuses. You install things you do not need. You configure services you forget about. You accumulate digital weight.

A phone forces discipline. Every package I install, I justify. Every service I run, I monitor. The battery constraint alone keeps me honest — if something is wasteful, I notice when my phone dies at 2 PM.

There is also the portability argument. My phone is always in my pocket. A laptop is in my bag, which is in my car, which is parked somewhere. The computer that is always with you beats the computer that is sometimes with you.

## The Real Limitations

I will not pretend this is perfect.

**Screen real estate** is the obvious one. I do most of my work through Telegram notifications and the Hermes WebUI. When I need a full terminal, I am on the phone screen. It works. It is not comfortable for long sessions.

**Android kills background processes.** This is the biggest pain point. Termux can be killed when the system reclaims memory. I mitigate this with `termux-wake-lock` and by keeping services lightweight. But if you are running something that must stay alive 24/7, test it first.

**No hardware acceleration.** If your workflow involves GPU compute, this is not your machine. I do not train models. I run agents, scripts, and web scrapers. All CPU-bound. All fine.

**Storage is limited.** My phone has 128 GB. I offload media to cloud storage and keep the local filesystem lean. This is actually a feature — it forces me to treat the phone as a compute device, not a storage dump.

## The Philosophy

There is a deeper point here. The tech industry wants you to believe you need more. More RAM, more cores, more devices. A MacBook Pro. A cloud server. A homelab rack.

But the most sovereign computer is the one you already own. It does not depend on a cloud provider. It does not depend on a landlord's electricity. It runs on a battery, in your pocket, and the software is free.

Termux is not a toy. It is not a "mobile development environment." It is a real Unix system that happens to run on the device in your pocket. And for the kind of work I do — writing, scripting, automating, investing — it is enough.

More than enough.

## Getting Started

If you want to try this, here is the minimal path:

1. Install Termux from [F-Droid](https://f-droid.org/packages/com.termux/) — not the Play Store version (it is outdated)
2. Run `pkg update && pkg upgrade`
3. Install what you need: `pkg install git python openssh`
4. Set up SSH keys for GitHub: `ssh-keygen -t ed25519`
5. Start building

You do not need to replicate my setup. You need to find what works for you. The point is not that a phone can replace a laptop. The point is that you might not need the laptop in the first place.

---

*I run Hermes, OmniRoute, and a handful of cron jobs from a Termux session on Android. If you want to see what a phone-first development setup looks like in practice, the configs are on my GitHub.*
