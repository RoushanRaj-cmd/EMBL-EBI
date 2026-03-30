import pandas as pd
import numpy as np
import os

def generate_mave_mock():
    # Focused on prioritized genes from Perturbation Catalogue
    gene_configs = {
        "TP53": ["p.Arg175H", "p.Gly245S", "p.Arg248Q"],
        "PTEN": ["p.Arg130G", "p.Gly129E"],
        "BRCA1": ["p.Cys61G", "p.Asp67Y"]
    }
    
    data = []
    for gene, variants in gene_configs.items():
        for v in variants:
            score = np.random.uniform(-4, 0)
            interpretation = "Deleterious" if score < -2 else "Likely Pathogenic"
            data.append({
                "variant": v,
                "gene": gene,
                "functional_score": round(score, 2),
                "interpretation": interpretation,
                "assay": "Saturation Mutagenesis"
            })
    
    df = pd.DataFrame(data)
    df.to_csv("mock_mave_data.csv", index=False)
    print("Generated prioritized mock_mave_data.csv")

if __name__ == "__main__":
    generate_mave_mock()
