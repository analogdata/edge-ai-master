# EdgeAI Engineering Bootcamp

Bootcamp repository for the **EdgeAI Engineering Bootcamp** by Analog Data.

Live sessions: Mon–Fri, 7:30–9:00 PM IST
Instructor: Rajath Kumar K S

---

## How This Repo Is Organised

Each chapter has its own numbered folder.

```
edge-ai-master/
├── 1/       ← Chapter 1
├── 2/       ← Chapter 2
├── 3/       ← Chapter 3
│   ...
└── 97/      ← Chapter 97
```

Every chapter folder follows the same structure:

```
<chapter>/
├── notes/          ← PDF session notes for this chapter
├── *.ipynb         ← Notebooks (run in filename order)
├── pyproject.toml  ← Dependencies for this chapter
└── uv.lock         ← Locked dependency tree
```

---

## Setup

This repo uses **uv** as the package manager. Install it once and use it for every chapter.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For each chapter:

```bash
# Navigate to the chapter folder
cd edge-ai-master/<chapter-number>

# Install dependencies
uv sync

# Launch Jupyter
uv run jupyter notebook
```

Always run `uv sync` from inside the chapter folder — each chapter manages its own dependencies.

---

## How to Work Through a Chapter

1. Read the PDFs in `notes/` before the live session
2. Open the notebooks in filename order
3. Run every cell — do not skip
4. If something is unclear, re-read the corresponding PDF section before asking

---

## Getting Help

- Post your question in the **bootcamp WhatsApp group** with the chapter number and notebook name
- Bring unresolved questions to the next live session

---

## Links

- Course portal: [build.analogdata.io](https://build.analogdata.io)
- Blog: [analogdata.blog](https://analogdata.blog)
- Instructor: [edgeaiengineer.com](https://edgeaiengineer.com)