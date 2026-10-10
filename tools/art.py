"""Front-page art: the hero tesseract (inline SVG partial) and the post cover images.

Uses part 2's tesseract layout so the front page matches the figures.
Run from the repo root: python3 tools/art.py
"""
import sys
sys.path.insert(0, "posts/2026-10-08-hamming-hypercube-part-2/source")
from figs import tess_pos, DATA_C, P1_C, P2_C, EDGE

W = lambda c: bin(c).count("1")


def frame(pos, pad):
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    return min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad


def edges(corners, pos, dims, css, empty=0):
    out = []
    for a in corners:
        for k in dims:
            b = a ^ (1 << k)
            if a < b and b in corners:
                cls = "e0" if empty in (a, b) else ("e4" if k == 3 else "e")
                if css:
                    out.append(f"<line class='{cls}' x1='{pos[a][0]:.1f}' y1='{pos[a][1]:.1f}' x2='{pos[b][0]:.1f}' y2='{pos[b][1]:.1f}'/>")
                else:
                    dash = " stroke-dasharray='6 6'" if cls == "e0" else ""
                    col = "#bbb" if cls == "e0" else EDGE
                    op = 0.5 if cls == "e4" else 1
                    out.append(f"<line x1='{pos[a][0]:.1f}' y1='{pos[a][1]:.1f}' x2='{pos[b][0]:.1f}' y2='{pos[b][1]:.1f}' stroke='{col}' stroke-opacity='{op}' stroke-width='3'{dash}/>")
    return out


def hero():
    """Tesseract whose corners fill in layer by layer, like encoding: secrets, then squares, then cubes."""
    pos = {c: tess_pos(c, 0, 0) for c in range(16)}
    x, y, w, h = frame(pos, 30)
    out = edges(range(16), pos, range(4), css=True)
    for c in sorted(range(16), key=W):
        cls = "n0" if c == 0 else f"n n{min(W(c), 3)}"
        out.append(f"<circle class='{cls}' cx='{pos[c][0]:.1f}' cy='{pos[c][1]:.1f}' r='22'><title>{c:04b}</title></circle>")
    return (f"<svg class='tess' viewBox='{x:.0f} {y:.0f} {w:.0f} {h:.0f}' role='img' "
            f"aria-label='A tesseract whose corners fill in layer by layer'>{''.join(out)}</svg>\n")


def cover(corners, dims, fill, scale, empty):
    pos = {c: tess_pos(c, 0, 0) for c in corners}
    x, y, w, h = frame(pos, 24 * scale + 6)
    out = edges(corners, pos, dims, css=False, empty=empty)
    for c in corners:
        if c == empty:
            out.append(f"<circle cx='{pos[c][0]:.1f}' cy='{pos[c][1]:.1f}' r='{24 * scale:.0f}' fill='none' stroke='#bbb' stroke-width='2.5' stroke-dasharray='6 6'/>")
        else:
            out.append(f"<circle cx='{pos[c][0]:.1f}' cy='{pos[c][1]:.1f}' r='{24 * scale:.0f}' fill='{fill(c)}' stroke='{EDGE}' stroke-width='3'/>")
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='{x:.0f} {y:.0f} {w:.0f} {h:.0f}'>{''.join(out)}</svg>\n"


open("layouts/_partials/tesseract.html", "w").write(hero())

# Part 1: the cube (drawn as the tesseract's outer cube 1xyz, so 1000 is its empty corner), Hamming (7, 4): one-1 corners are parity.
cube = [8 | c for c in range(8)]
open("posts/2013-04-01-hamming-hypercube/cover.svg", "w").write(
    cover(cube, range(3), lambda c: P1_C if W(c & 7) == 1 else DATA_C, 1.6, empty=8))
# Part 2: the tesseract with two parity dimensions, (15, 5).
open("posts/2026-10-08-hamming-hypercube-part-2/cover.svg", "w").write(
    cover(list(range(16)), range(4), lambda c: {1: P1_C, 2: P2_C}.get(W(c), DATA_C), 1.0, empty=0))
