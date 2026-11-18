import math
OUT='/mnt/user-data/outputs/top10_30/'
os.makedirs(OUT,exist_ok=True)
os.makedirs(OUT,exist_ok=True)
DZ.add('little-mix')
SD=R+'songs_data/'
def tot(slug):
    j=json.load(open(SD+slug+'.json'));return j['rows'][0]['streams']
def sg(slug):
    j=json.load(open(SD+slug+'.json'));return sorted(j['rows'][2:],key=lambda r:-r['streams'])
B=lambda v:f'{v/1e9:.1f}B'
B2=lambda v:f'{v/1e9:.2f}B'
PH={'Lana Del Rey':'lana-del-rey#1','Taylor Swift':'taylor-swift#0','Chappell Roan':'chappell-roan#0','Ice Spice':'ice-spice#1','Rihanna':'rihanna#2','Beyoncé':'beyonce#1','Shakira':'shakira#1','Ariana Grande':'ariana-grande#0','Billie Eilish':'billie-eilish#0','Bruno Mars':'bruno-mars#1','Lady Gaga':'lady-gaga#1','Mariah Carey':'mariah-carey#1','Selena Gomez':'selena-gomez#0','Miley Cyrus':'miley-cyrus#0','Demi Lovato':'demi-lovato#0','BLACKPINK':'blackpink#0','JENNIE':'jennie#0','LISA':'lisa#1','Michael Jackson':'michael-jackson#0','Whitney Houston':'whitney-houston#0','Nicki Minaj':'nicki-minaj#0','Cardi B':'cardi-b#0','Kehlani':'kehlani#0','Adele':'adele#0','Olivia Rodrigo':'olivia-rodrigo#0','Olivia Dean':'olivia-dean#0','Katy Perry':'katy-perry#0','Zara Larsson':'zara-larsson#0','Madonna':'madonna#0','Britney Spears':'britney-spears#0','Tate McRae':'tate-mcrae#1','Sabrina Carpenter':'sabrina-carpenter#1'}
def cpaste(im,key,cx,cy,d,ring=NAVY,rw=5):
    S=d
    ph=photo(key).resize((1280,1280));p=cover_fit(ph,S,S,face=FACE.get(key,(0.5,0.35)))
    m=Image.new('L',(S*4,S*4),0);ImageDraw.Draw(m).ellipse((0,0,S*4-1,S*4-1),fill=255);m=m.resize((S,S),Image.LANCZOS)
    rm=Image.new('L',((S+2*rw)*4,(S+2*rw)*4),0);ImageDraw.Draw(rm).ellipse((0,0,(S+2*rw)*4-1,(S+2*rw)*4-1),fill=255);rm=rm.resize((S+2*rw,S+2*rw),Image.LANCZOS)
    im.paste(Image.new('RGB',(S+2*rw,S+2*rw),ring),(int(cx-S/2-rw),int(cy-S/2-rw)),rm);im.paste(p,(int(cx-S/2),int(cy-S/2)),m)

OUT='/mnt/user-data/outputs/top10_30/'
os.makedirs(OUT,exist_ok=True)
ACC=(232,130,40);LIGHT=(200,212,232)
def head(d,W,t):
    ls=wrap(d,t,F('Bold',58),W-120)
    for j,l in enumerate(ls):ctext(d,W/2,56+j*68,l,F('Bold',58),NAVY)
    return 56+len(ls)*68+30
def foot(im,d,W,H,sub):
    ls=wrap(d,sub,F('Medium',32),W-140)
    y=H-100-len(ls)*44
    for j,l in enumerate(ls):ctext(d,W/2,y+j*44,l,F('Medium',32),(28,40,60))
    ctext(d,W/2,H-58,"@PopByNumbers",F('Bold',34),NAVY)
    return y
def pill(d,cx,cy,name,val,big=True):
    f1=F('Bold',26 if big else 22);f2=F('Bold',36 if big else 28)
    w=max(d.textlength(name,font=f1),d.textlength(val,font=f2))+30;h=(78 if big else 64)
    d.rounded_rectangle((cx-w/2,cy-h/2,cx+w/2,cy+h/2),14,fill=NAVY)
    ctext(d,cx,cy-h/2+6,name,f1,(200,212,232));ctext(d,cx,cy-h/2+(34 if big else 28),val,f2,(255,255,255))
