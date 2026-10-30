import os
import base64

ASSET_DIR = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/assets"
HTML_PATH = "/home/duck/CLI/Wildfire-Rescue-Robotic/wildfire_rescue_swarm/presentation.html"

def get_b64_image(filename):
    path = os.path.join(ASSET_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    return ""

hero_b64 = get_b64_image("title_hero.png")
pipe_b64 = get_b64_image("pipeline_diagram.png")
unet_b64 = get_b64_image("unet_diagram.png")
path_b64 = get_b64_image("fire_path_diagram.png")
chart_b64 = get_b64_image("benchmark_chart.png")
demo_b64 = get_b64_image("dashboard_full_stack.png")
if not demo_b64:
    demo_b64 = get_b64_image("tactical_map_demo.png")

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic Presentation</title>
<style>
  :root {{
    --bg-slide: #FFFFFF;
    --title-purple: #7030A0;
    --text-main: #1E1E24;
    --text-footer: #454551;
    --card-purple-bg: #F1ECF8;
    --card-purple-title: #7030A0;
    --card-purple-accent: #502CD1;
    --card-blue-bg: #E1F0FA;
    --card-blue-title: #1C6FA6;
    --card-blue-accent: #0284C7;
    --card-pink-bg: #FBE3F0;
    --card-pink-title: #B3236F;
    --card-pink-accent: #BE185D;
    --card-green-bg: #DCFCE7;
    --card-green-title: #15803D;
    --card-green-accent: #16A34A;
    --card-amber-bg: #FEF3C7;
    --card-amber-title: #B45309;
    --card-amber-accent: #D97706;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: Arial, Helvetica, sans-serif;
    background-color: #0F172A;
    color: var(--text-main);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
  }}

  #deck-container {{
    position: relative;
    width: 100%;
    max-width: 1280px;
    aspect-ratio: 16 / 9;
    background: var(--bg-slide);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 12px;
    overflow: hidden;
  }}

  .slide {{
    display: none;
    position: absolute;
    inset: 0;
    padding: 30px 45px 32px 60px;
    background: var(--bg-slide);
  }}

  .slide.active {{
    display: flex;
    flex-direction: column;
  }}

  /* Thanh bên Gradient chuẩn 100% template GCOS108-L5-Clustering.pdf */
  .slide-stripe {{
    position: absolute;
    top: 0;
    left: 0;
    width: 26px;
    height: 100%;
    background: linear-gradient(180deg, 
      #FFCC00 0%, 
      #F9A721 15%, 
      #F28343 25%, 
      #EC5E64 40%, 
      #E53986 50%, 
      #C345AE 65%, 
      #926AD9 75%, 
      #6C73E4 85%, 
      #4875E7 100%
    );
    z-index: 10;
  }}

  /* Slide Title */
  .slide-title {{
    color: var(--title-purple);
    font-size: 2.1rem;
    font-weight: 700;
    margin-bottom: 16px;
    line-height: 1.2;
  }}

  /* Footer */
  .slide-footer {{
    position: absolute;
    bottom: 14px;
    left: 60px;
    right: 45px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text-footer);
    pointer-events: none;
  }}

  .footer-center {{
    margin: 0 auto;
  }}

  /* Card Bento Containers (Aligned strictly at top, no empty void above title!) */
  .card {{
    border-radius: 14px;
    padding: 18px 22px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }}

  .card-purple {{ background-color: var(--card-purple-bg); }}
  .card-purple h3 {{ color: var(--card-purple-title); }}
  .card-purple .accent {{ color: var(--card-purple-accent); }}

  .card-blue {{ background-color: var(--card-blue-bg); }}
  .card-blue h3 {{ color: var(--card-blue-title); }}
  .card-blue .accent {{ color: var(--card-blue-accent); }}

  .card-pink {{ background-color: var(--card-pink-bg); }}
  .card-pink h3 {{ color: var(--card-pink-title); }}
  .card-pink .accent {{ color: var(--card-pink-accent); }}

  .card-green {{ background-color: var(--card-green-bg); }}
  .card-green h3 {{ color: var(--card-green-title); }}
  .card-green .accent {{ color: var(--card-green-accent); }}

  .card-amber {{ background-color: var(--card-amber-bg); }}
  .card-amber h3 {{ color: var(--card-amber-title); }}
  .card-amber .accent {{ color: var(--card-amber-accent); }}

  .card h3 {{
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 0;
    margin-bottom: 10px;
    line-height: 1.25;
  }}

  .card ul {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}

  .card li {{
    position: relative;
    padding-left: 18px;
    font-size: 0.95rem;
    line-height: 1.4;
  }}

  .card li::before {{
    content: "•";
    position: absolute;
    left: 0;
    font-size: 1.3rem;
    line-height: 1;
    top: -1px;
  }}
  .card-purple li::before {{ color: var(--card-purple-title); }}
  .card-blue li::before {{ color: var(--card-blue-title); }}
  .card-pink li::before {{ color: var(--card-pink-title); }}
  .card-green li::before {{ color: var(--card-green-title); }}
  .card-amber li::before {{ color: var(--card-amber-title); }}

  .accent {{
    font-weight: 700;
  }}

  /* Grid Layouts */
  .grid-2col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    flex: 1;
    margin-bottom: 22px;
  }}

  .grid-3col {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
    flex: 1;
    margin-bottom: 22px;
  }}

  .grid-split {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
    flex: 1;
    margin-bottom: 22px;
    align-items: stretch;
  }}

  .img-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    background: #F8FAFC;
    border-radius: 14px;
    padding: 10px;
    border: 1px solid #E2E8F0;
  }}

  .img-container img {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 8px;
  }}

  /* Table Style */
  .styled-table {{
    width: 100%;
    border-collapse: collapse;
    border-radius: 10px;
    overflow: hidden;
    font-size: 0.95rem;
    margin-bottom: 16px;
  }}

  .styled-table th {{
    background-color: var(--title-purple);
    color: white;
    font-weight: 700;
    padding: 12px 16px;
    text-align: left;
  }}

  .styled-table td {{
    padding: 11px 16px;
    border-bottom: 1px solid #E2E8F0;
  }}

  .row-highlight {{
    background-color: var(--card-green-bg);
    color: var(--card-green-title);
    font-weight: 700;
  }}

  .row-alt {{
    background-color: var(--card-purple-bg);
  }}

  /* Controls */
  .controls {{
    display: flex;
    gap: 14px;
    align-items: center;
    margin-top: 14px;
    color: #94A3B8;
  }}

  .btn {{
    background: #1E293B;
    color: #F8FAFC;
    border: 1px solid #334155;
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.92rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }}
  .btn:hover {{
    background: #334155;
    color: #FFFFFF;
  }}

  /* Title Slide Specifics */
  .slide-title-layout {{
    padding: 0 !important;
  }}
  .title-hero-banner {{
    width: 100%;
    height: 46%;
    object-fit: cover;
  }}
  .title-content {{
    padding: 24px 45px 24px 60px;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }}
