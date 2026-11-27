# 📋 ANNEXURE: INDIVIDUAL STUDENT CONTRIBUTIONS

### Project Title: HemoLens Multi-Model — Non-Invasive Hemoglobin Estimation
**Academic Year**: 2025–2026  
**Repository**: `multimodel-hemoglobin-estimation`

---

## 🎯 Summary Annexure Table

| Student Name | Roll Number | Contribution |
|:---|:---:|:---|
| **Parth Diwale** | **B - 41** | Multi-model latent feature fusion, Three-Branch deep neural network architecture (TriModalNet), inverse-variance precision-weighted Bayesian consensus engine, singleton production inference manager (`HemoglobinInferenceEngine`), WHO clinical anemia diagnostic tier classification, and production CLI prediction tool. |
| **Sayee Deshmukh** | **B - 61** | Interactive Streamlit clinical web dashboard development, point-of-care mobile camera integration, comparative benchmark evaluation vs. JMIR 2026 state-of-the-art research paper (Bland-Altman 95% LoA, ROC-AUC, sensitivity/specificity), 29-test automated QA test harness, and cloud deployment configuration. |
| **Tanay Tonpe** | **B - 65** | Pretrained EfficientNet-B0 deep convolutional feature extraction (1,280-d), 16-d domain optical colorimetry formulation (Erythema Index, CIELAB $a^*, L^*$, $R/G$ attenuation ratio), PyTorch deep training pipeline with Cosine Annealing learning rate scheduling, and single-modality regression models (Models 1, 2, and 3). |
| **Jayesh Jumde** | **B - 10** | Digital image preprocessing, Gray-World chromatic constancy illuminant filter, dynamic tissue ROI localization & contour segmentation (fingernail bed, finger skin, palpebral conjunctiva), Laplacian focus/blur quality auditing, specular reflection glare masking, dual-cohort clinical dataset ingestion, and master manifest management. |

---

## 📑 Detailed Breakdown of Individual Student Contributions

### 1. Parth Diwale (Roll No: B - 41)
* **Designated Role**: Multi-Model Fusion & Core Inference System Engineer
* **Allotted Modules & Checkpoints**:
  - `src/models_multimodal.py`
  - `src/inference_pipeline.py`
  - `src/inference.py`
  - `scripts/predict.py`
  - `test_engine.py`
  - `checkpoints/model4_nail_skin_fusion.joblib`
  - `checkpoints/model5_nail_conj_fusion.joblib`
  - `checkpoints/model6_tri_modal.pth`
* **Specific Technical Contributions**:
  1. **Multi-Model Latent Fusion (Model 4 & 6)**: Formulated the mathematical feature concatenation strategy combining independent tissue embeddings into a 2,592-d dual-branch vector and 3,888-d tri-modal space.
  2. **TriModalHemoglobinNet (PyTorch)**: Implemented the three-branch deep convolutional PyTorch neural network that processes Nail, Skin, and Eye representations simultaneously through parallel private projection layers ($1296 \to 128$) and a dense fusion head.
  3. **Precision-Weighted Bayesian Consensus Engine**: Designed an empirical inverse-variance weighting algorithm that fuses estimates across tissue sites based on historical validation error: Conjunctiva ($49.4\%$), Fingernail ($30.1\%$), and Skin ($20.5\%$), mathematically minimizing prediction variance.
  4. **Production Inference Engine (`HemoglobinInferenceEngine`)**: Created the singleton inference manager supporting automated model artifact discovery, Gray-World illumination correction, and World Health Organization (WHO) clinical diagnostic stratification (Normal, Mild, Moderate, Severe Anemia).
  5. **Command-Line Inference Tool (`scripts/predict.py`)**: Built the terminal utility supporting single and multi-model predictions with JSON output for automated batch execution.

---

### 2. Sayee Deshmukh (Roll No: B - 61)
* **Designated Role**: Full-Stack Development, Evaluation & Research Benchmark Engineer
* **Allotted Modules & Documentation**:
  - `app.py` & `app_streamlit.py`
  - `generate_paper_comparison_plots.py`
  - `generate_metrics.py`
  - `generate_pdf_dossier.py`
  - `scripts/train_evaluate_all.py`
  - `scripts/generate_modality_distribution_chart.py`
  - `scratch_evaluate.py`
  - `tests/test_system.py` & `tests/test_pipeline.py`
  - `requirements.txt`, `packages.txt`, `setup.py`, `README.md`
