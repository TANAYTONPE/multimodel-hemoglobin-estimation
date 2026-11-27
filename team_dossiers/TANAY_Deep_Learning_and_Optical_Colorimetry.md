# 🧬 HemoLens Multi-Model — Team Member Engineering Dossier

**Team Member**: Tanay  
**Official Project Role**: Deep Learning & Optical Colorimetric Engineer  
**Core Domain**: Deep Convolutional Latent Representations, Domain Optical Colorimetry, Biophysical Biomarker Formulation, PyTorch Training Loops & Single-Modality Regressors  
**Project**: HemoLens Multi-Model — Non-Invasive Hemoglobin Estimation  
**Repository**: `multimodel-hemoglobin-estimation`

---

## 1. 🎯 Executive Summary of Tanay's Contribution

As the **Deep Learning & Optical Colorimetric Engineer**, Tanay designed and trained the core mathematical and neural representation layer of HemoLens. 

Pure deep learning often behaves as an uninterpretable "black box" that can overfit to lighting artifacts or skin tones. Conversely, purely classical colorimetry cannot capture rich vascular micro-textures. Tanay solved this fundamental trade-off by engineering a **dual-representation feature pipeline** combining:
1. **1,280-Dimensional Deep Convolutional Representations**: Extracted from a pretrained, frozen **EfficientNet-B0** convolutional neural network backbone, capturing complex microvascular morphology, capillary distribution, and tissue spatial context.
2. **16-Dimensional Biophysical Optical Biomarkers**: Formulated using optical absorption physics (Beer-Lambert law of hemoglobin attenuation) to measure erythema, red-to-green optical attenuation, CIELAB $a^*$ (vascular chroma), CIELAB $L^*$ (tissue pallor), and HSV saturation.

### Key Responsibilities & Achievements:
- Designed the unified 1,296-dimensional feature vector ($1280\text{ deep} + 16\text{ color}$) implemented in `src/feature_extractor.py` and `src/features.py`.
- Formulated the biophysical erythema index and vascular chrominance metrics based on oxyhemoglobin ($\text{HbO}_2$) and deoxyhemoglobin ($\text{Hb}$) extinction coefficients.
- Built the PyTorch training infrastructure in `scripts/train.py` featuring Cosine Annealing learning rate schedules and patient-stratified validation.
- Trained, hyperparameter-tuned, and validated **Model 1 (Fingernail Regressor)**, **Model 2 (Skin Regressor)**, and **Model 3 (Palpebral Conjunctiva Regressor)**, achieving an exceptional **MAE of 1.392 g/dL** and $R^2 = +0.488$ on conjunctival mucosa.

---

## 2. 📁 Master Inventory of Tanay's Allotted Files

| File Path | Component Category | Key Functionality |
|---|---|---|
| `src/features.py` | Core Biomarker Library | Optical colorimetry extraction: Erythema Index, CIELAB $a^*, L^*$, $R/G$ ratio |
| `src/feature_extractor.py` | Deep Neural Backbone | Pretrained EfficientNet-B0 (1280-d) + 16-d colorimetry extractor class |
| `src/models.py` | Neural Architecture | PyTorch single-modality CNN regression heads and backbone definition |
| `scripts/train.py` | Training Pipeline | PyTorch deep learning training loop with Cosine Annealing and early stopping |
| `checkpoints/model1_fingernail.joblib` | Trained Checkpoint | Deployed Model 1 weights for fingernail bed hemoglobin estimation |
| `checkpoints/model2_skin.joblib` | Trained Checkpoint | Deployed Model 2 weights for finger skin hemoglobin estimation |
| `checkpoints/model3_conjunctiva.joblib` | Trained Checkpoint | Deployed Model 3 weights for palpebral conjunctiva hemoglobin estimation |
| `scratch_test_models.py` | Research & Ablation | Benchmark script testing Ridge, ElasticNet, Huber, SVR, and Gradient Boosting |

---

## 3. 🔍 Detailed File-by-File Breakdown

### 3.1 `src/features.py` & `src/feature_extractor.py` (The 1,296-Dimensional Feature Pipeline)
* **What Tanay Did in These Files**:
  - Implemented the singleton `CNNFeatureExtractor` class that loads pretrained EfficientNet-B0 weights, strips the classification head, and extracts 1,280-d global average pooled latent vectors.
  - Formulated and coded the 16 domain-specific optical colorimetry biomarkers in `extract_color_features()`.
  - Created erythema heatmap visualization utilities using OpenCV and Matplotlib.
