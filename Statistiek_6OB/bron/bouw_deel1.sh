#!/bin/bash
# Bouwt de bundel 'Statistiek 6OB - deel 1: Basisbegrippen' (leerlingen- en docentenversie).
set -e
cd "$(dirname "$0")"
python3 figs.py > figdata.txt
python3 figs_deel1.py
python3 maak_referentie.py
UIT=..
bouw() { # $1=versie  $2=bestandsnaam  $3=titel
  pandoc deel1.tex -f latex -t docx --reference-doc=reference.docx --lua-filter=filter.lua -M versie=$1 --resource-path=. -o tmp1_$1.docx
  python3 nabewerking.py tmp1_$1.docx "$UIT/$2" "$3"
  rm -f tmp1_$1.docx
}
bouw leerling Statistiek_6OB_Deel1_Leerlingen.docx "Statistiek 6OB · Deel 1: Basisbegrippen · Remediëring"
bouw docent Statistiek_6OB_Deel1_Docent_met_oplossingen.docx "Statistiek 6OB · Deel 1: Basisbegrippen · Docentenversie met oplossingen"
