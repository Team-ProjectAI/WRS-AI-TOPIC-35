import matplotlib.pyplot as plt
from PIL import Image

# Load current raw screenshot
raw_im = Image.open("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/tactical_map_demo.png")

fig, ax = plt.subplots(figsize=(6.5, 5.6), dpi=220)
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#0F172A")
ax.axis("off")

# Title at top of card
ax.text(0.5, 0.96, "Giao diện Tác chiến Streamlit 2D Real-time", 
        ha="center", va="top", transform=ax.transAxes,
        fontsize=11.5, weight="bold", color="#7030A0")

# Inset tactical map image
ax_in = fig.add_axes([0.05, 0.08, 0.90, 0.82])
ax_in.imshow(raw_im)
ax_in.axis("off")

# Add a stylish border around screenshot
for spine in ax_in.spines.values():
    spine.set_edgecolor("#38BDF8")
    spine.set_linewidth(1.5)
    spine.set_visible(True)

plt.savefig("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/tactical_map_demo_styled.png", dpi=220, bbox_inches="tight")
plt.close()
print("Saved tactical_map_demo_styled.png")
