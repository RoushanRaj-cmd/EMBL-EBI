# Blog Post: The Lab-in-the-Loop – How LLMs are Mastering Biological Perturbations

**By Roushan Raj | GSoC 2026 Applicant for EMBL-EBI**

Imagine a world where a biologist can ask their computer: *"What happens to a T-cell if I knock out FOXP3 and simultaneously inhibit STAT3?"* and receive not just a list of numbers, but a reasoned, pathway-grounded prediction. 

This is the vision of the **Perturbation-Aware LLM**, my project for GSoC 2026.

### Bridging the Gap
Single-cell data is exploding, but it often stays locked in matrices. By using a "Cell-to-Sentence" approach, we translate these matrices into the language of foundation models. Suddenly, the model isn't just seeing numbers; it's seeing biological concepts and their relationships.

### Multimodal Power
Our prototype doesn't stop at RNA-seq. By integrating data from the **Perturbation Catalogue**, including CRISPR screens and MAVE variants, we're building a truly multimodal knowledge layer. This project supports the emerging "Virtual Cell" and "Lab-in-the-Loop" paradigms, where AI guides the next experiment.

### Ready for the Future
With a working Proof-of-Concept, a robust fine-tuning pipeline, and an interactive dashboard, I'm excited to contribute to EMBL-EBI's mission of making biological knowledge accessible and causal.

*Check out the live PoC here:* [https://embl-ebi-roushan.streamlit.app](https://embl-ebi-roushan.streamlit.app)
