import os
import sys
from fpdf import FPDF

os.makedirs("team_dossiers", exist_ok=True)

class MemberDossierPDF(FPDF):
    def __init__(self, member_name, role_title, accent_color=(37, 99, 235)):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.member_name = member_name
        self.role_title = role_title
        self.accent_color = accent_color
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, f"HemoLens Multi-Model | Engineering Dossier: {self.member_name}", border=0, align="L")
        self.cell(0, 6, "Tanay Tonpe & Team", border=0, align="R")
        self.ln(7)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 6, f"Page {self.page_no()}/{{nb}} - Confidential Clinical Engineering Dossier", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(*self.accent_color)
        self.cell(0, 8, title, border=0, align="L")
        self.ln(9)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(15, 23, 42)
        self.cell(0, 6, title, border=0, align="L")
        self.ln(6)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.6, text)
        self.ln(2.5)

    def bullet_point(self, title, description):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(15, 23, 42)
        self.cell(5, 4.6, chr(149), border=0)
        self.cell(48, 4.6, f" {title}: ", border=0)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.6, description)
        self.ln(1.5)

    def callout_box(self, title, content, bg_color=(241, 245, 249)):
        self.set_fill_color(*bg_color)
        self.set_draw_color(*self.accent_color)
        self.set_line_width(0.5)
        
        # Calculate height roughly
        self.rect(10, self.get_y(), 190, 22, style="DF")
        orig_y = self.get_y()
        self.set_xy(13, orig_y + 2)
        self.set_font("Helvetica", "B", 9.5)
        self.set_text_color(*self.accent_color)
        self.cell(0, 5, title)
        self.set_xy(13, orig_y + 8)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(51, 65, 85)
        self.multi_cell(184, 4.2, content)
        self.set_y(orig_y + 25)

    def add_table_header(self, cols, widths):
        self.set_fill_color(241, 245, 249)
        self.set_draw_color(203, 213, 225)
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(15, 23, 42)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6, col, border=1, fill=True, align="C")
        self.ln(6)

    def add_table_row(self, row, widths, is_even=False):
        if is_even:
            self.set_fill_color(248, 250, 252)
        else:
            self.set_fill_color(255, 255, 255)
        self.set_draw_color(226, 232, 240)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(51, 65, 85)
        for i, val in enumerate(row):
            align = "L" if i > 0 else "C"
            self.cell(widths[i], 5.5, str(val), border=1, fill=True, align=align)
        self.ln(5.5)


