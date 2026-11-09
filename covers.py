import json, os, re, sys, time
import unicodedata, urllib.parse, urllib.request

ARTISTS = [(l.strip(), None) for l in open(sys.argv[1]) if l.strip()]

DRY = "--dry-run" in sys.argv
OUT = "albums"
UA = {"User-Agent": "pop-covers-script/1.0"}
API = "https://itunes.apple.com/"


def slug(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return s.strip("-")


def clean_album(n):
    return re.sub(r"\s*-\s*(EP|Single)$", "", n, flags=re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s).lower()
    return re.sub(r"[^a-z0-9]", "", s)


def get(url):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            if i == 3:
                raise
            time.sleep(3 * (i + 1))


def find_artist(name, term):
    q = urllib.parse.urlencode({
        "term": term or name,
        "entity": "musicArtist",
        "limit": 25,
    })
    res = json.loads(get(API + "search?" + q))["results"]
    for r in res:
        if norm(r["artistName"]) == norm(name):
            return r
    return res[0] if res else None


def albums_for(aid):
    q = urllib.parse.urlencode({
        "id": aid,
        "entity": "album",
        "limit": 200,
    })
    res = json.loads(get(API + "lookup?" + q))["results"]
    return [r for r in res
            if r.get("wrapperType") == "collection"]


os.makedirs(OUT, exist_ok=True)
report = []
for name, term in ARTISTS:
    a = find_artist(name, term)
    time.sleep(1)
    if not a:
        report.append("!! " + name + ": not found")
        continue
    if a["artistName"].lower() != name.lower():
        report.append("?? " + name + ": matched "
                      + a["artistName"] + " - check these")
    seen = set()
    for r in albums_for(a["artistId"]):
        t = r.get("collectionName", "")
        if t.endswith(" - Single"):
            continue
        if r.get("trackCount", 0) < 4:
            continue
        fn = slug(name) + "--" + slug(clean_album(t)) + ".jpg"
        if fn in seen:
            continue
        seen.add(fn)
        path = os.path.join(OUT, fn)
        if os.path.exists(path):
            report.append("   " + fn + " (already in repo)")
            continue
        art = r.get("artworkUrl100", "")
        art = art.replace("100x100bb", "640x640bb")
        if not art:
            continue
        if DRY:
            report.append("+  " + fn)
            continue
        try:
            with open(path, "wb") as f:
                f.write(get(art))
            report.append("+  " + fn)
        except Exception as e:
            report.append("!! " + fn + ": failed " + str(e))
        time.sleep(0.3)
    time.sleep(1)
    print(name + ": done")

with open("kpop_covers_report.txt", "w") as f:
    f.write("\n".join(report) + "\n")
added = sum(1 for l in report if l.startswith("+"))
print(str(added) + " covers added. See kpop_covers_report.txt")

