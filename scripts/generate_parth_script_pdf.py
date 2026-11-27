import os
import sys
from fpdf import FPDF

class PresentationScriptPDF(FPDF):
    def __init__(self, member_name, title_text, accent_color=(37, 99, 235)):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.member_name = member_name
        self.title_text = title_text
        self.accent_color = accent_color
        self.set_auto_page_break(auto=True, margin=15)

    def clean_text(self, text):
        return (
            text.replace("—", " - ")
            .replace("–", "-")
            .replace("’", "'")
            .replace("‘", "'")
            .replace("“", '"')
            .replace("”", '"')
            .replace("≈", "~")
            .replace("≤", "<=")
            .replace("≥", ">=")
            .replace("±", "+/-")
            .replace("×", "x")
            .replace("→", "->")
            .replace("·", "*")
            .replace("ε", "e")
            .replace("σ", "sigma")
            .replace("μ", "mu")
            .replace("δ", "delta")
            .replace("λ", "lambda")
            .replace("ℝ", "R")
            .replace("∥", "||")
        )

    def header(self):
        self.set_font("Helvetica", "B", 8.5)
        self.set_text_color(100, 116, 139)
        self.cell(0, 6, f"HemoLens Multi-Model | Presentation Script: {self.member_name}", border=0, align="L")
        self.cell(0, 6, "Tanay Tonpe & Team", border=0, align="R")
        self.ln(7)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 6, f"Page {self.page_no()}/{{nb}} - Oral Defense Speaking Guide", align="C")

    def section_header(self, title):
        self.set_font("Helvetica", "B", 11.5)
        self.set_text_color(*self.accent_color)
        self.cell(0, 7, self.clean_text(title), border=0, align="L")
        self.ln(7.5)

    def spoken_text(self, text):
        self.set_font("Helvetica", "I", 9.2)
        self.set_text_color(15, 23, 42)
        self.multi_cell(0, 4.8, f'"{self.clean_text(text)}"')
        self.ln(2.5)

    def narrative_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.6, self.clean_text(text))
        self.ln(2)

    def bullet_item(self, bold_prefix, text):
        self.set_font("Helvetica", "B", 8.8)
        self.set_text_color(15, 23, 42)
        self.cell(5, 4.6, chr(149), border=0)
        self.cell(52, 4.6, f" {self.clean_text(bold_prefix)}: ", border=0)
        self.set_font("Helvetica", "", 8.8)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.6, self.clean_text(text))
        self.ln(1.5)

    def tip_box(self, title, content):
        self.set_fill_color(239, 246, 255) # Light blue
        self.set_draw_color(*self.accent_color)
        self.set_line_width(0.5)
        orig_y = self.get_y()
        self.rect(10, orig_y, 190, 19, style="DF")
        self.set_xy(13, orig_y + 2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.accent_color)
        self.cell(0, 4.5, self.clean_text(title))
        self.set_xy(13, orig_y + 7.5)
        self.set_font("Helvetica", "I", 8.3)
        self.set_text_color(51, 65, 85)
        self.multi_cell(184, 4.0, self.clean_text(content))
        self.set_y(orig_y + 22)


