import os
import pptx
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

# Brand Colors extracted directly from GCOS108-L5-Clustering.pdf
COLOR_TITLE = RGBColor(112, 48, 160)     # #7030A0 Deep Purple
COLOR_TEXT_MAIN = RGBColor(30, 30, 36)   # #1E1E24 Dark Body Text
COLOR_FOOTER = RGBColor(69, 69, 81)      # #454551 Neutral Slate

FONT_FAMILY = "Arial"

# Exact Pastel Bento Palette
PALETTE = {
    "purple": {
        "bg": RGBColor(241, 236, 248),    # #F1ECF8 Soft Lavender
        "title": RGBColor(112, 48, 160),  # #7030A0 Deep Purple
        "accent": RGBColor(80, 44, 209),  # #502CD1 Electric Indigo
    },
    "blue": {
        "bg": RGBColor(225, 240, 250),    # #E1F0FA Soft Sky
        "title": RGBColor(28, 111, 166),  # #1C6FA6 Deep Cyan/Blue
        "accent": RGBColor(2, 132, 199),  # #0284C7 Sky Blue
    },
    "pink": {
        "bg": RGBColor(251, 227, 240),    # #FBE3F0 Soft Rose
        "title": RGBColor(179, 35, 111),  # #B3236F Deep Magenta
        "accent": RGBColor(190, 24, 93),  # #BE185D Rose Pink
    },
    "green": {
        "bg": RGBColor(220, 252, 231),    # #DCFCE7 Soft Mint
        "title": RGBColor(21, 128, 61),   # #15803D Emerald Green
        "accent": RGBColor(22, 163, 74),  # #16A34A Leaf Green
    },
    "amber": {
        "bg": RGBColor(254, 243, 199),    # #FEF3C7 Soft Amber
        "title": RGBColor(180, 83, 9),    # #B45309 Deep Amber
        "accent": RGBColor(217, 119, 6),  # #D97706 Orange Gold
    }
}

