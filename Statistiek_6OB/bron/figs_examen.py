import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from figs import NAVY,TEAL,ORANGE,CORAL,GREY,save
import figs
figs.OUT="figuren/"
def f_staaf():
    yrs=["2019","2020","2021","2022","2023"]; v=[60,62,65,68,72]
    fig,ax=plt.subplots(figsize=(6.2,3.0)); b=ax.bar(yrs,v,color=ORANGE); ax.set_ylim(58,74); ax.set_ylabel("aantal leden")
    for r,val in zip(b,v): ax.text(r.get_x()+r.get_width()/2,val+0.3,str(val),ha="center",fontsize=9)
    ax.set_title("Onze jeugdbeweging explodeert!",loc="left",fontweight="bold",fontsize=10)
    fig.tight_layout(); save(fig,"exam_staaf")
def f_hist():
    q=norm.ppf((np.arange(1,151)-0.5)/150); rng=np.random.default_rng(31)
    d=np.round(110+4.6*q+rng.normal(0,0.7,150)).astype(int)
    fig,ax=plt.subplots(figsize=(6.4,3.0)); ax.hist(d,bins=np.arange(95.5,125,3),color=TEAL,edgecolor="white")
    ax.set_xlabel("lengte (cm)"); ax.set_ylabel("aantal kinderen"); fig.tight_layout(); save(fig,"exam_hist")
    print("x̄",d.mean(),"s",d.std(ddof=1),"med",np.median(d))
if __name__=="__main__": f_staaf(); f_hist()
