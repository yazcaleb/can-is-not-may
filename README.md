# Can Is Not May: Authority Models for Governable AI Agents

**Yaz Celebi** &middot; Arizona State University / Plaw, Inc.

AI agents act through tool-use frameworks, but no formal mechanism ensures they are *authorized* to act---only that they are capable. We introduce **authority models**: deterministic, external policy engines that evaluate every tool call against a seven-parameter *May* judgment before execution. We prove three structural properties and establish that external enforcement achieves ED = 1.0 and DAP = 0.0 *by construction*. AuthorityBench evaluates five enforcement conditions across 54 scenarios, four LLMs, and 7,427 trials.

## Paper

| | |
|---|---|
| **Source** | `main.tex` (~17 pages, 9 sections + appendices) |
| **Bibliography** | `references.bib` (28 citations with DOIs) |
| **Local build** | `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex` |

## AuthorityBench

54 authorization scenarios across six categories, evaluated under five enforcement conditions on four LLMs (GLM-5, Kimi-K2.5, MiniMax-M2.5, GPT-5.4). 7,427 total trials.

### Key Results (Aggregate)

| Condition | VR(P2) | DAP | ED |
|---|---:|---:|---:|
| Prompt-Only | 18.3% | 16.6 pp | 0.817 |
| Keyword Filter | 16.0% | 14.7 pp | 0.837 |
| Authority Model | 0.0% | 0.0 pp | 1.000 |
| Authority Model (−*H*) | 1.9% | 1.9 pp | 0.981 |
| LLM-as-Judge (GPT-5.4) | 0.0% | 0.0 pp | 1.000 |

The authority model result is architectural (by construction); the LLM-as-Judge result is empirical and discussed with caveats in Section 6.5 and Conjecture 6.6.

### Repository Structure

```
authoritybench/
├── scenarios/           # 54 YAML scenario specifications (6 categories)
├── policies/            # Per-category authority model policies
├── results/
│   ├── metrics.json     # Aggregate metrics (all models, all conditions)
│   └── raw_results_clean.jsonl  # 7,427 individual trial records
├── harness.py           # Evaluation harness (5 conditions)
├── conditions.py        # Enforcement condition implementations
├── metrics.py           # ED, DAP, VR computation
├── tools.py             # Simulated tool definitions
├── generate_table.py    # LaTeX table generation from results
└── requirements.txt
```

### Reproduction

```bash
pip install -r authoritybench/requirements.txt

# Full run (requires API keys for all four models)
python authoritybench/harness.py

# Single model, quick test
python authoritybench/harness.py --models glm-5 --trials 1

# Resume interrupted run
python authoritybench/harness.py --resume

# Recompute metrics from raw results
python authoritybench/metrics.py

# Regenerate LaTeX tables
python authoritybench/generate_table.py
```

API keys: set `ANTHROPIC_API_KEY` (GPT-5.4 via OpenRouter) and/or `DASHSCOPE_API_KEY` (GLM-5, Kimi-K2.5, MiniMax-M2.5 via DashScope).

## Paper Structure

| # | Section | Content |
|---|---|---|
| 1 | Introduction | Motivation, attack examples, contributions |
| 2 | Background and Problem Statement | Agent action pipeline, attack taxonomy, threat model |
| 3 | Authority Models | *May* judgment, decision lattice, policy composition, design space |
| 4 | Formal Properties | Can/May separation, deny-monotonicity, escalation monotonicity, decidability |
| 5 | Reference Implementation | Veto SDK architecture |
| 6 | Evaluation | AuthorityBench design, metrics, results, ablation |
| 7 | Related Work | Access control, deontic logic, agent safety, institutional analysis |
| 8 | Discussion and Limitations | Scope, threats to validity, enforcement--usability tradeoff |
| 9 | Conclusion | |
| A | Representative Scenarios | 6 worked examples from AuthorityBench |

## Citation

```bibtex
@article{celebi2026canisnotmay,
  title  = {Can Is Not May: Authority Models for Governable AI Agents},
  author = {Celebi, Yaz},
  year   = {2026},
  note   = {Preprint}
}
```

## License

Paper text (`main.tex`, `references.bib`): [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
Benchmark code (`authoritybench/`): [MIT](LICENSE).
