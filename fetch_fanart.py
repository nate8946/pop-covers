"""Download up to 3 photos per artist from fanart.tv (artist thumbs first, then backgrounds).
Needs a free fanart.tv personal API key:   export FANART_KEY=yourkey
Usage:  python3 fetch_fanart.py "Taylor Swift" "Sabrina Carpenter"
        python3 fetch_fanart.py list all_ladies.txt     (lines: Name  or  Name|musicbrainz search name)
        add --force to redo artists that already have a folder
Saves fanart/<artist>/1.jpg 2.jpg 3.jpg and sources.txt
"""
import sys, os, re, json, unicodedata, urllib.parse, urllib.request, time

KEY = os.environ.get("FANART_KEY", "").strip()
if not KEY:
    sys.exit("Set your key first:  export FANART_KEY=yourkey")
OUT = "fanart"
UA = {"User-Agent": "PopByNumbers-image-script/1.0 (personal project)"}

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
            err = e; time.sleep(1.5 + i)
    raise err

def mbid(name):
    d = json.loads(get("https://musicbrainz.org/ws/2/artist/?query=artist:%s&fmt=json&limit=10" % urllib.parse.quote('"%s"' % name)))
    arts = [a for a in d.get("artists", []) if norm(a["name"]).lower() == norm(name).lower()]
    if not arts: return None
    return max(arts, key=lambda a: a.get("score", 0))["id"]

def fetch(name, query=None, force=False):
    folder = "%s/%s" % (OUT, slug(name))
    if os.path.isdir(folder) and not force:
        print("have:", folder); return
    mb = mbid(query or name); time.sleep(1.1)
    if not mb:
        print("NO MATCH:", name); return
    try:
        d = json.loads(get("https://webservice.fanart.tv/v3/music/%s?api_key=%s" % (mb, KEY)))
    except Exception as e:
        print("NO FANART:", name, e); return
    urls = []
    for k in ("artistthumb", "artistbackground"):
        items = sorted(d.get(k, []), key=lambda x: -int(x.get("likes", 0) or 0))
        urls += [(k, i["url"]) for i in items]
    if not urls:
        print("NO PHOTOS:", name); return
    os.makedirs(folder, exist_ok=True)
    notes = []
    for n, (k, u) in enumerate(urls[:3], 1):
        open("%s/%d.jpg" % (folder, n), "wb").write(get(u))
        notes.append("%d.jpg | %s | %s" % (n, k, u))
    open(folder + "/sources.txt", "w").write("\n".join(notes) + "\n")
    print("saved %d/3: %s" % (min(3, len(urls)), folder))

force = "--force" in sys.argv
args = [a for a in sys.argv[1:] if a != "--force"]
items = [l.strip() for l in open(args[1]) if l.strip()] if args and args[0] == "list" else args
for it in items:
    nm, _, q = it.partition("|")
    try:
        fetch(nm.strip(), q.strip() or None, force)
    except Exception as e:
        print("ERROR:", nm, e)
