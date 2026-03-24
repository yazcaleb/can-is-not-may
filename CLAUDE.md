# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

LaTeX whitepaper: "Can Is Not May: Authority Models for Governable AI Agents." Two source files, compiled via Overleaf.

## Files

- `main.tex` — Full paper (~17 pages, 10 sections + 4 appendices)
- `references.bib` — Bibliography (natbib, 28 citations with DOIs)

## Building

This paper is compiled on **Overleaf**, not locally. There is no local build system. Do not create build scripts.

To compile locally if needed: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`

## LaTeX Conventions

- Custom commands: `\May`, `\Can` (smallcaps), `\authoritymodel` (italicized)
- Colors: `darkblue` (headings), `accentteal` (links/citations), `lightgray`/`midgray` (boxes)
- Theorem environments: `definition`, `proposition` (both numbered by section)
- TikZ diagrams use `shapes.geometric`, `arrows.meta`, `positioning`, `fit`, `calc`, `backgrounds`
- Citations use `natbib` (`\citep`, `\citet`)
- Cross-references use `cleveref` (`\cref`, `\Cref`)
- Callout boxes use `tcolorbox`

## Paper Structure

The paper argues that AI agent governance requires a new primitive — authority models — distinct from capability, safety, or alignment. Section 8 connects to the Veto product. The parent repo (`../veto/` and `../veto-platform/`) contains the implementation.