def generate_jayesh_pdf():
    pdf = MemberDossierPDF(
        member_name="Jayesh",
        role_title="Computer Vision & Data Ingestion Engineer",
        accent_color=(13, 148, 136) # Teal
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Banner
    pdf.set_fill_color(240, 253, 250)
    pdf.set_draw_color(13, 148, 136)
    pdf.rect(10, 18, 190, 26, style="DF")
    pdf.set_xy(14, 21)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 8, "JAYESH - Engineering Dossier & Defense Guide")
    pdf.set_xy(14, 30)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Role: Computer Vision & Data Ingestion Engineer | HemoLens Multi-Model")
    pdf.set_xy(14, 36)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Domain: ROI Localization, Gray-World Chromatic Constancy, Blur/Glare Auditing, Master Manifests")
    pdf.set_y(48)

    pdf.chapter_title("1. Executive Summary of Jayesh's Contribution")
    pdf.body_text(
        "Jayesh is the architect of the front-end sensory and biological image processing pipeline of HemoLens. "
        "Non-invasive optical hemoglobin estimation fails in the clinic if the system is fed uncalibrated, blurry, "
        "overexposed, or poorly localized tissue photographs. Jayesh built the foundational computer-vision layer "
        "that converts arbitrary, unstandardized smartphone photographs of hands and eyes into calibrated, 224x224 px "
        "normalized tissue regions of interest (ROIs)."
    )

    pdf.section_title("Key Responsibilities & Deliverables:")
    pdf.bullet_point("Dynamic Tissue ROIs", "Engineered automated erythema contouring and palpebral mucosa detection in src/roi_extractor.py.")
    pdf.bullet_point("Gray-World Normalization", "Implemented mathematical illuminant normalization in src/preprocessing.py to cancel ambient lighting drift.")
    pdf.bullet_point("Quality Auditing", "Created 2D Laplacian focus variance filter for blur rejection and specular flash reflection masking.")
    pdf.bullet_point("Clinical Manifests", "Curated 451 clinical subjects across Nature and Eyes-defy-anemia cohorts with patient-independent splits.")

    pdf.ln(3)
    pdf.chapter_title("2. Master Inventory of Jayesh's Allotted Files")
    cols = ["File Path", "Category", "Core Responsibility"]
    widths = [62, 38, 90]
    pdf.add_table_header(cols, widths)
    rows = [
        ["src/preprocessing.py", "Core Library", "Gray-World white balancing & color-preserving transforms"],
        ["src/roi_extractor.py", "Core Library", "Automated tissue ROI localization & blur/glare auditing"],
        ["scripts/ingest_eyes_dataset.py", "Pipeline Script", "Cropping & metadata parsing for 201 clinical eye subjects"],
        ["scripts/extract_conjunctiva_features.py", "Batch Script", "Precomputation pipeline for conjunctiva crops"],
        ["analyze_dataset.py", "Audit Script", "Full dataset integrity, missingness & resolution check"],
        ["data/metadata.csv", "Dataset Annotations", "Ground truth laboratory Hb and bounding box coordinates"],
        ["data/dataset_manifest.csv", "Master Manifest", "Links 250 patients to 750 nail and 750 skin crops"],
        ["data/conjunctiva_manifest.csv", "Master Manifest", "Links 201 patients across Italy and India clinical cohorts"],
    ]
    for i, r in enumerate(rows):
        pdf.add_table_row(r, widths, is_even=(i % 2 == 1))

    pdf.ln(4)
    pdf.chapter_title("3. Detailed File Breakdown & Architecture Connections")
    pdf.section_title("A. src/preprocessing.py & Gray-World White Balance")
    pdf.body_text(
        "Under warm tungsten room lighting (3000K), tissues appear artificially reddish, which would cause an AI to "
        "overestimate hemoglobin. Under cool daylight (6500K), tissues appear pale, mimicking severe anemia. "
        "Jayesh implemented Gray-World chromatic constancy: scaling R, G, B channels relative to the scene's global mean "
        "illuminant, guaranteeing true physiological pallor is measured. Standard color augmentations were replaced strictly "
        "with affine spatial transforms to preserve hemodynamic spectral integrity."
    )
    pdf.bullet_point("Connected with Tanay", "Tanay's feature extractor receives normalized 224x224 RGB crops directly from this module.")
    pdf.bullet_point("Connected with Parth", "Parth's inference engine calls apply_gray_world_white_balance() as Step 1 of all predictions.")

    pdf.section_title("B. src/roi_extractor.py & Optical Quality Auditing")
    pdf.body_text(
        "Jayesh built adaptive contouring in HSV color space to segment nail beds and palpebral mucosa. "
        "Furthermore, he added a 2D Laplacian focus filter: images with edge variance < 100 are flagged as motion blurred. "
        "A binary specular glare mask detects flash highlights (> 245 in RGB) to prevent blinding downstream models."
    )
    pdf.bullet_point("Connected with Sayee", "Sayee's Streamlit frontend renders Jayesh's bounding box overlays directly on patient photos.")

    pdf.ln(3)
    pdf.chapter_title("4. Viva / Defense Preparation Questions for Jayesh")
    pdf.section_title("Q1: Why couldn't you use standard ImageNet ColorJitter augmentations?")
    pdf.body_text(
        "Jayesh's Answer: In general computer vision, color invariance is desired (a bus is a bus whether red or blue). "
        "In optical hematology, color IS the medical signal. Applying random hue or saturation jitter destroys the physical "
        "erythema index and Beer-Lambert attenuation ratios. I restricted augmentations strictly to spatial operations."
    )
    pdf.section_title("Q2: How does the system reject blurry photographs?")
    pdf.body_text(
        "Jayesh's Answer: We compute the variance of the 2D Laplacian operator across the tissue ROI. Crisp capillaries exhibit "
        "high spatial gradient variance (> 100). Motion-blurred images have smoothed gradients, automatically triggering an optical audit warning."
    )

    out_file = "team_dossiers/JAYESH_Computer_Vision_and_Data_Ingestion.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")


