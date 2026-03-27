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
This script takes an `.h5ad` single-cell file and transforms it into an instruction-tuning format suitable for LLMs. It converts the gene expression values into a "Cell Sentence" (a ranked list of genes).
```bash
python data_to_prompt.py
```

### 3. Virtual Cell Reasoning Test
The `gold_standard_eval.json` includes early benchmarks (ground truth) that map specific perturbations (e.g. TP53 Knockout or MYC Activation) to their expected biological responses, representing a rudimentary validation benchmark.
