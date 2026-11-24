# Statistiek 6OB – remediëringsbundel

- `Statistiek_6OB_Leerlingen.docx` – bundel voor de leerlingen (Verdana 10 pt, interlinie 1,5)
- `Statistiek_6OB_Docent_met_oplossingen.docx` – dezelfde bundel mét oplossingen (groene kaders)
- `bron/` – LaTeX-bron (`statistiek_6OB.tex`, `level0–7.tex`, `toets.tex`, …), figuren (`figs.py`), Word-stijlen en bouwscript

Opnieuw bouwen (vereist pandoc, python-docx, matplotlib, scipy):

    bash bron/bouw.sh

## Deel 1 – Basisbegrippen (hoofdstuk 1: steekproef, misleidingen, causaliteit)

- `Statistiek_6OB_Deel1_Leerlingen.docx` en `Statistiek_6OB_Deel1_Docent_met_oplossingen.docx`
- Bron: `bron/deel1.tex` met `d1_*.tex`; bouwen met `bash bron/bouw_deel1.sh`

## Examen (75 minuten, beide hoofdstukken)

- `Examen_Statistiek_6OB.docx` (40 punten) en `Verbetersleutel_Examen_Statistiek_6OB.docx`
- Bron: `bron/examen.tex`; bouwen met `bash bron/bouw_examen.sh`
