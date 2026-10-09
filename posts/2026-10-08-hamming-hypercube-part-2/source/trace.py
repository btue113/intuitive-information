# Direct port of the 2013 CubeCode decoder for m=4, p=2 (punctured, 15 corners)
m,p=4,2
B=lambda v:format(v,'04b')
order=sorted(range(1,16),key=lambda c:(-bin(c).count('1'),-c))   # bit_to_cube
levels={w:[c for c in order if bin(c).count('1')==w] for w in range(4,0,-1)}
def unit(c): return [x for x in range(1,16) if x&c==c]
def par(code,cube): return sum(code[x] for x in cube)%2
def parallel(c,limit):
    pos=[i for i in range(m) if c>>i&1]; k=len(pos); out=[]
    for ones in range(k,0,-1):
        ws=sorted([w for w in range(1,1<<k) if bin(w).count('1')==ones],reverse=True)
        for w in ws:
            v=sum(1<<pos[i] for i in range(k) if w>>(k-1-i)&1)
            out.append(v)
            if len(out)==limit: return out
    return out
votes=(1<<(p+1))-1; need=1<<p
enc="101100011000110"
def word(s): return {order[i]:int(ch) for i,ch in enumerate(s)}
cw=word(enc)
for name,rx in [("t1","101110001000010"),("t2","101100011101111"),("t3","011000011000110")]:
    code=word(rx)
    errs=[B(c) for c in order if code[c]!=cw[c]]
    fails=[B(c) for c in order[5:] if par(code,unit(c))]
    print(f"== {name} received {rx}  errors at {errs}  failing checks: {fails}")
    coeff={c:0 for c in range(16)}
    for w in (3,4):   # dim 1 (weight 3) first, then weight 4
        mask={c:0 for c in range(16)}
        for c in levels[w]:
            vs=[]
            for V in parallel(c,votes):
                cube=[x for x in range(1,16) if x&c==V]
                vs.append((B(V),[B(x) for x in cube],par(code,cube)))
            t=[0,0]; dec=0
            for _,_,b in vs:
                t[b]+=1
                if t[b]==need: dec=b; break
            mask[c]=dec; coeff[c]=dec
            print(f"  corner {B(c)} votes:", [(v,b) for v,_,b in vs], "->", dec)
        # propagate over next p-1 = 1 lighter level, then cancel
        for c in levels[w-1] if w-1>=1 else []:
            mask[c]=par(mask,[x for x in unit(c) if x!=c])
        changed=[B(c) for c in range(1,16) if mask[c]]
        for c in range(1,16): code[c]^=mask[c]
        print(f"  cancel weight-{w} decisions: flip {changed}")
    data=[sum(coeff[x] for x in unit(c))%2 for c in order[:5]]
    print("  data:", ''.join(map(str,data)))