STRIPE_PATH = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/slide_sidebar_stripe.png"
ASSET_DIR = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets"

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def add_base_decorations(slide, slide_num, title_text=None):
    # 1. Left Gradient Stripe (Thanh bên 100% khớp mẫu)
    if os.path.exists(STRIPE_PATH):
        slide.shapes.add_picture(STRIPE_PATH, Inches(0), Inches(0), Inches(0.32), Inches(7.5))
        
    # 2. Slide Title
    if title_text:
        tb = slide.shapes.add_textbox(Inches(0.95), Inches(0.44), Inches(11.8), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_FAMILY
        p.font.bold = True
        p.font.size = Pt(34)
        p.font.color.rgb = COLOR_TITLE
        
    # 3. Footer
    if slide_num > 1:
        ft = slide.shapes.add_textbox(Inches(3.5), Inches(7.05), Inches(6.333), Inches(0.35))
        p_ft = ft.text_frame.paragraphs[0]
        p_ft.text = "Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic"
        p_ft.font.name = FONT_FAMILY
        p_ft.font.bold = True
        p_ft.font.size = Pt(11)
        p_ft.font.color.rgb = COLOR_FOOTER
        p_ft.alignment = PP_ALIGN.CENTER
        
        # Page Number
        pg = slide.shapes.add_textbox(Inches(12.0), Inches(7.05), Inches(0.95), Inches(0.35))
        p_pg = pg.text_frame.paragraphs[0]
        p_pg.text = str(slide_num)
        p_pg.font.name = FONT_FAMILY
        p_pg.font.bold = True
        p_pg.font.size = Pt(11)
        p_pg.font.color.rgb = COLOR_FOOTER
        p_pg.alignment = PP_ALIGN.RIGHT

def create_card(slide, left, top, width, height, theme_name, title, bullet_items, title_size=19, body_size=13.5):
    theme = PALETTE.get(theme_name, PALETTE["purple"])
    # Rounded Bento Container
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = theme["bg"]
    shape.line.color.rgb = theme["bg"]
    shape.line.width = Pt(0.5)
    shape.adjustments[0] = 0.04
    
    tf = shape.text_frame
    # Align text immediately at TOP of card (Eliminates the big blank gap above title!)
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.word_wrap = True
    tf.margin_left = Inches(0.28)
    tf.margin_right = Inches(0.28)
    tf.margin_top = Inches(0.20)
    tf.margin_bottom = Inches(0.18)
    
    # Title paragraph
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.name = FONT_FAMILY
    p0.font.bold = True
    p0.font.size = Pt(title_size)
    p0.font.color.rgb = theme["title"]
    p0.space_before = Pt(0)
    p0.space_after = Pt(8)
    
    for item in bullet_items:
        p = tf.add_paragraph()
        p.space_before = Pt(2)
        p.space_after = Pt(4)
        p.font.name = FONT_FAMILY
        
        if isinstance(item, tuple):
            prefix, body = item
            # Bullet dot
            r_bullet = p.add_run()
            r_bullet.text = "• "
            r_bullet.font.name = FONT_FAMILY
            r_bullet.font.bold = True
            r_bullet.font.size = Pt(body_size)
            r_bullet.font.color.rgb = theme["title"]
            # Bold keyword/prefix
            r_pre = p.add_run()
            r_pre.text = prefix + ": " if prefix else ""
            r_pre.font.name = FONT_FAMILY
            r_pre.font.bold = True
            r_pre.font.size = Pt(body_size)
            r_pre.font.color.rgb = theme["accent"]
            # Body text
            r_body = p.add_run()
            r_body.text = body
            r_body.font.name = FONT_FAMILY
            r_body.font.bold = False
            r_body.font.size = Pt(body_size)
            r_body.font.color.rgb = COLOR_TEXT_MAIN
        else:
            r_bullet = p.add_run()
            r_bullet.text = "• "
            r_bullet.font.name = FONT_FAMILY
            r_bullet.font.bold = True
            r_bullet.font.size = Pt(body_size)
            r_bullet.font.color.rgb = theme["title"]
            
            r_body = p.add_run()
            r_body.text = str(item)
            r_body.font.name = FONT_FAMILY
            r_body.font.size = Pt(body_size)
            r_body.font.color.rgb = COLOR_TEXT_MAIN

# ==========================================================
# SLIDE 1: Title Slide (ĐỒ ÁN TRÍ TUỆ NHÂN TẠO - TS. Nguyễn Đắc Dự Trình)
# ==========================================================
s1 = prs.slides.add_slide(blank_layout)
add_base_decorations(s1, 1)

# Top Hero Graphic Banner
hero_path = os.path.join(ASSET_DIR, "title_hero.png")
if os.path.exists(hero_path):
    s1.shapes.add_picture(hero_path, Inches(0.32), Inches(0), Inches(13.013), Inches(3.20))

# Course & Code top-right
tb_code = s1.shapes.add_textbox(Inches(10.5), Inches(3.30), Inches(2.3), Inches(0.4))
p_code = tb_code.text_frame.paragraphs[0]
p_code.text = "GCOS108 | AI-HUTECH"
p_code.font.name = FONT_FAMILY
p_code.font.bold = True
p_code.font.size = Pt(13)
p_code.font.color.rgb = COLOR_FOOTER
p_code.alignment = PP_ALIGN.RIGHT

# Main Title Box
tb_t1 = s1.shapes.add_textbox(Inches(0.95), Inches(3.35), Inches(11.5), Inches(1.35))
tf_t1 = tb_t1.text_frame
tf_t1.word_wrap = True
tf_t1.margin_left = tf_t1.margin_top = tf_t1.margin_right = tf_t1.margin_bottom = 0

p_cname = tf_t1.paragraphs[0]
p_cname.text = "ĐỒ ÁN TRÍ TUỆ NHÂN TẠO — BÁO CÁO ĐỀ TÀI"
p_cname.font.name = FONT_FAMILY
p_cname.font.bold = True
p_cname.font.size = Pt(14)
p_cname.font.color.rgb = RGBColor(179, 35, 111)

p_t1 = tf_t1.add_paragraph()
p_t1.text = "Wildfire Rescue Robotic"
p_t1.font.name = FONT_FAMILY
p_t1.font.bold = True
p_t1.font.size = Pt(40)
p_t1.font.color.rgb = COLOR_TITLE
p_t1.space_before = Pt(4)

p_sub1 = tf_t1.add_paragraph()
p_sub1.text = "Hệ Thống Cứu Hộ Cháy Rừng Tự Hành Bằng Trí Tuệ Bầy Đàn & Deep Learning"
p_sub1.font.name = FONT_FAMILY
p_sub1.font.bold = True
p_sub1.font.size = Pt(18.5)
p_sub1.font.color.rgb = RGBColor(28, 111, 166)
p_sub1.space_before = Pt(4)

# Academic Meta Box (Instructor: TS. Nguyễn Đắc Dự Trình)
tb_meta = s1.shapes.add_textbox(Inches(0.95), Inches(5.15), Inches(11.5), Inches(1.65))
tf_meta = tb_meta.text_frame
tf_meta.word_wrap = True
tf_meta.margin_left = tf_meta.margin_top = tf_meta.margin_right = tf_meta.margin_bottom = 0

p_m1 = tf_meta.paragraphs[0]
p_m1.text = "Giảng viên Hướng dẫn: "
p_m1.font.name = FONT_FAMILY
p_m1.font.size = Pt(14)
p_m1.font.color.rgb = COLOR_TEXT_MAIN
r_gv = p_m1.add_run()
r_gv.text = "TS. Nguyễn Đắc Dự Trình (Ph.D.)"
r_gv.font.bold = True
r_gv.font.color.rgb = COLOR_TITLE

p_m2 = tf_meta.add_paragraph()
p_m2.text = "Khoa Công Nghệ Thông Tin (FIT) — Trường Đại học Công nghệ TP.HCM (HUTECH)"
p_m2.font.name = FONT_FAMILY
p_m2.font.bold = True
p_m2.font.size = Pt(13.5)
p_m2.font.color.rgb = COLOR_FOOTER
p_m2.space_before = Pt(4)

p_m3 = tf_meta.add_paragraph()
p_m3.text = "Nhóm Sinh viên Thực hiện: Topic 35 (4 Thành viên)"
p_m3.font.name = FONT_FAMILY
p_m3.font.bold = True
p_m3.font.size = Pt(13.5)
p_m3.font.color.rgb = RGBColor(179, 35, 111)
p_m3.space_before = Pt(4)

# ==========================================================
# SLIDE 2: Bối cảnh Thực tiễn & Tính Cấp thiết
# ==========================================================
s2 = prs.slides.add_slide(blank_layout)
add_base_decorations(s2, 2, "Bối cảnh Thực tiễn & Tính Cấp thiết")

create_card(s2, Inches(0.95), Inches(1.30), Inches(5.60), Inches(3.85), "pink",
            "Thảm Họa Cháy Rừng Toàn Cầu",
            [
                ("Biến đổi khí hậu", "Siêu cháy rừng cực đoan tăng hơn 40% trong thập kỷ qua."),
                ("Tốc độ lan truyền", "Vận tốc ngọn lửa 10–15 km/h, vượt xa khả năng ứng cứu thủ công."),
                ("Tổn thất diện rộng", "Thiêu rụi hàng triệu ha rừng, đe dọa sinh mạng người dân và tài nguyên.")
            ])

create_card(s2, Inches(6.80), Inches(1.30), Inches(5.60), Inches(3.85), "purple",
            "Tử Huyệt Cứu Hộ Truyền Thống",
            [
                ("Khói mù & nhiệt độ", "Tầm nhìn bằng 0, trực thăng không thể tiếp cận tầm thấp an toàn."),
                ("Rủi ro bẫy lửa", "Địa hình hiểm trở khiến lính cứu hộ đối mặt nguy cơ bị lửa vây bọc."),
                ("Thiếu dự báo vi mô", "Dữ liệu thời tiết vĩ mô không tính được hướng lan cục bộ từng mét vuông.")
            ])

create_card(s2, Inches(0.95), Inches(5.35), Inches(11.45), Inches(1.30), "blue",
            "Sứ Mệnh Đề Tài Topic 35",
            [
                ("Giải pháp Đột phá", "Phát triển bầy Robot UGV tự hành dẫn đường bằng AI dự báo để cứu hộ an toàn tuyệt đối.")
            ])

# ==========================================================
# SLIDE 3: Phát biểu Bài toán & Mô hình Baseline
# ==========================================================
s3 = prs.slides.add_slide(blank_layout)
add_base_decorations(s3, 3, "Phát biểu Bài toán & Giới hạn Greedy Baseline")

create_card(s3, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35), "purple",
            "Định Nghĩa Bài Toán Tác Chiến 2D",
            [
                ("Không gian Lưới (Grid)", "Bản đồ N x M chứa thực bì, độ dốc và chướng ngại vật tĩnh."),
                ("Nạn nhân (Victims)", "Tọa độ Vk gắn với độ khẩn cấp Uk in {1: Trung bình, 2: Nguy cấp, 3: Tử vong}."),
                ("Bầy Robot Cứu hộ", "K robot cứu nạn UGV xuất phát đồng thời từ trạm cơ sở ban đầu."),
                ("Đám cháy Động (Fire)", "Lan truyền phi tuyến F(x, y, t) biến thiên theo vector gió và thực bì.")
            ])

