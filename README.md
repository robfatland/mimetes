# mimetes


Learning by imitation; integrating technologies to discover, build and use models. 
Key resources include Hugging Face, `pytorch`, Asta Labs, the `kiro` IDE, AWS `Bedrock`. 


> From the Greek: μιμητής "one who imitates".


## Overview


This repo is built as case studies comprising a learning sequence. Primary focus is
on neural networks



| Technology Layer | Tool |
|-------|------|
| Language | Python |
| ML Framework | PyTorch |
| Model Ecosystem | Hugging Face (transformers, datasets, hub) |
| Environment | Miniconda (`mimetes` env) on WSL/Linux |
| Containerization | Docker |
| IDE | Kiro: An AWS-provided VS Code variant with coding assistant |


## Getting Started


Use `requirements.txt` to build a necessary environment including `pytorch`.


```bash
# Create and activate the conda environment
conda create -n mimetes python=3.11 -y
conda activate mimetes

# Install dependencies
pip install -r requirements.txt
```


## Case Studies


| # | Topic | Status |
|---|-------|--------|
| 01 | Fine-tuning ResNet-18 on CIFAR-10 | In progress |
| 02 | Train a neural network from scratch (MNIST) | Not started |
| 03 | Using 3 types of AI for research (glaciology) | Presented |
| 04 | GAN: generative adversarial network | Not started |
| 05 | Science gateway API | Not started |
| 06 | Clustering: k-means vs spectral graph theory | Not started |
| 07 | Random forest | Not started |
| 08 | TBD | — |
| 09 | TBD | — |



## Rendering Slide Decks

Each case study has a `slides.md` (Marp format). The root `slides.md` is the
PyTorch overview deck. All render to self-contained HTML with embedded images.

```bash
# Render all decks
make decks

# Render just the root PyTorch deck
make deck-pytorch

# List which slide sources exist
make deck-list

# Clean generated HTML
make clean-decks
```

Requires: `npm install -g @marp-team/marp-cli`


## Project Structure

```
mimetes/
├── README.md                  # This file
├── LearnPyTorch.md            # Conceptual deep-dive, built incrementally
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container for reproducibility / cloud migration
├── logistics_map.py           # Dynamical systems visualization (bifurcation, cobwebs)
├── images/                    # Shared images (logos, logistics map diagrams)
├── case_studies/
│   ├── 01_HF_fine_tuning/     # Fine-tune ResNet-18 on CIFAR-10
│   ├── 02_train_from_scratch/ # Train a network from scratch on MNIST
│   ├── 03_research_mechanics/ # Programmatic AWS-AI for research (presented)
│   ├── 04_GAN/                # Generative adversarial network
│   ├── 05_science_gateway/    # Science gateway API
│   ├── 06_clustering/         # Clustering: k-means vs spectral graph theory
│   ├── 07_random_forest/      # Random forest
│   ├── 08_tbd/
│   └── 09_tbd/
└── ScienceGatewayAPI/         # Prototype notebooks (→ case study 05)
```
