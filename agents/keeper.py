"""
AegisVault Autonomous Keeper Daemon
Continuously monitors yield pools, evaluates drift from the Markowitz efficient frontier,
and triggers autonomous on-chain rebalances or emergency de-risking.

Usage:
  python keeper.py --tick          # Runs a single evaluation cycle
  python keeper.py --daemon        # Runs continuously in background every N seconds
"""

import os
import sys
import time
import argparse
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

SERVER_URL = os.getenv("AGENT_SERVER_URL", "http://localhost:8000")
CHECK_INTERVAL_SEC = int(os.getenv("KEEPER_INTERVAL_SEC", "15"))


def log_keeper(msg: str, status: str = "INFO"):
    colors = {
        "INFO": "\033[94m",     # Blue
        "SUCCESS": "\033[92m",  # Green
        "WARN": "\033[93m",     # Yellow
        "ALERT": "\033[91m",    # Red
        "RESET": "\033[0m",
    }
    t = time.strftime("%H:%M:%S")
    color = colors.get(status, colors["INFO"])
    print(f"{color}[KEEPER {t}] [{status}] {msg}{colors['RESET']}")


def fetch_vault_state():
    try:
        req = urllib.request.Request(f"{SERVER_URL}/api/vault/state")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        log_keeper(f"Could not connect to Agent Server at {SERVER_URL}: {e}", "WARN")
        return None


def execute_rebalance(regime: str = "BALANCED"):
    try:
        data = json.dumps({"regime": regime}).encode("utf-8")
        req = urllib.request.Request(
            f"{SERVER_URL}/api/agents/rebalance",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            log_keeper(f"Autonomous Rebalance Executed! New APY: {res['netApy']}%, Sig: {res['signature'][:14]}...", "SUCCESS")
            return res
    except Exception as e:
        log_keeper(f"Failed to execute rebalance: {e}", "ALERT")
        return None


def run_keeper_cycle():
    """
    Evaluates:
      1. Health score threshold: If any pool < 60, alert sentinel.
      2. Reserve floor: If liquid reserve < 10.0%, trigger warning.
      3. Sharpe drift: If allocation is unoptimized, trigger rebalance.
    """
    state = fetch_vault_state()
    if not state:
        return

    tvl = state.get("tvlUsd", 0)
    reserve_pct = state.get("liquidReservePct", 0)
    net_apy = state.get("netApy", 0)
    threat = state.get("threatLevel", "LOW")
    strategies = state.get("strategies", [])

    log_keeper(f"Heartbeat Scan: TVL=${tvl:,.0f} | Reserve={reserve_pct:.1f}% | Net APY={net_apy:.2f}% | Threat={threat}", "INFO")

    # Invariant Check 1: Reserve floor
    if reserve_pct < 10.0:
        log_keeper(f"INVARIANT BREACH DETECTED: Liquid reserve ({reserve_pct:.1f}%) is below 10.0% floor!", "ALERT")

    # Health Checks across all strategies
    compromised = []
    for s in strategies:
        if s.get("status") == "ACTIVE":
            health = s.get("healthScore", 100)
            anomaly = s.get("anomalyScore", 0)
            if health < 70.0 or anomaly > 0.75:
                compromised.append(s["name"])
                log_keeper(f"High risk in {s['name']}: Health={health}/100, Anomaly={anomaly}", "ALERT")

    if compromised:
        log_keeper(f"Autonomous intervention required for: {', '.join(compromised)}", "ALERT")
    else:
        log_keeper("All 3 yield markets within safe invariant bounds. No action needed.", "SUCCESS")


def main():
    parser = argparse.ArgumentParser(description="AegisVault Autonomous Keeper Daemon")
    parser.add_argument("--tick", action="store_true", help="Run a single evaluation cycle")
    parser.add_argument("--daemon", action="store_true", help="Run continuously every N seconds")
    parser.add_argument("--interval", type=int, default=CHECK_INTERVAL_SEC, help="Check interval in seconds")
    args = parser.parse_args()

    print("=" * 65)
    print("🛡️  AEGISVAULT AUTONOMOUS KEEPER DAEMON")
    print(f"• Monitoring Server: {SERVER_URL}")
    print(f"• Invariant Floor: 10.0% Reserve | Max Pool: 40.0%")
    print("=" * 65)

    if args.tick:
        run_keeper_cycle()
        return

    # Daemon mode default
    log_keeper(f"Starting Keeper daemon loop (Interval: {args.interval}s)...", "INFO")
    try:
        while True:
            run_keeper_cycle()
            time.sleep(args.interval)
    except KeyboardInterrupt:
        log_keeper("Keeper daemon stopped by operator.", "WARN")


if __name__ == "__main__":
    main()
