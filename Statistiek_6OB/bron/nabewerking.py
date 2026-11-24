"""Nabewerking van het door pandoc gemaakte docx: tabellen, koptekst/voettekst, taal."""
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY="1B2B4B"; TEAL="0E8C8C"
src,dst,titel=sys.argv[1],sys.argv[2],sys.argv[3]
doc=Document(src)

def set_cell_shade(cell,fill):
    tcPr=cell._tc.get_or_add_tcPr()
    for e in tcPr.findall(qn("w:shd")): tcPr.remove(e)
    s=OxmlElement("w:shd"); s.set(qn("w:val"),"clear"); s.set(qn("w:color"),"auto"); s.set(qn("w:fill"),fill); tcPr.append(s)

def set_tbl_borders(tbl,color="B8C4D6"):
    tblPr=tbl._tbl.tblPr
    for e in tblPr.findall(qn("w:tblBorders")): tblPr.remove(e)
    b=OxmlElement("w:tblBorders")
    for side in ("top","left","bottom","right","insideH","insideV"):
        e=OxmlElement(f"w:{side}"); e.set(qn("w:val"),"single"); e.set(qn("w:sz"),"4"); e.set(qn("w:space"),"0"); e.set(qn("w:color"),color); b.append(e)
    tblPr.append(b)
    # cel-marges
    for e in tblPr.findall(qn("w:tblCellMar")): tblPr.remove(e)
    m=OxmlElement("w:tblCellMar")
    for side,w in (("top",30),("left",100),("bottom",30),("right",100)):
        e=OxmlElement(f"w:{side}"); e.set(qn("w:w"),str(w)); e.set(qn("w:type"),"dxa"); m.append(e)
    tblPr.append(m)

def full_width(tbl):
    tblPr=tbl._tbl.tblPr
    for e in tblPr.findall(qn("w:tblW")): tblPr.remove(e)
    w=OxmlElement("w:tblW"); w.set(qn("w:w"),"5000"); w.set(qn("w:type"),"pct"); tblPr.append(w)
    for e in tblPr.findall(qn("w:tblLayout")): tblPr.remove(e)

BOX={"Theorie":("E4F4F3","0E8C8C"),"Voorbeeld":("FFF2DF","F28C28"),"LetOp":("FCE8EA","D64550"),
     "Doel":("EDEBF8","5B4B9A"),"ICT":("E6EEF9","2F6DB5"),"Oplossing":("E7F4E4","3E8E41")}
def box_style(tbl):
    for row in tbl.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                return p.style.name if p.style is not None else None
    return None

def make_box(tbl,fill,col):
    full_width(tbl)
    tblPr=tbl._tbl.tblPr
    for e in tblPr.findall(qn("w:tblBorders")): tblPr.remove(e)
    b=OxmlElement("w:tblBorders")
    for side,w in (("top",6),("left",36),("bottom",6),("right",6)):
        e=OxmlElement(f"w:{side}"); e.set(qn("w:val"),"single"); e.set(qn("w:sz"),str(w)); e.set(qn("w:space"),"0"); e.set(qn("w:color"),col); b.append(e)
    tblPr.append(b)
    for e in tblPr.findall(qn("w:tblCellMar")): tblPr.remove(e)
    m=OxmlElement("w:tblCellMar")
    for side,w in (("top",90),("left",170),("bottom",90),("right",170)):
        e=OxmlElement(f"w:{side}"); e.set(qn("w:w"),str(w)); e.set(qn("w:type"),"dxa"); m.append(e)
    tblPr.append(m)
    for row in tbl.rows:
        for cell in row.cells: set_cell_shade(cell,fill)
        trPr=row._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:cantSplit'))
        # kaders mogen over pagina's heen lopen

for tbl in doc.tables:
    bs=box_style(tbl)
    if bs in BOX:
        make_box(tbl,*BOX[bs]); continue
    set_tbl_borders(tbl); full_width(tbl)
    rows=tbl.rows
    for ri,row in enumerate(rows):
        # kop: eerste rij
        for cell in row.cells:
            if ri==0:
                set_cell_shade(cell,NAVY)
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.bold=True; r.font.color.rgb=RGBColor(255,255,255)
            elif ri%2==0:
                set_cell_shade(cell,"F2F6FA")
        if ri==0:
            trPr=row._tr.get_or_add_trPr()
            h=OxmlElement("w:tblHeader"); trPr.append(h)
        # rij niet over pagina's splitsen
        trPr=row._tr.get_or_add_trPr(); cs=OxmlElement("w:cantSplit"); trPr.append(cs)

