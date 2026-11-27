# HemoLens Multi-Model - Presentation Script (Tanay)

> *Tip for Tanay*: Use this document as your speaking guide during project presentations, reviews, and viva voce. It covers your deep learning representation learning, the biophysical formulation of 16 optical colorimetric biomarkers based on the Beer-Lambert law, single-modality model training, and the scientific discovery of the palpebral conjunctiva as the optimal optical window.

---

## 1. Introduction 

*"Hello everyone, my name is Tanay, and I architected the deep convolutional representation learning, optical colorimetric feature engineering, and single-modality model training for the HemoLens Multi-Model framework."*

"In non-invasive medical imaging, deep neural networks are frequently treated as opaque black boxes that output numbers without physical justification. However, in optical hematology, photon-tissue interaction is governed by well-established laws of physics. If you do not ground your machine learning architecture in biophysical optical absorption, your models will memorize spurious camera artifacts instead of true blood physiology."

"Over the course of my engineering work, I bridged physical optics and deep representation learning spanning 5 core files. My primary goals were:"
1. Formulating 16 biophysical colorimetric biomarkers rooted in the Beer-Lambert law of optical absorption across RGB, HSV, and CIELAB color spaces.
2. Developing transfer learning architectures using deep EfficientNet-B0 backbones to extract 1,280-dimensional microvascular latent embeddings.
3. Training and optimizing individual single-modality regressors (Models 1, 2, and 3) for the fingernail bed, finger skin, and palpebral conjunctiva.
4. Discovering and proving empirically that the unpigmented palpebral conjunctiva provides the cleanest optical window into systemic hemoglobin ($r = 0.706, p < 0.0001$), overcoming the melanin confounding factor.

"I will now explain how these biophysical features and neural networks extract true blood hemoglobin signals from smartphone pixels."

---

## 2. Biophysical Optical Colorimetry Engine (`src/feature_extraction.py`)

*"Everything in optical colorimetry begins with the Beer-Lambert law of light absorption. In `src/feature_extraction.py`, I engineered 16 domain-specific optical features."*

*   *The Biophysics of Hemoglobin Absorption:* Blood hemoglobin exists in two primary states: oxygenated hemoglobin ($\text{HbO}_2$) and deoxygenated hemoglobin ($\text{Hb}$). Both molecules exhibit intense optical absorption bands (the *Q-bands*) in the green spectral region between $540\text{ nm}$ and $575\text{ nm}$, while absorbing substantially less light in the red spectral band ($\sim 650\text{ nm}$). Consequently, as capillary blood hemoglobin concentration increases, tissue absorbs more green photons while reflecting red photons back to the camera sensor.
*   *Erythema Index ($EI$):* Grounded in logarithmic optical attenuation, I formulated the Erythema Index:
    $$EI = \log_{10}(R) - \log_{10}(G)$$
    This quantifies the differential absorption between the red and green spectral bands, directly tracking microvascular blood perfusion independent of absolute lighting intensity.
*   *Hemoglobin Index ($HI$):* I implemented the normalized ratio:
    $$HI = \frac{R - G}{R + G}$$
    This bounded index isolates capillary redness while neutralizing broad-spectrum illumination fluctuations.
*   *CIELAB Perceptual Color Space ($a^*$ Redness):* Unlike RGB where color and illumination are entangled, the CIELAB space separates perceptual luminance ($L^*$) from chromaticity. The $a^*$ channel represents the green-to-red axis ($+a^* = \text{redness}$). I extracted the mean and standard deviation of $a^*$ across segmented tissue regions, capturing true microvascular erythema.
*   *Normalized Chromaticity Coordinates:* I computed illumination-invariant coordinates:
    $$r = \frac{R}{R + G + B}, \quad g = \frac{G}{R + G + B}, \quad b = \frac{B}{R + G + B} \quad (\text{such that } r + g + b = 1.0)$$
    These ratios eliminate light intensity shadows caused by uneven smartphone flash angles.

---

## 3. Deep Transfer Learning with EfficientNet-B0 (`src/models.py`)

*"Handcrafted color features capture macroscopic tissue redness, but microvascular structure has microscopic textures that linear equations miss. I built deep convolutional encoders to capture these latent patterns."*

