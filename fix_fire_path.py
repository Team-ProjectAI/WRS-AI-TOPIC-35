import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ASSET_DIR = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets"

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
ax.text(r_pos[0], r_pos[1] - 1.3, "Robot R1", color="#38BDF8", weight="bold", fontsize=9.5, ha="center")

# Goal Victim
v_pos = (17.8, 10.0)
ax.scatter([v_pos[0]], [v_pos[1]], s=320, c="#EAB308", edgecolors="#000000", lw=2.5, zorder=10)
ax.text(v_pos[0], v_pos[1] - 1.3, "Nạn nhân V2", color="#FDE047", weight="bold", fontsize=9.5, ha="center")

# Trapped Greedy Path
gx = np.linspace(2.2, 10.5, 25)
gy = np.linspace(10.0, 10.0, 25)
ax.plot(gx, gy, color="#EF4444", lw=3.5, linestyle="--", zorder=7)

# Fire Trap explosion marker
ax.scatter([10.5], [10.0], s=380, marker="X", c="#EF4444", edgecolors="#FFFFFF", lw=2, zorder=11)

# Generous, spacious badge for Greedy Trap
# Center at (10.5, 11.8), width = 4.2, height = 1.6
# Box lower left: x = 10.5 - 2.1 = 8.4, y = 11.8 - 0.8 = 11.0
badge = patches.FancyBboxPatch((8.3, 10.9), 4.4, 1.7, boxstyle="round,pad=0.12,rounding_size=0.25",
                               facecolor="#7F1D1D", edgecolor="#EF4444", lw=1.8, zorder=12)
ax.add_patch(badge)
# Position lines with ample breathing room inside 1.7-tall box
ax.text(10.5, 12.0, "BẪY LỬA GREEDY [X]", color="#FCA5A5", weight="bold", fontsize=8.8, ha="center", va="center", zorder=13)
ax.text(10.5, 11.4, "Phơi nhiễm rủi ro = 0.88", color="#FFFFFF", fontsize=7.8, ha="center", va="center", zorder=13)

# Safe Fire-Aware A* Arc Path
theta = np.linspace(np.pi, 0, 40)
safe_x = 10.0 - 7.8 * np.cos(theta)
safe_y = 10.0 + 6.6 * np.sin(theta)
ax.plot(safe_x, safe_y, color="#10B981", lw=4.2, zorder=8)

# Spacious badge for Fire-Aware A*
# Arc apex is at (10.0, 16.6). Place badge above at y = 18.0
s_badge = patches.FancyBboxPatch((8.1, 17.2), 4.2, 1.7, boxstyle="round,pad=0.12,rounding_size=0.25",
                                 facecolor="#064E3B", edgecolor="#10B981", lw=1.8, zorder=12)
ax.add_patch(s_badge)
ax.text(10.2, 18.3, "FIRE-AWARE A* [OK]", color="#6EE7B7", weight="bold", fontsize=8.8, ha="center", va="center", zorder=13)
ax.text(10.2, 17.7, "Né lửa an toàn 100%", color="#FFFFFF", fontsize=7.8, ha="center", va="center", zorder=13)

ax.set_title("Hành lang Tác chiến: Né Lửa An Toàn vs Sa Bẫy", fontsize=11.5, weight="bold", color="#1E1E24", pad=12)
ax.set_xlim(0, 20)
ax.set_ylim(0, 20)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
out_path = os.path.join(ASSET_DIR, "fire_path_diagram.png")
plt.savefig(out_path, dpi=220, bbox_inches="tight")
plt.close()
print("Saved fixed fire_path_diagram.png")
