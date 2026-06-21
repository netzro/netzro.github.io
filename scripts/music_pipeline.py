#!/usr/bin/env python3
"""
Music Pipeline: search, download, upload to IA, return embed-ready metadata.

Usage:
  python3 music_pipeline.py "Artist - Title"
  python3 music_pipeline.py --batch "song1" "song2" "song3"

Output: JSON with IA URL, metadata, and <audio> embed HTML.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import shutil

# --- Config ---
IA_ACCESS_KEY = os.environ.get("IA_AK", "qC6pZUEVuW1ofjQI")
IA_SECRET_KEY = os.environ.get("IA_SK", "1l5vE9P7rhgvMQVM")
MAX_FILE_SIZE_MB = 4
TARGET_BITRATE = "128k"  # ~1-3MB per song
DOWNLOAD_DIR = tempfile.mkdtemp(prefix="music_pipeline_")

# --- Helpers ---

def search_musicbrainz(artist, title):
    """Search MusicBrainz for track metadata."""
    query = f'artist:"{artist}" AND recording:"{title}"'
    url = f"https://musicbrainz.org/ws/2/recording/?query={urllib.parse.quote(query)}&fmt=json&limit=5"
    req = urllib.request.Request(url, headers={"User-Agent": "MusicPipeline/1.0 (blog)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("recordings", [])
    except Exception as e:
        print(f"  [MB] Search failed: {e}", file=sys.stderr)
        return []


def get_cover_art_mb(artist, title):
    """Get cover art URL from Cover Art Archive (linked to MusicBrainz)."""
    query = f'artist:"{artist}" AND release:"{title}"'
    url = f"https://musicbrainz.org/ws/2/release/?query={urllib.parse.quote(query)}&fmt=json&limit=3"
    req = urllib.request.Request(url, headers={"User-Agent": "MusicPipeline/1.0 (blog)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            for release in data.get("releases", []):
                rid = release.get("id")
                if rid:
                    cover_url = f"https://coverartarchive.org/release/{rid}/front-250"
                    return cover_url
    except Exception:
        pass
    return None


def search_youtube(artist, title):
    """Search YouTube for the best match."""
    query = f"{artist} {title} audio"
    cmd = [
        "yt-dlp",
        "--no-download",
        "--print", "%(id)s %(title)s",
        f"ytsearch5:{query}"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        lines = result.stdout.strip().split("\n")
        for line in lines:
            parts = line.split(" ", 1)
            if len(parts) == 2:
                return parts[0], parts[1]
    except Exception as e:
        print(f"  [YT] Search failed: {e}", file=sys.stderr)
    return None, None


def download_audio(artist, title, video_id):
    """Download audio from YouTube as MP3, target 1-4MB."""
    safe_name = re.sub(r'[^\w\-.]', '_', f"{artist}_{title}")[:60]
    output_path = os.path.join(DOWNLOAD_DIR, f"{safe_name}.mp3")

    cmd = [
        "yt-dlp",
        "--js-runtimes", "node",
        "--remote-components", "ejs:github",
        "-f", "bestaudio/best",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", TARGET_BITRATE,
        "-o", output_path,
        f"https://www.youtube.com/watch?v={video_id}"
    ]
    print(f"  [DL] Downloading audio...")
    try:
        subprocess.run(cmd, check=True, timeout=120, capture_output=True)
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  [DL] Done: {size_mb:.1f}MB")
        return output_path, size_mb
    except subprocess.CalledProcessError as e:
        print(f"  [DL] Failed: {e.stderr.decode()[:200]}", file=sys.stderr)
        return None, 0


def upload_to_internet_archive(identifier, title, artist, audio_path, metadata):
    """Upload audio file to Internet Archive."""
    try:
        from internetarchive import upload, get_item
    except ImportError:
        print("  [IA] Installing internetarchive library...", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "pip", "install", "internetarchive", "-q"], check=True)
        from internetarchive import upload, get_item

    # Set credentials
    os.environ["IAS3_ACCESS"] = IA_ACCESS_KEY
    os.environ["IAS3_SECRET"] = IA_SECRET_KEY

    ia_metadata = {
        "collection": "opensource_audio",
        "title": f"{artist} — {title}",
        "creator": artist,
        "mediatype": "audio",
        "year": str(metadata.get("year", "")),
        "album": metadata.get("album", ""),
        "artist": metadata.get("artist", artist),
    }

    print(f"  [IA] Uploading to Internet Archive as '{identifier}'...")
    try:
        item = get_item(identifier)
        item.upload(
            audio_path,
            metadata=ia_metadata,
            access_key=IA_ACCESS_KEY,
            secret_key=IA_SECRET_KEY,
            verbose=False
        )
        # Construct the file URL
        filename = os.path.basename(audio_path)
        ia_url = f"https://archive.org/download/{identifier}/{filename}"
        print(f"  [IA] Uploaded successfully: {ia_url}")
        return ia_url
    except Exception as e:
        print(f"  [IA] Upload failed: {e}", file=sys.stderr)
        return None


def process_song(artist, title):
    """Full pipeline for one song."""
    print(f"\n🎵 Processing: {artist} — {title}")
    print("=" * 50)

    # Step 1: Metadata
    print("  [1/4] Searching MusicBrainz...")
    recordings = search_musicbrainz(artist, title)
    metadata = {"artist": artist, "title": title, "year": "", "album": ""}
    if recordings:
        rec = recordings[0]
        metadata["title"] = rec.get("title", title)
        metadata["artist"] = rec.get("artist-credit", [{}])[0].get("name", artist)
        releases = rec.get("releases", [])
        if releases:
            rel = releases[0]
            metadata["album"] = rel.get("title", "")
            date = rel.get("date", "")
            if date:
                metadata["year"] = date[:4]
        print(f"  [1/4] Found: {metadata['artist']} — {metadata['title']} ({metadata['year']})")
    else:
        print("  [1/4] No MusicBrainz result, using search terms as metadata")

    # Step 2: YouTube search
    print("  [2/4] Searching YouTube...")
    video_id, yt_title = search_youtube(artist, title)
    if not video_id:
        print("  [2/4] No YouTube result", file=sys.stderr)
        return None
    print(f"  [2/4] Found: {yt_title} ({video_id})")

    # Step 3: Download
    print("  [3/4] Downloading audio...")
    audio_path, size_mb = download_audio(artist, title, video_id)
    if not audio_path:
        return None
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"  [3/4] File too large ({size_mb:.1f}MB), retrying with lower quality...", file=sys.stderr)
        # Retry with lower bitrate
        global TARGET_BITRATE
        TARGET_BITRATE = "96k"
        audio_path, size_mb = download_audio(artist, title, video_id)
        TARGET_BITRATE = "128k"  # reset
        if not audio_path or size_mb > MAX_FILE_SIZE_MB:
            print("  [3/4] Still too large, skipping", file=sys.stderr)
            return None

    # Step 4: Upload to IA
    print("  [4/4] Uploading to Internet Archive...")
    safe_id = re.sub(r'[^\w\-]', '_', f"{artist}_{title}_{video_id}")[:80]
    ia_url = upload_to_internet_archive(safe_id, metadata["title"], metadata["artist"], audio_path, metadata)

    if not ia_url:
        return None

    # Cover art
    cover_url = get_cover_art_mb(artist, title)

    # Build result
    result = {
        "artist": metadata["artist"],
        "title": metadata["title"],
        "album": metadata["album"],
        "year": metadata["year"],
        "ia_url": ia_url,
        "cover_url": cover_url,
        "size_mb": round(size_mb, 1),
        "embed_html": f'<audio controls preload="metadata" style="width:100%;max-width:400px;"><source src="{ia_url}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
    }

    # Cleanup
    os.remove(audio_path)

    return result


def main():
    parser = argparse.ArgumentParser(description="Music pipeline: search → download → IA upload")
    parser.add_argument("songs", nargs="+", help="Song in 'Artist - Title' format")
    parser.add_argument("--output", default="-", help="Output file (default: stdout)")
    args = parser.parse_args()

    results = []
    for song in args.songs:
        if " - " in song:
            artist, title = song.split(" - ", 1)
        else:
            artist, title = "", song
        result = process_song(artist.strip(), title.strip())
        if result:
            results.append(result)

    output = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w") as f:
            f.write(output)

    print(f"\n✅ Done! {len(results)}/{len(args.songs)} songs processed.", file=sys.stderr)


if __name__ == "__main__":
    main()
