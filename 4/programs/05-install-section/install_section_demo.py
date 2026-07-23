#!/usr/bin/env python3
"""
05 — The [Install] Section Demo

Explains the [Install] section and how systemd's boot sequence works.
Shows what 'enable' actually does behind the scenes.
"""

BOOT_SEQUENCE = [
    ("1", "BIOS/firmware", "Hardware initialization"),
    ("2", "systemd starts", "First process (PID 1) — manages everything"),
    ("3", "basic.target", "Basic system setup (filesystems, kernel modules)"),
    ("4", "sysinit.target", "System initialization (udev, SELinux)"),
    ("5", "network.target", "Network interfaces are up"),
    ("6", "multi-user.target", "Full boot complete — all services running"),
    ("7", "graphical.target", "Desktop environment (if installed)"),
]


def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          THE [Install] SECTION                           ║")
    print("║          Analog Data — EdgeAI Bootcamp                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n--- The [Install] Section ---\n")
    print("  [Install]")
    print("  WantedBy=multi-user.target")
    print()

    print("--- What WantedBy Does ---\n")
    print("  Tells systemd at which boot stage to start your service.")
    print()
    print("  multi-user.target = system is fully booted and ready.")
    print("  This is the correct target for almost every Pi application.")
    print()
    print("  This line only takes effect when you run:")
    print("    sudo systemctl enable edgeai")
    print()
    print("  Behind the scenes, 'enable' creates a symlink:")
    print("    /etc/systemd/system/multi-user.target.wants/edgeai.service")
    print("    → points to → /etc/systemd/system/edgeai.service")
    print()
    print("  When systemd reaches multi-user.target during boot,")
    print("  it sees the symlink and starts your service automatically.")

    print("\n--- Linux Boot Sequence (simplified) ---\n")
    print(f"  {'Step':<6} {'Target':<22} {'What happens'}")
    print(f"  {'-' * 6} {'-' * 22} {'-' * 40}")
    for step, target, desc in BOOT_SEQUENCE:
        marker = " ← your service starts here" if target == "multi-user.target" else ""
        print(f"  {step:<6} {target:<22} {desc}{marker}")

    print("\n--- enable vs start (recap) ---\n")
    print("  sudo systemctl start edgeai")
    print("    → starts the service RIGHT NOW")
    print("    → does NOT survive a reboot")
    print()
    print("  sudo systemctl enable edgeai")
    print("    → creates the symlink for boot-time startup")
    print("    → does NOT start the service now")
    print("    → service starts automatically on next boot")
    print()
    print("  sudo systemctl enable --now edgeai")
    print("    → does BOTH: starts now AND enables for boot")
    print("    → shortcut for: start + enable")

    print("\n--- Disabling ---\n")
    print("  sudo systemctl disable edgeai")
    print("    → removes the symlink")
    print("    → service will NOT start at next boot")
    print("    → can still be started manually with 'start'")


if __name__ == "__main__":
    main()
