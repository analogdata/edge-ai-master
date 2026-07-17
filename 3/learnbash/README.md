# learnbash — Shell Scripting Practice for Edge AI

All scripts are based on the notes: **3.1 — Shell Scripting for EdgeAI**.

## Getting Started

Before running any script, make it executable (one-time per script):

```bash
chmod +x script_name.sh
```

Then run it:

```bash
./script_name.sh
```

Or, make all scripts executable at once:

```bash
chmod +x *.sh
```

## Scripts from the Notes

### Section 2 — Your First Shell Script
| Script | Description |
|--------|-------------|
| `01_hello.sh` | Prints a greeting and the current date |

### Section 3 — Variables
| Script | Description |
|--------|-------------|
| `02_variables.sh` | Creating and using variables with `$` and `${}` |
| `03_command_output.sh` | Capturing command output with `$(...)` |
| `04_readonly_vars.sh` | Read-only (constant) variables with `readonly` |

### Section 4 — Arguments
| Script | Description |
|--------|-------------|
| `05_greet.sh` | Accessing `$0`, `$1`, `$2`, `$#` arguments |
| `06_check_arg.sh` | Checking if an argument was provided with `-z` |

### Section 5 — if Statements
| Script | Description |
|--------|-------------|
| `07_if_numbers.sh` | Comparing numbers with `-gt`, `-eq`, etc. |
| `08_if_strings.sh` | Comparing strings with `=` and `!=` |
| `09_if_file_check.sh` | Checking if a file exists with `-f` |

### Section 6 — for Loops
| Script | Description |
|--------|-------------|
| `10_for_list.sh` | Loop over a list of values |
| `11_for_range.sh` | Loop over a range of numbers using `{1..10}` |
| `12_for_files.sh` | Loop over files matching a glob pattern |
| `13_for_command.sh` | Loop over the output of a command |

### Section 7 — while Loops
| Script | Description |
|--------|-------------|
| `14_while_basic.sh` | Basic while loop with a counter |
| `15_while_infinite.sh` | Infinite loop with `while true` (stop with Ctrl+C) |
| `16_while_read_file.sh` | Read a file line by line with `while IFS= read -r` |

### Section 8 — case Statements
| Script | Description |
|--------|-------------|
| `17_case_statement.sh` | Handle multiple options with `case`/`esac` |

### Section 9 — Safe Mode (`set -euo pipefail`)
| Script | Description |
|--------|-------------|
| `18_set_e.sh` | Demo of `set -e` (exit on error) |
| `19_set_u.sh` | Demo of `set -u` (error on undefined variables) |
| `20_safe_mode.sh` | Full `set -euo pipefail` safe header |

### Section 10 — Practical Script: Health Reporter
| Script | Description |
|--------|-------------|
| `21_health_report.sh` | Checks Pi temperature, memory, disk, CPU load, throttling |

### Section 11 — Practical Script: Model Download + SHA256
| Script | Description |
|--------|-------------|
| `22_download_model.sh` | Downloads a model file and verifies its SHA256 hash |

### Section 12 — cron (Scheduling)
| Script | Description |
|--------|-------------|
| `23_cron_examples.sh` | Prints sample crontab entries and cron expression reference |

### Section 13 — Functions
| Script | Description |
|--------|-------------|
| `24_functions.sh` | Defines and calls functions with `local` variables and arguments |

### Section 14 — Reading User Input
| Script | Description |
|--------|-------------|
| `25_read_input.sh` | Basic `read` for user input |
| `26_read_prompt.sh` | `read -p` for prompt on the same line |
| `27_read_password.sh` | `read -s` for hidden password input |

### Section 15 — Colours
| Script | Description |
|--------|-------------|
| `28_colours.sh` | Colour-coded output using ANSI escape codes |

## Extra Scripts (Beyond the Notes)

| Script | Description |
|--------|-------------|
| `29_cleanup_logs.sh` | Delete log files older than N days (for cron scheduling) |
| `30_batch_inference.sh` | Run inference on all images in a folder |
| `31_run_inference.sh` | Single-image inference runner with colour output and file checks |
| `32_combined_demo.sh` | Interactive demo combining variables, if, for, while, case, functions, colours, and user input |

## Quick Reference

```
Shebang:        #!/bin/bash
Safe mode:      set -euo pipefail
Variable:       name="value"
Use variable:   $name or ${name}
Command output: var=$(command)
Arguments:      $0 $1 $2 ... $# $@
Arithmetic:     $((a + b))
if:             if [ cond ]; then ... elif ... else ... fi
for:            for x in list; do ... done
while:          while [ cond ]; do ... done
case:           case "$var" in val) ;; *) ;; esac
Function:       myFunc() { ... }
File exists:    [ -f "$path" ]
String empty:   [ -z "$var" ]
Make executable: chmod +x script.sh
Edit crontab:   crontab -e
List crontab:   crontab -l
```
