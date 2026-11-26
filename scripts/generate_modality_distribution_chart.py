import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Ensure output directory exists
os.makedirs("results", exist_ok=True)

# 1. Gather actual counts from disk and manifests
nail_crops = glob.glob("data/crops/nail/*.jpg")
skin_crops = glob.glob("data/crops/skin/*.jpg")
conj_crops = glob.glob("data/crops/conjunctiva/*.jpg")

count_nail = len(nail_crops)
count_skin = len(skin_crops)
count_conj = len(conj_crops)
total_crops = count_nail + count_skin + count_conj

df_manifest = pd.read_csv("data/dataset_manifest.csv")
df_conj = pd.read_csv("data/conjunctiva_manifest.csv")
df_meta = pd.read_csv("data/metadata.csv")

# Split counts (crops)
# Nail and skin have 3 crops per patient
train_pts_ns = (df_manifest["split"] == "train").sum()
val_pts_ns = (df_manifest["split"] == "val").sum()
test_pts_ns = (df_manifest["split"] == "test").sum()

nail_splits = [train_pts_ns * 3, val_pts_ns * 3, test_pts_ns * 3]
skin_splits = [train_pts_ns * 3, val_pts_ns * 3, test_pts_ns * 3]

conj_train = (df_conj["split"] == "train").sum()
conj_val = (df_conj["split"] == "val").sum()
conj_test = (df_conj["split"] == "test").sum()
conj_splits = [conj_train, conj_val, conj_test]

# Configure styling
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#cbd5e1"
plt.rcParams["axes.linewidth"] = 0.8

fig = plt.figure(figsize=(16, 11), dpi=300)
fig.patch.set_facecolor("#ffffff")

# Grid layout: 2x2 grid
gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.25)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

# Color scheme
c_nail = "#e11d48"   # Rose / Coral
c_skin = "#d97706"   # Amber / Dermal
c_conj = "#0284c7"   # Sky blue / Conjunctival
colors_modalities = [c_nail, c_skin, c_conj]
modality_names = ["Fingernail Bed\n(Model 1)", "Finger Skin\n(Model 2)", "Palpebral Conjunctiva\n(Model 3)"]

# ==========================================
# PANEL A: Bar Chart - Absolute Crop Counts
# ==========================================
bars = ax1.bar(
    modality_names,
    [count_nail, count_skin, count_conj],
    color=colors_modalities,
    edgecolor="#1e293b",
    linewidth=1.2,
    width=0.55,
    zorder=3
)
ax1.set_title("A. Absolute Image Crop Counts Across Modalities", fontsize=13, fontweight="bold", pad=12, color="#0f172a")
ax1.set_ylabel("Number of Extracted Tissue Crops (224×224 px)", fontsize=11, fontweight="medium", color="#334155")
ax1.set_ylim(0, 900)
ax1.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

for bar in bars:
    yval = bar.get_height()
    pct = (yval / total_crops) * 100
    ax1.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval + 20,
        f"{yval:,} crops\n({pct:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=10.5,
        fontweight="bold",
        color="#0f172a"
    )

# Annotate source cohorts
ax1.text(0, 400, "Nature Scientific Data\n(250 Patients × 3 Fingers)", ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=9.5)
ax1.text(1, 400, "Nature Scientific Data\n(250 Patients × 3 Fingers)", ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=9.5)
ax1.text(2, 100, "Eyes-defy-anemia\n(201 Patients × 1 Palpebral Crop)", ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=9.0)

# ==========================================
# PANEL B: Donut Chart - Proportional Sample Distribution
# ==========================================
wedges, texts, autotexts = ax2.pie(
    [count_nail, count_skin, count_conj],
    labels=None,
    autopct="%1.1f%%",
    pctdistance=0.76,
    startangle=140,
    colors=colors_modalities,
    wedgeprops=dict(width=0.45, edgecolor="#ffffff", linewidth=2.5)
)

for autotext in autotexts:
    autotext.set_color("#ffffff")
    autotext.set_fontsize(11)
    autotext.set_fontweight("bold")

# Center circle text
ax2.text(0, 0.12, "Total Samples", ha="center", va="center", fontsize=11, color="#64748b", fontweight="medium")
ax2.text(0, -0.10, f"{total_crops:,}", ha="center", va="center", fontsize=20, color="#0f172a", fontweight="bold")
ax2.text(0, -0.26, "Tissue Crops", ha="center", va="center", fontsize=10, color="#64748b")

ax2.set_title(f"B. Proportion of Total Tissue Image Samples (N = {total_crops:,})", fontsize=13, fontweight="bold", pad=12, color="#0f172a")

# Legend for Donut
legend_patches = [
    mpatches.Patch(color=c_nail, label=f"Fingernail: {count_nail} crops (44.1%)"),
    mpatches.Patch(color=c_skin, label=f"Finger Skin: {count_skin} crops (44.1%)"),
    mpatches.Patch(color=c_conj, label=f"Palpebral Conjunctiva: {count_conj} crops (11.8%)")
]
ax2.legend(handles=legend_patches, loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=1, frameon=False, fontsize=9.5)

