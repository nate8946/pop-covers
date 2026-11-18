import re,json,glob,sys
sys.path.insert(0,'/home/claude/wd')
src=open('/home/claude/lk/build30.py').read().split("RAW={}")[0].replace("/outputs/fwtmp/","/outputs/fw37/"); exec(src)
from bo_data import R,AP
def pool(sl):
    g=sorted(glob.glob(f'{R}approved/{sl}/*.jpg'));sg=[]
    for i in AP.get(sl,[]):sg+=glob.glob(f'{R}source_test4/{sl}/{i:02d}-*.jpg')
    return list(dict.fromkeys(g+sg))
TS=sorted(glob.glob(R+'source_test4/taylor-swift/*.jpg'))+sorted(glob.glob(R+'source_test/taylor-swift/*.jpg'))
TSI=[12,4,46,47]
DZ={'ella-langley','megan-moroney'}
LABEL={'taylor-swift':'Taylor Swift','bts':'BTS','olivia-rodrigo':'Olivia Rodrigo','stray-kids':'Stray Kids','ateez':'ATEEZ','enhypen':'ENHYPEN','ariana-grande':'Ariana Grande','drake':'Drake','madonna':'Madonna','gracie-abrams':'Gracie Abrams','phoebe-bridgers':'Phoebe Bridgers','kacey-musgraves':'Kacey Musgraves','ella-langley':'Ella Langley','megan-moroney':'Megan Moroney','jhene-aiko':'Jhené Aiko','miley-cyrus':'Miley Cyrus','tomorrow-x-together':'TXT','aespa':'aespa','seventeen':'Seventeen'}
def sl(n):return n.split('#')[0]
ALBM={'eminem':'eminem--the-marshall-mathers-lp','ozuna':'ozuna--odisea','pitbull':'pitbull--planet-pit','tame-impala':'tame-impala--currents','black-eyed-peas':'black-eyed-peas--the-e-n-d','justin-timberlake':'justin-timberlake--futuresex-lovesounds','linkin-park':'linkin-park--hybrid-theory'}
def photo(name,k=0):
    s=sl(name);i=int(name.split('#')[1]) if '#' in name and name.split('#')[1].isdigit() else 0
    ALB=ALBM
    if name.startswith('alb:'):f=R+'albums/'+name[4:]+'.jpg'
    elif name.endswith('#alb'):f=R+'albums/'+ALB[s]+'.jpg'
    elif s=='taylor-swift':f=TS[TSI[i]]
    elif s in DZ:f=R+'deezer_photos/'+s+'.jpg'
    else:
        pl=pool(s) or sorted(glob.glob(R+'source_test4/'+s+'/*.jpg'))
        f=pl[PI.get(name,i)] if False else pl[i]
    p=Image.open(f).convert('RGB')
    if name=='eminem#0':
        w0,h0=p.size;p=p.crop((int(w0*0.50),int(h0*0.05),w0,int(h0*0.75)))
    w,h=p.size;q=min(w,h);l=(w-q)//2
    t=int((h-q)*0.10) if h>w else 0
    return p.crop((l,t,l+q,t+q)).resize((T*S,T*S),Image.LANCZOS)
short=lambda n:LABEL.get(sl(n),sl(n))
def board(fn,top,rows,cols=4):
    n=len(rows);nr=n//cols;W=cols*T+(cols-1)*G;H=3*BAR+nr*T+(nr-1)*G
    cv=Image.new('RGB',(W*S,H*S),(255,255,255));y=0
    cv.paste(bar(W*S,top),(0,y));y+=BAR*S
    for r_ in range(nr):
        for c_ in range(cols):
            j=r_*cols+c_;nm,val,sub=rows[j]
            cv.paste(tile((nm,),j+1,val,sub,j),(c_*(T+G)*S,y))
        y+=T*S
        if nr>1 and r_==(nr-1)//2: cv.paste(bar(W*S),(0,y));y+=BAR*S
        elif r_<nr-1:y+=G*S
    cv=cv.crop((0,0,W*S,y));cv.resize((2200,int(cv.height*2200/cv.width)),Image.LANCZOS).save(OUTD+fn,quality=93)
