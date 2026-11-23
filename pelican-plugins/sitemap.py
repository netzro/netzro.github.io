"""Minimal sitemap generator for netzro.github.io.

Replaces the broken empty `sitemap` plugin file. Pelican 4.12 has no built-in
sitemap, so this writes sitemap.xml from the finished article and page list.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from pelican import signals


def generate_sitemap(generators):
    settings = generators[0].settings
    siteurl = (settings.get("SITEURL") or "").rstrip("/")
    if not siteurl:
        return  # dev builds with no SITEURL: no sitemap, no bad URLs

    contents = []
    for generator in generators:
        contents.extend(getattr(generator, "articles", None) or [])
        contents.extend(getattr(generator, "pages", None) or [])

    entries = []
    for content in contents:
        url = getattr(content, "url", None)
        if not url:
            continue
        loc = f"{siteurl}/{url.lstrip('/')}"
        line = f"  <url><loc>{escape(loc)}</loc>"
        modified = getattr(content, "modified", None) or getattr(content, "date", None)
        if modified is not None:
            line += f"<lastmod>{modified.strftime('%Y-%m-%d')}</lastmod>"
        entries.append(line + "</url>")

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    output = Path(settings.get("OUTPUT_PATH", "output"))
    (output / "sitemap.xml").write_text(xml, encoding="utf-8")


def register():
    signals.all_generators_finalized.connect(generate_sitemap)
