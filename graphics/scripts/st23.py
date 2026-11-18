import json,sys,os,re,itertools
sys.path.insert(0,'/home/claude/wd')
from bo_data import R
SD=R+'songs_data/'
cl=lambda t:re.sub(r'\s*[\(\[].*','',t).split(' - ')[0].strip()
DATA={}
for f in os.listdir(SD):
    j=json.load(open(SD+f));s=f[:-5]
    rows=[(r['title'],r['streams'],r.get('feat')) for r in j['rows'][2:]]
    DATA[s]=dict(name=j['artist'],tot=j['rows'][0]['streams'],daily=j['rows'][1]['streams'],rows=sorted(rows,key=lambda x:-x[1]))
def clean(s):
    seen={};out=[]
    for t,v,fe in DATA[s]['rows']:
        if any(x in t for x in ('emix','Live','live','Version','Instrumental','Sped','Slowed','Acoustic')):continue
        c=cl(t)
        if c.lower() in seen:continue
        seen[c.lower()]=1;out.append((c,v,fe))
    return out
CL={s:clean(s) for s in DATA}
EXC={'doechii','summer-walker','latto','christina-aguilera','little-mix','sia','janet-jackson'}
