import os
import sys
from fpdf import FPDF

class PresentationScriptPDF(FPDF):
    def __init__(self, member_name, title_text, accent_color=(13, 148, 136)):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.member_name = member_name
        self.title_text = title_text
        self.accent_color = accent_color
        self.set_auto_page_break(auto=True, margin=15)

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
        self.cell(0, 7, title, border=0, align="L")
        self.ln(7.5)

    def spoken_text(self, text):
        self.set_font("Helvetica", "I", 9.2)
        self.set_text_color(15, 23, 42)
        self.multi_cell(0, 4.8, f'"{text}"')
        self.ln(2.5)

    def narrative_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.6, text)
        self.ln(2)

    def bullet_item(self, bold_prefix, text):
        self.set_font("Helvetica", "B", 8.8)
        self.set_text_color(15, 23, 42)
        self.cell(5, 4.6, chr(149), border=0)
        self.cell(52, 4.6, f" {bold_prefix}: ", border=0)
        self.set_font("Helvetica", "", 8.8)
        self.set_text_color(51, 65, 85)
        self.multi_cell(0, 4.6, text)
        self.ln(1.5)

    def tip_box(self, title, content):
        self.set_fill_color(240, 253, 250)
        self.set_draw_color(*self.accent_color)
        self.set_line_width(0.5)
        orig_y = self.get_y()
        self.rect(10, orig_y, 190, 19, style="DF")
        self.set_xy(13, orig_y + 2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.accent_color)
        self.cell(0, 4.5, title)
        self.set_xy(13, orig_y + 7.5)
        self.set_font("Helvetica", "I", 8.3)
        self.set_text_color(51, 65, 85)
        self.multi_cell(184, 4.0, content)
        self.set_y(orig_y + 22)