create_card(s3, Inches(6.80), Inches(1.30), Inches(5.60), Inches(5.35), "pink",
            "Nhược Điểm Cốt Tử Của Greedy Baseline",
            [
                ("Tham lam Thiển cận", "Mỗi robot chỉ chọn nạn nhân gần nhất theo khoảng cách hình học."),
                ("Bỏ qua Động học Lửa", "Hoàn toàn mù mờ trước ngọn lửa, dễ dẫn robot lao thẳng vào tâm cháy."),
                ("Tỉ lệ Thất bại Cao", "Chỉ đạt 40.0% tỉ lệ cứu hộ trong thực nghiệm; 60% nạn nhân tử nạn."),
                ("Xung đột Bầy đàn", "Tranh chấp cùng một mục tiêu, bỏ rơi các nạn nhân nguy cấp ở xa.")
            ])

# ==========================================================
# SLIDE 4: Kiến trúc Tổng thể Hệ thống Hybrid AI
# ==========================================================
s4 = prs.slides.add_slide(blank_layout)
add_base_decorations(s4, 4, "Kiến trúc Tổng thể Hệ thống Hybrid AI (4 Tầng)")

pipe_path = os.path.join(ASSET_DIR, "pipeline_diagram.png")
if os.path.exists(pipe_path):
    s4.shapes.add_picture(pipe_path, Inches(0.95), Inches(1.25), Inches(11.45), Inches(3.70))

