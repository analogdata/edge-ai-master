# 08 — Full Setup Walkthrough (Step by Step)

## Concept (Part 11 of the notes)

Follow these steps **in order** the first time you set up a service.

### The Setup Order

1. Create your project folder
2. Place your Python script
3. Create the `.env` file
4. Protect the `.env` file (`chmod 600`)
5. Add `.env` to `.gitignore`
6. Write the `.service` file
7. Copy the `.service` file to `/etc/systemd/system/`
8. `daemon-reload` — tell systemd about the new file
9. `start` — start the service now
10. `status` — verify it's running
11. `enable` — auto-start at boot

### Why Order Matters

- You must `daemon-reload` **before** `start` — otherwise systemd doesn't know about your file
- You must `start` **before** `enable` — so you can verify it actually works
- You `enable` **last** — so it only auto-starts at boot after you've confirmed it runs

## What This Program Does

`setup_walkthrough.py` is an interactive guide that prints each step with the exact commands
to run. It also includes a shell script (`setup.sh`) that automates the setup on a Raspberry Pi.

## How to Run

```bash
# Interactive guide:
python3 setup_walkthrough.py

# Automated setup (on Raspberry Pi only):
sudo bash setup.sh
```
