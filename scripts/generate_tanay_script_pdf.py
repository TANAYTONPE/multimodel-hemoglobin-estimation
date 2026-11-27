import os
import sys
from fpdf import FPDF

class PresentationScriptPDF(FPDF):
    def __init__(self, member_name, title_text, accent_color=(225, 29, 72)):
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
        self.set_fill_color(255, 241, 242) # Light rose
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


def generate_tanay_script_pdf():
    pdf = PresentationScriptPDF(
        member_name="Tanay",
        title_text="Deep Learning & Optical Colorimetric Engineering",
        accent_color=(225, 29, 72) # Rose / Red
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Header Banner
    pdf.set_fill_color(255, 241, 242)
    pdf.set_draw_color(225, 29, 72)
    pdf.rect(10, 17, 190, 24, style="DF")
    pdf.set_xy(14, 19)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(190, 18, 60)
    pdf.cell(0, 7, "HemoLens Multi-Model - Presentation Script (Tanay)")
    pdf.set_xy(14, 27)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, "Speaking Guide & Oral Presentation Script | Role: Deep Learning & Optical Engineer")
    pdf.set_xy(14, 33)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, "Domain: Beer-Lambert Optical Biophysics, 16 Color Biomarkers, EfficientNet-B0 & Conjunctiva Discovery")
    pdf.set_y(44)

    # Tip Box
    pdf.tip_box(
        "Tip for Tanay:",
        "Use this document as your speaking guide during project presentations, reviews, and viva voce. "
        "It covers your deep learning representation learning, the biophysical formulation of 16 optical colorimetric biomarkers "
        "based on the Beer-Lambert law, single-modality model training, and the scientific discovery of the palpebral conjunctiva as the optimal optical window."
    )

    # Section 1
    pdf.section_header("1. Introduction")
    pdf.spoken_text(
        "Hello everyone, my name is Tanay, and I architected the deep convolutional representation learning, "
        "optical colorimetric feature engineering, and single-modality model training for the HemoLens Multi-Model framework."
    )
    pdf.narrative_text(
        "In non-invasive medical imaging, deep neural networks are frequently treated as opaque black boxes that output "
        "numbers without physical justification. However, in optical hematology, photon-tissue interaction is governed "
        "by well-established laws of physics. If you do not ground your machine learning architecture in biophysical "
        "optical absorption, your models will memorize spurious camera artifacts instead of true blood physiology."
    )
    pdf.narrative_text(
        "Over the course of my engineering work, I bridged physical optics and deep representation learning spanning "
        "5 core files. My primary goals were:"
    )
    pdf.bullet_item("Biophysical Colorimetry", "Formulate 16 optical biomarkers rooted in the Beer-Lambert law of absorption across RGB, HSV, and CIELAB.")
    pdf.bullet_item("Deep Transfer Learning", "Develop EfficientNet-B0 transfer learning architectures to extract 1,280-dimensional latent embeddings.")
    pdf.bullet_item("Single-Modality Models", "Train and optimize individual regressors (Models 1, 2, and 3) for the fingernail, skin, and conjunctiva.")
    pdf.bullet_item("Conjunctiva Discovery", "Empirically prove that the unpigmented conjunctiva provides the cleanest optical window (r=0.706, p<0.0001).")
    pdf.spoken_text(
        "I will now explain how these biophysical features and neural networks extract true blood hemoglobin signals from smartphone pixels."
    )

    pdf.ln(2)

    # Section 2
    pdf.section_header("2. Biophysical Optical Colorimetry Engine (src/feature_extraction.py)")
    pdf.spoken_text(
        "Everything in optical colorimetry begins with the Beer-Lambert law of light absorption. In src/feature_extraction.py, "
        "I engineered 16 domain-specific optical features."
    )
    pdf.bullet_item(
        "Biophysics of Absorption",
        "Oxygenated (HbO2) and deoxygenated (Hb) hemoglobin exhibit intense optical absorption bands (Q-bands) in the green spectral region "
        "(540-575 nm), while absorbing substantially less light in the red spectral band (~650 nm). Consequently, as capillary blood hemoglobin "
        "concentration increases, tissue absorbs more green photons while reflecting red photons back to the camera sensor."
    )
    pdf.bullet_item(
        "Erythema Index (EI)",
        "Grounded in logarithmic optical attenuation, I formulated EI = log10(R) - log10(G). This quantifies the differential absorption "
        "between red and green spectral bands, directly tracking microvascular blood perfusion independent of absolute lighting intensity."
    )
    pdf.bullet_item(
        "Hemoglobin Index (HI)",
        "I implemented the normalized ratio HI = (R - G) / (R + G). This bounded index isolates capillary redness while neutralizing broad-spectrum illumination fluctuations."
    )
    pdf.bullet_item(
        "CIELAB a* Redness Axis",
        "Unlike RGB where color and illumination are entangled, CIELAB separates perceptual luminance (L*) from chromaticity. The a* channel "
        "represents the green-to-red axis (+a* = redness). I extracted the mean and standard deviation of a*, capturing true microvascular erythema."
    )
    pdf.bullet_item(
        "Normalized Coordinates",
        "I computed illumination-invariant coordinates r = R/(R+G+B), g = G/(R+G+B), b = B/(R+G+B) summing to 1.0, eliminating shadows."
    )

    pdf.ln(2)

    # Section 3
    pdf.section_header("3. Deep Transfer Learning with EfficientNet-B0 (src/models.py)")
    pdf.spoken_text(
        "Handcrafted color features capture macroscopic tissue redness, but microvascular structure has microscopic textures that linear "
        "equations miss. I built deep convolutional encoders to capture these latent patterns."
    )
    pdf.bullet_item(
        "Compound Scaling",
        "I selected EfficientNet-B0 as our visual backbone. Unlike standard ResNets that uniformly scale only depth, EfficientNet utilizes compound "
        "scaling to uniformly scale depth, channel width, and input image resolution (224x224). This delivers superior parameter efficiency: "
        "5.3 million parameters compared to ResNet-50's 25.6 million, preventing overfitting on clinical sample cohorts."
    )
    pdf.bullet_item(
        "1,280-Dim Latent Embeddings",
        "I truncated the classification head and attached a Global Average Pooling (GAP) layer directly to the terminal stage: "
        "input 3x224x224 -> feature maps 1280x7x7 -> GAP -> z in R^1280. These continuous embeddings encode microscopic capillary loops and tissue pallor."
    )
    pdf.bullet_item(
        "Regularization & Stability",
        "To ensure robust training across small medical cohorts, I incorporated Dropout (p = 0.2 - 0.3), Batch Normalization, Swish (SiLU) "
        "activation functions, and L2 weight decay (1e-4)."
    )

    pdf.ln(2)

    # Section 4
    pdf.section_header("4. Single-Modality Optimization & The Conjunctiva Discovery (scripts/train.py)")
    pdf.spoken_text(
        "Once the feature pipelines were established, I trained and evaluated individual models for each anatomical site in scripts/train.py. "
        "This led to the central scientific finding of our research."
    )
    pdf.bullet_item(
        "Single-Modality Performance",
        "Model 1 (Fingernail Bed Regressor): MAE = 1.638 g/dL, R2 = 0.286. "
        "Model 2 (Finger Skin Regressor): MAE = 1.745 g/dL, R2 = 0.208. "
        "Model 3 (Palpebral Conjunctiva Regressor): MAE = 1.392 g/dL, R2 = +0.488."
    )
    pdf.bullet_item(
        "The Conjunctiva Breakthrough",
        "Model 3 demonstrated overwhelming statistical superiority, explaining nearly 50% of systemic blood hemoglobin variance alone (R2 = 0.488) "
        "with a Pearson correlation of r = 0.706 (p < 0.0001)."
    )
    pdf.bullet_item(
        "Overcoming Epidermal Melanin",
        "Skin and nail folds contain variable melanin in the epidermis (Fitzpatrick skin types I-VI). Melanin is a broadband light absorber "
        "that severely confounds optical readings. In stark contrast, the palpebral conjunctiva contains zero melanocytes and minimal keratin, "
        "providing an unobstructed optical window directly into microvascular capillaries."
    )

    pdf.ln(2)

    # Section 5
    pdf.section_header("5. Training Routine & Optimization Pipeline (scripts/extract_conjunctiva_features.py)")
    pdf.spoken_text(
        "To train these models reliably without data leakage or overfitting, I engineered dedicated training routines."
    )
    pdf.bullet_item(
        "Feature Caching Pipeline",
        "In scripts/extract_conjunctiva_features.py, I created an automated batch caching pipeline that pre-computes and serializes feature vectors "
        "into structured NumPy arrays, accelerating model training and cross-validation by 50x."
    )
    pdf.bullet_item(
        "Smooth L1 (Huber) Regression Loss",
        "Clinical reference values from blood draws can contain measurement outliers (+/- 0.5 g/dL). Instead of MSE which squares outlier errors "
        "and destabilizes gradients, I utilized Smooth L1 loss: quadratic near zero, linear for large errors, preventing divergence."
    )
    pdf.bullet_item(
        "Optimization Schedule",
        "Trained using the AdamW optimizer with decoupled weight decay and cosine annealing learning rate schedules."
    )

    pdf.ln(2)

    # Section 6
    pdf.section_header("6. Closing (Tying it to the App & Team)")
    pdf.spoken_text(
        "To wrap up, my deep learning and optical colorimetry engineering provides the physiological intelligence inside HemoLens: "
        "It processes Jayesh's standardized, glare-free, and Gray-World balanced 224x224 tissue crops through our Beer-Lambert extraction formulas; "
        "it feeds trained model checkpoints (Models 1, 2, and 3), 1,280-dimensional CNN embeddings, and empirical variance calibrations (sigma_m) "
        "into Parth's Model 6 Bayesian Consensus Engine; and "
        "it enables Sayee's Streamlit clinical dashboard to render live, interpretable biomarker breakdowns (Erythema Index, Hemoglobin Index, CIELAB a*) "
        "and powers the scientific superiority documented in our JMIR comparative benchmark."
    )
    pdf.spoken_text(
        "By bridging biophysical optical principles with modern deep learning representations, we transformed smartphone cameras into "
        "precision non-invasive hemoglobin sensors."
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "--- (End of Script) ---", align="C")

    out_file = "team_dossiers/TANAY_Presentation_Script.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    generate_tanay_script_pdf()
