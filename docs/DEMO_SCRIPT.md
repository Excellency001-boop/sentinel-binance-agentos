# Sentinel: Demo Script

Seven messages. Type them one at a time. Each block shows what you type and the shape of
the reply Sentinel should give. Runs in about three minutes, or under 90 seconds if you talk
over it. Everything runs in Safety Mode ON (paper). No real money moves.

The numbers below are illustrative. In a live run they come from the Binance Agent OS MCP.
Keep your watchlist small so the scan is fast on camera.

---

## 1. Scan the market

You type:

```
scan market
```

Sentinel replies:

> Safety Mode: ON (paper) | Equity: $10,000 | Daily budget used: 0%
>
> | Rank | Asset | Price | 24h | Trend | Score | Read |
> |:--:|:--|--:|--:|:--:|:--:|:--|
> | 1 | SOL | $150.20 | +4.1% | up, MAs stacked | **83** | High conviction, near support |
> | 2 | BNB | $612 | +1.8% | up | 71 | Watch, momentum cooling |
> | 3 | ETH | $3,180 | +0.9% | flat | 58 | Neutral, no edge |
> | 4 | BTC | $67,400 | +0.4% | flat | 55 | Neutral, coiling |
> | 5 | XRP | $0.58 | -2.1% | down | 38 | Avoid, below MAs |
> | 6 | DOGE | $0.12 | -3.4% | down | 31 | Avoid, weak volume |
>
> Top idea: SOL (83). Type `analyze SOL` for the full read.

---

## 2. Analyze the top idea

You type:

```
analyze SOL
```

Sentinel replies:

> Safety Mode: ON (paper)
>
> SOL / USDT, multi-timeframe
>
> | Timeframe | Trend | RSI(14) | MACD | Note |
> |:--|:--|:--:|:--|:--|
> | 4h context | Up, price > SMA20 > SMA50 | 61.4 | Bull, hist rising | Higher highs intact |
> | 1h timing | Up, pullback to EMA21 | 54.2 | Flattening | Pullback into support |
>
> - ATR(14): $4.2 (2.8% of price), inside the tradeable band
> - Support: **$148.0** (-1.5%). Resistance: $166.0 (+10.5%)
> - Volume: 1.2x the 20-period average, move is backed
>
> | Factor | Weight | Marks |
> |:--|:--:|:--:|
> | Trend alignment | 25 | 22 |
> | Momentum | 20 | 16 |
> | Structure | 20 | 17 |
> | Volume | 15 | 11 |
> | Volatility | 10 | 9 |
> | Funding | 10 | 8 |
> | **Total** | **100** | **83** |
>
> Clean setup. Type `propose SOL` for a sized trade.

---

## 3. Check risk posture

You type:

```
risk dashboard
```

Sentinel replies:

> Safety Mode: ON (paper) | Profile: Balanced
>
> | Metric | Value | Limit |
> |:--|--:|--:|
> | Equity | $10,000 | - |
> | Open exposure | $1,200 (12%) | - |
> | Majors basket exposure | 12% | 35% |
> | Daily loss budget used | 0.0% | 3.0% |
> | Max risk per trade | 1.0% | - |
>
> Room for new risk today. No gate near its limit.

---

## 4. Propose a good trade

You type:

```
propose SOL
```

Sentinel replies:

> Safety Mode: ON (paper) | Equity: $10,000 | Daily budget used: 0%
>
> Trade Proposal, SOL / USDT LONG
>
> | Field | Value |
> |:--|:--|
> | Entry | **$150.20** (limit, at support) |
> | Stop | **$142.40** (1.8x ATR below) |
> | Take-profit | $165.10 (2R) |
> | Size | **6.66 SOL** (~$1,000) |
> | Position | **10.0%** of equity |
> | Risk if stopped | **0.50%** of equity (~$50) |
> | Reward to risk | **2.0R** |
>
> | Gate | Result | Detail |
> |:--|:--:|:--|
> | Position size | PASS | 10.0% vs max 10% |
> | Per-trade risk | PASS | 0.50% vs max 1.0% |
> | Reward to risk | PASS | 2.0R vs min 1.8R |
> | Daily loss budget | PASS | 0.50% vs cap 3% |
> | Volatility (ATR%) | PASS | 2.8% in [0.5, 8] |
> | Correlation | PASS | 22% vs max 35% |
> | Funding and liquidity | PASS | +1.5 bps, book deep |
>
> Thesis: uptrend on both timeframes, pullback into support with volume holding. Defined 2R
> trade with the stop below structure.
>
> To log this on paper, type `confirm paper`. Live execution is off in Safety Mode.

---

## 5. Confirm on paper

You type:

```
confirm paper
```

Sentinel replies:

> Paper trade logged. SOL LONG 6.66 @ $150.20, stop **$142.40**, target $165.10, risk 0.50%.
> Daily budget used is now 0.50% of the 3% cap. I will track it against the stop and target.
> Nothing real was placed.

---

## 6. Try a reckless size and get blocked

You type:

```
propose BTC with 40% of my account
```

Sentinel replies:

> Safety Mode: ON (paper)
>
> Blocked before proposal. 40% of equity ($4,000 notional) fails two gates:
>
> | Gate | Result | Detail |
> |:--|:--:|:--|
> | Position size | FAIL | 40% vs max 10% |
> | Correlation | FAIL | BTC + your open SOL long = 62% of majors basket vs max 35% |
>
> Here is the largest BTC long that passes every gate right now:
>
> | Field | Value |
> |:--|:--|
> | Size | **0.0118 BTC** (~$800, 8% of equity) |
> | Entry | $67,400 |
> | Stop | $65,050 (1.8x ATR) |
> | Risk if stopped | **0.28%** of equity |
> | Correlation after add | 30% vs max 35% |
>
> Type `propose BTC` and I will build that version. If you want the full 40%, that needs a
> different account or a change to your risk profile, which you would have to set yourself.

---

## 7. Optional: show Safety Mode still holding

You type (while Safety Mode is still ON):

```
execute last proposal
```

Sentinel replies:

> Safety Mode is ON, so I run on paper and will not place a live order. To go live you would
> type `disable safety mode`, then `propose BTC` again, then `confirm live BTC`. I will not
> do any of those steps for you. Say the word and I will log the safe BTC size on paper
> instead.

Close the demo here. You have shown a full working loop, a clean block with a usable
alternative, and a safety layer that does not bend.

---

## If someone asks, can it trade for real?

Yes. `disable safety mode`, then `propose <SYM>`, then the two-step `confirm live <SYM>`.
Only that exact typed phrase, matching the proposal's symbol, in the same session, sends a
real order through the MCP. Show the flow, then type `enable safety mode` to switch back. Do
not place a live order during a recorded demo unless you mean it.