create_card(s4, Inches(0.95), Inches(5.15), Inches(5.60), Inches(1.50), "purple",
            "Chu Trình 4 Tầng Khép Kín",
            [
                ("Quy trình Đồng bộ", "U-Net Dự báo -> PettingZoo Môi trường -> PSO Phân bầy -> A* Dẫn đường né lửa."),
                ("Cập nhật Real-time", "Toàn bộ hệ thống làm mới trạng thái đồng bộ sau mỗi bước di chuyển t.")
            ])

create_card(s4, Inches(6.80), Inches(5.15), Inches(5.60), Inches(1.50), "blue",
            "Vòng Lặp Phản Ứng Đột Biến",
            [
                ("Dynamic Replanning", "Tái hoạch định lộ trình tức thì trong < 1ms khi lửa bất ngờ chặn đường."),
                ("Zero Trapped", "Bảo đảm bầy robot không bao giờ bị động trước sự biến đổi của đám cháy.")
            ])

# ==========================================================
# SLIDE 5: Tầng 1 - Deep Learning PyTorch U-Net 2D
# ==========================================================
s5 = prs.slides.add_slide(blank_layout)
add_base_decorations(s5, 5, "Tầng 1 — Deep Learning PyTorch U-Net 2D")

unet_path = os.path.join(ASSET_DIR, "unet_diagram.png")
if os.path.exists(unet_path):
    s5.shapes.add_picture(unet_path, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35))

create_card(s5, Inches(6.80), Inches(1.30), Inches(5.60), Inches(2.55), "purple",
            "Kiến Trúc & Skip Connections",
            [
                ("5 Kênh Đa Phổ Đầu Vào", "Vị trí lửa, Mật độ thực bì, Độ cao DEM, Vector gió X và Gió Y (5x20x20)."),
                ("Skip Connections", "Truyền chi tiết biên độ cao từ Encoder sang Decoder, giữ vẹn đường bao lửa."),
                ("Đầu Ra Heatmap", "Ma trận xác suất rủi ro lửa P_fire(x, y) in [0, 1] phục vụ dẫn đường.")
            ])

create_card(s5, Inches(6.80), Inches(4.05), Inches(5.60), Inches(2.60), "blue",
            "Hàm Mất Mát Kết Hợp BCE-Dice Loss",
            [
                ("Chống Mất Cân Bằng Cực Đoan", "Điểm cháy thực tế chỉ chiếm < 5% diện tích lưới (severe class imbalance)."),
                ("Công Thức Loss Kết Hợp", "L_total = L_BCE + lambda_dice * L_Dice tối ưu đồng thời Cross-Entropy và IoU."),
                ("Độ Chính Xác Cao", "F1-Score đạt 0.942 và IoU đạt 0.891 trên tập kiểm thử unseen độc lập.")
            ])

# ==========================================================
# SLIDE 6: Tầng 2 - Môi trường Đa tác tử PettingZoo & CA
# ==========================================================
s6 = prs.slides.add_slide(blank_layout)
add_base_decorations(s6, 6, "Tầng 2 — Môi trường Đa tác tử PettingZoo & CA")

create_card(s6, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35), "blue",
            "Động Học Lan Truyền Cellular Automata",
            [
                ("Quy Tắc Lân Cận", "Cập nhật trạng thái ô lưới theo 8 ô lân cận (Moore): Chưa cháy -> Cháy -> Tro tàn."),
                ("Vector Gió & Độ Dốc", "Gió và địa hình làm đám cháy lan bất đối xứng hình elip sát thực tế."),
                ("Thực Bì Khô Cằn", "Thảm thực vật khô tăng tốc độ bén lửa lên gấp 2.5 - 3.0 lần."),
                ("Khách Quan Tuyệt Đối", "Sinh trường hợp ngẫu nhiên, loại trừ hoàn toàn việc AI học tủ kết quả.")
            ])

