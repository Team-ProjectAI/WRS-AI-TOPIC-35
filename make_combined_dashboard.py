from PIL import Image, ImageDraw

im_map = Image.open("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/tactical_map_demo.png")
im_top = Image.open("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/dashboard_overview.jpg")

# Both are 1024 x 435
# Combine them into a single clean preview: Top = Settings/Telemetry, Bottom = Live Tactical Swarm Grid
w = 1024
total_h = 435 + 435 + 20
canvas = Image.new("RGB", (w + 24, total_h + 50), (15, 23, 42))
draw = ImageDraw.Draw(canvas)

# Window header
draw.rectangle([0, 0, w + 24, 34], fill=(30, 41, 59))
draw.ellipse([14, 11, 24, 21], fill=(239, 68, 68))
draw.ellipse([32, 11, 42, 21], fill=(245, 158, 11))
draw.ellipse([50, 11, 60, 21], fill=(16, 185, 129))

# Paste Top Overview
canvas.paste(im_top, (12, 42))
# Separator line
draw.line([(12, 42 + 435 + 8), (w + 12, 42 + 435 + 8)], fill=(56, 189, 248), width=2)
# Paste Tactical Map
canvas.paste(im_map, (12, 42 + 435 + 16))

# Border
draw.rectangle([0, 0, w + 23, total_h + 49], outline=(56, 189, 248), width=2)

out_p = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/dashboard_full_stack.png"
canvas.save(out_p, quality=95)
print("Saved dashboard_full_stack.png:", canvas.size, "ratio:", canvas.size[0] / canvas.size[1])
