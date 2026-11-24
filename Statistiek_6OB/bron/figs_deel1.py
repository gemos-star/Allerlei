import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Ellipse
from figs import NAVY,TEAL,ORANGE,CORAL,INDIGO,GREY,LTEAL,LORANGE,save
import figs
figs.OUT="figuren/"

def f_cyclus():
    steps=["1 probleem-\nstelling","2 onderzoeks-\nvraag en\nhypothese","3 onderzoek\nopzetten en\nuitvoeren","4 data\nverzamelen","5 data analyseren\nen samenvatten","6 conclusies\ntrekken","7 antwoord op de\nonderzoeksvraag","8 reflecteren en\ncommuniceren"]
    fig,ax=plt.subplots(figsize=(7.2,5.0)); ax.set_xlim(-1.7,1.7); ax.set_ylim(-1.25,1.35); ax.axis("off"); ax.set_aspect("equal")
    cols=[TEAL,TEAL,TEAL,TEAL,ORANGE,ORANGE,ORANGE,INDIGO]
    n=8; pts=[]
    for i in range(n):
        ang=np.pi/2-i*2*np.pi/n
        x,y=1.2*np.cos(ang),0.95*np.sin(ang); pts.append((x,y))
    for i,(x,y) in enumerate(pts):
        ax.add_patch(FancyBboxPatch((x-0.38,y-0.17),0.76,0.34,boxstyle="round,pad=0.02,rounding_size=0.08",fc="white",ec=cols[i],lw=2.2))
        ax.text(x,y,steps[i],ha="center",va="center",fontsize=7.3,color=NAVY,fontweight="bold")
    for i in range(n):
        a=np.array(pts[i]); b=np.array(pts[(i+1)%n]); d=(b-a); d/=np.linalg.norm(d)
        s=a+d*0.36*(1 if abs(d[0])>abs(d[1]) else 0.5)+ (0 if abs(d[0])>abs(d[1]) else 0)
        ax.add_patch(FancyArrowPatch(a+d*0.33,b-d*0.33,arrowstyle="-|>",mutation_scale=12,lw=1.6,color=GREY,connectionstyle="arc3,rad=-0.15",shrinkA=0,shrinkB=0))
    ax.text(0,0.05,"onderzoeks-\ncyclus",ha="center",va="center",fontsize=11,fontweight="bold",color=NAVY)
    ax.text(0,-0.25,"(nieuwe onderzoeksvraag\nvoor een vervolgonderzoek)",ha="center",va="center",fontsize=7,color=GREY)
    fig.tight_layout(); save(fig,"d1_cyclus")

def f_vormen():
    fig,ax=plt.subplots(figsize=(7.2,3.5)); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.axis("off")
    ax.add_patch(Ellipse((2.3,2.6),4.0,3.9,fc=LTEAL,ec=TEAL,lw=2.5)); ax.text(2.3,3.9,"POPULATIE",ha="center",fontweight="bold",color=NAVY); ax.text(2.3,3.5,"(grootte N)",ha="center",fontsize=8.5,color=NAVY)
    rng=np.random.default_rng(3)
    for _ in range(60):
        r=1.7*np.sqrt(rng.uniform()); t=rng.uniform(0,2*np.pi); ax.plot(2.3+r*np.cos(t)*0.98,2.1+r*np.sin(t)*0.78-0.2,"o",ms=3,color=GREY,alpha=.7)
    ax.add_patch(Ellipse((7.7,2.6),2.8,2.6,fc=LORANGE,ec=ORANGE,lw=2.5)); ax.text(7.7,3.45,"STEEKPROEF",ha="center",fontweight="bold",color=NAVY); ax.text(7.7,3.1,"(grootte n)",ha="center",fontsize=8.5,color=NAVY)
    for _ in range(16):
        r=1.0*np.sqrt(rng.uniform()); t=rng.uniform(0,2*np.pi); ax.plot(7.7+r*np.cos(t)*1.05,2.2+r*np.sin(t)*0.8-0.1,"o",ms=4,color=ORANGE)
    ax.add_patch(FancyArrowPatch((4.3,3.1),(6.2,3.1),arrowstyle="-|>",mutation_scale=18,lw=2.4,color=TEAL)); ax.text(5.25,3.4,"verzamelende\nstatistiek",ha="center",fontsize=8.5,fontweight="bold",color=TEAL)
    ax.add_patch(FancyArrowPatch((6.2,1.7),(4.3,1.7),arrowstyle="-|>",mutation_scale=18,lw=2.4,color=CORAL)); ax.text(5.25,1.1,"verklarende statistiek\n(veralgemenen)",ha="center",fontsize=8.5,fontweight="bold",color=CORAL)
    ax.annotate("beschrijvende\nstatistiek",xy=(7.7,1.3),xytext=(7.7,0.35),ha="center",fontsize=8.5,fontweight="bold",color=INDIGO,arrowprops=dict(arrowstyle="-|>",color=INDIGO,lw=2))
    fig.tight_layout(); save(fig,"d1_vormen")