</style>
</head>
<body>

<div id="deck-container">
  <div class="slide-stripe"></div>

  <!-- SLIDE 1: Title Slide (Đồ án Trí Tuệ Nhân Tạo — TS. Nguyễn Đắc Dự Trình) -->
  <div class="slide slide-title-layout active">
    <img src="{hero_b64}" class="title-hero-banner" alt="Hero Banner">
    <div class="title-content">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="font-size: 1.05rem; font-weight: 700; color: var(--card-pink-title);">
          ĐỒ ÁN TRÍ TUỆ NHÂN TẠO — BÁO CÁO ĐỀ TÀI
        </span>
        <span style="font-size: 0.9rem; font-weight: 700; color: var(--text-footer);">
          GCOS108 | AI-HUTECH
        </span>
      </div>
      <h1 style="color: var(--title-purple); font-size: 2.7rem; font-weight: 800; line-height: 1.15; margin-bottom: 6px;">
        Wildfire Rescue Robotic
      </h1>
      <h2 style="color: var(--card-blue-title); font-size: 1.35rem; font-weight: 700; margin-bottom: 16px;">
        Hệ Thống Cứu Hộ Cháy Rừng Tự Hành Bằng Trí Tuệ Bầy Đàn & Deep Learning
      </h2>
      <div style="font-size: 0.96rem; color: var(--text-main); margin-bottom: 4px;">
        Giảng viên Hướng dẫn: <strong style="color: var(--title-purple);">TS. Nguyễn Đắc Dự Trình (Ph.D.)</strong>
      </div>
      <div style="font-size: 0.92rem; color: var(--text-footer); margin-bottom: 4px; font-weight: 600;">
        Khoa Công Nghệ Thông Tin (FIT) — Trường Đại học Công nghệ TP.HCM (HUTECH)
      </div>
      <div style="font-size: 0.92rem; color: var(--card-pink-title); font-weight: 700;">
        Nhóm Sinh viên Thực hiện: Topic 35 (4 Thành viên)
      </div>
    </div>
  </div>

  <!-- SLIDE 2: Bối cảnh Thực tiễn & Tính Cấp thiết -->
  <div class="slide">
    <h2 class="slide-title">Bối cảnh Thực tiễn & Tính Cấp thiết</h2>
    <div class="grid-2col" style="flex: 0.85; margin-bottom: 14px;">
      <div class="card card-pink">
        <h3>Thảm Họa Cháy Rừng Toàn Cầu</h3>
        <ul>
          <li><span class="accent">Biến đổi khí hậu:</span> Siêu cháy rừng cực đoan tăng hơn 40% trong thập kỷ qua.</li>
          <li><span class="accent">Tốc độ lan truyền:</span> Vận tốc ngọn lửa 10–15 km/h, vượt xa khả năng ứng cứu thủ công.</li>
          <li><span class="accent">Tổn thất diện rộng:</span> Thiêu rụi hàng triệu ha rừng, đe dọa sinh mạng người dân.</li>
        </ul>
      </div>
      <div class="card card-purple">
        <h3>Tử Huyệt Cứu Hộ Truyền Thống</h3>
        <ul>
          <li><span class="accent">Khói mù & nhiệt độ:</span> Tầm nhìn bằng 0, trực thăng không thể tiếp cận tầm thấp an toàn.</li>
          <li><span class="accent">Rủi ro bẫy lửa:</span> Địa hình hiểm trở khiến lính cứu hộ đối mặt nguy cơ bị lửa vây bọc.</li>
          <li><span class="accent">Thiếu dự báo vi mô:</span> Dữ liệu thời tiết vĩ mô không tính được hướng lan cục bộ.</li>
        </ul>
      </div>
    </div>
    <div class="card card-blue" style="padding: 12px 20px;">
      <h3>Sứ Mệnh Đề Tài Topic 35</h3>
      <ul>
        <li><span class="accent">Giải pháp Đột phá:</span> Phát triển bầy Robot UGV tự hành dẫn đường bằng AI dự báo để cứu hộ an toàn tuyệt đối.</li>
      </ul>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">2</div>
    </div>
  </div>

  <!-- SLIDE 3: Phát biểu Bài toán & Mô hình Baseline -->
  <div class="slide">
    <h2 class="slide-title">Phát biểu Bài toán & Giới hạn Greedy Baseline</h2>
    <div class="grid-2col">
      <div class="card card-purple">
        <h3>Định Nghĩa Bài Toán Tác Chiến 2D</h3>
        <ul>
          <li><span class="accent">Không gian Lưới (Grid):</span> Bản đồ N x M chứa thực bì, độ dốc và chướng ngại vật tĩnh.</li>
          <li><span class="accent">Nạn nhân (Victims):</span> Tọa độ Vk gắn với độ khẩn cấp Uk in (1: TB, 2: Nguy cấp, 3: Tử vong).</li>
          <li><span class="accent">Bầy Robot Cứu hộ:</span> K robot cứu nạn UGV xuất phát đồng thời từ trạm cơ sở ban đầu.</li>
          <li><span class="accent">Đám cháy Động (Fire):</span> Lan truyền phi tuyến F(x, y, t) biến thiên theo vector gió và thực bì.</li>
        </ul>
      </div>
      <div class="card card-pink">
        <h3>Nhược Điểm Cốt Tử Của Greedy Baseline</h3>
        <ul>
          <li><span class="accent">Tham lam Thiển cận:</span> Mỗi robot chỉ chọn nạn nhân gần nhất theo khoảng cách hình học.</li>
          <li><span class="accent">Bỏ qua Động học Lửa:</span> Hoàn toàn mù mờ trước ngọn lửa, dễ dẫn robot lao thẳng vào tâm cháy.</li>
          <li><span class="accent">Tỉ lệ Thất bại Cao:</span> Chỉ đạt 40.0% tỉ lệ cứu hộ trong thực nghiệm; 60% nạn nhân tử nạn.</li>
          <li><span class="accent">Xung đột Bầy đàn:</span> Tranh chấp cùng một mục tiêu, bỏ rơi các nạn nhân nguy cấp ở xa.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">3</div>
    </div>
  </div>

  <!-- SLIDE 4: Kiến trúc Tổng thể Hệ thống Hybrid AI -->
  <div class="slide">
    <h2 class="slide-title">Kiến trúc Tổng thể Hệ thống Hybrid AI (4 Tầng)</h2>
    <div class="img-container" style="flex: 1.15; margin-bottom: 14px;">
      <img src="{pipe_b64}" alt="4-Layer Architecture Pipeline">
    </div>
    <div class="grid-2col" style="flex: 0.65; margin-bottom: 20px;">
      <div class="card card-purple">
        <h3>Chu Trình 4 Tầng Khép Kín</h3>
        <ul>
          <li><span class="accent">Quy trình Đồng bộ:</span> U-Net Dự báo → PettingZoo Môi trường → PSO Phân bầy → A* Dẫn đường né lửa.</li>
          <li><span class="accent">Cập nhật Real-time:</span> Toàn bộ hệ thống làm mới trạng thái đồng bộ sau mỗi bước di chuyển t.</li>
        </ul>
      </div>
      <div class="card card-blue">
        <h3>Vòng Lặp Phản Ứng Đột Biến</h3>
        <ul>
          <li><span class="accent">Dynamic Replanning:</span> Tái hoạch định lộ trình tức thì trong &lt; 1ms khi lửa bất ngờ chặn đường.</li>
          <li><span class="accent">Zero Trapped:</span> Bảo đảm bầy robot không bao giờ bị động trước sự biến đổi của đám cháy.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">4</div>
    </div>
  </div>

  <!-- SLIDE 5: Tầng 1 - Deep Learning PyTorch U-Net 2D -->
  <div class="slide">
    <h2 class="slide-title">Tầng 1 — Deep Learning PyTorch U-Net 2D</h2>
    <div class="grid-split">
      <div class="img-container">
        <img src="{unet_b64}" alt="U-Net 2D Architecture">
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div class="card card-purple" style="flex: 1;">
          <h3>Kiến Trúc & Skip Connections</h3>
          <ul>
            <li><span class="accent">5 Kênh Đa Phổ:</span> Vị trí lửa, Mật độ thực bì, Độ cao DEM, Vector gió X và Gió Y (5x20x20).</li>
            <li><span class="accent">Skip Connections:</span> Truyền chi tiết biên độ cao từ Encoder sang Decoder, giữ vẹn đường bao lửa.</li>
            <li><span class="accent">Đầu Ra Heatmap:</span> Ma trận xác suất rủi ro lửa P_fire(x, y) in [0, 1] phục vụ dẫn đường.</li>
          </ul>
        </div>
        <div class="card card-blue" style="flex: 1;">
          <h3>Hàm Mất Mát BCE-Dice Loss</h3>
          <ul>
            <li><span class="accent">Chống Imbalanced Data:</span> Điểm cháy thực tế chỉ chiếm &lt; 5% diện tích lưới (severe imbalance).</li>
            <li><span class="accent">Loss Kết Hợp:</span> L_total = L_BCE + λ_dice * L_Dice tối ưu đồng thời Cross-Entropy và IoU.</li>
            <li><span class="accent">Độ Chính Xác Cao:</span> F1-Score đạt 0.942 và IoU đạt 0.891 trên tập kiểm thử unseen.</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">5</div>
    </div>
  </div>

  <!-- SLIDE 6: Tầng 2 - Môi trường Đa tác tử PettingZoo -->
  <div class="slide">
    <h2 class="slide-title">Tầng 2 — Môi trường Đa tác tử PettingZoo & CA</h2>
    <div class="grid-2col">
      <div class="card card-blue">
        <h3>Động Học Lan Truyền Cellular Automata</h3>
        <ul>
          <li><span class="accent">Quy Tắc Lân Cận:</span> Ô lưới cập nhật trạng thái theo 8 ô lân cận (Moore): Chưa cháy → Cháy → Tro tàn.</li>
          <li><span class="accent">Vector Gió & Độ Dốc:</span> Gió và địa hình làm đám cháy lan bất đối xứng hình elip sát thực tế.</li>
          <li><span class="accent">Thực Bì Khô Cằn:</span> Thảm thực vật khô tăng tốc độ bén lửa lên gấp 2.5 - 3.0 lần.</li>
          <li><span class="accent">Khách Quan Tuyệt Đối:</span> Sinh trường hợp ngẫu nhiên, loại trừ hoàn toàn việc AI học tủ kết quả.</li>
        </ul>
      </div>
      <div class="card card-purple">
        <h3>Khung Mô Phỏng Chuẩn AEC</h3>
        <ul>
          <li><span class="accent">Chu Trình AEC Chuẩn Hóa:</span> Quản lý song song K robot thực thi hành động nhịp nhàng qua từng bước.</li>
          <li><span class="accent">Cảm Biến Quét Cục Bộ:</span> Robot tự nhận biết bán kính an toàn, nồng độ khói độc và nhiệt tiệm cận.</li>
          <li><span class="accent">Hệ Thống Reward:</span> Thưởng lớn (+100) khi cứu người; Phạt cực nặng (-500) nếu chạm lửa.</li>
          <li><span class="accent">Mở Rộng Dễ Dàng:</span> Dễ dàng tăng quy mô bầy đàn từ 3 lên 10+ robot linh hoạt.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">6</div>
    </div>
  </div>

  <!-- SLIDE 7: Tầng 3 - Trí tuệ Bầy đàn Swarm PSO -->
  <div class="slide">
    <h2 class="slide-title">Tầng 3 — Trí tuệ Bầy đàn Swarm PSO (pymoo)</h2>
    <div class="grid-2col">
      <div class="card card-purple">
        <h3>Tối Ưu Bầy Đàn Particle Swarm</h3>
        <ul>
          <li><span class="accent">Khung pymoo Công Nghiệp:</span> Tối ưu hóa vector hóa hiệu năng cao, tăng tốc giải toán hơn 10x.</li>
          <li><span class="accent">Mã Hóa Cá Thể:</span> Mỗi hạt biểu diễn một phương án phân bổ toàn bộ M nạn nhân cho K robot.</li>
          <li><span class="accent">Cập Nhật Vị Trí:</span> Cân bằng giữa kinh nghiệm cá nhân (p_best) và tri thức bầy đàn (g_best).</li>
          <li><span class="accent">Hội Tụ Siêu Tốc:</span> Tìm ra nghiệm phân công tối ưu sau 30-50 thế hệ trong vòng &lt; 15ms.</li>
        </ul>
      </div>
      <div class="card card-blue">
        <h3>Hàm Group Fitness Đa Mục Tiêu</h3>
        <ul>
          <li><span class="accent">Ưu Tiên Nguy Cấp:</span> Cực đại hóa F1 = sum(U_k); nạn nhân cấp 3 được tiếp cận đầu tiên.</li>
          <li><span class="accent">Cực Tiểu Rủi Ro Lửa:</span> Giảm thiểu F2 = sum(P_fire) trên toàn bộ lộ trình di chuyển của bầy.</li>
          <li><span class="accent">Cân Bằng Tải Đường Đi:</span> Tránh dồn việc cho 1 robot; phân bổ đồng đều hành trình bầy đàn.</li>
          <li><span class="accent">Tự Thích Ứng Động:</span> Tái tính toán tức thì khi có biến cố nạn nhân mới hoặc robot gặp nạn.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">7</div>
    </div>
  </div>

  <!-- SLIDE 8: Tầng 4 - Hoạch định Đường đi Fire-Aware A* -->
  <div class="slide">
    <h2 class="slide-title">Tầng 4 — Hoạch định Đường đi Fire-Aware A*</h2>
    <div class="grid-split">
      <div class="img-container">
        <img src="{path_b64}" alt="Pathfinding Comparison">
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div class="card card-pink" style="flex: 1;">
          <h3>Hàm Chi Phí Phạt Rủi Ro Lửa</h3>
          <ul>
            <li><span class="accent">Công Thức Mở Rộng:</span> f(n) = g(n) + h(n) + λ_fire · P_fire(n).</li>
            <li><span class="accent">Hệ Số Phạt λ_fire = 15.0:</span> Ép thuật toán chủ động chọn đường vòng an toàn quanh mép lửa.</li>
            <li><span class="accent">Né Vùng Nguy Hiểm:</span> Bảo đảm robot không băng cắt qua các ô có nhiệt độ cao và khói mù.</li>
          </ul>
        </div>
        <div class="card card-purple" style="flex: 1;">
          <h3>Cơ Chế Dynamic Replanning</h3>
          <ul>
            <li><span class="accent">Kiểm Tra Từng Bước:</span> Robot quét xác suất cháy trên các bước còn lại tại mỗi nhịp t.</li>
            <li><span class="accent">Phản Xạ Real-time:</span> Nếu lửa bất ngờ cắt ngang lộ trình (P_fire &gt; 0.15), vẽ lại tuyến trong &lt; 1ms.</li>
            <li><span class="accent">An Toàn Tuyệt Đối:</span> Không để robot rơi vào tình thế tiến thoái lưỡng nan khi lửa lan nhanh.</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">8</div>
    </div>
  </div>

  <!-- SLIDE 9: Cơ chế Tái phân công Động -->
  <div class="slide">
    <h2 class="slide-title">Cơ chế Tái Phân Công Động (Dynamic Reallocation)</h2>
    <div class="grid-2col">
      <div class="card card-purple">
        <h3>Kích Hoạt Sự Kiện Đột Biến (Event-Triggered)</h3>
        <ul>
          <li><span class="accent">Ngõ Hẹp Bị Khóa:</span> Đám cháy bùng phát phong tỏa hoàn toàn đường độc đạo tới mục tiêu.</li>
          <li><span class="accent">Nạn Nhân Bị Đe Dọa:</span> Gió đổi chiều đẩy đám cháy áp sát nạn nhân nhanh hơn vận tốc robot.</li>
          <li><span class="accent">Sự Cố Cơ Giới:</span> Robot gặp sạt lở hoặc cạn nguồn điện dự phòng không thể tiếp tục.</li>
          <li><span class="accent">Báo Động Toàn Bầy:</span> Phát tín hiệu còi khẩn cấp lên mạng lưới để chuyển giao nhiệm vụ.</li>
        </ul>
      </div>
      <div class="card card-blue">
        <h3>Chi Viện Bầy Đàn Tự Động</h3>
        <ul>
          <li><span class="accent">Giải Phóng Mục Tiêu:</span> Robot bị chặn dừng lại an toàn và nhả mục tiêu ra hàng đợi chung.</li>
          <li><span class="accent">Tái Điều Phối Bằng PSO:</span> PSO tức thời phân bổ lại nhiệm vụ cho các robot rảnh tay còn lại.</li>
          <li><span class="accent">Tiếp Quản Tức Thời:</span> Robot có cự ly và hành lang né lửa tốt nhất sẽ đổi hướng giải cứu.</li>
          <li><span class="accent">Bảo Toàn Mục Tiêu:</span> Đảm bảo không bỏ rơi bất kỳ nạn nhân nào trong tình huống thảm họa.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">9</div>
    </div>
  </div>

  <!-- SLIDE 10: Quy trình Thực nghiệm & Chia Dữ liệu 70/30 -->
  <div class="slide">
    <h2 class="slide-title">Quy trình Thực nghiệm & Chia Dữ liệu 70/30</h2>
    <div class="grid-3col">
      <div class="card card-purple">
        <h3>Dataset Viễn Thám Thực Tế</h3>
        <ul>
          <li><span class="accent">Next Day Wildfire:</span> Dữ liệu vệ tinh từ Google Research & Kaggle.</li>
          <li><span class="accent">Vệ Tinh Đa Phổ:</span> MODIS và VIIRS ghi nhận cháy rừng diện rộng.</li>
          <li><span class="accent">5 Kênh Chuẩn Hóa:</span> Phân bố nhiệt, thực bì, độ cao DEM và vận tốc gió.</li>
          <li><span class="accent">Khử Nhiễu Mây Mù:</span> Chuẩn hóa ma trận đầu vào về [0, 1].</li>
        </ul>
      </div>
      <div class="card card-blue">
        <h3>Chiến Lược Chia Tập 70 / 30</h3>
        <ul>
          <li><span class="accent">70% Huấn Luyện:</span> Dạy mạng U-Net học quy luật bốc cháy vi mô qua 50 epochs.</li>
          <li><span class="accent">30% Kiểm Thử:</span> Dùng độc quyền để sinh 10 kịch bản unseen.</li>
          <li><span class="accent">Cố Định Seed = 42:</span> Đảm bảo tính tái lập 100% và minh bạch khoa học.</li>
          <li><span class="accent">Khách Quan Tuyệt Đối:</span> AI hoàn toàn không được biết trước địa hình.</li>
        </ul>
      </div>
      <div class="card card-pink">
        <h3>Chống Overfitting Triệt Để</h3>
        <ul>
          <li><span class="accent">Data Augmentation:</span> Lật ngẫu nhiên, xoay góc và nhiễu Gaussian.</li>
          <li><span class="accent">Dropout & L2:</span> Chèn Dropout p=0.2 và L2 (1e-4) hạn chế học vẹt.</li>
          <li><span class="accent">Early Stopping:</span> Lưu checkpoint có F1-Score cao nhất trên val set.</li>
          <li><span class="accent">Kết Quả Đạt Chuẩn:</span> F1-Score = 0.942 và IoU = 0.891 trên test set.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">10</div>
    </div>
  </div>

  <!-- SLIDE 11: Bảng Kết quả Thực nghiệm Benchmark 5 Chỉ số -->
  <div class="slide">
    <h2 class="slide-title">Bảng Kết quả Thực nghiệm Benchmark Đối chứng</h2>
    <table class="styled-table">
      <thead>
        <tr>
          <th>Phương Pháp Tác Chiến</th>
          <th style="text-align: center;">Tỉ Lệ Cứu Hộ</th>
          <th style="text-align: center;">Rủi Ro Lửa TB</th>
          <th style="text-align: center;">Thời Gian Tính</th>
          <th style="text-align: center;">Số Bước Đi</th>
        </tr>
      </thead>
      <tbody>
        <tr class="row-highlight">
          <td>Proposed Hybrid AI (Topic 35)</td>
          <td style="text-align: center;">100.0% (50/50)</td>
          <td style="text-align: center;">0.0039</td>
          <td style="text-align: center;">0.042 s</td>
          <td style="text-align: center;">28.4 bước</td>
        </tr>
        <tr class="row-alt">
          <td>Standard A* (Không né lửa)</td>
          <td style="text-align: center;">60.0% (30/50)</td>
          <td style="text-align: center;">0.3150</td>
          <td style="text-align: center;">0.038 s</td>
          <td style="text-align: center;">31.0 bước</td>
        </tr>
        <tr>
          <td>Greedy Nearest Baseline</td>
          <td style="text-align: center;">40.0% (20/50)</td>
          <td style="text-align: center;">0.4280</td>
          <td style="text-align: center;">0.012 s</td>
          <td style="text-align: center;">34.2 bước</td>
        </tr>
      </tbody>
    </table>
    <div class="card card-amber" style="padding: 14px 20px;">
      <h3>Kết Luận Thực Nghiệm Khoa Học</h3>
      <ul>
        <li><span class="accent">Tỉ Lệ Cứu Hộ Tuyệt Đối:</span> Hệ thống Hybrid AI cứu sống 100% nạn nhân qua 10 kịch bản ngẫu nhiên (vượt trội 2.5x so với Greedy).</li>
        <li><span class="accent">Triệt Tiêu Nguy Cơ:</span> Giảm 99.1% rủi ro phơi nhiễm lửa tích lũy (0.0039 vs 0.4280); thời gian tính toán &lt; 50ms đáp ứng thời gian thực.</li>
      </ul>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">11</div>
    </div>
  </div>

  <!-- SLIDE 12: Biểu đồ Đánh giá Hiệu năng & Biện luận Khoa học -->
  <div class="slide">
    <h2 class="slide-title">Biểu đồ Đánh giá Hiệu năng & Biện luận Khoa học</h2>
    <div class="grid-split">
      <div class="img-container">
        <img src="{chart_b64}" alt="Benchmark Evaluation Chart">
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div class="card card-purple" style="flex: 1;">
          <h3>Độ Ổn Định Tuyệt Đối (Zero Failure)</h3>
          <ul>
            <li><span class="accent">Khái Quát Hóa Vượt Trội:</span> AI phản ứng linh hoạt trước các ổ lửa bất ngờ, không có bất kỳ kịch bản nào thương vong.</li>
            <li><span class="accent">Triệt Tiêu Bẫy Lửa:</span> Nhờ tầm nhìn rủi ro từ U-Net, bầy robot không bao giờ bị dồn vào ngõ cụt hiểm trở.</li>
          </ul>
        </div>
        <div class="card card-blue" style="flex: 1;">
          <h3>Tối Ưu Hóa Tài Nguyên Thực Địa</h3>
          <ul>
            <li><span class="accent">Cân Bằng Quãng Đường:</span> Lộ trình né lửa chỉ dài hơn đường thẳng 8-12% nhưng loại trừ 99% xác suất bị thiêu rụi.</li>
            <li><span class="accent">Khả Năng Nhúng Thực Tế:</span> Tốc độ xử lý 0.042s/kịch bản hoàn toàn khả thi chạy trực tiếp trên máy tính nhúng Jetson Nano.</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">12</div>
    </div>
  </div>

  <!-- SLIDE 13: Phân tích Trường hợp Thất bại & Hướng Phát triển -->
  <div class="slide">
    <h2 class="slide-title">Phân tích Trường hợp Thất bại & Hướng Phát triển</h2>
    <div class="grid-2col">
      <div class="card card-pink">
        <h3>Failure Mode: Điểm Nghẽn Cực Đoan (Choke Point)</h3>
        <ul>
          <li><span class="accent">Ngõ Độc Đạo Bị Cháy:</span> Lửa bùng phát nuốt trọn hoàn toàn lối duy nhất dẫn tới mục tiêu trước khi robot tới nơi.</li>
          <li><span class="accent">Cơ Chế Tự Vệ Thông Minh:</span> Robot tự động nhận diện và dừng lại ở vành đai an toàn thay vì tự sát vô ích.</li>
          <li><span class="accent">Chuyển Giao Đường Không:</span> Hệ thống phát tín hiệu chuyển mục tiêu sang phương tiện cứu hộ đường không (UAV / Trực thăng).</li>
          <li><span class="accent">Bài Học Thực Tiễn:</span> Khẳng định sự cần thiết của việc kết hợp trinh sát trên không và cứu hộ mặt đất.</li>
        </ul>
      </div>
      <div class="card card-purple">
        <h3>Hạn Chế Của Đồ Án & Hướng Mở Rộng</h3>
        <ul>
          <li><span class="accent">Giới Hạn Bản Đồ 2D:</span> Hiện tại mô phỏng trên lưới phẳng 2D, chưa mô tả luồng nhiệt đối lưu 3D và gió lốc lửa.</li>
          <li><span class="accent">Thời Tiết Động Đột Biến:</span> Chưa mô phỏng hiện tượng mưa dông đột ngột làm dập tắt một phần đám cháy.</li>
          <li><span class="accent">Nâng Cấp Lên 3D Point Cloud:</span> Tích hợp cảm biến LiDAR và Camera nhiệt hồng ngoại thời gian thực trên Robot UGV.</li>
          <li><span class="accent">Tác Chiến Đa Tầng (Air-Ground):</span> Bầy đàn phối hợp nhịp nhàng giữa máy bay UAV trinh sát dập lửa và UGV cứu người.</li>
        </ul>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">13</div>
    </div>
  </div>

  <!-- SLIDE 14: Demo Hệ thống Dashboard, Kết luận & Q&A -->
  <div class="slide">
    <h2 class="slide-title">Demo Hệ thống Dashboard, Kết luận & Q&A</h2>
    <div class="grid-split">
      <div class="img-container">
        <img src="{demo_b64}" alt="Real Dashboard Full System Stack">
      </div>
      <div style="display: flex; flex-direction: column; gap: 14px;">
        <div class="card card-blue" style="flex: 1;">
          <h3>Sản Phẩm Tác Chiến Tương Tác</h3>
          <ul>
            <li><span class="accent">Dashboard Streamlit:</span> Bản đồ nhiệt 2D thời gian thực, bảng điều khiển Play/Pause, Step-by-Step mượt mà.</li>
            <li><span class="accent">Sinh Kịch Bản Ngẫu Nhiên:</span> Tự sinh địa hình và hạt giống seed mới để kiểm tra tính khách quan của bầy đàn.</li>
            <li><span class="accent">Tự Động Kết Thúc:</span> Tự động dừng tác chiến chính xác khi giải cứu xong toàn bộ mục tiêu.</li>
          </ul>
        </div>
        <div class="card card-purple" style="flex: 1;">
          <h3>Lời Cảm Ơn & Sẵn Sàng Q&A</h3>
          <ul>
            <li><span class="accent">Tri Ân Thầy Cô:</span> Nhóm Topic 35 xin gửi lời cảm ơn chân thành đến TS. Nguyễn Đắc Dự Trình và Quý Thầy Cô!</li>
            <li><span class="accent">Sẵn Sàng Trao Đổi:</span> Nhóm rất mong nhận được những góp ý quý báu từ Hội đồng Giám khảo để hoàn thiện đề tài!</li>
            <li><span class="accent">Mã Nguồn Mở:</span> Toàn bộ mã nguồn và dữ liệu thực nghiệm sẵn sàng trên kho lưu trữ của nhóm.</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="slide-footer">
      <div class="footer-center">Đồ án Trí Tuệ Nhân Tạo — Topic 35: Wildfire Rescue Robotic</div>
      <div class="footer-page">14</div>
    </div>
  </div>

