#!/usr/bin/env python3
"""Fetch an open-licence icon set into a topic as one local sprite.

  icons.py <topic-dir> <set>

Sets: feather, lucide, tabler, tabler-filled (published sprites), and
phosphor-<thin|light|regular|bold|fill|duotone>, heroicons-<outline|solid>
(built from the npm package). Writes <topic>/icons-<set>.svg and .txt
(feather keeps its old names, icons.svg and icons.txt). The sprite must be
local: browsers refuse <use href> to another origin. Prints the path, the
icon count, and the <svg> attributes the set needs (stroke or fill).
"""
import io, json, os, re, sys, tarfile, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme_core import ICON_SETS

CDN = "https://cdn.jsdelivr.net/npm/"
SPRITES = {
    "feather": CDN + "feather-icons@4/dist/feather-sprite.svg",
    "lucide": CDN + "lucide-static@0/sprite.svg",
    "tabler": CDN + "@tabler/icons-sprite@3/dist/tabler-sprite.svg",
    "tabler-filled": CDN + "@tabler/icons-sprite@3/dist/tabler-sprite-filled.svg",
}
PACKAGES = {  # set: (npm package, directory inside the tarball, filename suffix to strip)
    **{f"phosphor-{w}": ("@phosphor-icons/core", f"package/assets/{w}/", "" if w == "regular" else f"-{w}")
       for w in ("thin", "light", "regular", "bold", "fill", "duotone")},
    "heroicons-outline": ("heroicons", "package/24/outline/", ""),
    "heroicons-solid": ("heroicons", "package/24/solid/", ""),
}
SETS = tuple(ICON_SETS)
FILL_SETS = ("tabler-filled", "heroicons-solid") + tuple(s for s in SETS if s.startswith("phosphor-"))
LICENCES = {"feather": "MIT", "lucide": "ISC", "tabler": "MIT", "tabler-filled": "MIT", "heroicons-outline": "MIT", "heroicons-solid": "MIT"}
PRESENTATION = ("fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin")


def sprite_name(s):
    return "icons" if s == "feather" else f"icons-{s}"


def usage(s):
    return 'fill="currentColor"' if s in FILL_SETS else 'fill="none" stroke="currentColor" stroke-width="1.75"'


def build_sprite(files, strip_suffix=""):
    """(sprite text, sorted ids) from (name, svg text) pairs. Root presentation attributes move onto a <g>."""
    symbols = {}
    for name, svg in files:
        sid = name[:-len(strip_suffix)] if strip_suffix and name.endswith(strip_suffix) else name
        root = re.search(r"<svg\b([^>]*)>", svg)
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', root.group(1)))
        inner = svg[root.end():svg.rindex("</svg>")].strip()
        g = " ".join(f'{k}="{attrs[k]}"' for k in attrs if k in PRESENTATION)
        body = f"<g {g}>{inner}</g>" if g else inner
        symbols[sid] = f'<symbol id="{sid}" viewBox="{attrs.get("viewBox", "0 0 24 24")}">{body}</symbol>'
    ids = sorted(symbols)
    return '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join(symbols[i] for i in ids) + "</svg>\n", ids


def normalize(sprite, s):
    """Make published sprites behave like the built ones: plain ids (no "tabler-" prefix), a viewBox on every
    symbol, and no stroke-width baked into a symbol, so the page's stroke-width sets the icon weight."""
    prefix = {"tabler": "tabler-", "tabler-filled": "tabler-filled-"}.get(s)
    if prefix:
        sprite = sprite.replace(f'id="{prefix}', 'id="')
    sprite = re.sub(r'(<symbol\b[^>]*?)\s+stroke-width="[^"]*"', r"\1", sprite)
    return re.sub(r"<symbol\b(?![^>]*viewBox)", '<symbol viewBox="0 0 24 24"', sprite)


def _get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def fetch(s):
    if s in SPRITES:
        sprite = normalize(_get(SPRITES[s]).decode("utf-8"), s)
        return sprite, sorted(set(re.findall(r'<symbol[^>]*\bid="([^"]+)"', sprite)))
    pkg, folder, suffix = PACKAGES[s]
    meta = json.loads(_get(f"https://registry.npmjs.org/{pkg}/latest"))
    tgz = tarfile.open(fileobj=io.BytesIO(_get(meta["dist"]["tarball"])), mode="r:gz")
    files = [(os.path.basename(m.name)[:-4], tgz.extractfile(m).read().decode("utf-8"))
             for m in tgz.getmembers() if m.name.startswith(folder) and m.name.endswith(".svg")]
    return build_sprite(files, suffix)


def main(argv):
    if len(argv) != 2 or argv[1] not in SETS:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    topic, s = argv
    sprite, ids = fetch(s)
    name = sprite_name(s)
    with open(os.path.join(topic, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(sprite)
    with open(os.path.join(topic, name + ".txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(ids) + "\n")
    lic = LICENCES.get(s, "MIT")
    print(f"ICONS {os.path.join(topic, name + '.svg')} ({len(ids)} icons, {lic}; use <svg {usage(s)}><use href=\"../../{name}.svg#ID\"/></svg>)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
