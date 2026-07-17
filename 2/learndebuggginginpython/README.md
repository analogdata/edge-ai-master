# Python Debugging & Profiling — Demo Programs

Companion programs for the lecture **"2.4 Python Debugging & Profiling"**.

## Programs

| # | File | Topic | Run Command |
|---|------|-------|-------------|
| 01 | `01_pdb_breakpoint.py` | Interactive debugging with `pdb` / `breakpoint()` | `python 01_pdb_breakpoint.py` |
| 02 | `02_logging_rotating_handler.py` | Structured logging with `RotatingFileHandler` | `python 02_logging_rotating_handler.py` |
| 03 | `03_cprofile_pstats.py` | Function-level profiling with `cProfile` + `pstats` | `python 03_cprofile_pstats.py` |
| 04 | `04_line_profiler.py` | Line-by-line timing with `line_profiler` | `kernprof -l -v 04_line_profiler.py` |
| 05 | `05_memory_profiler.py` | Per-line memory tracking with `memory_profiler` | `python -m memory_profiler 05_memory_profiler.py` |
| 06 | `06_profiling_workflow.py` | Full workflow: profile → find bottleneck → optimise → re-profile | `python 06_profiling_workflow.py` |

## Prerequisites

```bash
pip install line_profiler memory_profiler
```

## Profiling Tool Decision Guide

| Question | Tool |
|----------|------|
| Which function is consuming the most time? | `cProfile` + `pstats` |
| Which exact line inside that function is the bottleneck? | `line_profiler` |
| Why is my Pi running out of memory? | `memory_profiler` |
| My code is returning wrong values — I need to inspect live state | `pdb` |
| I need permanent, structured, size-bounded logs in production | `logging` + `RotatingFileHandler` |

## Optimisation Workflow

```
cProfile  →  find the slow function
    ↓
line_profiler  →  find the slow line
    ↓
optimise  →  fix the bottleneck
    ↓
re-profile  →  confirm improvement
```

## Key Takeaways for Edge AI

- **Profiling before optimising** — intuition is wrong surprisingly often
- **RotatingFileHandler is mandatory** on Pi — unbounded logs fill the SD card
- **Memory leaks kill** — 1MB/frame leak OOM-kills a Pi in minutes
- **`breakpoint()` over `print()`** — inspect live state, don't guess
