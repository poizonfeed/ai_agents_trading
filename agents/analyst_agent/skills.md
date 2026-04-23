# Analyst Agent Skills

## Input Files

This agent reads three upstream research files before writing its report.
All paths are relative to the project root.

### research/macro_research.md
Written by the Macro Agent. Contains:
- Overall macro regime assessment
- Key indicators table (GDP, CPI, Fed Funds Rate, Unemployment)
- Market implications of the macro environment
- Macro risk factors

### research/market_research.md
Written by the Market Data Agent. Contains:
- Market overview and risk-on/risk-off read
- Ticker snapshot table with price, change %, high, low
- Sector & index signals (SPY/QQQ relationship)
- Notable movers
- Trading signals summary

### research/news_research.md
Written by the News Agent. Contains:
- Overall news sentiment (BULLISH / BEARISH / NEUTRAL)
- Top stories with ticker tags and sentiment scores
- Ticker-level sentiment table
- Macro news signals
- Risk events ahead

## Output File

### research/analyst_report.md
The synthesized output of this agent. Written after reading all three
input files. Location is always `research/analyst_report.md` relative
to the project root.

## Synthesis Guidelines

- **Confluence = conviction**: when macro, market data, and news all point
  the same direction for a ticker, that is a high-conviction trade candidate.
- **Divergence = risk**: when sources contradict, flag the tension explicitly
  and reduce conviction — do not paper over disagreements.
- **Recency weighting**: market data reflects today's price action; weight it
  highest for short-term trade candidates. Macro sets the regime context.
  News can override both if a major catalyst is present.
- **Index signals first**: always read SPY/QQQ direction before picking
  individual tickers — do not recommend longs in a confirmed risk-off tape.
