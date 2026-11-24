import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
from scipy.stats import norm
from calc import *

NAVY="#1B2B4B"; TEAL="#0E8C8C"; ORANGE="#F28C28"; CORAL="#D64550"; INDIGO="#5B4B9A"; GREY="#8A94A6"; LTEAL="#BFE6E4"; LORANGE="#FFD9A8"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.edgecolor":GREY,"axes.labelcolor":NAVY,
    "xtick.color":NAVY,"ytick.color":NAVY,"axes.spines.top":False,"axes.spines.right":False,"text.color":NAVY})
OUT="figuren/"
def save(fig,name):
    fig.savefig(OUT+name+".png",dpi=200,bbox_inches="tight",facecolor="white"); plt.close(fig)

# ---------- F1 (L1) gemiddelde, mediaan en uitschieter
def f_uitschieter():
    d1=[9,10,11,12,15,15,15,18,21]; d2=[9,10,11,12,15,15,15,18,60]
    fig,axs=plt.subplots(2,1,figsize=(7,3.2),sharex=True)
    for ax,d,t in zip(axs,[d1,d2],["Zonder uitschieter","Met uitschieter (21 wordt 60)"]):
        from collections import Counter
        c=Counter(d)
        for v,k in c.items():
            ax.scatter([v]*k,range(1,k+1),s=90,color=TEAL,zorder=3)
        ax.axvline(mean(d),color=CORAL,lw=2,label=f"gemiddelde = {mean(d):.1f}".replace(".",","))
        ax.axvline(median(d),color=ORANGE,lw=2,ls="--",label=f"mediaan = {median(d):.0f}")
        ax.set_yticks([]); ax.set_ylim(0,4); ax.set_title(t,loc="left",fontsize=10,color=NAVY,fontweight="bold")
        ax.legend(loc="upper right",frameon=False,fontsize=9); ax.spines["left"].set_visible(False)
    axs[1].set_xlabel("aantal uitgeleende boeken"); axs[1].set_xlim(5,65)
    fig.tight_layout(); save(fig,"l1_uitschieter")

# ---------- F2 (L2) drie dotplots
def datasets_dot():
    a=[20+o for o in [-2,-1,-1,-1,0,0,0,0,0,0,0,0,1,1,1,2,0,0,-1,1]]   # klein
    b=[20+o for o in [-7,-5,-4,-3,-3,-2,-1,-1,0,0,0,0,1,1,2,3,3,4,5,7]]  # middel
    c=[20+o for o in [-14,-12,-11,-9,-8,-7,-5,-4,-2,-1,1,2,4,5,7,8,9,11,12,14]]  # groot
    return a,b,c
def f_dotplots():
    a,b,c=datasets_dot()
    fig,axs=plt.subplots(3,1,figsize=(7,4.6),sharex=True)
    from collections import Counter
    for ax,d,t in zip(axs,[b,c,a],["Grafiek A","Grafiek B","Grafiek C"]):
        cc=Counter(d)
        for v,k in cc.items(): ax.scatter([v]*k,range(1,k+1),s=40,color=TEAL,zorder=3)
        ax.axvline(mean(d),color=CORAL,lw=1.5)
        ax.set_yticks([]); ax.set_ylim(0,max(cc.values())+1); ax.spines["left"].set_visible(False)
        ax.set_ylabel(t,rotation=0,ha="right",va="center",fontweight="bold",color=NAVY)
    axs[2].set_xlabel("waarde"); axs[2].set_xlim(0,40)
    fig.tight_layout(); save(fig,"l2_dotplots")
    for n,d in zip("ABC",[b,c,a]): print("dotplot",n,"mean",round(mean(d),2),"sd_pop",round(sd_pop(d),2))