def packcard(fn,title,items,sub,hi=None,scale=1300):
    # items: (name,value,valtxt); hi: name of comparator (accent ring)
    W,H=1080,1350;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    y0=head(d,W,title);ysub=H-100-len(wrap(d,sub,F('Medium',32),W-140))*44-20
    top=y0+10;bot=ysub-20
    mx=max(v for _,v,_ in items);cx0,cy0=W/2,(top+bot)/2
    while True:
        cs=[];ok=True
        for nm,v,vt in sorted(items,key=lambda x:-x[1]):
            r=scale/2*math.sqrt(v/mx)
            if not cs:
                if len(items)==1:r=min(r,(bot-top)/2-50,W/2-30)
                cs.append([cx0,cy0,r,nm,v,vt]);continue
            best=None
            for dist in range(0,900,4):
                for ang in range(0,360,3):
                    x=cx0+dist*math.cos(math.radians(ang));y=cy0+dist*math.sin(math.radians(ang))
                    if all(math.hypot(x-c[0],y-c[1])>=r+c[2]+30 for c in cs) and r+10<x<W-r-10 and top+r<y<bot-r-30:
                        best=(x,y);break
                if best:break
            if best is None:ok=False;break
            cs.append([best[0],best[1],r,nm,v,vt])
        if ok:break
        scale*=0.97
    mnY=min(c[1]-c[2] for c in cs);mxY=max(c[1]+c[2]+30 for c in cs);dy=(top+bot)/2-(mnY+mxY)/2
    for c in cs:c[1]+=dy
    for x,y,r,nm,v,vt in cs:
        cpaste(im,PH[nm],x,y,int(2*r),ring=ACC if nm==hi else NAVY,rw=6 if nm==hi else 3)
    d=ImageDraw.Draw(im)
    for x,y,r,nm,v,vt in cs:pill(d,x,y+r,nm,vt,big=r>=60)
    foot(im,d,W,H,sub)
    im.convert('RGB').save(OUT+fn,quality=94)
