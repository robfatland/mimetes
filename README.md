# mimetes

Integrating technologies to explore and build models found at Hugging Face.


> From the Greek: μιμητής "one who imitates".


## What This Is

A progressive learning sequence for working with ML models and data, primarily from
Hugging Face. The journey moves from simple inference tasks through fine-tuning to
eventually building a model from scratch.

## Tech Stack


| Layer | Tool |
|-------|------|
| Language | Python |
| ML Framework | PyTorch |
| Model Ecosystem | Hugging Face (transformers, datasets, hub) |
| Environment | Miniconda (`mimetes` env) on WSL/Linux |
| Containerization | Docker |
| IDE | Kiro: An AWS-provided VS Code variant with coding assistant |


## Getting Started

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
| 01 | Sentiment analysis on IMDB | 🔲 Not started |
| 02 | TBD | 🔲 Not started |
| 03 | AWS Bedrock (Claude): Retrieve an EarthArXiv paper | 🔲 Underway |
| 04 | TBD | 🔲 Not started |

(Minimum 4 case studies; target ~7, culminating in a de novo model.)

## Project Structure

```
mimetes/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container for reproducibility / cloud migration
├── case_studies/
│   ├── 01_Sentimentale/        # Each case study in its own directory
│   ├── 02_<topic>/
│   └── 03_EarthArXiv
└── docs/                  # Additional documentation as needed
```

## Docker

```bash
docker build -t mimetes .
docker run -it mimetes
```
