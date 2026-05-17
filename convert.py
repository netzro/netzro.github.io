"""
Convert YAML frontmatter to Pelican native (Key: Value) format.
Processes all .md files in content/posts/ and content/pages/ recursively.

Usage:
    uv run python convert_frontmatter.py          # dry run
    uv run python convert_frontmatter.py --apply  # apply changes
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ── config ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent
CONTENT_DIRS = [
    REPO_ROOT / "content" / "posts",
    REPO_ROOT / "content" / "pages",
]
DRY_RUN = "--apply" not in sys.argv

# YAML key → Pelican key mapping
KEY_MAP = {
    "title": "Title",
    "date": "Date",
    "modified": "Modified",
    "author": "Author",
    "authors": "Authors",
    "category": "Category",
    "categories": "Category",   # Pelican only supports one category
    "tags": "Tags",
    "slug": "Slug",
    "summary": "Summary",
    "description": "Summary",  # common alias
    "status": "Status",
    "lang": "Lang",
    "template": "Template",
    "save_as": "Save_as",
    "url": "URL",
}

# Keys to drop entirely
DROP_KEYS = {
    "draft",        # meaningless to Pelican
    "layout",       # Jekyll artifact
    "published",    # Jekyll artifact
    "permalink",    # Jekyll artifact
    "comments",     # Jekyll artifact
    "keywords",     # only relevant in HTML metadata
}

# ── helpers ───────────────────────────────────────────────────────────────────

YAML_BLOCK = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_yaml_block(yaml_text: str) -> dict[str, str]:
    """Parse simple flat YAML into a dict. Handles multiline list values."""
    result: dict[str, str] = {}
    current_key: str | None = None
    list_items: list[str] = []

    for line in yaml_text.splitlines():
        # list item
        if line.startswith("  - ") or line.startswith("- "):
            item = line.lstrip("- ").strip()
            if current_key:
                list_items.append(item)
            continue

        m = re.match(r"^([\w\-]+):\s*(.*)", line)
        if m:
            # flush previous list
            if current_key and list_items:
                result[current_key] = ", ".join(list_items)
                list_items = []

            current_key = m.group(1).lower()
            value = m.group(2).strip().strip('"').strip("'")

            if value:
                result[current_key] = value
            # else wait for list items

    # flush last list
    if current_key and list_items:
        result[current_key] = ", ".join(list_items)

    return result


def convert_status(value: str) -> str | None:
    """Normalise status values."""
    v = value.lower().strip()
    if v in ("draft", "hidden", "skip", "published"):
        return v.capitalize()
    if v == "false":    # draft: false → published (no status needed)
        return None
    if v == "true":     # draft: true → draft
        return "draft"
    return value.capitalize()


def build_pelican_header(fields: dict[str, str]) -> str:
    """Build Pelican native frontmatter string."""
    lines: list[str] = []

    # preferred field order
    order = ["Title", "Date", "Modified", "Author", "Authors",
             "Category", "Tags", "Slug", "Summary", "Status",
             "Lang", "Template", "Save_as", "URL"]

    seen = set()
    for key in order:
        if key in fields:
            lines.append(f"{key}: {fields[key]}")
            seen.add(key)

    # any remaining unmapped keys
    for key, val in fields.items():
        if key not in seen:
            lines.append(f"{key}: {val}")

    return "\n".join(lines)


def process_file(path: Path) -> tuple[bool, str]:
    """
    Returns (changed, report_line).
    If DRY_RUN, reports what would change without writing.
    """
    text = path.read_text(encoding="utf-8")

    m = YAML_BLOCK.match(text)
    if not m:
        return False, f"  SKIP (no YAML block): {path.name}"

    yaml_text = m.group(1)
    body = text[m.end():]

    raw = parse_yaml_block(yaml_text)

    pelican: dict[str, str] = {}
    dropped: list[str] = []

    for raw_key, raw_val in raw.items():
        if raw_key in DROP_KEYS:
            dropped.append(raw_key)
            continue

        pelican_key = KEY_MAP.get(raw_key)
        if pelican_key is None:
            # keep unknown keys as-is, title-cased
            pelican_key = raw_key.capitalize()

        if pelican_key == "Status":
            converted = convert_status(raw_val)
            if converted:
                pelican[pelican_key] = converted
            # else drop (published is the default)
        else:
            pelican[pelican_key] = raw_val

    new_header = build_pelican_header(pelican)
    new_content = new_header + "\n\n" + body.lstrip("\n")

    changed = new_content != text

    if not DRY_RUN and changed:
        path.write_text(new_content, encoding="utf-8")

    report = f"  {'WOULD UPDATE' if DRY_RUN else 'UPDATED'}: {path.name}"
    if dropped:
        report += f" (dropped: {', '.join(dropped)})"

    return changed, report


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    mode = "DRY RUN" if DRY_RUN else "APPLYING CHANGES"
    print(f"\n{'='*50}")
    print(f"  Frontmatter Converter — {mode}")
    print(f"{'='*50}")

    total_changed = 0
    total_skipped = 0

    for content_dir in CONTENT_DIRS:
        if not content_dir.exists():
            print(f"\n  WARNING: {content_dir} not found, skipping.")
            continue

        files = sorted(content_dir.rglob("*.md"))
        print(f"\n  [{content_dir.name}/] — {len(files)} files")

        for path in files:
            changed, report = process_file(path)
            print(report)
            if changed:
                total_changed += 1
            else:
                total_skipped += 1

    print(f"\n{'='*50}")
    print(f"  {'Would update' if DRY_RUN else 'Updated'}: {total_changed} files")
    print(f"  Skipped (no YAML or already clean): {total_skipped} files")
    if DRY_RUN:
        print(f"\n  Run with --apply to make changes.")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
