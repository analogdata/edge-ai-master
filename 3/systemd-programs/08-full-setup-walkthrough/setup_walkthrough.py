#!/usr/bin/env python3
"""
08 — Full Setup Walkthrough

An interactive step-by-step guide that prints the exact commands
to set up a systemd service from scratch.

This is a teaching tool — it prints commands but does NOT execute them.
Run the commands on your Raspberry Pi.
"""

STEPS = [
    ("Step 1 — Create your project folder", [
        "mkdir -p /home/pi/edgeai/models",
    ], "Creates the project directory and a models/ subdirectory."),

    ("Step 2 — Place your Python script", [
        "# Copy your inference script:",
        "cp inference.py /home/pi/edgeai/",
        "# Place your model file:",
        "cp model.tflite /home/pi/edgeai/models/",
    ], "Your script and model file go in the project folder."),

    ("Step 3 — Create the .env file", [
        "nano /home/pi/edgeai/.env",
        "# Add your configuration (one KEY=value per line):",
        "# MODEL_PATH=/home/pi/edgeai/models/model.tflite",
        "# CAMERA_ID=0",
        "# MQTT_BROKER=192.168.1.100",
        "# API_KEY=your_secret_key_here",
    ], "Store all configuration in .env — never hardcode in source."),

    ("Step 4 — Protect the .env file", [
        "chmod 600 /home/pi/edgeai/.env",
        "# Verify: only owner can read/write",
        "ls -la /home/pi/edgeai/.env",
        "# Should show: -rw------- 1 pi pi ...",
    ], "Sets permissions so only your user can read the .env file.\n"
       "   This protects your API keys and secrets from other users on the system."),

    ("Step 5 — Add .env to .gitignore", [
        "echo '.env' >> /home/pi/edgeai/.gitignore",
    ], "Tells Git to never track the .env file.\n"
       "   Your secrets will never accidentally end up on GitHub."),

    ("Step 6 — Write the .service file", [
        "sudo nano /etc/systemd/system/edgeai.service",
        "# Paste the complete service file (see program 07)",
    ], "The service file tells systemd how to run your script.\n"
       "   All service files live in /etc/systemd/system/."),

    ("Step 7 — daemon-reload (tell systemd about the new file)", [
        "sudo systemctl daemon-reload",
    ], "REQUIRED after creating or editing any .service file.\n"
       "   Tells systemd to re-read all service files."),

    ("Step 8 — Start the service", [
        "sudo systemctl start edgeai",
    ], "Starts the service right now, in the background."),

    ("Step 9 — Check the status", [
        "sudo systemctl status edgeai",
    ], "Verify the service is running.\n"
       "   Look at the 'Active:' line — should say 'active (running)'.\n"
       "   Check the log lines at the bottom for any errors."),

    ("Step 10 — Enable auto-start at boot", [
        "sudo systemctl enable edgeai",
    ], "Marks the service to start automatically on every boot.\n"
       "   Creates a symlink in multi-user.target.wants/."),

    ("Step 11 — Watch live logs (verify everything works)", [
        "journalctl -u edgeai -f",
    ], "Streams live logs from your service.\n"
       "   Press Ctrl+C to stop watching (the service keeps running)."),
]


def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          FULL SETUP WALKTHROUGH                          ║")
    print("║          Step-by-step: script → .env → service → run     ║")
    print("║          Analog Data — EdgeAI Bootcamp                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n  Follow these steps IN ORDER the first time you set up a service.\n")
    print("  Commands below are for a Raspberry Pi running Raspberry Pi OS.\n")

    for title, commands, explanation in STEPS:
        print(f"\n{'─' * 60}")
        print(f"  {title}")
        print(f"{'─' * 60}")
        print()
        for line in explanation.split("\n"):
            print(f"  {line}")
        print()
        for cmd in commands:
            print(f"    $ {cmd}")
        print()

    print(f"{'═' * 60}")
    print("  SETUP COMPLETE!")
    print(f"{'═' * 60}")
    print()
    print("  Your service is now:")
    print("    ✓ Running in the background (no terminal needed)")
    print("    ✓ Auto-restarting if it crashes (Restart=always)")
    print("    ✓ Starting automatically at boot (enabled)")
    print("    ✓ Logging to the journal (viewable with journalctl)")
    print("    ✓ Loading config from .env (secrets protected)")
    print()
    print("  Remember the order: script → .env → service → daemon-reload → start → status → enable")


if __name__ == "__main__":
    main()
