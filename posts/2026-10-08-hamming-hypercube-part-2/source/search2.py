import random, math, itertools
random.seed(7)
A = 560
edges = [(a, a ^ (1 << k)) for a in range(16) for k in range(4) if a < a ^ (1 << k)]
def layout(DO, BS, DI):
    oc = (A / 2 + DO[0] / 2, A / 2 + DO[1] / 2)                 # outer cube centre
    IP = (oc[0] - BS / 2 - DI[0] / 2, oc[1] - BS / 2 - DI[1] / 2)  # inner cube centred on it
    pos = {}
    for c in range(16):
        b3, b2, b1, b0 = (c >> 3) & 1, (c >> 2) & 1, (c >> 1) & 1, c & 1
        pos[c] = (b0 * A + b2 * DO[0], b1 * A + b2 * DO[1]) if b3 else (IP[0] + b0 * BS + b2 * DI[0], IP[1] + b1 * BS + b2 * DI[1])
    return pos, IP
def seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = dx * dx + dy * dy
    t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
def score(pos):
    cc = min(math.dist(pos[a], pos[b]) for a, b in itertools.combinations(range(16), 2))
    ce = min(seg_dist(pos[c], pos[a], pos[b]) for c in range(16) for a, b in edges if c not in (a, b))
    return min(cc / 2.2, ce)
best = None
for _ in range(80000):
    DO = (random.uniform(120, 280), random.uniform(-220, -80))
    BS = random.uniform(140, 280)
    DI = (random.uniform(-160, 200), random.uniform(-200, 120))
    pos, IP = layout(DO, BS, DI)
    s = score(pos)
    if best is None or s > best[0]:
        best = (s, DO, BS, DI, IP)
print(best)

best = None
for _ in range(80000):
    DO = (random.uniform(140, 300), random.uniform(-220, -90))
    BS = random.uniform(150, 300)
    k = random.uniform(0.25, 0.9); ang = math.radians(random.uniform(-15, 15))
    DI = (k * (DO[0] * math.cos(ang) - DO[1] * math.sin(ang)), k * (DO[0] * math.sin(ang) + DO[1] * math.cos(ang)))
    pos, IP = layout(DO, BS, DI)
    s = score(pos)
    if best is None or s > best[0]:
        best = (s, DO, BS, DI, IP)
print("same orientation:", best)
