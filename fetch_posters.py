#!/usr/bin/env python3
"""Fetch missing posters for movies.md from OMDB, resize to 300x450, update markdown."""
import urllib.request, urllib.parse, json, os, re, time

POSTERS_DIR = 'content/images/posters'
MD_PATH = 'content/pages/movies.md'
OMDB_KEY = '96f41149'

with open(MD_PATH, 'r') as f:
    lines = f.readlines()

existing = set(os.listdir(POSTERS_DIR))

def slugify(title, year=""):
    s = title.lower().replace(':', '').replace('&', 'and').replace("'", '').replace(',', '').replace('!', '').replace('?', '').replace('.', '')
    s = re.sub(r'[^a-z0-9\s-]', '', s).replace(' ', '-')
    if year and year != 'unknown':
        s += f'-{year}'
    return s + '.jpg'

def fetch_poster(title, year=""):
    query = urllib.parse.quote(title)
    url = f'http://www.omdbapi.com/?t={query}&y={year}&apikey={OMDB_KEY}' if year else f'http://www.omdbapi.com/?t={query}&apikey={OMDB_KEY}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if data.get('Response') == 'True':
                poster = data.get('Poster', '')
                if poster and poster != 'N/A':
                    return poster
    except Exception as e:
        print(f"  OMDB error: {e}")
    return None

def download_poster(url, filepath):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(filepath, 'wb') as f:
                f.write(data)
            return True
    except Exception as e:
        print(f"  Download failed: {e}")
        return False

# Collect movies needing posters - regex fix: closing ** after year
to_fetch = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('**') and '![](https' not in stripped:
        m = re.search(r'\*\*([^*]+?)\s*\((\d{4})\)\*\*', stripped)
        if m:
            title = m.group(1).strip()
            year = m.group(2)
            slug = slugify(title, year)
            if slug not in existing:
                to_fetch.append((i, title, year, slug))
            else:
                print(f"SKIP (exists): {title} ({year})")

print(f"Need posters: {len(to_fetch)}")

fetched = 0
failed = []
for idx, title, year, slug in to_fetch:
    print(f"FETCHING: {title} ({year})")
    poster_url = fetch_poster(title, year)
    if poster_url:
        filepath = os.path.join(POSTERS_DIR, slug)
        if download_poster(poster_url, filepath):
            # Resize to 300x450
            os.system(f"python3 -c \"from PIL import Image; im=Image.open('{filepath}'); im=im.resize((300,450), Image.LANCZOS); im.save('{filepath}')\" 2>/dev/null")
            print(f"  OK -> {slug}")
            fetched += 1
        else:
            failed.append((title, year, "download"))
    else:
        failed.append((title, year, "no OMDB match"))
    time.sleep(0.5)

print(f"\nDone: fetched={fetched}, failed={len(failed)}")
for t, y, r in failed:
    print(f"  FAIL: {t} ({year}): {r}")
