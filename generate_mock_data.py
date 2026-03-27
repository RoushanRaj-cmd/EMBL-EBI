import scanpy as sc
import pandas as pd
import numpy as np
from anndata import AnnData

def generate_mock_h5ad(filename="sample_perturb.h5ad"):
    # Create mock data
    n_obs = 100
    n_vars = 500
    
    # Random count matrix (using poisson to simulate counts)
    X = np.random.poisson(lam=2, size=(n_obs, n_vars)).astype(np.float32)
    
    # Mock observation annotations (cells)
    obs = pd.DataFrame({
        'condition': pd.Categorical(np.random.choice(['TP53_knockout', 'Control', 'MYC_activation'], n_obs)),
        'cell_type': pd.Categorical(np.random.choice(['T-Cell', 'B-Cell', 'Macrophage'], n_obs))
    }, index=[f'cell_{i}' for i in range(n_obs)])
    
    # Mock variable annotations (genes)
    var = pd.DataFrame(index=[f'gene_{i}' for i in range(n_vars)])
    
    # Create AnnData object
    adata = AnnData(X=X, obs=obs, var=var)
    adata.write_h5ad(filename)
    print(f"Mock dataset saved to {filename}")

if __name__ == "__main__":
    generate_mock_h5ad()
