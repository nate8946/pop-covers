import math
from PIL import ImageDraw
OUT='/mnt/user-data/outputs/fun20g/'
os.makedirs(OUT,exist_ok=True)

DT='Nov 16 and 17'
def foot(im,d,W,H,sub):
    sub=sub.replace('{DT}',DT)
    ls=wrap(d,sub,F('Medium',22),W-140)
    y=H-80-len(ls)*30
    for j,l in enumerate(ls):ctext(d,W/2,y+j*30,l,F('Medium',22),(60,72,95))
    ctext(d,W/2,H-52,"@PopByNumbers",F('Bold',30),NAVY)
    return y
def newc(title,sub):
    sub=sub.replace('{DT}',DT)
    im=Image.new('RGB',(W_,H_),BG);d=ImageDraw.Draw(im);y0=head(d,W_,title)
    ysub=H_-80-len(wrap(d,sub,F('Medium',22),W_-140))*30-14
    return im,d,y0,ysub

def trunc(d,t,f,w):
    if d.textlength(t,font=f)<=w:return t
    while len(t)>3 and d.textlength(t+'…',font=f)>w:t=t[:-1]
    return t.rstrip()+'…'
exec(open('/tmp/g/st25.py').read())
PHC={'kesha':'kesha#0','cardi-b':'cardi-b#0','adele':'adele#0','olivia-rodrigo':'olivia-rodrigo#0','dua-lipa':'dua-lipa#0','taylor-swift':'taylor-swift#0','doja-cat':'doja-cat#0','lana-del-rey':'lana-del-rey#1','selena-gomez':'selena-gomez#0','ariana-grande':'ariana-grande#0','halsey':'halsey#0','madonna':'madonna#0','camila-cabello':'camila-cabello#0','bruno-mars':'bruno-mars#1','katy-perry':'katy-perry#1','demi-lovato':'demi-lovato#0','rihanna':'rihanna#2','billie-eilish':'billie-eilish#0','gracie-abrams':'gracie-abrams#0','kehlani':'kehlani#0','alicia-keys':'alicia-keys#1','nicki-minaj':'nicki-minaj#0','mariah-carey':'mariah-carey#1','chappell-roan':'chappell-roan#0','miley-cyrus':'miley-cyrus#0','tate-mcrae':'tate-mcrae#1','sabrina-carpenter':'sabrina-carpenter#1','lady-gaga':'lady-gaga#1','meghan-trainor':'meghan-trainor#0','karol-g':'karol-g#1','whitney-houston':'whitney-houston#0','beyonce':'beyonce#1','michael-jackson':'michael-jackson#0','jennie':'jennie#0','lisa':'lisa#1','jennifer-lopez':'jennifer-lopez#0','ice-spice':'ice-spice#1','shakira':'shakira#1','megan-thee-stallion':'megan-thee-stallion#0'}
PHC.update({'charli-xcx':'charli-xcx#0','rosalia':'rosalia#0','zara-larsson':'zara-larsson#0','lorde':'lorde#0','sza':'sza#0','ellie-goulding':'ellie-goulding#0','olivia-dean':'olivia-dean#0'})
PHK.update(PHC)

def lolli2(fn,title,items,sub):
    im,d,y0,ysub=newc(title,sub);items=sorted(items,key=lambda x:-x[2]);n=len(items);rh=min((ysub-30-(y0+20))/n,110);mx=items[0][2];x0=50;xm=W_-690
    top=y0+20+((ysub-30-(y0+20))-rh*n)/2;dd=int(min(rh-14,100));f1=F('Medium',27)
    for i,(l,p,v,t) in enumerate(items):
        cy=top+i*rh+rh/2;xe=x0+140+(xm-x0-140)*v/mx
        d.rounded_rectangle((x0,cy-6,xe,cy+6),6,fill=NAVY if i else ACC)
        cpaste(im,PHK[p],xe,cy,dd,rw=3);d=ImageDraw.Draw(im)
        sx_=xe+dd/2+16
        d.text((sx_,cy-17),t,font=F('Bold',38),fill=NAVY,anchor='lm')
        d.text((sx_,cy+22),trunc(d,l,f1,W_-24-sx_),font=f1,fill=(28,40,60),anchor='lm')
    finish(im,d,sub,fn)
