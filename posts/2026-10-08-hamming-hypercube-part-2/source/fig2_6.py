from figs import *
w = lambda c: bin(c).count('1')
DATA_FILL = DATA_C; GREEN = "#2a9d4b"; GREEN_TEXT = "#1e7a39"; PINK = FAIL_C
OX, OY, S = 200, 190, 0.9          # tesseract placement for the full-size figures
NOTES = 770                        # first line of notes under the drawing

def bolt(x, y):
    pts = [(0,0),(9,0),(4,9),(11,9),(-2,26),(3,13),(-4,13)]
    return "<polygon points='" + " ".join(f"{x+a:.1f},{y+b:.1f}" for a, b in pts) + "' fill='#ffd60a' stroke='#8a6d00' stroke-width='1.2'/>"
def mid(pos, a, b, dy=-12):
    return (pos[a][0] + pos[b][0]) / 2, (pos[a][1] + pos[b][1]) / 2 + dy
def note(y, s, **kw):
    kw.setdefault('size', 18); kw.setdefault('anchor', 'start')
    return text(40, NOTES + y, s, **kw)
def cube_edges(prefix_bit):  # the 12 edges of the outer (1) or inner (0) cube
    return [(a, a ^ (1 << k)) for a in range(16) for k in range(3) if (a >> 3) == prefix_bit and a < a ^ (1 << k)]

# ---------- fig2: encoding 10110 ----------
roles = {c: (DATA_FILL if w(c) >= 3 else 'white') for c in range(1, 16)}
square = [(0b0110, 0b0111), (0b0111, 0b1111), (0b1111, 0b1110), (0b1110, 0b0110)]
big = [(a, b, P1_C) for a, b in cube_edges(1)] + [(a, b, P2_C) for a, b in square]
body = text(40, 52, "Encoding 10110: every group must hold an even number of 1s", size=28, weight=700, anchor='start')
t, pos = tesseract(OX, OY, S, bits=cw, roles=roles, edges_hi=big)
body += t
body += note(0, "Blue corners hold the five secrets 1, 0, 1, 1, 0 (corners 1111, 1110, 1101, 1011, 0111). Every white corner is a parity bit.")
body += f"<line x1='40' y1='{NOTES+26}' x2='62' y2='{NOTES+26}' stroke='#e9c44a' stroke-width='7' stroke-linecap='round'/>" + text(72, NOTES + 32, "Group of 1000 = the whole outer cube: its 8 corners hold four 1s, even", size=18, anchor='start')
body += f"<line x1='40' y1='{NOTES+56}' x2='62' y2='{NOTES+56}' stroke='#8f7fd6' stroke-width='7' stroke-linecap='round'/>" + text(72, NOTES + 62, "Group of 0110 = one square, linking the two cubes: 0110, 0111, 1110, 1111 hold 1+0+0+1 = 2 ones, even", size=18, anchor='start')
body += note(96, "Each parity corner owns one group: itself plus every corner that has 1s wherever it has 1s.", color=QUIET)
body += note(122, "4 corners with one 1 own a whole cube (like part 1's faces); 6 corners with two 1s own a square.", color=QUIET)
body += note(150, "Sent, in the program's order: 101100011000110", weight=700)
open("fig2.svg", "w").write(svg(1240, NOTES + 176, body))

# ---------- fig3: three errors, the checks ----------
failing = [c for c in order[5:] if sum(rx[x] for x in range(1, 16) if x & c == c) % 2]
roles = {c: (PINK if c in failing else 'white') for c in range(1, 16)}
body = text(40, 52, "Three cheaters: part 1's shortcut blames an innocent seat", size=28, weight=700, anchor='start')
t, pos = tesseract(OX, OY, S, bits=rx, roles=roles, rings={c: RED for c in ERR})
body += t
for c in ERR:
    lx, _ = label_xy(c, pos, cube_center(c, OX, OY, S), d=41)
    body += bolt(pos[c][0] + (20 if lx < pos[c][0] else -30), pos[c][1] - 50)
body += f"<circle cx='52' cy='{NOTES-6}' r='11' fill='white' stroke='{RED}' stroke-width='3.5'/>" + text(72, NOTES, "flipped in transit: 0111, 1001, 0100", size=18, anchor='start')
body += f"<circle cx='52' cy='{NOTES+26}' r='11' fill='{PINK}' stroke='{EDGE}' stroke-width='2'/>" + text(72, NOTES + 32, "owns a group that is now odd: 6 of the 10 groups fail, so the magician knows someone lied", size=18, anchor='start')
body += note(70, "Try part 1's trick on the four big groups: those of 1000 and 0010 fail, which spells 1010.")
body += note(96, "But 1010 is honest. Only all ten groups together leave a pattern that names the cheaters.", weight=700)
body += note(130, "Received: 101110001000010 (the program's own 3-error test)", color=QUIET)
open("fig3.svg", "w").write(svg(1240, NOTES + 156, body))

# ---------- fig4: corner 1110 votes along its 7 parallel edges ----------
V = [0b1110, 0b1100, 0b1010, 0b0110, 0b1000, 0b0100, 0b0010]
edges, votes = [], []
for v in V:
    a, b = v, v | 1
    vote = (rx[a] + rx[b]) % 2; spoiled = a in ERR or b in ERR
    edges.append((a, b, RED if spoiled else GREEN)); votes.append((a, b, vote, spoiled))
