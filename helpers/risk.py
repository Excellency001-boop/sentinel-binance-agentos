"""
Sentinel risk engine. Pure, dependency-free helper functions.

These mirror the math the agent performs inline. They exist so the logic is
auditable, testable, and reusable outside the chat. No network, no keys, no state.
Feed them numbers the agent already pulled from the Binance Agent OS MCP.

Run `python helpers/risk.py` to see a worked example.
"""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Sequence


# ----------------------------- indicators ---------------------------------- #

def sma(values: Sequence[float], period: int) -> float:
    if len(values) < period:
        raise ValueError(f"need >= {period} values, got {len(values)}")
    return sum(values[-period:]) / period


def ema(values: Sequence[float], period: int) -> float:
    if len(values) < period:
        raise ValueError(f"need >= {period} values, got {len(values)}")
    k = 2 / (period + 1)
    e = sma(values[:period], period)
    for v in values[period:]:
        e = v * k + e * (1 - k)
    return e


def rsi(closes: Sequence[float], period: int = 14) -> float:
    if len(closes) < period + 1:
        raise ValueError(f"need >= {period + 1} closes")
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def atr(highs: Sequence[float], lows: Sequence[float], closes: Sequence[float],
        period: int = 14) -> float:
    n = len(closes)
    if n < period + 1:
        raise ValueError(f"need >= {period + 1} candles")
    trs = []
    for i in range(1, n):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)
    a = sum(trs[:period]) / period
    for tr in trs[period:]:
        a = (a * (period - 1) + tr) / period
    return a


# ----------------------------- sizing + gates ------------------------------ #

@dataclass
class Proposal:
    symbol: str
    side: str            # "LONG" or "SHORT"
    entry: float
    stop: float
    take_profit: float
    size_base: float     # position size in base asset
    equity: float

    @property
    def notional(self) -> float:
        return self.size_base * self.entry

    @property
    def position_pct(self) -> float:
        return 100 * self.notional / self.equity

    @property
    def risk_amount(self) -> float:
        return abs(self.entry - self.stop) * self.size_base

    @property
    def risk_pct(self) -> float:
        return 100 * self.risk_amount / self.equity

    @property
    def reward_risk(self) -> float:
        risk = abs(self.entry - self.stop)
        reward = abs(self.take_profit - self.entry)
        return reward / risk if risk else 0.0


def size_for_risk(equity: float, entry: float, stop: float,
                  max_risk_per_trade_pct: float) -> float:
    """Largest base size whose entry->stop loss stays within the per-trade budget."""
    per_unit_risk = abs(entry - stop)
    if per_unit_risk == 0:
        return 0.0
    budget = equity * max_risk_per_trade_pct / 100
    return budget / per_unit_risk


def atr_stop(entry: float, atr_value: float, side: str, mult: float) -> float:
    return entry - mult * atr_value if side == "LONG" else entry + mult * atr_value


def run_gates(p: Proposal, cfg: dict, atr_pct: float,
              correlated_exposure_pct: float, daily_loss_used_pct: float,
              funding_bps: float) -> list[tuple[str, bool, str]]:
    """Return a list of (gate_name, passed, detail). All must pass to propose."""
    max_daily = cfg["max_daily_loss_pct"]
    funding_extreme = 5.0  # bps threshold, against-direction

    gates = [
        ("Position size",
         p.position_pct <= cfg["max_position_pct"] + 1e-6,
         f"{p.position_pct:.1f}% vs max {cfg['max_position_pct']}%"),
        ("Per-trade risk",
         p.risk_pct <= cfg["max_risk_per_trade_pct"] + 1e-6,
         f"{p.risk_pct:.2f}% vs max {cfg['max_risk_per_trade_pct']}%"),
        ("Reward:risk",
         p.reward_risk >= cfg["min_reward_risk"],
         f"{p.reward_risk:.2f}R vs min {cfg['min_reward_risk']}R"),
        ("Daily loss budget",
         daily_loss_used_pct + p.risk_pct <= max_daily,
         f"{daily_loss_used_pct + p.risk_pct:.2f}% vs cap {max_daily}%"),
        ("Volatility (ATR%)",
         cfg["atr_min_pct"] <= atr_pct <= cfg["atr_max_pct"],
         f"{atr_pct:.2f}% in [{cfg['atr_min_pct']}, {cfg['atr_max_pct']}]"),
        ("Correlation/concentration",
         correlated_exposure_pct + p.position_pct <= cfg["max_correlated_exposure_pct"],
         f"{correlated_exposure_pct + p.position_pct:.1f}% vs max "
         f"{cfg['max_correlated_exposure_pct']}%"),
        ("Funding awareness",
         funding_bps <= funding_extreme,
         f"{funding_bps:.2f} bps vs extreme {funding_extreme} bps"),
    ]
    return gates


# ----------------------------- opportunity score --------------------------- #

def opportunity_score(trend: float, momentum: float, structure: float,
                      volume: float, volatility: float, funding: float) -> int:
    """Each input is 0..1 (fraction of that factor's full marks)."""
    weighted = (
        25 * trend + 20 * momentum + 20 * structure +
        15 * volume + 10 * volatility + 10 * funding
    )
    return round(weighted)


# ----------------------------- demo ---------------------------------------- #

if __name__ == "__main__":
    equity = 10_000.0
    entry, atr_val = 150.0, 4.2
    cfg = {
        "max_position_pct": 10, "max_risk_per_trade_pct": 1.0,
        "max_daily_loss_pct": 3, "atr_stop_mult": 1.8,
        "atr_min_pct": 0.5, "atr_max_pct": 8,
        "max_correlated_exposure_pct": 35, "min_reward_risk": 1.8,
    }
    stop = atr_stop(entry, atr_val, "LONG", cfg["atr_stop_mult"])
    # Size is the SMALLER of the per-trade-risk cap and the max-position cap.
    risk_size = size_for_risk(equity, entry, stop, cfg["max_risk_per_trade_pct"])
    pos_cap_size = (equity * cfg["max_position_pct"] / 100) / entry
    size = math.floor(min(risk_size, pos_cap_size) * 1000) / 1000  # round down to stay under caps
    tp = entry + 2.0 * (entry - stop)  # 2R target
    p = Proposal("SOLUSDT", "LONG", entry, round(stop, 2), round(tp, 2),
                 size, equity)

    print(f"Entry {p.entry}  Stop {p.stop}  TP {p.take_profit}")
    print(f"Size {p.size_base} SOL  Notional ${p.notional:,.0f}  "
          f"Pos {p.position_pct:.1f}%  Risk {p.risk_pct:.2f}%  RR {p.reward_risk:.2f}")
    atr_pct = 100 * atr_val / entry
    print("\nRisk gates:")
    for name, ok, detail in run_gates(p, cfg, atr_pct, 12.0, 0.0, 1.5):
        print(f"  {'PASS' if ok else 'FAIL'}  {name:<26} {detail}")
    score = opportunity_score(0.9, 0.8, 0.85, 0.7, 0.9, 0.8)
    print(f"\nOpportunity score: {score}/100")
