import math
from PIL import ImageDraw
OUT='/mnt/user-data/outputs/top10_30/'
os.makedirs(OUT,exist_ok=True)

def foot(im,d,W,H,sub):
    ls=wrap(d,sub,F('Medium',22),W-140)
    y=H-80-len(ls)*30
    for j,l in enumerate(ls):ctext(d,W/2,y+j*30,l,F('Medium',22),(60,72,95))
    ctext(d,W/2,H-52,"@PopByNumbers",F('Bold',30),NAVY)
    return y
def newc(title,sub):
    im=Image.new('RGB',(W_,H_),BG);d=ImageDraw.Draw(im);y0=head(d,W_,title)
    ysub=H_-80-len(wrap(d,sub,F('Medium',22),W_-140))*30-14
    return im,d,y0,ysub
SKIP=('emix','Live','live','Instrumental','Sped','Slowed','Acoustic','Version','Edit)')
def top10(rows):
    out=[];seen=set()
    for t,v in sorted(rows,key=lambda x:-x[1]):
        t2=re.sub('[\U0001F000-\U0001FFFF\u2500-\u25FF\u2600-\u2661\u2663-\u27BF\ufe0f]','',t.lstrip('* ').strip()).strip()
        if any(s in t2 for s in SKIP):continue
        c=cl_(t2)
        if not c:c=t2
        if c.lower() in seen:continue
        seen.add(c.lower());out.append((c,v))
        if len(out)==10:break
    return out
def trunc(d,t,f,w):
    if d.textlength(t,font=f)<=w:return t
    while len(t)>3 and d.textlength(t+'…',font=f)>w:t=t[:-1]
    return t.rstrip()+'…'
BLUES=[(255,255,255)]
PAL=[(232,130,40),(16,34,72),(30,60,110),(47,93,138),(79,143,192),(120,170,215),(150,190,225),(98,120,160),(60,80,120),(180,200,228)]
def row10(fn,title,key,items,sub):
    im,d,y0,ysub=newc(title,sub);n=len(items);top=y0+10;rh=(ysub-10-top)/n;mx=items[0][1];bh=min(rh-14,70);x0=40
    xm=W_-40-bh/2-16-150;fo=F('Bold',30)
    for i,(t,v) in enumerate(items):
        cy=top+i*rh+rh/2;L=380+(xm-380)*v/mx;xe=x0+L
        d.rounded_rectangle((x0,cy-bh/2,xe,cy+bh/2),bh/2.5,fill=NAVY if i else (232,130,40))
        d.text((x0+22,cy),trunc(d,t,fo,L-40-bh/2),font=fo,fill=(255,255,255),anchor='lm')
        cpaste(im,key,xe,cy,int(bh+10),rw=4);d=ImageDraw.Draw(im)
        d.text((xe+bh/2+22,cy),fmt(v),font=F('Bold',36),fill=NAVY,anchor='lm')
    finish(im,d,sub,fn)
def col10(fn,title,key,items,sub):
    im,d,y0,ysub=newc(title,sub);n=len(items);top=y0+10;base=ysub-345;colw=(W_-40)/n;mx=items[0][1]
    maxh=base-(top+84+60);fo=F('Bold',26)
    for i,(t,v) in enumerate(items):
        cx=20+colw*i+colw/2;h=140+(maxh-140)*v/mx
        d.rounded_rectangle((cx-colw*0.38,base-h,cx+colw*0.38,base),8,fill=ACC if i==0 else NAVY)
        ctext(d,cx,base-34,str(i+1),F('Bold',30),(255,255,255))
        cpaste(im,key,cx,base-h-48,int(colw*0.8),rw=3);d=ImageDraw.Draw(im)
        ctext(d,cx,base-h-48-colw*0.4-40,fmt(v),F('Bold',24),NAVY)
        tt_=trunc(d,t,fo,318);tw=int(d.textlength(tt_,font=fo))+6
        tmp=Image.new('RGBA',(tw,36),(0,0,0,0));ImageDraw.Draw(tmp).text((0,2),tt_,font=fo,fill=(28,40,60,255))
        tmp=tmp.rotate(-90,expand=True);im.paste(tmp,(int(cx-18),int(base+14)),tmp)
    finish(im,d,sub,fn)
