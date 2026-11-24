#!/bin/bash
# Bouwt het examen (leerlingenversie) en de verbetersleutel (docentenversie).
set -e
cd "$(dirname "$0")"
python3 figs.py > figdata.txt
python3 figs_examen.py
python3 maak_referentie.py
UIT=..
bouw() { # $1=versie  $2=bestandsnaam  $3=titel
  pandoc examen.tex -f latex -t docx --reference-doc=reference.docx --lua-filter=filter.lua -M versie=$1 --resource-path=. -o tmp3_$1.docx
  python3 nabewerking.py tmp3_$1.docx "$UIT/$2" "$3"
  rm -f tmp3_$1.docx
}
bouw leerling Examen_Statistiek_6OB.docx "Examen Statistiek 6OB · 75 minuten"
bouw docent Verbetersleutel_Examen_Statistiek_6OB.docx "Verbetersleutel · Examen Statistiek 6OB · 75 minuten"