create_card(s6, Inches(6.80), Inches(1.30), Inches(5.60), Inches(5.35), "purple",
            "Khung Mô Phỏng Chuẩn AEC",
            [
                ("Chu Trình AEC Chuẩn Hóa", "Quản lý song song K robot thực thi hành động nhịp nhàng qua từng bước."),
                ("Cảm Biến Quét Cục Bộ", "Robot tự nhận biết bán kính an toàn, nồng độ khói độc và nhiệt tiệm cận."),
                ("Hệ Thống Reward", "Thưởng lớn (+100) khi cứu người; Phạt cực nặng (-500) nếu chạm lửa."),
                ("Mở Rộng Dễ Dàng", "Dễ dàng tăng quy mô bầy đàn từ 3 lên 10+ robot linh hoạt.")
            ])

# ==========================================================
# SLIDE 7: Tầng 3 - Trí tuệ Bầy đàn Swarm PSO (pymoo)
# ==========================================================
s7 = prs.slides.add_slide(blank_layout)
add_base_decorations(s7, 7, "Tầng 3 — Trí tuệ Bầy đàn Swarm PSO (pymoo)")

create_card(s7, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35), "purple",
            "Tối Ưu Bầy Đàn Particle Swarm",
            [
                ("Khung pymoo Công Nghiệp", "Tối ưu hóa vector hóa hiệu năng cao, tăng tốc giải toán hơn 10x."),
                ("Mã Hóa Cá Thể (Particle)", "Mỗi hạt biểu diễn một phương án phân bổ toàn bộ M nạn nhân cho K robot."),
                ("Cập Nhật Vị Trí & Vận Tốc", "Cân bằng giữa kinh nghiệm cá nhân (p_best) và tri thức bầy đàn (g_best)."),
                ("Hội Tụ Siêu Tốc", "Tìm ra nghiệm phân công tối ưu sau 30-50 thế hệ trong vòng < 15ms.")
            ])

create_card(s7, Inches(6.80), Inches(1.30), Inches(5.60), Inches(5.35), "blue",
            "Hàm Group Fitness Đa Mục Tiêu",
            [
                ("Ưu Tiên Nạn Nhân Nguy Cấp", "Cực đại hóa F1 = sum(U_k); nạn nhân cấp 3 được tiếp cận đầu tiên."),
                ("Cực Tiểu Rủi Ro Lửa", "Giảm thiểu F2 = sum(P_fire) trên toàn bộ lộ trình di chuyển của bầy."),
                ("Cân Bằng Tải Đường Đi", "Tránh dồn việc cho 1 robot; phân bổ đồng đều hành trình bầy đàn."),
                ("Tự Thích Ứng Động", "Tái tính toán tức thì khi có biến cố nạn nhân mới hoặc robot gặp nạn.")
            ])

# ==========================================================
# SLIDE 8: Tầng 4 - Hoạch định Đường đi Fire-Aware A*
# ==========================================================
s8 = prs.slides.add_slide(blank_layout)
add_base_decorations(s8, 8, "Tầng 4 — Hoạch định Đường đi Fire-Aware A*")

path_img = os.path.join(ASSET_DIR, "fire_path_diagram.png")
if os.path.exists(path_img):
    s8.shapes.add_picture(path_img, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35))

create_card(s8, Inches(6.80), Inches(1.30), Inches(5.60), Inches(2.55), "pink",
            "Hàm Chi Phí Phạt Rủi Ro Lửa",
            [
                ("Công Thức Mở Rộng", "f(n) = g(n) + h(n) + lambda_fire * P_fire(n)."),
                ("Hệ Số Phạt lambda_fire = 15.0", "Ép thuật toán chủ động chọn đường vòng an toàn quanh mép lửa."),
                ("Né Vùng Nguy Hiểm", "Bảo đảm robot không băng cắt qua các ô có nhiệt độ cao và khói mù.")
            ])

create_card(s8, Inches(6.80), Inches(4.05), Inches(5.60), Inches(2.60), "purple",
            "Cơ Chế Dynamic Replanning",
            [
                ("Kiểm Tra Từng Bước", "Robot quét xác suất cháy trên các bước còn lại tại mỗi nhịp di chuyển t."),
                ("Phản Xạ Thời Gian Thực", "Nếu lửa bất ngờ cắt ngang lộ trình (P_fire > 0.15), vẽ lại tuyến trong < 1ms."),
                ("Đảm Bảo An Toàn Tuyệt Đối", "Không để robot rơi vào tình thế tiến thoái lưỡng nan khi lửa lan nhanh.")
            ])