* **How Tanay Did It**:
  - **EfficientNet-B0 Backbone**: Loaded `torchvision.models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)`. Replaced the final 1000-class classifier with `nn.Identity()`. Fed preprocessed $224 \times 224$ images through the convolutional feature extractor, applying adaptive average pooling to yield a compact 1,280-d latent vector.
  - **Biophysical Optical Colorimetry (16 Features)**:
    1. **Erythema Index ($\text{EI}$)**: Hemoglobin absorbs strongly in the green spectrum ($540-575\text{ nm}$) and reflects in the red spectrum ($620-750\text{ nm}$). Tanay implemented:
       $$\text{EI} = \log_{10}(R_{\text{norm}}) - \log_{10}(G_{\text{norm}})$$
    2. **Red-to-Green Ratio**: Direct optical proxy for vascular perfusion:
       $$\text{Ratio}_{R/G} = \frac{R}{G + 1.0}$$
    3. **CIELAB Chrominance ($a^*$) & Lightness ($L^*$)**: Converted RGB into device-independent CIELAB space. $a^*$ measures the red-green opponent color dimension (pure vascular hyperemia vs. pallor), while $L^*$ quantifies tissue reflectance and pallor.
    4. **Normalized Color Channels ($r, g, b$)**:
       $$r = \frac{R}{R+G+B}, \quad g = \frac{G}{R+G+B}, \quad b = \frac{B}{R+G+B}$$
    5. **HSV Color Metrics**: Hue, Saturation, and Value distributions.
  - Combined the 1,280 CNN dimensions with the 16 optical dimensions into an exact **1,296-dimensional feature vector**.
* **Connections with Tanay's Other Files**:
  - Used in `scripts/train.py` and `scratch_test_models.py` to precompute feature arrays stored in `data/cached_features/`.
* **Connections with Other Members' Files**:
  - **Jayesh (`src/preprocessing.py`, `src/roi_extractor.py`)**: Tanay ingests the $224 \times 224$ tissue crops and Gray-World normalized images generated by Jayesh.
  - **Parth (`src/models_multimodal.py`, `src/inference_pipeline.py`)**: Parth's fusion architectures directly concatenate Tanay's 1,296-d feature vectors to build multi-model ensembles.
  - **Sayee (`app.py`)**: Sayee displays Tanay's extracted optical biomarkers ($\text{EI}$, Normalized Red, $a^*$, $L^*$) in the clinical diagnostic metrics table on the Streamlit dashboard.

---

### 3.2 `src/models.py` & `scripts/train.py` (PyTorch Architectures & Deep Training Loop)
* **What Tanay Did in These Files**:
  - Architected the PyTorch deep regression models (`FingernailModel`, `SkinModel`, `ConjunctivalModel`).
  - Wrote the end-to-end training and validation loop with Cosine Annealing learning rate scheduling, Mean Squared Error ($\text{MSE}$) loss, and early stopping.
* **How Tanay Did It**:
  - **Neural Architecture**:
    ```python
    self.backbone = efficientnet_b0(weights=DEFAULT)
    self.fc = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(1280, 256),
        nn.SiLU(),
        nn.BatchNorm1d(256),
        nn.Dropout(p=0.2),
        nn.Linear(256, 1) # Direct quantitative Hb (g/dL) prediction
    )
    ```
  - **Cosine Annealing Learning Rate Schedule**: Used `torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)`. This gradually decreases the learning rate following a half-cosine curve, allowing smooth convergence to a flat minimum without oscillating around steep loss walls.
  - **Checkpointing**: Tracked validation Mean Absolute Error ($\text{MAE}$) after every epoch, automatically serializing the model state dict to `checkpoints/` only when validation loss reached a new historical best.
* **Connections with Tanay's Other Files**:
  - Trains the neural network representations that produce the model checkpoints.
* **Connections with Other Members' Files**:
  - **Jayesh (`data/metadata.csv`)**: Reads ground-truth venous hemoglobin concentrations for training supervision.
  - **Parth (`src/models_multimodal.py`)**: Parth's `TriModalHemoglobinNet` uses the structural principles and layer dimensions established by Tanay.

---

### 3.3 `checkpoints/model1_fingernail.joblib`, `model2_skin.joblib`, `model3_conjunctiva.joblib`
* **What Tanay Did in These Files**:
  - Trained and hyperparameter-tuned the three production single-modality clinical estimators on held-out patient splits.
* **How Tanay Did It**:
  - Applied regularized Ridge and ElasticNet regression with cross-validated penalty parameter $\alpha = 300.0$ and L1-ratio $0.2$. Regularization was essential to prevent overfitting given the 1,296-dimensional feature space relative to patient cohort size ($N = 250$ and $N = 201$).
  - **Model 1 (Fingernail)**: Test $\text{MAE} = 1.577\text{ g/dL}$, $R^2 = +0.356$.
  - **Model 2 (Finger Skin)**: Test $\text{MAE} = 1.797\text{ g/dL}$, $R^2 = +0.059$.
  - **Model 3 (Conjunctiva)**: Test $\text{MAE} = 1.392\text{ g/dL}$, $R^2 = +0.488$ (the strongest single anatomical modality in the project).
