# 01 — The Problem with Running Scripts Manually

## Concept (Part 1 of the notes)

When you run a Python script manually in a terminal:

```bash
python3 inference.py
```

It works, but has critical problems:

| Situation | What happens |
|---|---|
| You close the terminal | The script dies immediately |
| The Pi restarts (power cut) | The script never starts again |
| The script crashes (bug) | It stays dead until you manually fix it |
| You disconnect from SSH | Every process you started dies |

Scripts run manually only live as long as the terminal session is open.

## What This Program Demonstrates

`inference_manual.py` simulates an Edge AI inference loop that runs in the foreground.
Run it, then try pressing `Ctrl+C` or closing the terminal — the script dies immediately.

This is the **before** picture. The next programs show how systemd solves every one of these problems.

## How to Run

```bash
python3 inference_manual.py
```

Press `Ctrl+C` to stop it. Notice how it just dies — no restart, no cleanup, no auto-recovery.
