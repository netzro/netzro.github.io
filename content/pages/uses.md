Title: Uses
Date: 2026-06-12

# Uses
_last updated 12th June, 2026_

## My Daily Driver Setup

I do not own a laptop. Everything runs from an Android phone through Termux.

### Hardware
- Android phone with Termux installed (F-Droid version, not Play Store)
- 128 GB storage, 4 GB RAM
- No desktop or laptop — the phone is the computer

### Core Stack
- **Termux** — Linux terminal emulator, the foundation of everything
- **proot-distro** — runs a full Debian environment without root
- **uv** — Python package management with UV_LINK_MODE=copy
- **Git + SSH** — version control and GitHub access

### What I Run
- **Hermes Agent** — personal AI agent with WebUI and Telegram bot
- **OmniRoute** — LLM routing through free API tiers (Claude Sonnet 4.5 via Kiro)
- **ngx-portfolio** — CLI + MCP server for tracking my NGX stock portfolio
- **Cron jobs** — daily backups, price refreshes, document organization
- **Python** — all tooling, scripts, and automation

### Software I Use
- **Termux** — Linux environment
- **Acode** — code editor
- **Markor** — Markdown editor
- **Feeder** — RSS reader
- **Via** — lightweight browser

### Principles
- Zero-cost: free API tiers only
- Phone-first: everything runs on Android
- Private: self-hosted, private repos, no cloud dependency for core services
- Minimal: every package justified, every service monitored
