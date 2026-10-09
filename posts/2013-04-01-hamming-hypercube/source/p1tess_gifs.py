# Hamming (15, 11) on the tesseract: encoding and catching one cheater, from the 2013 tests.
from figs import *
B4 = lambda c: format(c, '04b')
w = lambda c: bin(c).count('1')
OX, OY, S, NOTES = 200, 190, 0.9, 770
order15 = sorted(range(1, 16), key=lambda c: (-w(c), -c))          # the program's bit order
PARITY = [c for c in order15 if w(c) == 1]                          # 1000, 0100, 0010, 0001
ENC = "100100100101011"                                             # 2013 test: encode 10010010010
RX = "100100110101011"                                              # 2013 test: one bit flipped
cw = {order15[i]: int(b) for i, b in enumerate(ENC)}
rx = {order15[i]: int(b) for i, b in enumerate(RX)}
for p in PARITY:   # check the test vector against the rule: every group even
    assert sum(cw[x] for x in range(1, 16) if x & p) % 2 == 0
CHEAT = [c for c in range(1, 16) if cw[c] != rx[c]]
assert len(CHEAT) == 1
def group(p): return [x for x in range(1, 16) if x & p]
def gedges(p):
    g = set(group(p))
    return [(a, a ^ (1 << k)) for a in g for k in range(4) if (a ^ (1 << k)) in g and a < a ^ (1 << k)]
def bolt(x, y):
    pts = [(0,0),(9,0),(4,9),(11,9),(-2,26),(3,13),(-4,13)]
    return "<polygon points='" + " ".join(f"{x+a:.1f},{y+b:.1f}" for a, b in pts) + "' fill='#ffd60a' stroke='#8a6d00' stroke-width='1.2'/>"

def frame(title, lines, bits, known, focus=None, bar=None, cheat=(), final=False):
    roles = {c: (DATA_C if w(c) >= 2 else P1_C) for c in known}
    if final:
        roles.update({c: FAIL_C for c in cheat})
    rings = {c: RED for c in cheat}
    if focus:
        rings[focus] = INK
        for m in group(focus):
            roles.setdefault(m, 'white')
    hi = [(a, b, P1_C) for a, b in gedges(focus)] if focus else []
    t, pos = tesseract(OX, OY, S, bits={c: (bits[c] if c in known else '') for c in range(1, 16)}, roles=roles, rings=rings, edges_hi=hi)
    body = text(40, 52, title, size=27, weight=700, anchor='start') + t
    for c in cheat:
        lx, _ = label_xy(c, pos, cube_center(c, OX, OY, S), d=41)
        body += bolt(pos[c][0] + (20 if lx < pos[c][0] else -30), pos[c][1] - 50)
    for i, (s, kw) in enumerate(lines):
        body += text(40, NOTES + 6 + 30 * i, s, size=19, weight=kw.get('weight', 400), color=kw.get('color', INK), anchor='start')
    if bar is not None:
        for j, p in enumerate(PARITY):
            x = 40 + j * 200; st = bar.get(p)
            fill = '#e9e9e9' if st is None else (FAIL_C if st else OK_C)
            body += f"<rect x='{x}' y='{NOTES + 76}' width='186' height='38' rx='6' fill='{fill}' stroke='{INK if p == focus else 'none'}' stroke-width='2.5'/>"
            body += text(x + 93, NOTES + 101, f"group of {B4(p)}: " + ('?' if st is None else 'fails' if st else 'passes'), size=16, weight=700)
    return svg(1240, NOTES + 130, body)

# ---------- encoding ----------
data = [c for c in order15 if w(c) >= 2]
frames = [frame("Hamming (15, 11): the 11 secrets sit on the corners with two or more 1s",
                [("My 2013 test: the secrets 10010010010, in the program's order (1111, 1110, 1101, 1011, 0111, then the 2-ones).", {}),
                 ("Only the four corners with a single 1 are left. Each one owns a group: half of the tesseract, a whole cube.", {})], cw, set(data))]
known = set(data)
for i, p in enumerate(PARITY, 1):
    others = [x for x in group(p) if x != p]
    ones = sum(cw[x] for x in others); known = known | {p}
    frames.append(frame(f"Step {i} of 4: corner {B4(p)} evens out its cube",
                        [(f"Its group is every corner with a 1 where {B4(p)} has its 1: 8 corners, a whole cube.", {}),
                         (f"The other 7 hold {ones} ones, so {B4(p)} = {cw[p]} to make the total even.", {'weight': 700})], cw, known, focus=p))
frames.append(frame("Done: four groups, all even", [(f"Sent, in the program's order: {ENC}", {'weight': 700}),
                    ("Just like the cube's 3 faces, but now 4 cubes, one for each direction of the tesseract.", {})], cw, known))
for i, f in enumerate(frames): open(f"tenc_{i:02d}.svg", "w").write(f)

# ---------- detection ----------
allc = set(range(1, 16))
frames = [frame("Someone cheated. Which seat?", [(f"The magician receives {RX}, my 2013 one-error test. He checks the four groups.", {}),
               ("(The cheater is marked here for you; the magician doesn't know.)", {'color': QUIET})], rx, allc, bar={}, cheat=CHEAT)]
bar = {}
for p in PARITY:
    mem = group(p); s = sum(rx[x] for x in mem); bar[p] = s % 2 == 1
    frames.append(frame(f"Check the group of {B4(p)}", [(f"Its 8 seats hold {s} ones: " + ("odd, so it FAILS." if s % 2 else "even, so it passes."), {'weight': 700}),
                        ("A group fails exactly when the cheater sits in it.", {'color': QUIET})], rx, allc, focus=p, bar=dict(bar), cheat=CHEAT))
spell = "".join("1" if bar[p] else "0" for p in PARITY)
frames.append(frame(f"The failures spell the cheater: {spell}", [(f"Groups of 1000 and 0001 fail, 0100 and 0010 pass. Read fail = 1: {spell}, the seat {B4(CHEAT[0])}.", {'weight': 700}),
                    ("Every seat sits in a different set of groups, so one cheater is always named. Flip it back: 10010010010.", {})],
                    rx, allc, bar=dict(bar), cheat=CHEAT, final=True))
for i, f in enumerate(frames): open(f"tdet_{i:02d}.svg", "w").write(f)
print("cheater", B4(CHEAT[0]), "pattern", spell)
