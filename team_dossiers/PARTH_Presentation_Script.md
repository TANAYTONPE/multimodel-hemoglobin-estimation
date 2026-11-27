# HemoLens Multi-Model - Presentation Script (Parth)

> *Tip for Parth*: Use this document as your speaking guide during project presentations, reviews, and viva voce. It covers the multi-model decision architecture, the Bayesian uncertainty-weighted consensus engine, deep TriModalNet intermediate feature fusion, singleton inference latency optimization, and WHO clinical triage classification.

---

## 1. Introduction 

*"Hello everyone, my name is Parth, and I architected the multi-model fusion algorithms, deep neural network integration, and core clinical inference engine for the HemoLens framework."*

"In non-invasive optical hematology, relying on any single biological site is fundamentally vulnerable. If you only look at the fingernails, thick nail plates, nail polish, or peripheral vasoconstriction from cold hands can distort the signal. If you only look at the skin, differences in epidermal melanin and Fitzpatrick skin phototypes create confounding absorption. And if you only inspect the eyes, sudden tear film reflections or patient blinking can degrade quality."

"To solve this, our project's fundamental breakthrough is Multi-Model Fusion. Over the course of my engineering work, I owned the fusion mathematics, deep neural network architecture, and real-time inference pipeline across 6 core files. My primary goals were:"
1. Formulating a Bayesian uncertainty-weighted consensus engine that dynamically weights each anatomical tissue by its empirical inverse variance.
2. Engineering TriModalNet, a deep PyTorch neural network that performs intermediate feature fusion across three parallel EfficientNet-B0 backbones.
3. Building a high-throughput, singleton inference engine (`src/inference.py`) capable of executing multi-model predictions in under 2 seconds.
4. Implementing automated clinical decision support that maps continuous hemoglobin estimates to World Health Organization (WHO) diagnostic tiers with critical transfusion referral alerts.

"I will now explain how these components fit together to deliver an accurate, robust clinical prediction."

---

## 2. The Singleton Clinical Inference Engine (`src/inference.py`)

*"Everything comes together in `src/inference.py`. I engineered `HemoglobinInferenceEngine` to act as the centralized orchestrator connecting sensory inputs to our models."*

*   *Singleton Architecture & Memory Management:* In medical deployment, loading deep neural network weights into memory on every patient query creates unacceptable latency and memory leaks. I designed the engine as a cached singleton. When initialized, it lazy-loads all six trained model weight files—including our PyTorch TriModalNet and scikit-learn regressors—holding them warm in memory for instantaneous execution.
*   *End-to-End Orchestration:* The engine exposes a clean, high-level API: `engine.predict(nail_img, eye_img, skin_img)`. Internally, it coordinates the entire pipeline:
    1. It delegates raw patient photos to Jayesh's `roi_extractor.py` to crop microvascular tissues and apply Gray-World white balancing.
    2. It executes Tanay's `feature_extraction.py` to extract 16 biophysical colorimetric features and 1,280 deep CNN embeddings per tissue.
    3. It feeds these representations into our single-modality models and multi-model consensus fusion.
*   *Fault-Tolerant Dynamic Fallback:* In real-world clinics, a patient might have an eye injury or an amputated digit, making 3-tissue acquisition impossible. I built dynamic fallback handlers into the inference loop: if a user submits only two modalities, the engine gracefully detects the missing input, recalculates consensus weights over the available tissues, and flags a warning without crashing.

---

## 3. Bayesian Uncertainty-Weighted Consensus Engine (`src/model_fusion.py`)

*"The mathematical heart of HemoLens is Model 6: the Bayesian Consensus Engine that I formulated in `src/model_fusion.py`."*

*   *Inverse Variance Formulation:* A naive approach to multi-model estimation is simple arithmetic averaging: $(\text{Hb}_1 + \text{Hb}_2 + \text{Hb}_3) / 3$. However, treating an erratic model identically to a highly accurate model degrades performance. I applied the statistical principle of Maximum A Posteriori (MAP) estimation under Gaussian assumptions:
    $$\hat{\text{Hb}}_{\text{consensus}} = \sum_{m \in \{\text{nail}, \text{eye}, \text{skin}\}} w_m \cdot \hat{\text{Hb}}_m \quad \text{where} \quad w_m = \frac{1 / \sigma_m^2}{\sum_k 1 / \sigma_k^2}$$
*   *Empirically Derived Modality Weights:* From extensive cross-validation on our held-out test cohort, the model standard deviations are:
    - Palpebral Conjunctiva: $\sigma = 1.83\text{ g/dL} \implies w_{\text{eye}} = \mathbf{49.4\%}$
    - Fingernail Bed: $\sigma = 2.35\text{ g/dL} \implies w_{\text{nail}} = \mathbf{30.1\%}$
    - Finger Skin: $\sigma = 2.85\text{ g/dL} \implies w_{\text{skin}} = \mathbf{20.5\%}$
    Because the conjunctiva has no melanocytes and minimal keratin, the Bayesian engine automatically assigns it nearly half the total decision weight.
