from figs import *
B4 = lambda c: format(c, '04b')
w = lambda c: bin(c).count('1')
GROUPS = order[5:]                                   # program order: 6 squares, then 4 cubes
SEATS = order                                        # 5 secrets, 6 square parities, 4 cube parities
inside = lambda s, g: s & g == g
CHEAT = [0b1101, 0b0110]
x0, y0, cw_, rh = 250, 170, 86, 36
body = text(40, 52, "Every seat has a fingerprint: the groups it sits in", size=28, weight=700, anchor='start')
body += text(40, 84, "A dot means the seat is in that parity bit's group (it has 1s wherever the group's corner has 1s).", size=18, color=QUIET, anchor='start')
for j, g in enumerate(GROUPS):
    x = x0 + j * cw_ + cw_ / 2
    fill = P2_C if w(g) == 2 else P1_C
    body += f"<rect x='{x - 38}' y='{y0 - 46}' width='76' height='34' rx='6' fill='{fill}'/>" + text(x, y0 - 23, B4(g), size=17, weight=700)
body += text(x0 + 3 * cw_, y0 - 60, "square groups", size=16, color=QUIET) + text(x0 + 8 * cw_, y0 - 60, "cube groups", size=16, color=QUIET)
for i, s in enumerate(SEATS):
    y = y0 + i * rh
    role = DATA_C if w(s) >= 3 else P2_C if w(s) == 2 else P1_C
    if i % 2 == 0:
        body += f"<rect x='{x0 - 200}' y='{y}' width='{10 * cw_ + 200}' height='{rh}' fill='#f6f6f6'/>"
    body += f"<circle cx='{x0 - 180}' cy='{y + rh / 2}' r='10' fill='{role}' stroke='{EDGE}' stroke-width='1.5'/>"
    body += text(x0 - 160, y + rh / 2 + 6, f"seat {B4(s)}", size=18, weight=(700 if s in CHEAT else 400), color=(RED if s in CHEAT else INK), anchor='start')
    for j, g in enumerate(GROUPS):
        if inside(s, g):
            body += f"<circle cx='{x0 + j * cw_ + cw_ / 2}' cy='{y + rh / 2}' r='9' fill='{RED if s in CHEAT else INK}'/>"
# the 2-cheater example: combine fingerprints
yb = y0 + len(SEATS) * rh + 40
body += text(40, yb, "Two cheaters, 1101 and 0110: a group fails when an odd number of them sit in it.", size=19, weight=700, anchor='start')
yr = yb + 22
body += text(x0 - 160, yr + 24, "fails?", size=18, weight=700, anchor='start')
fails = []
for j, g in enumerate(GROUPS):
    n = sum(inside(s, g) for s in CHEAT)
    f = n % 2 == 1; fails.append(f)
    x = x0 + j * cw_ + cw_ / 2
    body += f"<rect x='{x - 38}' y='{yr}' width='76' height='34' rx='6' fill='{FAIL_C if f else OK_C}'/>" + text(x, yr + 23, ("fail" if f else "pass") + f" ({n})", size=15, weight=700)
body += text(40, yr + 70, "(n) = how many cheaters sit in the group. Two cheaters in the same group cancel out, which is why part 1 broke.", size=17, color=QUIET, anchor='start')
body += text(40, yr + 98, "But no other set of three or fewer seats leaves this exact pattern: checked for all 576 possible sets.", size=17, weight=700, anchor='start')
open("fig9.svg", "w").write(svg(1240, yr + 124, body))
print("fails:", [B4(g) for g, f in zip(GROUPS, fails) if f], "height", yr + 124)
