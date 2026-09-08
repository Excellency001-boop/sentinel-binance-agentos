# Sentinel: Architecture

## Design principles

1. **A system-prompt agent, not a script.** The entire behavior lives in `AGENT.md`.
   There is no server to run and no state machine to maintain. The logic is the reasoning
   model plus a fixed operating procedure.

2. **Capability binding, not hardcoded tool names.** At session start Sentinel enumerates
   the live MCP tools and maps them to capabilities (ticker, book, klines, funding,
   balances, positions, orders). If the server renames a tool tomorrow, Sentinel still
   works. It binds to what the endpoint actually exposes.

3. **A decision spine, walked every time.** Scan → Analyze → Score → Risk gate → Propose
   → Confirm → Execute. No stage is skippable. The gate sits before the proposal, so a
   bad idea never even reaches the human as a suggestion.

4. **Safety by construction.** Paper mode is the default and can only be left by a typed
   human phrase. Live execution needs a second typed confirmation naming the exact
   symbol. The agent treats every non-human input as untrusted data, so a malicious
   string in a tool result can never flip it live.

5. **Local memory, zero secrets in the repo.** Risk profile, watchlist, paper trades, and
   the last proposal live in small JSON files. No API keys are stored. Account access is
   brokered entirely through the authenticated Agent OS MCP sub-account.

## Data flow

```
User turn
   │
   ▼
[Startup once] enumerate MCP tools ──▶ capability map (in working memory)
   │                       load memory/ + config/ ──▶ risk profile, watchlist, state
   ▼
Command / intent
   │
   ├─ read-only path ────────────────────────────────────────────────┐
   │   ticker · 24h · order book · klines · funding · balances · pos  │
   │        │                                                         │
   │        ▼                                                         │
   │   compute indicators (SMA/EMA/RSI/MACD/ATR/S-R/volume)           │
   │        │                                                         │
   │        ▼                                                         │
   │   opportunity score 0-100 (weighted, shown as a table)           │
   │                                                                  │
   └─ action path ──▶ RISK GATES (7) ──▶ pass? ──▶ Proposal ──▶ human confirm
                              │                                         │
                              └─ fail ─▶ block + explain + safe altern. │
                                                                        ▼
                                                    paper log  OR  place order (MCP)
                                                                        │
                                                                        ▼
                                                    update memory/, restate stop+target
```

## Why the gate comes before the proposal

If you propose first and check risk second, the human has already anchored on the trade.
Putting the gate first means the only trades a human ever sees are trades that already
passed the checks. The human is never put in the position of talking themselves out of a
bad idea the agent already surfaced.

## State model

- **Working memory (session):** the tool capability map, the active proposal, current
  mode.
- **Persistent memory (`memory/session_memory.json`):** risk profile, watchlist, paper
  trade ledger, daily loss budget used, a short rolling history summary. Written after
  every material action so a fresh session resumes with context.
- **Config (`config/`):** the three risk profiles and the watchlist. Human-editable,
  version-controlled, sane defaults.

## Failure behavior

If a tool errors or returns empty, Sentinel says so and stops rather than guessing. A
missing capability degrades gracefully (for example, support and resistance are derived
from klines if there is no dedicated level tool). Stale proposals are re-analyzed, never
executed on old numbers.
