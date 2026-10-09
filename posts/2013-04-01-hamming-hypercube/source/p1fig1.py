from p1common import *
# Figure 1: the three groups are the three faces of a cube
body = text(40, 52, "The magic's explanation: three groups, three faces of a cube", size=28, weight=700, anchor='start')
fills = {CORNER[a]: (P1_C if a >= 5 else DATA_C) for a in range(1, 8)}
t, pos = draw_cube(330, 250, 1.0, inside={CORNER[a]: a for a in range(1, 8)}, fills=fills,
                   faces=[(5, FACE_COL[5], 0.16), (6, FACE_COL[6], 0.16), (7, FACE_COL[7], 0.16)], label='full')
body += t
y = 620
for p in (5, 6, 7):
    m = ", ".join(str(a) for a in members(p))
    body += f"<rect x='40' y='{y - 16}' width='22' height='22' rx='4' fill='{FACE_COL[p]}' fill-opacity='0.5' stroke='{FACE_COL[p]}' stroke-width='2'/>"
    body += text(74, y + 1, f"group of {p}: audience members {m} (every corner whose {['first','second','third'][[0b100,0b010,0b001].index(GROUP_OF[p])]} bit is 1)", size=18, anchor='start')
    y += 32
body += f"<circle cx='51' cy='{y - 6}' r='11' fill='{DATA_C}' stroke='{EDGE}' stroke-width='2'/>" + text(74, y, "1-4 pick their bits freely", size=18, anchor='start')
body += f"<circle cx='351' cy='{y - 6}' r='11' fill='{P1_C}' stroke='{EDGE}' stroke-width='2'/>" + text(374, y, "5, 6, 7 make their group's sum even", size=18, anchor='start')
body += f"<circle cx='741' cy='{y - 6}' r='11' fill='white' stroke='#bbb' stroke-dasharray='4 4' stroke-width='2'/>" + text(764, y, "corner 000: nobody sits there", size=18, anchor='start')
open("fig1.svg", "w").write(svg(1240, y + 30, body))
print("height", y + 30)
