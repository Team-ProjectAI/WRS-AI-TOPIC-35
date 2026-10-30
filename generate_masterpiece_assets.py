import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ASSET_DIR = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets"
os.makedirs(ASSET_DIR, exist_ok=True)

# 1. SLIDE 1: Cinematic High-Tech Title Banner (1920 x 520)
def create_hero_banner():
    w, h = 1920, 520
    im = Image.new("RGBA", (w, h), (18, 10, 42, 255))
    draw = ImageDraw.Draw(im)
    
    # 1. Dark cosmic gradient
    for y in range(h):
        ratio = y / h
        r = int(18 * (1 - ratio) + 28 * ratio)
        g = int(10 * (1 - ratio) + 12 * ratio)
        b = int(42 * (1 - ratio) + 68 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
    # 2. Glowing isometric terrain grid on right
    grid_surf = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_surf)
    for x in range(int(w * 0.35), w + 200, 60):
        gdraw.line([(x, int(h * 0.15)), (x - 350, h)], fill=(120, 70, 200, 45), width=1)
    for y in range(int(h * 0.15), h, 35):
        gdraw.line([(int(w * 0.35) - 350, y), (w + 200, y)], fill=(120, 70, 200, 45), width=1)
    im = Image.alpha_composite(im, grid_surf)
    
    # 3. Wildfire heat front (orange/red glowing particles)
    np.random.seed(108)
    fire_surf = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fire_surf)
    for _ in range(60):
        cx = np.random.randint(int(w * 0.65), int(w * 0.98))
        cy = np.random.randint(int(h * 0.2), int(h * 0.88))
        rad = np.random.randint(15, 65)
        alpha = np.random.randint(30, 90)
        fdraw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(235, 75, 30, alpha))
    for _ in range(30):
        cx = np.random.randint(int(w * 0.72), int(w * 0.95))
        cy = np.random.randint(int(h * 0.3), int(h * 0.8))
        rad = np.random.randint(8, 25)
        fdraw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(255, 190, 40, 140))
    fire_surf = fire_surf.filter(ImageFilter.GaussianBlur(8))
    im = Image.alpha_composite(im, fire_surf)
    
    # 4. Swarm Robot Nodes & High-Tech Blue Trajectory Vectors
    swarm_surf = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(swarm_surf)
    pts = [
        (int(w * 0.12), int(h * 0.72)),
        (int(w * 0.25), int(h * 0.58)),
        (int(w * 0.38), int(h * 0.68)),
        (int(w * 0.52), int(h * 0.45)),
        (int(w * 0.64), int(h * 0.35))
    ]
    for i in range(len(pts) - 1):
        sdraw.line([pts[i], pts[i+1]], fill=(0, 215, 255, 180), width=3)
        # pulses
        mx = (pts[i][0] + pts[i+1][0]) // 2
        my = (pts[i][1] + pts[i+1][1]) // 2
        sdraw.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(255, 255, 255, 220))
        
    for idx, (px, py) in enumerate(pts):
        # glow
        sdraw.ellipse([px - 22, py - 22, px + 22, py + 22], fill=(0, 180, 255, 60))
        sdraw.ellipse([px - 14, py - 14, px + 14, py + 14], fill=(14, 165, 233, 240))
        sdraw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(255, 255, 255, 255))
    im = Image.alpha_composite(im, swarm_surf)
    
    # 5. Left cyber badge
    draw = ImageDraw.Draw(im)
    draw.rectangle([int(w * 0.08), int(h * 0.18), int(w * 0.08) + 6, int(h * 0.82)], fill=(245, 158, 11))
    
    out_path = os.path.join(ASSET_DIR, "title_hero.png")
    im.convert("RGB").save(out_path, quality=95)
    print("Created high-res title_hero.png")

