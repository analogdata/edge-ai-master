# 05 — The [Install] Section

## Concept (Part 7 of the notes)

The `[Install]` section tells systemd **when** to start your service during the boot sequence.

```ini
[Install]
WantedBy=multi-user.target
```

### `WantedBy=multi-user.target`

`multi-user.target` is the stage where the Pi has fully booted, all system services are running,
and the system is ready for normal use. This is the correct target for almost every Pi application.

This line only takes effect when you run:
```bash
sudo systemctl enable edgeai
```

Under the hood, `enable` creates a symbolic link inside:
```
/etc/systemd/system/multi-user.target.wants/edgeai.service
```

This symlink causes systemd to start your service whenever it reaches `multi-user.target` during boot.

## What This Program Does

`install_section_demo.py` explains the [Install] section and the boot sequence.

## How to Run

```bash
python3 install_section_demo.py
```
