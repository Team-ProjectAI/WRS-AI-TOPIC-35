import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets"
os.makedirs(ASSET_DIR, exist_ok=True)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

# 1. Slide 1: High-Tech Hero Banner (ratio ~ 3.7)
def generate_title_hero():
    w, h = 1920, 500
    im = Image.new("RGB", (w, h), color=(26, 11, 46))
    draw = ImageDraw.Draw(im)
    
    # Background gradient
    for y in range(h):
        r = int(26 + (14 - 26) * (y / h))
        g = int(11 + (14 - 11) * (y / h))
        b = int(46 + (28 - 46) * (y / h))
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Perspective grid lines
    for x in range(0, w, 70):
        draw.line([(x, int(h * 0.35)), (int((x - w/2) * 2.5 + w/2), h)], fill=(75, 35, 125), width=1)
    for y in range(int(h * 0.35), h, 35):
        draw.line([(0, y), (w, y)], fill=(75, 35, 125), width=1)
        
    # Fire nodes and heat aura
    np.random.seed(42)
    for _ in range(45):
        cx = np.random.randint(int(w * 0.52), int(w * 0.96))
        cy = np.random.randint(int(h * 0.25), int(h * 0.88))
        rad = np.random.randint(18, 55)
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=(225, 65, 35, 100))
        
    # Robot nodes & swarm trajectories
    for i in range(5):
        rx = int(w * 0.12 + i * 150)
        ry = int(h * 0.68 - i * 22)
        draw.ellipse([rx - 18, ry - 18, rx + 18, ry + 18], fill=(30, 150, 240))
        draw.ellipse([rx - 8, ry - 8, rx + 8, ry + 8], fill=(255, 255, 255))
        if i > 0:
            prev_rx = int(w * 0.12 + (i - 1) * 150)
            prev_ry = int(h * 0.68 - (i - 1) * 22)
            draw.line([(prev_rx, prev_ry), (rx, ry)], fill=(0, 230, 255), width=3)
            
    im.save(os.path.join(ASSET_DIR, "title_hero.png"))
    print("Generated title_hero.png (1920x500)")

# 2. Slide 4: Wide 4-Layer Architecture Flowchart (ratio = 12 / 3.8 = 3.16)
def generate_architecture_flowchart():
    fig, ax = plt.subplots(figsize=(12, 3.8), dpi=200)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.axis("off")
    
    layers = [
        {"num": "TẦNG 1", "title": "PyTorch U-Net 2D", "sub": "Dự báo Nguy cơ Cháy\n(5 Kênh đầu vào -> Heatmap 2D)", "color": "#7030A0", "bg": "#F1ECF8"},
        {"num": "TẦNG 2", "title": "PettingZoo AEC", "sub": "Môi trường Đa tác tử\n(Cellular Automata + Gió + Thực bì)", "color": "#1C6FA6", "bg": "#E1F0FA"},
        {"num": "TẦNG 3", "title": "Swarm PSO (pymoo)", "sub": "Phân công Cứu hộ Bầy đàn\n(Tối ưu hóa Group Fitness)", "color": "#B3236F", "bg": "#FBE3F0"},
        {"num": "TẦNG 4", "title": "Fire-Aware A*", "sub": "Hoạch định Tuyến Né lửa\n(Dynamic Replanning < 1ms)", "color": "#15803D", "bg": "#DCFCE7"},
    ]
    
    bw, bh = 2.45, 2.5
    y_pos = 0.75
    for i, l in enumerate(layers):
        x_pos = 0.35 + i * 2.85
        # Rounded container
        box = patches.FancyBboxPatch((x_pos, y_pos), bw, bh, boxstyle="round,pad=0.12,rounding_size=0.15",
                                     linewidth=2.5, edgecolor=l["color"], facecolor=l["bg"])
        ax.add_patch(box)
        
        # Header pill
        pill = patches.FancyBboxPatch((x_pos + 0.2, y_pos + bh - 0.55), bw - 0.4, 0.42,
                                      boxstyle="round,pad=0.06,rounding_size=0.1",
                                      facecolor=l["color"], edgecolor="none")
        ax.add_patch(pill)
        ax.text(x_pos + bw/2, y_pos + bh - 0.34, l["num"], ha="center", va="center", color="white", weight="bold", fontsize=11.5)
        
        # Layer title
        ax.text(x_pos + bw/2, y_pos + bh - 0.95, l["title"], ha="center", va="center", color=l["color"], weight="bold", fontsize=12)
        # Layer subtext
        ax.text(x_pos + bw/2, y_pos + 0.68, l["sub"], ha="center", va="center", color="#1E1E24", fontsize=10, linespacing=1.35)
        
        # Forward Arrow
        if i < 3:
            ax.annotate("", xy=(x_pos + bw + 0.32, y_pos + bh/2), xytext=(x_pos + bw + 0.04, y_pos + bh/2),
                        arrowprops=dict(arrowstyle="-|>", lw=3, color="#7030A0", mutation_scale=18))
            
    # Feedback dynamic loop arrow
    ax.annotate("Dynamic Replanning Loop (Tái kích hoạt khi ngọn lửa chia cắt)",
                xy=(1.58, y_pos - 0.15), xytext=(10.15, y_pos - 0.15),
                arrowprops=dict(arrowstyle="->", lw=2.2, color="#B3236F", linestyle="dashed",
                                connectionstyle="arc3,rad=-0.16"),
                ha="center", va="top", color="#B3236F", weight="bold", fontsize=11)

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3.8)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSET_DIR, "pipeline_diagram.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("Generated pipeline_diagram.png (12x3.8)")