body = text(40, 52, "Corner 1110 asks its question seven times, once per parallel edge", size=28, weight=700, anchor='start')
t, pos = tesseract(OX, OY, S, bits=rx, rings={c: RED for c in ERR}, edges_hi=edges, dim_others=True)
body += t
for a, b, vote, spoiled in votes:
    x, y = mid(pos, a, b, dy=-14)
    body += text(x, y, f"says {vote}", size=17, weight=700, color=(RED if spoiled else GREEN_TEXT))
body += note(0, "Question: \"what is the parity of my edge 1110–1111?\" The seven left-to-right edges are copies of that edge.")
body += note(26, "Without errors they all give the same answer, and no corner sits on two of them,")
body += note(52, "so each cheater can spoil only one answer. (The eighth copy, 0000–0001, is the empty corner's.)")
body += f"<line x1='40' y1='{NOTES+81}' x2='70' y2='{NOTES+81}' stroke='{GREEN}' stroke-width='7' stroke-linecap='round'/>" + text(80, NOTES + 87, "4 clean edges say 1", size=18, anchor='start')
body += f"<line x1='300' y1='{NOTES+81}' x2='330' y2='{NOTES+81}' stroke='{RED}' stroke-width='7' stroke-linecap='round'/>" + text(340, NOTES + 87, "3 edges with a cheater say 0", size=18, anchor='start')
body += text(640, NOTES + 87, "Majority: 1", size=20, weight=700, anchor='start')
open("fig4.svg", "w").write(svg(1240, NOTES + 114, body))

# ---------- fig5: each heavy corner votes along its own direction ----------
body = text(40, 52, "Every heavy corner votes along its own direction", size=28, weight=700, anchor='start')
panels = [(0b1110, 0, "1110: along the left-to-right edges"), (0b1101, 1, "1101: along the up-down edges"),
          (0b1011, 2, "1011: along the front-to-back edges"), (0b0111, 3, "0111: along the links between the cubes")]
s5 = 0.5
for i, (c, bit, title) in enumerate(panels):
    ox = 90 + (i % 2) * 610; top = 90 + (i // 2) * 520; oy = top + 50 + 93 * s5
    hi = []; ones = zeros = 0
    for v in range(1, 16):
        if v & c == v:
            a, b = v, v | (1 << bit)
            vote = (rx[a] + rx[b]) % 2; spoiled = a in ERR or b in ERR
            ones += vote; zeros += 1 - vote
            hi.append((a, b, RED if spoiled else GREEN))
    t, pos = tesseract(ox, oy, s5, bits=None, rings={x: RED for x in ERR}, edges_hi=hi, dim_others=True, names=False, r=10)
    body += t
    dec = 1 if ones > zeros else 0
    body += text(ox - 30, top + 30, title, size=19, weight=700, anchor='start')
    body += text(ox - 30, oy + 560 * s5 + 48, f"{ones} edges say 1, {zeros} say 0  →  majority {dec}", size=19, weight=700, color=GREEN_TEXT, anchor='start')
body += text(40, 1150, "Green edges are clean, red ones hold a cheater. Each corner gets 7 answers and 3 cheaters spoil at most 3, so every majority is right.", size=17, color=QUIET, anchor='start')
open("fig5.svg", "w").write(svg(1240, 1178, body))

# ---------- fig6: 1111 votes last, then the secrets come back ----------
after = {0b1111: 1, 0b0111: 0, 0b1011: 1, 0b1101: 1, 0b1110: 1, 0b0011: 1, 0b0101: 1}   # from trace.py
bits = {c: after.get(c, '') for c in range(1, 16)}
rings = {c: (RED if c in ERR else GREEN) for c in after}
roles = {c: (OK_C if c in after and c not in ERR else PINK if c in after else 'white') for c in range(1, 16)}
body = text(40, 52, "Last question: corner 1111. Seven single corners answer, and the secrets come back", size=28, weight=700, anchor='start')
t, pos = tesseract(OX, OY, S, bits=bits, roles=roles, rings=rings, dim_others=True)
body += t
body += note(0, "Take the four answers out of the picture (flip the corners they account for); what is left at each ringed corner")
body += note(26, "is just 1111's own bit. Six say 1, the liar at 0111 says 0: corner 1111 = 1.")
body += note(68, "Now every secret is one step away: a heavy corner's secret = its edge's answer combined with 1111's bit.", weight=700)
rows = [("1111", "its vote", "1"), ("1110", "1 ⊕ 1", "0"), ("1101", "0 ⊕ 1", "1"), ("1011", "0 ⊕ 1", "1"), ("0111", "1 ⊕ 1", "0")]
x = 40
for name, expr, val in rows:
    body += f"<rect x='{x}' y='{NOTES+90}' width='200' height='70' rx='8' fill='{DATA_FILL}' stroke='{EDGE}' stroke-width='1.5'/>"
    body += text(x + 100, NOTES + 116, name, size=17, color=QUIET) + text(x + 100, NOTES + 146, f"{expr} = {val}", size=21, weight=700)
    x += 220
body += note(200, "Recovered 10110, exactly what was sent, with three of the fifteen seats lying.", size=20, weight=700, color=GREEN_TEXT)
open("fig6.svg", "w").write(svg(1240, NOTES + 226, body))
