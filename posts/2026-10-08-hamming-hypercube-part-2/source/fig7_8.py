from figs import *
OX, OY, S, NOTES = 200, 190, 0.9, 770
GREEN_TEXT = "#1e7a39"; AMBER_RING = "#e08a00"
B4 = lambda c: format(c, '04b')
CHEAT = [0b1101, 0b0110]
rx2 = dict(cw)
for c in CHEAT: rx2[c] ^= 1
WORD = ''.join(str(rx2[c]) for c in order)
def bolt(x, y):
    pts = [(0,0),(9,0),(4,9),(11,9),(-2,26),(3,13),(-4,13)]
    return "<polygon points='" + " ".join(f"{x+a:.1f},{y+b:.1f}" for a, b in pts) + "' fill='#ffd60a' stroke='#8a6d00' stroke-width='1.2'/>"
def note(y, s, **kw):
    kw.setdefault('size', 18); kw.setdefault('anchor', 'start')
    return text(40, NOTES + y, s, **kw)
def bolts(pos, corners):
    out = ""
    for c in corners:
        lx, _ = label_xy(c, pos, cube_center(c, OX, OY, S), d=41)
        out += bolt(pos[c][0] + (20 if lx < pos[c][0] else -30), pos[c][1] - 50)
    return out

# ---------- fig7: two cheaters fool part 1's trick ----------
fails = [c for c in order[5:] if sum(rx2[x] for x in range(1, 16) if x & c == c) % 2]
big = [c for c in fails if bin(c).count('1') == 1]
blamed = sum(big)
roles = {c: (FAIL_C if c in fails else 'white') for c in range(1, 16)}
rings = {c: RED for c in CHEAT}; rings[blamed] = AMBER_RING
body = text(40, 52, "Two cheaters: part 1's shortcut blames an innocent seat", size=28, weight=700, anchor='start')
t, pos = tesseract(OX, OY, S, bits=rx2, roles=roles, rings=rings)
body += t + bolts(pos, CHEAT)
x, y = pos[blamed]
body += f"<circle cx='{x:.1f}' cy='{y:.1f}' r='29' fill='none' stroke='{AMBER_RING}' stroke-width='3' stroke-dasharray='6 5'/>"
body += f"<circle cx='52' cy='{NOTES-6}' r='11' fill='white' stroke='{RED}' stroke-width='3.5'/>" + text(72, NOTES, "the two cheaters: 1101 (a secret holder) and 0110 (a square's parity)", size=18, anchor='start')
body += f"<circle cx='52' cy='{NOTES+26}' r='11' fill='{FAIL_C}' stroke='{EDGE}' stroke-width='2'/>" + text(72, NOTES + 32, f"owns a group that is now odd: {len(fails)} of the 10 groups fail, so the magician knows someone lied", size=18, anchor='start')
body += note(70, "Part 1's trick reads the four big groups: those of " + ", ".join(B4(c) for c in big) + f" fail, which spells {B4(blamed)}.")
body += note(96, f"But {B4(blamed)} (dashed ring) is honest. The four big groups alone are fooled; all ten groups together are not.", weight=700)
body += note(130, f"Received: {WORD}", color=QUIET)
open("fig7.svg", "w").write(svg(1240, NOTES + 156, body))

# ---------- fig8: naming the cheaters ----------
roles = {c: (FAIL_C if c in CHEAT else OK_C) for c in range(1, 16)}
rings = {c: (RED if c in CHEAT else "#2a9d4b") for c in range(1, 16)}
body = text(40, 52, "Naming the cheaters: encode the secrets again and compare", size=28, weight=700, anchor='start')
t, pos = tesseract(OX, OY, S, bits=rx2, roles=roles, rings=rings)
body += t + bolts(pos, CHEAT)
for c in CHEAT:
    x, y = pos[c]
    label = f"said {rx2[c]}, should be {cw[c]}"
    wdt = len(label) * 8.6 + 20
    bx, by = x - 34 - wdt, y - 16          # tag to the left of the corner, joined by a short line
    body += f"<line x1='{bx + wdt:.1f}' y1='{y:.1f}' x2='{x - 22:.1f}' y2='{y:.1f}' stroke='{RED}' stroke-width='2'/>"
    body += f"<rect x='{bx:.1f}' y='{by:.1f}' width='{wdt:.1f}' height='32' rx='6' fill='white' stroke='{RED}' stroke-width='2'/>"
    body += text(bx + wdt / 2, y + 6, label, size=17, weight=700, color=RED)
body += note(0, "1. Vote, as before. Every majority is wide: 1110 wins 5–2, 1101 2–5, 1011 2–5, 0111 5–2, then 1111 6–1. Secrets: 10110.")
body += note(28, "2. Encode 10110 again. That gives the honest seating: 101100011000110.")
body += note(56, "3. Compare it with what each seat said. Green seats agree; the two red seats, 1101 and 0110, are the cheaters.", weight=700)
body += note(92, "The same check names the three cheaters from the earlier test (0111, 1001, 0100). Any three or fewer are caught.", color=QUIET)
open("fig8.svg", "w").write(svg(1240, NOTES + 118, body))
print("word", WORD, "fails", [B4(c) for c in fails], "blamed", B4(blamed))
