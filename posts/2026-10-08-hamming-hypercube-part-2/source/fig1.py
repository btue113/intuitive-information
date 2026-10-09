from figs import *
w = lambda c: bin(c).count('1')
# Part 1 ended with Hamming (15, 11) on the tesseract; part 2 keeps the tesseract and moves parity one level deeper.
part1 = {c: (P1_C if w(c) == 1 else DATA_C) for c in range(1, 16)}
part2 = {c: (P1_C if w(c) == 1 else P2_C if w(c) == 2 else DATA_C) for c in range(1, 16)}
body = text(40, 52, "Same tesseract, parity one level deeper", size=28, weight=700, anchor='start')
t, _ = tesseract(60, 180, 0.55, roles=part1)
body += t
body += text(300, 560, "Part 1: Hamming (15, 11)", size=21, weight=700)
body += text(300, 588, "4 parity seats, catches 1 cheater", size=18, color=QUIET)
t, _ = tesseract(650, 180, 0.55, roles=part2)
body += t
body += text(890, 560, "Part 2: two parity dimensions (15, 5)", size=21, weight=700)
body += text(890, 588, "4 + 6 parity seats, catches 3 cheaters", size=18, color=QUIET)
lx = 120
for fill, label in [(DATA_C, "data (secret) seat"), (P1_C, "parity, 1 one in its name"), (P2_C, "parity, 2 ones in its name"), ("white", "0000: left empty")]:
    body += f"<circle cx='{lx}' cy='650' r='12' fill='{fill}' stroke='{EDGE if fill != 'white' else '#bbb'}' stroke-width='2' {'stroke-dasharray=\"4 4\"' if fill == 'white' else ''}/>"
    body += text(lx + 22, 656, label, size=17, anchor='start')
    lx += 280
open("fig1.svg", "w").write(svg(1240, 690, body))
