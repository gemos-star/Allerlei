"""Hulpfuncties: alle getallen in de bundel worden hiermee gecontroleerd."""
import math, statistics as st
from scipy.stats import norm

def mean(x): return sum(x)/len(x)
def median(x):
    s=sorted(x); n=len(s)
    return s[n//2] if n%2 else (s[n//2-1]+s[n//2])/2
def quartiles(x):
    """Methode uit de les: mediaan van de onderste/bovenste helft (middelste waarde telt niet mee bij oneven n)."""
    s=sorted(x); n=len(s)
    low=s[:n//2]; up=s[n//2:] if n%2==0 else s[n//2+1:]
    return median(low), median(s), median(up)
def var_pop(x):
    m=mean(x); return sum((v-m)**2 for v in x)/len(x)
def var_samp(x):
    m=mean(x); return sum((v-m)**2 for v in x)/(len(x)-1)
def sd_pop(x): return math.sqrt(var_pop(x))
def sd_samp(x): return math.sqrt(var_samp(x))
def modes(x):
    from collections import Counter
    c=Counter(x); m=max(c.values()); return [k for k,v in c.items() if v==m], m
def summary(x,name=""):
    q1,q2,q3=quartiles(x)
    print(f"{name}: n={len(x)} som={sum(x)} mean={mean(x):.4f} med={median(x)} modes={modes(x)} "
          f"Q1={q1} Q3={q3} dQ={q3-q1} R={max(x)-min(x)} var_pop={var_pop(x):.4f} sd_pop={sd_pop(x):.4f} "
          f"var_s={var_samp(x):.4f} sd_s={sd_samp(x):.4f}")
