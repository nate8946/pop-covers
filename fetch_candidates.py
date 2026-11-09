"""Download up to ~20 candidate photos per artist so you can approve/deny them.
Usage:  python3 fetch_candidates.py "Taylor Swift" "Sabrina Carpenter"
        python3 fetch_candidates.py list all_ladies.txt     (lines: Name  or  Name|search name)
Saves candidates/<artist>/01-deezer.jpg, 02-audiodb.jpg, 10-commons.jpg ... and sources.txt
"""
import sys, os, re, json, hashlib, unicodedata, urllib.parse, urllib.request, time

OUT = "candidates"; MAXN = 20
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", "Accept": "image/avif,image/webp,image/*,*/*;q=0.8"}

def norm(s): return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
def slug(s): return re.sub(r"[^a-z0-9]+", "-", norm(s).lower()).strip("-")

def get(url, headers=None):
    err = None
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=headers or UA), timeout=30).read()
        except Exception as e:
            err = e; time.sleep(1.5 + i)
    raise err

def deezer(name):
    try:
        d = json.loads(get("https://api.deezer.com/search/artist?q=%s&limit=10" % urllib.parse.quote(name)))
        hits = [a for a in d.get("data", []) if norm(a["name"]).lower() == norm(name).lower()]
        if not hits: return []
        b = max(hits, key=lambda a: a.get("nb_fan", 0))
        img = b.get("picture_xl") or b.get("picture_big")
        return [("deezer", img, {})] if img and "/images/artist//" not in img else []
    except Exception as e:
        print("  (deezer error: %s)" % e); return []

def audiodb(name):
    try:
        arts = []
        for key in ("123", "2"):
            d = json.loads(get("https://www.theaudiodb.com/api/v1/json/%s/search.php?s=%s" % (key, urllib.parse.quote(name))))
            arts = d.get("artists") or []
            if arts: break
        a = next((x for x in arts if norm(x["strArtist"]).lower() == norm(name).lower()), None)
        if not a: return []
        keys = ["strArtistThumb", "strArtistFanart", "strArtistFanart2", "strArtistFanart3", "strArtistFanart4", "strArtistWideThumb"]
        return [("audiodb", a[k], {}) for k in keys if a.get(k)]
    except Exception as e:
        print("  (audiodb error: %s)" % e); return []

BAD = ("tussauds", "wax", "figure", "collection", "fan ", "logo", "signature", "autograph", "map", "poster", "stamp", "cartoon", "statue", "mural", "doll", "cover", "album", "tour book", "ticket", "billboard", "sign")

def commons(name):
    try:
        params = {"action": "query", "format": "json", "generator": "search", "gsrsearch": name + " filetype:bitmap",
                  "gsrnamespace": 6, "gsrlimit": 50, "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1200}
        d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)))
        tokens = [t for t in re.split(r"[^a-z0-9]+", norm(name).lower()) if len(t) > 2]
        out = []
        for p in d.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [None])[0]
            if not ii or ii.get("mime") != "image/jpeg": continue
            t = norm(p["title"]).lower()
            if tokens and not all(x in t for x in tokens[-2:]): continue
            if any(b in t for b in BAD): continue
            if ii["width"] < 900 or ii["height"] < 900: continue
            out.append((ii["width"] * ii["height"], ("commons", ii.get("thumburl") or ii["url"], {"title": p["title"]})))
        out.sort(key=lambda x: -x[0])
        return [o[1] for o in out]
    except Exception as e:
        print("  (commons error: %s)" % e); return []

def fetch(name, query=None, force=False):
    q = query or name; folder = "%s/%s" % (OUT, slug(name))
    if os.path.isdir(folder) and not force:
        print("have:", folder); return
    cands = deezer(q) + audiodb(q) + commons(q)
    seen, n, notes = set(), 0, []
    for src, url, meta in cands:
        if n >= MAXN: break
        try: data = get(url)
        except Exception as e:
            print("  skip %s: %s" % (src, e)); continue
        h = hashlib.md5(data).hexdigest()
        if h in seen or len(data) < 15000: continue
        seen.add(h); n += 1
        os.makedirs(folder, exist_ok=True)
        fn = "%02d-%s.jpg" % (n, src)
        open("%s/%s" % (folder, fn), "wb").write(data)
        notes.append("%s | %s | %s" % (fn, meta.get("title", ""), url))
    if n:
        open(folder + "/sources.txt", "w").write("\n".join(notes) + "\n")
        print("saved %d candidates: %s" % (n, folder))
    else:
        print("NO PHOTOS:", name)
    time.sleep(0.5)

force = "--force" in sys.argv
args = [a for a in sys.argv[1:] if a != "--force"]
items = [l.strip() for l in open(args[1]) if l.strip()] if args and args[0] == "list" else args
for it in items:
    nm, _, q = it.partition("|")
    try: fetch(nm.strip(), q.strip() or None, force)
    except Exception as e: print("ERROR:", nm, e)
