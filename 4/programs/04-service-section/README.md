# 04 — The [Service] Section

## Concept (Part 6 of the notes)

The `[Service]` section is the most important part of a `.service` file. It tells systemd
exactly how to run your program.

```ini
[Service]
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
SyslogIdentifier=edgeai
```

### Fields Explained

| Field | Purpose |
|---|---|
| `Type=simple` | Process type — runs in foreground. Use for all Python scripts |
| `User=pi` | Run as this user account (never root unless necessary) |
| `WorkingDirectory=` | Sets `cd` before running the script |
| `EnvironmentFile=` | Load env vars from a `.env` file |
| `ExecStartPre=` | Pre-condition check — if it fails, service won't start |
| `ExecStart=` | The command to run your program (always absolute paths!) |
| `ExecStop=` | Command to run on stop (default: SIGTERM) |
| `Restart=always` | Auto-restart on any exit (self-healing) |
| `RestartSec=5` | Wait 5 seconds before restarting |
| `TimeoutStopSec=10` | Wait 10s for clean shutdown, then force-kill |
| `StandardOutput=journal` | Send stdout to systemd journal |
| `StandardError=journal` | Send stderr to systemd journal |
| `SyslogIdentifier=` | Label in log output (defaults to process name) |

### Restart Values

| Value | Behaviour |
|---|---|
| `no` | Never restart (default) |
| `always` | Always restart, no matter why it stopped |
| `on-failure` | Restart only on non-zero exit code |
| `on-abnormal` | Restart on crash/timeout, not on clean exit |

### Type Values

| Type | When to use |
|---|---|
| `simple` | Program runs in foreground and keeps running (all Python scripts) |
| `oneshot` | Program runs once and exits (setup/cleanup scripts) |
| `forking` | Program forks into background (rare, older software) |

## What This Program Does

`service_section_demo.py` generates and explains every field in the [Service] section.
`restart_behavior_demo.py` simulates different Restart= behaviors.

## How to Run

```bash
python3 service_section_demo.py
python3 restart_behavior_demo.py
```