def tree10(fn,title,key,items,sub):
    im,d,y0,ysub=newc(title,sub)
    rects=squarify([v for _,v in items],30,y0+10,W_-60,ysub-20-(y0+10))
    for (t,v),(x,y,w,h) in zip(items,rects):rpaste(im,key,x,y,w,h)
    d=ImageDraw.Draw(im)
    for i,((t,v),(x,y,w,h)) in enumerate(zip(items,rects)):
        d.rectangle((x,y,x+w,y+h),outline=BG,width=5)
        big=min(w,h)>=190;f1=F('Bold',26 if big else 22);f2=F('Bold',36 if big else 28)
        nm=trunc(d,t,f1,w-40);val=fmt(v)
        pw=max(d.textlength(nm,font=f1),d.textlength(val,font=f2))+24;ph=78 if big else 62
        cy=y+h-(52 if big else 40)
        d.rounded_rectangle((x+w/2-pw/2,cy-ph/2,x+w/2+pw/2,cy+ph/2),12,fill=NAVY if i else (190,95,20))
        ctext(d,x+w/2,cy-ph/2+5,nm,f1,(215,225,242));ctext(d,x+w/2,cy-ph/2+(32 if big else 26),val,f2,(255,255,255))
    finish(im,d,sub,fn)
def lolli10(fn,title,key,items,sub):
    im,d,y0,ysub=newc(title,sub);n=len(items);rh=(ysub-30-(y0+20))/n;mx=items[0][1];x0=60;xm=W_-420;dd=int(min(rh-14,100))
    f1=F('Medium',26)
    for i,(t,v) in enumerate(items):
        cy=y0+20+i*rh+rh/2;xe=x0+120+(xm-x0-120)*v/mx
        d.rounded_rectangle((x0,cy-6,xe,cy+6),6,fill=NAVY if i else ACC)
        cpaste(im,key,xe,cy,dd,rw=3);d=ImageDraw.Draw(im)
        d.text((xe+dd/2+16,cy-16),fmt(v),font=F('Bold',38),fill=NAVY,anchor='lm')
        d.text((xe+dd/2+16,cy+22),trunc(d,t,f1,W_-30-(xe+dd/2+16)),font=f1,fill=(28,40,60),anchor='lm')
    finish(im,d,sub,fn)
def donut10(fn,title,key,items,sub):
    im,d,y0,ysub=newc(title,sub);tot_=sum(v for _,v in items);cx=W_/2;R_=190;cy=y0+20+R_;SS_=3
    big=Image.new('RGBA',(2*R_*SS_,2*R_*SS_),(0,0,0,0));bd=ImageDraw.Draw(big);a=-90.0
    for i,(t,v) in enumerate(items):
        sw=360*v/tot_;bd.pieslice((0,0,2*R_*SS_-1,2*R_*SS_-1),a,a+sw,fill=PAL[i]+(255,));bd.arc((0,0,2*R_*SS_-1,2*R_*SS_-1),a,a+sw,fill=BG+(255,),width=0);a+=sw
    # separators
    a=-90.0
    for i,(t,v) in enumerate(items):
        x2=R_*SS_+R_*SS_*math.cos(math.radians(a));y2=R_*SS_+R_*SS_*math.sin(math.radians(a));bd.line((R_*SS_,R_*SS_,x2,y2),fill=BG+(255,),width=8);a+=360*v/tot_
    hole=Image.new('L',big.size,0);ImageDraw.Draw(hole).ellipse((R_*SS_-108*SS_,R_*SS_-108*SS_,R_*SS_+108*SS_,R_*SS_+108*SS_),fill=255)
    big.paste((0,0,0,0),(0,0),hole);big=big.resize((2*R_,2*R_),Image.LANCZOS);im.paste(big,(int(cx-R_),int(cy-R_)),big)
    cpaste(im,key,cx,cy,190,rw=5);d=ImageDraw.Draw(im)
    ly=cy+R_+26;rh=(ysub-4-ly)/10;f1=F('Medium',28);f2=F('Bold',28)
    for i,(t,v) in enumerate(items):
        y=ly+i*rh+rh/2;x=150
        d.rounded_rectangle((x,y-13,x+26,y+13),6,fill=PAL[i])
        d.text((x+44,y),trunc(d,f'{i+1}. {t}',f1,W_-150-44-150-110),font=f1,fill=(28,40,60),anchor='lm')
        d.text((W_-150,y),fmt(v),font=f2,fill=NAVY,anchor='rm')
    finish(im,d,sub,fn)
