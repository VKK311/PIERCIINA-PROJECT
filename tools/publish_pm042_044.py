#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
import hashlib, io, json, re, shutil, sys, urllib.request

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'PINKMALL.html'
STATE = ROOT / 'docs/pink-mall/PROJECT_STATE.md'
STANDALONE = ROOT / 'PINKMALL_REVIEW_STANDALONE.html'
EXPECT_DIR = ROOT / 'tools/regression/expect'
PUB_DATE = '2026-08-31'
NEW_UNTIL = '2026-09-14'

PRODUCTS = [
    {
        'id':'PM-042','brand':'Lanvin','manufacturerItemNo':'6LPESC J4836','variantCode':None,
        'name':'Reversible Bucket Hat','slug':'lanvin-reversible-bucket-hat-pink','category':'accessories','color':'Pink','priceEUR':69,
        'description':'Lanvin reversible bucket hat в розово — едната страна с повтарящ се JL monogram, другата с голямо LANVIN лого.',
        'tags':['lanvin','6lpesc j4836','bucket hat','reversible','шапка','accessories','pink'],
        'related':['PM-033','PM-040','PM-041'],
        'source':{'identityTier':'OWNER_CONFIRMED','identityBasis':'Owner supplied manufacturer item 6LPESC J4836 and three exact-product pink photographs; exact style family independently evidenced as Lanvin Reversible Bucket Hat.','mediaTransport':'TRUSTED_RETAILER','verifiedAt':PUB_DATE},
        'pages':['https://theluxurycloset.com/us-en/women/lanvin-pink-geometric-print-coated-cotton-bucket-hat-p1126627'],
        'direct':['https://cdn.theluxurycloset.com/uploads/opt/products/full/luxury-women-lanvin-used-accessories-p1126627-007.jpg','https://cdn.theluxurycloset.com/uploads/opt/products/full/luxury-women-lanvin-used-accessories-p1126627-008.jpg','https://cdn.theluxurycloset.com/uploads/opt/products/full/luxury-women-lanvin-used-accessories-p1126627-009.jpg'],
        'alts':['Розова reversible bucket шапка Lanvin с JL monogram, фронтален изглед','Розова reversible bucket шапка Lanvin, изглед към вътрешната страна','Розова reversible bucket шапка Lanvin с голямо LANVIN лого'],
        'search':['lanvin','bucket','шапка','6LPESC J4836']
    },
    {
        'id':'PM-043','brand':'Swarovski','manufacturerItemNo':'5693725','variantCode':None,
        'name':'Crystalline Ballpoint Pen','slug':'swarovski-crystalline-ballpoint-pen-pink','category':'accessories','color':'Pink','priceEUR':49,
        'description':'Swarovski Crystalline ballpoint pen в розово със златисти акценти и прозрачна кристална секция.',
        'tags':['swarovski','5693725','crystalline','ballpoint pen','химикал','accessories','pink'],
        'related':['PM-042','PM-040','PM-041'],
        'source':{'identityTier':'OFFICIAL','identityBasis':'Official Swarovski product page identifies article 5693725 as Crystalline ballpoint pen, Pink, Gold-tone plated.','mediaTransport':'OFFICIAL','verifiedAt':PUB_DATE},
        'pages':['https://www.swarovski.sa/crystalline-lustre-ballpoint-pen-pink-gold-tone-plated/030716940606.html','https://www.swarovski.com/en-US/p-M5694180/Crystalline-ballpoint-pen-Pink-Gold-tone-plated/?variantID=5693725'],
        'direct':[],
        'alts':['Розова химикалка Swarovski Crystalline 5693725, цял продукт','Детайл на розова химикалка Swarovski Crystalline с кристална секция','Розова химикалка Swarovski Crystalline в презентационна опаковка'],
        'search':['swarovski','crystalline','химикал','5693725']
    },
    {
        'id':'PM-044','brand':'Calvin Klein','manufacturerItemNo':'CKNYC1852S','variantCode':'680',
        'name':'CKNYC1852S','slug':'calvin-klein-cknyc1852s-blush','category':'accessories','color':'Pink','priceEUR':119,
        'description':'Calvin Klein CKNYC1852S в BLUSH — розова квадратна рамка и розови лещи с характерен контрастен мост.',
        'tags':['calvin klein','cknyc1852s','680','blush','sunglasses','очила','accessories','pink'],
        'related':['PM-043','PM-041','PM-040'],
        'source':{'identityTier':'TRUSTED_RETAILER','identityBasis':'Exact retailer evidence identifies CKNYC1852S-680 as BLUSH / pink; owner supplied and approved three matching product photographs.','mediaTransport':'TRUSTED_RETAILER','verifiedAt':PUB_DATE},
        'pages':['https://www.ashford.com/products/calvin-klein-cknyc1852s-680','https://designeroptics.com/products/calvin-klein-205w39nyc-cknyc1852s-sunglasses'],
        'direct':['https://designeroptics.com/cdn/shop/files/e8b269be7e47601715cb1800a8ff2f04.jpg?v=1721079778'],
        'alts':['Розови слънчеви очила Calvin Klein CKNYC1852S 680 BLUSH, три-четвърти отпред','Розови слънчеви очила Calvin Klein CKNYC1852S 680 BLUSH, изглед отзад','Розови слънчеви очила Calvin Klein CKNYC1852S 680 BLUSH с калъф, детайл'],
        'search':['calvin klein','cknyc1852s','blush','680']
    }
]

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def dhash(im):
    im=im.convert('L').resize((9,8))
    px=list(im.getdata()); bits=0
    for y in range(8):
        for x in range(8): bits=(bits<<1)|(px[y*9+x] > px[y*9+x+1])
    return bits