# ==========================================================
# SLIDE 9: Cơ chế Tái phân công Động (Dynamic Reallocation)
# ==========================================================
s9 = prs.slides.add_slide(blank_layout)
add_base_decorations(s9, 9, "Cơ chế Tái Phân Công Động (Dynamic Reallocation)")

create_card(s9, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35), "purple",
            "Kích Hoạt Sự Kiện Đột Biến (Event-Triggered)",
            [
                ("Ngõ Hẹp Bị Khóa (Choke Point)", "Đám cháy bùng phát phong tỏa hoàn toàn đường độc đạo tới mục tiêu."),
                ("Nạn Nhân Bị Đe Dọa Nhanh", "Gió đổi chiều đẩy đám cháy áp sát nạn nhân nhanh hơn vận tốc robot."),
                ("Sự Cố Cơ Giới", "Robot gặp sạt lở hoặc cạn nguồn điện dự phòng không thể tiếp tục."),
                ("Báo Động Toàn Bầy", "Phát tín hiệu còi khẩn cấp lên mạng lưới bầy đàn để chuyển giao nhiệm vụ.")
            ])

create_card(s9, Inches(6.80), Inches(1.30), Inches(5.60), Inches(5.35), "blue",
            "Chi Viện Bầy Đàn Tự Động",
            [
                ("Giải Phóng Mục Tiêu", "Robot bị chặn dừng lại an toàn và nhả mục tiêu ra hàng đợi chung."),
                ("Tái Điều Phối Bằng PSO", "PSO tức thời phân bổ lại nhiệm vụ cho các robot rảnh tay còn lại."),
                ("Robot Thuận Lợi Tiếp Quản", "Robot có cự ly và hành lang né lửa tốt nhất sẽ đổi hướng giải cứu."),
                ("Bảo Toàn 100% Mục Tiêu", "Đảm bảo không bỏ rơi bất kỳ nạn nhân nào trong tình huống thảm họa.")
            ])

# ==========================================================
# SLIDE 10: Quy trình Thực nghiệm & Chia Dữ liệu 70/30
# ==========================================================
s10 = prs.slides.add_slide(blank_layout)
add_base_decorations(s10, 10, "Quy trình Thực nghiệm & Chia Dữ liệu 70/30")

col_w = Inches(3.60)
create_card(s10, Inches(0.95), Inches(1.30), col_w, Inches(5.35), "purple",
            "Dataset Viễn Thám Thực Tế",
            [
                ("Next Day Wildfire", "Bộ dữ liệu vệ tinh từ Google Research & Kaggle."),
                ("Vệ Tinh Đa Phổ", "MODIS và VIIRS ghi nhận cháy rừng diện rộng."),
                ("5 Kênh Chuẩn Hóa", "Phân bố nhiệt, thực bì, độ cao DEM và vận tốc gió."),
                ("Khử Nhiễu Mây Mù", "Chuẩn hóa ma trận đầu vào về khoảng [0, 1].")
            ])

create_card(s10, Inches(4.85), Inches(1.30), col_w, Inches(5.35), "blue",
            "Chiến Lược Chia Tập 70 / 30",
            [
                ("70% Huấn Luyện", "Dạy mạng U-Net học quy luật bốc cháy vi mô qua 50 epochs."),
                ("30% Kiểm Thử Độc Lập", "Dùng độc quyền để sinh 10 kịch bản unseen."),
                ("Cố Định Seed = 42", "Đảm bảo tính tái lập 100% và minh bạch khoa học."),
                ("Khách Quan Tuyệt Đối", "AI hoàn toàn không được biết trước địa hình thực nghiệm.")
            ])

create_card(s10, Inches(8.75), Inches(1.30), col_w, Inches(5.35), "pink",
            "Chống Overfitting Triệt Để",
            [
                ("Data Augmentation", "Lật ngẫu nhiên, xoay góc và nhiễu Gaussian tăng tính tổng quát."),
                ("Dropout & L2 Decay", "Chèn Dropout p=0.2 và L2 (1e-4) hạn chế học vẹt dữ liệu."),
                ("Giám Sát Early Stopping", "Lưu checkpoint có F1-Score cao nhất trên tập Validation."),
                ("Kết Quả Đạt Chuẩn", "Đạt F1-Score = 0.942 và IoU = 0.891 trên tập kiểm thử.")
            ])