* **Specific Technical Contributions**:
  1. **Interactive Clinical Web Dashboard (`app.py`)**: Engineered the responsive dark-slate Streamlit interface featuring a compulsory 3-modality patient image acquisition workflow, real-time ROI bounding box visualizer, and 1-click clinical test cases (*Verified Normal* vs *Verified Anemic*).
  2. **Point-of-Care Mobile Integration**: Configured camera upload inputs that seamlessly launch native smartphone cameras on iOS and Android devices, allowing real-time clinical triage.
  3. **Comparative Benchmark vs. JMIR 2026 Study**: Programmed the statistical evaluation benchmarking HemoLens directly against the published research paper by *Zuccotti et al. (JMIR Form Res 2026)*, proving:
     - **$\sim 6\times$ Higher Linear Correlation**: Pearson $r = 0.706$ vs. $0.120$ ($p < 0.0001$).
     - **$\sim 11\times$ Higher Clinical Sensitivity**: $69.2\%$ vs. $6.4\%$ (catching $11\times$ more anemic patients).
     - **31% Tighter Error Span**: Bland-Altman 95% Limits of Agreement span of $6.63\text{ g/dL}$ vs. $9.68\text{ g/dL}$.
  4. **Automated QA Test Suite (`tests/`)**: Built the 29-test automated test harness covering tensor dimensions, ROI extractors, model checkpoints, and edge-case exceptions (all passing in ~7.8s).
  5. **Cloud Deployment Configuration**: Authored `packages.txt` (`libgl1`, `libglib2.0-0`) and `requirements.txt` ensuring zero-friction deployment to Streamlit Community Cloud.

---

### 3. Tanay Tonpe (Roll No: B - 65)
* **Designated Role**: Deep Learning & Optical Colorimetric Engineer
* **Allotted Modules & Checkpoints**:
  - `src/features.py`
  - `src/feature_extractor.py`
  - `src/models.py`
  - `scripts/train.py`
  - `checkpoints/model1_fingernail.joblib`
  - `checkpoints/model2_skin.joblib`
  - `checkpoints/model3_conjunctiva.joblib`
  - `scratch_test_models.py`
* **Specific Technical Contributions**:
  1. **1,296-Dimensional Feature Representation**: Developed the unified feature extractor combining 1,280 deep CNN latent representations with 16 biophysical optical colorimetry biomarkers.
  2. **Pretrained EfficientNet-B0 Backbone**: Loaded ImageNet-pretrained weights, removed classification layers, and extracted global average pooled microvascular spatial feature embeddings.
  3. **Biophysical Colorimetry Biomarkers**: Formulated optical attenuation proxies based on the Beer-Lambert law of hemoglobin absorption:
     - **Erythema Index ($\text{EI}$)**: $\text{EI} = \log_{10}(R_{\text{norm}}) - \log_{10}(G_{\text{norm}})$
     - **CIELAB Vascular Redness ($a^*$) and Lightness ($L^*$)**: Capturing microvascular hyperemia and tissue pallor independent of camera sensor color temperature.
     - **Normalized RGB Ratios**: Calculating spectral absorption differences between oxygenated and deoxygenated hemoglobin.
  4. **Deep Training Architecture (`scripts/train.py`)**: Designed the PyTorch training pipeline incorporating Cosine Annealing learning rate schedules and historical validation loss checkpointing.
  5. **Single-Modality Regressor Training**: Trained and cross-validated **Model 1 (Nail)** ($\text{MAE} = 1.58\text{ g/dL}$), **Model 2 (Skin)** ($\text{MAE} = 1.80\text{ g/dL}$), and **Model 3 (Conjunctiva)** ($\text{MAE} = 1.39\text{ g/dL}$, $R^2 = +0.488$).

---

### 4. Jayesh Jumde (Roll No: B - 10)
* **Designated Role**: Computer Vision & Data Ingestion Engineer
* **Allotted Modules & Datasets**:
  - `src/preprocessing.py`
  - `src/roi_extractor.py`
  - `scripts/ingest_eyes_dataset.py`
  - `scripts/extract_conjunctiva_features.py`
  - `analyze_dataset.py`
  - `data/metadata.csv`
  - `data/dataset_manifest.csv`
  - `data/conjunctiva_manifest.csv`
* **Specific Technical Contributions**:
  1. **Dynamic Vascular ROI Extraction (`src/roi_extractor.py`)**: Built automated tissue segmentation detectors in OpenCV using adaptive HSV color thresholding, contour hierarchy, and aspect ratio filtering to isolate the subungual nail bed and palpebral conjunctival mucosa.
  2. **Gray-World Chromatic Constancy Filter (`src/preprocessing.py`)**: Implemented the mathematical illuminant normalization algorithm:
     $$R' = R \cdot \frac{\mu}{\mu_R}, \quad G' = G \cdot \frac{\mu}{\mu_G}, \quad B' = B \cdot \frac{\mu}{\mu_B}$$
     neutralizing ambient room lighting temperature (3000K warm vs. 6500K cool light) to prevent false-positive hyperemia or pseudo-anemic pallor.
  3. **Biophysical Image Quality Auditing**: Programmed an automated 2D Laplacian focus variance filter ($\text{Var}(\nabla^2 I)$) to detect motion blur and an overexposure mask to reject specular flash reflections ($R, G, B > 245$).
  4. **Clinical Dataset Ingestion & Preprocessing**: Ingested and structured 451 clinical subjects across two international cohorts (*Nature Scientific Data* for nails/skin, and *Eyes-defy-anemia* for Italy and India eye cohorts).
  5. **Patient-Independent Partitioning**: Curated master manifests establishing strict patient-level separation across Train ($70\%$), Validation ($15\%$), and Test ($15\%$) sets, guaranteeing zero data leakage between finger crops of the same subject.