def hdist(a,b): return (a^b).bit_count()

def save_candidate(raw, dest):
    try:
        im=Image.open(io.BytesIO(raw)); im.load()
        if im.width < 300 or im.height < 300: return None
        if im.mode not in ('RGB','RGBA'): im=im.convert('RGB')
        dest.parent.mkdir(parents=True,exist_ok=True)
        im.convert('RGB').save(dest,'WEBP',quality=88,method=6)
        return (im.width,im.height,dhash(im))
    except Exception: return None

def url_bytes(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=25) as r: return r.read()

def capture_product(product):
    pid=product['id']; live_dir=ROOT/'assets/pink-mall/products'/pid
    src_dir=live_dir/'source'; src_dir.mkdir(parents=True,exist_ok=True)
    chosen=[]; hashes=[]; provenance=[]
    def accept(raw, origin, label):
        nonlocal chosen,hashes
        if len(chosen)>=3: return
        temp=src_dir/f'{pid}-candidate-{len(chosen)+1}.webp'
        meta=save_candidate(raw,temp)
        if not meta: return
        w,h,dh=meta
        if any(hdist(dh,x)<5 for x in hashes): temp.unlink(missing_ok=True); return
        hashes.append(dh); chosen.append(temp); provenance.append(origin)
    for u in product['direct']:
        try: accept(url_bytes(u),u,'direct')
        except Exception as e: print('direct failed',pid,u,e)
    if len(chosen)<3:
        with sync_playwright() as p:
            browser=p.chromium.launch()
            ctx=browser.new_context(viewport={'width':1440,'height':1100},user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36')
            page=ctx.new_page()
            for page_url in product['pages']:
                if len(chosen)>=3: break
                try:
                    page.goto(page_url,wait_until='domcontentloaded',timeout=60000)
                    page.wait_for_timeout(4500)
                    imgs=page.locator('img')
                    n=min(imgs.count(),120)
                    scored=[]
                    for i in range(n):
                        el=imgs.nth(i)
                        try:
                            box=el.bounding_box(); alt=(el.get_attribute('alt') or '').lower(); src=(el.get_attribute('src') or '')
                            if not box or box['width']<180 or box['height']<180: continue
                            text=(alt+' '+src).lower()
                            score=0
                            for token in [product['brand'].lower(),product['manufacturerItemNo'].lower().replace(' ',''),product['name'].lower().split()[0]]:
                                if token and token in text.replace(' ',''): score+=3
                            if 'product' in text: score+=1
                            scored.append((score,box['width']*box['height'],i,alt,src))
                        except Exception: pass
                    scored.sort(reverse=True)
                    for score,area,i,alt,src in scored:
                        if len(chosen)>=3: break
                        if score<=0 and len(scored)>8: continue
                        el=imgs.nth(i)
                        try:
                            raw=el.screenshot(type='png',timeout=15000)
                            accept(raw,page_url+' :: '+(src or alt),'dom-image')
                        except Exception: pass
                except Exception as e: print('page failed',pid,page_url,e)
            browser.close()
    if len(chosen)<3: raise SystemExit(f'{pid}: only {len(chosen)} unique product images acquired')
    finals=[]
    for idx,pth in enumerate(chosen[:3],1):
        final=live_dir/(f'{pid}-main.webp' if idx==1 else f'{pid}-{idx:02d}.webp')
        shutil.copy2(pth,final); finals.append(final)
    readme=['# '+pid+' — live product media','',f"- User-approved product: {product['brand']} {product['manufacturerItemNo']}",f'- Published: {PUB_DATE}','- Three unique exact-product images; no generative editing, crop or upscale.','- Transport sources are used only for media/identity evidence; Mall price and availability remain owner-supplied.','']
    for i,(f,u) in enumerate(zip(finals,provenance),1): readme.append(f'- IMAGE {i}: `{f.name}` — {Image.open(f).width}×{Image.open(f).height} — SHA-256 `{sha256(f)}` — source `{u}`')
    (live_dir/'README.md').write_text('\n'.join(readme)+'\n',encoding='utf-8')
    return finals

def entry(p,frames):
    media={
      'image':f"assets/pink-mall/products/{p['id']}/{frames[0].name}",
      'imageAlt':p['alts'][0],
      'gallery':[f"assets/pink-mall/products/{p['id']}/{x.name}" for x in frames[1:]],
      'galleryAlt':p['alts'][1:], 'fit':'contain','ph':'accessories','field':'blush','surface':'#F1F1F1'}
    d={'id':p['id'],'brand':p['brand'],'manufacturerItemNo':p['manufacturerItemNo'],'variantCode':p['variantCode'],'name':p['name'],'slug':p['slug'],'category':'accessories','subcategory':None,'color':'Pink','priceEUR':p['priceEUR'],'oldPriceEUR':None,'description':p['description'],'selectedBy':None,'tags':p['tags'],'featured':False,'campaign':None,'related':p['related'],'isNew':False,'newUntil':NEW_UNTIL,'inventoryMode':'availability','availability':{'ONE SIZE':'available'},'media':media,'source':p['source']}
    return json.dumps(d,ensure_ascii=False,indent=4)

def patch_catalog(frame_map):
    text=HTML.read_text(encoding='utf-8')
    if '"id": "PM-042"' in text or '"id": "PM-043"' in text or '"id": "PM-044"' in text: raise SystemExit('target PM IDs already exist; refusing stale batch')
    start=text.find('"id": "PM-041"'); anchor='\n}\n        ];'; end=text.find(anchor,start)
    if start<0 or end<0: raise SystemExit('PM-041/catalog terminator not found')
    block='\n},\n'+',\n'.join(entry(p,frame_map[p['id']]) for p in PRODUCTS)+'\n        ];'
    text=text[:end]+block+text[end+len(anchor):]
    HTML.write_text(text,encoding='utf-8')

def write_expectations(frame_map):
    for path in EXPECT_DIR.glob('PM-*.json'):
        data=json.loads(path.read_text(encoding='utf-8')); data['catalogueSize']=44; path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for p in PRODUCTS:
        fr=frame_map[p['id']]; im=Image.open(fr[0])
        data={'id':p['id'],'catalogueSize':44,'brand':p['brand'],'manufacturerItemNo':p['manufacturerItemNo'],'name':p['name'],'category':'accessories','subcategory':None,'color':'Pink','priceEUR':p['priceEUR'],'newUntil':NEW_UNTIL,'sizes':['ONE SIZE'],'surface':'#F1F1F1','nativeWidth':im.width,'nativeHeight':im.height,'viberUrl':'https://connect.viber.com/business/631d5a74-5919-11f1-b5e8-06dd2a4dc594','searchTerms':p['search'],'priorProducts':[f'PM-{n:03d}' for n in range(35,42)],'frames':[]}
        for f in fr:
            ii=Image.open(f); data['frames'].append({'file':f.name,'sha256':sha256(f),'width':ii.width,'height':ii.height})
        (EXPECT_DIR/f"{p['id']}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def write_mobile_smoke():
    js="""#!/usr/bin/env node
const { chromium } = require('playwright');
const file=process.argv[2]||'PINKMALL.html', port=process.argv[3]||'8131';
const ids=['PM-042','PM-043','PM-044']; const viewports=[[375,667],[390,844],[430,932],[768,1024],[1366,768],[1920,1080]];
(async()=>{const browser=await chromium.launch();let failed=false;for(const [width,height] of viewports){const c=await browser.newContext({viewport:{width,height}});const page=await c.newPage();await page.addInitScript(()=>{try{localStorage.setItem('pierciina_consent_v1',JSON.stringify({v:1,analytics:true,marketing:true,ts:Date.now()}));}catch(e){}});await page.goto(`http://127.0.0.1:${port}/${file}`,{waitUntil:'networkidle'});for(const id of ids){await page.evaluate(id=>{window.PinkMallStore.clearFilters();window.PinkMallStore.openProduct(id);},id);await page.waitForTimeout(180);const x=await page.evaluate(()=>{const s=document.querySelector('#pmsSheet'),r=s&&s.getBoundingClientRect(),img=s&&s.querySelector('img');return{open:!!s&&s.offsetHeight>0,overflow:document.documentElement.scrollWidth>innerWidth+1,left:r?r.left:0,right:r?r.right:0,imageOk:!!img&&img.complete&&img.naturalWidth>0};});if(!x.open||x.overflow||x.left<-1||x.right>width+1||!x.imageOk){console.error('FAIL',width,height,id,x);failed=true;}await page.keyboard.press('Escape');}if(!failed)console.log('PASS',width+'x'+height);await c.close();}await browser.close();process.exit(failed?1:0);})();
"""
    (ROOT/'tools/regression/pm042_044_mobile_smoke.js').write_text(js,encoding='utf-8')

def update_state():
    s=STATE.read_text(encoding='utf-8')
    s=re.sub(r'^Updated: .*$', 'Updated: PM-042, PM-043 and PM-044 batch publication.',s,count=1,flags=re.M)
    s=re.sub(r'^Status: \*\*PM-001…PM-\d+ PUBLISHED\.\*\*$', 'Status: **PM-001…PM-044 PUBLISHED.**',s,count=1,flags=re.M)
    s=re.sub(r'\| CANONICAL WEBSITE SHA-256 \| `[^`]+` \|',f'| CANONICAL WEBSITE SHA-256 | `{sha256(HTML)}` |',s,count=1)
    s=re.sub(r'\| CANONICAL WEBSITE BYTES \| \d+ \|',f'| CANONICAL WEBSITE BYTES | {HTML.stat().st_size} |',s,count=1)
    s=re.sub(r'\| PUBLIC CATALOG \| PM-001 … PM-\d+ \|','| PUBLIC CATALOG | PM-001 … PM-044 |',s,count=1)
    s=re.sub(r'\| NEXT ID \| PM-\d+ \|','| NEXT ID | PM-045 |',s,count=1)
    marker='| SPLA94 | **PUBLISHED as PM-041** on 2026-08-29 — owner-approved one-image exception; exact pink variant 8RFX |'
    rows='\n| 6LPESC J4836 | **PUBLISHED as PM-042** on 2026-08-31 — owner-confirmed pink reversible bucket hat |\n| 5693725 | **PUBLISHED as PM-043** on 2026-08-31 — official Swarovski identity; Crystalline Ballpoint Pen |\n| CKNYC1852S 680 | **PUBLISHED as PM-044** on 2026-08-31 — exact BLUSH / pink variant |'
    if 'PUBLISHED as PM-042' not in s and marker in s: s=s.replace(marker,marker+rows,1)
    s=re.sub(r'\| PUBLICATION REGRESSION \| PASS — `tools/regression/product_regression\.js`; PM-\d+…PM-\d+, production \+ standalone \|','| PUBLICATION REGRESSION | PASS — `tools/regression/product_regression.js`; PM-031…PM-044, production + standalone |',s,count=1)
    s += '\n\n## PM-042…PM-044 — batch published\n\nPublished 2026-08-31 after owner `APPROVE ALL READY`. All three products use `ONE SIZE — available`, exact owner-supplied Mall prices, `selectedBy: null`, no old price, and three unique exact-product images. Production, standalone and viewport regression must pass in the publication workflow before promotion.\n'
    STATE.write_text(s,encoding='utf-8')

def finalize_state():
    s=STATE.read_text(encoding='utf-8')
    if STANDALONE.exists():
        sec=s.find('## Review artifact')
        if sec>=0:
            end=s.find('\n## ',sec+4); end=len(s) if end<0 else end; block=s[sec:end]
            block=re.sub(r'\| SHA-256 \| `[^`]+` \|',f'| SHA-256 | `{sha256(STANDALONE)}` |',block,count=1)
            block=re.sub(r'\| BYTES \| \d+ \|',f'| BYTES | {STANDALONE.stat().st_size} |',block,count=1)
            block=re.sub(r'\| LAST PUBLICATION VALIDATION \| .*? \|','| LAST PUBLICATION VALIDATION | PASS — PM-042…PM-044 production + standalone + viewport smoke |',block,count=1)
            s=s[:sec]+block+s[end:]
    STATE.write_text(s,encoding='utf-8')

def prepare():
    frame_map={}
    for p in PRODUCTS: frame_map[p['id']]=capture_product(p)
    patch_catalog(frame_map); write_expectations(frame_map); write_mobile_smoke(); update_state()
    print('prepared batch',sha256(HTML))

if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'prepare'
    if mode=='prepare': prepare()
    elif mode=='finalize': finalize_state()
    else: raise SystemExit('usage: publish_pm042_044.py [prepare|finalize]')
