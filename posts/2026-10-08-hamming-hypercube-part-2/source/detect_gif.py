# One GIF per example: the magician checks the 10 groups one at a time.
import sys
from figs import *
OX, OY, S, NOTES = 200, 190, 0.9, 770
B4 = lambda c: format(c, '04b')
w = lambda c: bin(c).count('1')
GROUPS = order[5:]
def bolt(x, y):
    pts = [(0,0),(9,0),(4,9),(11,9),(-2,26),(3,13),(-4,13)]
    return "<polygon points='" + " ".join(f"{x+a:.1f},{y+b:.1f}" for a, b in pts) + "' fill='#ffd60a' stroke='#8a6d00' stroke-width='1.2'/>"
def members(g): return [x for x in range(1, 16) if x & g == g]
def gedges(g):
    m = set(members(g))
    return [(a, a ^ (1 << k)) for a in m for k in range(4) if (a ^ (1 << k)) in m and a < a ^ (1 << k)]

def make(cheaters, name, intro):
    rx = dict(cw)
    for c in cheaters: rx[c] ^= 1
    results = {}
    frames = []
    def frame(title, lines, focus=None, final=False):
        roles = {c: (FAIL_C if final and c in cheaters else 'white') for c in range(1, 16)}
        rings = {c: RED for c in cheaters}
        hi = []
        if focus:
            col = P2_C if w(focus) == 2 else P1_C
            hi = [(a, b, col) for a, b in gedges(focus)]
            for m in members(focus):
                if m not in cheaters: roles[m] = '#fff3c4' if w(focus) == 1 else '#efe6fb'
        t, pos = tesseract(OX, OY, S, bits=rx, roles=roles, rings=rings, edges_hi=hi)
        body = text(40, 52, title, size=27, weight=700, anchor='start') + t
        for c in cheaters:
            lx, _ = label_xy(c, pos, cube_center(c, OX, OY, S), d=41)
            body += bolt(pos[c][0] + (20 if lx < pos[c][0] else -30), pos[c][1] - 50)
        for i, (s, kw) in enumerate(lines):
            body += text(40, NOTES + 6 + 30 * i, s, size=19, weight=kw.get('weight', 400), color=kw.get('color', INK), anchor='start')
        # the pattern bar
        yb = NOTES + 76
        body += text(40, yb + 24, "pattern:", size=18, weight=700, anchor='start')
        for j, g in enumerate(GROUPS):
            x = 150 + j * 104
            st = results.get(g)
            fill = '#e9e9e9' if st is None else (FAIL_C if st else OK_C)
            stroke = INK if g == focus else 'none'
            body += f"<rect x='{x}' y='{yb}' width='94' height='36' rx='6' fill='{fill}' stroke='{stroke}' stroke-width='2.5'/>"
            body += text(x + 47, yb + 16, B4(g), size=14, weight=700) + text(x + 47, yb + 31, '' if st is None else ('fail' if st else 'pass'), size=12)
        frames.append(svg(1240, NOTES + 130, body))
    who = ", ".join(B4(c) for c in cheaters)
    frame(intro, [(f"The magician doesn't know who ({who}, marked here for you). He checks the ten groups one by one.", {}),
                  ("Each parity bit watches one group: a square or a whole cube.", {})])
    for k, g in enumerate(GROUPS, 1):
        mem = members(g)
        s = sum(rx[x] for x in mem)
        inn = [c for c in cheaters if c in mem]
        fails = s % 2 == 1
        results[g] = fails
        shape = "square" if w(g) == 2 else "cube"
        why = ("no cheater inside" if not inn else f"{len(inn)} cheater inside ({B4(inn[0])})" if len(inn) == 1
               else f"{len(inn)} cheaters inside ({', '.join(B4(c) for c in inn)})" + (", they cancel out" if len(inn) % 2 == 0 else ""))
        frame(f"Check {k} of 10: the {shape} group of {B4(g)}",
              [(f"Its {len(mem)} seats hold " + " + ".join(str(rx[x]) for x in mem) + f" = {s}: " + ("odd, so it FAILS." if fails else "even, so it passes."), {'weight': 700}),
               (f"Why: {why}.", {'color': QUIET})], focus=g)
    frame(f"The pattern names the cheaters: {who}",
          [(f"Only one set of three or fewer seats leaves exactly this pattern: {who}.", {'weight': 700}),
           ("(Checked for all 576 possible sets. Each set of up to 3 cheaters has its own pattern.)", {'color': QUIET})], final=True)
    for i, f in enumerate(frames):
        open(f"{name}_{i:02d}.svg", "w").write(f)
    return len(frames)

print(make([0b1011], "det1", "One cheater: the pattern is its fingerprint"))
print(make([0b1101, 0b0110], "det2", "Two cheaters: the pattern still names them both"))
print(make([0b0111, 0b1001, 0b0100], "det3", "Three cheaters: still one pattern, one answer"))
