#!/usr/bin/env python3
"""
04 — The [Service] Section Demo

Generates and explains every field in the [Service] section of a .service file.
This is the most important section — it tells systemd exactly how to run your program.
"""

SERVICE_SECTION = """[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/edgeai
EnvironmentFile=/home/pi/edgeai/.env
ExecStartPre=/bin/bash -c 'test -f ${MODEL_PATH}'
ExecStart=/usr/bin/python3 /home/pi/edgeai/inference.py
ExecStop=/bin/kill -SIGTERM $MAINPID
Restart=always
RestartSec=5
TimeoutStopSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=edgeai"""

FIELDS = [
    ("Type=simple", "Process type",
     "Tells systemd what kind of process this is.\n"
     "  simple   → runs in foreground, keeps running (use for ALL Python scripts)\n"
     "  oneshot  → runs once and exits (setup/cleanup scripts)\n"
     "  forking  → forks into background (rare, older software)"),
    ("User=pi", "Run as this user",
     "Which Linux user account to run the script as.\n"
     "  Running as 'pi' gives access to files, camera, GPIO, I2C.\n"
     "  NEVER use User=root unless absolutely necessary.\n"
     "  A bug running as root can damage the entire OS."),
    ("WorkingDirectory=", "Set working directory",
     "Sets the current directory before running the script.\n"
     "  Equivalent to: cd /home/pi/edgeai\n"
     "  Without this, systemd starts from / and relative paths fail.\n"
     "  With this, relative paths like './models/model.tflite' work."),
    ("EnvironmentFile=", "Load env vars from file",
     "Loads environment variables from a .env file before starting.\n"
     "  Your script reads them via os.environ.get('KEY', 'default').\n"
     "  Covered in detail in program 06."),
    ("ExecStartPre=", "Pre-condition check",
     "A command to run BEFORE ExecStart. If it fails, service won't start.\n"
     "  Example: check if model file exists before starting inference.\n"
     "  ExecStartPre=/bin/bash -c 'test -f ${MODEL_PATH}'\n"
     "  If model is missing → clear error in logs, Python never starts."),
    ("ExecStart=", "The main command",
     "The command that runs your program.\n"
     "  ALWAYS use full absolute paths — never relative.\n"
     "  WRONG:  ExecStart=python3 inference.py\n"
     "  RIGHT:  ExecStart=/usr/bin/python3 /home/pi/edgeai/inference.py\n"
     "  With venv: ExecStart=/home/pi/edgeai/venv/bin/python3 /home/pi/edgeai/inference.py"),
    ("ExecStop=", "Stop command",
     "Command to run when you issue 'systemctl stop'.\n"
     "  By default systemd sends SIGTERM — usually enough.\n"
     "  $MAINPID is a special variable systemd fills with your process ID.\n"
     "  ExecStop=/bin/kill -SIGTERM $MAINPID"),
    ("Restart=always", "Auto-restart behavior",
     "Makes your service self-healing.\n"
     "  always      → restart on ANY exit (exception, crash, OOM, anything)\n"
     "  on-failure  → restart only on non-zero exit code\n"
     "  on-abnormal → restart on crash/timeout, not clean exit\n"
     "  no          → never restart (default)\n"
     "  For production Edge AI: use Restart=always"),
    ("RestartSec=5", "Restart delay",
     "Seconds to wait before restarting after exit.\n"
     "  Without this, systemd restarts immediately.\n"
     "  If script crashes in first 2 seconds, zero delay = hundreds of\n"
     "  restarts per minute (hence StartLimitBurst also exists).\n"
     "  RestartSec=5 gives 5 seconds to recover before retrying."),
    ("TimeoutStopSec=10", "Shutdown timeout",
     "How long systemd waits for clean shutdown after SIGTERM,\n"
     "  before force-killing with SIGKILL.\n"
     "  Gives your script 10 seconds to: catch signal, close camera,\n"
     "  finish writing data, exit cleanly. After 10s → force kill."),
    ("StandardOutput=journal", "stdout destination",
     "Where to send your script's stdout output.\n"
     "  journal → goes to systemd journal (read with journalctl)\n"
     "  Without this, print() and logging.info() go nowhere."),
    ("StandardError=journal", "stderr destination",
     "Where to send your script's stderr output.\n"
     "  journal → error messages and Python tracebacks go to journal.\n"
     "  Essential for debugging — you can see why your script crashed."),
    ("SyslogIdentifier=edgeai", "Log label",
     "The label that appears in journal next to every log line.\n"
     "  Without this, label defaults to 'python3' — useless when you\n"
     "  have multiple Python services. Set it to a meaningful name."),
]


def main():
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║          THE [Service] SECTION                           ║")
    print("║          The most important section!                     ║")
    print("║          Analog Data — EdgeAI Bootcamp                   ║")
    print("╚══════════════════════════════════════════════════════════╝")

    print("\n--- Complete [Service] Section ---\n")
    for line in SERVICE_SECTION.strip().split("\n"):
        print(f"  {line}")

    print("\n--- Field-by-Field Explanation ---\n")
    for field, purpose, explanation in FIELDS:
        print(f"  {field}")
        print(f"  Purpose: {purpose}")
        for line in explanation.split("\n"):
            print(f"    {line}")
        print()

    print("--- ExecStart: Absolute Paths Rule ---\n")
    print("  systemd does NOT search PATH like a terminal does.")
    print("  You must give the full path to both python3 AND your script.")
    print()
    print("  Find python3 path on your Pi:")
    print("    which python3")
    print("    # /usr/bin/python3")
    print()
    print("  With a virtual environment:")
    print("    ExecStart=/home/pi/edgeai/venv/bin/python3 /home/pi/edgeai/inference.py")


if __name__ == "__main__":
    main()
