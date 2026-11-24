"""Maakt reference.docx: alle stijlen in Verdana 10 pt, interlinie 1,5, met gekleurde kaders."""
import subprocess, copy
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY="1B2B4B"; TEAL="0E8C8C"; ORANGE="F28C28"; CORAL="D64550"; INDIGO="5B4B9A"; GREEN="3E8E41"; BLUE="2F6DB5"
FONT="Verdana"

subprocess.run("pandoc -o ref0.docx --print-default-data-file reference.docx", shell=True, check=True) if False else None
open("ref0.docx","wb").write(subprocess.check_output(["pandoc","--print-default-data-file","reference.docx"]))
doc=Document("ref0.docx")

def set_fonts(style,size=None,bold=None,italic=None,color=None):
    rpr=style.element.get_or_add_rPr()
    for el in rpr.findall(qn("w:rFonts")): rpr.remove(el)
    rf=OxmlElement("w:rFonts")
    for a in ("ascii","hAnsi","cs","eastAsia"): rf.set(qn("w:"+a),FONT)
    rpr.insert(0,rf)
    f=style.font
    if size: f.size=Pt(size)
    if bold is not None: f.bold=bold
    if italic is not None: f.italic=italic
    if color: f.color.rgb=RGBColor.from_string(color)

def spacing(style,before=0,after=6,line=1.5,keep_next=None,page_break=False):
    pf=style.paragraph_format
    pf.space_before=Pt(before); pf.space_after=Pt(after); pf.line_spacing=line
    if keep_next is not None: pf.keep_with_next=keep_next
    if page_break: pf.page_break_before=True

def borders(style,color,left=None,box=None,space=6):
    """left = dikte linkerrand (1/8 pt), box = dikte overige randen."""
    ppr=style.element.get_or_add_pPr()
    for el in ppr.findall(qn("w:pBdr")): ppr.remove(el)
    b=OxmlElement("w:pBdr")
    for side in ("top","left","bottom","right"):
        w = left if (side=="left" and left) else box
        if not w: continue
        e=OxmlElement(f"w:{side}"); e.set(qn("w:val"),"single"); e.set(qn("w:sz"),str(w)); e.set(qn("w:space"),str(space)); e.set(qn("w:color"),color); b.append(e)
    # pBdr moet voor w:shd / w:spacing / w:ind staan: voeg in op juiste plek
    insert_ppr(ppr,b)

ORDER=["pStyle","keepNext","keepLines","pageBreakBefore","framePr","widowControl","numPr","suppressLineNumbers","pBdr","shd","tabs","suppressAutoHyphens","kinsoku","wordWrap","overflowPunct","topLinePunct","autoSpaceDE","autoSpaceDN","bidi","adjustRightInd","snapToGrid","spacing","ind","contextualSpacing","mirrorIndents","suppressOverlap","jc","textDirection","textAlignment","textboxTightWrap","outlineLvl","divId","cnfStyle","rPr","sectPr","pPrChange"]
def insert_ppr(ppr,el):
    tag=el.tag.split("}")[1]
    for old in ppr.findall(el.tag): ppr.remove(old)
    idx=ORDER.index(tag)
    for i,child in enumerate(list(ppr)):
        ct=child.tag.split("}")[1]
        if ct in ORDER and ORDER.index(ct)>idx:
            child.addprevious(el); return
    ppr.append(el)

def shade(style,fill):
    ppr=style.element.get_or_add_pPr()
    s=OxmlElement("w:shd"); s.set(qn("w:val"),"clear"); s.set(qn("w:color"),"auto"); s.set(qn("w:fill"),fill)
    insert_ppr(ppr,s)

def indent(style,left=0,right=0):
    pf=style.paragraph_format; pf.left_indent=Cm(left); pf.right_indent=Cm(right)

styles=doc.styles
class _S:
    def __init__(self,real): self.real=real
    def __getitem__(self,k):
        for st in self.real:
            if st.name==k: return st
        raise KeyError(k)
    def add_style(self,*a,**k): return self.real.add_style(*a,**k)
    def __iter__(self): return iter(self.real)
styles=_S(doc.styles)
# ---- basis
for nm in ["Normal","Body Text","First Paragraph","Compact","Block Text","Table","Image Caption","Figure","Captioned Figure","Date","Author","Abstract"]:
    try: st=styles[nm]
    except KeyError: continue
    if st.type==WD_STYLE_TYPE.PARAGRAPH:
        set_fonts(st,size=10,color=NAVY if nm!="Normal" else "222B3A")
        spacing(st,before=0,after=4 if nm=="Compact" else 6,line=1.5)
    elif st.type==WD_STYLE_TYPE.TABLE:
        set_fonts(st,size=10)