# ---------- F3 (L2) boxplots
def f_boxplots():
    fig,ax=plt.subplots(figsize=(7,2.6))
    groups=[("Klas X",(4,10,12,16,21)),("Klas Y",(8,12,14,15,19))]
    for i,(nm,(mn,q1,med,q3,mx)) in enumerate(groups):
        y=i
        ax.plot([mn,q1],[y,y],color=NAVY,lw=2); ax.plot([q3,mx],[y,y],color=NAVY,lw=2)
        ax.plot([mn,mn],[y-.15,y+.15],color=NAVY,lw=2); ax.plot([mx,mx],[y-.15,y+.15],color=NAVY,lw=2)
        ax.add_patch(plt.Rectangle((q1,y-.3),q3-q1,.6,facecolor=[LTEAL,LORANGE][i],edgecolor=NAVY,lw=2))
        ax.plot([med,med],[y-.3,y+.3],color=CORAL,lw=3)
    ax.set_yticks([0,1]); ax.set_yticklabels([g[0] for g in groups],fontweight="bold")
    ax.set_xlim(0,24); ax.set_ylim(-.7,1.7); ax.set_xlabel("aantal gelezen boeken"); ax.grid(axis="x",color="#E5E8EE")
    ax.set_xticks(range(0,25,2))
    fig.tight_layout(); save(fig,"l2_boxplot")

# ---------- F4 (L3) populatie en steekproef: representatief vs vertekend
def f_steekproef():
    rng=np.random.default_rng(7)
    fig,axs=plt.subplots(1,3,figsize=(8,2.9))
    N=60
    pts=rng.uniform(-1,1,(400,2)); pts=pts[(pts**2).sum(1)<0.9][:N]
    cols=np.array([TEAL]*40+[ORANGE]*20); rng.shuffle(cols)
    ax=axs[0]; ax.scatter(pts[:,0],pts[:,1],c=cols,s=45); ax.set_title("Populatie\n(2/3 blauw, 1/3 oranje)",fontsize=9,fontweight="bold")
    # representatief: 12 punten 8 blauw 4 oranje
    blue=[i for i in range(N) if cols[i]==TEAL]; org=[i for i in range(N) if cols[i]==ORANGE]
    rep=blue[:8]+org[:4]
    ax=axs[1]; ax.scatter(pts[:,0],pts[:,1],c="#E3E7EE",s=45); ax.scatter(pts[rep,0],pts[rep,1],c=cols[rep],s=70,edgecolors=NAVY,linewidths=1.3)
    ax.set_title("Representatieve steekproef\n(8 blauw, 4 oranje)",fontsize=9,fontweight="bold",color=TEAL)
    bad=org[:10]+blue[:2]
    ax=axs[2]; ax.scatter(pts[:,0],pts[:,1],c="#E3E7EE",s=45); ax.scatter(pts[bad,0],pts[bad,1],c=cols[bad],s=70,edgecolors=NAVY,linewidths=1.3)
    ax.set_title("Vertekende steekproef\n(10 oranje, 2 blauw)",fontsize=9,fontweight="bold",color=CORAL)
    for ax in axs:
        ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
        for s in ax.spines.values(): s.set_visible(False)
        ax.add_patch(Circle((0,0),1.0,fill=False,edgecolor=GREY,lw=1.5))
        ax.set_xlim(-1.1,1.1); ax.set_ylim(-1.1,1.1)
    fig.tight_layout(); save(fig,"l3_steekproef")

# ---------- F5 (L4) spreidingsdiagrammen
def f_scatter():
    rng=np.random.default_rng(3)
    fig,axs=plt.subplots(1,3,figsize=(8.4,2.9))
    x=rng.uniform(3,10,25)
    specs=[("Grafiek 1","uren geslapen","concentratiescore",x,5*x+rng.normal(0,5,25)+20),
           ("Grafiek 2","uren schermtijd","uren slaap",x,12-0.7*x+rng.normal(0,.6,25)),
           ("Grafiek 3","schoenmaat leerkracht","punten op toets",rng.uniform(36,46,25),rng.uniform(30,90,25))]
    for ax,(t,xl,yl,xx,yy) in zip(axs,specs):
        ax.scatter(xx,yy,color=TEAL,s=35,alpha=.85,edgecolors="white")
        ax.set_title(t,fontsize=10,fontweight="bold"); ax.set_xlabel(xl,fontsize=8.5); ax.set_ylabel(yl,fontsize=8.5)
        ax.tick_params(labelsize=8)
    fig.tight_layout(); save(fig,"l4_spreiding")