# ==========================================
# PANEL C: Stacked Bar Chart - Split Distribution (Train/Val/Test)
# ==========================================
x_splits = np.arange(3)
width = 0.52

c_train = "#2563eb"  # Blue
c_val = "#f59e0b"    # Amber
c_test = "#10b981"   # Emerald green

train_vals = [nail_splits[0], skin_splits[0], conj_splits[0]]
val_vals = [nail_splits[1], skin_splits[1], conj_splits[1]]
test_vals = [nail_splits[2], skin_splits[2], conj_splits[2]]

p1 = ax3.bar(x_splits, train_vals, width, label="Train Split (70%)", color=c_train, edgecolor="#ffffff", linewidth=1.5, zorder=3)
p2 = ax3.bar(x_splits, val_vals, width, bottom=train_vals, label="Val Split (15%)", color=c_val, edgecolor="#ffffff", linewidth=1.5, zorder=3)
p3 = ax3.bar(
    x_splits,
    test_vals,
    width,
    bottom=np.array(train_vals) + np.array(val_vals),
    label="Held-Out Test Split (15%)",
    color=c_test,
    edgecolor="#ffffff",
    linewidth=1.5,
    zorder=3
)

ax3.set_title("C. Patient-Independent Dataset Split Distribution", fontsize=13, fontweight="bold", pad=12, color="#0f172a")
ax3.set_ylabel("Number of Samples", fontsize=11, fontweight="medium", color="#334155")
ax3.set_xticks(x_splits)
ax3.set_xticklabels(["Fingernail Bed", "Finger Skin", "Palpebral Conjunctiva"], fontsize=10.5, fontweight="medium")
ax3.set_ylim(0, 880)
ax3.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
ax3.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=9.5)

# Add split count annotations
for i in range(3):
    t_v = train_vals[i]
    v_v = val_vals[i]
    te_v = test_vals[i]
    tot = t_v + v_v + te_v
    
    # Text inside train bar
    ax3.text(i, t_v / 2, f"Train\n{t_v}", ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=9)
    # Text inside val bar
    ax3.text(i, t_v + v_v / 2, f"Val {v_v}", ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=8.5)
    # Text inside test bar
    ax3.text(i, t_v + v_v + te_v / 2, f"Test {te_v}", ha="center", va="center", color="#ffffff", fontweight="bold", fontsize=8.5)
    # Total on top
    ax3.text(i, tot + 15, f"Total: {tot}", ha="center", va="bottom", color="#0f172a", fontweight="bold", fontsize=9.5)

# ==========================================
# PANEL D: Ground Truth Hemoglobin Distribution across Cohorts
# ==========================================
hb_ns = df_meta["hemoglobin"]
hb_conj = df_conj["hemoglobin"]

bins = np.linspace(4.0, 18.0, 29)
ax4.hist(hb_ns, bins=bins, alpha=0.65, color=c_nail, label="Nail & Skin Cohort (N = 250, Mean = 12.76 g/dL)", edgecolor="#ffffff", zorder=3)
ax4.hist(hb_conj, bins=bins, alpha=0.65, color=c_conj, label="Conjunctiva Cohort (N = 201, Mean = 12.67 g/dL)", edgecolor="#ffffff", zorder=3)

# WHO reference threshold lines
ax4.axvline(12.0, color="#ef4444", linestyle="--", linewidth=1.8, label="WHO Anemia Threshold (12.0 g/dL)", zorder=4)
ax4.axvline(10.0, color="#f59e0b", linestyle=":", linewidth=1.5, label="Moderate Anemia Threshold (10.0 g/dL)", zorder=4)
ax4.axvline(7.0, color="#b91c1c", linestyle="-.", linewidth=1.5, label="Severe Anemia Threshold (7.0 g/dL)", zorder=4)

ax4.set_title("D. Ground Truth Hemoglobin Distribution Across Cohorts", fontsize=13, fontweight="bold", pad=12, color="#0f172a")
ax4.set_xlabel("Reference Laboratory Hemoglobin (g/dL)", fontsize=11, fontweight="medium", color="#334155")
ax4.set_ylabel("Patient Count", fontsize=11, fontweight="medium", color="#334155")
ax4.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
ax4.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=8.8)

# Subtitle / Header
fig.suptitle(
    "HemoLens Multimodal: Dataset Sample Distribution Across Anatomical Modalities",
    fontsize=16,
    fontweight="bold",
    color="#0f172a",
    y=0.98
)

plt.tight_layout(rect=[0, 0, 1, 0.95])

out_path = "results/distribution_samples_modalities.png"
plt.savefig(out_path, dpi=300)
plt.close()

print(f"Successfully generated publication chart at: {out_path}")
print(f"Total tissue crops: {total_crops} (Nail: {count_nail}, Skin: {count_skin}, Conjunctiva: {count_conj})")