K=lambda x:f'{x/1e6:.2f}M' if x>=1e6 else f'{round(x/1e3)}K'
import os,re,json
_hd=dict(globals())
exec(open('/tmp/f/sel.py').read().split('BOARDS=[]')[0])
WM=[x for x in W if x[0] not in ('doechii','anuel-aa','bad-bunny','daddy-yankee','feid','j-balvin','maluma','rauw-alejandro')]
for _k in ('W','S','BAR','F','T','G','P','D','C','K'):
    if _k in _hd: globals()[_k]=_hd[_k]
src=open('/tmp/k/data.py').read()
NAME=eval(src[src.index("NAME="):].split('\n')[0][5:]);PHK=eval(src[src.index("PH="):].split('\n')[0][3:])
FR=json.load(open('/tmp/k3/fresh.json'))
KR=sorted([(k,l.rsplit('|',1)[0],int(l.rsplit('|',1)[1])) for k,v in FR.items() for l in v.split('\n')],key=lambda x:-x[2])
KD={k:[(l.rsplit('|',1)[0],int(l.rsplit('|',1)[1])) for l in v.split('\n')] for k,v in FR.items()}
OUT='/mnt/user-data/outputs/fw37';os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT):os.remove(OUT+'/'+f)
fm=lambda x:f'{x/1e9:.2f}B' if x>=1e9 else f'{int(x/1e6)}M' if x>=999.5e6 else f'{round(x/1e6)}M'
for k,v in NAME.items():LABEL[k]=v
for k,(nm,txt,ph) in d.items():LABEL.setdefault(k,nm)
n=0
def nm_(s):
    global n;n+=1;return f'{n:02d}_{s}.jpg'
def dd(pool,f,m,ex=()):
    out=[];seen=set()
    for x in pool:
        if f(x[1]) and not any(e in x[1] for e in ex):
            key=re.sub(r'\W','',x[1].lower())
            if key in seen:continue
            seen.add(key);out.append(x)
    return out[:m]
def kb(s,title,L):
    assert len(L) in(12,16),(s,len(L));board(nm_(s),title,[(f'{k}#{PHK[k]}',fm(v),t) for k,t,v in L],4)
def wb(s,title,L):
    assert len(L) in(12,16),(s,len(L));board(nm_(s),title,[(f'{k}#{d[k][2][0]}',fm(v),t) for k,t,v in L],4)
from collections import defaultdict
WS=defaultdict(list)
for s_,t_,v_ in WM:WS[s_].append((t_,v_))
WS={k:sorted(v,key=lambda x:-x[1]) for k,v in WS.items() if len(v)>=16 and k in d}
from PIL import Image,ImageDraw,ImageFont
import textwrap
OUTD='/mnt/user-data/outputs/grammy_final3/'
FD='/usr/share/fonts/opentype/inter/'
def F(w,s):return ImageFont.truetype(FD+f'Inter-{w}.otf',s)
def fmt(v):return f'{v/1e9:.2f}B' if v>=1e9 else f'{round(v/1e6)}M'
FACE={'taylor-swift#0':(0.5,0.36),'tame-impala#3':(0.45,0.30),'raye#1':(0.5,0.30),'lady-gaga#0':(0.5,0.50),'madonna#0':(0.5,0.50),'olivia-dean#0':(0.5,0.45),'ella-langley#0':(0.5,0.32),'bruno-mars#0':(0.5,0.30),'ariana-grande#0':(0.5,0.40),'olivia-rodrigo#0':(0.5,0.30),'rosalia#0':(0.5,0.30)}
def cover_fit(im,w,h,fy=0.30,face=(0.5,0.35)):
    s=max(w/im.width,h/im.height);im=im.resize((max(w,round(im.width*s)),max(h,round(im.height*s))),Image.LANCZOS)
    l=min(max(int(face[0]*im.width-w/2),0),im.width-w);t=min(max(int(face[1]*im.height-h*0.5),0),im.height-h)
    return im.crop((l,t,l+w,t+h))
