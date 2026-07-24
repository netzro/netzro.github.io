Title: Setting Up Pass as My Password Manager
Date: 2024-08-15
Tags: 100daystooffload, linux
Summary: A guide to setting up Pass, a lightweight Unix password manager, on a Linux environment (Termux) and syncing with GitHub.

Managing passwords without a dedicated password manager is challenging. Having been online for decades, I’ve used countless websites and services—email, banking, forums, and chat platforms—all requiring unique credentials.

Remembering usernames and passwords is tough, so I used to rely on similar passwords across platforms, a practice I **strongly** advise against. Previously, I depended on browser-built-in password managers and Google services (on my Android smartphone). Once I created login credentials, the browser would save them and autofill them on return visits, eliminating the need to memorize them.

Today, I explored password managers and chose **Pass**, a simple, lightweight, and minimalistic Unix password manager. In this post, I’ll document my workflow for setting up Pass on my Linux environment (Termux) and Android smartphone.

## Generating a GPG Key

First, I installed GnuPG and generated a GPG key:

```bash
pkg install gnupg
gpg --full-generate-key
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