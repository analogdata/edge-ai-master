#!/usr/bin/env python3
"""
04b — Restart Behavior Simulator

Simulates how different Restart= values behave when a script exits
with different exit codes. Helps students understand when systemd
will or won't restart a service.
"""

import time
import random

RESTART_POLICIES = {
    "no": lambda exit_code: False,
    "always": lambda exit_code: True,
    "on-failure": lambda exit_code: exit_code != 0,
    "on-abnormal": lambda exit_code: exit_code != 0,  # simplified
}

SCENARIOS = [
    ("Normal exit (code 0)", 0),
    ("Python exception (code 1)", 1),
    ("Segfault (code 139)", 139),
    ("OOM killed (code 137)", 137),
    ("Manual stop (SIGTERM)", -15),
]


def simulate(policy_name, exit_code, restart_sec=5, max_burst=5):
    """Simulate systemd's restart decision for a given policy and exit code."""
    should_restart = RESTART_POLICIES[policy_name](exit_code)
    restarts = 0

    print(f"\n  Policy: Restart={policy_name}")
    print(f"  Exit code: {exit_code}")
    print(f"  RestartSec={restart_sec}s, StartLimitBurst={max_burst}")

    if not should_restart:
        print(f"  → systemd does NOT restart (policy says no)")
        print(f"  → Service stays dead")
        return

    print(f"  → systemd WILL restart this service")
    print(f"  → Waiting {restart_sec}s before restart...")

    while restarts < max_burst:
        restarts += 1
        print(f"  → Restart attempt {restarts}/{max_burst}")
        if restarts >= max_burst:
            print(f"  → StartLimitBurst reached! Service marked 'failed'.")
            print(f"  → Run: sudo systemctl reset-failed edgeai")
            break
        # In real life, if the crash keeps happening, we'd loop here
        break  # just show one cycle for demo


def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          RESTART BEHAVIOR SIMULATOR                      ║")
    print("║          Analog Data — EdgeAI Bootcamp                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n--- Restart= Policy Comparison ---\n")
    print(f"  {'Scenario':<30} {'no':<8} {'always':<8} {'on-fail':<8} {'on-abnrm':<8}")
    print(f"  {'-' * 30} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 8}")

    for name, code in SCENARIOS:
        results = []
        for policy in ["no", "always", "on-failure", "on-abnormal"]:
            will_restart = RESTART_POLICIES[policy](code)
            results.append("YES" if will_restart else "no")
        print(f"  {name:<30} {results[0]:<8} {results[1]:<8} {results[2]:<8} {results[3]:<8}")

    print("\n--- Detailed Simulation: Crash with Restart=always ---\n")
    simulate("always", 1, restart_sec=5, max_burst=5)

    print("\n--- Detailed Simulation: Crash with Restart=on-failure ---\n")
    simulate("on-failure", 1, restart_sec=5, max_burst=5)

    print("\n--- Detailed Simulation: Clean exit with Restart=on-failure ---\n")
    simulate("on-failure", 0, restart_sec=5, max_burst=5)

    print("\n--- Key Takeaways ---\n")
    print("  • Restart=always   → restarts on ANY exit (best for production)")
    print("  • Restart=on-failure → restarts only on errors, not clean exits")
    print("  • RestartSec=5     → 5s delay prevents crash loops from thrashing")
    print("  • StartLimitBurst  → stops trying after N crashes in a window")
    print("  • For Edge AI: always use Restart=always with RestartSec=5")


if __name__ == "__main__":
    main()
