# 09 — journalctl: Viewing and Filtering Logs

## Concept (Part 12 of the notes)

`journalctl` is the tool for reading logs that systemd collects from your services.
Since our `.service` file has `StandardOutput=journal` and `StandardError=journal`,
everything our Python script prints goes to the journal.

### Essential journalctl Commands

| Command | What it does |
|---|---|
| `journalctl -u edgeai` | All logs for edgeai |
| `journalctl -u edgeai -f` | Watch logs live (like `tail -f`) |
| `journalctl -u edgeai -n 50` | Last 50 lines |
| `journalctl -u edgeai -n 50 -f` | Last 50 lines then watch live |
| `journalctl -u edgeai -p err` | Errors only |
| `journalctl -u edgeai -p warning` | Warnings and above |
| `journalctl -u edgeai -p debug` | All levels including debug |
| `journalctl -u edgeai -b` | Logs from this boot only |
| `journalctl -u edgeai -b -1` | Logs from previous boot |
| `journalctl -u edgeai --since today` | Today's logs only |
| `journalctl -u edgeai --since "1 hour ago"` | Last hour |
| `journalctl -u edgeai --since "18:00" --until "19:00"` | Between two times |
| `journalctl -u edgeai --no-pager` | No line wrapping (good for copy-paste) |
| `journalctl -u edgeai -r` | Reverse order (newest first) |
| `journalctl -u edgeai -o short-precise` | Readable timestamps with microseconds |

### Log Severity Levels (OTel ordering)

| Level | Flag | Description |
|---|---|---|
| `trace` | `-p trace` | Very detailed debugging info |
| `debug` | `-p debug` | Debug information |
| `info` | `-p info` | Informational messages |
| `warning` | `-p warning` | Warnings |
| `err` | `-p err` | Errors |
| `crit` | `-p crit` | Critical conditions |
| `alert` | `-p alert` | Alerts |
| `emerg` | `-p emerg` | Emergency |

### Journal Disk Management (important on Raspberry Pi)

```bash
# See how much disk space the journal is using
journalctl --disk-usage

# Remove logs older than 7 days
sudo journalctl --vacuum-time=7d

# Keep only the last 100MB of logs
sudo journalctl --vacuum-size=100M
```

**Why this matters on a Pi:** The journal stores logs on the SD card. On a long-running Pi
that generates lots of log output, the journal can fill the SD card over time.

## What This Program Does

- `journalctl_cheatsheet.py` — prints all journalctl commands with explanations
- `log_level_demo.py` — demonstrates Python logging levels that journalctl can filter

## How to Run

```bash
python3 journalctl_cheatsheet.py
python3 log_level_demo.py
```