# 3. Slide 5: U-Net Architecture (ratio = 6.5 / 5.6 = 1.16)
def generate_unet_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 5.6), dpi=200)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")
    ax.axis("off")
    
    # Title
    ax.text(3.25, 5.3, "Kiến trúc PyTorch U-Net 2D (5 Kênh)", ha="center", va="center", fontsize=13, weight="bold", color="#7030A0")
    
    # Input
    ax.text(0.9, 4.4, "Đầu vào 5 Kênh\n(5 x 20 x 20)", ha="center", va="center", fontsize=9.5, weight="bold", color="#7030A0")
    b_in = patches.Rectangle((0.4, 3.2), 1.0, 0.7, facecolor="#F1ECF8", edgecolor="#7030A0", lw=2)
    ax.add_patch(b_in)
    ax.text(0.9, 3.55, "Fire, Fuel\nWind, DEM", ha="center", va="center", fontsize=8.5, color="#1E1E24")
    
    # Enc1
    b_e1 = patches.Rectangle((1.8, 2.4), 0.9, 1.5, facecolor="#E1F0FA", edgecolor="#1C6FA6", lw=2)
    ax.add_patch(b_e1)
    ax.text(2.25, 3.15, "Conv 32\n20x20", ha="center", va="center", fontsize=9, weight="bold", color="#1C6FA6")
    
    # Enc2
    b_e2 = patches.Rectangle((2.9, 1.4), 0.9, 2.5, facecolor="#E1F0FA", edgecolor="#1C6FA6", lw=2)
    ax.add_patch(b_e2)
    ax.text(3.35, 2.65, "Conv 64\n10x10", ha="center", va="center", fontsize=9, weight="bold", color="#1C6FA6")
    
    # Dec1
    b_d1 = patches.Rectangle((4.0, 1.4), 0.9, 2.5, facecolor="#DCFCE7", edgecolor="#15803D", lw=2)
    ax.add_patch(b_d1)
    ax.text(4.45, 2.65, "UpConv 64\n10x10", ha="center", va="center", fontsize=9, weight="bold", color="#15803D")
    
    # Dec0
    b_d0 = patches.Rectangle((5.1, 2.4), 0.9, 1.5, facecolor="#DCFCE7", edgecolor="#15803D", lw=2)
    ax.add_patch(b_d0)
    ax.text(5.55, 3.15, "UpConv 32\n20x20", ha="center", va="center", fontsize=9, weight="bold", color="#15803D")
    
    # Skip connections
    ax.annotate("", xy=(5.1, 3.15), xytext=(2.7, 3.15),
                arrowprops=dict(arrowstyle="->", lw=2, color="#7030A0", linestyle="dashed"))
    ax.text(3.9, 3.35, "Skip Connection", ha="center", color="#7030A0", fontsize=8.5, weight="bold")
    
    # Output Heatmap
    b_out = patches.Rectangle((2.6, 0.2), 1.3, 0.7, facecolor="#FEF3C7", edgecolor="#B45309", lw=2)
    ax.add_patch(b_out)
    ax.text(3.25, 0.55, "Heatmap Rủi Ro\n(1 x 20 x 20)", ha="center", va="center", fontsize=9, weight="bold", color="#B45309")
    
    # Connect Dec0 to Output
    ax.annotate("", xy=(3.9, 0.55), xytext=(5.55, 2.4),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#B45309", connectionstyle="arc3,rad=0.2"))

    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 5.6)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSET_DIR, "unet_diagram.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("Generated unet_diagram.png (6.5x5.6)")