*   *Statistical Uncertainty & 95% Confidence Intervals:* Clinicians need to know not just the estimate, but the model's confidence. I derived the combined standard error:
    $$\text{SE} = \sqrt{\frac{1}{\sum_k 1 / \sigma_k^2}} \approx 1.28\text{ g/dL}$$
    This produces rigorous 95% Confidence Intervals: $[\hat{\text{Hb}} \pm 1.96 \cdot \text{SE}]$, displayed directly to the clinician.
*   *Explainable Diagnostic Contributions:* The engine outputs the exact percentage contribution of each tissue site for every patient, giving clinicians complete interpretability rather than a black-box output.

---

## 4. Deep Intermediate Feature Fusion (`src/models.py` - `TriModalNet`)

*"Beyond statistical post-hoc fusion, I engineered Model 5: TriModalNet, an end-to-end deep neural network that fuses latent anatomical features inside the network itself."*

*   *Tri-Stream Neural Architecture:* TriModalNet instantiates three parallel convolutional branches using pre-trained EfficientNet-B0 backbones. Each branch receives a standardized $224 \times 224 \times 3$ crop of a different anatomical site (nail, conjunctiva, skin).
*   *Latent Concatenation (3,840-Dimensional Representation):* The final global average pooling layers from each branch are concatenated into a joint 3,840-dimensional multimodal embedding vector:
    $$\mathbf{z}_{\text{joint}} = [\mathbf{z}_{\text{nail}} \,\|\, \mathbf{z}_{\text{eye}} \,\|\, \mathbf{z}_{\text{skin}}] \in \mathbb{R}^{3840}$$
*   *Non-Linear Fusion Head:* This dense joint embedding passes through an MLP fusion block:
    $$\mathbb{R}^{3840} \xrightarrow{\text{Dense + SiLU + Drop(0.3)}} \mathbb{R}^{512} \xrightarrow{\text{Dense + SiLU + Drop(0.2)}} \mathbb{R}^{128} \xrightarrow{\text{Linear}} \mathbb{R}^1$$
    This architecture enables the network to learn complex cross-tissue non-linear interactions—for instance, distinguishing between systemic pallor (which affects all three tissues simultaneously) versus localized peripheral cold-induced vasoconstriction (which only affects fingers).
*   *Ensemble Regressors:* Alongside the deep network, I developed L2-regularized Ridge, Lasso, and Gradient Boosting regressors in `src/models.py` with cross-validated hyperparameter tuning ($\alpha = 10.0$) to benchmark against linear baselines.

---

## 5. Clinical Triage Decision Logic & WHO Severity Stratification

*"A quantitative hemoglobin number must be translated into actionable medical decisions. I implemented the World Health Organization (WHO) clinical diagnostic logic."*

*   *Stratified Clinical Alert Tiers:*
    - **Normal** ($\text{Hb} \ge 12.0\text{ g/dL}$): Renders green reassurance badge indicating adequate oxygen carrying capacity.
    - **Mild Anemia** ($10.0 \le \text{Hb} < 12.0\text{ g/dL}$): Renders yellow warning with dietary counseling recommendations.
    - **Moderate Anemia** ($7.0 \le \text{Hb} < 10.0\text{ g/dL}$): Renders orange clinical alert recommending oral iron supplementation and physician consultation.
    - **Severe Anemia** ($\text{Hb} < 7.0\text{ g/dL}$): Renders a prominent red alert with an urgent **Emergency Blood Transfusion Referral Alert**.
*   *Empirical Accuracy:* Model 6 achieves a state-of-the-art Mean Absolute Error of **$1.39\text{ g/dL}$** across all test subjects, delivering the stability required for non-invasive community screening.

---

## 6. Closing (Tying it to the App & Team)

*"To wrap up, my fusion architecture and inference engineering serve as the central mathematical bridge of HemoLens:"*
1. It ingests *Jayesh's* automated tissue bounding boxes and Gray-World color-balanced crops, ensuring the models receive standardized inputs.
2. It synthesizes *Tanay's* deep EfficientNet feature representations and 16 optical colorimetric biomarkers across all three anatomical modalities.
3. It powers *Sayee's* Streamlit clinical dashboard with a lightning-fast, synchronous prediction API that delivers quantitative hemoglobin, confidence intervals, contribution percentages, and WHO triage badges in under 2 seconds.

*"By uniting three distinct biological windows through Bayesian consensus fusion, we achieved an accuracy and clinical reliability that no single-tissue model could ever match alone."*

---
*(End of Script)*
