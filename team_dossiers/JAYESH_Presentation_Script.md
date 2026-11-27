# HemoLens Multi-Model - Presentation Script (Jayesh)

> *Tip for Jayesh*: Use this document as your speaking guide during project presentations, reviews, and viva voce. It covers the foundation of the optical pipeline that you built, emphasizing automated vascular ROI localization, Gray-World illumination normalization, biophysical focus/glare quality auditing, and clinical cohort curation.

---

## 1. Introduction 

*"Hello everyone, my name is Jayesh, and I architected the computer vision, tissue ROI extraction, and clinical data ingestion infrastructure for the HemoLens Multi-Model framework."*

"When building a non-invasive optical screening platform where blood hemoglobin is estimated purely from smartphone digital photography, image quality and tissue localization cannot be an afterthought. An AI model is only as reliable as the biological pixels fed into it. If an input image is out of focus, blinded by flash glare, distorted by warm room lighting, or cropped incorrectly, even the deepest neural network will output medically dangerous predictions."

"Over the course of my engineering work, I laid the foundational sensory and computer vision architecture spanning 8 core files and 1,701 standardized tissue crops. My primary goals were:"
1. Designing an automated, dynamic Region of Interest (ROI) localization engine for fingernails, skin, and palpebral conjunctiva.
2. Formulating a mathematical Gray-World chromatic constancy filter to eliminate smartphone sensor and ambient room lighting drift.
3. Implementing an automated biophysical quality auditing gatekeeper that detects motion blur and masks out specular flash reflections.
4. Ingesting, harmonizing, and structuring 451 clinical patients across two international cohorts into patient-independent manifests.

"I will now walk you through how these components work together to deliver pristine, calibrated biological inputs to our models."

---

## 2. Gray-World Chromatic Constancy & Preprocessing (`src/preprocessing.py`)

*"Everything in optical colorimetry depends on color integrity. In `src/preprocessing.py`, I solved the ambient lighting problem that causes most mobile health apps to collapse."*

*   *The Ambient Lighting Confounder:* If a patient takes a photo in a clinic under warm tungsten bulbs (3000K), the tissue looks artificially red, which naive models misinterpret as elevated hemoglobin (hyperemia). Under cool daylight (6500K), the tissue appears pale, falsely mimicking severe anemia.
*   *The Mathematical Normalization:* Under the Gray-World assumption, the average reflectance in a natural scene is achromatic gray. I implemented an automated channel-wise scaling algorithm:
    $$\mu = \frac{\mu_R + \mu_G + \mu_B}{3}, \quad R' = R \cdot \frac{\mu}{\mu_R}, \quad G' = G \cdot \frac{\mu}{\mu_G}, \quad B' = B \cdot \frac{\mu}{\mu_B}$$
    This dynamically normalizes color temperature variations, guaranteeing that the redness we measure reflects real capillary perfusion rather than the room's lightbulbs.
*   *Color-Preserving Augmentations:* In standard computer vision, developers apply random hue jitter or convert images to grayscale to prevent overfitting. In optical hematology, color IS the medical signal. I strictly eliminated hue and saturation jitter in our PyTorch `HemoglobinDataset`, restricting augmentations solely to spatial affine transforms (random rotations and horizontal flips), preserving the physical Beer-Lambert absorption properties of hemoglobin.

---

## 3. Dynamic Vascular ROI Extraction Engine (`src/roi_extractor.py`)

*"Next, we cannot expect doctors or rural health workers to manually crop fingernails or inner eyelids. I built automated localization algorithms that pinpoint microvascular tissue in seconds."*

*   *Fingernail Bed & Skin Contouring:* In `detect_hand_nail_roi()`, I applied adaptive Otsu thresholding in HSV color space to segment the hand from background clutter. By analyzing contour hierarchies, convex hulls, and phalanx aspect ratios ($W/H \in [0.4, 2.5]$), my algorithm isolates the distal phalanges, separating the keratinized subungual nail bed from the surrounding dorsal skin.
*   *Palpebral Conjunctiva Localization:* In `detect_eye_conjunctiva_roi()`, I leveraged the physiological fact that the palpebral mucosa of the everted lower eyelid has the highest capillary density and vascular redness in the eye ($R/(G+1) > 1.25$ and CIELAB $a^* > 15$). The algorithm tracks this crimson strip, extracts a centered bounding box, and crops it to our standard $224 \times 224 \times 3$ resolution.
*   *Visual Overlays:* The module automatically draws color-coded bounding boxes on the original photo, providing doctors with complete visual transparency so they can confirm the AI looked at the correct tissue.

