import os
from fpdf import FPDF

class AnnexurePDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, "ANNEXURE | Student Contribution Record - Academic Year 2025-2026", border=0, align="L")
        self.cell(0, 6, "HemoLens Multi-Model", border=0, align="R")
        self.ln(7)
        self.set_draw_color(203, 213, 225)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 6, f"Page {self.page_no()}/{{nb}} - Official Project Report Annexure", align="C")

def generate_annexure_pdf():
    pdf = AnnexurePDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Title Block
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "ANNEXURE: INDIVIDUAL STUDENT CONTRIBUTIONS", align="C")
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 6, "Project Title: HemoLens Multi-Model - Non-Invasive Hemoglobin Estimation", align="C")
    pdf.ln(8)

    pdf.set_font("Helvetica", "I", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 4.5, 
        "This annexure details the distinct technical contributions, module ownership, and implementation responsibilities "
        "fulfilled by each member of the engineering team for the final year capstone project.",
        align="C"
    )
    pdf.ln(5)

    # -------------------------------------------------------------
    # 1. Official Summary Table (Matches Uploaded Image Structure)
    # -------------------------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "1. Project Contribution Summary Table", border=0)
    pdf.ln(8)

    # Table Header
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(15, 23, 42)
    pdf.set_line_width(0.4)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(15, 23, 42)

    w_name = 38
    w_roll = 26
    w_desc = 126

    pdf.cell(w_name, 7, "Student Name", border=1, fill=True, align="L")
    pdf.cell(w_roll, 7, "Roll Number", border=1, fill=True, align="C")
    pdf.cell(w_desc, 7, "Contribution", border=1, fill=True, align="L")
    pdf.ln(7)

    # Data Rows
    students = [
        {
            "name": "Parth Diwale",
            "roll": "B - 41",
            "desc": "Multi-model latent space fusion, Three-Branch deep neural network architecture (TriModalNet), inverse-variance precision-weighted Bayesian consensus engine, singleton production inference manager (HemoglobinInferenceEngine), WHO clinical anemia diagnostic tier classification, and production CLI prediction tool."
        },
        {
            "name": "Sayee Deshmukh",
            "roll": "B - 61",
            "desc": "Interactive Streamlit clinical web dashboard development, point-of-care mobile camera integration, comparative benchmark evaluation vs. JMIR 2026 research paper (Bland-Altman 95% LoA, ROC-AUC, sensitivity/specificity), 29-test automated QA test harness, and cloud deployment configuration."
        },
        {
            "name": "Tanay Tonpe",
            "roll": "B - 65",
            "desc": "Pretrained EfficientNet-B0 deep convolutional feature extraction (1,280-d), 16-d domain optical colorimetry formulation (Erythema Index, CIELAB a*, L*, R/G attenuation ratio), PyTorch deep training pipeline with Cosine Annealing learning rate scheduling, and single-modality regression models (Models 1, 2, and 3)."
        },
        {
            "name": "Jayesh Jumde",
            "roll": "B - 10",
            "desc": "Digital image preprocessing, Gray-World chromatic constancy illuminant filter, dynamic tissue ROI localization & contour segmentation (fingernail bed, finger skin, palpebral conjunctiva), Laplacian focus/blur quality auditing, specular reflection glare masking, dual-cohort clinical dataset ingestion, and master manifest management."
        }
    ]

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(30, 41, 59)
    pdf.set_draw_color(15, 23, 42)

    for s in students:
        start_x = pdf.get_x()
        start_y = pdf.get_y()

        # Calculate height needed for description
        # Using a dummy multi_cell calculation or measuring lines
        # Approx 4-5 lines at 4.2mm each = 20-22mm
        row_height = 23

        # Draw borders and cells
        pdf.rect(start_x, start_y, w_name, row_height)
        pdf.rect(start_x + w_name, start_y, w_roll, row_height)
        pdf.rect(start_x + w_name + w_roll, start_y, w_desc, row_height)

        # Print Name
        pdf.set_xy(start_x + 2, start_y + 3)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(w_name - 4, 5, s["name"], border=0)

        # Print Roll Number
        pdf.set_xy(start_x + w_name, start_y + 3)
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(w_roll, 5, s["roll"], border=0, align="C")

        # Print Description
        pdf.set_xy(start_x + w_name + w_roll + 2, start_y + 2)
        pdf.set_font("Helvetica", "", 7.8)
        pdf.multi_cell(w_desc - 4, 3.8, s["desc"])

        pdf.set_y(start_y + row_height)

    pdf.ln(8)

    # -------------------------------------------------------------
    # 2. Detailed Technical Breakdown Section
    # -------------------------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 7, "2. Module Ownership & System Integration", border=0)
    pdf.ln(7)

    details = [
        ("Parth Diwale (B - 41) - Multi-Model Fusion & Core Inference",
         "Owned Modules: src/models_multimodal.py, src/inference_pipeline.py, src/inference.py, scripts/predict.py, test_engine.py, checkpoints/model4*, checkpoints/model6*.\n"
         "Key Work: Developed the TriModalHemoglobinNet 3-branch deep network in PyTorch. Formulated inverse-variance Bayesian consensus weighting (Conjunctiva 49.4%, Nail 30.1%, Skin 20.5%) minimizing overall MSE. Built the singleton HemoglobinInferenceEngine with WHO clinical tiers.",
         (37, 99, 235)),
        
        ("Sayee Deshmukh (B - 61) - Full-Stack Development & Benchmarks",
         "Owned Modules: app.py, app_streamlit.py, generate_paper_comparison_plots.py, generate_metrics.py, generate_pdf_dossier.py, tests/test_system.py, tests/test_pipeline.py, packages.txt, requirements.txt, README.md.\n"
         "Key Work: Developed the interactive Streamlit clinical dashboard with mobile camera support. Led the comparative evaluation vs. JMIR 2026 paper proving 6x higher correlation (r=0.706 vs 0.120) and 11x higher sensitivity (69.2% vs 6.4%). Built the 29-test automated QA test harness.",
         (124, 58, 237)),

        ("Tanay Tonpe (B - 65) - Deep Learning & Optical Colorimetry",
         "Owned Modules: src/features.py, src/feature_extractor.py, src/models.py, scripts/train.py, checkpoints/model1*, checkpoints/model2*, checkpoints/model3*, scratch_test_models.py.\n"
         "Key Work: Engineered the 1,296-d feature pipeline combining EfficientNet-B0 (1,280-d) with 16 Beer-Lambert optical biomarkers (Erythema Index, CIELAB a*, L*, R/G ratio). Built PyTorch training with Cosine Annealing, training Model 1 (Nail: MAE 1.58), Model 2 (Skin: MAE 1.80), and Model 3 (Conjunctiva: MAE 1.39).",
         (225, 29, 72)),

        ("Jayesh Jumde (B - 10) - Computer Vision & Data Ingestion",
         "Owned Modules: src/preprocessing.py, src/roi_extractor.py, scripts/ingest_eyes_dataset.py, scripts/extract_conjunctiva_features.py, analyze_dataset.py, data/metadata.csv, data/dataset_manifest.csv, data/conjunctiva_manifest.csv.\n"
         "Key Work: Implemented Gray-World chromatic constancy to eliminate room lighting color temperature drift. Engineered dynamic tissue ROI detectors in HSV space, 2D Laplacian focus blur filter, and specular glare mask. Ingested 451 clinical subjects with strict patient-independent splits.",
         (13, 148, 136))
    ]

    for title, text, color in details:
        # Check if page break needed
        if pdf.get_y() > 240:
            pdf.add_page()

        pdf.set_font("Helvetica", "B", 9.5)
        pdf.set_text_color(*color)
        pdf.cell(0, 5, title, border=0)
        pdf.ln(5)

        pdf.set_font("Helvetica", "", 8.2)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 4.0, text)
        pdf.ln(4)

    # Sign-off block
    if pdf.get_y() > 245:
        pdf.add_page()
    pdf.ln(6)
    pdf.set_draw_color(203, 213, 225)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(47, 5, "Parth Diwale (B - 41)", align="C")
    pdf.cell(47, 5, "Sayee Deshmukh (B - 61)", align="C")
    pdf.cell(47, 5, "Tanay Tonpe (B - 65)", align="C")
    pdf.cell(47, 5, "Jayesh Jumde (B - 10)", align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(47, 4, "(Signature / Date)", align="C")
    pdf.cell(47, 4, "(Signature / Date)", align="C")
    pdf.cell(47, 4, "(Signature / Date)", align="C")
    pdf.cell(47, 4, "(Signature / Date)", align="C")

    out_pdf = "team_dossiers/ANNEXURE_STUDENT_CONTRIBUTIONS.pdf"
    pdf.output(out_pdf)
    print(f"Generated: {out_pdf}")

if __name__ == "__main__":
    generate_annexure_pdf()