# 2. SLIDE 4: 4-Layer Architecture Diagram (Publication-grade, 2400 x 780)
def create_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(12, 3.9), dpi=220)
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
    y0 = 0.8
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
            
    # Feedback loop arrow (Dynamic Replanning)
    ax.annotate("", xy=(1.58, y0 - 0.12), xytext=(10.25, y0 - 0.12),
                arrowprops=dict(arrowstyle="->", lw=2.2, color="#B3236F", linestyle="dashed",
                                connectionstyle="arc3,rad=-0.16"))
    ax.text(5.9, y0 - 0.46, "Dynamic Replanning Feedback Loop (Tái điều phối tức thời khi ngọn lửa chia cắt)",
            color="#B3236F", weight="bold", fontsize=10.2, ha="center", va="center")

    ax.set_xlim(0, 12)
    ax.set_ylim(0.1, 3.8)
    plt.tight_layout()
    out_path = os.path.join(ASSET_DIR, "pipeline_diagram.png")
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print("Created professional pipeline_diagram.png")

# 3. SLIDE 5: Publication-grade U-Net Architecture (1400 x 1200)
def create_unet_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 5.6), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")
    
    ax.text(3.25, 5.25, "Kiến trúc Mạng PyTorch U-Net 2D", ha="center", va="center",
            fontsize=13, weight="bold", color="#7030A0")
    
    # Blocks definition: (name, x, y, w, h, fill, border, label)
    blocks = [
        # Input Tensor
        ("Input", 0.3, 3.6, 0.9, 0.9, "#F1ECF8", "#7030A0", "5 Kênh\n(5x20x20)"),
        # Encoder 1
        ("Enc1", 1.5, 3.2, 0.8, 1.7, "#E1F0FA", "#1C6FA6", "Conv 32\n(20x20)"),
        # Encoder 2
        ("Enc2", 2.6, 2.3, 0.8, 2.6, "#E1F0FA", "#1C6FA6", "Conv 64\n(10x10)"),
        # Bottleneck
        ("Bottle", 3.7, 1.4, 0.8, 3.5, "#FBE3F0", "#B3236F", "Latent 128\n(5x5)"),
        # Decoder 1
        ("Dec1", 4.8, 2.3, 0.8, 2.6, "#DCFCE7", "#15803D", "UpConv 64\n(10x10)"),
        # Decoder 0
        ("Dec0", 5.9, 3.2, 0.8, 1.7, "#DCFCE7", "#15803D", "UpConv 32\n(20x20)"),
    ]
    
    for name, bx, by, bw, bh, bfill, bborder, blabel in blocks:
        patch = patches.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.06,rounding_size=0.1",
                                       facecolor=bfill, edgecolor=bborder, linewidth=2)
        ax.add_patch(patch)
        ax.text(bx + bw/2, by + bh/2, blabel, ha="center", va="center", fontsize=8.8, weight="bold", color="#1E1E24")
        
    # Input to Enc1 arrow
    ax.annotate("", xy=(1.5, 4.05), xytext=(1.2, 4.05),
                arrowprops=dict(arrowstyle="->", lw=2, color="#7030A0"))
    
    # Down arrows (Maxpool)
    ax.annotate("", xy=(2.6, 3.6), xytext=(2.3, 4.0),
                arrowprops=dict(arrowstyle="->", lw=2, color="#1C6FA6"))
    ax.text(2.4, 4.1, "MaxPool", fontsize=7.5, color="#1C6FA6", ha="center")
    
    ax.annotate("", xy=(3.7, 3.1), xytext=(3.4, 3.6),
                arrowprops=dict(arrowstyle="->", lw=2, color="#1C6FA6"))
    ax.text(3.5, 3.7, "MaxPool", fontsize=7.5, color="#1C6FA6", ha="center")
    
    # Up arrows (UpConv)
    ax.annotate("", xy=(4.8, 3.6), xytext=(4.5, 3.1),
                arrowprops=dict(arrowstyle="->", lw=2, color="#15803D"))
    ax.annotate("", xy=(5.9, 4.0), xytext=(5.6, 3.6),
                arrowprops=dict(arrowstyle="->", lw=2, color="#15803D"))
    
    # Skip Connection (Horizontal purple bridges)
    ax.annotate("", xy=(5.9, 4.2), xytext=(2.3, 4.2),
                arrowprops=dict(arrowstyle="->", lw=2.2, color="#7030A0", linestyle="dashed"))
    # Badge over skip connection
    sb = patches.FancyBboxPatch((3.3, 4.02), 1.6, 0.36, boxstyle="round,pad=0.04,rounding_size=0.08",
                                facecolor="#F1ECF8", edgecolor="#7030A0", lw=1.2)
    ax.add_patch(sb)
    ax.text(4.1, 4.2, "Skip Connection", fontsize=8.2, weight="bold", color="#7030A0", ha="center", va="center")
    
    # Output Heatmap Box below Dec0
    out_box = patches.FancyBboxPatch((2.2, 0.3), 3.0, 0.75, boxstyle="round,pad=0.06,rounding_size=0.1",
                                     facecolor="#FEF3C7", edgecolor="#B45309", lw=2)
    ax.add_patch(out_box)
    ax.text(3.7, 0.67, "Heatmap Rủi Ro Lửa (1 x 20 x 20)", fontsize=9.2, weight="bold", color="#B45309", ha="center")
    ax.text(3.7, 0.45, "Xác suất cháy P(x, y) ∈ [0, 1] cho A*", fontsize=8.0, color="#1E1E24", ha="center")
    
    # Dec0 to Output arrow
    ax.annotate("", xy=(4.8, 1.05), xytext=(6.3, 3.2),
                arrowprops=dict(arrowstyle="->", lw=2.0, color="#B45309", connectionstyle="arc3,rad=0.25"))

    ax.set_xlim(0, 7.0)
    ax.set_ylim(0, 5.6)
    plt.tight_layout()
    out_path = os.path.join(ASSET_DIR, "unet_diagram.png")
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print("Created publication unet_diagram.png")

