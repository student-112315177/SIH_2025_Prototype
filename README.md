# Elysian Analytics — Deep-Sea eDNA AI Explorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://elysian-analytics-7lr7c8jvkadnuykxlteokg.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Demo Video](https://img.shields.io/badge/demo-watch-red?logo=youtube)](https://www.youtube.com/watch?v=KUIW1Y8ABew)
[![GitHub Codespaces](https://img.shields.io/badge/ready-codespaces-1f425f?logo=github)](https://github.com/features/codespaces)

**Accelerate biodiversity discovery from environmental DNA with hybrid AI + BLAST analysis.**

Upload a FASTA file and get an instant, interactive biodiversity report — taxonomic predictions, confidence scores, live NCBI cross-references, and novelty flags for every sequence.

---

## Table of Contents

- [What It Does](#what-it-does)
- [Features](#features)
- [Pipeline Overview](#pipeline-overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Training Your Own Models](#training-your-own-models)
- [Bioinformatics Pipeline](#bioinformatics-pipeline)
- [Deployment](#deployment)
- [Performance Notes](#performance-notes)
- [License](#license)

---

## What It Does

Environmental DNA (eDNA) analysis lets us survey biodiversity from a water or soil sample — but traditional methods are slow and miss organisms absent from reference databases. **Elysian Analytics** solves this with a hybrid workflow:

1. **AI-First Classification** — Three machine learning models (CNN, XGBoost, Random Forest) predict taxonomy from DNA sequence patterns in milliseconds.
2. **Live BLAST Validation** — Each AI prediction is cross-referenced against NCBI's `nt` database in real time.
3. **Novelty Detection** — Sequences that don't match known databases are automatically flagged as potential discoveries.

The result is a unified, color-coded dashboard that tells you at a glance: *"Is this a known species, a potential new find, or an AI-discovered novel pattern?"*

---

## Features

| Capability | Detail |
|-----------|--------|
| **Multi-Model AI** | Choose between **XGBoost** (recommended), **1D-CNN** (TensorFlow/Keras), or **Random Forest** |
| **Live NCBI BLAST** | Automatic `blastn` queries with real-time percent identity and taxonomy |
| **Novelty Triaging** | Flags sequences as: 🟢 *Consistent*, 🟡 *Potentially Novel*, or 🔴 *AI Discovery* |
| **Interactive Dashboard** | Summary metrics, Plotly pie charts, color-coded results table |
| **CSV Export** | One-click download of the full annotated report |
| **FASTA Upload** | Supports `.fasta`, `.fa`, `.fna` — automatic deduplication |
| **Deep Ocean Theme** | Immersive UI with custom CSS styling |
| **Devcontainer Ready** | One-click spin up in GitHub Codespaces or VS Code Remote |

---

## Pipeline Overview

```
Raw FASTQ
    │
    ▼
┌─────────────────────┐
│   fastp (QC)        │  bioinformatics/01_qc_fastp.ps1
├─────────────────────┤
│   cutadapt (trim)   │  bioinformatics/02_trim_cutadapt.ps1
├─────────────────────┤
│   DADA2 (ASVs)      │  bioinformatics/03_dada2_pipeline.R
└─────────┬───────────┘
          │  FASTA
          ▼
┌─────────────────────┐
│  AI Classification  │  XGBoost / CNN / Random Forest
├─────────────────────┤
│  Live NCBI BLAST    │  BioPython NCBIWWW.qblast()
├─────────────────────┤
│  Novelty Analysis   │  Cross-reference AI × BLAST
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Interactive Report │  Streamlit dashboard
└─────────────────────┘
```

---

## Technology Stack

| Layer | Tools |
|-------|-------|
| **Frontend** | [Streamlit](https://streamlit.io/) + Custom CSS |
| **Backend** | Python 3.9+ |
| **Data** | Pandas, NumPy |
| **Bioinformatics** | [BioPython](https://biopython.org/), [DADA2](https://benjjneb.github.io/dada2/) (R), fastp, cutadapt |
| **Classic ML** | [scikit-learn](https://scikit-learn.org/) (Random Forest, LabelEncoder), [XGBoost](https://xgboost.readthedocs.io/) |
| **Deep Learning** | [TensorFlow / Keras](https://www.tensorflow.org/) (1D-CNN) |
| **Visualization** | [Plotly Express](https://plotly.com/python/plotly-express/) |
| **Environment** | Devcontainer (Debian bookworm), GitHub Codespaces |

---

## Project Structure

```
Elysian-Analytics/
│
├── app/                        # Streamlit web application
│   ├── main.py                 # Main app entry point
│   ├── style.css               # Deep Ocean theme CSS
│   └── __init__.py
│
├── bioinformatics/             # FASTQ → ASV preprocessing
│   ├── 01_qc_fastp.ps1
│   ├── 02_trim_cutadapt.ps1
│   ├── 03_dada2_pipeline.R
│   └── run_dada2.R
│
├── ml/                         # ML embedding + training helpers
│   ├── embeddings.py           # K-mer frequency generation
│   ├── random_forest.py
│   └── __init__.py
│
├── scripts/                    # Standalone utility scripts
│   ├── train_rf_model.py
│   ├── train_xgb_model.py
│   ├── train_dl_model.py
│   ├── generate_report.py      # BLAST + XML report
│   ├── parse_blast_report.py
│   ├── run_blast_and_flag.py   # BLAST + novelty flagging
│   ├── clean_dataset.py
│   ├── cluster_fasta.py
│   ├── find_eukaryotes.py
│   └── ...
│
├── src/                        # Data preparation + unified training
│   ├── download_data.py        # NCBI Entrez download
│   ├── prepare_data.py
│   ├── prepare_data_v2.py
│   ├── train_all_models.py     # Train RF + XGBoost + CNN at once
│   ├── explore_fasta.py
│   └── train_ml.py
│
├── models/                     # Pre-trained model files
│   ├── xgboost_model.pkl
│   ├── random_forest_baseline.pkl
│   ├── label_encoder.pkl
│   ├── dl_model.h5
│   ├── eDNA_model_xgboost_50_seq.pkl
│   ├── eDNA_model_random_forest_50_seq.pkl
│   └── eDNA_model_cnn_50_seq.h5
│
├── data/                       # Sequence datasets
│   ├── fasta/                  # Training, demo, and ASV FASTA files
│   ├── fastq/                  # Raw sequencing reads
│   ├── filtered/               # QC-passed reads
│   ├── labels/                 # Labeled datasets
│   ├── processed/              # Feature matrices
│   ├── raw/                    # Raw source sequences
│   └── tables/                 # ASV tables + BLAST reports
│
├── requirements.txt
├── .devcontainer/
└── LICENSE
```

---

## Quick Start

### Prerequisites

- Python 3.9+
- (Optional) [R](https://www.r-project.org/) + [DADA2](https://benjjneb.github.io/dada2/) for the bioinformatics pipeline
- (Optional) [fastp](https://github.com/OpenGene/fastp) + [cutadapt](https://cutadapt.readthedocs.io/) for read QC

### Installation

```bash
# Clone the repo
git clone https://github.com/shivvein/Elysian-Analytics.git
cd Elysian-Analytics

# Create and activate a virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS / Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app/main.py
```

Open your browser to **http://localhost:8501**.

> Pre-trained models are included in `models/`. If you want to train fresh ones, see [Training Your Own Models](#training-your-own-models).

### Docker / Devcontainer

The `.devcontainer/devcontainer.json` provides a ready-to-use environment for VS Code Remote Containers or GitHub Codespaces. It auto-installs dependencies and launches the app on port 8501.

---

## Usage Guide

1. **Upload a FASTA file** — Use the sidebar file uploader (`.fasta`, `.fa`, `.fna`).
2. **Select a model** — XGBoost is recommended for best speed/accuracy.
3. **Click "Analyze Sequences"** — The app will:
   - Parse and deduplicate sequences
   - Run AI classification
   - Query NCBI BLAST for each sequence
   - Cross-reference results
4. **Explore the dashboard:**
   - **Summary cards** — Total ASVs, AI Discoveries, Top Predicted Group
   - **Pie chart** — Taxonomic distribution (interactive Plotly)
   - **Results table** — Color-coded by novelty status
   - **Download CSV** — Full annotated report

### Novelty Classification

| Status | Color | Meaning |
|--------|-------|---------|
| **Consistent with NCBI** | 🟢 Green | AI prediction matches NCBI (identity ≥ 90%) |
| **Potentially Novel** | 🟡 Yellow | Best BLAST match < 90% identity |
| **AI Discovery** | 🔴 Red | AI predicted a novel pattern label with no NCBI match |

---

## Training Your Own Models

The repository includes a complete training pipeline.

### Data Preparation

```bash
# Download sequences from NCBI Entrez
python src/download_data.py

# Prepare labeled dataset (combine FASTA files with taxon labels)
python src/prepare_data.py

# Or use inline-annotated FASTA files
python src/prepare_data_v2.py

# Clean dataset (remove rare classes)
python scripts/clean_dataset.py

# Generate a BLAST-annotated golden dataset
python scripts/create_golden_dataset.py
```

### Train Models

```bash
# Train all three models at once (edit MODEL_TO_TRAIN in the script)
python src/train_all_models.py

# Or train individually:
python scripts/train_rf_model.py     # Random Forest
python scripts/train_xgb_model.py    # XGBoost
python scripts/train_dl_model.py     # 1D-CNN
```

### Model Architectures

| Model | Features | Architecture |
|-------|----------|-------------|
| **Random Forest** | 6-mer frequency counts | `RandomForestClassifier(n_estimators=100, class_weight='balanced')` |
| **XGBoost** | 6-mer frequency counts | `XGBClassifier(objective='multi:softprob')` |
| **1D-CNN** | One-hot encoded (282 bp padded) | `Conv1D(32,12)` → `MaxPool1D(4)` → `Conv1D(64,8)` → `Dense(256)` → Softmax |

### The Novelty Pattern Label

The model is trained with a special label (`Rhizoclosmatium sp.`) that represents sequences with unusual patterns. When the model predicts this label for a sequence that has no close BLAST match, the app flags it as an **AI Discovery** — a genuinely novel pattern the AI has recognized.

---

## Bioinformatics Pipeline

For processing raw FASTQ sequencing data into ASV FASTA files:

```powershell
# Step 1: Quality control with fastp
.\bioinformatics\01_qc_fastp.ps1

# Step 2: Primer trimming with cutadapt
.\bioinformatics\02_trim_cutadapt.ps1

# Step 3: DADA2 denoising (R)
Rscript bioinformatics/03_dada2_pipeline.R
```

This produces an ASV table and representative FASTA sequences ready for upload into the Elysian Analytics app.

---

## Deployment

### Streamlit Community Cloud

The app is deployed at:
**https://elysian-analytics-7lr7c8jvkadnuykxlteokg.streamlit.app/**

To deploy your own fork:

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your repo, set the main file to `app/main.py`
4. Ensure all model files in `models/` are committed (use Git LFS if needed)

### Custom Server

```bash
streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
```

---

## Performance Notes

- **BLAST queries** take ~2–5 seconds per sequence depending on NCBI server load. Analysis of 50 ASVs typically completes in 2–4 minutes.
- **AI classification** is near-instant (< 100 ms per sequence).
- The CNN model requires a 282 bp fixed input; shorter sequences are zero-padded.
- For large datasets (> 200 ASVs), consider running BATCH BLAST via `scripts/run_blast_and_flag.py` as a preprocessing step.

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.

---

<p align="center">
  Built with ❤️ for the deep sea and open science<br>
  <sub>— shivvein, 2025</sub>
</p>
