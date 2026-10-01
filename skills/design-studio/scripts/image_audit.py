#!/usr/bin/env python3
"""Measure the colours an app's screenshots really use.

  image_audit.py <screenshot.png> [...] [--out image-audit.json]

The glow-up audit for a topic with no codebase (source: images). Decodes
each PNG with the standard library, samples it, drops anti-aliasing (any
exact colour under 0.2% of a screen), clusters the rest in OKLab, flags
clusters that match Tailwind's default palette, and names the neutrals'
temperature. Gradients never pass the anti-aliasing filter (each step is
too small), so chromatic pixels are also binned by hue: any hue covering
0.3% of the screens is an accent, and one spread over many distinct colours
is reported as a gradient. Prints "IMAGE-AUDIT <headline>".
"""
import json, math, os, struct, sys, zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme_core import TAILWIND_HEX, parse, srgb_to_oklch, to_hex

MIN_SHARE = 0.002      # an exact colour must cover this much of a screen to count
MERGE = 0.03           # OKLab distance under which two colours are one
TAILWIND_NEAR = 0.02   # OKLab distance under which a colour is a Tailwind default
SAMPLE = 250_000       # pixels sampled per screen
ACCENT_CHROMA = 0.06   # OKLCH chroma above which a pixel counts toward an accent hue
ACCENT_SHARE = 0.003   # share of all screens a hue needs to be an accent
GRADIENT_STEPS = 40    # distinct colours in one hue that mark it as a gradient
HUES = ((20, "red"), (45, "orange"), (70, "yellow"), (160, "green"), (200, "teal"), (250, "blue"),
        (320, "purple"), (350, "pink"), (360, "red"))
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


