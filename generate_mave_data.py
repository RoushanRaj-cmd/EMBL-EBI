import pandas as pd
import numpy as np
import os

def generate_mave_mock():
    # Mocking a MAVE (Multiplexed Assay of Variant Effect) dataset
    # Focusing on variant-level effects (e.g., missense mutations in TP53)
    variants = ["p.Arg175H", "p.Gly245S", "p.Arg248Q", "p.Arg273H", "p.Arg282W"]
    data = []
    
    for v in variants:
        # Score represents the functional impact (lower = more deleterious often)
        score = np.random.uniform(-4, 1)
        # Class indicates clinical or functional interpretation
        interpretation = "Deleterious" if score < -2 else "Neutral"
        data.append({
            "variant": v,
            "gene": "TP53",
            "functional_score": round(score, 2),
            "interpretation": interpretation,
            "assay": "BrCA1 saturation mutagenesis"
        })
    
    df = pd.DataFrame(data)
    df.to_csv("mock_mave_data.csv", index=False)
    print("Generated mock_mave_data.csv")

if __name__ == "__main__":
    generate_mave_mock()
