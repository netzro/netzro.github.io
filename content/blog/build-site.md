---
title: Building My Site/Blog
date: 2024-08-09 12:15am
tag: pelican
category: python
---

Today, I successfully set up this site/blog.

As a Python enthusiast, I used Pelican, a static site generator, to create and deploy this site/blog to GitHub Pages.

The process was both fun and informative, and I'll be documenting it here.

To get started, you'll need the following:

1. A GitHub account.
2. A Linux environment (I used Termux on my phone since I don't have a laptop).
3. Python installed.

Let's begin by creating a repository on GitHub named:

```
<username>.github.io
```

Initialize it with a `.gitignore` file that includes the following entries:

```
venv/
output/
```

Next, create two branches:

```
master
```

```
gh-pages
```

In the repository settings, go to Pages and set `gh-pages` as the branch to serve your static files.

In your Linux environment, clone the repository you just created:

```
git clone <URL>
```

Navigate into the newly cloned repository and create a virtual environment:

```python
python -m venv venv
```

Activate it with:

```
source venv/bin/activate
```

Now, it's time to install Pelican. Run the following command:

```
pip install pelican markdown tzdata ghp-import
```

To save your dependencies, run:

```
pip freeze > requirements.txt
```

That's all for today. In the next post, we'll generate our site and publish it to GitHub Pages.
