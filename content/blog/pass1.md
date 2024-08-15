---
title: Setting Up Pass as My Password Manager
date: 2024-08-15
tags: #100DaysToOffload, linux
---

Managing passwords without a dedicated password manager can be a challenge. Having been online for decades, I've encountered countless sites and services requiring passwords—ranging from email services and banking sites to forums and chat platforms.

Remembering all these usernames and passwords is difficult, so I used to rely on using the same or similar passwords across different platforms—a practice I **strongly** advise against. However, I often defaulted to using built-in password managers in browsers and Google services (on my Android smartphone). Typically, once I created login credentials, I would let the browser save them to its database and autofill them whenever I revisited the site, eliminating the need to remember them.

Today, I decided to explore how a password manager works. I've heard of 1Password, Bitwarden, etc., but I wanted something simple, lightweight, and minimalistic. After some research, I settled on "Pass," which is often touted as the default password manager for Unix.

In this post, I will document my workflow for setting up Pass on my Linux environment (Termux) and Android smartphone.

### Generating a GPG Key

First, I generated a GPG key:

```bash
pkg install gnupg
gpg --gen-key
```

Setting Up Pass

```bash
pkg install pass
pass --version
pass init <gpg-id>
pass git init
```

Add some passwords to Pass.

```bash
pass insert <test.com>
```

Create a private repository on GitHub.

Pull and push your Pass store to GitHub:

```bash
pass git pull remote origin <repo-url> <branch>
pass git push remote origin <repo-url> <branch>
```

In a future post, we’ll explore how to install Android Password Store and set it up as my primary password manager instead of relying on Google.