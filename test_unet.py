import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(9.2, 5.8), dpi=220)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")
ax.axis("off")

# Title
ax.text(4.6, 5.4, "Kiến trúc Mạng Nơ-ron PyTorch U-Net 2D (5 Kênh)", 
        ha="center", va="center", fontsize=14, weight="bold", color="#7030A0")

# 1. Input Box
box_in = patches.FancyBboxPatch((0.4, 3.8), 1.25, 1.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#F1ECF8", edgecolor="#7030A0", lw=2)
ax.add_patch(box_in)
ax.text(1.025, 4.5, "Input 5 Kênh", ha="center", va="center", fontsize=10, weight="bold", color="#7030A0")
ax.text(1.025, 4.15, "5 x 20 x 20\n(Lửa, Gió, DEM)", ha="center", va="center", fontsize=8.2, color="#1E1E24")

# Arrow In -> Enc1
ax.annotate("", xy=(2.05, 4.4), xytext=(1.65, 4.4),
            arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#7030A0", mutation_scale=15))

# 2. Enc1 (20x20)
box_e1 = patches.FancyBboxPatch((2.05, 3.8), 1.35, 1.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#E1F0FA", edgecolor="#1C6FA6", lw=2)
ax.add_patch(box_e1)
ax.text(2.725, 4.5, "Encoder 1", ha="center", va="center", fontsize=10, weight="bold", color="#1C6FA6")
ax.text(2.725, 4.15, "Conv 32\n(20 x 20)", ha="center", va="center", fontsize=8.5, color="#1E1E24")

# Arrow Enc1 -> Enc2 (MaxPool)
ax.annotate("", xy=(2.725, 3.1), xytext=(2.725, 3.8),
            arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#1C6FA6", mutation_scale=15))
ax.text(3.05, 3.45, "MaxPool", fontsize=7.8, color="#1C6FA6", va="center")

# 3. Enc2 (10x10)
box_e2 = patches.FancyBboxPatch((2.05, 1.9), 1.35, 1.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#E1F0FA", edgecolor="#1C6FA6", lw=2)
ax.add_patch(box_e2)
ax.text(2.725, 2.6, "Encoder 2", ha="center", va="center", fontsize=10, weight="bold", color="#1C6FA6")
ax.text(2.725, 2.25, "Conv 64\n(10 x 10)", ha="center", va="center", fontsize=8.5, color="#1E1E24")

# Arrow Enc2 -> Bottleneck
ax.annotate("", xy=(3.85, 1.1), xytext=(3.4, 2.0),
            arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#B3236F", mutation_scale=15))
ax.text(3.4, 1.4, "MaxPool", fontsize=7.8, color="#B3236F")

# 4. Bottleneck (5x5)
box_bn = patches.FancyBboxPatch((3.85, 0.4), 1.5, 1.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#FBE3F0", edgecolor="#B3236F", lw=2.4)
ax.add_patch(box_bn)
ax.text(4.6, 1.1, "Bottleneck", ha="center", va="center", fontsize=10.5, weight="bold", color="#B3236F")
ax.text(4.6, 0.75, "Conv 128\n(5 x 5)", ha="center", va="center", fontsize=8.8, color="#1E1E24")

# Arrow Bottleneck -> Dec1
ax.annotate("", xy=(5.8, 2.0), xytext=(5.35, 1.1),
            arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#15803D", mutation_scale=15))
ax.text(5.6, 1.4, "UpConv", fontsize=7.8, color="#15803D")

# 5. Dec1 (10x10)
box_d1 = patches.FancyBboxPatch((5.8, 1.9), 1.35, 1.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#DCFCE7", edgecolor="#15803D", lw=2)
ax.add_patch(box_d1)
ax.text(6.475, 2.6, "Decoder 1", ha="center", va="center", fontsize=10, weight="bold", color="#15803D")
ax.text(6.475, 2.25, "UpConv 64\n(10 x 10)", ha="center", va="center", fontsize=8.5, color="#1E1E24")

# Arrow Dec1 -> Dec0
ax.annotate("", xy=(6.475, 3.8), xytext=(6.475, 3.1),
            arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#15803D", mutation_scale=15))
ax.text(6.75, 3.45, "UpConv", fontsize=7.8, color="#15803D", va="center")

# 6. Dec0 (20x20)
box_d0 = patches.FancyBboxPatch((5.8, 3.8), 1.35, 1.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                facecolor="#DCFCE7", edgecolor="#15803D", lw=2)
ax.add_patch(box_d0)
ax.text(6.475, 4.5, "Decoder 0", ha="center", va="center", fontsize=10, weight="bold", color="#15803D")
ax.text(6.475, 4.15, "UpConv 32\n(20 x 20)", ha="center", va="center", fontsize=8.5, color="#1E1E24")

# Arrow Dec0 -> Output
ax.annotate("", xy=(7.55, 4.4), xytext=(7.15, 4.4),
            arrowprops=dict(arrowstyle="-|>", lw=2.2, color="#B45309", mutation_scale=15))

# 7. Output Box
box_out = patches.FancyBboxPatch((7.55, 3.8), 1.25, 1.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                                 facecolor="#FEF3C7", edgecolor="#B45309", lw=2)
ax.add_patch(box_out)
ax.text(8.175, 4.5, "Heatmap 2D", ha="center", va="center", fontsize=10, weight="bold", color="#B45309")
ax.text(8.175, 4.15, "1 x 20 x 20\nP(x, y) in [0, 1]", ha="center", va="center", fontsize=8.2, color="#1E1E24")

# Skip Connections: Draw arrow from Enc1 right edge to badge left, then from badge right to Dec0 left!
# Level 1: Enc1 (3.4) -> Badge1 (3.7 to 5.5) -> Dec0 (5.8)
badge1 = patches.FancyBboxPatch((3.65, 4.1), 1.9, 0.6, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor="#FFFFFF", edgecolor="#7030A0", lw=1.5, zorder=5)
ax.add_patch(badge1)
ax.text(4.6, 4.48, "Skip Connection", fontsize=8.2, weight="bold", color="#7030A0", ha="center", va="center", zorder=6)
ax.text(4.6, 4.25, "(Ghép 20x20)", fontsize=7.5, color="#1E1E24", ha="center", va="center", zorder=6)

ax.annotate("", xy=(3.65, 4.4), xytext=(3.4, 4.4),
            arrowprops=dict(arrowstyle="-", lw=2.0, color="#7030A0", linestyle="dashed"))
ax.annotate("", xy=(5.8, 4.4), xytext=(5.55, 4.4),
            arrowprops=dict(arrowstyle="-|>", lw=2.0, color="#7030A0", linestyle="dashed", mutation_scale=14))

# Level 2: Enc2 (3.4) -> Badge2 (3.65 to 5.55) -> Dec1 (5.8)
badge2 = patches.FancyBboxPatch((3.65, 2.2), 1.9, 0.6, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor="#FFFFFF", edgecolor="#1C6FA6", lw=1.5, zorder=5)
ax.add_patch(badge2)
ax.text(4.6, 2.58, "Skip Connection", fontsize=8.2, weight="bold", color="#1C6FA6", ha="center", va="center", zorder=6)
ax.text(4.6, 2.35, "(Ghép 10x10)", fontsize=7.5, color="#1E1E24", ha="center", va="center", zorder=6)

ax.annotate("", xy=(3.65, 2.5), xytext=(3.4, 2.5),
            arrowprops=dict(arrowstyle="-", lw=2.0, color="#1C6FA6", linestyle="dashed"))
ax.annotate("", xy=(5.8, 2.5), xytext=(5.55, 2.5),
            arrowprops=dict(arrowstyle="-|>", lw=2.0, color="#1C6FA6", linestyle="dashed", mutation_scale=14))

# Loss banner at bottom
loss_b = patches.FancyBboxPatch((1.6, -0.1), 6.0, 0.42, boxstyle="round,pad=0.06,rounding_size=0.1",
                                facecolor="#F3F4F6", edgecolor="#9CA3AF", lw=1.0)
ax.add_patch(loss_b)
ax.text(4.6, 0.11, "Hàm Loss Kết Hợp: BCE-Dice Loss | F1 = 0.942 | IoU = 0.891", 
        fontsize=9.0, weight="bold", color="#1E1E24", ha="center", va="center")

ax.set_xlim(0, 9.2)
ax.set_ylim(-0.2, 5.6)
plt.tight_layout()
plt.savefig("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/unet_diagram.png", dpi=220, bbox_inches="tight")
plt.close()
print("Saved perfect unet_diagram.png")
