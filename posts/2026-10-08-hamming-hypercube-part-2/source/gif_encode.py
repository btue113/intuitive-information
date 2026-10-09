# Frames for an animation of encoding 10110: parity computed layer by layer.
from figs import *
w = lambda c: bin(c).count('1')
OX, OY, S = 200, 190, 0.9
NOTES = 770
B4 = lambda c: format(c, '04b')

def group(c):
    return [x for x in range(1, 16) if x & c == c]
def group_edges(c):
    g = set(group(c))
    return [(a, a ^ (1 << k)) for a in g for k in range(4) if (a ^ (1 << k)) in g and a < a ^ (1 << k)]
def fill_of(c):
    return DATA_C if w(c) >= 3 else P2_C if w(c) == 2 else P1_C

frames = []
def frame(title, lines, known, focus=None, colour=None, step=""):
    roles = {c: fill_of(c) for c in known}
    bits = {c: (cw[c] if c in known else '') for c in range(1, 16)}
    hi = [(a, b, colour) for a, b in group_edges(focus)] if focus else []
    rings = {focus: INK} if focus else {}
    if focus:
        roles = dict(roles)
        for x in group(focus):
            if x != focus and x not in roles:
                roles[x] = 'white'
    t, pos = tesseract(OX, OY, S, bits=bits, roles=roles, rings=rings, edges_hi=hi)
    body = text(40, 52, title, size=28, weight=700, anchor='start')
    if step:
        body += text(1200, 52, step, size=20, color=QUIET, anchor='end')
    body += t
    for i, (s, kw) in enumerate(lines):
        body += text(40, NOTES + 6 + 30 * i, s, size=kw.get('size', 20), weight=kw.get('weight', 400), color=kw.get('color', INK), anchor='start')
    lx, ly = 40, NOTES + 116
    for fill, label in [(DATA_C, "secret"), (P2_C, "parity, layer 2 (squares)"), (P1_C, "parity, layer 1 (cubes)")]:
        body += f"<circle cx='{lx + 10}' cy='{ly}' r='10' fill='{fill}' stroke='{EDGE}' stroke-width='2'/>" + text(lx + 28, ly + 6, label, size=17, color=QUIET, anchor='start')
        lx += 300
    frames.append(svg(1240, NOTES + 140, body))

data = [c for c in order if w(c) >= 3]
layer2 = [c for c in order if w(c) == 2]
layer1 = [c for c in order if w(c) == 1]
known = set(data)
total = len(layer2) + len(layer1)
frame("Encoding 10110 on the tesseract", [("The five secrets 1, 0, 1, 1, 0 sit on the heaviest corners: 1111, 1110, 1101, 1011, 0111.", {}),
      ("Every other corner computes a parity bit, heaviest layer first, so its group is even.", {})], known, step="start")
for i, c in enumerate(layer2 + layer1, 1):
    layer = 2 if w(c) == 2 else 1
    others = [x for x in group(c) if x != c]
    ones = sum(cw[x] for x in others)
    shape = "a square" if layer == 2 else "a whole cube"
    known = known | {c}
    frame(f"Layer {layer}: corner {B4(c)} evens out its group",
          [(f"Its group is {shape}: every corner with 1s wherever {B4(c)} has 1s ({len(others) + 1} corners).", {}),
           (f"The other {len(others)} hold " + " + ".join(str(cw[x]) for x in others) + f" = {ones} ones, so {B4(c)} = {cw[c]} to make the total even.", {'weight': 700})],
          known, focus=c, colour=(P2_C if layer == 2 else P1_C), step=f"step {i} of {total}")
frame("Done: every group is even", [("Sent, in the program's order: 101100011000110", {'weight': 700}),
      ("Squares first, then cubes: each layer only needs the corners above it, which are already known.", {})], known, step="done")
for i, f in enumerate(frames):
    open(f"enc_{i:02d}.svg", "w").write(f)
print(len(frames), "frames")
