from figs import *
def cube_pos(c, ox, oy, s=1.0):
    b2, b1, b0 = (c >> 2) & 1, (c >> 1) & 1, c & 1
    return ox + b0 * 200 * s + b2 * 100 * s, oy + b1 * 170 * s - b2 * 80 * s
def cube(ox, oy, s, roles):
    pos = {c: cube_pos(c, ox, oy, s) for c in range(8)}
    cx = sum(p[0] for p in pos.values()) / 8; cy = sum(p[1] for p in pos.values()) / 8
    out = []
    for a in range(8):
        for k in range(3):
            b = a ^ (1 << k)
            if a < b:
                d = a == 0 or b == 0
                out.append(f"<line x1='{pos[a][0]}' y1='{pos[a][1]}' x2='{pos[b][0]}' y2='{pos[b][1]}' stroke='{'#c9c9c9' if d else EDGE}' stroke-width='1.6' {'stroke-dasharray=\"5 5\"' if d else ''}/>")
    for c in range(8):
        x, y = pos[c]
        if c == 0:
            out.append(f"<circle cx='{x}' cy='{y}' r='19' fill='white' stroke='#bbb' stroke-dasharray='4 4' stroke-width='1.5'/>"); continue
        out.append(f"<circle cx='{x}' cy='{y}' r='19' fill='{roles[c]}' stroke='{EDGE}' stroke-width='2'/>")
        lx, ly = label_xy(c, pos, (cx, cy), d=42)
        out.append(text(lx, ly, format(c, '03b'), size=15, color=QUIET))
    return "".join(out)

w = lambda c: bin(c).count('1')
cube_roles = {c: (P1_C if w(c) == 1 else DATA_C) for c in range(1, 8)}
tess_roles = {c: (P1_C if w(c) == 1 else P2_C if w(c) == 2 else DATA_C) for c in range(1, 16)}
body = text(40, 52, "From 1 to 2 parity dimensions: parity moves one level deeper", size=28, weight=700, anchor='start')
body += cube(70, 250, 0.85, cube_roles)
body += text(200, 640, "Part 1: Hamming (7, 4)", size=21, weight=700)
body += text(200, 668, "parity on the 3 light corners", size=18, color=QUIET)
t, _ = tesseract(660, 210, 0.6, roles=tess_roles)
body += t
body += text(860, 640, "Part 2: two parity dimensions (15, 5)", size=21, weight=700)
body += text(860, 668, "parity on the 4 + 6 light corners, data on the 5 heavy ones", size=18, color=QUIET)
# legend
lx = 120
for fill, label in [(DATA_C, "data (secret) corner"), (P1_C, "parity, 1 one in its name"), (P2_C, "parity, 2 ones in its name"), ("white", "0000 / 000: left empty")]:
    body += f"<circle cx='{lx}' cy='720' r='12' fill='{fill}' stroke='{EDGE if fill != 'white' else '#bbb'}' stroke-width='2' {'stroke-dasharray=\"4 4\"' if fill == 'white' else ''}/>"
    body += text(lx + 22, 726, label, size=17, anchor='start')
    lx += 280
open("fig1.svg", "w").write(svg(1240, 760, body))
