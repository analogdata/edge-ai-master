#!/usr/bin/env python3
"""
02 — systemctl Command Reference

An interactive cheatsheet that teaches all the essential systemctl commands.
Prints commands with explanations and shows the correct order of operations.

Note: The actual commands must be run on a Linux system with systemd (e.g. Raspberry Pi OS).
This script is a teaching reference — it does NOT execute systemctl commands.
"""

COMMANDS = [
    ("daemon-reload", "sudo systemctl daemon-reload",
     "Tell systemd to re-read all service files.\n"
     "   Run this AFTER creating or editing any .service file."),
    ("start", "sudo systemctl start edgeai",
     "Start the service right now.\n"
     "   The service runs in the background — no terminal needed."),
    ("stop", "sudo systemctl stop edgeai",
     "Stop a running service.\n"
     "   systemd sends SIGTERM to your script for graceful shutdown."),
    ("restart", "sudo systemctl restart edgeai",
     "Stop then start the service.\n"
     "   Use after editing your Python script or .env file."),
    ("status", "sudo systemctl status edgeai",
     "Show current state and recent log lines.\n"
     "   Look at the 'Active:' line and the log output at the bottom."),
    ("enable", "sudo systemctl enable edgeai",
     "Mark the service to auto-start at every boot.\n"
     "   Creates a symlink in multi-user.target.wants/"),
    ("disable", "sudo systemctl disable edgeai",
     "Remove auto-start at boot.\n"
     "   The service can still be started manually with 'start'."),
    ("cat", "systemctl cat edgeai",
     "View the service file exactly as systemd reads it.\n"
     "   Useful to verify your edits were loaded correctly."),
    ("is-active", "systemctl is-active edgeai",
     "Prints: active  or  inactive\n"
     "   Useful inside scripts to check service state."),
    ("is-enabled", "systemctl is-enabled edgeai",
     "Prints: enabled  or  disabled\n"
     "   Useful inside scripts to check boot-time config."),
    ("reset-failed", "sudo systemctl reset-failed edgeai",
     "Clear the 'failed' state after hitting StartLimitBurst.\n"
     "   Run this AFTER fixing the root cause of a crash loop."),
    ("list-units", "systemctl list-units --type=service --state=running",
     "Show all currently running services on the system.\n"
     "   Useful to see what else systemd is managing."),
]

SETUP_ORDER = [
    "1. Write your Python script (inference.py)",
    "2. Write your .env file with configuration",
    "3. Write your .service file in /etc/systemd/system/",
    "4. sudo systemctl daemon-reload    ← tell systemd about the new file",
    "5. sudo systemctl start edgeai     ← start it now",
    "6. sudo systemctl status edgeai    ← verify it's running",
    "7. sudo systemctl enable edgeai    ← auto-start at boot",
]


def print_separator(title):
    print()
    print("=" * 60)
    print(f" {title}")
    print("=" * 60)


def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          SYSTEMCTL COMMAND REFERENCE                     ║")
    print("║          Analog Data — EdgeAI Bootcamp                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print_separator("ALL ESSENTIAL COMMANDS")
    for name, cmd, desc in COMMANDS:
        print(f"\n  {name}")
        print(f"  $ {cmd}")
        for line in desc.split("\n"):
            print(f"     {line}")

    print_separator("CORRECT SETUP ORDER (first time)")
    for step in SETUP_ORDER:
        print(f"  {step}")

    print_separator("START vs ENABLE — THE CRITICAL DIFFERENCE")
    print("  start  → runs the service RIGHT NOW")
    print("  enable → marks it to auto-start at EVERY FUTURE BOOT")
    print()
    print("  Starting without enabling → service dies on next reboot")
    print("  Enabling without starting → service starts on next boot only")
    print("  You almost always want BOTH:")
    print()
    print("    sudo systemctl start edgeai")
    print("    sudo systemctl enable edgeai")

    print_separator("WHEN TO USE daemon-reload")
    print("  After CREATING a new .service file     → YES, daemon-reload")
    print("  After EDITING a .service file          → YES, daemon-reload")
    print("  After editing only the Python script   → NO, just restart")
    print("  After editing only the .env file       → NO, just restart")
    print()
    print("  Rule: if the .service file changed → daemon-reload")
    print("        if only .py or .env changed  → just restart")


if __name__ == "__main__":
    main()