def ring(im,cx,cy,R,frac,w,col=ACC):
    SSx=4;S2=int(2*R+10)*SSx;lay=Image.new('RGBA',(S2,S2),(0,0,0,0));ld=ImageDraw.Draw(lay)
    c=S2/2;ld.ellipse((c-R*SSx,c-R*SSx,c+R*SSx,c+R*SSx),outline=LIGHT+(255,),width=w*SSx)
    ld.arc((c-R*SSx,c-R*SSx,c+R*SSx,c+R*SSx),-90,-90+360*frac,fill=col+(255,),width=w*SSx)
    lay=lay.resize((S2//SSx,S2//SSx),Image.LANCZOS);im.paste(lay,(int(cx-S2/SSx/2),int(cy-S2/SSx/2)),lay)
def ringcard(fn,title,items,sub):
    W,H=1080,1350;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    y0=head(d,W,title);n=len(items)
    R={1:250,3:165}[n];xs=[W/2] if n==1 else [W*(2*i+1)/6 for i in range(3)]
    cy=y0+R+40 if n==1 else y0+R+150
    for (nm,frac,big,lab),cx in zip(items,xs):
        w=int(R*0.17);ring(im,cx,cy,R-w//2,frac,w)
        cpaste(im,PH[nm],cx,cy,int(2*(R-w-12)),rw=0)
        d=ImageDraw.Draw(im)
        ctext(d,cx,cy+R+20,big,F('Bold',110 if n==1 else 84),NAVY)
        ctext(d,cx,cy+R+(150 if n==1 else 120),nm,F('Bold',40 if n==1 else 30),(28,40,60))
        if lab:ctext(d,cx,cy+R+(200 if n==1 else 160),lab,F('Medium',30 if n==1 else 24),SUB)
    foot(im,d,W,H,sub)
    im.convert('RGB').save(OUT+fn,quality=94)
def barcard(fn,title,groups,sub,line=None,unit=1e9,ymax=None):
    # groups: (name, [(label,value)]) ; vertical bars scaled from zero
    W,H=1080,1350;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    y0=head(d,W,title);n=len(groups)
    vm=ymax or max(v for _,bs in groups for _,v in bs)*1.05
    base=H-560;hmax=base-(y0+120)
    gw=W/n
    if line:
        ly=base-hmax*line/vm;d.line((40,ly,W-40,ly),fill=ACC,width=4);d.text((46,ly-34),f"{line/unit:.0f}B",font=F('Bold',28),fill=ACC)
    for gi,(nm,bs) in enumerate(groups):
        gx=gw*gi+gw/2;bw=min(95,(gw-50)/len(bs)-8)
        for bi,(lab,v) in enumerate(bs):
            x=gx+(bi-(len(bs)-1)/2)*(bw+10);h=hmax*v/vm
            d.rounded_rectangle((x-bw/2,base-h,x+bw/2,base),8,fill=PAL[(gi*2+1)%8] if False else (27,42,73) if gi%2==0 else (47,93,138))
            ctext(d,x,base-h-40,f"{v/unit:.2f}B",F('Bold',24 if n>2 else 28),NAVY)
        cpaste(im,PH[nm],gx,base+95,150,rw=4);d=ImageDraw.Draw(im)
        ctext(d,gx,base+185,nm,F('Bold',32),(28,40,60))
    foot(im,d,W,H,sub)
    im.convert('RGB').save(OUT+fn,quality=94)
TT={s:tot(s) for s in ['gracie-abrams','dua-lipa','ellie-goulding','sza','karol-g','sia','doja-cat','janet-jackson','megan-thee-stallion','anitta','kesha','halsey','lana-del-rey','michael-jackson','taylor-swift','chappell-roan','ice-spice','rihanna','beyonce','shakira','ariana-grande','billie-eilish','bruno-mars','lady-gaga','mariah-carey','selena-gomez','miley-cyrus','demi-lovato','blackpink','jennie','lisa','michael-jackson','whitney-houston','nicki-minaj','cardi-b','kehlani','adele','olivia-rodrigo','olivia-dean','katy-perry','zara-larsson','madonna','britney-spears','tate-mcrae','sabrina-carpenter']}
SS={s:sg(s) for s in TT}
sh3=lambda s:sum(r['streams'] for r in SS[s][:3])/TT[s]
n=lambda s,t:sum(1 for r in SS[s] if r['streams']>=t)


PH.update({'Gracie Abrams':'gracie-abrams#1','Dua Lipa':'dua-lipa#0','Ellie Goulding':'ellie-goulding#1','SZA':'sza#0','Karol G':'karol-g#1','Sia':'sia#0','Doja Cat':'doja-cat#0','Janet Jackson':'janet-jackson#0','Megan Thee Stallion':'megan-thee-stallion#0','Anitta':'anitta#0','Kesha':'kesha#0','Halsey':'halsey#0','Flowers':'miley-cyrus#0','Party In The U.S.A.':'miley-cyrus#0','Billie Jean':'michael-jackson#0','bad guy':'billie-eilish#0'})
def clean(s):
    seen={}
    for r in SS[s]:
        t=r['title']
        if ' - ' in t:continue
        if t not in seen:seen[t]=r['streams']
    return sorted(seen.values(),reverse=True)
def song(s,t):
    return [r['streams'] for r in SS[s] if r['title'].startswith(t)][0]
def sh1(s):return SS[s][0]['streams']/TT[s]

for _s in ['alicia-keys','lorde','charli-xcx','camila-cabello','jennifer-lopez']:
    TT[_s]=tot(_s);SS[_s]=sg(_s)
PH.update({'Alicia Keys':'alicia-keys#1','Lorde':'lorde#0','Charli xcx':'charli-xcx#0','Camila Cabello':'camila-cabello#0','Jennifer Lopez':'jennifer-lopez#1','Cruel Summer':'taylor-swift#0','Janet Jackson':'janet-jackson#0','Someone Like You':'adele#0','We Found Love':'rihanna#2','BIRDS OF A FEATHER':'billie-eilish#0','Espresso':'sabrina-carpenter#1','drivers license':'olivia-rodrigo#0','Kiss Me More (Doja Cat)':'doja-cat#0','Kiss Me More (SZA)':'sza#0','Taki Taki (Cardi B)':'cardi-b#0','Taki Taki (Selena Gomez)':'selena-gomez#0'})
def shk(s,k):return sum(r['streams'] for r in SS[s][:k])/TT[s]
def shb(s):return sum(r['streams'] for r in SS[s] if r['streams']>=1e9)/TT[s]
Pc=lambda x:f"{x*100:.0f}%"
def bars3(fn,title,arts,sub):
    barcard(fn,title,[(a,[(r['title'],r['streams']) for r in SS[s][:3]]) for a,s in arts],sub)
def dots(fn,title,artist,key,slug,thr,word,sub):
    W,H=1080,1350;im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    A=clean(slug);N=len(A);k=sum(1 for v in A if v>=thr)
    y0=head(d,W,title.format(k=k,N=N))
    cpaste(im,PH[key],W/2,y0+150,260,rw=6);d=ImageDraw.Draw(im)
    cols=10;gx=(W-cols*76)/2+38;gy=y0+400
    for i in range(N):
        x=gx+(i%cols)*76;y=gy+(i//cols)*76;d.ellipse((x-27,y-27,x+27,y+27),fill=ACC if i<k else LIGHT)
    foot(im,d,W,H,sub.format(k=k,N=N));im.convert('RGB').save(OUT+fn,quality=94);print(fn,k,N)

PH.update({'All I Want for Christmas':'mariah-carey#1','Obsessed':'mariah-carey#1','We Belong Together':'mariah-carey#1','Blank Space':'taylor-swift#0','Bad':'michael-jackson#0','Shallow':'lady-gaga#1','Rolling in the Deep':'adele#0','Umbrella':'rihanna#2','Halo':'beyonce#1','good 4 u':'olivia-rodrigo#0','Dark Horse':'katy-perry#0','White Horse':'taylor-swift#0','HOT TO GO!':'chappell-roan#0','Cold Heart':'dua-lipa#0','7 rings':'ariana-grande#0','Please Please Please':'sabrina-carpenter#1','I Wanna Dance with Somebody':'whitney-houston#0','I Will Always Love You':'whitney-houston#0','Die With A Smile':'bruno-mars#1'})
POP=8.2e9
yrs=lambda v,m=3.5:v*m/60/24/365
yl=lambda y:f"{y/1e3:.0f}K years" if y>=1e4 else f"{y:,.0f} years"
def sg1(s,t,exact=False):
    return [r['streams'] for r in SS[s] if (r['title']==t if exact else r['title'].startswith(t))][0]
POP=8.2e9
EX=json.load(open('/tmp/g/extra.json'))
AD='/mnt/user-data/uploads/PopByNumbers/repo/albums_data/'
def AL(s):
    d_={}
    for r in json.load(open(AD+s+'.json'))['rows']:d_.setdefault(r['title'],r['streams'])
    return d_
def EXS(k):return sorted([(t.lstrip('* ').strip(),v) for t,v in EX[k]['songs']],key=lambda x:-x[1])
def exs(k,t):return [v for tt,v in EXS(k) if tt==t][0]
fmt=lambda v:f"{v/1e9:.2f}B" if v>=1e9 else f"{v/1e6:.0f}M"
def pk(label,key):PH[label]=key;return label
PHK={'DY':'daddy-yankee#0','BB':'bad-bunny#0','BTS':'bts#0','BG':'becky-g#3','RO':'rosalia#0','BM':'babymonster#0','KG':'karol-g#1','SH':'shakira#1','AN':'anitta#0','BP':'blackpink#0','JE':'jennie#0','LI':'lisa#1'}
for k,v in {'Daddy Yankee':'DY','Bad Bunny':'BB','BTS':'BTS','Becky G':'BG','Rosalía':'RO','BABYMONSTER':'BM','Karol G':'KG','Shakira':'SH','Anitta':'AN','BLACKPINK':'BP','JENNIE':'JE','LISA':'LI'}.items():PH[k]=PHK[v]
def pc(fn,title,items,sub,hi=None):
    packcard(fn,title,[(pk(l,PHK[p]),v,t or fmt(v)) for l,p,v,t in items],sub,hi=hi)
def rc(fn,title,items,sub):
    ringcard(fn,title,[(pk(l,PHK[p]),f,b,lab) for l,p,f,b,lab in items],sub)
PHK.update({'GA':'lady-gaga#1','TS':'taylor-swift#0','OR':'olivia-rodrigo#0','AG':'ariana-grande#0','RI':'rihanna#2','BE':'beyonce#1','BI':'billie-eilish#0','SE':'selena-gomez#0','MI':'miley-cyrus#0','KP':'katy-perry#0','DU':'dua-lipa#0','SC':'sabrina-carpenter#1','CR':'chappell-roan#0','MA':'madonna#0','BR':'britney-spears#0','MC':'mariah-carey#1','TM':'tate-mcrae#1','AD':'adele#0','WH':'whitney-houston#0','HA':'halsey#0','CA':'camila-cabello#0','LO':'lorde#0','LA':'lana-del-rey#1','OD':'olivia-dean#0','GR':'gracie-abrams#1','JL':'jennifer-lopez#1','SZ':'sza#0'})
def LD(s):
    rows=json.load(open(SD+s+'.json'))['rows'];return rows[0]['streams'],rows[1]['streams'],sorted(rows[2:],key=lambda r:-r['streams'])
D={}
for k,s in {'TS':'taylor-swift','OR':'olivia-rodrigo','AG':'ariana-grande','RI':'rihanna','BE':'beyonce','BI':'billie-eilish','SE':'selena-gomez','MI':'miley-cyrus','KP':'katy-perry','DU':'dua-lipa','SC':'sabrina-carpenter','CR':'chappell-roan','MA':'madonna','BR':'britney-spears','MC':'mariah-carey','TM':'tate-mcrae','AD':'adele','WH':'whitney-houston','HA':'halsey','CA':'camila-cabello','LO':'lorde','LA':'lana-del-rey','OD':'olivia-dean','GR':'gracie-abrams','JL':'jennifer-lopez','GA':'lady-gaga'}.items():D[k]=LD(s)
tt=lambda k:D[k][0];dl=lambda k:D[k][1];sx=lambda k,i=0:D[k][2][i]
def st(k,t):return [r['streams'] for r in D[k][2] if r['title'].startswith(t)][0]
n1=lambda k,th=1e9:sum(r['streams']>=th for r in D[k][2])
PHK.update({'NM':'nicki-minaj#0','DC':'doja-cat#0','HA':'halsey#0'})
for k,s in {'NM':'nicki-minaj','DC':'doja-cat','LA':'lana-del-rey','SZ':'sza'}.items():D[k]=LD(s)
PH.update({'Nicki Minaj':'nicki-minaj#0','Doja Cat':'doja-cat#0','SZA':'sza#0'})
cl_=lambda t:re.sub(r'\s*[\(\[].*','',t).split(' - ')[0].strip()
def tops(k,i):return cl_(sx(k,i)['title']),sx(k,i)['streams']
def t3(fn,title,k,sub,fix=None):
    items=[]
    for i in range(3):
        t,v=tops(k,i);t=(fix or {}).get(t,t);items.append((t,k,v,fmt(v)))
    pc(fn,title,items,sub)
D['SZ']=LD('sza');D['HA']=LD('halsey');D['SC']=LD('sabrina-carpenter');D['DC']=LD('doja-cat')
SDD={'JE':'jennie','LI':'lisa','BP':'blackpink','RO':'rosalia','SH':'shakira','AN':'anitta','KG':'karol-g'}
for k,s in SDD.items():D[k]=LD(s)
W_,H_=1080,1350
def newc(title,sub):
    im=Image.new('RGB',(W_,H_),BG);d=ImageDraw.Draw(im);y0=head(d,W_,title)
    ysub=H_-100-len(wrap(d,sub,F('Medium',32),W_-140))*44-20
    return im,d,y0,ysub
def finish(im,d,sub,fn):
    foot(im,d,W_,H_,sub);im.convert('RGB').save(OUT+fn,quality=94)
def rpaste(im,key,x,y,w,h):
    w=int(w);h=int(h);ph=photo(key).resize((1280,1280));p=cover_fit(ph,w,h,face=FACE.get(key,(0.5,0.35)));im.paste(p,(int(x),int(y)))
def squarify(vals,x,y,w,h):
    # vals sorted desc, returns rects
    tot=sum(vals);sc=w*h/tot;a=[v*sc for v in vals];out=[]
    def worst(row,side):
        s=sum(row);return max(max(side*side*r/(s*s),s*s/(side*side*r)) for r in row)
    i=0
    while i<len(a):
        side=min(w,h);row=[a[i]];j=i+1
        while j<len(a) and worst(row+[a[j]],side)<=worst(row,side):row.append(a[j]);j+=1
        s=sum(row)
        if w>=h:
            cw=s/h;yy=y
            for r in row:rh=r/cw;out.append((x,yy,cw,rh));yy+=rh
            x+=cw;w-=cw
        else:
            ch=s/w;xx=x
            for r in row:rw=r/ch;out.append((xx,y,rw,ch));xx+=rw
            y+=ch;h-=ch
        i+=len(row)
    return out
def treemap(fn,title,items,sub):
    # items (label,pcode,value,valtxt)
    im,d,y0,ysub=newc(title,sub);items=sorted(items,key=lambda x:-x[2])
    rects=squarify([v for _,_,v,_ in items],30,y0+10,W_-60,ysub-20-(y0+10))
    for (l,p,v,t),(x,y,w,h) in zip(items,rects):
        rpaste(im,PHK[p],x,y,w,h)
    d=ImageDraw.Draw(im)
    for (l,p,v,t),(x,y,w,h) in zip(items,rects):
        d.rectangle((x,y,x+w,y+h),outline=BG,width=5)
        big=min(w,h)>=190
        pill(d,x+w/2,y+h-(52 if big else 40),l,t,big=big)
    finish(im,d,sub,fn)
def waffle(fn,title,p,frac,lab,sub):
    im,d,y0,ysub=newc(title,sub);cell=46;gap=5;gw=10*cell+9*gap;gx=(W_-gw)/2;gy=y0+310
    cpaste(im,PHK[p],W_/2,y0+110,190,rw=6);d=ImageDraw.Draw(im)
    k=round(frac*100)
    for i in range(100):
        r_,c_=divmod(i,10);x=gx+c_*(cell+gap);y=gy+(9-r_)*(cell+gap)
        d.rounded_rectangle((x,y,x+cell,y+cell),8,fill=ACC if i<k else LIGHT)
    ctext(d,W_/2,gy-72,f"{frac*100:.0f}%",F('Bold',64),NAVY)
    finish(im,d,sub,fn)
def stacked(fn,title,rows,sub):
    # rows (label,pcode,[(frac,label)])
    im,d,y0,ysub=newc(title,sub);n=len(rows);rh=(ysub-60-(y0+120))/n
    cols=[ACC,(27,42,73),(79,143,192),LIGHT];names=['Biggest song','Songs 2 to 3','Songs 4 to 10','All other songs']
    for i,(l,p,fr) in enumerate(rows):
        cy=y0+120+i*rh+rh/2;cpaste(im,PHK[p],110,cy,min(110,int(rh-30)),rw=3);d=ImageDraw.Draw(im)
        x=200;bw=W_-240;bh=min(80,rh-50)
        d.text((x,cy-bh/2-34),l,font=F('Bold',28),fill=NAVY)
        for j,f in enumerate(fr):
            w=bw*f;d.rectangle((x,cy-bh/2+4,x+w,cy+bh/2+4),fill=cols[j])
            if w>70:ctext(d,x+w/2,cy+4-18,f"{f*100:.0f}%",F('Bold',32),(255,255,255) if j!=3 else NAVY)
            x+=w
    lx=60;ly=ysub-48
    for j in range(4):
        d.rectangle((lx,ly,lx+26,ly+26),fill=cols[j]);d.text((lx+36,ly-2),names[j],font=F('Medium',24),fill=(28,40,60));lx+=255
    finish(im,d,sub,fn)
def sqpack(fn,title,items,sub,scale=1000):
    im,d,y0,ysub=newc(title,sub);items=sorted(items,key=lambda x:-x[2]);mx=items[0][2];top=y0+10;bot=ysub-20;cx0,cy0=W_/2,(top+bot)/2
    while True:
        cs=[];ok=True
        for l,p,v,t in items:
            s=scale*math.sqrt(v/mx)/1.6
            if not cs:cs.append([cx0,cy0,s,l,p,v,t]);continue
            best=None
            for dist in range(0,900,4):
                for ang in range(0,360,3):
                    x=cx0+dist*math.cos(math.radians(ang));y=cy0+dist*math.sin(math.radians(ang))
                    if all(max(abs(x-c[0]),abs(y-c[1]))>=(s+c[2])/2+24 for c in cs) and s/2+10<x<W_-s/2-10 and top+s/2<y<bot-s/2-30:best=(x,y);break
                if best:break
            if best is None:ok=False;break
            cs.append([best[0],best[1],s,l,p,v,t])
        if ok:break
        scale*=0.97
    mn=min(c[1]-c[2]/2 for c in cs);mxy=max(c[1]+c[2]/2+30 for c in cs);dy=(top+bot)/2-(mn+mxy)/2
    for c in cs:c[1]+=dy
    for x,y,s,l,p,v,t in cs:rpaste(im,PHK[p],x-s/2,y-s/2,s,s)
    d=ImageDraw.Draw(im)
    for x,y,s,l,p,v,t in cs:
        d.rectangle((x-s/2,y-s/2,x+s/2,y+s/2),outline=NAVY,width=3);pill(d,x,y+s/2,l,t,big=s>=130)
    finish(im,d,sub,fn)
def podium(fn,title,items,sub):
    im,d,y0,ysub=newc(title,sub);order=[1,0,2];hs={0:420,1:300,2:220};bw=300;base=ysub-40
    for pos,idx in enumerate(order):
        l,p,v,t=items[idx];x=W_/2+(pos-1)*(bw+10);h=hs[idx]
        d.rectangle((x-bw/2,base-h,x+bw/2,base),fill=NAVY if idx==0 else (47,93,138) if idx==1 else (79,143,192))
        ctext(d,x,base-h+20,f"#{idx+1}",F('Bold',90),(255,255,255))
        cpaste(im,PHK[p],x,base-h-130,220,rw=5);d=ImageDraw.Draw(im)
        pill(d,x,base-h+210 if idx==0 else base-h+190,l,t,big=True)
    finish(im,d,sub,fn)
def lolli(fn,title,items,sub):
    im,d,y0,ysub=newc(title,sub);items=sorted(items,key=lambda x:-x[2]);n=len(items);rh=(ysub-30-(y0+20))/n;mx=items[0][2];x0=60;xm=W_-330
    for i,(l,p,v,t) in enumerate(items):
        cy=y0+20+i*rh+rh/2;xe=x0+(xm-x0)*v/mx
        d.rounded_rectangle((x0,cy-6,xe,cy+6),6,fill=NAVY)
        cpaste(im,PHK[p],xe,cy,int(min(rh-14,100)),rw=3);d=ImageDraw.Draw(im)
        d.text((xe+min(rh-14,100)/2+16,cy-14),t,font=F('Bold',38),fill=NAVY,anchor='lm');d.text((xe+min(rh-14,100)/2+16,cy+24),l,font=F('Medium',26),fill=(28,40,60),anchor='lm')
    finish(im,d,sub,fn)
def tower(fn,title,items,sub):
    im,d,y0,ysub=newc(title,sub);n=len(items);mx=max(v for _,_,v,_ in items);base=ysub-250;avail=base-(y0+80);bh=min(34,avail/mx-4);colw=W_/n
    for i,(l,p,v,t) in enumerate(items):
        cx=colw*i+colw/2
        for k in range(v):
            yy=base-(k+1)*(bh+4)+4;d.rounded_rectangle((cx-colw*0.3,yy,cx+colw*0.3,yy+bh),4,fill=ACC if k%2==0 else (232,160,90))
        cpaste(im,PHK[p],cx,base+80,130,rw=4);d=ImageDraw.Draw(im)
        ctext(d,cx,base-v*(bh+4)-52,str(v),F('Bold',44),NAVY)
        ctext(d,cx,base+170,l,F('Bold',24),(28,40,60))
    finish(im,d,sub,fn)
