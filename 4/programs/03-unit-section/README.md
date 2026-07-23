# 03 — The [Unit] Section

## Concept (Parts 4 & 5 of the notes)

A `.service` unit file has three sections. This program focuses on the **[Unit]** section:

```ini
[Unit]
Description=Edge AI Inference Service
After=network.target
StartLimitIntervalSec=60
StartLimitBurst=5
```

### Fields Explained

| Field | Purpose |
|---|---|
| `Description=` | Human-readable name shown in `systemctl status` and logs |
| `After=` | Startup order — which milestones must be reached first |
| `StartLimitIntervalSec=` | Time window for counting restart attempts |
| `StartLimitBurst=` | Max restarts within that window before systemd gives up |

### Common `After=` Values

| Value | Meaning |
|---|---|
| `network.target` | Network interfaces are up |
| `network-online.target` | Network is up AND internet is reachable |
| `time-sync.target` | System clock synchronised via NTP |
| `multi-user.target` | Full system boot is complete |

You can list multiple: `After=network.target time-sync.target`

### StartLimitBurst Protection

If your script has a bug that crashes it immediately, `Restart=always` would restart it
thousands of times per minute. `StartLimitBurst=5` within `StartLimitIntervalSec=60` means:
**"If the service crashes and restarts more than 5 times in 60 seconds, stop trying."**

When the limit is hit, `systemctl status` shows `failed`. You must fix the root cause and run:
```bash
sudo systemctl reset-failed edgeai
sudo systemctl start edgeai
```

## What This Program Does

`unit_section_demo.py` generates and explains a complete [Unit] section, showing how each
field affects service behavior.

## How to Run

```bash
python3 unit_section_demo.py
```