# 4. Slide 8: Fire Path Diagram (ratio = 6.5 / 5.6 = 1.16)
def generate_fire_path_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 5.6), dpi=200)
    ax.set_facecolor("#0F172A")
    fig.patch.set_facecolor("#FFFFFF")
    
    x = np.linspace(0, 20, 100)
    y = np.linspace(0, 20, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-((X - 10)**2 + (Y - 10)**2) / 14) + 0.5 * np.exp(-((X - 13.5)**2 + (Y - 8)**2) / 8)
    ax.contourf(X, Y, Z, levels=14, cmap="inferno", alpha=0.85)
    
    start = (2.5, 10)
    goal = (17.5, 10)
    ax.scatter([start[0]], [start[1]], c="#38BDF8", s=220, zorder=5, label="Robot Khởi hành (2, 10)", edgecolors="white", linewidth=2)
    ax.scatter([goal[0]], [goal[1]], c="#FACC15", s=220, zorder=5, label="Nạn nhân (18, 10)", edgecolors="black", linewidth=2)
    
    # Greedy Path (Trapped)
    greedy_x = np.linspace(2.5, 10.5, 20)
    greedy_y = np.linspace(10, 10, 20)
    ax.plot(greedy_x, greedy_y, color="#EF4444", lw=3.2, linestyle="--", label="Greedy (Bị thiêu rụi)")
    ax.scatter([10.5], [10], c="#EF4444", s=300, marker="X", zorder=6)
    ax.text(10.5, 11.2, "BẪY LỬA!", color="#FCA5A5", weight="bold", fontsize=11, ha="center")
    
    # Safe Fire-Aware A* Path
    theta = np.linspace(np.pi, 0, 30)
    safe_x = 10 - 7.5 * np.cos(theta)
    safe_y = 10 + 6.2 * np.sin(theta)
    ax.plot(safe_x, safe_y, color="#22C55E", lw=3.8, label="Fire-Aware A* (Né lửa 100%)")
    
    ax.set_title("Quỹ đạo Di chuyển: Né lửa vs Sa bẫy", fontsize=12, weight="bold", color="#111827", pad=10)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=8.8, frameon=True, facecolor="#F3F4F6")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.grid(color="#334155", linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(ASSET_DIR, "fire_path_diagram.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("Generated fire_path_diagram.png (6.5x5.6)")

# 5. Slide 12: Benchmark Dual Chart (Vertical Stacked, ratio = 6.5 / 5.6 = 1.16)
def generate_benchmark_chart():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5.6), dpi=200)
    fig.patch.set_facecolor("#FFFFFF")
    
    methods = ["Greedy Baseline", "Standard A*", "Proposed Hybrid AI"]
    rescue_rates = [40.0, 60.0, 100.0]
    fire_risks = [0.428, 0.315, 0.0039]
    colors = ["#EF4444", "#F59E0B", "#10B981"]
    
    # Ax1: Rescue Rate
    bars1 = ax1.bar(methods, rescue_rates, color=colors, width=0.45, edgecolor="#1E1E24", lw=1)
    ax1.set_ylabel("Tỉ Lệ Cứu Hộ (%)", fontsize=10, weight="bold", color="#1E1E24")
    ax1.set_title("Tỉ Lệ Cứu Hộ Thành Công (10 Scenarios)", fontsize=11, weight="bold", color="#7030A0")
    ax1.set_ylim(0, 120)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 3, f"{yval:.1f}%", ha="center", va="bottom", weight="bold", fontsize=10)
        
    # Ax2: Fire Risk
    bars2 = ax2.bar(methods, fire_risks, color=colors, width=0.45, edgecolor="#1E1E24", lw=1)
    ax2.set_ylabel("Rủi Ro Lửa TB", fontsize=10, weight="bold", color="#1E1E24")
    ax2.set_title("Rủi Ro Phơi Nhiễm Lửa Tích Lũy (Càng thấp càng an toàn)", fontsize=11, weight="bold", color="#7030A0")
    ax2.set_ylim(0, 0.52)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.015, f"{yval:.4f}", ha="center", va="bottom", weight="bold", fontsize=10)
        
    for ax in (ax1, ax2):
        ax.set_facecolor("#F9FAFB")
        ax.tick_params(colors="#1E1E24", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color("#E5E7EB")
            
    plt.tight_layout()
    plt.savefig(os.path.join(ASSET_DIR, "benchmark_chart.png"), dpi=200, bbox_inches="tight")
    plt.close()
    print("Generated benchmark_chart.png (6.5x5.6 vertical stacked)")

if __name__ == "__main__":
    generate_title_hero()
    generate_architecture_flowchart()
    generate_unet_diagram()
    generate_fire_path_diagram()
    generate_benchmark_chart()
    print("All slide visual assets updated with ideal aspect ratios!")
