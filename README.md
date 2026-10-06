# Offaux Fonts

A document-style showcase of open-source stand-ins for Office fonts, published at
https://muglug.github.io/offaux-fonts/.

Eight selectable specimens cover Fauxdana, the four Intos families, Carlito Light,
Arimo, Hindoe UI, and Outfit Gothic. Aptos (with an Intos fallback) is used for the site interface;
small text uses Hindoe UI. Carlito Bold accompanies the Carlito Light specimen;
Carlito Light links to it as a complementary family. Each includes source links; font licenses ship with the generated site.
Intos Display provides the headline in the combined Intos specimen, with Intos
used for its body text. The paper, rulers, and indentation markers are ornamental; there is no editor toolbar.
The rulers scale to an 8.5-inch paper width, including on smaller screens.

## Build and preview

Requires Python 3.13.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 8765 --directory dist
```

Open http://localhost:8765. The initial build needs network access to GitHub;
subsequent builds reuse `.cache/`. `dist/` is the complete deployable site.

## Font sources

`fonts.json` pins each upstream repository to an exact commit and lists the font
files, styles, and licenses. To update a font, review its upstream changes and
update its revision (and file paths if necessary), then rebuild and check.

The build converts full TTFs to WOFF2 without subsetting or altering outlines,
preserves font metadata, verifies Git LFS object hashes, and includes upstream
licenses in `dist/licenses/`. Fonts are served locally with no third-party font
requests. Every family uses its own CSS name, including Carlito Light.

Edit `index.html` for specimen copy, `styles.css` for the document presentation,
and `rulers.js` for decorative rulers. The content and fonts work without JavaScript;
JavaScript only draws and scales rulers.

## GitHub Pages

`.github/workflows/pages.yml` builds and validates pull requests, and deploys
`main` using GitHub Actions. The repository's Pages source must be **GitHub Actions**.
All asset paths are relative so the site works under `/offaux-fonts/`.

Font licenses belong to their respective upstream projects and are distributed
alongside the generated webfonts. This is an independent collection, not a Microsoft project.
