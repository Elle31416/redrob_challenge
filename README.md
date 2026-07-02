# Redrob Hackathon: Senior AI Engineer Candidate Ranking

This repository contains the candidate ranking pipeline (`rank.py`) for the Redrob Data and AI Hackathon. Our solution deterministically and efficiently ranks 100,000 candidates to identify the top 100 genuine fits for the Senior AI Engineer (Founding Team) role.

## 🚀 Setup Instructions

This ranking pipeline is built completely with **Python Standard Library** and has **no external dependencies**. It relies on highly optimized local processing to comfortably fit within the <5 minute CPU-only and 16GB memory constraints.

### Prerequisites

- **Python 3.8+**
- The `candidates.jsonl` data file must be available locally.

*(Optional)* You can create a virtual environment, though no `pip install` is necessary.

## 💻 Commands for Reproduction

To execute the pipeline and generate the final submission CSV, run the following single command:

```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

*Note: Replace `./candidates.jsonl` with the path to the actual candidates dataset if it resides in another directory.*

The pipeline streams the JSONL file to minimize memory footprint and outputs exactly 100 correctly formatted rows (candidate_id, rank, score, reasoning) directly to `submission.csv`.

## 🧠 Architecture Description

![Pipeline Flow](./pipeline_funnel.svg)

The solution employs a highly optimized, two-stage deterministic ranking architecture to maximize relevance and rigorously avoid honeypots.

### 1. Stage 1: Retrieval and Honeypot Defense
- **Streaming Pipeline:** The ranker streams `candidates.jsonl` to keep memory consumption under 100 MB.
- **Honeypot Detection:** Robust contradiction logic filters out anomalous profiles before any scoring takes place. It checks for impossible career timelines, technical skills claimed prior to actual release dates (e.g., claiming 6 years of GPT-4 experience), and logically disjoint employment chronologies.
- **Fast Retrieval Heap:** A lightweight scoring function prioritizes high-impact product company experience, modern AI/ML skills, and years of experience, maintaining a min-heap of the top 1,500 candidates.

### 2. Stage 2: Deep Re-ranking
The top 1,500 candidates are subjected to a rigorous 100-point multi-dimensional scoring rubric:
- **Capability (30 pts):** Deep semantic evaluation of skills, penalizing shallow keyword stuffing and rewarding coherent clusters (e.g., RAG + Vector DBs).
- **Trajectory (30 pts):** Evaluation of career progression, stability, and tier-1 product company experience over pure IT services backgrounds.
- **Product Fit (25 pts):** Alignment with founding team imperatives—prioritizing product-builders and shippers over pure researchers.
- **Behavioral (15 pts):** Behavioral signals, factoring in notice period constraints, salary alignment, platform responsiveness, and work model (Bangalore/On-site).

Finally, the score resolves deterministic ties to generate the pristine Top 100 submission, supplemented with transparent, candidate-specific reasoning notes.

## 🧪 Testing and Reproducibility

We have included a suite of unit tests to ensure our custom Honeypot and Contradiction logic is bulletproof and rigorously detects synthetic, anomalous, or chronologically impossible profiles. 

To run the unit tests, execute:
```bash
python -m unittest tests/test_honeypot.py
```
This tests for critical edge cases such as claiming expert-level knowledge with zero duration, matching skills against foundation years of new startups, detecting timeline impossibilities (e.g., claiming GPT-4 experience years before release), and ensuring educational chronologies make logical sense.

## 📄 Submission Metadata

Please refer to the `submission_metadata.yaml` at the root of the repository to mirror our portal metadata for the submission process.
If you need the template, please utilize the `submission_metadata_template.yaml` provided in the hackathon bundle.
