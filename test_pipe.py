import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(12, 4.4), dpi=220)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")
ax.axis("off")

layers = [
    {
        "tag": "TẦNG 1",
        "name": "PyTorch U-Net 2D",
        "bullets": ["Dự báo Rủi ro Lửa", "5 Kênh Đa phổ Đầu vào", "Mô hình Heatmap 2D"],
        "theme": "#7030A0",
        "bg": "#F5F0FB"
    },
    {
        "tag": "TẦNG 2",
        "name": "PettingZoo AEC",
        "bullets": ["Môi trường Đa tác tử", "Cellular Automata (CA)", "Gió & Thực bì Động học"],
        "theme": "#1C6FA6",
        "bg": "#EDF6FD"
    },
    {
        "tag": "TẦNG 3",
        "name": "Swarm PSO (pymoo)",
        "bullets": ["Trí tuệ Bầy đàn Phân công", "Hàm Group Fitness", "Tối ưu hóa Cân bằng Tải"],
        "theme": "#B3236F",
        "bg": "#FDF0F7"
    },
    {
        "tag": "TẦNG 4",
        "name": "Fire-Aware A*",
        "bullets": ["Hoạch định Tuyến Né lửa", "Phạt Rủi ro lambda=15.0", "Dynamic Replanning < 1ms"],
        "theme": "#15803D",
        "bg": "#EDFAF1"
    }
]

bw, bh = 2.45, 2.5
y0 = 1.35  # plenty of room below
for i, l in enumerate(layers):
    x0 = 0.35 + i * 2.85
    
    # Outer Card with gentle rounded corner
    card = patches.FancyBboxPatch((x0, y0), bw, bh, boxstyle="round,pad=0.1,rounding_size=0.14",
                                  facecolor=l["bg"], edgecolor=l["theme"], linewidth=2.0)
    ax.add_patch(card)
    
    # Tag Badge
    badge = patches.FancyBboxPatch((x0 + 0.3, y0 + bh - 0.45), bw - 0.6, 0.36,
                                   boxstyle="round,pad=0.06,rounding_size=0.08",
                                   facecolor=l["theme"], edgecolor="none")
    ax.add_patch(badge)
    ax.text(x0 + bw/2, y0 + bh - 0.27, l["tag"], color="white", weight="bold", fontsize=10.5, ha="center", va="center")
    
    # Layer Name
    ax.text(x0 + bw/2, y0 + bh - 0.85, l["name"], color=l["theme"], weight="bold", fontsize=11.5, ha="center", va="center")
    
    # Bullet list inside card
    for b_idx, b_text in enumerate(l["bullets"]):
        by = y0 + bh - 1.25 - b_idx * 0.34
        ax.scatter([x0 + 0.3], [by], color=l["theme"], s=20, zorder=5)
        ax.text(x0 + 0.42, by, b_text, color="#1E1E24", fontsize=9.2, va="center", ha="left")
        
    # Connect Arrow
    if i < 3:
        ax.annotate("", xy=(x0 + bw + 0.35, y0 + bh/2), xytext=(x0 + bw + 0.05, y0 + bh/2),
                    arrowprops=dict(arrowstyle="-|>", lw=2.8, color="#7030A0", mutation_scale=18))
        
# Dynamic loop arrow
ax.annotate("", xy=(1.58, y0 - 0.35), xytext=(10.25, y0 - 0.35),
            arrowprops=dict(arrowstyle="->", lw=2.2, color="#B3236F", linestyle="dashed",
                            connectionstyle="arc3,rad=-0.12"))
# Put text ABOVE the arrow arc, between boxes and arrow!
ax.text(5.9, y0 - 0.22, "Dynamic Replanning Loop (Tái điều phối tức thời khi ngọn lửa chia cắt)",
        color="#B3236F", weight="bold", fontsize=10.2, ha="center", va="center")

ax.set_xlim(0, 12)
ax.set_ylim(0.2, 4.4)
plt.tight_layout()
plt.savefig("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/pipeline_diagram.png", dpi=220, bbox_inches="tight")
plt.close()
print("Saved clean pipeline_diagram.png")