* **Connections with Other Members' Files**:
  - **Parth (`src/inference_pipeline.py`)**: Parth loads these three `.joblib` checkpoints in `HemoglobinInferenceEngine._load_available_models()` and runs them in parallel.
  - **Sayee (`app.py`, `generate_metrics.py`)**: Sayee benchmarks these three models against the JMIR 2026 published research paper.

---

### 3.4 `scratch_test_models.py` (Machine Learning Exploration & Ablation)
* **What Tanay Did in This File**:
  - Ran systematic machine learning algorithm benchmarks comparing Ridge, ElasticNet, Huber Robust Regressor, Support Vector Regression ($\text{SVR}$ with RBF kernel), ExtraTrees, and Gradient Boosting.
* **How Tanay Did It**:
  - Evaluated cross-validated $\text{MAE}$, $\text{RMSE}$, and Pearson $r$. Confirmed that L2-regularized linear Ridge regression with $\alpha = 300.0$ achieved the best generalization and lowest variance on held-out medical test patients, avoiding the extreme overfitting seen in unregularized gradient boosted trees.
* **Connections with Other Members' Files**:
  - **Sayee (`generate_metrics.py`)**: Provided the baseline experimental logs that Sayee compiled into the master performance comparison tables.

---

## 4. 🔄 Cross-Team Collaboration & Dependency Map

```mermaid
flowchart LR
    J["JAYESH\n(Preprocessed Crops\n& Gray-World WB)"] --> T["TANAY\n(EfficientNet-B0 1280d +\nOptical Colorimetry 16d)"]
    T --> M["TANAY: Trained Models\n(Model 1, Model 2, Model 3)"]
    M --> P["PARTH\n(Multi-Model Fusion Head\n& Consensus Engine)"]
    P --> S["SAYEE\n(Streamlit UI, Plots\n& Research Dossier)"]
```

---

## 5. 🎓 Tanay's Viva / Defense Questions & Model Answers

### Q1: "Why did you use frozen EfficientNet-B0 weights instead of training a CNN from scratch?"
> **Tanay's Answer**: "Our clinical cohorts consist of $N = 250$ hand subjects and $N = 201$ eye subjects. A standard deep convolutional network has over 4 to 20 million trainable parameters. Training a deep CNN from scratch on a medical dataset of hundreds of subjects causes immediate catastrophic overfitting—the network memorizes skin freckles, wrinkles, and background noise rather than hemoglobin absorption. By using an EfficientNet-B0 pretrained on ImageNet and freezing its convolutional feature extractor, we transfer robust spatial low- and mid-level microvascular filters without overfitting. We then train a low-capacity regularized regression head on the extracted 1,280-d latent representations."

### Q2: "What is the physical basis of the Erythema Index ($\text{EI}$) you implemented in `src/features.py`?"
> **Tanay's Answer**: "The Erythema Index is derived directly from the **Beer-Lambert law of optical absorption**:
> $$I = I_0 \cdot 10^{-\epsilon(\lambda) \cdot c \cdot d}$$
> Oxygenated hemoglobin ($\text{HbO}_2$) and deoxygenated hemoglobin ($\text{Hb}$) have strong optical absorption peaks in the green spectrum ($\lambda \approx 540\text{ nm}$ and $575\text{ nm}$), whereas optical absorption in the red spectrum ($\lambda > 620\text{ nm}$) is drastically lower. Therefore, as hemoglobin concentration increases, green light reflectance drops relative to red light reflectance. By formulating:
> $$\text{EI} = \log_{10}(R_{\text{norm}}) - \log_{10}(G_{\text{norm}})$$
> we create a logarithmic absorption proxy that linearly scales with the blood volume and hemoglobin concentration in microvascular capillary beds."

### Q3: "Why did Model 3 (Conjunctiva) achieve a significantly better MAE ($1.39\text{ g/dL}$) than Model 2 (Skin: $1.80\text{ g/dL}$)?"
> **Tanay's Answer**: "This difference is biophysically grounded in human skin anatomy. Cutaneous skin tissue contains an epidermal layer rich in **melanin** (eumelanin and pheomelanin), which has a broad, non-specific absorption spectrum that confounds and attenuates the microvascular hemoglobin absorption signal. In contrast, the **palpebral conjunctiva** of the lower inner eyelid is a thin, completely unpigmented mucous membrane fed directly by branches of the ophthalmic and internal carotid arteries. Because there is zero melanin interference, the light penetrates directly into the sub-epithelial capillary plexus, giving Model 3 the highest signal-to-noise ratio and tightest linear correlation ($r = 0.706, p < 0.0001$) with systemic venous blood hemoglobin."