*   *Compound Scaling Architecture:* I selected EfficientNet-B0 as our visual backbone. Unlike standard ResNets that uniformly scale only depth, EfficientNet utilizes compound scaling to uniformly scale depth, channel width, and input image resolution ($224 \times 224$). This delivers superior parameter efficiency: 5.3 million parameters compared to ResNet-50's 25.6 million parameters, preventing overfitting on clinical sample cohorts.
*   *1,280-Dimensional Latent Visual Embeddings:* I truncated the classification head and attached a Global Average Pooling (GAP) layer directly to the terminal convolutional stage:
    $$\mathbf{x} \in \mathbb{R}^{3 \times 224 \times 224} \xrightarrow{\text{EfficientNet-B0 Backbone}} \mathbf{F} \in \mathbb{R}^{1280 \times 7 \times 7} \xrightarrow{\text{Global Avg Pooling}} \mathbf{z} \in \mathbb{R}^{1280}$$
    These 1,280 continuous embeddings encode microscopic capillary loops, subungual vascular beds, and subtle tissue pallor.
*   *Regularization & Stability:* To ensure robust training across small medical cohorts, I incorporated Dropout ($p = 0.2 - 0.3$), Batch Normalization, Swish ($\text{SiLU}$) activation functions, and L2 weight decay ($10^{-4}$).

---

## 4. Single-Modality Optimization & The Conjunctiva Discovery (`scripts/train.py`)

*"Once the feature pipelines were established, I trained and evaluated individual models for each anatomical site in `scripts/train.py`. This led to the central scientific finding of our research."*

*   *Single-Modality Performance Breakdown:*
    - **Model 1 (Fingernail Bed Regressor):** $\text{MAE} = 1.638\text{ g/dL}, R^2 = 0.286$.
    - **Model 2 (Finger Skin Regressor):** $\text{MAE} = 1.745\text{ g/dL}, R^2 = 0.208$.
    - **Model 3 (Palpebral Conjunctiva Regressor):** $\mathbf{\text{MAE} = 1.392\text{ g/dL}, R^2 = +0.488}$.
*   *The Conjunctiva Breakthrough ($r = 0.706, p < 0.0001$):* Model 3 demonstrated overwhelming statistical superiority, explaining nearly 50% of systemic blood hemoglobin variance alone ($R^2 = 0.488$) with a Pearson correlation of $r = 0.706$.
*   *The Biophysical Explanation (Overcoming Melanin):* 
    - Human skin and nail folds contain variable concentrations of eumelanin and pheomelanin in the epidermal stratum basale. Melanin is a broadband light absorber that directly competes with hemoglobin absorption, severely confounding optical readings in darker skin tones (Fitzpatrick types IV-VI).
    - In stark contrast, the palpebral conjunctiva (the inner mucous membrane of the lower eyelid) contains **zero melanocytes** and an extremely thin, non-keratinized epithelial layer. It provides an unobstructed, melanin-free optical window directly into subepithelial microvascular capillary beds.

---

## 5. Training Routine & Optimization Pipeline (`scripts/extract_conjunctiva_features.py`)

*"To train these models reliably without data leakage or overfitting, I engineered dedicated training routines."*

*   *Feature Caching & High-Throughput Pipeline:* Extracting 1,280 deep embeddings per image across hundreds of patients is computationally expensive. In `scripts/extract_conjunctiva_features.py`, I created an automated batch caching pipeline that pre-computes and serializes feature vectors into structured NumPy arrays, accelerating model training and cross-validation by $50\times$.
*   *Smooth L1 (Huber) Regression Loss:* Clinical reference values from venous blood draws can contain measurement outliers ($\pm 0.5\text{ g/dL}$). Instead of Mean Squared Error ($\text{MSE}$) which squares outlier errors and destabilizes gradients, I utilized Smooth L1 loss:
    $$L_{\delta}(y, \hat{y}) = \begin{cases} 0.5 (y - \hat{y})^2 & \text{if } |y - \hat{y}| < 1 \\ |y - \hat{y}| - 0.5 & \text{otherwise} \end{cases}$$
    This provides quadratic convergence near zero while maintaining linear robustness against measurement noise.
*   *AdamW Optimization:* Trained using the AdamW optimizer with decoupled weight decay and cosine annealing learning rate schedules.

---

## 6. Closing (Tying it to the App & Team)

*"To wrap up, my deep learning and optical colorimetry engineering provides the physiological intelligence inside HemoLens:"*
1. It processes *Jayesh's* standardized, glare-free, and Gray-World balanced $224 \times 224$ tissue crops through our Beer-Lambert colorimetric extraction formulas.
2. It feeds trained model checkpoints (Models 1, 2, and 3), 1,280-dimensional CNN embeddings, and empirical variance calibrations ($\sigma_m$) into *Parth's* Model 6 Bayesian Consensus Engine.
3. It enables *Sayee's* Streamlit clinical dashboard to render live, interpretable biomarker breakdowns (Erythema Index, Hemoglobin Index, CIELAB $a^*$) and powers the scientific superiority documented in our JMIR comparative benchmark.

*"By bridging biophysical optical principles with modern deep learning representations, we transformed smartphone cameras into precision non-invasive hemoglobin sensors."*

---
*(End of Script)*
