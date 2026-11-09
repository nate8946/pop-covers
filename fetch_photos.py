"""Download up to 3 photos per artist from Wikimedia Commons (free-licensed images).
Usage:  python3 fetch_photos.py "Taylor Swift" "Sabrina Carpenter"
        python3 fetch_photos.py list all_ladies.txt     (lines: Name   or   Name|search words)
        add --force to redo artists that already have a folder
Saves photos/<artist>/1.jpg 2.jpg 3.jpg and photos/<artist>/credits.txt
"""
import sys, os, re, json, unicodedata, urllib.parse, urllib.request, time

OUT = "photos"
UA = {"User-Agent": "PopByNumbers-image-script/1.0 (personal project; python urllib)"}

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s).lower()).strip("-")

def get(url):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except Exception as e:
            err = e; time.sleep(2 + 2 * i)
    raise err

def strip_html(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()

def candidates(query, name):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query + " filetype:bitmap", "gsrnamespace": 6, "gsrlimit": 40,
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1400,
    }
    data = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)))
    pages = data.get("query", {}).get("pages", {}).values()
    tokens = [t for t in re.split(r"[^a-z0-9]+", norm(name).lower()) if len(t) > 2]
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [None])[0]
        if not ii or ii.get("mime") != "image/jpeg":
            continue
        title = norm(p["title"]).lower()
        if tokens and not all(t in title for t in tokens[-2:]):
            continue
        w, h = ii["width"], ii["height"]
        if w < 800 or h < 800:
            continue
        if any(b in title for b in ("logo", "signature", "autograph", "map", "poster", "stamp", "wax", "cartoon")):
            continue
        meta = ii.get("extmetadata", {})
        out.append({
            "url": ii.get("thumburl") or ii["url"], "title": p["title"],
            "area": w * h, "ratio": h / w,
            "author": strip_html(meta.get("Artist", {}).get("value")),
            "license": strip_html(meta.get("LicenseShortName", {}).get("value")),
            "page": ii.get("descriptionurl", ""),
        })
    # prefer portrait-ish / square, then bigger
    out.sort(key=lambda c: (abs(c["ratio"] - 1.2) > 0.5, -c["area"]))
    return out

def fetch(name, query=None, force=False):
    folder = f"{OUT}/{slug(name)}"
    if os.path.isdir(folder) and not force:
        print("have:", folder); return
    cands = candidates(query or name, name)
    if not cands:
        print("NO PHOTOS:", name); return
    os.makedirs(folder, exist_ok=True)
    credits = []
    for i, c in enumerate(cands[:3], 1):
        open(f"{folder}/{i}.jpg", "wb").write(get(c["url"]))
        credits.append(f"{i}.jpg | {c['title']} | {c['author']} | {c['license']} | {c['page']}")
    open(f"{folder}/credits.txt", "w").write("\n".join(credits) + "\n")
    print(f"saved {min(3, len(cands))}/3: {folder}")
    time.sleep(1)

force = "--force" in sys.argv
args = [a for a in sys.argv[1:] if a != "--force"]
if args and args[0] == "list":
    items = [l.strip() for l in open(args[1]) if l.strip()]
else:
    items = args
for it in items:
    nm, _, q = it.partition("|")
    try:
        fetch(nm.strip(), q.strip() or None, force)
    except Exception as e:
        print("ERROR:", nm, e)
