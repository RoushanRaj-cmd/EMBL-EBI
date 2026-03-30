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

def create_variant_prompt(mave_row):
    """Encodes a MAVE variant effect into a prompt with compositional reasoning."""
    reasoning_map = {
        "TP53": "This mutation typically disrupts the DNA-binding domain, leading to a loss of transcriptional activation of p21, thereby bypassing G1 cell-cycle arrest.",
        "PTEN": "The variant likely destabilizes the phosphatase domain, causing a sustained activation of the PI3K/AKT signaling pathway and downstream metabolic shifts.",
        "BRCA1": "This substitution in the RING domain disrupts E3 ubiquitin ligase activity, compromising the cell's ability to repair double-strand DNA breaks via homologous recombination."
    }
    
    gene = mave_row['gene']
    reasoning = reasoning_map.get(gene, "This mutation disrupts protein stability and alters the downstream transcriptomic signature.")
    
    prompt = {
        "instruction": f"Predict the functional impact and transcriptional consequence of the {mave_row['variant']} variant in gene {gene}.",
        "context": f"Assay: {mave_row['assay']}. Functional Score: {mave_row['functional_score']}.",
        "response": f"The variant {mave_row['variant']} is {mave_row['interpretation']}. {reasoning}"
    }
    return prompt

def main():
    import os
    print("--- [Compositional PAL-LLM] Multimodal Prompt Generator ---")
    
    # 1. Handle Single-Cell (scPerturb-seq)
    if os.path.exists("sample_perturb.h5ad"):
        print("\n[Loading scRNA-seq Component...]")
        prompt = create_perturbation_prompt("sample_perturb.h5ad")
        print(f"Cell-to-Sentence: {prompt['instruction'][:50]}...")
    
    # 2. Handle Variant-Effect (MAVE / DNA-Level)
    if os.path.exists("mock_mave_data.csv"):
        print("\n[Loading MAVE/Variant Component...]")
        mave_df = pd.read_csv("mock_mave_data.csv")
        # Show one sample of compositional mapping
        sample_row = mave_df.iloc[0] # Usually TP53
        variant_prompt = create_variant_prompt(sample_row)
        print(f"Composed Prompt: {variant_prompt['instruction']}")
        print(f"Biological Reasoning: {variant_prompt['response']}")

    print("\n[MOCK] PEFT Adapter Configuration (Compositional Modules):")
    print(mock_lora_config())

if __name__ == "__main__":
    main()
