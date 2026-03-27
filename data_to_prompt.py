import scanpy as sc
import pandas as pd
import json

def create_perturbation_prompt(h5ad_path):
    # 1. Load the scPerturb-seq data (AnnData format)
    adata = sc.read_h5ad(h5ad_path)
    
    # 2. Extract metadata (The 'Perturbation')
    # Assuming 'condition' and 'cell_type' are in metadata (obs)
    sample_cell = adata[0]
    
    # Safely extract categorical values or strings depending on pandas version
    perturbation = sample_cell.obs['condition'].iloc[0]
    cell_type = sample_cell.obs['cell_type'].iloc[0]
    
    # 3. Create the 'Cell Sentence' (Ranked Gene expression)
    # Get top 10 expressed genes for this cell
    gene_names = adata.var_names
    # Handle different sparse array types (csr_matrix, etc.)
    X = sample_cell.X
    expression_values = X.toarray().flatten() if hasattr(X, 'toarray') else X.flatten()
    
    ranked_genes = [gene for _, gene in sorted(zip(expression_values, gene_names), reverse=True)[:10]]
    gene_str = ", ".join(ranked_genes)
    
    # 4. Construct the Instruction-Tuning Prompt
    prompt = {
        "instruction": f"Predict the cellular response for a {cell_type} cell under {perturbation} perturbation.",
        "input": "",
        "output": f"The top 10 markers for this state are: {gene_str}."
    }
    return prompt

# Configuration for 350h project (efficient & scalable)
def mock_lora_config():
    try:
        from peft import LoraConfig
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"], # Targeting attention layers
            lora_dropout=0.05,
            task_type="CAUSAL_LM"
        )
        return str(lora_config)
    except ImportError:
        return "LoraConfig(r=16, lora_alpha=32, target_modules=['q_proj', 'v_proj'], lora_dropout=0.05, task_type='CAUSAL_LM') (mocked, peft not installed)"

if __name__ == "__main__":
    import os
    if not os.path.exists("sample_perturb.h5ad"):
        print("Error: sample_perturb.h5ad not found. Please run generate_mock_data.py first.")
    else:
        prompt = create_perturbation_prompt("sample_perturb.h5ad")
        print("Generated Prompt:")
        print(json.dumps(prompt, indent=2))
        
        print("\nMock LoRA Configuration:")
        print(mock_lora_config())