def scores_opvang():
    return ["Zonnetje","Regenboog","Kleurrijk","Speelhoek","Dolfijn"],[7.1,7.3,7.4,7.6,7.8]
def f_misleidend():
    nm,v=scores_opvang()
    fig,axs=plt.subplots(1,2,figsize=(8.2,3.2))
    for ax,(ymin,t) in zip(axs,[(7.0,"Grafiek A"),(0,"Grafiek B")]):
        b=ax.bar(nm,v,color=[GREY]*4+[ORANGE]); ax.set_ylim(ymin,8.0 if ymin else 10); ax.set_title(t,loc="left",fontweight="bold",fontsize=10)
        for r,val in zip(b,v): ax.text(r.get_x()+r.get_width()/2,val+(0.03 if ymin else 0.15),f"{val:.1f}".replace(".",","),ha="center",fontsize=8)
        ax.tick_params(axis="x",labelsize=7.5,rotation=20)
        if ymin: ax.set_yticks([]); ax.spines["left"].set_visible(False)
        else: ax.set_ylabel("tevredenheid (op 10)",fontsize=8.5)
    fig.tight_layout(); save(fig,"d1_misleidend")

def f_misvattingen():
    fig,axs=plt.subplots(1,3,figsize=(8.6,2.4))
    def node(ax,x,y,t,c=TEAL):
        ax.add_patch(Circle((x,y),0.33,fc="white",ec=c,lw=2.2)); ax.text(x,y,t,ha="center",va="center",fontsize=12,fontweight="bold",color=NAVY)
    def arr(ax,a,b,c=ORANGE,ls="-"):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=15,lw=2.2,color=c,ls=ls,shrinkA=0,shrinkB=0))
    for ax,t in zip(axs,["Omgekeerde oorzakelijke richting","Toevallige samenhang","Derde variabele"]):
        ax.set_xlim(0,4); ax.set_ylim(0,2.6); ax.axis("off"); ax.set_title(t,fontsize=9,fontweight="bold",color=NAVY)
    ax=axs[0]; node(ax,0.7,1.1,"x"); node(ax,3.3,1.1,"y"); arr(ax,(3.0,1.1),(1.05,1.1),CORAL); ax.text(2.0,1.45,"in werkelijkheid:\ny veroorzaakt x",ha="center",fontsize=7.5,color=CORAL)
    ax=axs[1]; node(ax,0.7,1.1,"x"); node(ax,3.3,1.1,"y"); ax.add_patch(FancyArrowPatch((1.1,1.1),(2.9,1.1),arrowstyle="<|-|>",mutation_scale=15,lw=2,color=GREY,ls=(0,(4,3)))); ax.text(2.0,1.45,"puur toeval",ha="center",fontsize=8,color=GREY)
    ax=axs[2]; node(ax,0.7,0.5,"x"); node(ax,3.3,0.5,"y"); node(ax,2.0,2.0,"z",ORANGE); arr(ax,(1.75,1.7),(0.9,0.8)); arr(ax,(2.25,1.7),(3.1,0.8)); ax.add_patch(FancyArrowPatch((1.1,0.5),(2.9,0.5),arrowstyle="<|-|>",mutation_scale=13,lw=1.6,color=GREY,ls=(0,(4,3))))
    fig.tight_layout(); save(fig,"d1_misvattingen")

def f_toets_staaf():
    yrs=["2019","2020","2021","2022","2023"]; v=[92,95,98,104,108]
    fig,ax=plt.subplots(figsize=(6.2,3.0))
    b=ax.bar(yrs,v,color=TEAL); ax.set_ylim(90,110); ax.set_ylabel("deelnemers aan het jeugdkamp")
    for r,val in zip(b,v): ax.text(r.get_x()+r.get_width()/2,val+0.4,str(val),ha="center",fontsize=9)
    ax.set_title("Het jeugdkamp groeit razendsnel!",loc="left",fontweight="bold",fontsize=10)
    fig.tight_layout(); save(fig,"d1_toets_staaf")

if __name__=="__main__":
    f_cyclus(); f_vormen(); f_misleidend(); f_misvattingen(); f_toets_staaf(); print("ok")