def generate_tanay_pdf():
    pdf = MemberDossierPDF(
        member_name="Tanay",
        role_title="Deep Learning & Optical Colorimetric Engineer",
        accent_color=(225, 29, 72) # Rose / Red
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Banner
    pdf.set_fill_color(255, 241, 242)
    pdf.set_draw_color(225, 29, 72)
    pdf.rect(10, 18, 190, 26, style="DF")
    pdf.set_xy(14, 21)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(190, 18, 60)
    pdf.cell(0, 8, "TANAY - Engineering Dossier & Defense Guide")
    pdf.set_xy(14, 30)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Role: Deep Learning & Optical Colorimetric Engineer | HemoLens Multi-Model")
    pdf.set_xy(14, 36)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Domain: EfficientNet-B0 Backbone, 16-d Beer-Lambert Biomarkers, PyTorch Training & Single-Modality Models")
    pdf.set_y(48)

    pdf.chapter_title("1. Executive Summary of Tanay's Contribution")
    pdf.body_text(
        "Tanay engineered the neural representation and mathematical optical colorimetry layer of HemoLens. "
        "Pure deep learning is prone to overfitting and opacity on clinical datasets, while pure colorimetry fails to capture "
        "vascular micro-textures. Tanay harmonized both worlds by designing a unified 1,296-dimensional representation combining "
        "1,280 deep convolutional features from EfficientNet-B0 with 16 biophysical optical biomarkers derived from the Beer-Lambert "
        "law of hemoglobin attenuation."
    )

    pdf.section_title("Key Responsibilities & Deliverables:")
    pdf.bullet_point("1296-d Dual Feature Pipeline", "Designed EfficientNet-B0 (1280d) + 16-d optical biomarkers in src/feature_extractor.py.")
    pdf.bullet_point("Optical Biomarkers", "Formulated Erythema Index, CIELAB a* (vascular chroma), CIELAB L* (pallor), and R/G ratio.")
    pdf.bullet_point("Deep Training Loop", "Built PyTorch training infrastructure with Cosine Annealing learning rate scheduling in scripts/train.py.")
    pdf.bullet_point("Single-Modality Models", "Trained Model 1 (Nail: MAE 1.58), Model 2 (Skin: MAE 1.80), and Model 3 (Conjunctiva: MAE 1.39).")

    pdf.ln(3)
    pdf.chapter_title("2. Master Inventory of Tanay's Allotted Files")
    cols = ["File Path", "Category", "Core Responsibility"]
    widths = [62, 38, 90]
    pdf.add_table_header(cols, widths)
    rows = [
        ["src/features.py", "Biomarker Library", "16 domain optical colorimetry algorithms (EI, a*, L*, R/G)"],
        ["src/feature_extractor.py", "Neural Backbone", "Pretrained EfficientNet-B0 1280-d + 16-d colorimetry extractor"],
        ["src/models.py", "Neural Architecture", "PyTorch single-modality regression models and custom heads"],
        ["scripts/train.py", "Training Loop", "Cosine Annealing schedule, validation evaluation & checkpointing"],
        ["checkpoints/model1_fingernail.joblib", "Model Checkpoint", "Trained Fingernail Regressor weights (MAE = 1.58 g/dL)"],
        ["checkpoints/model2_skin.joblib", "Model Checkpoint", "Trained Finger Skin Regressor weights (MAE = 1.80 g/dL)"],
        ["checkpoints/model3_conjunctiva.joblib", "Model Checkpoint", "Trained Conjunctiva Regressor weights (MAE = 1.39 g/dL)"],
        ["scratch_test_models.py", "ML Ablation", "Benchmarked Ridge, ElasticNet, Huber, SVR, and Gradient Boosting"],
    ]
    for i, r in enumerate(rows):
        pdf.add_table_row(r, widths, is_even=(i % 2 == 1))

    pdf.ln(4)
    pdf.chapter_title("3. Detailed File Breakdown & Architecture Connections")
    pdf.section_title("A. src/feature_extractor.py & The 16-d Beer-Lambert Biomarkers")
    pdf.body_text(
        "Tanay loaded torchvision.models.efficientnet_b0 with frozen weights, stripping the classifier to yield 1,280 features. "
        "To this, he appended 16 handcrafted optical biomarkers: Erythema Index EI = log10(R) - log10(G), CIELAB a* (vascular redness), "
        "CIELAB L* (pallor/brightness), normalized color channels r, g, b, and HSV saturation. This provides both deep spatial "
        "microvascular patterns and physical hemodynamic color metrics."
    )
    pdf.bullet_point("Connected with Jayesh", "Processes the 224x224 crops and Gray-World normalized images output by Jayesh.")
    pdf.bullet_point("Connected with Parth", "Parth's multi-model fusion heads take Tanay's 1,296-d feature vectors as primary inputs.")

    pdf.section_title("B. Single-Modality Regressors (Model 1, Model 2, Model 3)")
    pdf.body_text(
        "Using regularized Ridge regression (alpha=300.0), Tanay trained three independent estimators. "
        "Model 3 (Conjunctiva) emerged as the single most powerful modality with MAE = 1.392 g/dL and R2 = +0.488, "
        "proving that unpigmented palpebral mucosa provides the cleanest optical window into systemic blood hemoglobin."
    )
    pdf.bullet_point("Connected with Sayee", "Sayee displays Tanay's individual model metrics and color biomarkers in app.py.")

    pdf.ln(3)
    pdf.chapter_title("4. Viva / Defense Preparation Questions for Tanay")
    pdf.section_title("Q1: Why freeze EfficientNet-B0 instead of fine-tuning the whole network?")
    pdf.body_text(
        "Tanay's Answer: Our datasets have hundreds of patients. Fine-tuning a 5-million parameter network on small clinical cohorts "
        "causes catastrophic overfitting to patient skin blemishes and background noise. Freezing the pretrained backbone transfers "
        "robust general spatial feature filters, while training a regularized linear head guarantees strong clinical generalization."
    )
    pdf.section_title("Q2: Why does Conjunctiva (Model 3) outperform Fingernail and Skin?")
    pdf.body_text(
        "Tanay's Answer: Cutaneous skin contains melanin which absorbs broadly and non-specifically, masking hemoglobin attenuation. "
        "The palpebral conjunctiva is an unpigmented mucous membrane fed by the ophthalmic artery with zero melanin interference, "
        "giving it the highest optical signal-to-noise ratio."
    )

    out_file = "team_dossiers/TANAY_Deep_Learning_and_Optical_Colorimetry.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")


