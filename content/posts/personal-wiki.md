Title: I Built a Personal Wiki That Thinks for Me
Date: 2026-06-14
Author: Gifted
Category: Dev
Tags: wiki, automation, knowledge-base, markdown, github, llm
Slug: personal-wiki
Summary: A personal wiki with an agent schema that ingests my notes, answers queries, and self-audits — all in plain markdown, all in git.

---

I have 138 files scattered across my notes directory — 123 of them markdown, the rest shell scripts, Python, JSON, CSV, and a couple of Bean text files. Investing tips, AI observations, business ideas, personal growth notes — all raw, none of it connected. I wanted a system that could ingest those notes, build structured knowledge pages, and answer questions from them. So I built one.

The result is `personal-wiki`: a git-tracked markdown wiki designed to be maintained by my AI agent.

## The Idea

The wiki is just three directories:

- `raw/` — a symlink to my existing notes folder. Never modified.
- `wiki/` — LLM-maintained knowledge pages, one topic per file.
- `index.md` — a flat catalog of every wiki page.
- `log.md` — append-only history of every ingest and query.

No database. No web frontend. No dependencies. Just markdown and git.

## How It Works

The project is configured with a set of instructions that tells my agent what to do:

**Ingest** — `ingest: [file or topic]`

When I point it at a source file, the AI reads the content, extracts key facts, creates or updates wiki pages, updates the index, and appends a log entry with timestamp and summary.

**Query** — `query: [question]`

The agent reads the index first to find candidate pages, then reads the relevant wiki pages, synthesises an answer, saves that answer as a new wiki page, and logs the interaction.

**Lint** — `lint wiki`

A self-audit pass. Checks for orphan pages (in wiki/ but not in index), contradictions across overlapping topics, stale entries older than 90 days, and missing cross-links between related pages.

Every wiki page follows a simple template — title, summary, key points, details, related links, source reference, and last-updated date. Consistent structure makes the linting pass possible.

## Scaffolding It

The whole thing took a few minutes. I told my AI what I wanted — directory structure, symlink, index, log — and it did the rest: created the directories, wrote the schema, committed, created a private GitHub repo, and pushed.

The project now lives at `~/projects/personal-wiki` with a private remote on GitHub.

## What Makes This Useful

I was tempted to reach for a vector database, or a fancy knowledge graph tool. But the constraint of "markdown only, git-tracked" turned out to be a feature.

Every wiki page is a plain text file. I can read it in any editor, diff it, grep it, or edit it manually. History is automatic because it's git. The knowledge base is portable — clone the repo and you have everything.

The AI does the hard work of reading messy source notes and distilling them into structured pages. I get to keep everything in a format I fully control.

## Next Steps

Right now the wiki is empty — no pages yet. The plan is to run a few `ingest` passes over my existing notes, let the AI build out the knowledge base, and then start using `query` to cross-reference ideas I've written months apart.

I also want to add a nightly cron job that runs `lint wiki` and reports any issues — orphans, stale pages, missing links. Keep the base clean without manual effort.

And eventually, I might add a lightweight static site generator on top so I can browse the wiki in a browser. But for now, markdown in a terminal is enough.

---

The source is on GitHub (private repo `netzro/personal-wiki`). The whole thing is fewer than 200 lines of markdown. Sometimes the best tool is the simplest one.
