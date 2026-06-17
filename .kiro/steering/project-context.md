---
inclusion: always
---

# Mimetes Project Context

## Overview: Tech Serving Research

AI/ML models and scientific data resources — a progressive learning sequence.

The name comes from Greek: μιμητής — one who imitates.

The goal is to build skill through a series of seven case studies. The
aspirational goal is to build a de novo model.

## Technology Stack

- **Primary language:** Python
- **Core framework:** PyTorch (planned, not yet exercised)
- **Model ecosystem:** Hugging Face, AWS Bedrock, AI2 Asta, and other resources as needed
- **Environment manager:** Miniconda
- **Conda environment name:** `mimetes`
- **OS:** Linux via WSL on Windows
- **Containerization:** Docker (for portability and eventual cloud migration)
- **IDE:** Kiro (AWS-provided VS Code variant with coding assistant)
- **Presentation:** Marp (Markdown → HTML slides)

## Development Environment

- The Python kernel runs in a Linux (WSL) environment.
- The developer works from one of two Windows laptops ("the Dell" or "the Surface"),
  accessing Linux through WSL.
- The `mimetes` conda environment is the only environment used for this repo.
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

## Project Structure

```
mimetes/
├── README.md                  # Top-level overview and navigation
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container definition for reproducibility
├── .gitignore                 # Excludes PDFs, KMLs, caches, secrets
├── .kiro/
│   └── steering/              # Kiro steering files
├── case_studies/
│   ├── 01_something_basic/
│   │   ├── StudyPlan.md
│   │   ├── slides.md          # Marp presentation deck
│   │   ├── images/
│   │   └── *.py
│   ├── 02_notional_GAN/
│   │   ├── StudyPlan.md
│   │   ├── slides.md
│   │   ├── images/
│   │   └── *.py
│   ├── 03_research_mechanics/
│   │   ├── StudyPlan.md
│   │   ├── slides.md
│   │   ├── images/
│   │   └── *.py
│   ├── 04_tbd/
│   │   ├── StudyPlan.md
│   │   ├── slides.md
│   │   └── ...
│   ├── 05_tbd/
│   │   ├── StudyPlan.md
│   │   ├── slides.md
│   │   └── ...
│   ├── 06_tbd/
│   │   ├── StudyPlan.md
│   │   ├── slides.md
│   │   └── ...
│   └── 07_tbd/
│       ├── StudyPlan.md
│       ├── slides.md
│       └── ...
```

## Conventions

- Case studies are numbered sequentially (`01_`, `02_`, ...) to reflect the learning progression.
- Each case study directory contains a `StudyPlan.md` documenting objectives, approach, and findings.
- Each case study directory contains a `slides.md` (Marp format) for its presentation deck.
- Python code follows standard formatting (prefer Black or similar formatter if configured).
- Commit messages should be descriptive of what was learned or built, not just what changed.

## Presentation (Marp) Conventions

- Slide content should be focused in the center 80% of the slide, both horizontally
  and vertically. Avoid text or images that crowd edges, headers, or footers.
- Use `<style scoped>` to reduce font size on dense slides rather than letting
  content overflow.
- Images use Marp's `![w:NNN]` syntax for sizing; place in an `images/` subfolder.
- Render command: `marp slides.md -o slides.html --allow-local-files --html`

## Cloud Migration Notes

- Docker is the planned mechanism for moving work off localhost to a cloud VM.
- The Dockerfile should capture the full environment so the project runs identically anywhere.
- Keep an eye on GPU requirements as models grow; document any CUDA/driver dependencies.
