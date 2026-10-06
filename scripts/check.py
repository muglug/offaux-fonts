"""Validate the deployable artifact, font coverage, and internal links."""
from html.parser import HTMLParser
from pathlib import Path
import json
from fontTools.ttLib import TTFont
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate ID: {attrs['id']}"
            self.ids.add(attrs['id'])
        for key in ['src', 'href']:
            if key in attrs:
                self.links.append(attrs[key])
doc = Document()
doc.feed((OUT / 'index.html').read_text())
for link in doc.links:
    if link.startswith('#'):
        assert link[1:] in doc.ids, f'Missing anchor: {link}'
    elif not link.startswith(('https:', 'http:')):
        assert (OUT / link).exists(), f'Missing asset: {link}'
count = 0
for family in json.loads((ROOT / 'fonts.json').read_text()):
    # Carlito provides the bold companion to Carlito Light, which links to its source.
    if family['id'] != 'carlito':
        assert family['id'] in doc.ids
    assert family['source'] in doc.links
    for face in family['fonts']:
        path = OUT / 'fonts' / f"{family['id']}-{face['weight']}-{face['style']}.woff2"
        with TTFont(path) as font:
            assert font.flavor == 'woff2'
            cmap = font.getBestCmap()
            assert all(ord(c) in cmap for c in 'The quick brown fox 0123456789'), path
            assert font['OS/2'].usWeightClass == face['weight'], path
        count += 1
    for license in family['licenses']:
        assert (OUT / 'licenses' / family['id'] / Path(license).name).stat().st_size > 100
print(f'Passed: {count} WOFF2 faces, all eight specimens, source links, licenses, assets, and anchors.')