# ==========================================================
# SLIDE 11: Bảng Kết quả Thực nghiệm Benchmark 5 Chỉ số
# ==========================================================
s11 = prs.slides.add_slide(blank_layout)
add_base_decorations(s11, 11, "Bảng Kết quả Thực nghiệm Benchmark Đối chứng")

rows, cols = 4, 5
table_shape = s11.shapes.add_table(rows, cols, Inches(0.95), Inches(1.30), Inches(11.45), Inches(2.90))
tbl = table_shape.table

tbl.columns[0].width = Inches(3.45)
tbl.columns[1].width = Inches(1.80)
tbl.columns[2].width = Inches(1.80)
tbl.columns[3].width = Inches(2.20)
tbl.columns[4].width = Inches(2.20)

table_data = [
    ["Phương Pháp Tác Chiến", "Tỉ Lệ Cứu Hộ", "Rủi Ro Lửa TB", "Thời Gian Tính", "Số Bước Đi"],
    ["Proposed Hybrid AI (Topic 35)", "100.0% (50/50)", "0.0039", "0.042 s", "28.4 bước"],
    ["Standard A* (Không né lửa)", "60.0% (30/50)", "0.3150", "0.038 s", "31.0 bước"],
    ["Greedy Nearest Baseline", "40.0% (20/50)", "0.4280", "0.012 s", "34.2 bước"]
]

bg_colors = [
    RGBColor(112, 48, 160),  # Header Purple
    RGBColor(220, 252, 231),  # Proposed Green Highlight (#DCFCE7)
    RGBColor(241, 236, 248),  # Soft Purple Alternating
    RGBColor(255, 255, 255)   # White
]

text_colors = [
    RGBColor(255, 255, 255),  # White
    RGBColor(21, 128, 61),    # Emerald Dark Green
    RGBColor(30, 30, 36),     # Charcoal
    RGBColor(30, 30, 36)      # Charcoal
]

for r_idx, row in enumerate(table_data):
    for c_idx, val in enumerate(row):
        cell = tbl.cell(r_idx, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_colors[r_idx]
        cell.margin_left = cell.margin_right = Inches(0.12)
        cell.margin_top = cell.margin_bottom = Inches(0.10)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_FAMILY
        p.font.size = Pt(13 if r_idx > 0 else 13.5)
        p.font.bold = True if (r_idx in [0, 1] or c_idx == 0) else False
        p.font.color.rgb = text_colors[r_idx]
        if c_idx > 0:
            p.alignment = PP_ALIGN.CENTER

create_card(s11, Inches(0.95), Inches(4.55), Inches(11.45), Inches(2.10), "amber",
            "Kết Luận Thực Nghiệm Khoa Học",
            [
                ("Tỉ Lệ Cứu Hộ Tuyệt Đối", "Hệ thống Hybrid AI cứu sống 100% nạn nhân qua 10 kịch bản ngẫu nhiên (vượt trội 2.5x so với Greedy)."),
                ("Triệt Tiêu Nguy Cơ", "Giảm 99.1% rủi ro phơi nhiễm lửa tích lũy (0.0039 vs 0.4280); thời gian tính toán < 50ms đáp ứng thời gian thực.")
            ])

# ==========================================================
# SLIDE 12: Biểu đồ Đánh giá Hiệu năng & Biện luận Khoa học
# ==========================================================
s12 = prs.slides.add_slide(blank_layout)
add_base_decorations(s12, 12, "Biểu đồ Đánh giá Hiệu năng & Biện luận Khoa học")

bm_img = os.path.join(ASSET_DIR, "benchmark_chart.png")
if os.path.exists(bm_img):
    s12.shapes.add_picture(bm_img, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35))

create_card(s12, Inches(6.80), Inches(1.30), Inches(5.60), Inches(2.55), "purple",
            "Độ Ổn Định Tuyệt Đối (Zero Failure)",
            [
                ("Khái Quát Hóa Vượt Trội", "AI phản ứng linh hoạt trước các ổ lửa bất ngờ, không có bất kỳ kịch bản nào thương vong."),
                ("Triệt Tiêu Bẫy Lửa", "Nhờ tầm nhìn rủi ro từ U-Net, bầy robot không bao giờ bị dồn vào ngõ cụt hiểm trở.")
            ])

create_card(s12, Inches(6.80), Inches(4.05), Inches(5.60), Inches(2.60), "blue",
            "Tối Ưu Hóa Tài Nguyên Thực Địa",
            [
                ("Cân Bằng Quãng Đường", "Lộ trình né lửa chỉ dài hơn đường thẳng 8-12% nhưng loại trừ 99% xác suất bị thiêu rụi."),
                ("Khả Năng Nhúng Thực Tế", "Tốc độ xử lý 0.042s/kịch bản hoàn toàn khả thi chạy trực tiếp trên máy tính nhúng Jetson Nano.")
            ])

