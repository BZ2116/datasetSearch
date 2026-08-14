# Dataset Research Project

## Directory conventions

- Root Markdown files define the long-term plan, research summary, and reusable templates.
- `daily/YYYY-MM-DD/` stores daily plans, summaries, and work items.
- `experiments/` stores experiment notes, configurations, results, and figures.
- `benchmarks/` stores benchmark descriptions and evaluation notes.
- `assets/figures/` and `assets/tables/` store reusable research assets.
- New work items use zero-padded numeric prefixes, for example `01_topic/`.
- Keep source files and reading cards together inside the corresponding work-item directory.

## Maintenance rules

- Update `daily_summary.md` after daily work.
- Update `01_research_summary.md` when research progress changes.
- Modify `00_master_plan.md` only when the long-term research route changes.
- Do not commit secrets, generated caches, or local environments.