def _paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def read_png(path):
    """(width, height, rgba bytearray) for an 8-bit, non-interlaced PNG."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    pos, idat, palette, alpha = 8, [], None, None
    w = h = depth = ctype = None
    while pos < len(data):
        n, kind = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        pos += 12 + n
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
            if interlace:
                raise ValueError(f"{path}: interlaced PNG; re-export it without interlacing")
            if depth != 8 or ctype not in CHANNELS:
                raise ValueError(f"{path}: only 8-bit PNGs are supported (got depth {depth}, colour type {ctype})")
        elif kind == b"PLTE":
            palette = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif kind == b"tRNS" and ctype == 3:
            alpha = list(body)
        elif kind == b"IDAT":
            idat.append(body)
        elif kind == b"IEND":
            break
    if w is None:
        raise ValueError(f"{path}: no IHDR chunk")
    raw = zlib.decompress(b"".join(idat))
    bpp = CHANNELS[ctype]
    stride = w * bpp
    out = bytearray(w * h * 4)
    prev = bytearray(stride)
    for y in range(h):
        f = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        if f == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif f == 2:
            line = bytearray((a + b) & 255 for a, b in zip(line, prev))
        elif f == 3:
            for i in range(stride):
                line[i] = (line[i] + (((line[i - bpp] if i >= bpp else 0) + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                c = prev[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + _paeth(a, prev[i], c)) & 255
        o = y * w * 4
        if ctype == 6:
            out[o:o + w * 4] = line
        elif ctype == 2:
            out[o:o + w * 4] = bytes(v for x in range(w) for v in (line[x * 3], line[x * 3 + 1], line[x * 3 + 2], 255))
        elif ctype == 0:
            out[o:o + w * 4] = bytes(v for g in line for v in (g, g, g, 255))
        elif ctype == 4:
            out[o:o + w * 4] = bytes(v for x in range(w) for v in (line[x * 2],) * 3 + (line[x * 2 + 1],))
        else:
            out[o:o + w * 4] = bytes(v for i in line for v in palette[i] + ((alpha[i] if alpha and i < len(alpha) else 255),))
        prev = line
    return w, h, out


def _lab(hexcol):
    L, C, H = srgb_to_oklch(parse(hexcol))
    return L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))


def _dist(p, q):
    return math.dist(p, q)


def hue_name(h):
    return next(name for limit, name in HUES if h < limit)


def screen_counts(path):
    """({hex: share} for every exact colour sampled from one screenshot)."""
    w, h, rgba = read_png(path)
    step = max(1, int(math.sqrt(w * h / SAMPLE)))
    counts, total = {}, 0
    for y in range(0, h, step):
        row = y * w * 4
        for x in range(0, w, step):
            i = row + x * 4
            if rgba[i + 3] < 128:
                continue
            key = (rgba[i], rgba[i + 1], rgba[i + 2])
            counts[key] = counts.get(key, 0) + 1
            total += 1
    if not total:
        return {}
    return {"#%02x%02x%02x" % k: n / total for k, n in counts.items()}


def audit(paths):
    shares, hues = {}, {}
    for p in paths:
        for col, s in screen_counts(p).items():
            if s >= MIN_SHARE:
                shares[col] = shares.get(col, 0) + s / len(paths)
            _, c, h = srgb_to_oklch(parse(col))
            if c >= ACCENT_CHROMA:
                b = hues.setdefault(hue_name(h), {"share": 0.0, "colours": set()})
                b["share"] += s / len(paths)
                b["colours"].add(col)
    accents = sorted(({"name": n, "share": round(b["share"], 4), "gradient": len(b["colours"]) > GRADIENT_STEPS}
                      for n, b in hues.items() if b["share"] >= ACCENT_SHARE), key=lambda a: -a["share"])
    clusters = []  # [rep_hex, rep_lab, share]
    for col, s in sorted(shares.items(), key=lambda kv: -kv[1]):
        lab = _lab(col)
        for c in clusters:
            if _dist(lab, c[1]) < MERGE:
                c[2] += s
                break
        else:
            clusters.append([col, lab, s])
    tw_labs = {h: _lab(h) for h in TAILWIND_HEX}
    tailwind = []
    for rep, lab, _ in clusters:
        if lab[0] > 0.995 or lab[0] < 0.005:
            continue  # pure white and black are everyone's, not a Tailwind fingerprint
        near = min(tw_labs, key=lambda h: _dist(lab, tw_labs[h]))
        if _dist(lab, tw_labs[near]) < TAILWIND_NEAR:
            tailwind.append({"hex": rep, "name": TAILWIND_HEX[near]})
    tailwind.sort(key=lambda t: t["name"])
    greys = [srgb_to_oklch(parse(rep)) for rep, _, _ in clusters if srgb_to_oklch(parse(rep))[1] < 0.03]
    if not greys:
        neutrals = "no"
    elif max(c for _, c, _ in greys) < 0.005:
        neutrals = "untinted"
    else:
        hue = max(greys, key=lambda g: g[1])[2]
        neutrals = "warm" if 20 <= hue <= 120 else "cool" if 180 <= hue <= 330 else "tinted"
    n, k = len(clusters), len(paths)
    parts = [f"{n} colour{'' if n == 1 else 's'} across {k} screen{'' if k == 1 else 's'}"]
    if tailwind:
        parts.append("Tailwind " + ", ".join(t["name"] for t in tailwind))
    parts.append(f"{neutrals} greys")
    parts += [f"{a['name']} gradient" for a in accents if a["gradient"]]
    return {
        "images": [os.path.basename(p) for p in paths],
        "colors": {"count": n, "values": {rep: {"share": round(s, 4)} for rep, _, s in sorted(clusters, key=lambda c: c[0])}},
        "tailwind": tailwind,
        "accents": accents,
        "neutrals": neutrals,
        "headline": " · ".join(parts),
    }


def main(argv):
    paths = [a for a in argv if a.endswith(".png")]
    if not paths:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        r = audit(paths)
    except ValueError as e:
        print(f"FAIL {e}")
        return 1
    if "--out" in argv:
        with open(argv[argv.index("--out") + 1], "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2)
            f.write("\n")
    print(f"IMAGE-AUDIT {r['headline']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
