from p1common import *
OK_RING, BAD = "#2a9d4b", RED

def check_panel(received, checked, title, lines, cheaters=(), blamed=None, final=False):
    """One frame of the 'check each group' animation on the cube."""
    fails = {p: sum(received[a] for a in members(p)) % 2 == 1 for p in checked}
    faces = [(p, (FAIL_C if fails[p] else OK_C), 0.35) for p in checked]
    fills = {CORNER[a]: (FAIL_C if final and a in cheaters else 'white') for a in range(1, 8)}
    rings = {CORNER[a]: BAD for a in cheaters} if final else {}
    if blamed:
        rings[CORNER[blamed]] = "#e08a00"
    t, pos = draw_cube(330, 230, 1.0, inside={CORNER[a]: received[a] for a in range(1, 8)}, fills=fills, rings=rings, faces=faces, label='full')
    body = text(40, 52, title, size=27, weight=700, anchor='start') + t
    if blamed:
        x, y = pos[CORNER[blamed]]
        body += f"<circle cx='{x:.1f}' cy='{y:.1f}' r='32' fill='none' stroke='#e08a00' stroke-width='3' stroke-dasharray='6 5'/>"
    yb = 600
    for i, p in enumerate((5, 6, 7)):
        x = 40 + i * 230
        st = fails.get(p)
        fill = '#e9e9e9' if st is None else (FAIL_C if st else OK_C)
        body += f"<rect x='{x}' y='{yb}' width='210' height='40' rx='6' fill='{fill}'/>" + text(x + 105, yb + 26, f"group of {p}: " + ('?' if st is None else 'fails' if st else 'passes'), size=17, weight=700)
    for i, (s, kw) in enumerate(lines):
        body += text(40, 690 + 30 * i, s, size=19, weight=kw.get('weight', 400), color=kw.get('color', INK), anchor='start')
    return svg(1240, 760, body), fails

honest = dict(BITS)
frames = []
for cheater in (5, 4):
    rx = dict(honest); rx[cheater] ^= 1
    frames.append(check_panel(rx, [], f"Round {1 if cheater == 5 else 2}: someone flipped a bit",
        [("Everyone reveals their number. Who cheated? The magician checks the three groups.", {})])[0])
    checked = []
    for p in (5, 6, 7):
        checked.append(p)
        total = sum(rx[a] for a in members(p))
        f, fails = check_panel(rx, checked, f"Round {1 if cheater == 5 else 2}: check the group of {p}",
            [(f"Members {', '.join(str(a) for a in members(p))} hold " + " + ".join(str(rx[a]) for a in members(p)) +
              f" = {total}: " + ("odd, so the group fails." if total % 2 else "even, so it passes."), {'weight': 700})])
        frames.append(f)
    failing = [p for p in (5, 6, 7) if fails[p]]
    why = ("Only the group of 5 fails. Number 5 is the only one who sits in that group and in no other."
           if cheater == 5 else "Groups of 5 and 7 fail, 6 passes. Only number 4 sits in exactly those two groups.")
    frames.append(check_panel(rx, checked, f"Round {1 if cheater == 5 else 2}: number {cheater} cheated!", [(why, {'weight': 700}),
        (f"Read the failures as bits (fail = 1): {''.join('1' if fails[p] else '0' for p in (5, 6, 7))} is corner {B3(CORNER[cheater])}, number {cheater}'s seat.", {'color': QUIET})],
        cheaters=[cheater], final=True)[0])
for i, f in enumerate(frames):
    open(f"catch_{i:02d}.svg", "w").write(f)
print(len(frames), "catch frames")

# ---------- figure 2: Hamming (7, 4) used to send information ----------
s = 0.52
panels = [(60, "1. Encoder", "1, 2, 3, 4 hold 1, 0, 1, 1; 5, 6, 7 even out their faces"),
          (470, "2. Noisy channel", "number 2's bit flips on the way"),
          (870, "3. Receiver", "all three faces fail: only number 2 sits in all three")]
body = text(40, 52, "Hamming (7, 4) used in transmitting information", size=28, weight=700, anchor='start')
rx = dict(honest); rx[2] ^= 1
for i, (ox, name, cap) in enumerate(panels):
    bits = honest if i == 0 else rx
    fills = {CORNER[a]: (P1_C if a >= 5 else DATA_C) for a in range(1, 8)} if i == 0 else {}
    rings = {CORNER[2]: RED} if i >= 1 else {}
    faces = [(5, FACE_COL[5], 0.14), (6, FACE_COL[6], 0.14), (7, FACE_COL[7], 0.14)] if i == 0 else \
            ([(p, FAIL_C, 0.35) for p in (5, 6, 7)] if i == 2 else [])
    if i == 2:
        fills = {CORNER[2]: FAIL_C}
    t, pos = draw_cube(ox + 40, 240, s, inside={CORNER[a]: bits[a] for a in range(1, 8)}, fills=fills, rings=rings, faces=faces, label='full', r=17)
    body += t
    if i == 1:
        x, y = pos[CORNER[2]]
        body += bolt(x + 14, y - 46)
    body += text(ox + 150, 470, name, size=21, weight=700) + text(ox + 150, 498, cap, size=15, color=QUIET)
    if i < 2:
        body += f"<path d='M{ox + 318} 300 h40' stroke='{INK}' stroke-width='3' marker-end='url(#arr)'/>"
body = body.replace("<rect width", "<defs><marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0 0L10 5L0 10z' fill='#222'/></marker></defs><rect width", 1)
body += text(40, 560, "Number 2 is fixed back to 0, and the four secrets 1, 0, 1, 1 come through.", size=19, weight=700, anchor='start')
open("fig2.svg", "w").write(svg(1240, 590, body).replace("<rect width", "<defs><marker id='arr' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' orient='auto'><path d='M0 0L10 5L0 10z' fill='#222'/></marker></defs><rect width", 1))

# ---------- figure 5: two cheaters fool the cube ----------
rx = dict(honest); rx[1] ^= 1; rx[3] ^= 1
f, fails = check_panel(rx, [5, 6, 7], "Two cheaters: the faces blame an innocent seat",
    [("Numbers 1 and 3 both cheat. Both sit in the group of 6, so their flips cancel and it passes.", {}),
     ("Groups 5 and 7 fail, which spells 101: number 4, who is honest. The trick needs bigger ideas: part 2.", {'weight': 700})],
    cheaters=[1, 3], blamed=4, final=True)
open("fig5.svg", "w").write(f)
print("fig5 fails", fails)
