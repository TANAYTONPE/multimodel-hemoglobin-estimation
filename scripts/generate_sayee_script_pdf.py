import os
import sys
from fpdf import FPDF

class PresentationScriptPDF(FPDF):
    def __init__(self, member_name, title_text, accent_color=(124, 58, 237)):
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
        self.set_fill_color(250, 245, 255) # Light purple
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


def generate_sayee_script_pdf():
    pdf = PresentationScriptPDF(
        member_name="Sayee",
        title_text="Full-Stack Development, Evaluation & Research Benchmark Engineering",
        accent_color=(124, 58, 237) # Violet / Purple
    )
    pdf.alias_nb_pages()
    pdf.add_page()

    # Cover Header Banner
    pdf.set_fill_color(250, 245, 255)
    pdf.set_draw_color(124, 58, 237)
    pdf.rect(10, 17, 190, 24, style="DF")
    pdf.set_xy(14, 19)
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(109, 40, 217)
    pdf.cell(0, 7, "HemoLens Multi-Model - Presentation Script (Sayee)")
    pdf.set_xy(14, 27)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 5, "Speaking Guide & Oral Presentation Script | Role: Full-Stack & Benchmark Engineer")
    pdf.set_xy(14, 33)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 4, "Domain: Streamlit Web UI, JMIR 2026 Paper Benchmark, Automated QA Test Suite & Cloud Deployment")
    pdf.set_y(44)

    # Tip Box
    pdf.tip_box(
        "Tip for Sayee:",
        "Use this document as your speaking guide during project presentations, reviews, and viva voce. "
        "It covers your full-stack deployment, rigorous comparative benchmarking against the published JMIR 2026 study, "
        "the 29-test automated QA test harness, and cloud production infrastructure."
    )

    # Section 1
    pdf.section_header("1. Introduction")
    pdf.spoken_text(
        "Hello everyone, my name is Sayee, and I architected the full-stack clinical interface, "
        "research benchmarking, and automated quality assurance infrastructure for the HemoLens Multi-Model framework."
    )
    pdf.narrative_text(
        "A breakthrough medical machine learning algorithm is useless to clinicians and patients if it only lives as "
        "fragmented code scripts in a Jupyter Notebook without rigorous statistical validation, clinical proof, or an "
        "intuitive point-of-care graphical interface. In healthcare, trust is built through usability, empirical verification, "
        "and bulletproof reliability."
    )
    pdf.narrative_text(
        "Over the course of my engineering work, I owned the user experience, clinical proof, and deployment infrastructure "
        "spanning 16 core files. My primary goals were:"
    )
    pdf.bullet_item("Interactive Clinical UI", "Develop a glassmorphism Streamlit UI supporting mobile camera capture, 1-click test cases, and WHO alerts.")
    pdf.bullet_item("JMIR 2026 Paper Benchmark", "Exhaustively compare HemoLens head-to-head against the state-of-the-art mobile app study (Zuccotti et al.).")
    pdf.bullet_item("29-Test QA Suite", "Engineer an automated unit and pipeline verification suite to guarantee end-to-end mathematical stability.")
    pdf.bullet_item("Cloud Production Deploy", "Architect zero-friction cloud deployment on Streamlit Community Cloud with Debian Linux packages.txt.")
    pdf.spoken_text(
        "I will now walk you through how these systems transform our deep learning models into an accessible, proven clinical screening tool."
    )

    pdf.ln(2)

    # Section 2
    pdf.section_header("2. The Interactive Clinical Web Dashboard (app.py, app_streamlit.py)")
    pdf.spoken_text(
        "Everything the doctor, nurse, or patient sees and touches was engineered in app.py. I designed a dark-mode clinical UI "
        "that balances medical seriousness with seamless usability."
    )
    pdf.bullet_item(
        "Compulsory 3-Tissue Grid",
        "Model 6 achieves high accuracy because it requires three orthogonal anatomical views: Fingernail Bed, Palpebral Conjunctiva, "
        "and Finger Skin. I built an upload grid that guides users through capturing all three sites, preventing partial or invalid model runs."
    )
    pdf.bullet_item(
        "Native Mobile Camera Integration",
        "When a health worker opens our live link on an iPhone or Android phone, tapping any upload box automatically invokes the device's "
        "native camera. They can photograph a patient's fingernail or lower eyelid right at the bedside and get a reading in under 2 seconds."
    )
    pdf.bullet_item(
        "1-Click Verified Demo Cases",
        "For evaluations where live patient photos aren't immediately available, I programmed instant test buttons: 'Load Verified Normal Case' "
        "(Hb: 13.8 g/dL) and 'Load Verified Anemic Case' (Hb: 8.4 g/dL). This pulls verified clinical cohort test samples with a single click."
    )
    pdf.bullet_item(
        "Diagnostic Transparency & Metrics",
        "Rather than just displaying a bare number, the dashboard presents: quantitative hemoglobin estimate (g/dL) with 95% Confidence Interval, "
        "color-coded WHO severity status pills (Normal, Mild, Moderate, Severe), Bayesian consensus weights (Conjunctiva 49.4%, Nail 30.1%, "
        "Skin 20.5%), and Jayesh's green localized tissue ROI overlays so clinicians can visually confirm accurate anatomical inspection."
    )

    pdf.ln(2)

    # Section 3
    pdf.section_header("3. Clinical Benchmark vs. JMIR 2026 Research Paper (generate_paper_comparison_plots.py)")
    pdf.spoken_text(
        "To prove that HemoLens is not just an academic exercise, I benchmarked our system head-to-head against the newest mobile "
        "non-invasive hemoglobin study published in JMIR Formative Research (February 2026 by Zuccotti et al., evaluating comestai.app on N=555 patients)."
    )
    pdf.spoken_text(
        "Our empirical findings completely vindicate our multi-model optical approach over their facial rPPG technique:"
    )
    pdf.bullet_item(
        "Fixing Near-Zero Correlation",
        "The published JMIR paper used facial video photoplethysmography and obtained a Pearson correlation of only r = 0.120 (R2 ~ 0.014). "
        "In contrast, our Conjunctiva model achieves r = 0.706 (p < 0.0001, R2 = 0.488), explaining nearly 50% of blood hemoglobin variance - a 6x higher correlation."
    )
    pdf.bullet_item(
        "Fixing 6.4% Sensitivity Collapse",
        "The published app missed a staggering 93.6% of anemic patients, delivering a sensitivity of only 6.4%. By targeting unpigmented conjunctival "
        "mucosa and subungual nail beds, our multi-model system achieves a sensitivity of 69.2% - an 11x improvement in detecting patients who need triage."
    )
    pdf.bullet_item(
        "Eliminating False Alarms",
        "In the published study, 89.5% of positive alarms were false positives (PPV = 10.5%). Our Model 4 delivers a PPV of 90.0%, "
        "providing 9 times higher clinical confidence."
    )
    pdf.bullet_item(
        "Bland-Altman 95% Error Envelope",
        "I generated Bland-Altman agreement plots showing that HemoLens achieves an error span of 6.63 g/dL ([-3.21, +3.42]) compared to the paper's "
        "9.68 g/dL ([-4.13, +5.55]) - a 31% tighter clinical error envelope."
    )
    pdf.bullet_item(
        "Diagnostic ROC-AUC",
        "Our Model 4 achieves an AUC of 0.909 compared to the paper's 0.701, confirming outstanding clinical discriminative power."
    )

    pdf.ln(2)

    # Section 4
    pdf.section_header("4. Automated 29-Test Quality Assurance Suite (tests/test_system.py, test_pipeline.py)")
    pdf.spoken_text(
        "In medical software, silent bugs can be fatal. I authored an automated 29-test verification harness that guarantees that any update "
        "to our codebase preserves total mathematical and pipeline integrity."
    )
    pdf.bullet_item(
        "Tiers of Verification",
        "1. Tissue ROI Integrity: Asserts valid bounding boxes and exact 224x224x3 RGB tensors. "
        "2. Optical Colorimetry: Verifies normalized channels sum to 1.0 and Erythema Index tracks attenuation. "
        "3. Checkpoint Verification: Confirms all 6 serialized model weight files exist, are non-empty, and load without corruption. "
        "4. Forward Pass Tests: Tests tensor flow through TriModalNet. "
        "5. WHO Threshold Compliance: Asserts border values map to exact clinical alert tiers. "
        "6. Fault Tolerance: Rejects empty images and zero-byte inputs without crashing."
    )
    pdf.bullet_item(
        "Execution Speed",
        "All 29 unit and integration tests execute in ~7.8 seconds, providing rapid continuous integration before every deployment."
    )

    pdf.ln(2)

    # Section 5
    pdf.section_header("5. Automated Clinical PDF Dossier & Cloud Deployment (generate_pdf_dossier.py, packages.txt)")
    pdf.spoken_text(
        "The final phase of my work was preparing HemoLens for medical review committees and deploying it worldwide."
    )
    pdf.bullet_item(
        "Automated 10-Page PDF Dossier",
        "In generate_pdf_dossier.py, I used Python's fpdf2 library to program an automated document generator that compiles "
        "HemoLens_Presentation_and_Defense_Dossier.pdf, structuring executive summaries, biophysical equations, comparison charts, and viva FAQs."
    )
    pdf.bullet_item(
        "Streamlit Cloud Debian Packages",
        "To ensure anyone can access the app on a phone or laptop without installing Python, I configured the cloud deployment files. "
        "On Debian Linux containers, OpenCV crashes due to missing OS graphics libraries. I authored packages.txt with libgl1 and libglib2.0-0 "
        "to automatically provision system dependencies via apt-get, guaranteeing 100% cloud build success."
    )
    pdf.bullet_item(
        "Master Documentation",
        "I authored the 460-line master README.md, including virtual environment setup guides across Windows PowerShell, Command Prompt, "
        "and Linux/macOS, making our work fully open-source and reproducible."
    )

    pdf.ln(2)

    # Section 6
    pdf.section_header("6. Closing (Tying it to the App & Team)")
    pdf.spoken_text(
        "To wrap up, my full-stack development, research benchmarking, and QA engineering ensure that: "
        "Jayesh's localized tissue crops and Gray-World white balancing are rendered transparently for doctors with live ROI bounding boxes and quality badges; "
        "Tanay's 1,280 deep CNN features and 16 optical colorimetry biomarkers are proven quantitatively superior to published international studies; and "
        "Parth's Model 6 Consensus Engine is delivered to clinicians as a fast, accessible, and responsive web tool backed by 29 passing automated tests."
    )
    pdf.spoken_text(
        "We didn't just train an AI model in a Jupyter Notebook; we engineered a rigorously validated, clinically benchmarked, and "
        "cloud-deployable diagnostic tool that any health worker can open on their smartphone right now."
    )

    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 5, "--- (End of Script) ---", align="C")

    out_file = "team_dossiers/SAYEE_Presentation_Script.pdf"
    pdf.output(out_file)
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    generate_sayee_script_pdf()
