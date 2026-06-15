---
inclusion: always
---

# Mimetes Project Context

## Overview

This repository is a learning sequence for working with models and data from Hugging Face
(and potentially other modeling resources). The name comes from Greek: μιμητής — one who imitates.

The goal is to build skill progressively through a series of case studies (minimum 4, target ~7),
culminating in building a de novo model.

## Technology Stack

- **Primary language:** Python
- **Core framework:** PyTorch
- **Model ecosystem:** Hugging Face (transformers, datasets, hub)
- **Environment manager:** Miniconda
- **Conda environment name:** `mimetes`
- **OS:** Linux via WSL on Windows
- **Containerization:** Docker (for portability and eventual cloud migration)

## Development Environment

- The Python kernel runs in a Linux (WSL) environment.
- The developer works from one of two Windows laptops ("the Dell" or "the Surface"),
  accessing Linux through WSL.
- The active miniconda environment is called `mimetes`.
- When processing scales up, work may migrate to a cloud VM.

## Dependency Management

- Prefer declaring dependencies in `requirements.txt` rather than ad hoc `conda install` commands.
- Keep `requirements.txt` up to date as new libraries are introduced.
- Use `pip install -r requirements.txt` within the conda environment for reproducibility.
- **Disk hygiene:** Be alert to practices that eat up disk volume on a laptop. After
  Python package installations, offer to clear the cache (`pip cache purge` and/or
  `conda clean --all -y`). PyTorch alone can leave multiple GB in cache.

## Documentation Standards

- Markdown files should stay at or under 500 lines.
- When a substantial advance is made during a session (new case study, new capability, structural
  change), Kiro will update the relevant markdown documentation to reflect that progress.
- **Every illuminating remark made in chat** (design decisions, technical findings, gotchas,
  performance observations) must be reflected in the relevant StudyPlan.md or case study
  documentation. The chat is ephemeral; the docs are the record.
- The README.md serves as the top-level guide; individual case studies get their own docs.

## Project Structure (aspirational)

```
mimetes/
├── README.md                  # Top-level overview and navigation
├── requirements.txt           # Pinned Python dependencies
├── Dockerfile                 # Container definition for reproducibility
├── .kiro/
│   └── steering/              # Kiro steering files
├── case_studies/
│   ├── 01_<topic>/            # Each case study in its own directory
│   │   ├── README.md          # Case study overview and learnings
│   │   ├── notebook.ipynb     # Exploratory work (optional)
│   │   └── *.py               # Scripts
│   ├── 02_<topic>/
│   └── ...
└── docs/                      # Additional documentation as needed
```

## Conventions

- Case studies are numbered sequentially (`01_`, `02_`, ...) to reflect the learning progression.
- Each case study directory contains its own README documenting objectives, approach, and findings.
- Python code follows standard formatting (prefer Black or similar formatter if configured).
- Commit messages should be descriptive of what was learned or built, not just what changed.

## Presentation (Marp) Conventions

- Slide content should be focused in the center 80% of the slide, both horizontally
  and vertically. Avoid text or images that crowd edges, headers, or footers.
- Use `<style scoped>` to reduce font size on dense slides rather than letting
  content overflow.
- Images use Marp's `![w:NNN]` syntax for sizing; place in an `images/` subfolder.

## Cloud Migration Notes

- Docker is the planned mechanism for moving work off localhost to a cloud VM.
- The Dockerfile should capture the full environment so the project runs identically anywhere.
- Keep an eye on GPU requirements as models grow; document any CUDA/driver dependencies.