---

## 4. Biophysical Quality Auditing Gatekeeper (`src/roi_extractor.py`)

*"Having an automated ROI detector is meaningless if the captured image is blurry or ruined by camera flash. To protect our downstream models, I engineered a two-stage optical quality auditor."*

*   *Laplacian Motion Blur Filter:* I implemented `assess_image_quality()` using the variance of the 2D Laplacian operator:
    $$\text{Var}(\nabla^2 I) = \text{Var}\left(\frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}\right)$$
    In crisp, focused photographs, sharp capillary margins yield high spatial edge variance. If a patient's hand trembles or the camera misfocuses, high-frequency edges disappear. If variance drops below $100.0$, the system instantly flags 'Motion Blur Detected / Soft Focus'.
*   *Specular Flash Glare Masking:* Direct smartphone flash produces intense white specular reflections where image sensors saturate ($R, G, B > 245$). If passed to optical colorimetry, these white patches severely dilute redness calculations. In `detect_specular_glare_mask()`, I built a dynamic binary mask that identifies saturated glare pixels and excludes them from downstream feature extraction.

---

## 5. Clinical Dataset Ingestion & Partitioning (`scripts/ingest_eyes_dataset.py`, `data/*.csv`)

*"The final pillar of my work was curating, auditing, and structuring our 451 clinical subjects across two international cohorts."*

*   *Two Peer-Reviewed Cohorts:*
    1. **Nature Scientific Data Cohort**: 250 patients providing paired fingernail and skin photographs. Because 3 fingers were photographed per patient, I processed and standardized $250 \times 3 = 750$ fingernail crops and $750$ skin crops.
    2. **Eyes-defy-anemia Cohort**: 201 patients from Italy ($N=106$) and India ($N=95$), yielding 201 segmented palpebral conjunctiva crops.
*   *Strict Patient-Independent Splitting:* In medical machine learning, image-level splitting causes data leakage—if finger 1 of patient #42 is in Train and finger 2 is in Test, the model memorizes the patient's skin tone rather than hemoglobin. In `data/dataset_manifest.csv` and `data/conjunctiva_manifest.csv`, I enforced strict patient-level partitioning:
    - **Train**: 70% ($175$ nail/skin patients, $140$ eye patients $\to$ $665$ total crops)
    - **Validation**: 15% ($37$ nail/skin patients, $30$ eye patients $\to$ $141$ total crops)
    - **Test (Held-Out)**: 15% ($38$ nail/skin patients, $31$ eye patients $\to$ $145$ total crops)
*   *Audit Script:* I authored `analyze_dataset.py` to continuously verify zero missing files, valid ground-truth laboratory ranges ($4.4$ to $17.4$ g/dL), and complete image integrity across our 569 MB dataset.

---

## 6. Closing (Tying it to the App & Team)

*"To wrap up, my computer vision and data engineering infrastructure ensures that whenever our system runs:"*
1. *Tanay's* deep EfficientNet-B0 backbone and optical colorimetry algorithms receive pristine, lighting-neutralized $224 \times 224$ tissue crops.
2. *Parth's* Model 6 Consensus Engine can trust that input features are derived from genuine microvascular capillaries rather than camera flash glare or blurry motion.
3. *Sayee's* Streamlit web interface can render live bounding box overlays, optical quality audit badges, and patient dataset splits with zero latency.

*"Because we solved tissue localization and lighting normalization at the foundational computer vision layer, our team was able to achieve an outstanding 1.39 g/dL MAE and 69.2% anemia sensitivity without being derailed by real-world smartphone variations."*

---
*(End of Script)*