def tower2(fn,title,items,sub):
    im,d,y0,ysub=newc(title,sub);n=len(items);mx=max(v for _,_,v,_ in items);base=ysub-230;avail=base-(y0+90);bh=min(78,avail/mx-5);colw=W_/n
    for i,(l,p,v,t) in enumerate(items):
        cx=colw*i+colw/2
        for k in range(v):
            yy=base-(k+1)*(bh+5)+5;d.rounded_rectangle((cx-colw*0.34,yy,cx+colw*0.34,yy+bh),6,fill=ACC if k%2==0 else (232,160,90))
        ctext(d,cx,base-v*(bh+5)-58,str(v),F('Bold',48),NAVY)
        cpaste(im,PHK[p],cx,base+70,int(colw*0.82),rw=4);d=ImageDraw.Draw(im)
        ls=wrap(d,l,F('Bold',25),colw-8)
        for j,x in enumerate(ls):ctext(d,cx,base+70+colw*0.41+16+j*30,x,F('Bold',25),(28,40,60))
    finish(im,d,sub,fn)
def nm(s):return DATA[s]['name'].replace('Sza','SZA')
def sv(s,t):
    for c,v,fe in CL[s]:
        if c.lower()==t.lower():return v
    raise KeyError((s,t))
def dfmt(d):return f'{round(d/1e3)}K' if d<1e6 else f'{d/1e6:.1f}M'
def poss(n):return n+"'S"
N=[0]
def nxt():N[0]+=1;return f'{N[0]:02d}.jpg'
def twin(a,ta,b,tb,disp=None):
    va,vb=sv(a,ta),sv(b,tb);d=abs(va-vb);da,db=(disp or (ta,tb))
    pc(nxt(),f"{poss(nm(a)).upper()} {da.upper()} AND {poss(nm(b)).upper()} {db.upper()} ARE {dfmt(d)} STREAMS APART",[(da,a,va,fmt(va)),(db,b,vb,fmt(vb))],f"{da} has {va/1e9:.3f}B and {db} has {vb/1e9:.3f}B on Spotify. Data from kworb as of {DT}.")
    print(N[0],'twin',nm(a),da,va,nm(b),db,vb,d)
twin('kesha','TiK ToK','cardi-b','I Like It')
twin('adele','Someone Like You','olivia-rodrigo','good 4 u')
twin('dua-lipa','New Rules','taylor-swift','Blank Space')
twin('doja-cat','Kiss Me More','lana-del-rey','Summertime Sadness')
twin('selena-gomez','It Ain’t Me','ariana-grande','positions',("It Ain't Me",'positions'))
twin('halsey','Boy With Luv','madonna','Popular')
twin('camila-cabello','Señorita','bruno-mars',"That's What I Like")
def totpair(a,b,key,word,unit):
    va,vb=DATA[a][key],DATA[b][key];d=abs(va-vb)
    f=(lambda v:f'{v/1e9:.3f}B') if key=='tot' else (lambda v:f'{v/1e6:.2f}M')
    ff=(lambda v:fmt(v)) if key=='tot' else (lambda v:f'{v/1e6:.2f}M')
    pc(nxt(),f"{nm(a).upper()} AND {nm(b).upper()} ARE {dfmt(d)} {word} APART",[(nm(a),a,va,ff(va)),(nm(b),b,vb,ff(vb))],f"{nm(a)} has {f(va)} and {nm(b)} has {f(vb)} {unit} on Spotify. Data from kworb as of {DT}.")
    print(N[0],'pair',nm(a),va,nm(b),vb,d)
totpair('gracie-abrams','kehlani','tot','STREAMS','total streams')
totpair('kesha','alicia-keys','tot','STREAMS','total streams')
totpair('nicki-minaj','lana-del-rey','tot','STREAMS','total streams')
totpair('meghan-trainor','whitney-houston','daily','DAILY STREAMS','daily streams')
totpair('cardi-b','chappell-roan','daily','DAILY STREAMS','daily streams')
# songs to 10B
def kto(s):
    c=0
    for k,(t,v,fe) in enumerate(DATA[s]['rows'],1):
        c+=v
        if c>=10e9:return k
SLL=[('billie-eilish','Billie Eilish'),('bruno-mars','Bruno Mars'),('taylor-swift','Taylor Swift'),('rihanna','Rihanna'),('ariana-grande','Ariana Grande'),('selena-gomez','Selena Gomez'),('camila-cabello','Camila Cabello'),('doja-cat','Doja Cat')]
tower2(nxt(),'SONGS NEEDED TO REACH 10 BILLION STREAMS',[(l,s,kto(s),str(kto(s))) for s,l in SLL],'Each block is one song, biggest first, added until the total passes 10 billion Spotify streams. Data from kworb as of {DT}.')
print(N[0],'tower',[(s,kto(s)) for s,l in SLL])
# ratio
rat=[]
for s,lab in [('jennie','JENNIE'),('mariah-carey','Mariah Carey'),('shakira','Shakira'),('chappell-roan','Chappell Roan'),('megan-thee-stallion','Megan Thee Stallion'),('charli-xcx','Charli XCX'),('sabrina-carpenter','Sabrina Carpenter'),('gracie-abrams','Gracie Abrams')]:
    a,b=CL[s][0],CL[s][1];rat.append((f"{a[0]} over {b[0]}",s,a[1]/b[1],f"{a[1]/b[1]:.1f}x"))
