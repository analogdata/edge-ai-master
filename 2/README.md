# Module 2 — NumPy for Edge AI

This module covers NumPy from basics to advanced Edge AI applications, following the **Edge AI Engineering Bootcamp** curriculum (Module 2.2: "NumPy — The Backbone of Every Edge AI Pipeline").

## Notebooks

| Notebook | Level | Description |
|---|---|---|
| [`numpy_basics.ipynb`](numpy_basics.ipynb) | Beginner | Array creation, shape, dtype, strides, slicing, views vs copies |
| [`numpy_intermediate.ipynb`](numpy_intermediate.ipynb) | Intermediate | Broadcasting, uint8 vs float32, overflow bugs, aggregations, boolean masking |
| [`numpy_advanced.ipynb`](numpy_advanced.ipynb) | Advanced | `np.frombuffer()`, `np.ascontiguousarray()`, vectorised ops vs loops, `np.einsum()`, performance optimization |
| [`numpy_edgeai.ipynb`](numpy_edgeai.ipynb) | Edge AI | Complete camera-to-model pipeline, preprocessing, post-processing, NMS, memory-conscious patterns, common bugs |

## Topics Covered

### Basics
- What is an array (vs Python list)
- Array creation methods (`np.array`, `np.zeros`, `np.ones`, `np.arange`, `np.linspace`, `np.random`)
- Shape and reshaping (`(height, width, channels)` convention)
- dtype (`uint8`, `float32`, `int16`, etc.) and memory implications
- Strides and zero-copy operations (flips, transposes)
- Slicing for image crops (`img[y1:y2, x1:x2]`)
- Views vs copies (`.copy()` when needed)

### Intermediate
- Broadcasting rules (right-to-left shape comparison)
- uint8 vs float32 memory and arithmetic implications
- The uint8 overflow/wraparound bug and safe arithmetic patterns
- Aggregation operations (`mean`, `sum`, `min`, `max`, `std` with `axis`)
- Boolean masking and thresholding
- `np.where` for conditional operations
- Fancy indexing
- Array concatenation and stacking (`np.stack` for batches)

### Advanced
- `np.frombuffer()` — zero-copy camera frame handling
- `np.ascontiguousarray()` — fixing memory layout after transpose/flip
- Vectorised operations vs Python loops (100x speed difference)
- C-order vs Fortran-order memory layout
- `np.einsum()` — Einstein notation for matrix operations
- Pre-allocation, in-place operations, and memory-efficient storage

### Edge AI
- Complete pipeline: Camera → uint8 → float32 → normalize → model → postprocess
- Image preprocessing (BGR→RGB, normalization, standardization, resizing, batching)
- Simulated model inference and post-processing (softmax, confidence thresholding, NMS)
- Batch processing for throughput
- Memory-conscious patterns (in-place ops, streaming, buffer reuse)
- Common Edge AI bugs (height/width swap, uint8 overflow, view modification, non-contiguous arrays, channel order)
- Complete `EdgeAIPipeline` class example

## Setup

```bash
# Install dependencies
uv sync

# Launch Jupyter Lab
uv run jupyter lab
```

## Requirements

- Python >= 3.13
- NumPy >= 2.5.1
- JupyterLab >= 4.6.1
