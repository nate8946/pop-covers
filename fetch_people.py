"""Download up to 3 normal photos of each artist (official promo/press shots).
Sources: Deezer (artist photo) + TheAudioDB (artist thumb and fan-art photos). No keys needed.
Usage:  python3 fetch_people.py "Taylor Swift" "Sabrina Carpenter"
        python3 fetch_people.py list all_ladies.txt     (lines: Name  or  Name|search name)
        add --force to redo artists that already have a folder
Saves people/<artist>/1.jpg 2.jpg 3.jpg and sources.txt
"""
import sys, os, re, json, hashlib, unicodedata, urllib.parse, urllib.request, time

OUT = "people"
UA = {"User-Agent": "Mozilla/5.0"}

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", norm(s).lower()).strip("-")

def get(url):
    err = None
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
        except Exception as e:
            err = e; time.sleep(1 + i)
    raise err

def deezer(name):
    try:
        d = json.loads(get("https://api.deezer.com/search/artist?q=%s&limit=10" % urllib.parse.quote(name)))
        hits = [a for a in d.get("data", []) if norm(a["name"]).lower() == norm(name).lower()]
        if not hits: return []
        b = max(hits, key=lambda a: a.get("nb_fan", 0))
        img = b.get("picture_xl") or b.get("picture_big")
        return [("deezer", img)] if img and "/images/artist//" not in img else []
    except Exception:
        return []

def audiodb(name):
    try:
        arts = []
        for key in ("123", "2"):
            d = json.loads(get("https://www.theaudiodb.com/api/v1/json/%s/search.php?s=%s" % (key, urllib.parse.quote(name))))
            arts = d.get("artists") or []
            if arts: break
        if not arts: print("  (audiodb: nothing for %s)" % name)
        a = next((x for x in arts if norm(x["strArtist"]).lower() == norm(name).lower()), None)
        if not a: return []
        keys = ["strArtistThumb", "strArtistFanart", "strArtistFanart2", "strArtistFanart3", "strArtistFanart4", "strArtistWideThumb"]
        return [("audiodb:" + k, a[k]) for k in keys if a.get(k)]
    except Exception as e:
        print('  (audiodb error: %s)' % e)
        return []

def fetch(name, query=None, force=False):
    folder = "%s/%s" % (OUT, slug(name))
    if os.path.isdir(folder) and not force:
        print("have:", folder); return
    q = query or name
    cands = deezer(q) + audiodb(q)
    seen, saved, notes = set(), 0, []
    for src, url in cands:
        if saved == 3: break
        try:
            data = get(url)
        except Exception:
            continue
        h = hashlib.md5(data).hexdigest()
        if h in seen or len(data) < 15000: continue
        seen.add(h)
        os.makedirs(folder, exist_ok=True)
        saved += 1
        open("%s/%d.jpg" % (folder, saved), "wb").write(data)
        notes.append("%d.jpg | %s | %s" % (saved, src, url))
    if saved:
        open(folder + "/sources.txt", "w").write("\n".join(notes) + "\n")
        print("saved %d/3: %s" % (saved, folder))
    else:
        print("NO PHOTOS:", name)
    time.sleep(0.5)

force = "--force" in sys.argv
args = [a for a in sys.argv[1:] if a != "--force"]
items = [l.strip() for l in open(args[1]) if l.strip()] if args and args[0] == "list" else args
for it in items:
    nm, _, q = it.partition("|")
    try:
        fetch(nm.strip(), q.strip() or None, force)
    except Exception as e:
        print("ERROR:", nm, e)