def generate_jayesh_script_pdf():
    pdf = PresentationScriptPDF(
        member_name="Jayesh",
        title_text="Computer Vision & Data Ingestion Engineering",
        accent_color=(13, 148, 136) # Teal
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Header Banner
    pdf.set_fill_color(240, 253, 250)
    pdf.set_draw_color(13, 148, 136)
    pdf.rect(10, 17, 190, 24, style="DF")
    pdf.set_xy(14, 19)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(15, 118, 110)
    pdf.cell(0, 7, "HemoLens Multi-Model - Presentation Script (Jayesh)")
    pdf.set_xy(14, 27)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, "Speaking Guide & Oral Presentation Script | Role: Computer Vision & Data Ingestion Engineer")
    pdf.set_xy(14, 33)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, "Domain: ROI Localization, Gray-World White Balance, Blur/Glare Auditing & Clinical Manifests")
    pdf.set_y(44)

    # Tip Box
    pdf.tip_box(
        "Tip for Jayesh:",
        "Use this document as your speaking guide during project presentations, reviews, and viva voce. "
        "It covers the foundation of the optical pipeline that you built, emphasizing automated vascular ROI localization, "
        "Gray-World illumination normalization, biophysical focus/glare quality auditing, and clinical cohort curation."
    )

    # Section 1
    pdf.section_header("1. Introduction")
    pdf.spoken_text(
        "Hello everyone, my name is Jayesh, and I architected the computer vision, tissue ROI extraction, "
        "and clinical data ingestion infrastructure for the HemoLens Multi-Model framework."
    )
    pdf.narrative_text(
        "When building a non-invasive optical screening platform where blood hemoglobin is estimated purely from "
        "smartphone digital photography, image quality and tissue localization cannot be an afterthought. An AI model "
        "is only as reliable as the biological pixels fed into it. If an input image is out of focus, blinded by flash glare, "
        "distorted by warm room lighting, or cropped incorrectly, even the deepest neural network will output medically dangerous predictions."
    )
    pdf.narrative_text(
        "Over the course of my engineering work, I laid the foundational sensory and computer vision architecture spanning "
        "8 core files and 1,701 standardized tissue crops. My primary goals were:"
    )
    pdf.bullet_item("Automated ROI Localization", "Pinpoint fingernails, dorsal skin, and palpebral conjunctiva without manual cropping.")
    pdf.bullet_item("Gray-World Chromatic Constancy", "Eliminate smartphone sensor color cast and room lighting color temperature drift.")
    pdf.bullet_item("Biophysical Quality Auditing", "Filter out motion-blurred photographs and mask out specular camera flash glare.")
    pdf.bullet_item("Clinical Cohort Curation", "Ingest and harmonize 451 clinical subjects across two international cohorts with zero data leakage.")
    pdf.spoken_text(
        "I will now walk you through how these components work together to deliver pristine, calibrated biological inputs to our models."
    )

    pdf.ln(2)

    # Section 2
    pdf.section_header("2. Gray-World Chromatic Constancy & Preprocessing (src/preprocessing.py)")
    pdf.spoken_text(
        "Everything in optical colorimetry depends on color integrity. In src/preprocessing.py, I solved the ambient lighting "
        "problem that causes most mobile health apps to collapse."
    )
    pdf.bullet_item(
        "The Ambient Lighting Confounder",
        "If a patient takes a photo in a clinic under warm tungsten bulbs (3000K), the tissue looks artificially red, which naive models "
        "misinterpret as elevated hemoglobin (hyperemia). Under cool daylight (6500K), the tissue appears pale, falsely mimicking severe anemia."
    )
    pdf.bullet_item(
        "Mathematical Normalization",
        "Under the Gray-World assumption, the average reflectance in a natural scene is achromatic gray. I implemented an automated "
        "channel-wise scaling algorithm: mu = (mu_R + mu_G + mu_B)/3, R' = R * (mu/mu_R), G' = G * (mu/mu_G), B' = B * (mu/mu_B). "
        "This dynamically normalizes color temperature variations, guaranteeing that measured redness reflects true capillary perfusion."
    )
    pdf.bullet_item(
        "Color-Preserving Augmentations",
        "In standard computer vision, developers apply random hue jitter or convert images to grayscale to prevent overfitting. In optical "
        "hematology, color IS the medical signal. I strictly eliminated hue and saturation jitter in our PyTorch HemoglobinDataset, "
        "restricting augmentations solely to spatial affine transforms (rotations and flips), preserving Beer-Lambert absorption properties."
    )

    pdf.ln(2)

    # Section 3
    pdf.section_header("3. Dynamic Vascular ROI Extraction Engine (src/roi_extractor.py)")
    pdf.spoken_text(
        "Next, we cannot expect doctors or rural health workers to manually crop fingernails or inner eyelids. I built automated localization "
        "algorithms that pinpoint microvascular tissue in seconds."
    )
    pdf.bullet_item(
        "Fingernail Bed & Skin Contouring",
        "In detect_hand_nail_roi(), I applied adaptive Otsu thresholding in HSV color space to segment the hand from background clutter. "
        "By analyzing contour hierarchies, convex hulls, and phalanx aspect ratios (W/H between 0.4 and 2.5), my algorithm isolates distal "
        "phalanges, separating the keratinized subungual nail bed from the surrounding dorsal skin."
    )
    pdf.bullet_item(
        "Palpebral Conjunctiva Localization",
        "In detect_eye_conjunctiva_roi(), I leveraged the physiological fact that the palpebral mucosa of the everted lower eyelid has the highest "
        "capillary density and vascular redness in the eye (R/(G+1) > 1.25 and CIELAB a* > 15). The algorithm tracks this crimson strip, "
        "extracts a centered bounding box, and crops it to our standard 224x224x3 resolution."
    )
    pdf.bullet_item(
        "Visual Diagnostic Overlays",
        "The module automatically draws color-coded bounding boxes on the original photo, providing doctors with complete visual transparency "
        "so they can confirm the AI looked at the correct anatomical tissue."
    )

    pdf.ln(2)

    # Section 4
    pdf.section_header("4. Biophysical Quality Auditing Gatekeeper (src/roi_extractor.py)")
    pdf.spoken_text(
        "Having an automated ROI detector is meaningless if the captured image is blurry or ruined by camera flash. To protect our downstream "
        "models, I engineered a two-stage optical quality auditor."
    )
    pdf.bullet_item(
        "Laplacian Motion Blur Filter",
        "I implemented assess_image_quality() using the variance of the 2D Laplacian operator Var(Laplacian(I)). In crisp photographs, sharp "
        "capillary margins yield high spatial edge variance. If a patient's hand trembles or the camera misfocuses, high-frequency edges disappear. "
        "If variance drops below 100.0, the system instantly flags 'Motion Blur Detected / Soft Focus'."
    )
    pdf.bullet_item(
        "Specular Flash Glare Masking",
        "Direct smartphone flash produces intense white specular reflections where image sensors saturate (R, G, B > 245). If passed to optical "
        "colorimetry, these white patches severely dilute redness calculations. In detect_specular_glare_mask(), I built a dynamic binary mask "
        "that identifies saturated glare pixels and excludes them from downstream feature extraction."
    )

    pdf.ln(2)

    # Section 5
    pdf.section_header("5. Clinical Dataset Ingestion & Partitioning (scripts/ingest_eyes_dataset.py, data/*.csv)")
    pdf.spoken_text(
        "The final pillar of my work was curating, auditing, and structuring our 451 clinical subjects across two international cohorts."
    )
    pdf.bullet_item(
        "Two Peer-Reviewed Cohorts",
        "Nature Scientific Data (250 patients, 750 nail crops and 750 skin crops) and Eyes-defy-anemia (201 patients from Italy and India, "
        "yielding 201 segmented palpebral conjunctiva crops)."
    )
    pdf.bullet_item(
        "Strict Patient-Independent Splits",
        "In medical machine learning, image-level splitting causes data leakage. In data/dataset_manifest.csv and data/conjunctiva_manifest.csv, "
        "I enforced strict patient-level partitioning: Train 70% (665 crops), Validation 15% (141 crops), and Held-Out Test 15% (145 crops)."
    )
    pdf.bullet_item(
        "Data Integrity Audit",
        "I authored analyze_dataset.py to continuously verify zero missing files, valid ground-truth laboratory ranges (4.4 to 17.4 g/dL), "
        "and complete image integrity across our 569 MB dataset."
    )

    pdf.ln(2)

    # Section 6
    pdf.section_header("6. Closing (Tying it to the App & Team)")
    pdf.spoken_text(
        "To wrap up, my computer vision and data engineering infrastructure ensures that whenever our system runs: "
        "Tanay's deep EfficientNet-B0 backbone and optical colorimetry algorithms receive pristine, lighting-neutralized 224x224 tissue crops; "
        "Parth's Model 6 Consensus Engine can trust that input features are derived from genuine microvascular capillaries rather than camera "
        "flash glare or blurry motion; and Sayee's Streamlit web interface can render live bounding box overlays, optical quality audit badges, "
        "and patient dataset splits with zero latency."
    )
    pdf.spoken_text(
        "Because we solved tissue localization and lighting normalization at the foundational computer vision layer, our team was able to "
        "achieve an outstanding 1.39 g/dL MAE and 69.2% anemia sensitivity without being derailed by real-world smartphone variations."
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "--- (End of Script) ---", align="C")

    out_file = "team_dossiers/JAYESH_Presentation_Script.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    generate_jayesh_script_pdf()
