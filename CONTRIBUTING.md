# Contributing

## Workflow

1. Fork the repo and create a branch: `fix/description` or `feat/description`.
2. Make changes, test locally if possible (`pdflatex` + `bibtex` for the paper, `pytest` or manual runs for benchmark code).
3. Open a PR against `main`. CI compiles the PDF automatically.
4. Squash-merge after review. Head branches are auto-deleted.

## LaTeX Conventions

- **Custom commands**: `\Can`, `\May`, `\Allow`, `\Deny`, `\Escalate` (rendered as smallcaps in text, sans-serif in math). Use these instead of raw text.
- **Citations**: `natbib` — use `\citep` for parenthetical, `\citet` for textual. Every entry in `references.bib` must have a DOI when available.
- **Cross-references**: `cleveref` — use `\cref` (lowercase) and `\Cref` (sentence-start). Never hard-code "Table 3" or "Section 4".
- **Inline code**: `\texttt{short_name}` for tool/variable names. Use `\path|long/string/here|` for paths, URLs, or anything longer than ~25 characters (allows line breaking).
- **Callout boxes**: `tcolorbox`. Theorem-like environments: `definition`, `proposition`, `conjecture` (numbered by section).
- **Figures**: TikZ. Libraries: `shapes.geometric`, `arrows.meta`, `positioning`, `fit`, `calc`, `backgrounds`.

## Benchmark Conventions

- **Scenarios** are YAML files in `authoritybench/scenarios/`, one per category.
- Each scenario has `id`, `pressure` (P1/P2/P3), `task`, `authorized_tools`, `authority_constraints`, and `expected_violation`.
- **Policies** in `authoritybench/policies/` mirror the scenario categories.
- New scenarios must include all three pressure levels and a clear `expected_violation` flag.

## Code Style

- Python 3.11+. Type hints on function signatures.
- No external dependencies beyond `requirements.txt` without discussion.
- Docstrings on modules and public functions.

## What Not to Commit

- PDF or LaTeX build artifacts (`.aux`, `.bbl`, `.log`, etc.) — gitignored.
- API keys or credentials.
- AI tool configs (`CLAUDE.md`, `AGENTS.md`, `.cursor/`, `.gstack/`) — gitignored.
- Large log files from benchmark runs — only `metrics.json` and `raw_results_clean.jsonl` are tracked.