# ---------- F6 (L4) schema verborgen variabele
def f_verborgen():
    fig,ax=plt.subplots(figsize=(7,3.0)); ax.axis("off"); ax.set_xlim(0,10); ax.set_ylim(0,4.2)
    def box(x,y,w,h,txt,fc,ec):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05,rounding_size=0.15",fc=fc,ec=ec,lw=2))
        ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=10,fontweight="bold",color=NAVY)
    box(3.2,3.0,3.6,0.9,"warm weer\n(verborgen variabele)",LORANGE,ORANGE)
    box(0.2,0.3,3.2,0.9,"meer ijsjes\nverkocht",LTEAL,TEAL)
    box(6.6,0.3,3.2,0.9,"meer\nverdrinkingen",LTEAL,TEAL)
    def arr(a,b,ls="-",c=ORANGE): ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=18,lw=2.2,color=c,ls=ls))
    arr((4.3,2.95),(2.4,1.3)); arr((5.7,2.95),(7.6,1.3))
    ax.add_patch(FancyArrowPatch((3.5,.75),(6.5,.75),arrowstyle="<|-|>",mutation_scale=16,lw=2,color=CORAL,ls=(0,(4,3))))
    ax.text(5,0.98,"samenhang ≠ oorzaak",ha="center",fontsize=9,color=CORAL,fontweight="bold")
    fig.tight_layout(); save(fig,"l4_verborgen")

# ---------- F7 (L5) Gausskromme met 68-95-99,7
def f_gauss_regel():
    mu,s=0,1; x=np.linspace(-4,4,600); y=norm.pdf(x)
    fig,ax=plt.subplots(figsize=(7.2,3.6))
    ax.plot(x,y,color=NAVY,lw=2.4)
    for k,col,al in [(3,LTEAL,1),(2,"#7FCFCB",1),(1,TEAL,1)]:
        m=(x>=-k)&(x<=k); ax.fill_between(x[m],y[m],color=col,alpha=al,lw=0)
    ax.plot(x,y,color=NAVY,lw=2.4)
    ax.axvline(0,color=NAVY,lw=1.2,ls="--")
    ax.set_xticks([-3,-2,-1,0,1,2,3]); ax.set_xticklabels([r"$\mu-3\sigma$",r"$\mu-2\sigma$",r"$\mu-\sigma$",r"$\mu$",r"$\mu+\sigma$",r"$\mu+2\sigma$",r"$\mu+3\sigma$"])
    ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_ylim(0,0.64)
    ax.annotate("",xy=(-1,0.45),xytext=(1,0.45),arrowprops=dict(arrowstyle="<->",color=NAVY,lw=1.6)); ax.text(0,0.465,"± 1σ: ≈ 68 %",ha="center",fontsize=9,fontweight="bold",bbox=dict(fc="white",ec="none",pad=1.5))
    ax.annotate("",xy=(-2,0.52),xytext=(2,0.52),arrowprops=dict(arrowstyle="<->",color=NAVY,lw=1.6)); ax.text(0,0.535,"± 2σ: ≈ 95 %",ha="center",fontsize=9,fontweight="bold",bbox=dict(fc="white",ec="none",pad=1.5))
    ax.annotate("",xy=(-3,0.59),xytext=(3,0.59),arrowprops=dict(arrowstyle="<->",color=NAVY,lw=1.6)); ax.text(0,0.605,"± 3σ: ≈ 99,7 %",ha="center",fontsize=9,fontweight="bold",bbox=dict(fc="white",ec="none",pad=1.5))
    # buigpunten
    for b in (-1,1): ax.plot([b],[norm.pdf(b)],"o",color=CORAL,ms=8,zorder=5)
    ax.text(1.05,norm.pdf(1)+.03,"buigpunt",color=CORAL,fontsize=8.5,fontweight="bold")
    fig.tight_layout(); save(fig,"l5_gauss_regel")

# ---------- F8 (L5) invloed van mu en sigma
def f_mu_sigma():
    x=np.linspace(20,90,700)
    fig,ax=plt.subplots(figsize=(7.2,3.2))
    for nm,mu,s,c in [("A",50,5,TEAL),("B",50,10,ORANGE),("C",65,5,INDIGO)]:
        y=norm.pdf(x,mu,s); ax.plot(x,y,color=c,lw=2.6); ax.text(mu,norm.pdf(mu,mu,s)+0.006,nm,ha="center",fontsize=13,fontweight="bold",color=c)
    ax.set_yticks([]); ax.spines["left"].set_visible(False); ax.set_xlabel("waarde van de variabele"); ax.set_ylim(0,0.1)
    ax.set_xticks(range(20,91,10))
    fig.tight_layout(); save(fig,"l5_mu_sigma")

