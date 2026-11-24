import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figs import NAVY, save
import figs
figs.OUT="figuren/"
k=json.load(open("kruiswoord.json")); h,b=k["h"],k["b"]
def teken(naam,met_letters):
    fig,ax=plt.subplots(figsize=(b*0.5,h*0.5)); ax.set_xlim(0,b); ax.set_ylim(h,0); ax.set_aspect("equal"); ax.axis("off")
    for r in range(h):
        for c in range(b):
            cel=k["rows"][r][c]
            if cel=="\\#": continue
            ax.add_patch(Rectangle((c,r),1,1,fc="white",ec=NAVY,lw=1.6))
            if cel: ax.text(c+0.07,r+0.08,cel,fontsize=7.5,va="top",ha="left",color=NAVY)
            if met_letters: ax.text(c+0.5,r+0.58,k["letters"][r][c],fontsize=13,va="center",ha="center",color="#2E7D32",fontweight="bold")
    fig.tight_layout(pad=0.1); save(fig,naam)
teken("exam_kruiswoord",False); teken("exam_kruiswoord_opl",True); print("ok",h,b)
