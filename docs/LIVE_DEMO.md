# Sentinel: Live Demo Runbook

Fastest path to a recorded, working demo. Follow top to bottom.

---

## A. Connect the Binance Agent OS MCP

Fastest client is Claude Code (CLI). Pick your client.

### Claude Code (recommended, fastest)

1. Add the server:

```bash
claude mcp add --transport http binance-agentos https://agent.binance.com/mcp/agentic
```

2. Authorize:

```bash
claude
```

Then inside the session run:

```
/mcp
```

Select `binance-agentos`, choose Authenticate. A browser opens on agent.binance.com.
Log in to Binance and approve. It links (or creates) your agentic sub-account.

3. Confirm it is connected:

```bash
claude mcp list
```

You want `binance-agentos` shown as connected.

### Claude Desktop

1. Settings (bottom left) -> Connectors -> Add custom connector.
2. Name: `binance-agentos`. URL: `https://agent.binance.com/mcp/agentic`. Save.
3. Click Connect / Authorize on the connector. Approve in the Binance browser page.
4. Fully quit and reopen Claude Desktop so the tools load.

### Cursor

1. Settings -> MCP -> Add new MCP server (or edit `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "binance-agentos": {
      "url": "https://agent.binance.com/mcp/agentic"
    }
  }
}
```

2. Reload. When prompted, authorize in the Binance page.

### What success looks like

- The client lists the `binance-agentos` tools (ticker, klines, balances, positions, and so on).
- A simple prompt like "list the tools you have from binance-agentos" returns a real list.
- "get the current BTCUSDT price" returns a live number.

### If auth fails or no tools appear

- Re-run `/mcp` and Authenticate again. First attempts sometimes drop.
- Make sure you are logged in to Binance in the same browser before authorizing.
- Check the URL is exactly `https://agent.binance.com/mcp/agentic` with no trailing space.
- Binance is geo-restricted. If the auth page errors on region, you will not be able to
  connect from that location. Go straight to the Fallback in section D.
- Remove and re-add:

```bash
claude mcp remove binance-agentos
claude mcp add --transport http binance-agentos https://agent.binance.com/mcp/agentic
```

- Restart the client fully (quit, not just close the window).
- If `claude mcp list` shows it connected but no tools respond, the sub-account is not
  authorized yet. Re-run the Authenticate step.
- Do not burn more than 15 minutes here. If it is not up, record the Fallback demo and move on.

---

## B. Load AGENT.md

The whole agent is the contents of `AGENT.md`. Paste it as the system prompt.

- Claude Code: create a `CLAUDE.md` in your project folder and paste `AGENT.md` into it,
  or start `claude` with `--append-system-prompt "$(cat AGENT.md)"`. The `CLAUDE.md` route
  is simplest: put the file in the folder, open `claude` there.
- Claude Desktop: create a Project, open Project settings, paste `AGENT.md` into the
  custom instructions box. Chat inside that Project.
- Cursor: paste `AGENT.md` into a `.cursorrules` file at the repo root, or into the system
  prompt field of your chat.

First reply should be the one-line status: `Sentinel online. Safety Mode: ON (paper)...`.

---

## C. The 7-message demo (type these live while recording)

Everything runs in Safety Mode ON. Nothing real is placed.

1. Type: `scan market`
   Expect: a ranked table of your watchlist with a 0-100 score per coin, and a named top
   idea.

2. Type: `analyze SOL` (use whatever ranked first)
   Expect: a multi-timeframe read (4h and 1h), indicator values (RSI, MACD, ATR, support
   and resistance), and a score breakdown table totaling the score.

3. Type: `risk dashboard`
   Expect: equity, open exposure, majors-basket exposure, and daily loss budget used vs
   the cap.

4. Type: `propose SOL`
   Expect: a Trade Proposal with entry, ATR stop, take-profit, size in coin and dollars,
   risk as a percent of equity, reward to risk, and a seven-row gate table all showing
   PASS. It ends by telling you to type `confirm paper`.

5. Type: `confirm paper`
   Expect: a short confirmation that the paper trade is logged, with the stop and target
   restated and daily budget updated. Nothing real placed.

6. Type: `propose BTC with 40% of my account`
   Expect: a clear block before any proposal, the two gates that fail (position size and
   correlation) with the real numbers, and the largest BTC size that would pass instead.

7. Type: `execute last proposal`
   Expect: it explains Safety Mode is on, that going live needs `disable safety mode` then
   a typed `confirm live BTC`, and that it will not do either on its own.

Keep the font large. Scroll slowly. Total time about two to three minutes.

---

## D. Fallback if the MCP will not connect

You still have a strong, honest demo. Do not fake live data.

### Fallback 1 (best): record the interactive page

The showcase page has a working, clickable demo that needs no connection.

- Open https://excellency001-boop.github.io/sentinel-binance-agentos/
- Scroll to "Run Sentinel right here".
- Click "Run full demo", or click the command chips one at a time.
- Screen-record that. It plays the full flow: scan, analyze, propose with seven gates,
  the reckless block, and Safety Mode holding.

What to say on camera:
> "This is Sentinel running its decision flow. It scans, scores, sizes to a fixed risk
> budget, and blocks trades that break the rules. The agent is defined in a single system
> prompt, AGENT.md, and connects to the Binance Agent OS MCP for live data. Here I am
> walking through the flow so you can see every step and every risk gate."

Then show the repo and `AGENT.md` on screen for a few seconds as proof of the real
implementation. This is legitimate: you are demonstrating the agent's logic and showing
the code. You are not claiming fake numbers are live.

### Fallback 2: run AGENT.md in Claude with no MCP

Open a chat with `AGENT.md` loaded but no MCP connected. Ask it to walk through its own
process and risk gates on an example. It will explain the flow. Say clearly on camera that
this is the reasoning layer and that live data comes from the Agent OS MCP once connected.
Keep any numbers labeled as illustrative.

Do not present illustrative numbers as live market data.

---

## E. Final checklist before you hit record

- The status line shows `Safety Mode: ON (paper)`.
- `scan market` returns a real ranked table (live path) or the page console is loaded
  (fallback path).
- The `propose SOL` reply shows the full seven-gate table, all PASS.
- The `propose BTC with 40%` reply clearly blocks and shows the failing gates plus a safe
  size.
- Font size is large enough to read on a phone.
- You know your first and last sentence: a one-line pitch at the open and the close.