# ---------- F9 (L5) kromme aflezen
def f_aflezen():
    mu,s=60,6; x=np.linspace(35,85,600); y=norm.pdf(x,mu,s)
    fig,ax=plt.subplots(figsize=(7,3.2))
    ax.plot(x,y,color=NAVY,lw=2.6); ax.fill_between(x,y,color=LTEAL,alpha=.6)
    ax.axvline(mu,color=CORAL,ls="--",lw=1.8)
    ax.plot([mu+s],[norm.pdf(mu+s,mu,s)],"o",color=CORAL,ms=9,zorder=5)
    ax.annotate("buigpunt",xy=(mu+s,norm.pdf(mu+s,mu,s)),xytext=(mu+s+4,norm.pdf(mu+s,mu,s)+.025),arrowprops=dict(arrowstyle="->",color=CORAL,lw=1.8),color=CORAL,fontweight="bold")
    ax.annotate("top",xy=(mu,norm.pdf(mu,mu,s)),xytext=(mu-10,norm.pdf(mu,mu,s)-.005),arrowprops=dict(arrowstyle="->",color=CORAL,lw=1.8),color=CORAL,fontweight="bold")
    ax.set_xticks([40,45,50,55,60,66,70,75,80]); ax.set_xticklabels(["40","45","50","55","60","66","70","75","80"])
    ax.set_xlabel("gewicht (kg)"); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    fig.tight_layout(); save(fig,"l5_aflezen")

# ---------- F10 (L5) vier histogrammen
def hist_data():
    rng=np.random.default_rng(11)
    A=np.round(rng.normal(177,7,300)).astype(int)                # lengte 17-jarige jongens (cm)
    B=np.round(np.exp(rng.normal(np.log(2600),0.55,300))/10).astype(int)*10   # inkomen (rechts scheef)
    C=np.round(np.concatenate([rng.normal(7,2.2,150),rng.normal(68,6,150)])).astype(int)  # leeftijd bezoekers
    C=np.clip(C,1,95)
    D=rng.integers(1,7,300)
    return A,B,C,D
def f_histogrammen():
    A,B,C,D=hist_data()
    fig,axs=plt.subplots(2,2,figsize=(7.6,5.2))
    specs=[(A,"Histogram 1","lengte (cm)",np.arange(155,201,4)),(B,"Histogram 2","maandinkomen (€)",np.arange(0,9500,500)),
           (C,"Histogram 3","leeftijd (jaar)",np.arange(0,100,8)),(D,"Histogram 4","aantal ogen",np.arange(0.5,7,1))]
    for ax,(d,t,xl,bins) in zip(axs.ravel(),specs):
        ax.hist(d,bins=bins,color=TEAL,edgecolor="white"); ax.set_title(t,fontweight="bold",fontsize=10,loc="left"); ax.set_xlabel(xl,fontsize=9); ax.set_ylabel("aantal",fontsize=9)
    fig.tight_layout(); save(fig,"l5_histogrammen")
    for nm,d in zip("ABCD",[A,B,C,D]): print("hist",nm,"n",len(d),"mean",round(float(np.mean(d)),1),"med",float(np.median(d)),"sd",round(float(np.std(d,ddof=1)),1))

# ---------- F11 (L5) histogram + model voor babylengtes
def baby_data():
    q=norm.ppf((np.arange(1,31)-0.5)/30)
    rng=np.random.default_rng(5)
    q=q+rng.normal(0,0.12,30)
    return [round(float(74+2.6*v),1) for v in q]
def f_baby():
    d=baby_data()
    fig,ax=plt.subplots(figsize=(7,3.2))
    ax.hist(d,bins=np.arange(66.5,82.6,1.5),color=LTEAL,edgecolor="white",density=False)
    ax.set_xlabel("lengte (cm)"); ax.set_ylabel("aantal kinderen")
    fig.tight_layout(); save(fig,"l5_baby_histogram")
    return d