def generate_parth_pdf():
    pdf = MemberDossierPDF(
        member_name="Parth",
        role_title="Multi-Model Fusion & Core Inference System Engineer",
        accent_color=(37, 99, 235) # Blue
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Banner
    pdf.set_fill_color(239, 246, 255)
    pdf.set_draw_color(37, 99, 235)
    pdf.rect(10, 18, 190, 26, style="DF")
    pdf.set_xy(14, 21)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(29, 78, 216)
    pdf.cell(0, 8, "PARTH - Engineering Dossier & Defense Guide")
    pdf.set_xy(14, 30)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Role: Multi-Model Fusion & Core Inference System Engineer | HemoLens Multi-Model")
    pdf.set_xy(14, 36)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Domain: Multi-Model Fusion, TriModalNet PyTorch Architecture, Bayesian Consensus & Production CLI")
    pdf.set_y(48)

    pdf.chapter_title("1. Executive Summary of Parth's Contribution")
    pdf.body_text(
        "Parth is the architect of the multi-model fusion systems and the production inference runtime of HemoLens. "
        "Single anatomical sites are vulnerable to localized confounders (nail polish, peripheral cold vasoconstriction, skin jaundice). "
        "Parth solved this clinical vulnerability by engineering multi-model fusion architectures combining all three tissue sites: "
        "Dual-Branch concatenation (Model 4: 2592-d), the three-branch PyTorch network (TriModalHemoglobinNet: Model 6), and the "
        "precision-weighted Bayesian Consensus Engine that achieves an outstanding 86.8% screening accuracy and 0.909 ROC-AUC."
    )

    pdf.section_title("Key Responsibilities & Deliverables:")
    pdf.bullet_point("Multi-Model Fusion", "Engineered Dual-Branch (2592d) and Tri-Modal (3888d) fusion in src/models_multimodal.py.")
    pdf.bullet_point("TriModalNet PyTorch", "Architected 3-branch deep network processing Nail, Skin, and Eye tensors simultaneously.")
    pdf.bullet_point("Bayesian Consensus", "Designed inverse-variance precision weighting (Conjunctiva 49.4%, Nail 30.1%, Skin 20.5%).")
    pdf.bullet_point("Production Pipeline", "Built singleton HemoglobinInferenceEngine, WHO clinical severity tiers, and CLI predict.py.")

    pdf.ln(3)
    pdf.chapter_title("2. Master Inventory of Parth's Allotted Files")
    cols = ["File Path", "Category", "Core Responsibility"]
    widths = [62, 38, 90]
    pdf.add_table_header(cols, widths)
    rows = [
        ["src/models_multimodal.py", "Core Fusion", "TriModalHemoglobinNet 3-branch network & regularized heads"],
        ["src/inference_pipeline.py", "Production Engine", "Singleton inference engine, Bayesian consensus & WHO tiers"],
        ["src/inference.py", "Inference Library", "Single-modality and multi-modality fallback inference utilities"],
        ["src/__init__.py", "Package Initializer", "Exposes unified API (get_inference_engine, classify_who_anemia)"],
        ["scripts/predict.py", "Production CLI", "Terminal prediction tool supporting single/multi-model & JSON export"],
        ["test_engine.py", "Verification Harness", "Fast end-to-end smoke test validating all loaded checkpoints"],
        ["checkpoints/model4_nail_skin_fusion.joblib", "Fusion Checkpoint", "Trained weights for paired Nail + Skin (2592-d input)"],
        ["checkpoints/model5_nail_conj_fusion.joblib", "Fusion Checkpoint", "Calibrated weights for Nail + Conjunctiva cross-modality"],
        ["checkpoints/model6_tri_modal.pth", "Deep Checkpoint", "PyTorch state dict for 3-branch TriModal consensus network"],
    ]
    for i, r in enumerate(rows):
        pdf.add_table_row(r, widths, is_even=(i % 2 == 1))

    pdf.ln(4)
    pdf.chapter_title("3. Detailed File Breakdown & Architecture Connections")
    pdf.section_title("A. src/models_multimodal.py & TriModalHemoglobinNet")
    pdf.body_text(
        "Parth designed TriModalHemoglobinNet to accept three independent 1,296-d feature branches. Each branch passes through "
        "a private linear projection layer (1296 -> 128) with SiLU activation. The 384-dimensional concatenated representation is fed "
        "into a fusion MLP with Dropout (p=0.3) and Batch Normalization to output quantitative Hb (g/dL)."
    )
    pdf.bullet_point("Connected with Tanay", "Directly ingests Tanay's 1,296-d feature vectors from EfficientNet and optical biomarkers.")

    pdf.section_title("B. src/inference_pipeline.py & Precision-Weighted Consensus")
    pdf.body_text(
        "Parth implemented the singleton HemoglobinInferenceEngine. Rather than a naive average, Model 6 uses inverse-variance "
        "weighting based on validation RMSE: Conjunctiva carries 49.4% weight, Nail carries 30.1%, and Skin carries 20.5%. "
        "He also mapped predictions to WHO diagnostic tiers (Normal, Mild, Moderate, Severe Anemia with critical transfusion alerts)."
    )
    pdf.bullet_point("Connected with Jayesh", "Calls Jayesh's auto_detect_roi() and apply_gray_world_white_balance() inside inference.")
    pdf.bullet_point("Connected with Sayee", "Sayee's app.py imports Parth's engine to execute predictions and render results.")

    pdf.ln(3)
    pdf.chapter_title("4. Viva / Defense Preparation Questions for Parth")
    pdf.section_title("Q1: Why use precision weighting instead of equal averaging in Model 6?")
    pdf.body_text(
        "Parth's Answer: Equal averaging is statistically sub-optimal when sensors have different noise variances. Conjunctiva has an "
        "RMSE of 1.695, Nail has 2.173, and Skin has 2.627. Weighting inversely to variance minimizes overall expected MSE."
    )
    pdf.section_title("Q2: How does multi-model fusion overcome the 6.4% sensitivity failure in literature?")
    pdf.body_text(
        "Parth's Answer: Published facial rPPG studies missed 93.6% of anemic patients because skin pallor has poor dynamic range. "
        "By fusing conjunctival mucosa with subungual nail capillaries, our Model 4 and 6 achieve 69.2% sensitivity and 0.909 AUC."
    )

    out_file = "team_dossiers/PARTH_Multi_Model_Fusion_and_Inference_Systems.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")


