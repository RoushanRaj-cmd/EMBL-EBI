import scanpy as sc
import pandas as pd
import numpy as np
import anndata
from anndata import AnnData

# Opt-in to newer string types as requested by the error handler
try:
    anndata.settings.allow_write_nullable_strings = True
except:
    pass

# FORCE legacy string storage to avoid ArrowStringArray serialization issues in AnnData
try:
    pd.options.mode.string_storage = "python"
except:
    pass

def generate_mock_h5ad(filename="sample_perturb.h5ad"):
    # Create mock data
    n_obs = 100
    n_vars = 500
    
    # Random count matrix (using poisson to simulate counts)
    X = np.random.poisson(lam=2, size=(n_obs, n_vars)).astype(np.float32)
    
    # Mock observation annotations (cells)
    obs = pd.DataFrame({
        'condition': np.random.choice(['TP53_knockout', 'Control', 'MYC_activation'], n_obs),
        'cell_type': np.random.choice(['T-Cell', 'B-Cell', 'Macrophage'], n_obs)
    }, index=[f'cell_{i}' for i in range(n_obs)])
    
    # Force everything to standard types to avoid ArrowStringArray issues in newer Pandas/AnnData
    obs['condition'] = obs['condition'].astype(str).astype('category')
    obs['cell_type'] = obs['cell_type'].astype(str).astype('category')
    obs.index = obs.index.astype(str)
    
    # Mock variable annotations (genes)
    var = pd.DataFrame(index=[f'gene_{i}' for i in range(n_vars)])
    var.index = var.index.astype(str)
    
    # Create AnnData object
    adata = AnnData(X=X, obs=obs, var=var)
    adata.write_h5ad(filename)
    print(f"Mock dataset saved to {filename}")

if __name__ == "__main__":
    generate_mock_h5ad()
