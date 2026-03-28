# GSoC 2026 EMBL-EBI Proof of Concept

This repository contains the Proof of Concept (PoC) for the **Perturbation-Aware LLM** project (EMBL-EBI GSoC 2026). It demonstrates a data-to-prompt pipeline bridging the gap between biological data structures (scPerturb-seq, MAVE) and natural language reasoning to support the "Virtual Cell" and "Lab-in-the-Loop" paradigms.

## Vision: Lab-in-the-Loop

The objective is not to train a foundation model from scratch, but rather to use Parameter-Efficient Fine-Tuning (PEFT, e.g., QLoRA) and textualized representations of expression profiles to turn an LLM into a reasoning engine for causal biological perturbations.

```mermaid
flowchart LR
    A[Perturbation Catalogue Data] --> B[Data Textualization Script]
    B --> C[JSON Prompt Formulation]
    C --> D[Fine-Tuned LLM Llama 3 / Mistral]
    D --> E[Predicted Response Reasoning]
    E --> F[New Experiment Design]
```

## Setup & Demo

### Dependencies
Install the required packages:
```bash
pip install scanpy pandas peft numpy h5py anndata
```

### 1. Generating Mock Data
Because the full Perturbation Catalogue datasets are massive, run this script to generate a small mock subset (`sample_perturb.h5ad`):
```bash
python generate_mock_data.py
```

### 2. The "Textualization" Script
This script takes an `.h5ad` single-cell file and transforms it into an instruction-tuning format. It converts expression values into a "Cell Sentence."
Visualizations are saved in the `graphs_and_images/` directory.
```bash
python visualize_poc.py
python data_to_prompt.py
```

### 3. Streamlit Dashboard (Interactive PoC)
A professional web interface for biological exploration and in silico perturbation predictions.
```bash
streamlit run app.py
```

### 4. Virtual Cell Reasoning Test
The `gold_standard_eval.json` includes early benchmarks (ground truth) mapping perturbations to expected biological responses.

## Project Structure
- `app.py`: Streamlit Dashboard implementation.
- `visualize_poc.py`: Generates UMAP, DotPlot, benchmarks, and confusion matrices.
- `data_to_prompt.py`: Textualization pipeline logic.
- `generate_mock_data.py`: Utility to generate dummy biological data.
- `graphs_and_images/`: Local storage for generated visual assets.