# ==========================================================
# SLIDE 13: Phân tích Trường hợp Thất bại & Hạn chế
# ==========================================================
s13 = prs.slides.add_slide(blank_layout)
add_base_decorations(s13, 13, "Phân tích Trường hợp Thất bại & Hướng Phát triển")

create_card(s13, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35), "pink",
            "Failure Mode: Điểm Nghẽn Cực Đoan (Choke Point)",
            [
                ("Ngõ Độc Đạo Bị Cháy", "Lửa bùng phát nuốt trọn hoàn toàn lối duy nhất dẫn tới mục tiêu trước khi robot tới nơi."),
                ("Cơ Chế Tự Vệ Thông Minh", "Robot tự động nhận diện và dừng lại ở vành đai an toàn thay vì tự sát vô ích."),
                ("Chuyển Giao Đường Không", "Hệ thống phát tín hiệu chuyển mục tiêu sang phương tiện cứu hộ đường không (UAV / Trực thăng)."),
                ("Bài Học Thực Tiễn", "Khẳng định sự cần thiết của việc kết hợp trinh sát trên không và cứu hộ mặt đất.")
            ])

create_card(s13, Inches(6.80), Inches(1.30), Inches(5.60), Inches(5.35), "purple",
            "Hạn Chế Của Đồ Án & Hướng Mở Rộng",
            [
                ("Giới Hạn Bản Đồ 2D", "Hiện tại mô phỏng trên lưới phẳng 2D, chưa mô tả luồng nhiệt đối lưu 3D và gió lốc lửa."),
                ("Thời Tiết Động Đột Biến", "Chưa mô phỏng hiện tượng mưa dông đột ngột làm dập tắt một phần đám cháy."),
                ("Nâng Cấp Lên 3D Point Cloud", "Tích hợp cảm biến LiDAR và Camera nhiệt hồng ngoại thời gian thực trên Robot UGV."),
                ("Tác Chiến Đa Tầng (Air-Ground)", "Bầy đàn phối hợp nhịp nhàng giữa máy bay UAV trinh sát dập lửa và UGV cứu người.")
            ])

# ==========================================================
# SLIDE 14: Demo Hệ thống Dashboard, Kết luận & Q&A
# ==========================================================
s14 = prs.slides.add_slide(blank_layout)
add_base_decorations(s14, 14, "Demo Hệ thống Dashboard, Kết luận & Q&A")

# Use the full stacked dashboard graphic (Both Setup and Live Tactical Swarm Map from user)
demo_img = os.path.join(ASSET_DIR, "dashboard_full_stack.png")
if not os.path.exists(demo_img):
    demo_img = os.path.join(ASSET_DIR, "tactical_map_demo.png")
if os.path.exists(demo_img):
    s14.shapes.add_picture(demo_img, Inches(0.95), Inches(1.30), Inches(5.60), Inches(5.35))

create_card(s14, Inches(6.80), Inches(1.30), Inches(5.60), Inches(2.55), "blue",
            "Sản Phẩm Tác Chiến Tương Tác",
            [
                ("Dashboard Streamlit", "Bản đồ nhiệt 2D thời gian thực, bảng điều khiển Play/Pause, Step-by-Step mượt mà."),
                ("Sinh Kịch Bản Ngẫu Nhiên", "Tự sinh địa hình và hạt giống seed mới để kiểm tra tính khách quan của bầy đàn."),
                ("Tự Động Kết Thúc", "Tự động dừng tác chiến chính xác khi giải cứu xong toàn bộ mục tiêu.")
            ])

create_card(s14, Inches(6.80), Inches(4.05), Inches(5.60), Inches(2.60), "purple",
            "Lời Cảm Ơn & Sẵn Sàng Q&A",
            [
                ("Tri Ân Thầy Cô", "Nhóm Topic 35 xin gửi lời cảm ơn chân thành đến TS. Nguyễn Đắc Dự Trình và Quý Thầy Cô!"),
                ("Sẵn Sàng Trao Đổi", "Nhóm rất mong nhận được những góp ý quý báu từ Hội đồng Giám khảo để hoàn thiện đề tài!"),
                ("Mã Nguồn Mở", "Toàn bộ mã nguồn và dữ liệu thực nghiệm sẵn sàng trên kho lưu trữ của nhóm.")
            ])

out_pptx = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/TOPIC_35_WILDFIRE_SWARM_PRESENTATION.pptx"
prs.save(out_pptx)
print(f"Presentation master deck saved successfully to: {out_pptx}")
