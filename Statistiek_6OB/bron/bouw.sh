#!/bin/bash
# Bouwt beide Word-documenten uit de LaTeX-bron (pandoc + filter + nabewerking).
set -e
cd "$(dirname "$0")"
python3 figs.py > figdata.txt
python3 maak_referentie.py
UIT=..
bouw() { # $1=versie  $2=bestandsnaam  $3=titel
  pandoc statistiek_6OB.tex -f latex -t docx --reference-doc=reference.docx --lua-filter=filter.lua -M versie=$1 --resource-path=. -o tmp_$1.docx
  python3 nabewerking.py tmp_$1.docx "$UIT/$2" "$3"
  rm -f tmp_$1.docx
}
bouw leerling Statistiek_6OB_Leerlingen.docx "Statistiek 6OB · Remediëring"
bouw docent  Statistiek_6OB_Docent_met_oplossingen.docx "Statistiek 6OB · Remediëring · Docentenversie met oplossingen"
