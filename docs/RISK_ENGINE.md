# Sentinel: Risk Engine

Seven gates. All must pass before a trade is proposed. The math is in
[`helpers/risk.py`](../helpers/risk.py) so it is auditable, not a black box.

## The seven gates

| # | Gate | Rule | Why it exists |
|---|------|------|---------------|
| 1 | Position size | notional ≤ `max_position_pct` of equity | No single trade dominates the book |
| 2 | Per-trade risk | (entry−stop) × size ≤ `max_risk_per_trade_pct` of equity | Cap the loss if the stop hits |
| 3 | Reward:risk | reward/risk ≥ `min_reward_risk` | Only take asymmetric bets |
| 4 | Daily loss budget | today's used loss + this trade's max loss ≤ `max_daily_loss_pct` | Stop the bleeding on a bad day |
| 5 | Volatility (ATR%) | `atr_min_pct` ≤ ATR% ≤ `atr_max_pct` | Skip dead tape and chaos alike |
| 6 | Correlation | correlated basket exposure ≤ `max_correlated_exposure_pct` | Crypto moves together, respect it |
| 7 | Funding / liquidity | funding not extreme against direction, book depth sane for size | Do not pay to hold or trade thin |

## Position sizing

Size is driven by risk, then capped by position limit. Take the smaller of:

- **Risk-based size** = (equity × `max_risk_per_trade_pct`) ÷ (entry − stop)
- **Position-cap size** = (equity × `max_position_pct`) ÷ entry

Round the result *down* so you never breach a cap on rounding. The stop itself is set
with ATR: `stop = entry ∓ atr_stop_mult × ATR(14)`. Volatility sets the stop, the stop
sets the size. Position size is an output of risk, never an input.

## Worked example (from `helpers/risk.py`)

Balanced profile, $10,000 equity, SOL long at $150, ATR(14) = $4.2.

```
Stop   = 150 − 1.8 × 4.2 = 142.44
Size   = min( (10000 × 1%) / 7.56 ,  (10000 × 10%) / 150 ) = min(13.22, 6.67) = 6.666 SOL
TP     = 150 + 2 × (150 − 142.44) = 165.12   (2R)
Risk   = 7.56 × 6.666 = $50.4 = 0.50% of equity
```

| Gate | Result | Detail |
|------|:------:|--------|
| Position size | ✅ | 10.0% vs max 10% |
| Per-trade risk | ✅ | 0.50% vs max 1.0% |
| Reward:risk | ✅ | 2.00R vs min 1.8R |
| Daily loss budget | ✅ | 0.50% vs cap 3% |
| Volatility (ATR%) | ✅ | 2.80% in [0.5, 8] |
| Correlation | ✅ | 22.0% vs max 35% |
| Funding | ✅ | 1.5 bps vs extreme 5.0 |

All pass, so this becomes a proposal. Change the profile to Conservative and the same
trade shrinks (0.5% per-trade cap) or the score threshold (82) blocks it entirely.

## Opportunity score weights

```
score = 25·trend + 20·momentum + 20·structure + 15·volume + 10·volatility + 10·funding
```

Each factor is scored 0..1. A high score authorizes *consideration*. The gates authorize
*action*. The two are deliberately separate so a beautiful setup with bad risk still gets
blocked, and a boring setup never sneaks through on a high number alone.