def sc(v,m):return v/m
def tw(d,t,f):return d.textlength(t,font=f)
def ctext(d,cx,y,t,f,fill):d.text((cx-tw(d,t,f)/2,y),t,font=f,fill=fill)
def wrap(d,t,f,maxw):
    out=[];cur=''
    for w in t.split():
        c=(cur+' '+w).strip()
        if tw(d,c,f)<=maxw:cur=c
        else:out.append(cur);cur=w
    out.append(cur);return out
BG=(223,233,245);NAVY=(18,38,76);SUB=(70,90,125)
def circle(im,ph,x,y,dia,bw=9):
    p=photo(ph).resize((1280,1280));fc=FACE.get(ph,(0.5,0.35));c=cover_fit(p,dia,dia,face=fc)
    m=Image.new('L',(dia*4,dia*4),0);ImageDraw.Draw(m).ellipse([0,0,dia*4-1,dia*4-1],fill=255);m=m.resize((dia,dia),Image.LANCZOS)
    o=Image.new('RGB',(dia+2*bw,dia+2*bw),NAVY);om=Image.new('L',(dia+2*bw,dia+2*bw),0)
    ImageDraw.Draw(om).ellipse([0,0,dia+2*bw-1,dia+2*bw-1],fill=255);im.paste(o,(x-bw,y-bw),om);im.paste(c,(x,y),m)
import csv
CSV=list(csv.DictReader(open(R+'grammy_out/ranked.csv',encoding='utf-8')))
def V(cat,nom):
    for r in CSV:
        if r['category']==cat and r['nominee']==nom: return int(r['streams'])
    raise KeyError((cat,nom))
def photofile(path):
    p=Image.open(path).convert('RGB');w,h=p.size;q=min(w,h);l=(w-q)//2;t=int((h-q)*0.12) if h>w else 0
    return p.crop((l,t,l+q,t+q)).resize((1280,1280),Image.LANCZOS)
_photo=photo
AN='/mnt/user-data/outputs/approved_new/'
def photo(name,k=0):
    if name.startswith('new:'):return photofile(AN+name[4:]+'/1.jpg')
    return _photo(name,k)
def columns(title,items,fn,circ,W=1800,bw=168,gap=27,mx=900,cx=1300,cd=440):
    H=1480;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((143,62+(0 if len(title)<32 else 8)),title,font=F('Bold',58 if len(title)<32 else 50),fill=NAVY)
    d.text((143,138),SUBT,font=F('Medium',30),fill=SUB)
    base=1255;x0=143 if len(items)>4 else (W-(len(items)*bw+(len(items)-1)*gap))//2
    for i,(t,a,v,ph) in enumerate(items):
        h=max(60,round(mx*sc(v,items[0][2])));x=x0+i*(bw+gap)
        p=photo(ph).resize((1280,1280));im.paste(cover_fit(p,bw,h,face=FACE.get(ph,(0.5,0.35))),(x,base-h))
        ctext(d,x+bw/2,base-h-62,fmt(v),F('Bold',44),NAVY)
        ls=wrap(d,t,F('Medium',27),bw+gap-4)
        for j,l in enumerate(ls):ctext(d,x+bw/2,base+14+j*34,l,F('Medium',27),(28,40,60))
        ctext(d,x+bw/2,base+14+len(ls)*34+4,a,F('Regular',24),SUB)
    circle(im,circ,cx,40,cd)
    ctext(d,W/2,1415,"@PopByNumbers",F('Bold',36),NAVY)
    im.convert('RGB').save(OUTD+fn,quality=94)