lolli2(nxt(),"HOW MANY TIMES BIGGER AN ARTIST'S BIGGEST SONG IS THAN THEIR SECOND-BIGGEST",rat,'Biggest song divided by second-biggest song on Spotify. Data from kworb as of {DT}.')
print(N[0],'ratio',[(a,b,c) for a,b,c,d in rat])
# near ties
for s,t1,t2 in [('katy-perry','Dark Horse','Last Friday Night'),('demi-lovato','Solo','Heart Attack')]:
    va,vb=sv(s,t1),sv(s,t2);d=va-vb
    pc(nxt(),f"{poss(nm(s)).upper()} TWO BIGGEST SONGS ARE {dfmt(d)} STREAMS APART",[(t1,s,va,fmt(va)),(t2,s,vb,fmt(vb))],f"{t1} has {va/1e9:.3f}B and {t2} has {vb/1e9:.3f}B on Spotify. Data from kworb as of {DT}.")
    print(N[0],'tie',s,va,vb,d)
# taylor > rihanna+billie
TSW,Rr,Bb=DATA['taylor-swift']['tot'],DATA['rihanna']['tot'],DATA['billie-eilish']['tot']
def trio(fn):
    im,d,y0,ysub=newc('TAYLOR SWIFT HAS MORE STREAMS THAN RIHANNA AND BILLIE EILISH COMBINED',f"Rihanna and Billie Eilish combined have {(Rr+Bb)/1e9:.2f}B total Spotify streams. Data from kworb as of {DT}.")
    avail=ysub-y0;RT=min(300,avail*0.36);R2=RT*math.sqrt(Rr/TSW);R3=RT*math.sqrt(Bb/TSW)
    cT=(30+RT,y0+avail*0.52);c2=(W_-30-R2,y0+R2+20);c3=(W_-30-R3,ysub-R3-70)
    for (cx,cy),R_,k in ((cT,RT,'taylor-swift'),(c2,R2,'rihanna'),(c3,R3,'billie-eilish')):cpaste(im,PHK[k],cx,cy,int(2*R_),rw=4)
    d=ImageDraw.Draw(im)
    for (cx,cy),R_,l,v in ((cT,RT,'Taylor Swift',TSW),(c2,R2,'Rihanna',Rr),(c3,R3,'Billie Eilish',Bb)):pill(d,cx,cy+R_,l,fmt(v),big=True)
    finish(im,d,f"Rihanna and Billie Eilish combined have {(Rr+Bb)/1e9:.2f}B total Spotify streams. Data from kworb as of {DT}.",fn)
trio(nxt())
print(N[0],'tay',TSW,Rr+Bb)
# days
d=DATA['taylor-swift']['daily']
ds=[]
for s,t in [('chappell-roan','Good Luck, Babe!'),('tate-mcrae','greedy'),('olivia-rodrigo','drivers license'),('sabrina-carpenter','Espresso'),('billie-eilish','BIRDS OF A FEATHER'),('lady-gaga','Die With A Smile')]:
    v=sv(s,t);ds.append((t,s,v/d,f"{round(v/d)} days"))
lolli2(nxt(),"DAYS OF TAYLOR SWIFT'S DAILY STREAMS NEEDED TO EQUAL ONE SONG",ds,f"Taylor Swift's catalog streams {d/1e6:.1f}M times a day on Spotify. Days are a song's total streams divided by that. Data from kworb as of {DT}.")
print(N[0],'days',[(a,round(c,1)) for a,b,c,e in ds])
# crossed / short of 1B
def gather(lo,hi):
    out=[]
    for s in DATA:
        if s in EXC:continue
        for c,v,fe in CL[s]:
            if lo<=v<hi:out.append((c,s,v))
    return sorted(out,key=lambda x:x[2])
cr=gather(1e9,1.02e9)
lolli2(nxt(),'SONGS THAT HAVE JUST PASSED 1 BILLION STREAMS',[(c,s,v,f'{v/1e9:.3f}B') for c,s,v in cr],'Songs with between 1.000B and 1.020B Spotify streams among the artists tracked. Data from kworb as of {DT}.')
print(N[0],'crossed',[(c,nm(s),v) for c,s,v in cr])
sh=gather(975e6,1e9)
lolli2(nxt(),'SONGS JUST SHORT OF 1 BILLION STREAMS',[(c,s,v,f'{v/1e6:.1f}M') for c,s,v in sh],'Songs with between 975M and 1.000B Spotify streams among the artists tracked. Data from kworb as of {DT}.')
print(N[0],'short',[(c,nm(s),v) for c,s,v in sh])
print('DONE',N[0])
