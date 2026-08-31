#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import hashlib, zipfile

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / 'docs/pink-mall/publication-staging/pm042-044-owner-media.zip'
OWNER = ROOT / '.owner-media'
BUILDER = ROOT / 'tools/publish_pm042_044.py'
IDS = ('PM-042','PM-043','PM-044')


def stage():
    if not ZIP.exists():
        raise SystemExit('owner media staging archive missing')
    if not zipfile.is_zipfile(ZIP):
        raise SystemExit('owner media staging archive is not a valid binary ZIP')
    if OWNER.exists():
        import shutil
        shutil.rmtree(OWNER)
    OWNER.mkdir()
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(OWNER)
    for pid in IDS:
        files = sorted((OWNER / pid).glob('owner-*.webp'))
        if len(files) != 3:
            raise SystemExit(f'{pid}: expected 3 owner files, got {len(files)}')
        shas = []
        for f in files:
            with Image.open(f) as im:
                if im.size != (970, 1182):
                    raise SystemExit(f'{f}: unexpected dimensions {im.size}')
            shas.append(hashlib.sha256(f.read_bytes()).hexdigest())
        if len(set(shas)) != 3:
            raise SystemExit(f'{pid}: duplicate owner media bytes')
        print(pid, 'OWNER MEDIA PASS', *shas)


def patch_builder():
    p = BUILDER
    s = p.read_text(encoding='utf-8')
    needle = "def capture_product(product):\n    pid=product['id']; live_dir=ROOT/'assets/pink-mall/products'/pid"
    repl = '''def capture_product(product):
    pid=product['id']
    owner_dir=ROOT/'.owner-media'/pid
    if owner_dir.exists():
        live_dir=ROOT/'assets/pink-mall/products'/pid
        src_dir=live_dir/'source'
        src_dir.mkdir(parents=True,exist_ok=True)
        finals=[]
        source_shas=[]
        for idx in range(1,4):
            src=owner_dir/f'owner-{idx:02d}.webp'
            if not src.exists():
                raise SystemExit(f'{pid}: missing approved owner frame {idx}')
            source_sha=hashlib.sha256(src.read_bytes()).hexdigest()
            source_shas.append(source_sha)
            preserved=src_dir/f'{pid}-owner-{idx:02d}.webp'
            shutil.copy2(src,preserved)
            final=live_dir/(f'{pid}-main.webp' if idx==1 else f'{pid}-{idx:02d}.webp')
            shutil.copy2(src,final)
            with Image.open(final) as im:
                if im.size != (970,1182):
                    raise SystemExit(f'{pid}: owner frame dimensions changed: {im.size}')
            finals.append(final)
        if len(set(source_shas)) != 3:
            raise SystemExit(f'{pid}: owner frames are not byte-unique')
        readme=['# '+pid+' — live product media','',f"- User-approved product: {product['brand']} {product['manufacturerItemNo']}",f'- Published: {PUB_DATE}','- Media transport: `USER_SUPPLIED`.','- Three byte-unique owner-approved exact-product images.','- Technical WebP preservation only; no crop, resize, upscale, recolouring or generative edit.','']
        for i,f in enumerate(finals,1):
            readme.append(f'- IMAGE {i}: `{f.name}` — 970×1182 — SHA-256 `{sha256(f)}`')
        (live_dir/'README.md').write_text('\\n'.join(readme)+'\\n',encoding='utf-8')
        return finals
    live_dir=ROOT/'assets/pink-mall/products'/pid'''
    if needle not in s:
        raise SystemExit('capture_product patch anchor missing')
    s = s.replace(needle, repl, 1)
    s = s.replace("'mediaTransport':'TRUSTED_RETAILER'", "'mediaTransport':'USER_SUPPLIED'")
    s = s.replace("'mediaTransport':'OFFICIAL'", "'mediaTransport':'USER_SUPPLIED'")
    p.write_text(s, encoding='utf-8')


if __name__ == '__main__':
    stage()
    patch_builder()