# ---------- F12 (L6) gearceerde oppervlakten (koppelen)
def f_gearceerd():
    mu,s=0,1; x=np.linspace(-3.6,3.6,500); y=norm.pdf(x)
    fig,axs=plt.subplots(2,2,figsize=(7.4,4.6))
    cases=[("Figuur A",lambda x:x<=-0.8,[(-0.8,"a")]),("Figuur B",lambda x:x>=1.0,[(1.0,"a")]),
           ("Figuur C",lambda x:(x>=-1)&(x<=1.2),[(-1,"a"),(1.2,"b")]),("Figuur D",lambda x:(x<=-1.3)|(x>=1.3),[(-1.3,"a"),(1.3,"b")])]
    for ax,(t,cond,marks) in zip(axs.ravel(),cases):
        ax.plot(x,y,color=NAVY,lw=2); m=cond(x); ax.fill_between(x,y,where=m,color=ORANGE,alpha=.8)
        ax.set_title(t,fontweight="bold",fontsize=10,loc="left"); ax.set_yticks([]); ax.spines["left"].set_visible(False)
        ax.set_xticks([v for v,_ in marks]); ax.set_xticklabels([l for _,l in marks],fontweight="bold"); ax.set_ylim(0,.45)
    fig.tight_layout(); save(fig,"l6_gearceerd")

# ---------- F13 (L6) voorbeeld gearceerd P(X<2500)
def f_geboortegewicht():
    mu,s=3400,450; x=np.linspace(1700,5100,600); y=norm.pdf(x,mu,s)
    fig,ax=plt.subplots(figsize=(7,3.1))
    ax.plot(x,y,color=NAVY,lw=2.4); m=x<=2500; ax.fill_between(x[m],y[m],color=ORANGE,alpha=.85)
    ax.axvline(mu,color=NAVY,ls="--",lw=1)
    ax.set_xticks([2000,2500,3000,3400,4000,4500]); ax.set_xlabel("geboortegewicht (g)"); ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.annotate("P(X ≤ 2500)\n≈ 2,3 %",xy=(2300,0.0003),xytext=(1800,0.0006),fontsize=9,fontweight="bold",color=ORANGE if False else CORAL,
                arrowprops=dict(arrowstyle="->",color=CORAL,lw=1.5))
    fig.tight_layout(); save(fig,"l6_geboortegewicht")


# ---------- F14 (toets) twee histogrammen
def toets_data():
    rng=np.random.default_rng(21)
    q=norm.ppf((np.arange(1,201)-0.5)/200); a=np.round(25+5*q+rng.normal(0,0.6,200),0)
    e=np.round(np.sort(rng.exponential(12,200))+1,0)
    return a,e
def f_toetshist():
    a,e=toets_data()
    fig,axs=plt.subplots(1,2,figsize=(7.8,3.0))
    axs[0].hist(a,bins=np.arange(7.5,43,3),color=TEAL,edgecolor="white"); axs[0].set_title("Histogram P",loc="left",fontweight="bold"); axs[0].set_xlabel("tijd om een puzzel te maken (min)")
    axs[1].hist(e,bins=np.arange(0.5,80,5),color=ORANGE,edgecolor="white"); axs[1].set_title("Histogram Q",loc="left",fontweight="bold"); axs[1].set_xlabel("wachttijd op de spoeddienst (min)")
    for ax in axs: ax.set_ylabel("aantal",fontsize=9)
    fig.tight_layout(); save(fig,"toets_histogrammen")
    for nm,d in (("P",a),("Q",e)): print("toets hist",nm,"n",len(d),"mean",round(float(np.mean(d)),1),"med",float(np.median(d)),"sd",round(float(np.std(d,ddof=1)),1))

if __name__=="__main__":
    f_uitschieter(); f_dotplots(); f_boxplots(); f_steekproef(); f_scatter(); f_verborgen(); f_gauss_regel()
    f_mu_sigma(); f_aflezen(); f_histogrammen(); d=f_baby(); f_gearceerd(); f_geboortegewicht(); f_toetshist()
    print("baby",d); summary(d,"baby")