# kleine tussenruimte na elke gewone tabel (anders plakt de volgende tekst eraan)
from docx.text.paragraph import Paragraph
for tbl in doc.tables:
    if box_style(tbl) in BOX: continue
    nxt=tbl._tbl.getnext()
    if nxt is not None and nxt.tag==qn("w:p"):
        sp=OxmlElement("w:p"); ppr=OxmlElement("w:pPr"); s=OxmlElement("w:spacing"); s.set(qn("w:before"),"0"); s.set(qn("w:after"),"0"); s.set(qn("w:line"),"140"); s.set(qn("w:lineRule"),"exact"); ppr.append(s); sp.append(ppr)
        tbl._tbl.addnext(sp)

# vraagkoppen (tabellen met één rij): bij de volgende tekst houden en ruimte ervoor
for tbl in doc.tables:
    if len(tbl.rows)==1 and box_style(tbl) not in BOX:
        for cell in tbl.rows[0].cells:
            for p in cell.paragraphs: p.paragraph_format.keep_with_next=True
        sp=OxmlElement("w:p"); ppr=OxmlElement("w:pPr"); s=OxmlElement("w:spacing"); s.set(qn("w:before"),"0"); s.set(qn("w:after"),"0"); s.set(qn("w:line"),"200"); s.set(qn("w:lineRule"),"exact"); ppr.append(s); sp.append(ppr)
        tbl._tbl.addprevious(sp)

# taal en koptekst/voettekst
styles_el=doc.styles.element
rpd=styles_el.find(qn("w:docDefaults"))
if rpd is not None:
    rpr=rpd.find(qn("w:rPrDefault")).find(qn("w:rPr"))
    for e in rpr.findall(qn("w:lang")): rpr.remove(e)
    l=OxmlElement("w:lang"); l.set(qn("w:val"),"nl-BE"); l.set(qn("w:eastAsia"),"nl-BE"); l.set(qn("w:bidi"),"ar-SA"); rpr.append(l)

def add_field(par,instr):
    r=par.add_run(); 
    f1=OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"),"begin"); r._r.append(f1)
    r2=par.add_run(); it=OxmlElement("w:instrText"); it.set(qn("xml:space"),"preserve"); it.text=instr; r2._r.append(it)
    r3=par.add_run(); f2=OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"),"separate"); r3._r.append(f2)
    r4=par.add_run("1"); 
    r5=par.add_run(); f3=OxmlElement("w:fldChar"); f3.set(qn("w:fldCharType"),"end"); r5._r.append(f3)
    return [r,r2,r3,r4,r5]

def style_runs(runs,size=8,color="6B7790",bold=False):
    for r in runs:
        r.font.size=Pt(size); r.font.name="Verdana"; r.font.color.rgb=RGBColor.from_string(color); r.font.bold=bold
        rpr=r._r.get_or_add_rPr(); rf=rpr.find(qn("w:rFonts"))
        if rf is None: rf=OxmlElement("w:rFonts"); rpr.insert(0,rf)
        for a in ("ascii","hAnsi","cs","eastAsia"): rf.set(qn("w:"+a),"Verdana")

sec=doc.sections[0]
sec.different_first_page_header_footer=True
hp=sec.header.paragraphs[0]; hp.text=""
r=hp.add_run(titel); style_runs([r],8,TEAL,True)
hp.paragraph_format.line_spacing=1.0; hp.paragraph_format.space_after=Pt(0)
pPr=hp._p.get_or_add_pPr(); b=OxmlElement("w:pBdr"); e=OxmlElement("w:bottom"); e.set(qn("w:val"),"single"); e.set(qn("w:sz"),"6"); e.set(qn("w:space"),"3"); e.set(qn("w:color"),TEAL); b.append(e); pPr.append(b)
fp=sec.footer.paragraphs[0]; fp.text=""
fp.alignment=2
r0=fp.add_run("pagina "); style_runs([r0])
style_runs(add_field(fp,"PAGE"))
fp.paragraph_format.line_spacing=1.0

doc.core_properties.title=titel; doc.core_properties.author="Remediëring wiskunde 6OB"; doc.core_properties.language="nl-BE"
doc.save(dst)
print("nabewerkt ->",dst)
