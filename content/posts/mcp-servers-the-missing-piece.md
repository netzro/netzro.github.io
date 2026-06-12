Title: MCP Servers: The Missing Piece in AI Agent Development
Date: 2026-05-19
Author: Gifted
Category: Tech
Tags: ai, python, technology
Slug: mcp-servers-the-missing-piece
Summary: What MCP servers are, why they matter, and how I use them to extend my AI agents.
Status: published

If you've been building AI agents for any length of time, you've probably hit the same wall I did — the model is smart, but it can't actually *do* anything without you wiring up every tool by hand. That's where MCP servers changed everything for me.

## What Is MCP?

MCP stands for Model Context Protocol. It's an open standard that defines how AI models communicate with external tools and services. Think of it as a universal plug — instead of building a custom integration every time you want your agent to talk to a new service, you build one MCP server and any compliant agent can use it.

The architecture is simple. An MCP server exposes a list of tools — functions with names, descriptions, and typed parameters. The agent discovers these tools at startup, and when it decides to use one, it sends a structured JSON call. The server executes the logic and returns a result. That's the entire contract.

## Why It Matters

Before MCP, every agent framework had its own tool format. LangChain tools looked different from AutoGen tools, which looked different from whatever you cobbled together yourself. Switching frameworks meant rewriting everything.

MCP breaks that coupling. The server doesn't know or care what agent is calling it. The agent doesn't know or care what language the server is written in. I've built servers in Python using FastMCP and connected them to nanobot, and the only thing that matters is that the stdio transport speaks the protocol correctly.

## How I Build Them

My stack is straightforward. Every MCP server I build follows the same pattern:

```python
from __future__ import annotations

import logging
logging.getLogger("mcp").setLevel(logging.WARNING)

from contextlib import asynccontextmanager
from fastmcp import FastMCP

@asynccontextmanager
async def lifespan(app: FastMCP):
    # initialise resources here
    yield
    # cleanup here

mcp = FastMCP("server-name", lifespan=lifespan)

@mcp.tool()
async def my_tool(param: str) -> str:
    """Description the agent reads to decide when to use this tool."""
    return "result"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

A few things I've learned the hard way:

**Never instantiate async clients at module level.** httpx, aiohttp, database connections — all of these need to live inside the lifespan context manager. If you put them at module level, they break in proot environments and cause hard-to-debug event loop errors.

**Tool descriptions are everything.** The agent reads the docstring to decide whether to call your tool. A vague description means your tool gets ignored. Be specific — include what the tool does, what parameters it expects, and when to use it.

**Return strings, not JSON.** Some agent frameworks double-decode JSON strings and crash. Return plain text or use `json.dumps()` only when you need structured output that the agent will parse.

## My Current Stack

Right now I'm running several MCP servers connected to my main agent:

**portfolio_mcp** — 16 tools for tracking my Nigerian and US stock positions. Reads from local SQLite databases updated by my scrapers. The agent can pull real-time P&L, dividend history, and compare performance across both markets.

**news_mcp** — 6 tools that scrape Nigerian news sources. Gives the agent current headlines filtered by relevance to my holdings.

**gmail_mcp** — 35 tools wrapping the Gmail API. Full email management — read, compose, label, search.

**agentmail** — 11 tools for agent-to-agent email via AgentMail. Useful for async tasks where I want the agent to send itself a reminder or receive external triggers.

The combined tool count matters — Groq's API has a hard limit of 128 tools per request. Exceed that and every call fails silently. I learned this by adding one server too many and spending an hour debugging what looked like an unrelated rate limit error.

## The Workflow

Adding a new MCP server to an agent takes about 20 minutes now that I have the pattern down:

1. Create the project directory with `uv init --no-workspace`
2. Add `fastmcp`, `httpx`, and `loguru` with `uv add`
3. Write `server.py` with the tools
4. Test with a minimal stdio client before wiring it to the agent
5. Add the server config to `config.json`

The config entry is just a command and arguments:

```json
"my_server": {
  "command": "uv",
  "args": ["--directory", "/path/to/server", "run", "server.py"]
}
```

The agent handles the rest — spawns the process, initialises the connection, and makes the tools available.

## What's Next

The protocol is still young. Right now MCP is primarily stdio-based, which means each server is a subprocess. HTTP transport is coming and will open up remote servers, shared tool registries, and proper multi-agent architectures where agents expose tools to each other.

For now though, stdio is more than enough. My agent wakes up, connects to seven servers, loads over 100 tools, and is ready to manage my portfolio, check my inbox, and publish blog posts — all from a phone running Debian in Termux.

That's the thing about MCP. It's not glamorous infrastructure. It's just a clean protocol that lets your agent actually touch the world.
