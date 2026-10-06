"""Build a self-contained Pages site from revision-pinned upstream fonts."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import quote
import hashlib
import json
import shutil
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
CACHE = ROOT / '.cache'

def fetch(repo, revision, path):
    url = f'https://raw.githubusercontent.com/{repo}/{revision}/{quote(path)}'
    cached = CACHE / hashlib.sha256(url.encode()).hexdigest()
    if not cached.exists():
        with urlopen(Request(url, headers={'User-Agent': 'offaux-fonts-build'}), timeout=60) as response:
            data = response.read()
        cached.write_bytes(data)
    if cached.read_bytes().startswith(b'version https://git-lfs.github.com/spec/v1'):
        pointer = cached.read_text().splitlines()
        digest = next(line.split('sha256:')[1] for line in pointer if line.startswith('oid '))
        size = int(next(line.split()[1] for line in pointer if line.startswith('size ')))
        media = f'https://media.githubusercontent.com/media/{repo}/{revision}/{quote(path)}'
        with urlopen(media, timeout=60) as response:
            data = response.read()
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f'Git LFS integrity check failed: {path}')
        cached.write_bytes(data)
    return cached

def main():
    OUT.mkdir(exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    (OUT / 'fonts').mkdir(exist_ok=True)
    css = []
    manifest = json.loads((ROOT / 'fonts.json').read_text())
    for family in manifest:
        for face in family['fonts']:
            source = fetch(family['repo'], family['revision'], face['path'])
            filename = f"{family['id']}-{face['weight']}-{face['style']}.woff2"
            with TTFont(source, recalcTimestamp=False) as font:
                font.flavor = 'woff2'
                font.save(OUT / 'fonts' / filename)
            css.append(f"@font-face{{font-family:'{family['name']}';src:url('./fonts/{filename}') format('woff2');font-weight:{face['weight']};font-style:{face['style']};font-display:swap;}}")
        license_dir = OUT / 'licenses' / family['id']
        license_dir.mkdir(parents=True, exist_ok=True)
        for path in family['licenses']:
            shutil.copyfile(fetch(family['repo'], family['revision'], path), license_dir / Path(path).name)
        print(f"Built {family['name']}", flush=True)
    (OUT / 'fonts.css').write_text('\n'.join(css) + '\n')
    for name in ['index.html', 'styles.css', 'rulers.js', 'favicon.svg']:
        shutil.copyfile(ROOT / name, OUT / name)
    shutil.copyfile(ROOT / 'fonts.json', OUT / 'fonts.json')
    (OUT / '.nojekyll').touch()
    print(f'Built {len(manifest)} families in {OUT}')

if __name__ == '__main__':
    main()
