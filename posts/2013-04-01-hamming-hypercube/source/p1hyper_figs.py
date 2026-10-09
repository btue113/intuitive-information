from p1common import *
ARROW = "#1f6fd1"; SUM = "#e08a00"
defs = ("<defs><marker id='ua' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto'><path d='M0 0L10 5L0 10z' fill='" + ARROW + "'/></marker>"
        "<marker id='sa' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto'><path d='M0 0L10 5L0 10z' fill='" + SUM + "'/></marker><marker id='ka' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto'><path d='M0 0L10 5L0 10z' fill='#222'/></marker></defs>")
def arrow(p, q, col, mk, r=14):
    dx, dy = q[0] - p[0], q[1] - p[1]; n = math.hypot(dx, dy)
    x1, y1 = p[0] + dx / n * r, p[1] + dy / n * r; x2, y2 = q[0] - dx / n * (r + 3), q[1] - dy / n * (r + 3)
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{col}' stroke-width='3.5' marker-end='url(#{mk})'/>"
def vec_label(c, bits):  # bit string -> "(1, 0, 1)"
    return "(" + ", ".join(format(c, f'0{bits}b')) + ")"
def simple_cube(ox, oy, s, dims, removed=False, unit=False, sum_to=None, labels=True, r=14):
    """dims = 2 (square), 3 (cube) or 4 (tesseract, cube-in-cube). Returns svg."""
    n = 1 << dims
    if dims == 4:
        pos = {c: tess_pos(c, ox, oy, s) for c in range(n)}
    elif dims == 3:
        pos = {c: cube_xy(c, ox, oy, s) for c in range(n)}
    else:
        pos = {c: (ox + (c & 1) * 260 * s, oy + ((c >> 1) & 1) * 260 * s) for c in range(n)}
    cx = sum(p[0] for p in pos.values()) / n; cy = sum(p[1] for p in pos.values()) / n
    out = []
    for a in range(n):
        for k in range(dims):
            b = a ^ (1 << k)
            if a < b:
                gone = removed and (a == 0 or b == 0)
                out.append(f"<line x1='{pos[a][0]:.1f}' y1='{pos[a][1]:.1f}' x2='{pos[b][0]:.1f}' y2='{pos[b][1]:.1f}' stroke='{'#c9c9c9' if gone else EDGE}' stroke-width='1.6' stroke-opacity='{0.55 if dims == 4 and k == 3 and not gone else 1}' {'stroke-dasharray=\"5 5\"' if gone else ''}/>")
    if unit:
        for k in range(dims):
            out.append(arrow(pos[0], pos[1 << k], ARROW, 'ua', r))
    if sum_to is not None:   # walk the unit vectors head to tail, along the cube's own edges
        at, off = 0, 7
        for step in sum_to:
            p, q = pos[at], pos[at | step]
            dx, dy = q[0] - p[0], q[1] - p[1]; ln = math.hypot(dx, dy)
            ox_, oy_ = -dy / ln * off, dx / ln * off      # shift sideways so blue arrows stay visible
            out.append(arrow((p[0] + ox_, p[1] + oy_), (q[0] + ox_, q[1] + oy_), SUM, 'sa', r))
            at |= step
    for c in range(n):
        x, y = pos[c]
        if removed and c == 0:
            out.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='white' stroke='#bbb' stroke-width='1.5' stroke-dasharray='4 4'/>")
            continue
        fill = P1_C if removed and bin(c).count('1') == 1 else (DATA_C if removed else 'white')
        out.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{fill}' stroke='{EDGE}' stroke-width='2'/>")
        if labels:
            dx, dy = x - cx, y - cy; nn = math.hypot(dx, dy) or 1
            if dims == 4:
                ccx, ccy = cube_center(c, ox, oy, s); dx, dy = x - ccx, y - ccy; nn = math.hypot(dx, dy) or 1
            out.append(text(x + dx / nn * (r + 26), y + dy / nn * (r + 26) + 5, vec_label(c, dims) if unit or sum_to is not None else format(c, f'0{dims}b'), size=13, color=QUIET))
    return "".join(out)

# ---------- figure 3: hypercube -> Hamming graph ----------
body = defs + text(40, 52, "Take away one corner, and a hypercube becomes a Hamming code", size=28, weight=700, anchor='start')
body += simple_cube(90, 190, 0.62, 3) + text(230, 440, "Q3, the cube", size=19, weight=700)
body += f"<path d='M420 270 h80' stroke='{INK}' stroke-width='3' marker-end='url(#ka)'/>"
body += simple_cube(560, 190, 0.62, 3, removed=True) + text(700, 440, "Hamming (7, 4)", size=19, weight=700)
body += simple_cube(90, 640, 0.42, 4) + text(270, 955, "Q4, the tesseract", size=19, weight=700)
body += f"<path d='M470 760 h80' stroke='{INK}' stroke-width='3' marker-end='url(#ka)'/>"
body += simple_cube(610, 640, 0.42, 4, removed=True) + text(790, 955, "Hamming (15, 11)", size=19, weight=700)
for i, (fill, lab) in enumerate([(DATA_C, "data"), (P1_C, "parity: the corners with a single 1"), ('white', "removed corner")]):
    x = [40, 200, 620][i]
    body += f"<circle cx='{x + 10}' cy='1015' r='10' fill='{fill}' stroke='{EDGE if fill != 'white' else '#bbb'}' stroke-width='2' {'stroke-dasharray=\"4 4\"' if fill == 'white' else ''}/>" + text(x + 28, 1021, lab, size=17, anchor='start')
open("fig3.svg", "w").write(svg(1240, 1045, body))

# ---------- figure 4: Q2, Q3, Q4 from unit vectors ----------
body = defs + text(40, 52, "n unit vectors and vector addition place every corner of an n-cube", size=28, weight=700, anchor='start')
body += simple_cube(90, 170, 0.75, 2, unit=True, sum_to=[0b01, 0b10], r=13) + text(190, 450, "Q2 (square)", size=19, weight=700) + text(190, 476, "(0, 1) + (1, 0) = (1, 1)", size=16, color=SUM)
body += simple_cube(470, 200, 0.62, 3, unit=True, sum_to=[0b001, 0b100], r=13) + text(610, 450, "Q3 (cube)", size=19, weight=700) + text(610, 476, "(0, 0, 1) + (1, 0, 0) = (1, 0, 1)", size=16, color=SUM)
body += simple_cube(150, 640, 0.6, 4, unit=True, sum_to=[0b1000, 0b0010, 0b0001], r=13) + text(420, 1058, "Q4 (tesseract)", size=19, weight=700) + text(420, 1084, "(1, 0, 0, 0) + (0, 0, 1, 0) + (0, 0, 0, 1) = (1, 0, 1, 1)", size=16, color=SUM)
body += f"<line x1='760' y1='640' x2='800' y2='640' stroke='{ARROW}' stroke-width='3.5' marker-end='url(#ua)'/>" + text(810, 646, "unit vectors from the zero corner", size=16, anchor='start')
body += f"<line x1='760' y1='670' x2='800' y2='670' stroke='{SUM}' stroke-width='3.5' marker-end='url(#sa)'/>" + text(810, 676, "their sum: walk the unit vectors head to tail", size=16, anchor='start')
open("fig4.svg", "w").write(svg(1240, 1110, body))