def kali2(title,items,fn,mode='inside',rh=104,bh=88):
    W=1080;top=215;n=len(items);H=top+n*rh+120;im=Image.new('RGB',(W,H),(0,0,0));d=ImageDraw.Draw(im)
    ctext(d,W/2,36,title,F('Bold',66),(200,100,255))
    ctext(d,W/2,128,"2027 Grammy nominees, ranked by total Spotify streams",F('Regular',26),(150,150,150))
    d.line([(40,186),(1040,186)],fill=(45,45,45),width=1);bx=190;bmax=745
    for i,(t,v,ph,col) in enumerate(items):
        y=top+i*rh-6;d.text((52,y+rh//2-22),str(i+1),font=F('Regular',22),fill=(150,150,150))
        c=photo(ph) if not ph.startswith('alb:') else Image.open(R+'albums/'+ph[4:]+'.jpg').convert('RGB')
        c=cover_fit(c,bh,bh);im.paste(c,(86,y+(rh-bh)//2))
        bl=max(40,round(bmax*sc(v,items[0][1])));by=y+(rh-bh)//2
        if mode=='above':
            f=F('SemiBold',24);d.text((bx,y+2),t,font=f,fill=(255,255,255));by=y+34;h=rh-52
            d.rectangle([bx,by,bx+bl,by+h],fill=col)
            s_=fmt(v);d.text((bx+bl+14,by+h/2-16),s_,font=F('SemiBold',28),fill=(255,255,255))
        else:
            d.rectangle([bx,by,bx+bl,by+bh],fill=col)
            f=F('SemiBold',28)
            if tw(d,t,f)+24<=bl:d.text((bx+14,by+bh/2-18),t,font=f,fill=(255,255,255))
            else:
                f2=F('SemiBold',21);ls=wrap(d,t,f2,bl-20)
                if len(ls)<=3 and all(tw(d,l,f2)<=bl-16 for l in ls):
                    for k,l in enumerate(ls):d.text((bx+10,by+bh/2-len(ls)*13+k*26+2),l,font=f2,fill=(255,255,255))
                else:d.text((bx+bl+14,by+bh/2-18),t,font=f,fill=(255,255,255))
            s_=fmt(v);d.text((1040-tw(d,s_,F('Regular',28)),by+bh/2-17),s_,font=F('Regular',28),fill=(255,255,255))
        d.line([(40,y+rh),(1040,y+rh)],fill=(45,45,45),width=1)
    ctext(d,W/2,H-70,"@PopByNumbers",F('Bold',34),(255,255,255));im.convert('RGB').save(OUTD+fn,quality=94)

PHO={"Taylor Swift":'taylor-swift#0',"Olivia Dean":'olivia-dean#0',"RAYE":'raye#1',"Ella Langley":'ella-langley#0',"Tame Impala":'tame-impala#3',"Bruno Mars":'bruno-mars#0',"Olivia Rodrigo":'olivia-rodrigo#0',"ROSALÍA":'rosalia#0',"Ariana Grande":'ariana-grande#0',"Slayyyter":'new:slayyyter',"Zara Larsson":'new:zara-larsson',"Madonna":'madonna#0',"Tinashe":'new:tinashe',"Lady Gaga":'lady-gaga#0'}
def songs(cat,sel=None):
    rs=[r for r in CSV if r['category']==cat]
    return sorted([(r['nominee'],r['artist'],int(r['streams'])) for r in rs],key=lambda x:-x[2])
def cols(cat,title,fn,circ=None,**kw):
    it=[(t,a,v,PHO[a]) for t,a,v in songs(cat)]
    columns(title,it,fn,circ or it[0][3],**kw)
import os;os.makedirs(OUTD,exist_ok=True)
for s in ['poppy','knocked-loose','megadeth','mastodon','anthrax','aerosmith','geese','the-rolling-stones','foo-fighters','bruce-springsteen','doechii']:pass
PHO.update({"Poppy":'new:poppy',"Knocked Loose":'new:knocked-loose',"Megadeth":'new:megadeth',"Mastodon":'new:mastodon',"Anthrax":'new:anthrax',"Phoebe Bridgers":'phoebe-bridgers#0',"Aerosmith":'new:aerosmith',"Geese":'new:geese',"The Rolling Stones":'new:the-rolling-stones',"Foo Fighters":'new:foo-fighters',"Bruce Springsteen":'new:bruce-springsteen'})
SUBT='x'
import re,unicodedata,os
def _slug(x):
    x=unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower().replace('&','and');return re.sub(r'[^a-z0-9]+','-',x).strip('-')
class P(dict):
    def __missing__(self,a):
        s=_slug(a);s={'mumford-and-sons':'mumford-sons','victoria-monet':'victoria-monet'}.get(s,s)
        return 'new:'+s if os.path.exists(AN+s+'/1.jpg') else s+'#0'
PHO["Tems"]="new:tems";FACE['new:jill-scott']=(0.5,0.40)
PHO=P(PHO)

PHO["Tems"]="new:tems"
import csv,collections,json,os
CATS=json.load(open('/tmp/g/cats.json'))['cats']
CATS.pop('Engineered Non-Classical',None)
def norm(a):
    m={'Rosalía':'ROSALÍA','Elena Rose':'Elena Rose'}
    return m.get(a.strip(),a.strip())
GROUPS={
'ALL':None,
'BIG4':['Record Of The Year','Album Of The Year','Song Of The Year','Best New Artist'],
'POP':['Best Pop Solo Performance','Best Pop Duo/Group Performance','Best Pop Vocal Album','Best Traditional Pop Vocal Performance','Best Traditional Pop Vocal Album','Best Dance Pop Recording'],
'ROCK':['Best Rock Performance','Best Metal Performance','Best Rock Song','Best Rock Album','Best Alternative Music Performance','Best Alternative Music Album'],
'RNB':['Best R&B Solo Performance','Best R&B Collaboration or Duo/Group Performance','Best Traditional R&B Performance','Best Progressive R&B Album','Best R&B Album','R&B Song'],
'RAP':['Best Rap Performance','Best Melodic Rap Performance','Best Rap Song','Best Rap Album'],
'COUNTRY':['Best Country Solo Performance','Best Country Duo/Group Performance','Best Country Song','Best Traditional Country Album','Best Contemporary Country Album','Best Contemporary Folk Album','Americana Performance','American Roots Performance','American Roots Song','Americana Album','Traditional Folk Album'],
'LATIN':['Best Latin Song','Best Latin Pop Album','Best Música Urbana Album','Best Latin Rock Or Alternative Album','Best Música Mexicana Album','Best Tropical Latin Album'],
'DANCE':['Best Dance/Electronic Recording','Best Dance Pop Recording','Best Dance/Electronic Album'],
}
OV={'Miranda Lambert':7,'Bruno Mars':6,'Madonna':5}
def counts(g):
    c=collections.Counter()
    for k,l in CATS.items():
        if GROUPS[g] is None or k in GROUPS[g]:
            for n in l:
                for a in set(map(norm,n)):c[a]+=1
    if g=='ALL':
        for a,v in OV.items():c[a]=v
    return c
def nomfig(g,minc=2,maxn=10):
    c=counts(g)
    return [(a,n) for a,n in sorted(c.items(),key=lambda x:(-x[1],x[0])) if n>=minc][:maxn]
OUTD='/mnt/user-data/outputs/grammy_nominations_v2/'
os.makedirs(OUTD,exist_ok=True)
fmt=lambda v:str(int(v))
FACE['new:jill-scott']=(0.5,0.40)
def fig(g,title,sub,fn,bw,gap,minc=2,maxn=10,cd=470,cx=1270):
    global SUBT
    SUBT=sub
    top=nomfig(g,minc,maxn)
    print(fn,top)
    items=[(a,'',n,PHO[a]) for a,n in top]
    columns(title,items,fn,items[0][3],W=1800,bw=bw,gap=gap,cx=cx,cd=cd)
FACE['rosalia#0']=(0.57,0.24);FACE['new:don-toliver']=(0.49,0.30);FACE['new:busta-rhymes']=(0.27,0.27)
FACE['new:durand-bernarr']=(0.72,0.28);FACE['new:geese']=(0.38,0.25);FACE['new:angine-de-poitrine']=(0.14,0.25)
print('KEYS',PHO['RAYE'],PHO['Tinashe'])
FACE['rosalia#0']=(0.63,0.24)
FACE[PHO['RAYE']]=(0.53,0.35);FACE[PHO['Tinashe']]=(0.33,0.40)
