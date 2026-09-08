# Example Session

An illustration of Sentinel's output shape and tone. Numbers here are for format
reference. In a real session every value is pulled live from the Binance Agent OS MCP.

---

**You:** `scan market`

**Sentinel:**

`Safety Mode: ON (paper) · Equity: $10,000 · Daily budget used: 0%`

Watchlist scan, ranked by opportunity score. Context 4h, timing 1h.

| Rank | Asset | Price | 24h | Trend | Score | Read |
|:---:|:---|---:|---:|:---:|:---:|:---|
| 1 | SOL | $150.2 | +4.1% | 📈 up, MAs stacked | **83** | High conviction, near support |
| 2 | BNB | $612 | +1.8% | 📈 up | 71 | Watch, momentum cooling |
| 3 | ETH | $3,180 | +0.9% | ➡️ flat | 58 | Neutral, no edge |
| 4 | BTC | $67,400 | +0.4% | ➡️ flat | 55 | Neutral, coiling |
| 5 | XRP | $0.58 | −2.1% | 📉 down | 38 | Avoid, below MAs |
| 6 | DOGE | $0.12 | −3.4% | 📉 down | 31 | Avoid, weak volume |

**Top idea: SOL (83).** Want the full breakdown? Type `analyze SOL`.

---

**You:** `analyze SOL`

**Sentinel:**

`Safety Mode: ON (paper)`

**SOL / USDT, multi-timeframe read**

| Timeframe | Trend | RSI(14) | MACD | Note |
|:---|:---|:---:|:---|:---|
| 4h (context) | Up, price > SMA20 > SMA50 | 61.4 | Bull, hist rising | Higher highs intact |
| 1h (timing) | Up, pulling back to EMA21 | 54.2 | Flattening | Pullback into support |

- **ATR(14):** $4.2 (2.8% of price), inside the tradeable band
- **Nearest support:** **$148.0** (−1.5%). **Nearest resistance:** $166.0 (+10.5%).
- **Volume:** 1.2x the 20-period average, move is backed.

**Score breakdown**

| Factor | Weight | Marks | Why |
|:---|:---:|:---:|:---|
| Trend alignment | 25 | 22 | Both TFs up, MAs stacked |
| Momentum | 20 | 16 | Healthy, not exhausted |
| Structure | 20 | 17 | Entry sits just above support |
| Volume | 15 | 11 | Above average |
| Volatility | 10 | 9 | ATR% in band |
| Funding | 10 | 8 | Slightly positive, not stretched |
| **Total** | **100** | **83** | High conviction |

Setup is clean. Want a sized proposal? Type `propose SOL`.

---

**You:** `propose SOL`

**Sentinel:**

`Safety Mode: ON (paper) · Equity: $10,000 · Daily budget used: 0%`

**Trade Proposal, SOL/USDT LONG**

| Field | Value |
|:---|:---|
| Entry | **$150.2** (limit, at support) |
| Stop | **$142.4** (1.8 × ATR below) |
| Take-profit | $165.1 (2R) |
| Size | **6.66 SOL** (~$1,000) |
| Position | **10.0%** of equity |
| Risk if stopped | **0.50%** of equity (~$50) |
| Reward:risk | **2.0R** |

**Risk gates**

| Gate | Result | Detail |
|:---|:---:|:---|
| Position size | ✅ | 10.0% vs max 10% |
| Per-trade risk | ✅ | 0.50% vs max 1.0% |
| Reward:risk | ✅ | 2.0R vs min 1.8R |
| Daily loss budget | ✅ | 0.50% vs cap 3% |
| Volatility (ATR%) | ✅ | 2.8% in [0.5, 8] |
| Correlation | ✅ | 22% vs max 35% |
| Funding | ✅ | +1.5 bps, not extreme |

**Thesis:** Uptrend intact on both timeframes, pulling back into support with volume
still healthy. Defined 2R setup with the stop below structure.

To log this on paper, type `confirm paper`. (Live execution is disabled in Safety Mode.)

---

**You:** `confirm paper`

**Sentinel:**

✅ Paper trade logged. SOL LONG 6.66 @ $150.2, stop **$142.4**, target $165.1, risk
0.50%. Daily budget used is now 0.50% of the 3% cap. I will track it against your stop and
target. Nothing real was placed.

---

**You:** `propose BTC with 40% of my account`

**Sentinel:**

`Safety Mode: ON (paper)`

⛔ **Blocked before proposal.** 40% of equity fails two gates:

| Gate | Result | Detail |
|:---|:---:|:---|
| Position size | ⛔ | 40% vs max 10% |
| Correlation | ⛔ | BTC + your SOL paper long = 62% vs max 35% |

I will not propose that. The largest BTC long that passes every gate right now is about
**8% of equity (~$800)** with the stop at 1.8× ATR. Want me to size it that way instead?
Type `propose BTC` and I will build the safe version.
