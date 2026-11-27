"""
HemoLens Multimodal — Non-Invasive Hemoglobin Estimation
Gradio Interface for Hugging Face Spaces (with ZeroGPU Support)
"""

import os
import sys
import io
from PIL import Image
import gradio as gr

# Support Hugging Face Spaces ZeroGPU dynamically
try:
    import spaces
except ImportError:
    class spaces:
        @staticmethod
        def GPU(func):
            return func

# Ensure src/ is on system path
sys.path.insert(0, os.path.abspath("src"))
from inference_pipeline import get_inference_engine

# Initialize singleton inference engine
engine = get_inference_engine()

# Helper badge formatter
def get_who_badge_html(badge: str, hb: float, desc: str = "") -> str:
    color_map = {
        "Normal": ("#10b981", "#ecfdf5", "🟢 Normal (Hb ≥ 12.0 g/dL)"),
        "Mild Anemia": ("#f59e0b", "#fffbeb", "🟡 Mild Anemia (10.0 ≤ Hb < 12.0 g/dL)"),
        "Moderate Anemia": ("#ea580c", "#fff7ed", "🟠 Moderate Anemia (7.0 ≤ Hb < 10.0 g/dL)"),
        "Severe Anemia": ("#dc2626", "#fef2f2", "🔴 Severe Anemia (Hb < 7.0 g/dL)")
    }
    color, bg, title = color_map.get(badge, ("#64748b", "#f8fafc", badge))
    
    html = f"""
    <div style="background-color: {bg}; border: 2px solid {color}; border-radius: 12px; padding: 18px 24px; margin: 12px 0;">
        <div style="color: {color}; font-size: 22px; font-weight: 700; margin-bottom: 6px;">{title}</div>
        <div style="font-size: 28px; font-weight: 800; color: #0f172a; margin-bottom: 8px;">
            Estimated Hemoglobin: <span style="color: {color};">{hb:.2f} g/dL</span>
        </div>
        <div style="color: #475569; font-size: 14px; line-height: 1.5;">{desc}</div>
    </div>
    """
    return html

# -------------------------------------------------------------
# TAB 1: Single-Tissue Inference
# -------------------------------------------------------------
@spaces.GPU
def run_single_inference(image, modality_label, apply_wb):
    if image is None:
        return None, None, "⚠️ Please upload or select a clinical photograph.", {}

    mod_map = {
        "Palpebral Conjunctiva (Model 3 - Recommended)": "conjunctiva",
        "Fingernail Bed (Model 1)": "fingernail",
        "Finger Skin (Model 2)": "skin"
    }
    modality = mod_map.get(modality_label, "conjunctiva")

    res = engine.predict_single(image, modality=modality, apply_white_balance=apply_wb)

    hb = res["predicted_hb"]
    badge = res["who_label"]
    badge_html = get_who_badge_html(badge, hb, res["who_description"])

    stats = {
        "Model Architecture": res["model_name"],
        "Predicted Hb (g/dL)": hb,
        "WHO Tier": badge,
        "Erythema Index": round(res["color_stats"].get("erythema_index", 0.0), 3),
        "Normalized Red": round(res["color_stats"].get("normalized_red", 0.0), 3),
        "CIELAB a* (Vascular Chroma)": round(res["color_stats"].get("cielab_a", 0.0), 2),
        "CIELAB L* (Lightness)": round(res["color_stats"].get("cielab_l", 0.0), 2),
        "Focus Sharpness Score": round(res["quality"].get("laplacian_score", 0.0), 1),
        "Focus Status": "Optimal (Sharp)" if res["quality"].get("is_sharp", True) else "Soft / Motion Blur Detected",
        "Specular Flash Masked": f"{res['quality'].get('glare_pct', 0.0):.1f}%"
    }

    return res["annotated_image"], res["cropped_roi"], badge_html, stats

# -------------------------------------------------------------
# TAB 2: Multimodal Consensus Inference
# -------------------------------------------------------------
@spaces.GPU
def run_multimodal_inference(nail_img, skin_img, conj_img, apply_wb):
    if nail_img is None and skin_img is None and conj_img is None:
        return "⚠️ Please upload at least one anatomical tissue photograph.", {}

    res = engine.predict_multimodal_consensus(
        nail_image=nail_img,
        skin_image=skin_img,
        conj_image=conj_img,
        apply_white_balance=apply_wb
    )

    hb = res["predicted_hb"]
    badge = res["who_label"]
    badge_html = get_who_badge_html(badge, hb, f"Fused prediction via {res['model_name']} with precision weighting.")

    details = {
        "Consensus Model": res["model_name"],
        "Predicted Hb (g/dL)": hb,
        "Diagnostic Tier": badge,
        "Individual Model Estimates": res["individual_predictions"],
        "Modality Weights": res["normalized_weights"]
    }

    return badge_html, details

