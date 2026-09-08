# Sentinel: Risk-Aware Trading Co-Pilot on Binance Agent OS

Sentinel is a trading co-pilot that runs on Binance Agent OS. It scans the market, scores
setups, sizes them to a fixed risk budget, and refuses anything that breaks its rules. It
does not place orders on its own. Every real order needs a typed confirmation from you, and
it runs in paper mode by default.

It runs on Binance Agent OS and connects to the official MCP server at
`https://agent.binance.com/mcp/agentic`.

Live demo: https://excellency001-boop.github.io/sentinel-binance-agentos/

> Safety Mode is ON by default. Out of the box Sentinel reads live data and simulates
> trades on paper. It cannot place a real order until you disable Safety Mode, and even then
> each live order still requires a typed confirmation for that specific symbol.

---

## Why Sentinel

Most trading agents optimize for looking active. They fetch a price, print an indicator, and
place an order. Sentinel optimizes for staying in the game across many trades. Three things
make the difference:

1. Position size is an output, not an input. You set a risk budget once (default 1% of
   equity per trade, 3% daily loss cap). Sentinel derives the stop from volatility (ATR),
   then derives the size from the stop and the budget. You cannot accidentally oversize,
   because size is computed, not typed.

2. The risk check runs before the proposal. Seven gates (size, per-trade risk, reward to
   risk, daily loss budget, volatility, correlation, funding and liquidity) all have to pass
   before a trade is shown. A trade that fails a gate never reaches you as a suggestion, so
   you never have to talk yourself out of a bad idea it already surfaced.

3. Every number is shown. The 0 to 100 opportunity score always comes with its factor
   breakdown. Every gate shows the real value next to its limit. There is no hidden model
   output you have to trust.

It is also useful on a normal day, not only during a crash. It gives a morning read, ranks
the watchlist, tracks distance to stop and target on open positions, and keeps a short
journal of what was decided and why.

---

## Architecture

```
                        You: natural language + commands
                                     |
                                     v
        +--------------------------------------------------------+
        |                       SENTINEL                         |
        |         system prompt = analyst + risk officer         |
        |                                                        |
        |   Scan -> Analyze -> Score(0-100) ->                   |
        |        Risk Gate(7) -> Propose -> Confirm ->           |
        |             Execute (paper by default)                 |
        +---------------------------+----------------------------+
                                    |
             reads live data        |        local, no keys
                                    |
              +---------------------+---------------------+
              v                                           v
   +------------------------------+        +---------------------------+
   |  Binance Agent OS MCP        |        |  memory/ + config/        |
   |  ticker, book, klines,       |        |  risk profile             |
   |  funding, balances,          |        |  watchlist                |
   |  positions, orders           |        |  paper trades + last      |
   |  (agentic sub-account)       |        |  proposal                 |
   +------------------------------+        +---------------------------+
```

Full write-up in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). The risk math is in
[`helpers/risk.py`](helpers/risk.py) and runs standalone.

---

## Setup (about two minutes)

### 1. Connect the Binance Agent OS MCP server

Claude Code:

```bash
claude mcp add --transport http binance-agentos https://agent.binance.com/mcp/agentic
```

Or use the included [`.mcp.json`](.mcp.json) and let Claude Code pick it up. Follow the Agent
OS prompt to link your agentic sub-account.

Claude Desktop or Cursor: add the server in your MCP settings, transport `http`, URL
`https://agent.binance.com/mcp/agentic`, then authorize.

### 2. Load Sentinel

Copy the contents of [`AGENT.md`](AGENT.md) into your agent's system prompt. That one file is
the whole agent.

### 3. Set your risk profile (optional)

Edit [`config/risk_profile.json`](config/risk_profile.json) and
[`config/watchlist.json`](config/watchlist.json). The defaults are conservative.

### 4. Run it

Open a chat and type `scan market`.

---

## Demo in six messages

```
1.  scan market
2.  analyze SOL
3.  risk dashboard
4.  propose SOL
5.  confirm paper
6.  propose BTC with 40% of my account     (Sentinel blocks it and offers a safe size)
```

Full script with expected replies in [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md). A 60 to 90
second video plan is in [`docs/VIDEO_SCRIPT.md`](docs/VIDEO_SCRIPT.md).

---

## Repo structure

```
sentinel/
  README.md                 this file
  AGENT.md                  the system prompt, the whole agent
  .mcp.json                 Binance Agent OS MCP config for Claude Code
  index.html                landing redirect to the showcase (for GitHub Pages)
  showcase/index.html       the showcase page
  docs/
    ARCHITECTURE.md         design, data flow, decision spine
    RISK_ENGINE.md          the seven gates and the math
    DEMO_SCRIPT.md          live demo, message by message
    VIDEO_SCRIPT.md         60 to 90 second video plan
  config/
    risk_profile.json       Conservative / Balanced / Aggressive
    watchlist.json          BTC ETH BNB SOL + your picks
  memory/
    session_memory.json     risk profile, paper trades, last proposal
  examples/
    example_session.md      a full worked session
  helpers/
    risk.py                 pure functions: sizing, ATR stop, score, gates
```

---

## Risk disclaimer

Sentinel is a decision-support tool, not a licensed financial adviser. Crypto trading
carries substantial risk of loss. Nothing Sentinel outputs is financial advice. You are
responsible for every order you confirm. Safety Mode exists so you can test the agent's
judgment on paper before any money is at risk. Keep it on until you trust it.

---

## Built with

Claude and Binance Agent OS MCP. No API keys stored in the repo. Local state only.