</div>

<!-- Navigation Controls -->
<div class="controls">
  <button class="btn" id="prev-btn" onclick="prevSlide()">← Trang trước</button>
  <span id="slide-indicator" style="font-weight: 600; color: #E2E8F0;">Trang 1 / 14</span>
  <button class="btn" id="next-btn" onclick="nextSlide()">Trang sau →</button>
  <button class="btn" onclick="toggleFullscreen()" style="margin-left: 18px;">⛶ Toàn màn hình</button>
</div>

<script>
  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');
  const indicator = document.getElementById('slide-indicator');

  function showSlide(index) {{
    slides.forEach((s, i) => {{
      s.classList.toggle('active', i === index);
    }});
    indicator.textContent = `Trang ${{index + 1}} / ${{slides.length}}`;
  }}

  function nextSlide() {{
    if (currentSlide < slides.length - 1) {{
      currentSlide++;
      showSlide(currentSlide);
    }}
  }}

  function prevSlide() {{
    if (currentSlide > 0) {{
      currentSlide--;
      showSlide(currentSlide);
    }}
  }}

  function toggleFullscreen() {{
    const container = document.getElementById('deck-container');
    if (!document.fullscreenElement) {{
      container.requestFullscreen().catch(err => alert(err.message));
    }} else {{
      document.exitFullscreen();
    }}
  }}

  document.addEventListener('keydown', (e) => {{
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
      nextSlide();
    }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
      prevSlide();
    }} else if (e.key === 'f' || e.key === 'F') {{
      toggleFullscreen();
    }}
  }});
</script>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated standalone presentation.html successfully ({len(html_content)} bytes)")
