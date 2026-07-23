#!/usr/bin/env python3
"""
03 — The [Unit] Section Demo

Generates and explains a complete [Unit] section of a .service file.
Shows how Description, After, StartLimitIntervalSec, and StartLimitBurst work.
"""

UNIT_SECTION = """[Unit]
Description=Edge AI Inference Service
After=network.target
StartLimitIntervalSec=60
StartLimitBurst=5"""

FIELD_EXPLANATIONS = {
    "Description": (
        "A short, human-readable name for your service.\n"
        "  Appears in: systemctl status output, journal logs\n"
        "  Good:  Description=Edge AI Inference Service\n"
        "  Bad:   Description=myapp"
    ),
    "After": (
        "Tells systemd the startup order — which milestones must be\n"
        "  reached before your service starts.\n"
        "  Your inference service needs network for MQTT/API, so:\n"
        "    After=network.target\n"
        "  You can list multiple targets:\n"
        "    After=network.target time-sync.target"
    ),
    "StartLimitIntervalSec": (
        "The time window (in seconds) for counting restart attempts.\n"
        "  Combined with StartLimitBurst, this prevents crash loops\n"
        "  from thrashing your CPU and SD card."
    ),
    "StartLimitBurst": (
        "Maximum number of restarts allowed within StartLimitIntervalSec.\n"
        "  If exceeded, systemd stops trying and marks the service as 'failed'.\n"
        "  You must fix the root cause, then run:\n"
        "    sudo systemctl reset-failed edgeai\n"
        "    sudo systemctl start edgeai"
    ),
}

AFTER_VALUES = {
    "network.target": "Network interfaces are up",
    "network-online.target": "Network is up AND internet is reachable",
    "time-sync.target": "System clock has been synchronised via NTP",
    "multi-user.target": "Full system boot is complete",
}


def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          THE [Unit] SECTION                               ║")
    print("║          Analog Data — EdgeAI Bootcamp                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n--- Complete [Unit] Section ---\n")
    for line in UNIT_SECTION.strip().split("\n"):
        print(f"  {line}")

    print("\n--- Field-by-Field Explanation ---\n")
    for field, explanation in FIELD_EXPLANATIONS.items():
        print(f"  {field}")
        for line in explanation.split("\n"):
            print(f"    {line}")
        print()

    print("--- Common After= Values ---\n")
    print(f"  {'Value':<25} {'Meaning'}")
    print(f"  {'-' * 25} {'-' * 40}")
    for value, meaning in AFTER_VALUES.items():
        print(f"  {value:<25} {meaning}")

    print("\n--- Crash Loop Protection Example ---\n")
    print("  Scenario: Your script has a bug that crashes it on startup.")
    print("  Without StartLimitBurst:")
    print("    systemd restarts it thousands of times per minute")
    print("    CPU thrashes, SD card fills with logs")
    print()
    print("  With StartLimitIntervalSec=60 and StartLimitBurst=5:")
    print("    systemd allows max 5 restarts within 60 seconds")
    print("    after that → service marked 'failed'")
    print("    you fix the bug, then:")
    print("      sudo systemctl reset-failed edgeai")
    print("      sudo systemctl start edgeai")

    print("\n--- Anatomy of a .service File (3 Sections) ---\n")
    print("  [Unit]     ← General info: description, startup order, limits")
    print("  [Service]  ← How to run: command, user, restart behavior")
    print("  [Install]  ← When to start during boot sequence")
    print()
    print("  All service files live in: /etc/systemd/system/")
    print("  File name = service name: edgeai.service → service 'edgeai'")


if __name__ == "__main__":
    main()