def generate_parth_script_pdf():
    pdf = PresentationScriptPDF(
        member_name="Parth",
        title_text="Multi-Model Fusion & Core Inference System Engineering",
        accent_color=(37, 99, 235) # Blue
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Header Banner
    pdf.set_fill_color(239, 246, 255)
    pdf.set_draw_color(37, 99, 235)
    pdf.rect(10, 17, 190, 24, style="DF")
    pdf.set_xy(14, 19)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(29, 78, 216)
    pdf.cell(0, 7, "HemoLens Multi-Model - Presentation Script (Parth)")
    pdf.set_xy(14, 27)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, "Speaking Guide & Oral Presentation Script | Role: Multi-Model Fusion Engineer")
    pdf.set_xy(14, 33)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, "Domain: Bayesian Consensus Engine, TriModalNet Deep Fusion, Singleton Inference & WHO Triage")
    pdf.set_y(44)

    # Tip Box
    pdf.tip_box(
        "Tip for Parth:",
        "Use this document as your speaking guide during project presentations, reviews, and viva voce. "
        "It covers the multi-model decision architecture, the Bayesian uncertainty-weighted consensus engine, "
        "deep TriModalNet intermediate feature fusion, singleton inference latency optimization, and WHO clinical triage classification."
    )

    # Section 1
    pdf.section_header("1. Introduction")
    pdf.spoken_text(
        "Hello everyone, my name is Parth, and I architected the multi-model fusion algorithms, "
        "deep neural network integration, and core clinical inference engine for the HemoLens framework."
    )
    pdf.narrative_text(
        "In non-invasive optical hematology, relying on any single biological site is fundamentally vulnerable. "
        "If you only look at the fingernails, thick nail plates, nail polish, or peripheral vasoconstriction from cold hands "
        "can distort the signal. If you only look at the skin, differences in epidermal melanin and Fitzpatrick skin phototypes "
        "create confounding absorption. And if you only inspect the eyes, sudden tear film reflections or patient blinking can degrade quality."
    )
    pdf.narrative_text(
        "To solve this, our project's fundamental breakthrough is Multi-Model Fusion. Over the course of my engineering work, "
        "I owned the fusion mathematics, deep neural network architecture, and real-time inference pipeline across 6 core files. My primary goals were:"
    )
    pdf.bullet_item("Bayesian Consensus Engine", "Formulate an uncertainty-weighted consensus engine weighting each tissue by its empirical inverse variance.")
    pdf.bullet_item("TriModalNet Deep Fusion", "Engineer an intermediate feature fusion PyTorch network across three parallel EfficientNet-B0 backbones.")
    pdf.bullet_item("Singleton Inference Pipeline", "Build a high-throughput, lazy-loading singleton inference engine executing predictions in under 2s.")
    pdf.bullet_item("WHO Triage Classification", "Implement automated clinical decision support mapping continuous estimates to WHO diagnostic alert tiers.")
    pdf.spoken_text(
        "I will now explain how these components fit together to deliver an accurate, robust clinical prediction."
    )

    pdf.ln(2)

    # Section 2
    pdf.section_header("2. The Singleton Clinical Inference Engine (src/inference.py)")
    pdf.spoken_text(
        "Everything comes together in src/inference.py. I engineered HemoglobinInferenceEngine to act as the centralized "
        "orchestrator connecting sensory inputs to our models."
    )
    pdf.bullet_item(
        "Singleton Architecture",
        "Loading deep neural network weights into memory on every patient query creates unacceptable latency and memory leaks. "
        "I designed the engine as a cached singleton. When initialized, it lazy-loads all six trained model weight files - including our "
        "PyTorch TriModalNet and scikit-learn regressors - holding them warm in memory for instantaneous execution."
    )
    pdf.bullet_item(
        "End-to-End Orchestration",
        "The engine exposes a clean API: engine.predict(nail_img, eye_img, skin_img). It delegates raw patient photos to Jayesh's "
        "roi_extractor.py for tissue cropping and Gray-World white balancing, executes Tanay's feature_extraction.py for 16 colorimetric "
        "and 1,280 deep CNN features, and feeds these into our single and multi-model consensus fusion."
    )
    pdf.bullet_item(
        "Fault-Tolerant Dynamic Fallback",
        "In real-world clinics, a patient might have an eye injury or an amputated digit. I built dynamic fallback handlers into the inference "
        "loop: if a user submits only two modalities, the engine gracefully detects the missing input, recalculates consensus weights over "
        "the available tissues, and flags a warning without crashing."
    )

    pdf.ln(2)

    # Section 3
    pdf.section_header("3. Bayesian Uncertainty-Weighted Consensus Engine (src/model_fusion.py)")
    pdf.spoken_text(
        "The mathematical heart of HemoLens is Model 6: the Bayesian Consensus Engine that I formulated in src/model_fusion.py."
    )
    pdf.bullet_item(
        "Inverse Variance Weighting",
        "A naive approach to multi-model estimation is simple arithmetic averaging. However, treating an erratic model identically to an accurate "
        "model degrades performance. I applied Maximum A Posteriori (MAP) estimation under Gaussian assumptions: "
        "w_m = (1 / sigma_m^2) / sum_k (1 / sigma_k^2), weighting predictions inversely proportional to error variance."
    )
    pdf.bullet_item(
        "Empirical Modality Weights",
        "From cross-validation on our held-out test cohort, the model standard deviations are: Conjunctiva (sigma = 1.83 g/dL -> weight = 49.4%), "
        "Nail (sigma = 2.35 g/dL -> weight = 30.1%), and Skin (sigma = 2.85 g/dL -> weight = 20.5%). Because the conjunctiva has no melanocytes, "
        "the Bayesian engine automatically assigns it nearly half the total decision weight."
    )
    pdf.bullet_item(
        "Statistical 95% Confidence Intervals",
        "Clinicians need to know not just the estimate, but the model's confidence. I derived the combined standard error SE = sqrt(1 / sum_k(1/sigma_k^2)) "
        "approx 1.28 g/dL, generating rigorous 95% Confidence Intervals [Hb +/- 1.96 * SE] displayed directly to the clinician."
    )
    pdf.bullet_item(
        "Explainable Contributions",
        "The engine outputs the exact percentage contribution of each tissue site for every patient, providing total clinical transparency."
    )

    pdf.ln(2)

    # Section 4
    pdf.section_header("4. Deep Intermediate Feature Fusion (src/models.py - TriModalNet)")
    pdf.spoken_text(
        "Beyond statistical post-hoc fusion, I engineered Model 5: TriModalNet, an end-to-end deep neural network that fuses latent "
        "anatomical features inside the network itself."
    )
    pdf.bullet_item(
        "Tri-Stream Convolutional Backbone",
        "TriModalNet instantiates three parallel convolutional branches using pre-trained EfficientNet-B0 backbones. Each branch receives "
        "a standardized 224x224x3 crop of a different anatomical site (nail, conjunctiva, skin)."
    )
    pdf.bullet_item(
        "3,840-Dimensional Joint Embedding",
        "The terminal global average pooling layers from each branch are concatenated into a joint 3,840-dimensional multimodal embedding vector: "
        "z_joint = [z_nail || z_eye || z_skin] in R^3840."
    )
    pdf.bullet_item(
        "Non-Linear Fusion Head",
        "This dense joint embedding passes through an MLP block: 3840 -> 512 (SiLU, Dropout 0.3) -> 128 (SiLU, Dropout 0.2) -> 1 (Linear). "
        "This architecture allows the network to learn complex cross-tissue non-linear interactions, distinguishing systemic pallor from peripheral vasoconstriction."
    )
    pdf.bullet_item(
        "Ensemble Regressors",
        "Alongside the deep network, I developed L2-regularized Ridge, Lasso, and Gradient Boosting regressors with tuned hyperparameters (alpha = 10.0) "
        "to benchmark against linear baselines."
    )

    pdf.ln(2)

    # Section 5
    pdf.section_header("5. Clinical Decision Support & WHO Severity Stratification")
    pdf.spoken_text(
        "A quantitative hemoglobin number must be translated into actionable medical decisions. I implemented the World Health Organization (WHO) "
        "clinical diagnostic logic."
    )
    pdf.bullet_item(
        "Stratified Alert Tiers",
        "Normal (>= 12.0 g/dL): Green reassurance badge. "
        "Mild Anemia (10.0 - 11.9 g/dL): Yellow warning with dietary counseling. "
        "Moderate Anemia (7.0 - 9.9 g/dL): Orange clinical alert recommending oral iron supplementation and physician consultation. "
        "Severe Anemia (< 7.0 g/dL): Red emergency alert with an urgent Blood Transfusion Referral Alert."
    )
    pdf.bullet_item(
        "Empirical Accuracy",
        "Model 6 achieves a state-of-the-art Mean Absolute Error of 1.39 g/dL across all test subjects, delivering the stability required for non-invasive community screening."
    )

    pdf.ln(2)

    # Section 6
    pdf.section_header("6. Closing (Tying it to the App & Team)")
    pdf.spoken_text(
        "To wrap up, my fusion architecture and inference engineering serve as the central mathematical bridge of HemoLens: "
        "It ingests Jayesh's automated tissue bounding boxes and Gray-World color-balanced crops; "
        "it synthesizes Tanay's deep EfficientNet representations and 16 optical colorimetric biomarkers across all three anatomical modalities; and "
        "it powers Sayee's Streamlit clinical dashboard with a lightning-fast, synchronous prediction API that delivers quantitative hemoglobin, "
        "confidence intervals, contribution percentages, and WHO triage badges in under 2 seconds."
    )
    pdf.spoken_text(
        "By uniting three distinct biological windows through Bayesian consensus fusion, we achieved an accuracy and clinical reliability "
        "that no single-tissue model could ever match alone."
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "--- (End of Script) ---", align="C")

    out_file = "team_dossiers/PARTH_Presentation_Script.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    generate_parth_script_pdf()