# 4. SLIDE 8: Fire Pathfinding Tactical Map (1400 x 1200)
def create_fire_path_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 5.6), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#0F172A") # Tactical Dark Map
    
    # Create smooth wildfire contour
    x = np.linspace(0, 20, 120)
    y = np.linspace(0, 20, 120)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-((X - 10)**2 + (Y - 10)**2) / 14) + 0.6 * np.exp(-((X - 14)**2 + (Y - 8.5)**2) / 9)
    
    # Dark tactical grid
    for i in range(0, 21, 2):
        ax.axhline(i, color="#1E293B", lw=0.6, linestyle=":")
        ax.axvline(i, color="#1E293B", lw=0.6, linestyle=":")
        
    # Heatmap contour
    cf = ax.contourf(X, Y, Z, levels=18, cmap="inferno", alpha=0.88)
    
    # Start Robot
    r_pos = (2.2, 10.0)
    ax.scatter([r_pos[0]], [r_pos[1]], s=320, c="#0284C7", edgecolors="#FFFFFF", lw=2.5, zorder=10)
    ax.text(r_pos[0], r_pos[1] - 1.2, "Robot R1", color="#38BDF8", weight="bold", fontsize=9.5, ha="center")
    
    # Goal Victim
    v_pos = (17.8, 10.0)
    ax.scatter([v_pos[0]], [v_pos[1]], s=320, c="#EAB308", edgecolors="#000000", lw=2.5, zorder=10)
    ax.text(v_pos[0], v_pos[1] - 1.2, "Nạn nhân V2", color="#FDE047", weight="bold", fontsize=9.5, ha="center")
    
    # Trapped Greedy Path
    gx = np.linspace(2.2, 10.5, 25)
    gy = np.linspace(10.0, 10.0, 25)
    ax.plot(gx, gy, color="#EF4444", lw=3.5, linestyle="--", zorder=7)
    # Fire Trap explosion marker
    ax.scatter([10.5], [10.0], s=380, marker="X", c="#EF4444", edgecolors="#FFFFFF", lw=2, zorder=11)
    
    # Trap badge
    badge = patches.FancyBboxPatch((8.8, 11.0), 3.4, 1.2, boxstyle="round,pad=0.1,rounding_size=0.2",
                                   facecolor="#7F1D1D", edgecolor="#EF4444", lw=1.5, zorder=12)
    ax.add_patch(badge)
    ax.text(10.5, 11.8, "BẪY LỬA GREEDY [X]", color="#FCA5A5", weight="bold", fontsize=8.8, ha="center", zorder=13)
    ax.text(10.5, 11.3, "Phơi nhiễm rủi ro = 0.88", color="#FFFFFF", fontsize=7.8, ha="center", zorder=13)
    
    # Safe Fire-Aware A* Arc Path
    theta = np.linspace(np.pi, 0, 40)
    safe_x = 10.0 - 7.8 * np.cos(theta)
    safe_y = 10.0 + 6.6 * np.sin(theta)
    ax.plot(safe_x, safe_y, color="#10B981", lw=4.2, zorder=8)
    
    # Safe badge
    s_badge = patches.FancyBboxPatch((8.2, 17.2), 3.6, 1.1, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor="#064E3B", edgecolor="#10B981", lw=1.5, zorder=12)
    ax.add_patch(s_badge)
    ax.text(10.0, 17.9, "FIRE-AWARE A* [OK]", color="#6EE7B7", weight="bold", fontsize=8.8, ha="center", zorder=13)
    ax.text(10.0, 17.4, "Né lửa an toàn 100%", color="#FFFFFF", fontsize=7.8, ha="center", zorder=13)
    
    ax.set_title("Hành lang Tác chiến: Né Lửa An Toàn vs Sa Bẫy", fontsize=11.5, weight="bold", color="#1E1E24", pad=12)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.tight_layout()
    out_path = os.path.join(ASSET_DIR, "fire_path_diagram.png")
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print("Created high-res fire_path_diagram.png")

