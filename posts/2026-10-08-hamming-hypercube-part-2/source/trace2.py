import importlib.util, sys
from figs import order, cw
B = lambda v: format(v, '04b')
CHEAT = [0b1101, 0b0110]
rx = dict(cw)
for c in CHEAT: rx[c] ^= 1
word = ''.join(str(rx[c]) for c in order)
fails = [c for c in order[5:] if sum(rx[x] for x in range(1, 16) if x & c == c) % 2]
big = [c for c in fails if bin(c).count('1') == 1]
print("received:", word)
print("failing groups:", [B(c) for c in fails])
print("big groups failing:", [B(c) for c in big], "-> part-1 blames", B(sum(big)))
# votes per weight-3 corner (all 7 parallel edges)
for c in [0b1110, 0b1101, 0b1011, 0b0111]:
    free = 15 & ~c
    vs = [(rx[v] + rx[v | free]) % 2 for v in range(1, 16) if v & c == v]
    print("corner", B(c), "votes", vs, "ones", sum(vs), "->", int(sum(vs) > 3))
open("word2.txt", "w").write(word)
