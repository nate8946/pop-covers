import json,re,itertools
FJ=json.load(open('/tmp/g/fresh17.json'))
cl=lambda t:re.sub(r'\s*[\(\[].*','',t).split(' - ')[0].strip()
NAMES={'charli-xcx':'Charli XCX','tate-mcrae':'Tate McRae','karol-g':'Karol G','sza':'SZA','jennie':'JENNIE','lisa':'LISA','karol-g':'Karol G','ice-spice':'Ice Spice','megan-thee-stallion':'Megan Thee Stallion','lady-gaga':'Lady Gaga','billie-eilish':'Billie Eilish','michael-jackson':'Michael Jackson'}
DATA={};CL={};UD={}
for s,v in FJ.items():
    DATA[s]=dict(name=NAMES.get(s,s.replace('-',' ').title().replace('Del Rey','Del Rey')),tot=v['t'],daily=v['d'],rows=[(t,n,t.startswith('* ')) for t,n in v['r']])
    UD[s]=v['u']
    seen={};out=[]
    for t,n in v['r']:
        fe=t.startswith('* ');t2=t[2:] if fe else t
        if any(x in t2 for x in ('emix','Live','live','Version','Instrumental','Sped','Slowed','Acoustic')) and 'Remix' not in t2.split('(')[0] and False:continue
        c=cl(t2)
        if c.lower() in seen:continue
        seen[c.lower()]=1;out.append((c,n,fe))
    CL[s]=out
DATA['adele']['name']='Adele'
EXC={'doechii','summer-walker','latto','christina-aguilera','little-mix','sia','janet-jackson'}
def dtl(*ss):
    ds=sorted({UD[s][5:].replace('/','-') for s in ss})
    m={'11-16':'Nov 16','11-17':'Nov 17'}
    ds=[m.get(x,x) for x in ds]
    return ds[0] if len(ds)==1 else f'{ds[0]} and {ds[-1]}'