def pack10(fn,title,key,items,sub):
    PH.clear() if False else None
    its=[]
    for t,v in items:
        l=t if len(t)<=16 else t[:15].rstrip()+'…';its.append((pk(l,key),v,fmt(v)))
    packcard(fn,title,its,sub,scale=900)

def tiles10(fn,title,key,items,sub):
    im,d,y0,ysub=newc(title,sub);top=y0+10;gap=14;w=(W_-60-gap)/2;h=(ysub-10-top-4*gap)/5;mx=items[0][1];dd=int(h-34)
    f1=F('Bold',29);f2=F('Bold',40)
    for i,(t,v) in enumerate(items):
        c=i//5;r=i%5;x=30+c*(w+gap);y=top+r*(h+gap)
        d.rounded_rectangle((x,y,x+w,y+h),16,fill=(246,249,254),outline=NAVY,width=3)
        cpaste(im,key,x+18+dd/2,y+h/2-4,dd,rw=3);d=ImageDraw.Draw(im)
        d.ellipse((x+4,y+4,x+4+40,y+4+40),fill=ACC if i==0 else NAVY);ctext(d,x+24,y+8,str(i+1),F('Bold',26),(255,255,255))
        tx=x+18+dd+18;ls=wrap(d,t,f1,w-(tx-x)-14)[:2]
        ty=y+14
        for j,l in enumerate(ls):d.text((tx,ty+j*34),l,font=f1,fill=(28,40,60))
        d.text((tx,y+h-58),fmt(v),font=f2,fill=NAVY)
        d.rounded_rectangle((x+18,y+h-14,x+18+(w-36),y+h-8),3,fill=(214,222,238));d.rounded_rectangle((x+18,y+h-14,x+18+(w-36)*v/mx,y+h-8),3,fill=ACC if i==0 else NAVY)
    finish(im,d,sub,fn)
def ladder10(fn,title,key,items,sub):
    im,d,y0,ysub=newc(title,sub);top=y0+10;n=len(items);rh=(ysub-10-top)/n;mx=items[0][1];ph=rh-12;f1=F('Bold',32)
    for i,(t,v) in enumerate(items):
        y=top+i*rh+6;x0=30;x1=W_-30
        d.rounded_rectangle((x0,y,x1,y+ph),14,fill=(246,249,254))
        d.rounded_rectangle((x0,y,x0+(x1-x0)*v/mx,y+ph),14,fill=(200,212,232) if i else (246,190,140))
        ctext(d,x0+44,y+ph/2-24,str(i+1),F('Bold',44),NAVY)
        cpaste(im,key,x0+140,y+ph/2,int(ph-10),rw=3);d=ImageDraw.Draw(im)
        d.text((x0+200,y+ph/2),trunc(d,t,f1,x1-x0-200-170),font=f1,fill=(20,34,64),anchor='lm')
        d.text((x1-20,y+ph/2),fmt(v),font=F('Bold',38),fill=NAVY,anchor='rm')
    finish(im,d,sub,fn)
ENG=[row10,col10,tiles10,lolli10,donut10,ladder10]

# ---- data
FR=json.load(open('/tmp/k3/fresh.json'))
EXX=json.load(open('/tmp/g/extra.json'))
RAWL={}
for l in open('/home/claude/lk/raw.txt'):
    n_,r_=l.rstrip('\n').split('#',1);RAWL[n_]=[(x.rsplit('~',1)[0],int(x.rsplit('~',1)[1])*10**6) for x in r_.split('|')]
