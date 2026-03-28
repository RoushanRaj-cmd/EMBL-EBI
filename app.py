import streamlit as st
import scanpy as sc
import pandas as pd
import numpy as np
import os
from PIL import Image
import subprocess
import sys

# --- SELF-BOOTSTRAPPING ---
# Ensure mock data and images exist for Streamlit Cloud deployment
@st.cache_resource
def bootstrap():
    # Streamlit Cloud uses 'python' or sys.executable
    py_exec = sys.executable
    if not os.path.exists("sample_perturb.h5ad"):
        st.info("Bootstrapping mock biological data...")
        subprocess.run([py_exec, "generate_mock_data.py"])
    if not os.path.exists("mock_mave_data.csv"):
        st.info("Bootstrapping multimodal MAVE data...")
        subprocess.run([py_exec, "generate_mave_data.py"])
    if not os.path.exists("graphs_and_images/umap_perturbations.png"):
        st.info("Generating premium visualizations...")
        os.makedirs("graphs_and_images", exist_ok=True)
        subprocess.run([py_exec, "visualize_poc.py"])

bootstrap()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Perturbation-Aware LLM PoC",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🧬 GSoC 2026 PoC")
    st.subheader("Multimodal Perturbation-Aware LLM")
    st.write("EMBL-EBI Lab-in-the-Loop")
    
    navigation = st.radio(
        "Navigation",
        ["Dashboard Overview", "In Silico Query Tool", "Model Evaluation"]
    )
    
    st.divider()
    st.info("This is a Proof of Concept (PoC) demonstrating how LLMs can act as a knowledge-integration layer for causal perturbation data.")

# --- DASHBOARD OVERVIEW ---
if navigation == "Dashboard Overview":
    st.title("📊 Biological Data Dashboard")
    st.write("Explore single-cell perturbation landscapes and expression markers.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Experimental Map (UMAP)")
        img_path = "graphs_and_images/umap_perturbations.png"
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
            st.caption("UMAP latent space showing Perturbation States and Cell Lineages.")
        else:
            st.warning("UMAP visual not found. Run visualize_poc.py first.")
            
    with col2:
        st.subheader("Expression Markers")
        img_path = "graphs_and_images/marker_expression.png"
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
            st.caption("Top 10 differentially expressed markers per condition.")
        else:
            st.warning("Marker visual not found. Run visualize_poc.py first.")

    st.divider()
    st.subheader("Multimodal Dataset Summary")
    
    tab1, tab2 = st.tabs(["scPerturb-seq (Single-Cell)", "MAVE (Variant Effects)"])
    
    with tab1:
        if os.path.exists("sample_perturb.h5ad"):
            adata = sc.read_h5ad("sample_perturb.h5ad")
            st.write(f"**Total Cells:** {adata.n_obs}")
            st.write(f"**Total Genes:** {adata.n_vars}")
            st.write("**Conditions:**", ", ".join(adata.obs['condition'].unique()))
            st.write("**Cell Types:**", ", ".join(adata.obs['cell_type'].unique()))
        else:
            st.error("Mock dataset (sample_perturb.h5ad) not found.")

    with tab2:
        if os.path.exists("mock_mave_data.csv"):
            mave_df = pd.read_csv("mock_mave_data.csv")
            st.write(f"**Total Variants:** {len(mave_df)}")
            st.dataframe(mave_df, hide_index=True)
        else:
            st.error("MAVE dataset (mock_mave_data.csv) not found.")

# --- IN SILICO QUERY TOOL ---
elif navigation == "In Silico Query Tool":
    st.title("🔮 In Silico Perturbation Query")
    st.write("Predict cellular responses to unseen perturbations using the fine-tuned LLM.")
    
    with st.form("query_form"):
        col1, col2 = st.columns(2)
        with col1:
            target_gene = st.text_input("Target Gene for Perturbation", value="FOXP3")
        with col2:
            cell_type = st.selectbox("Cell Type", ["T-Cell", "B-Cell", "Macrophage", "Lung Cell"])
            
        perturb_type = st.selectbox("Perturbation Type", ["CRISPR-Cas9 Knockout", "Activation (Overexpression)", "Chemical Inhibition"])
        
        submit = st.form_submit_button("Run Prediction")
        
    if submit:
        st.divider()
        st.subheader("Model Output (Reasoning)")
        
        # Mocking LLM reasoning
        if target_gene == "FOXP3":
            st.success(f"**Predicted Response for {target_gene} {perturb_type} in {cell_type}:**")
            st.write("> Based on the Perturbation Catalogue, a FOXP3 knockout is expected to cause a loss of suppressive function and a transition toward a Th1/Th17-like phenotype, with a significant upregulation of IFNG and IL17A expression.")
            st.info("**Top Predicted Markers:** IL17A, IFNG, RORC, STAT3, IL2")
        else:
            st.markdown(f"**Prediction for `{target_gene}` {perturb_type} in `{cell_type}`:**")
            st.write(f"The model predicts a significant shift in homeostasis for {cell_type}. Downstream markers suggest an activation of stress-response pathways and altered transcriptomic signatures for metabolic regulating genes.")
            st.info(f"**Top Predicted Markers:** {target_gene}-regulated, GAPDH, MT-CO1, ACTB")

# --- MODEL EVALUATION ---
elif navigation == "Model Evaluation":
    st.title("📈 Model Performance & Reasoning Accuracy")
    st.write("Benchmarking the LLM reasoning agent against baselines.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Zero-Shot vs Fine-Tuned (Top-10 Genes)")
        img_path = "graphs_and_images/benchmark_results.png"
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
            st.caption("Comparison of Top-10 marker prediction accuracy.")
        else:
            st.warning("Benchmark visual not found.")
            
    with col2:
        st.subheader("Confusion Matrix")
        img_path = "graphs_and_images/confusion_matrix.png"
        if os.path.exists(img_path):
            st.image(img_path, width='stretch')
            st.caption("Error analysis: Predicted vs Actual Biological State.")
        else:
            st.warning("Confusion matrix visual not found.")
            
    st.divider()
    st.subheader("Scientific Verification (Gold Standard)")
    if os.path.exists("gold_standard_eval.json"):
        import json
        with open("gold_standard_eval.json", "r") as f:
            gold_std = json.load(f)
            st.table(gold_std)
    else:
        st.warning("Gold standard evaluation set not found.")