# 5. SLIDE 12: Executive Benchmark Dual Card (1400 x 1200)
def create_benchmark_chart():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5.6), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    
    methods = ["Greedy Baseline", "Standard A*", "Proposed Hybrid AI"]
    rescue_rates = [40.0, 60.0, 100.0]
    fire_risks = [0.4280, 0.3150, 0.0039]
    colors = ["#F87171", "#FBBF24", "#34D399"]
    borders = ["#DC2626", "#D97706", "#059669"]
    
    # Chart 1: Rescue Rate
    ax1.set_facecolor("#FAFAFC")
    bars1 = ax1.bar(methods, rescue_rates, color=colors, edgecolor=borders, width=0.48, lw=1.8, zorder=3)
    ax1.set_ylabel("Tỉ Lệ Cứu Hộ (%)", fontsize=9.5, weight="bold", color="#1E1E24")
    ax1.set_title("Tỉ Lệ Cứu Hộ Nạn Nhân Thành Công (10 Scenarios Unseen)", fontsize=10.5, weight="bold", color="#7030A0", pad=8)
    ax1.set_ylim(0, 125)
    ax1.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    for b in bars1:
        yv = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, yv + 4, f"{yv:.1f}%", ha="center", weight="bold", fontsize=10, color="#1E1E24")
        
    # Chart 2: Fire Risk
    ax2.set_facecolor("#FAFAFC")
    bars2 = ax2.bar(methods, fire_risks, color=colors, edgecolor=borders, width=0.48, lw=1.8, zorder=3)
    ax2.set_ylabel("Rủi Ro Lửa TB", fontsize=9.5, weight="bold", color="#1E1E24")
    ax2.set_title("Rủi Ro Phơi Nhiễm Lửa Tích Lũy (Càng thấp càng an toàn)", fontsize=10.5, weight="bold", color="#7030A0", pad=8)
    ax2.set_ylim(0, 0.54)
    ax2.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    for b in bars2:
        yv = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, yv + 0.018, f"{yv:.4f}", ha="center", weight="bold", fontsize=10, color="#1E1E24")
        
    for ax in (ax1, ax2):
        ax.tick_params(colors="#1E1E24", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color("#E2E8F0")
            
    plt.tight_layout()
    out_path = os.path.join(ASSET_DIR, "benchmark_chart.png")
    plt.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close()
    print("Created executive benchmark_chart.png")

if __name__ == "__main__":
    create_hero_banner()
    create_pipeline_diagram()
    create_unet_diagram()
    create_fire_path_diagram()
    create_benchmark_chart()
    print("All masterpiece slide visual assets rendered successfully!")
