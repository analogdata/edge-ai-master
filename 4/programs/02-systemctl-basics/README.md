# 02 — systemctl Basics

## Concept (Part 3 of the notes)

`systemctl` is the tool you use to interact with systemd from the terminal.

### Key Commands

| Command | What it does |
|---|---|
| `sudo systemctl daemon-reload` | Tell systemd to re-read all service files |
| `sudo systemctl start edgeai` | Start a service right now |
| `sudo systemctl stop edgeai` | Stop a running service |
| `sudo systemctl restart edgeai` | Stop then start |
| `sudo systemctl status edgeai` | Show current state and recent logs |
| `sudo systemctl enable edgeai` | Auto-start at every boot |
| `sudo systemctl disable edgeai` | Remove auto-start at boot |
| `systemctl cat edgeai` | View the service file as systemd reads it |
| `systemctl is-active edgeai` | Print `active` or `inactive` (useful in scripts) |
| `systemctl is-enabled edgeai` | Print `enabled` or `disabled` |
| `sudo systemctl reset-failed edgeai` | Clear failed state after fixing crash loop |

### start vs enable — Critical Difference

- **start** → runs the service right now
- **enable** → marks the service to automatically start on every future boot

You almost always want to do **both**. Starting without enabling means the service dies on the next reboot.

## What This Program Does

`systemctl_cheatsheet.py` is an interactive reference that prints all systemctl commands
with explanations. It also shows the correct order of operations when setting up a new service.

## How to Run

```bash
python3 systemctl_cheatsheet.py
```

> **Note:** The actual systemctl commands require a Linux system with systemd (like Raspberry Pi OS).
> This program is a reference/teaching tool — it prints the commands you need to run on your Pi.
