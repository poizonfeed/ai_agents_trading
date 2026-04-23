# Strategy Agent Skills

## Input File

### research/analyst_report.md
Written by the Analyst Agent. Contains:
- Overall market assessment (BULLISH / BEARISH / NEUTRAL) with justification
- Key signals table (Macro / Market Data / News)
- Top 3 trade candidates (ticker, direction, reasoning)
- Risk warning with specific price levels and invalidation conditions

Read this file in full before producing any decisions. Pay particular
attention to:
- The contradiction note (if present) — it reveals the analyst's confidence level
- The SPY stop level — use it as the session risk-off trigger
- AVOID ratings — always include them as explicit 0% decisions

## Output File

### research/strategy_decision.md
The executable output of this agent. Written after reading the analyst report.
Location is always `research/strategy_decision.md` relative to project root.

## Sizing & Pricing Guidelines

### Position sizing by confidence
| Confidence Score | Max Position Size |
|-----------------|------------------|
| 8–10 | Up to 10% of portfolio |
| 5–7 | Up to 5% of portfolio |
| 1–4 | 1–2% or AVOID |

### Deriving price targets
- **Entry price**: use the current price from the analyst report or market data report.
- **Target price**: apply a reward multiple based on confidence and time horizon:
  - Intraday: 1.5:1 reward-to-risk minimum
  - Swing: 2:1 reward-to-risk minimum
  - Hold: 3:1 reward-to-risk minimum
- **Stop-loss**: derive from the analyst report's stated key levels, or use
  a percentage-based stop if none is given:
  - High confidence (8–10): 2–3% below entry
  - Medium confidence (5–7): 1.5–2% below entry
  - Low confidence (1–4): 1% below entry (or AVOID)

### Time horizon selection
- **Intraday**: ticker near intraday high, strong momentum, no clear catalyst ahead
- **Swing**: earnings catalyst, macro event, or multi-day momentum setup
- **Hold**: macro regime aligns, fundamental thesis, low near-term risk events

## Session Risk Budget Guidelines
- Max trades open simultaneously: 3
- Max total portfolio at risk: 15%
- Hard stop on broad market: if SPY drops 1.5% from open, close all positions
- Risk-off trigger: use the SPY level explicitly named in the analyst report
