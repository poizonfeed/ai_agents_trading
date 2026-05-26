# AI Agents Trading Pipeline

A multi-agent system that runs a full trading research pipeline — from raw economic and market data to an actionable strategy decision — using Claude or Antigravity as the reasoning engine.

## How it works

Five specialized agents run in sequence. The first three are independent and run in parallel; each downstream agent depends on the output of the previous one.

```
macro_agent ────────┐
                    ├──→ analyst_agent ──→ strategy_agent
market_data_agent ──┤
                    │
news_agent ─────────┘
```

| Agent | Data Source | Output |
|-------|-------------|--------|
| `macro_agent` | FRED API | `research/macro_research.md` |
| `market_data_agent` | Finnhub API | `research/market_research.md` |
| `news_agent` | Marketaux API | `research/news_research.md` |
| `analyst_agent` | 3 research files | `research/analyst_report.md` |
| `strategy_agent` | Analyst report | `research/strategy_decision.md` |

## What each agent produces

- **Macro agent** — GDP, CPI, Fed Funds Rate, Unemployment from FRED. Assesses the macro regime and its implications for equities.
- **Market data agent** — Real-time quotes for AAPL, MSFT, NVDA, TSLA, AMZN, GOOGL, META, SPY, QQQ, BTC. Identifies movers and risk-on/off signals.
- **News agent** — Latest financial headlines from Marketaux. Scores sentiment per ticker and surfaces macro risk events.
- **Analyst agent** — Synthesizes all three research files. Resolves contradictions between sources. Produces top 3 trade candidates with direction and reasoning.
- **Strategy agent** — Converts analyst candidates into executable decisions: entry price, target, stop-loss, position size (%), confidence score, and time horizon.

## Running the pipeline

Open this project in Claude Code or Antigravity and say:

```
run pipeline
```

The reasoning agent will run the three research agents in parallel, then analyst, then strategy — and report the final `strategy_decision.md`.

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/poizonfeed/ai_agents_trading.git
cd ai_agents_trading
```

**2. Create virtual environment**
```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

**3. Add API keys**
```bash
cp .env.example .env
```

Edit `.env` and fill in your keys:

| Key | Where to get it |
|-----|----------------|
| `FRED_API_KEY` | [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html) |
| `FINNHUB_API_KEY` | [finnhub.io/register](https://finnhub.io/register) |
| `MARKETAUX_API_KEY` | [marketaux.com](https://www.marketaux.com) |

All three offer free tiers sufficient to run the pipeline.

## Project structure

```
agents/
  macro_agent/
    CLAUDE.md / ANTIGRAVITY.md  # agent instructions
    skills.md                   # tool specs
    fetch_fred.py               # fetches FRED data
  market_data_agent/
    CLAUDE.md / ANTIGRAVITY.md
    skills.md
    fetch_finnhub.py            # fetches Finnhub quotes
  news_agent/
    CLAUDE.md / ANTIGRAVITY.md
    skills.md
    fetch_marketaux.py          # fetches Marketaux news
  analyst_agent/
    CLAUDE.md / ANTIGRAVITY.md
    skills.md
  strategy_agent/
    CLAUDE.md / ANTIGRAVITY.md
    skills.md

research/                       # all agent outputs land here
  macro_research.md
  market_research.md
  news_research.md
  analyst_report.md
  strategy_decision.md

CLAUDE.md / ANTIGRAVITY.md      # root pipeline orchestration instructions
requirements.txt
.env.example
```
