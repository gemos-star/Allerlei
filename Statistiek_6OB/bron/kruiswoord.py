"""Genereert een kruiswoordraadsel (eenvoudige backtracking) en schrijft het als LaTeX-tabel."""
import random, sys, json
WOORDEN=["STEEKPROEF","CAUSALITEIT","MEDIAAN","HYPOTHESE","UITSCHIETER","POPULATIE","RANDOMISATIE","VARIANTIE"]

def probeer(woorden,rng):
    grid={}   # (r,c)->letter
    plaatsing=[]  # (woord,r,c,richting)
    def kan(w,r,c,d):
        kruis=0
        dr,dc=(0,1) if d=="H" else (1,0)
        # cel voor en na moeten leeg zijn
        if (r-dr,c-dc) in grid or (r+dr*len(w),c+dc*len(w)) in grid: return None
        for i,ch in enumerate(w):
            rr,cc=r+dr*i,c+dc*i
            if (rr,cc) in grid:
                if grid[(rr,cc)]!=ch: return None
                kruis+=1
            else:
                # buurcellen loodrecht op de richting moeten leeg zijn
                for (ar,ac) in ((rr+dc,cc+dr),(rr-dc,cc-dr)):
                    if (ar,ac) in grid: return None
        return kruis
    def zet(w,r,c,d):
        dr,dc=(0,1) if d=="H" else (1,0)
        nieuw=[]
        for i,ch in enumerate(w):
            p=(r+dr*i,c+dc*i)
            if p not in grid: grid[p]=ch; nieuw.append(p)
        plaatsing.append((w,r,c,d)); return nieuw
    w0=woorden[0]; zet(w0,0,0,"H")
    rest=woorden[1:]
    def rec(i):
        if i==len(rest): return True
        w=rest[i]
        opties=[]
        for (w2,r2,c2,d2) in plaatsing:
            dn="V" if d2=="H" else "H"
            for a,ch in enumerate(w):
                for b,ch2 in enumerate(w2):
                    if ch!=ch2: continue
                    if d2=="H": r,c=r2-a,c2+b
                    else: r,c=r2+b,c2-a
                    k=kan(w,r,c,dn)
                    if k is not None and k>=1: opties.append((r,c,dn,k))
        rng.shuffle(opties)
        for (r,c,dn,k) in opties[:40]:
            nieuw=zet(w,r,c,dn)
            if rec(i+1): return True
            for p in nieuw: del grid[p]
            plaatsing.pop()
        return False
    ok=rec(0)
    return (grid,plaatsing) if ok else None

best=None
for seed in range(4000):
    rng=random.Random(seed); ws=WOORDEN[:]; rng.shuffle(ws)
    # langste woord eerst voor betere kans
    ws.sort(key=lambda w:-len(w)) if seed%2 else None
    res=probeer(ws,rng)
    if not res: continue
    grid,pl=res
    rs=[p[0] for p in grid]; cs=[p[1] for p in grid]
    h=max(rs)-min(rs)+1; b=max(cs)-min(cs)+1
    score=(max(h,b), h*b)
    if best is None or score<best[0]: best=(score,grid,pl,min(rs),min(cs),h,b)
score,grid,pl,r0,c0,h,b=best
print("afmetingen",h,"x",b,file=sys.stderr)
# nummering
starts={}
for (w,r,c,d) in pl: starts.setdefault((r-r0,c-c0),[]).append((w,d))
cells=sorted(starts.keys())
nummers={p:i+1 for i,p in enumerate(cells)}
hor=[];ver=[]
for (w,r,c,d) in pl:
    n=nummers[(r-r0,c-c0)]
    (hor if d=="H" else ver).append((n,w))
hor.sort(); ver.sort()
rows=[]
for r in range(h):
    row=[]
    for c in range(b):
        if (r+r0,c+c0) in grid: row.append(str(nummers[(r,c)]) if (r,c) in nummers else "")
        else: row.append("\\#")
    rows.append(row)
json.dump({"hor":hor,"ver":ver,"h":h,"b":b,"rows":rows},open("kruiswoord.json","w"),ensure_ascii=False)
print(json.dumps({"hor":hor,"ver":ver}),file=sys.stderr)
for row in rows: print(" ".join(x if x else "." for x in row).replace("\\#","#"),file=sys.stderr)