def generate_sayee_pdf():
    pdf = MemberDossierPDF(
        member_name="Sayee",
        role_title="Full-Stack Development, Evaluation & Research Benchmark Engineer",
        accent_color=(124, 58, 237) # Violet / Purple
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Banner
    pdf.set_fill_color(245, 243, 255)
    pdf.set_draw_color(124, 58, 237)
    pdf.rect(10, 18, 190, 26, style="DF")
    pdf.set_xy(14, 21)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(109, 40, 217)
    pdf.cell(0, 8, "SAYEE - Engineering Dossier & Defense Guide")
    pdf.set_xy(14, 30)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, "Role: Full-Stack Development, Evaluation & Benchmark Engineer | HemoLens Multi-Model")
    pdf.set_xy(14, 36)
    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "Domain: Streamlit Web UI, JMIR 2026 Paper Benchmark, Automated QA Test Suite & Cloud Deployment")
    pdf.set_y(48)

    pdf.chapter_title("1. Executive Summary of Sayee's Contribution")
    pdf.body_text(
        "Sayee bridges machine learning research and practical clinical application by owning the full-stack user experience, "
        "statistical validation, and deployment infrastructure of HemoLens. She engineered the interactive Streamlit clinical dashboard "
        "supporting live camera capture and 1-click test cases. Furthermore, she conducted the exhaustive statistical benchmark against "
        "the published state-of-the-art JMIR 2026 paper, authored the 29-test automated QA test harness, and configured the cloud "
        "deployment files that enable HemoLens to run worldwide on any phone or laptop."
    )

    pdf.section_title("Key Responsibilities & Deliverables:")
    pdf.bullet_point("Clinical Web Dashboard", "Developed point-of-care Streamlit dashboard with 3-tissue acquisition in app.py.")
    pdf.bullet_point("JMIR 2026 Benchmark", "Proved 6x higher correlation (r=0.706 vs 0.120) and 11x higher sensitivity (69.2% vs 6.4%).")
    pdf.bullet_point("Automated QA Suite", "Engineered 29 unit and integration tests across models, ROIs, and pipeline in tests/.")
    pdf.bullet_point("Cloud Deployment", "Configured packages.txt (libgl1), requirements.txt, setup.py, and 460-line master README.md.")

    pdf.ln(3)
    pdf.chapter_title("2. Master Inventory of Sayee's Allotted Files")
    cols = ["File Path", "Category", "Core Responsibility"]
    widths = [62, 38, 90]
    pdf.add_table_header(cols, widths)
    rows = [
        ["app.py", "Clinical Frontend", "Streamlit web UI with 3-modality acquisition & Model 6 Consensus"],
        ["app_streamlit.py", "UI Variant", "Auxiliary Streamlit interface implementation"],
        ["generate_paper_comparison_plots.py", "Research Benchmark", "Bland-Altman, Pearson r, and ROC curve comparison generators"],
        ["generate_metrics.py", "Biostatistics", "Calculates clinical MAE, RMSE, Pearson r, sensitivity, specificity, PPV"],
        ["generate_pdf_dossier.py", "PDF Tool", "Automated 10-page clinical presentation and defense PDF compiler"],
        ["scripts/train_evaluate_all.py", "Pipeline Script", "Retrains regressors and regenerates publication comparison plots"],
        ["scripts/generate_modality_distribution_chart.py", "Graphics", "Quad-panel publication chart of exact dataset counts and splits"],
        ["scratch_evaluate.py", "Evaluation Script", "Bland-Altman limits of agreement and clinical diagnostic matrices"],
        ["tests/test_system.py", "Automated QA", "29 comprehensive unit tests verifying models, ROIs, and pipelines"],
        ["tests/test_pipeline.py", "Automated QA", "Asserts WHO category thresholds and edge case exception handling"],
        ["packages.txt", "Linux OS Config", "Debian OS libraries (libgl1, libglib2.0-0) for Streamlit Cloud OpenCV"],
        ["requirements.txt & setup.py", "Packaging", "Pinned production dependencies and pip package configuration"],
        ["README.md", "Master Documentation", "Comprehensive documentation, setup guide & troubleshooting manual"],
    ]
    for i, r in enumerate(rows):
        pdf.add_table_row(r, widths, is_even=(i % 2 == 1))

    pdf.ln(4)
    pdf.chapter_title("3. Detailed File Breakdown & Architecture Connections")
    pdf.section_title("A. app.py (Point-of-Care Streamlit Web Dashboard)")
    pdf.body_text(
        "Sayee developed the dark-mode clinical UI. On smartphones, tapping upload triggers native mobile cameras directly. "
        "She added 1-click demo buttons ('Load Verified Normal Case' and 'Load Verified Anemic Case'), live localized ROI displays, "
        "and dynamic color-coded WHO status pills. The app connects to Parth's singleton engine via @st.cache_resource."
    )
    pdf.bullet_point("Connected with Parth", "Imports get_inference_engine() to run real-time inference and display results.")
    pdf.bullet_point("Connected with Jayesh & Tanay", "Displays Jayesh's green ROI overlays and Tanay's optical biomarkers.")

    pdf.section_title("B. generate_paper_comparison_plots.py & JMIR 2026 Benchmark")
    pdf.body_text(
        "Sayee benchmarked HemoLens against Zuccotti et al. (JMIR Form Res 2026, comestai.app, N=555). "
        "She proved our Model 3 achieves r=0.706 (vs 0.120), Model 4 achieves 69.2% sensitivity (vs 6.4%), and Bland-Altman "
        "span is 6.63 g/dL (vs 9.68 g/dL). This statistical critique defends why our multi-model optical approach succeeds."
    )

    pdf.section_title("C. tests/test_system.py & Cloud Deployment Configuration")
    pdf.body_text(
        "Sayee authored 29 automated tests verifying ROIs, feature extractors, checkpoints, and forward passes (all pass in ~7.8s). "
        "She added packages.txt (libgl1, libglib2.0-0) to resolve headless Linux OpenCV dependencies on Streamlit Community Cloud."
    )

    pdf.ln(3)
    pdf.chapter_title("4. Viva / Defense Preparation Questions for Sayee")
    pdf.section_title("Q1: How did you prove HemoLens is superior to published mobile rPPG apps?")
    pdf.body_text(
        "Sayee's Answer: In generate_paper_comparison_plots.py, I compared our models head-to-head with the JMIR 2026 study. "
        "Their rPPG app had near-zero correlation (r=0.120) and missed 93.6% of anemic patients (sensitivity 6.4%). Our system achieves "
        "r=0.706, 69.2% sensitivity, 90.0% PPV, and 0.909 AUC, proving multi-model tissue colorimetry is clinically viable."
    )
    pdf.section_title("Q2: Why was packages.txt required for cloud deployment?")
    pdf.body_text(
        "Sayee's Answer: Streamlit Community Cloud executes in Debian Linux containers where OpenCV requires system graphics libraries "
        "(libGL.so.1 and libglib2.0). Creating packages.txt instructs the builder to run apt-get install libgl1 libglib2.0-0, preventing crashes."
    )

    out_file = "team_dossiers/SAYEE_Full_Stack_Development_and_Research_Benchmarks.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")


if __name__ == "__main__":
    generate_jayesh_pdf()
    generate_tanay_pdf()
    generate_parth_pdf()
    generate_sayee_pdf()
    print("All 4 team member PDFs successfully compiled!")