styles["Normal"].font.color.rgb=RGBColor.from_string("222B3A")
for nm in ["Body Text","First Paragraph","Compact"]:
    styles[nm].font.color.rgb=RGBColor.from_string("222B3A")
styles["Body Text"].paragraph_format.space_after=Pt(6)
# verwijder lettergrootte-afhankelijke kleurthema's in headings
def heading(nm,size,color,bold=True,before=12,after=6,keep=True,page=False):
    st=styles[nm]; set_fonts(st,size=size,bold=bold,color=color); spacing(st,before,after,1.5 if size<=12 else 1.15,keep,page); return st
h1=heading("Heading 1",22,"FFFFFF",before=0,after=14,page=True)
shade(h1,NAVY); borders(h1,NAVY,left=24,box=24,space=10); indent(h1,0.35,0.35)
h2=heading("Heading 2",14,TEAL,before=16,after=6)
borders(h2,TEAL,left=None,box=None)
ppr=h2.element.get_or_add_pPr(); b=OxmlElement("w:pBdr"); e=OxmlElement("w:bottom"); e.set(qn("w:val"),"single"); e.set(qn("w:sz"),"12"); e.set(qn("w:space"),"2"); e.set(qn("w:color"),TEAL); b.append(e); insert_ppr(ppr,b)
h3=heading("Heading 3",11,NAVY,before=14,after=4)
borders(h3,ORANGE,left=36,box=None,space=6); indent(h3,0.3,0)
h4=heading("Heading 4",10,TEAL,before=8,after=2)
for n in ("Heading 5","Heading 6"):
    heading(n,10,NAVY,before=6,after=2)

# ---- eigen stijlen
def newstyle(name,base="Body Text",size=10,color="222B3A",bold=None,italic=None,fill=None,bcolor=None,left=36,box=4,l=0.4,r=0.4,before=4,after=4,line=1.5,jc=None,keep=False):
    st=styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH); st.base_style=styles[base]
    set_fonts(st,size=size,bold=bold,italic=italic,color=color); spacing(st,before,after,line,keep)
    if bcolor: borders(st,bcolor,left=left,box=box,space=6)
    if fill: shade(st,fill)
    indent(st,l,r)
    if jc is not None: st.paragraph_format.alignment=jc
    st.quick_style=True
    return st
newstyle("Theorie",l=0,r=0,before=2,after=2)
newstyle("Voorbeeld",l=0,r=0,before=2,after=2)
newstyle("LetOp",l=0,r=0,before=2,after=2)
newstyle("Doel",l=0,r=0,before=2,after=2)
newstyle("ICT",l=0,r=0,before=2,after=2)
newstyle("Oplossing",color="1F4D22",l=0,r=0,before=2,after=2)
newstyle("Missie",size=11,color=ORANGE,bold=True,italic=True,before=0,after=8,l=0,r=0)
newstyle("Antwoordlijn",color="FFFFFF",before=0,after=0,line=1.5,l=0,r=0)
ppr=styles["Antwoordlijn"].element.get_or_add_pPr(); b=OxmlElement("w:pBdr"); e=OxmlElement("w:bottom"); e.set(qn("w:val"),"dotted"); e.set(qn("w:sz"),"6"); e.set(qn("w:space"),"1"); e.set(qn("w:color"),"8A94A6"); b.append(e); insert_ppr(ppr,b)
newstyle("Voorblad Titel",size=36,color=NAVY,bold=True,before=0,after=0,line=1.15,l=0,r=0)
newstyle("Voorblad Subtitel",size=15,color=TEAL,bold=True,before=0,after=8,line=1.3,l=0,r=0)
newstyle("Banner",size=11,color="FFFFFF",bold=True,fill=NAVY,bcolor=NAVY,left=24,box=24,before=6,after=6,line=1.5)
newstyle("Afbeelding",before=4,after=8,line=1.0,l=0,r=0,jc=1)
newstyle("Midden",before=2,after=2,l=0,r=0,jc=1)
# tekenstijl voor oplossingen in tekst
cs=styles.add_style("OplossingTekst",WD_STYLE_TYPE.CHARACTER); cs.font.bold=True; cs.font.color.rgb=RGBColor.from_string("2E7D32")
cs.element.get_or_add_rPr()
set_fonts(cs,size=10,bold=True,color="2E7D32")
cs2=styles.add_style("Gat",WD_STYLE_TYPE.CHARACTER); set_fonts(cs2,size=10,bold=True,color=TEAL)
# paginamarges A4
for s in doc.sections:
    s.page_width=Cm(21); s.page_height=Cm(29.7); s.left_margin=s.right_margin=Cm(2.0); s.top_margin=Cm(2.0); s.bottom_margin=Cm(1.8)
doc.save("reference.docx")
print("reference.docx klaar")
