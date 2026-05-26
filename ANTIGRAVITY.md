# AI Agents Trading Pipeline

This is a multi-agent trading research pipeline. Each agent lives under
`agents/` and writes its output to a datetime-named run folder under `research/`.

## Project Structure

```
agents/
  macro_agent/        → fetches FRED data → research/{run_folder}/macro_research.md
  market_data_agent/  → fetches Finnhub quotes → research/{run_folder}/market_research.md
  news_agent/         → fetches Marketaux news → research/{run_folder}/news_research.md
  analyst_agent/      → synthesizes all three → research/{run_folder}/analyst_report.md
  strategy_agent/     → converts analysis → research/{run_folder}/strategy_decision.md

research/
  2026-04-24_21-30/   → example run folder (one per pipeline run)
    macro_research.md
    market_research.md
    news_research.md
    analyst_report.md
    strategy_decision.md

venv/                 → Python virtualenv (shared across all agents)
.env                  → API keys (never commit)
requirements.txt      → httpx, python-dotenv
```

## Environment

- Always use `venv/` for Python execution.
- If `venv/` does not exist: `python3 -m venv venv && pip install -r requirements.txt`
- API keys are read from `.env` via `python-dotenv`. Never hardcode them.

## "run pipeline" command

When the user says **"run pipeline"**, execute the following steps in order:

### Step 0 — Create run folder

Before launching any agent, create the run folder and capture its path:

```bash
venv/bin/python3 -c "
from datetime import datetime
import os
folder = 'research/' + datetime.now().strftime('%Y-%m-%d_%H-%M')
os.makedirs(folder, exist_ok=True)
print(folder)
"
```

Store the printed path as `{run_folder}` (e.g., `research/2026-04-24_21-30`).
Pass `{run_folder}` explicitly to every agent in their invocation prompt.

### Step 1 — Research agents (run IN PARALLEL, they are fully independent)

Simultaneously invoke all three, passing `{run_folder}` to each:
- `macro_agent` per its `agents/macro_agent/ANTIGRAVITY.md`
- `market_data_agent` per its `agents/market_data_agent/ANTIGRAVITY.md`
- `news_agent` per its `agents/news_agent/ANTIGRAVITY.md`

Wait for all three to finish before proceeding.

**On partial failure:** if one or two research agents fail, continue with the
available data. The analyst_agent must explicitly note which research files
are missing and proceed with what it has. Do not abort the pipeline.

**On total failure (all three fail):** stop and report — there is no data to
analyze.

### Step 2 — Analyst agent

Run `analyst_agent` per its `agents/analyst_agent/ANTIGRAVITY.md`, passing `{run_folder}`.

It reads the three research files from `{run_folder}` and writes
`{run_folder}/analyst_report.md`.

**On failure:** stop the pipeline and report the error. Do not run the
strategy agent without a valid analyst report.

### Step 3 — Strategy agent

Run `strategy_agent` per its `agents/strategy_agent/ANTIGRAVITY.md`, passing `{run_folder}`.

It reads `{run_folder}/analyst_report.md` and writes
`{run_folder}/strategy_decision.md`.

**On failure:** stop and report. This is the final output of the pipeline —
a partial result here is not useful.

### Step 4 — Report completion

When the full pipeline succeeds, print a summary:
```
Pipeline complete. Run folder: {run_folder}
  ✓ macro_research.md
  ✓ market_research.md
  ✓ news_research.md
  ✓ analyst_report.md
  ✓ strategy_decision.md
```

If any Step 1 agent failed, show ✗ for its file and note it was skipped.

## Agent reference

| Agent | Input | Output | Needs Python |
|-------|-------|--------|--------------|
| macro_agent | FRED API | {run_folder}/macro_research.md | Yes |
| market_data_agent | Finnhub API | {run_folder}/market_research.md | Yes |
| news_agent | Marketaux API | {run_folder}/news_research.md | Yes |
| analyst_agent | 3 research .md files | {run_folder}/analyst_report.md | No |
| strategy_agent | analyst_report.md | {run_folder}/strategy_decision.md | No |
