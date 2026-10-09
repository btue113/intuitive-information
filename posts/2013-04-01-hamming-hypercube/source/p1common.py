# Shared drawing helpers for part 1 (same look as part 2).
from figs import *
B3 = lambda c: format(c, '03b')
AUD = {0b110: 1, 0b111: 2, 0b011: 3, 0b101: 4, 0b100: 5, 0b010: 6, 0b001: 7}   # audience number -> corner
CORNER = {v: k for k, v in AUD.items()}
GROUP_OF = {5: 0b100, 6: 0b010, 7: 0b001}             # parity member -> the bit its face fixes to 1
FACE_COL = {5: "#f5b700", 6: "#2ab7a9", 7: "#e8618c"}  # one colour per group
BITS = {1: 1, 2: 0, 3: 1, 4: 1}                         # the post's example: members 1-4 pick 1, 0, 1, 1
for p, g in GROUP_OF.items():
    BITS[p] = sum(BITS[a] for a in (1, 2, 3, 4) if CORNER[a] & g) % 2
def members(p):
    return [a for a in range(1, 8) if CORNER[a] & GROUP_OF[p]]
def face(p):  # the face of corners whose bit GROUP_OF[p] is 1, in drawing order
    g = GROUP_OF[p]
    others = [b for b in (0b100, 0b010, 0b001) if b != g]
    return [g, g | others[0], g | others[0] | others[1], g | others[1]]

def cube_xy(c, ox, oy, s=1.0, W=300, H=260, D=(150, -110)):
    b2, b1, b0 = (c >> 2) & 1, (c >> 1) & 1, c & 1
    return ox + (b0 * W + b2 * D[0]) * s, oy + (b1 * H + b2 * D[1]) * s

def draw_cube(ox, oy, s=1.0, inside=None, fills=None, rings=None, faces=(), face_fill=None, label=True, r=22, edge_col=EDGE, dim=False):
    """inside: corner -> text in the circle; faces: list of (members' parity number, colour, opacity)."""
    pos = {c: cube_xy(c, ox, oy, s) for c in range(8)}
    cx = sum(p[0] for p in pos.values()) / 8; cy = sum(p[1] for p in pos.values()) / 8
    out = []
    for p, col, op in faces:
        pts = " ".join(f"{pos[c][0]:.1f},{pos[c][1]:.1f}" for c in face(p))
        out.append(f"<polygon points='{pts}' fill='{col}' fill-opacity='{op}' stroke='{col}' stroke-width='3'/>")
    for a in range(8):
        for k in range(3):
            b = a ^ (1 << k)
            if a < b:
                gone = a == 0 or b == 0
                col = "#c9c9c9" if (gone or dim) else edge_col
                out.append(f"<line x1='{pos[a][0]:.1f}' y1='{pos[a][1]:.1f}' x2='{pos[b][0]:.1f}' y2='{pos[b][1]:.1f}' stroke='{col}' stroke-width='{1.4 if gone else 1.8}' {'stroke-dasharray=\"5 5\"' if gone else ''}/>")
    for c in range(8):
        x, y = pos[c]
        if c == 0:
            out.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='white' stroke='#bbb' stroke-width='1.5' stroke-dasharray='4 4'/>")
            continue
        fill = (fills or {}).get(c, 'white'); ring = (rings or {}).get(c, EDGE)
        out.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}' stroke='{ring}' stroke-width='{3.5 if ring != EDGE else 2}'/>")
        if inside and c in inside:
            out.append(text(x, y + 7, str(inside[c]), size=20 if r >= 18 else 14, weight=700))
        if label:
            dx, dy = x - cx, y - cy; n = math.hypot(dx, dy) or 1
            lx, ly = x + dx / n * (r + 30), y + dy / n * (r + 30) + 5
            out.append(text(lx, ly, f"#{AUD[c]} · {B3(c)}" if label == 'full' else B3(c), size=15, color=QUIET))
    return "".join(out), pos

def bolt(x, y):
    pts = [(0,0),(9,0),(4,9),(11,9),(-2,26),(3,13),(-4,13)]
    return "<polygon points='" + " ".join(f"{x+a:.1f},{y+b:.1f}" for a, b in pts) + "' fill='#ffd60a' stroke='#8a6d00' stroke-width='1.2'/>"