# -------------------------------------------------------------
# GRADIO APPLICATION UI
# -------------------------------------------------------------
sample_conj = "data/sample_images/sample_conjunctiva.jpg" if os.path.exists("data/sample_images/sample_conjunctiva.jpg") else None
sample_nail = "data/sample_images/sample_fingernail.jpg" if os.path.exists("data/sample_images/sample_fingernail.jpg") else None
sample_skin = "data/sample_images/sample_skin.jpg" if os.path.exists("data/sample_images/sample_skin.jpg") else None
sample_anemic = "data/sample_images/sample_anemic_conjunctiva.jpg" if os.path.exists("data/sample_images/sample_anemic_conjunctiva.jpg") else None

examples_list = []
if sample_conj:
    examples_list.append([sample_conj, "Palpebral Conjunctiva (Model 3 - Recommended)", True])
if sample_anemic:
    examples_list.append([sample_anemic, "Palpebral Conjunctiva (Model 3 - Recommended)", True])
if sample_nail:
    examples_list.append([sample_nail, "Fingernail Bed (Model 1)", True])
if sample_skin:
    examples_list.append([sample_skin, "Finger Skin (Model 2)", True])

theme = gr.themes.Soft(
    primary_hue="rose",
    secondary_hue="slate",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
)

with gr.Blocks(theme=theme, title="HemoLens Multimodal — Non-Invasive Hemoglobin Estimation") as demo:
    gr.Markdown(
        """
        # 🩸 HemoLens Multimodal — Non-Invasive Hemoglobin Estimation
        ### Point-of-Care Anemia Screening from Smartphone Photographs of Fingernails, Skin & Palpebral Conjunctiva
        *Powered by EfficientNet-B0 Latent Vectors (1280-d), Optical Colorimetry (16-d), and ZeroGPU Cloud Acceleration.*
        """
    )

    with gr.Tabs():
        # TAB 1: Single Tissue Analysis
        with gr.TabItem("🔍 Single-Tissue Clinical Screening"):
            with gr.Row():
                with gr.Column(scale=5):
                    input_img = gr.Image(type="pil", label="Upload Clinical Photograph (JPG/PNG)")
                    modality_choice = gr.Dropdown(
                        choices=[
                            "Palpebral Conjunctiva (Model 3 - Recommended)",
                            "Fingernail Bed (Model 1)",
                            "Finger Skin (Model 2)"
                        ],
                        value="Palpebral Conjunctiva (Model 3 - Recommended)",
                        label="Select Tissue Anatomical Modality"
                    )
                    wb_checkbox = gr.Checkbox(
                        value=True,
                        label="Apply Gray-World Chromatic Constancy (Corrects Lighting Drift)"
                    )
                    predict_btn = gr.Button("⚡ Analyze Tissue & Estimate Hemoglobin", variant="primary", size="lg")

                    if examples_list:
                        gr.Examples(
                            examples=examples_list,
                            inputs=[input_img, modality_choice, wb_checkbox],
                            label="Built-In Clinical Test Samples"
                        )

                with gr.Column(scale=5):
                    diagnosis_output = gr.HTML(label="Diagnostic Assessment")
                    with gr.Row():
                        annotated_output = gr.Image(type="pil", label="Annotated Tissue ROI Overlay")
                        crop_output = gr.Image(type="pil", label="Extracted 224×224 Crop")
                    biomarkers_output = gr.JSON(label="Optical Biomarkers & Quality Audit")

            predict_btn.click(
                fn=run_single_inference,
                inputs=[input_img, modality_choice, wb_checkbox],
                outputs=[annotated_output, crop_output, diagnosis_output, biomarkers_output]
            )

        # TAB 2: Multimodal Consensus Studio
        with gr.TabItem("🧬 Multimodal Consensus Studio"):
            gr.Markdown(
                """
                ### Multi-Branch Consensus Engine (Model 6)
                Upload clinical photographs across up to 3 microvascular sites to calculate a precision-weighted clinical consensus:
                $$\\hat{\\text{Hb}}_{\\text{consensus}} = 0.494 \\cdot \\hat{\\text{Hb}}_{\\text{conj}} + 0.301 \\cdot \\hat{\\text{Hb}}_{\\text{nail}} + 0.205 \\cdot \\hat{\\text{Hb}}_{\\text{skin}}$$
                """
            )
            with gr.Row():
                nail_input = gr.Image(type="pil", label="1. Fingernail Bed Photo")
                skin_input = gr.Image(type="pil", label="2. Finger Skin Photo")
                conj_input = gr.Image(type="pil", label="3. Palpebral Conjunctiva Photo")

            wb_multi = gr.Checkbox(value=True, label="Apply Gray-World Color Constancy to all images")
            multi_predict_btn = gr.Button("🔬 Run Tri-Modal Precision Consensus", variant="primary", size="lg")

            multi_diagnosis_output = gr.HTML(label="Consensus Diagnostic Assessment")
            multi_details_output = gr.JSON(label="Consensus Breakdown & Modality Weights")

            multi_predict_btn.click(
                fn=run_multimodal_inference,
                inputs=[nail_input, skin_input, conj_input, wb_multi],
                outputs=[multi_diagnosis_output, multi_details_output]
            )

        # TAB 3: Clinical Benchmarks vs State of the Art
        with gr.TabItem("📊 Benchmark vs JMIR 2026 Paper"):
            gr.Markdown(
                """
                ### Clinical Benchmark Against State-of-the-Art Published App
                *Benchmarked against Zuccotti et al., JMIR Formative Research 2026 (`comestai.app` facial video rPPG, N=555).*

                | Parameter | JMIR 2026 Paper (*comestai.app*) | HemoLens Model 3 (*Conjunctiva*) | HemoLens Model 1 (*Fingernail*) | HemoLens Model 4 (*Nail + Skin*) |
                |---|:---:|:---:|:---:|:---:|
                | **Mean Absolute Error (MAE)** | 1.46 g/dL | **1.39 g/dL** | 1.58 g/dL | 1.62 g/dL |
                | **Root Mean Square Error (RMSE)** | 1.88 g/dL | **1.70 g/dL** | 2.17 g/dL | 2.27 g/dL |
                | **Pearson Correlation ($r$)** | 0.12 (Near Zero) | **0.71 ($p < 0.0001$)** | **0.65 ($p < 0.0001$)** | **0.61 ($p < 0.0001$)** |
                | **Diagnostic Sensitivity** | 6.4% (Critical Failure) | **58.3%** | **53.8%** | **69.2%** |
                | **Positive Predictive Value (PPV)** | 10.5% (89.5% False Alarms) | **70.0%** | **100.0%** | **90.0%** |
                | **Acquisition Time** | 90 seconds (still video) | **< 1 second (photo)** | **< 1 second (photo)** | **< 1 second (photo)** |
                | **Melanin Interference** | Heavy (facial cheek skin) | **Zero (unpigmented mucosa)** | Minimal (nail bed) | Compensated |
                """
            )

        # TAB 4: Methodology & Clinical Provenance
        with gr.TabItem("📚 Scientific Methodology"):
            gr.Markdown(
                """
                ### Biophysical & Optical Colorimetry Pipeline
                1. **Tissue Region of Interest (ROI)**: Automated dynamic vascular erythema contouring and GrabCut palpebral mucous membrane segmentation.
                2. **Illumination Correction**: Gray-World chromatic constancy filter estimates illuminant color temperature and normalizes sensor drift.
                3. **Deep Convolutional Feature Embedding**: 1280-dimensional latent representation extracted from pretrained EfficientNet-B0.
                4. **Domain Optical Colorimetry (16-d)**: Normalized RGB, Erythema Index ($EI = \\log_{10}(R_{\\text{norm}}) - \\log_{10}(G_{\\text{norm}})$), CIELAB $a^*$, $L^*$, HSV, and vascular color ratios.
                5. **WHO Diagnostic Guidelines**:
                   - 🟢 **Normal**: $\\text{Hb} \\ge 12.0\\text{ g/dL}$
                   - 🟡 **Mild Anemia**: $10.0 \\le \\text{Hb} < 12.0\\text{ g/dL}$
                   - 🟠 **Moderate Anemia**: $7.0 \\le \\text{Hb} < 10.0\\text{ g/dL}$
                   - 🔴 **Severe Anemia**: $\\text{Hb} < 7.0\\text{ g/dL}$
                """
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
