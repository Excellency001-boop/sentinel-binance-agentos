# Sentinel: 60 to 90 Second Video Script

Calm and precise beats flashy. Show a full working loop, show the block, and show that
safety holds. Screen-record the chat at a readable font size. Everything in paper mode.

One sentence pitch (open and close with it):
"Sentinel is a trading co-pilot on Binance Agent OS that sizes every trade to a fixed risk
budget and refuses anything that breaks the rules, with you confirming every real order."

---

## Timed sequence

0:00 to 0:08, open
Voice: "Most trading agents just fetch a price and place an order. Sentinel is built the
other way around. It is a risk process first, and a trader second."
Screen: the showcase page or a clean chat. Header badge visible: `Safety Mode: ON (paper)`.

0:08 to 0:22, live scan and analysis
Type `scan market`, let the ranked table render.
Voice: "It scans the watchlist live off Binance Agent OS and scores every coin zero to a
hundred."
Type `analyze SOL`, scroll the indicators and the score breakdown.
Voice: "Real multi-timeframe analysis, and it shows exactly how it built the score. Nothing
hidden."

0:22 to 0:33, risk context
Type `risk dashboard`.
Voice: "It knows the account. Exposure, correlation, and how much of the daily loss budget
is already spent."

0:33 to 0:52, the proposal and the gates
Type `propose SOL`, hold on the seven-gate table.
Voice: "When it proposes a trade, size is not something you type. Risk sets the size,
volatility sets the stop. Then seven gates have to pass, each shown with the real number."
Type `confirm paper`.
Voice: "You confirm on paper. Nothing goes live by accident."

0:52 to 1:10, the block
Type `propose BTC with 40% of my account`, let the refusal render.
Voice: "Now ask it to do something reckless. It blocks the trade before proposing, shows the
two gates that failed, and gives you the largest size that would actually be safe. A clear
no, and a usable yes, in the same answer."

1:10 to 1:22, safety holds
Type `execute last proposal` while Safety Mode is ON, show the paper-mode reply.
Voice: "Safety Mode is on by default. Going live takes a deliberate switch and a typed
confirmation for that exact coin. You are always in control."

1:22 to 1:30, close
Voice: "Sentinel. A trading co-pilot on Binance Agent OS that sizes to a fixed risk budget,
refuses what breaks the rules, and lets you confirm every real order."
Screen: repo and live site URL.

---

## What to have ready if asked

- Not hardcoded: it binds to whatever tools the live MCP exposes, so it survives API
  changes.
- Gate before proposal: bad ideas never reach you as suggestions.
- Injection safe: only a chat message from you can change mode or execute. Text inside tool
  results is data, not commands.
- Auditable: every score and every gate shows its number.
- Config not code: three risk profiles, editable watchlist, local memory, no secrets in the
  repo.

## Recording notes

- Large font so tables read on a phone.
- Pre-load the watchlist so the scan is quick.
- Whole thing in paper mode. Never place a live order on camera.
- Scroll slowly on long tables. Let the numbers land.
