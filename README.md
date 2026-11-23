# netzro.github.io

Pelican static site published to GitHub Pages at https://netzro.github.io.

## Changelog

- 2026-11-23 — Added `pelican-plugins/sitemap.py`, a minimal sitemap generator for Pelican 4.12 (which has no built-in one). The previous `pelican-plugins/sitemap` was a 0-byte placeholder: the build logged "Cannot load plugin `sitemap`" and produced no sitemap, while `robots.txt` advertised `/sitemap.xml` — a live 404 and a likely cause of Search Console's "Not found (404)" indexing notice. Scratch build now succeeds with no plugin error and emits a 96-URL sitemap; every URL checked returned HTTP 200. Source fix only — deployment to gh-pages is a separate, approved step.