def src_sd(s):return [(r['title'],r['streams']) for r in LD(s)[2]]
def src_fr(k):return [(a.rsplit('|',1)[0],int(a.rsplit('|',1)[1])) for a in FR[k].strip().split('\n') if '|' in a]
def src_ex(k):return [(t,v) for t,v in EXX[k]['songs']]
def src_raw(n):return RAWL[n]
CARDS=[
('Selena Gomez','selena-gomez#0',lambda:src_sd('selena-gomez'),'Nov 10'),
('BTS','bts#0',lambda:src_fr('bts'),'Nov 15'),
('Madonna','madonna#0',lambda:src_sd('madonna'),'Nov 10'),
('Bad Bunny','bad-bunny#0',lambda:src_raw('Bad Bunny'),'Nov 11'),
('Whitney Houston','whitney-houston#0',lambda:src_sd('whitney-houston'),'Nov 10'),
('TWICE','twice#0',lambda:src_fr('twice'),'Nov 15'),
('Jennifer Lopez','jennifer-lopez#0',lambda:src_sd('jennifer-lopez'),'Nov 10'),
('Tini','tini#0',lambda:src_raw('Tini'),'Nov 11'),
('Gracie Abrams','gracie-abrams#0',lambda:src_sd('gracie-abrams'),'Nov 10'),
('NewJeans','newjeans#0',lambda:src_fr('newjeans'),'Nov 15'),
('Olivia Dean','olivia-dean#0',lambda:src_sd('olivia-dean'),'Nov 10'),
('Maria Becerra','maria-becerra#0',lambda:src_raw('Maria Becerra'),'Nov 11'),
('Kesha','kesha#0',lambda:src_sd('kesha'),'Nov 10'),
('SEVENTEEN','seventeen#0',lambda:src_fr('seventeen'),'Nov 15'),
('Alicia Keys','alicia-keys#1',lambda:src_sd('alicia-keys'),'Nov 10'),
('Nicki Nicole','nicki-nicole#0',lambda:src_raw('Nicki Nicole'),'Nov 11'),
('aespa','aespa#0',lambda:src_fr('aespa'),'Nov 15'),
('Ayra Starr','ayra-starr#0',lambda:src_ex('ayrastarr'),'Nov 9'),
('ENHYPEN','enhypen#0',lambda:src_fr('enhypen'),'Nov 15'),
('BABYMONSTER','babymonster#0',lambda:src_ex('babymonster'),'Nov 10'),
('IVE','ive#0',lambda:src_fr('ive'),'Nov 15'),
('Meghan Trainor','meghan-trainor#0',lambda:src_sd('meghan-trainor'),'Nov 10'),
('Stray Kids','stray-kids#0',lambda:src_fr('stray-kids'),'Nov 15'),
('EXO','exo#1',lambda:src_raw('EXO'),'Nov 11'),
('LE SSERAFIM','le-sserafim#0',lambda:src_fr('le-sserafim'),'Nov 15'),
('ATEEZ','ateez#1',lambda:src_raw('ATEEZ'),'Nov 11'),
('NCT DREAM','nct-dream#1',lambda:src_fr('nct-dream'),'Nov 15'),
('TOMORROW X TOGETHER','tomorrow-x-together#1',lambda:src_raw('TOMORROW X TOGETHER'),'Nov 11'),
('TREASURE','treasure#1',lambda:src_fr('treasure'),'Nov 15'),
('BIGBANG','bigbang#0',lambda:src_raw('BIGBANG'),'Nov 11'),
]
for n,(nm,key,fn_,dt) in enumerate(CARDS,1):
    it=top10(fn_())
    if len(it)<10:print('SHORT',nm,len(it))
    eng=ENG[(n-1)%6]
    sub=f"The ten most streamed songs on Spotify. Excludes remixes and live versions. Data from kworb as of {dt}."
    print(n,nm,eng.__name__,dt,[(a,fmt(b)) for a,b in it[:3]],len(it))
    eng(f'{n:02d}.jpg',f"{nm.upper()}: 10 MOST STREAMED SONGS",key,it,sub)
print('DONE')
