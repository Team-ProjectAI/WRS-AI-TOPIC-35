from PIL import Image, ImageDraw, ImageFont

# Load both user images
im_map = Image.open("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/tactical_map_demo.png")
im_top = Image.open("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/dashboard_overview.jpg")

# The map image is 1024 x 435. It shows the real full simulation!
# Let's create a high-fidelity showcase image with a stylish laptop/browser frame
w, h = 1024, 435
frame_w, frame_h = w + 20, h + 50
canvas = Image.new("RGB", (frame_w, frame_h), (15, 23, 42))
draw = ImageDraw.Draw(canvas)

# Browser header bar
draw.rectangle([0, 0, frame_w, 36], fill=(30, 41, 59))
# Window buttons
draw.ellipse([14, 12, 24, 22], fill=(239, 68, 68))
draw.ellipse([32, 12, 42, 22], fill=(245, 158, 11))
draw.ellipse([50, 12, 60, 22], fill=(16, 185, 129))

# URL bar
draw.rectangle([90, 8, frame_w - 90, 28], fill=(15, 23, 42))

# Paste dashboard
canvas.paste(im_map, (10, 40))

# Border around entire canvas
draw.rectangle([0, 0, frame_w - 1, frame_h - 1], outline=(56, 189, 248), width=2)

canvas.save("/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets/dashboard_mockup.png", quality=95)
print("Saved dashboard_mockup.png:", canvas.size)
