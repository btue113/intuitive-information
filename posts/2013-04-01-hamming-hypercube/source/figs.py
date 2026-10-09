import math, sys
B = lambda v: format(v, '04b')
FONT = "Calibri, 'Segoe UI', Arial, sans-serif"
EDGE = "#d63384"; INK = "#222"; QUIET = "#666"; RED = "#d62828"; DATA = "#1f6fd1"
YEL = "#f3e3a1"; LAV = "#cfc6ee"; GRN = "#bfe3c4"; GREY = "#e4e4e4"
# high-contrast role colours
DATA_C = "#5b9bf0"; P1_C = "#f5b700"; P2_C = "#b48be8"; FAIL_C = "#f28b8b"; OK_C = "#7fd08f"

order = sorted(range(1, 16), key=lambda c: (-bin(c).count('1'), -c))
ENC = "101100011000110"
cw = {order[i]: int(ch) for i, ch in enumerate(ENC)}
RX = "101110001000010"
rx = {order[i]: int(ch) for i, ch in enumerate(RX)}
ERR = {c for c in range(1, 16) if rx[c] != cw[c]}

# Part 1 style: a cube inside a cube (layout found by search2.py: inner cube centred, same orientation).
# Outer cube = first bit 1, inner cube = first bit 0. (ox, oy) = outer cube's front top-left corner.
A, DO = 560, (297.5, -92.3)              # outer cube: size, depth vector
BS, DI = 285.6, (190.1, -73.1)           # inner cube: size, depth vector (same orientation)
IP = (A / 2 + DO[0] / 2 - BS / 2 - DI[0] / 2, A / 2 + DO[1] / 2 - BS / 2 - DI[1] / 2)  # centred in the outer cube

def tess_pos(c, ox, oy, s=1.0):
    b3, b2, b1, b0 = (c >> 3) & 1, (c >> 2) & 1, (c >> 1) & 1, c & 1
    if b3:
        x, y = b0 * A + b2 * DO[0], b1 * A + b2 * DO[1]
    else:
        x, y = IP[0] + b0 * BS + b2 * DI[0], IP[1] + b1 * BS + b2 * DI[1]
    return ox + x * s, oy + y * s

def cube_center(c, ox, oy, s=1.0):
    if (c >> 3) & 1:
        x, y = A / 2 + DO[0] / 2, A / 2 + DO[1] / 2
    else:
        x, y = IP[0] + BS / 2 + DI[0] / 2, IP[1] + BS / 2 + DI[1] / 2
    return ox + x * s, oy + y * s

def label_xy(c, pos, center, d=34):
    x, y = pos[c]; dx, dy = x - center[0], y - center[1]; n = math.hypot(dx, dy) or 1
    return x + dx / n * d, y + dy / n * d + 5

def svg(w, h, body):
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' viewBox='0 0 {w} {h}' font-family=\"{FONT}\"><rect width='{w}' height='{h}' fill='white'/>{body}</svg>"

def text(x, y, s, size=20, color=INK, weight=400, anchor='middle'):
    return f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' fill='{color}' font-weight='{weight}' text-anchor='{anchor}'>{s}</text>"

def tesseract(ox, oy, s, bits=None, roles=None, rings=None, groups=(), edges_hi=(), names=True, r=19, dim_others=False):
    """bits: dict corner->bit; roles: corner->fill; rings: corner->stroke colour; groups: [(corners, fill)]; edges_hi: [(a,b,colour)]."""
    pos = {c: tess_pos(c, ox, oy, s) for c in range(16)}
    cx = sum(p[0] for p in pos.values()) / 16; cy = sum(p[1] for p in pos.values()) / 16
    out = []
    for corners, fill in groups:
        pts = " ".join(f"{pos[c][0]:.1f},{pos[c][1]:.1f}" for c in corners)
        out.append(f"<polygon points='{pts}' fill='{fill}' fill-opacity='0.75' stroke='none'/>")
    for a in range(16):
        for k in range(4):
            b = a ^ (1 << k)
            if a < b:
                dashed = (a == 0 or b == 0)
                col = "#c9c9c9" if (dashed or dim_others) else EDGE
                op = 0.55 if k == 3 else 1.0
                out.append(f"<line x1='{pos[a][0]:.1f}' y1='{pos[a][1]:.1f}' x2='{pos[b][0]:.1f}' y2='{pos[b][1]:.1f}' stroke='{col}' stroke-opacity='{op}' stroke-width='{1.6 if not dashed else 1.2}' {'stroke-dasharray=\"5 5\"' if dashed else ''}/>")
    for a, b, col in edges_hi:
        out.append(f"<line x1='{pos[a][0]:.1f}' y1='{pos[a][1]:.1f}' x2='{pos[b][0]:.1f}' y2='{pos[b][1]:.1f}' stroke='{col}' stroke-width='7' stroke-linecap='round' stroke-opacity='0.85'/>")
    for c in range(16):
        x, y = pos[c]
        if c == 0:
            out.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='white' stroke='#bbb' stroke-width='1.5' stroke-dasharray='4 4'/>")
            continue
        fill = (roles or {}).get(c, 'white'); ring = (rings or {}).get(c, EDGE)
        out.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}' stroke='{ring}' stroke-width='{3.5 if ring != EDGE else 2}'/>")
        if bits is not None:
            out.append(text(x, y + 7, str(bits[c]), size=20, weight=700, color=INK))
        if names:
            lx, ly = label_xy(c, pos, cube_center(c, ox, oy, s), d=r + 22)
            out.append(text(lx, ly, B(c), size=15, color=QUIET))
    return "".join(out), pos
