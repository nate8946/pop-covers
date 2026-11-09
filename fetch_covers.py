#!/usr/bin/env python3
"""Download album covers and artist photos from Spotify into this repo.

Setup (once):
  1. Go to https://developer.spotify.com/dashboard, create an app (any name,
     redirect URI http://127.0.0.1:8888/callback), copy the Client ID and Secret.
  2. In your terminal:
       export SPOTIFY_CLIENT_ID=...      (Windows PowerShell: $env:SPOTIFY_CLIENT_ID="...")
       export SPOTIFY_CLIENT_SECRET=...

Usage (run from the repo folder, no installs needed, Python 3.8+):
  python fetch_covers.py album "Taylor Swift" "1989"
  python fetch_covers.py artist-albums "Sabrina Carpenter"     # every album + single
  python fetch_covers.py artist-photo "Rihanna"
  python fetch_covers.py list wanted.txt     # lines: "Artist | Album"  or  "Artist | *" for artist photo
Existing files are skipped; add --force to overwrite.
"""
import base64, json, os, re, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(ROOT, "manifest.json")
FORCE = "--force" in sys.argv
ARGS = [a for a in sys.argv[1:] if a != "--force"]

def slug(s):
    s = s.lower().replace("é", "e").replace("á", "a").replace("ó", "o").replace("ñ", "n")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def get(url, headers=None, data=None):
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def token():
    cid, sec = os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not cid or not sec:
        sys.exit("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET first (see the top of this file).")
    auth = base64.b64encode(f"{cid}:{sec}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    return json.loads(get("https://accounts.spotify.com/api/token",
                          {"Authorization": "Basic " + auth}, body))["access_token"]

TOK = None
def api(path, **params):
    global TOK
    TOK = TOK or token()
    url = "https://api.spotify.com/v1/" + path + ("?" + urllib.parse.urlencode(params) if params else "")
    return json.loads(get(url, {"Authorization": "Bearer " + TOK}))

def manifest():
    m = json.load(open(MAN)) if os.path.exists(MAN) else {}
    for k in ("albums", "artists", "unsorted"):
        m.setdefault(k, [])
    return m

def save_manifest(m):
    json.dump(m, open(MAN, "w"), indent=1, ensure_ascii=False)

def best(images):
    return sorted(images, key=lambda i: -(i.get("width") or 0))[0]["url"] if images else None

def put(kind, artist, album, url, m):
    folder = "albums" if kind == "albums" else "artists"
    name = f"{slug(artist)}--{slug(album)}.jpg" if kind == "albums" else f"{slug(artist)}.jpg"
    rel = f"{folder}/{name}"
    path = os.path.join(ROOT, rel)
    if os.path.exists(path) and not FORCE:
        print("skip (exists):", rel); return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(get(url))
    m[kind] = [e for e in m[kind] if e.get("file") != rel]
    m[kind].append({"artist": artist, "album": album, "file": rel})
    print("saved:", rel)

def find_artist(name):
    items = api("search", q=name, type="artist", limit=5)["artists"]["items"]
    for a in items:
        if a["name"].lower() == name.lower():
            return a
    return items[0] if items else None

def do_album(artist, album, m):
    r = api("search", q=f'artist:"{artist}" album:"{album}"', type="album", limit=10)["albums"]["items"]
    want = [x for x in r if any(a["name"].lower() == artist.lower() for a in x["artists"])] or r
    exact = [x for x in want if x["name"].lower() == album.lower()] or want
    if not exact:
        print("not found:", artist, "|", album); return
    x = exact[0]
    put("albums", artist, x["name"], best(x["images"]), m)

def do_artist_albums(artist, m):
    a = find_artist(artist)
    if not a: print("artist not found:", artist); return
    off = 0; seen = set()
    while True:
        page = api(f"artists/{a['id']}/albums", include_groups="album,single", limit=50, offset=off, market="US")
        for x in page["items"]:
            key = x["name"].lower()
            if key in seen: continue
            seen.add(key); put("albums", a["name"], x["name"], best(x["images"]), m)
        off += 50
        if not page.get("next"): break

def do_artist_photo(artist, m):
    a = find_artist(artist)
    if not a or not a["images"]: print("no photo:", artist); return
    put("artists", a["name"], "(artist photo)", best(a["images"]), m)

def main():
    if not ARGS: print(__doc__); return
    cmd, rest = ARGS[0], ARGS[1:]
    m = manifest()
    if cmd == "album" and len(rest) == 2: do_album(rest[0], rest[1], m)
    elif cmd == "artist-albums" and len(rest) == 1: do_artist_albums(rest[0], m)
    elif cmd == "artist-photo" and len(rest) == 1: do_artist_photo(rest[0], m)
    elif cmd == "list" and len(rest) == 1:
        for line in open(rest[0], encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "|" not in line: continue
            a, b = [s.strip() for s in line.split("|", 1)]
            do_artist_photo(a, m) if b == "*" else do_album(a, b, m)
    else: print(__doc__); return
    save_manifest(m)

if __name__ == "__main__":
    main()
