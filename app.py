"""
Wildfire Rescue Swarm Intelligence Framework - Streamlit Web Dashboard
Upgraded Edition with Framed Sections, Anti-Overlap UI, and High-Contrast Tactical Map:
- 🌲 Bản đồ Rừng xanh đậm độ tương phản cao, hiện rõ lưới từng ô (x, y), tách biệt hoàn toàn với màu nền trang web
- 🗂️ Thanh bên Sidebar chia thành 6 Ô/Mục đóng khung chuyên biệt, viền sắc nét, loại bỏ độ trơn
- 🎲 Sinh ngẫu nhiên kịch bản mới (Randomized Scenarios on-the-fly) tránh biết trước kết quả
- ▶ Chạy tự động Animation từng bước thời gian thực (Live Step-by-Step Auto Play)
- 🚫 Khắc phục triệt để lỗi đè chữ (Text Overlap Fix) giữa Title và Legend
- ⚔️ Chế độ Chạy Đơn lẻ hoặc So sánh Đối đầu Trực tiếp (Proposed vs Baseline)
- 📊 Bộ thử nghiệm Benchmark 10 kịch bản khoa học
- 🧠 Deep Learning Fire Predictor (PyTorch U-Net 2D, BCE-Dice Loss, Next Day Wildfire Spread)
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Ensure project modules can be loaded
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.simulation import SimulationEngine, SimulationResult
from src.fire import FirePredictor
from src.canvas_player import render_canvas_player_html, render_dual_canvas_player_html
from models.unet import UNet2D, predict_fire_heatmap
from scenario_generator import generate_single_scenario
from main import load_config, load_test_scenarios, run_benchmark
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Wildfire Rescue Swarm Intelligence",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-End Styling with Framed Modular Architecture
st.markdown("""
<style>
    /* Main Background & Padding */
    .block-container {
        padding-top: 1.0rem;
        padding-bottom: 2.5rem;
    }
    
    /* Brand Header Box */
    .brand-box {
        background: linear-gradient(135deg, #172338 0%, #0d1524 100%);
        border: 1px solid #2e4161;
        border-radius: 14px;
        padding: 16px 22px;
        margin-bottom: 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
    }
    .brand-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff8c00 50%, #facc15 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .brand-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 4px;
    }

    /* Structured Section Cards in Main Content */
    .section-card {
        background: #0d131f;
        border: 1px solid #223249;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #1e2c40;
        padding-bottom: 10px;
        margin-bottom: 14px;
    }
    .section-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #f1f5f9;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar Modular Containers - Anti-Flat High-Contrast Cards */
    [data-testid="stSidebar"] {
        background-color: #070b13 !important;
        border-right: 1px solid #1c2738 !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] > div {
        background: linear-gradient(180deg, #0e1728 0%, #0a111e 100%) !important;
        border: 1.5px solid #233752 !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.45) !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:hover,
    [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
        border-color: #3b82f6 !important;
        box-shadow: 0 4px 18px rgba(59, 130, 246, 0.25) !important;
        transition: all 0.2s ease;
    }
    .sidebar-box-header {
        background: #141f33;
        border-left: 3.5px solid #3b82f6;
        color: #f8fafc;
        font-size: 0.84rem;
        font-weight: 700;
        padding: 6px 10px;
        border-radius: 4px;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Telemetry KPI Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 12px;
    }
    .kpi-item {
        background: #111a2b;
        border: 1px solid #223249;
        border-radius: 10px;
        padding: 12px 14px;
        text-align: center;
    }
    .kpi-item:hover {
        border-color: #ff8c00;
        transition: border-color 0.2s ease;
    }
    .kpi-label {
        font-size: 0.76rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 3px 0;
    }
    .kpi-sub {
        font-size: 0.72rem;
        color: #64748b;
    }

    /* Dedicated Legend Bar (No Overlapping) */
    .legend-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        background: #111a2b;
        border: 1px solid #223249;
        border-radius: 8px;
        padding: 9px 16px;
        margin-bottom: 12px;
        font-size: 0.82rem;
        color: #cbd5e1;
        align-items: center;
        justify-content: center;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .legend-dot {
        width: 14px;
        height: 14px;
        border-radius: 3px;
        display: inline-block;
    }

    /* Terminal Event Log */
    .terminal-box {
        background-color: #060a12;
        border: 1px solid #1c2738;
        border-radius: 8px;
        padding: 10px 12px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.8rem;
        color: #38bdf8;
        height: 180px;
        overflow-y: auto;
    }

    /* Status Badges */
    .status-badge-p {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid #059669;
        padding: 3px 10px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 0.78rem;
    }
    .status-badge-b {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid #dc2626;
        padding: 3px 10px;
        border-radius: 16px;
        font-weight: 700;
        font-size: 0.78rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_config():
    return load_config(os.path.join(BASE_DIR, "config", "default_config.json"))


cfg = get_config()


# ==============================================================================
# HELPER: EVENT LOG GENERATION
# ==============================================================================
def extract_simulation_events(frames, scenario_info, mode_name):
    """Generates human-readable chronological event logs from simulation frames."""
    events = []
    events.append(f"[Step 00] Khởi động hệ thống Swarm ({mode_name.upper()}).")
    events.append(f"[Step 00] Bản đồ: {scenario_info.get('grid_size', [20, 20])} | {len(scenario_info.get('robots', []))} Robot | {len(scenario_info.get('victims', []))} Nạn nhân.")

    rescued_so_far = set()
    dead_so_far = set()
    replan_prev = {r["id"]: 0 for r in scenario_info.get("robots", [])}

    for step_idx, f in enumerate(frames):
        # Victims status changes
        for v in f["victims"]:
            v_id = v["id"]
            if v["status"] == "rescued" and v_id not in rescued_so_far:
                rescued_so_far.add(v_id)
                events.append(f"[Step {step_idx:02d}] 🎉 Nạn nhân #{v_id} (Ưu tiên {v['priority']}) đã được CỨU THÀNH CÔNG!")
            elif v["status"] == "dead" and v_id not in dead_so_far:
                dead_so_far.add(v_id)
                events.append(f"[Step {step_idx:02d}] 💀 Nạn nhân #{v_id} đã bị LỬA THIÊU RỤI tại ({v['x']}, {v['y']})!")

        # Replanning events
        for r in f["robots"]:
            r_id = r["id"]
            if r["replanning_count"] > replan_prev.get(r_id, 0):
                replan_prev[r_id] = r["replanning_count"]
                events.append(f"[Step {step_idx:02d}] 🔄 Robot #{r_id} phát hiện lửa đe dọa -> ĐÃ TÁI LẬP TUYẾN ĐƯỜNG MỚI (Replan).")

    return events


# ==============================================================================
# HELPER: 2D PLOTLY MAP RENDERER (HIGH-CONTRAST TACTICAL GRID)
# ==============================================================================
def render_plotly_grid(frame):
    """
    Renders 2D tactical grid with distinct forest green terrain (#163d27),
    visible cell boundary grid lines, and high-contrast satellite styling.
    Zero internal title and zero internal legend to prevent overlap bugs.
    """
    fire_mat = np.array(frame["fire_grid"])
    risk_mat = np.array(frame["risk_map"])
    h, w = fire_mat.shape

    fig = go.Figure()

    # 1. Base: High-contrast Tactical Heatmap
    # Non-fire / safe forest cells render in rich pine green (#163d27), clearly contrasting with page background!
    fig.add_trace(go.Heatmap(
        z=risk_mat,
        colorscale=[
            [0.0, "#163d27"],   # Safe Pine Forest (Xanh rừng thông đậm nổi bật)
            [0.2, "#205537"],   # Mild warmth / vegetation
            [0.45, "#6b5417"],  # High risk fuel heating zone (Vàng đất cảnh báo)
            [0.75, "#b91c1c"],  # Severe fire risk front (Cam đỏ nguy hiểm)
            [1.0, "#ef4444"],   # Active flame front (Đỏ rực mồi lửa)
        ],
        showscale=True,
        colorbar=dict(title="Nguy Cơ", thickness=12, len=0.8, x=1.02),
        zmin=0.0,
        zmax=1.0,
        hoverinfo="z",
    ))

    # 2. Obstacles (slate stone texture)
    obs_x = [o[0] for o in frame["obstacles"]]
    obs_y = [o[1] for o in frame["obstacles"]]
    if obs_x:
        fig.add_trace(go.Scatter(
            x=obs_x, y=obs_y,
            mode="markers",
            marker=dict(symbol="square", size=18, color="#475569", line=dict(color="#1e293b", width=1.5)),
            name="Vật cản",
            hoverinfo="name",
            showlegend=False,
        ))

    # 3. Fires: Active (🔥) vs Burnt ash (⬛)
    fires_act = np.argwhere(fire_mat == 1)
    fires_ash = np.argwhere(fire_mat == 2)
    if len(fires_act) > 0:
        fig.add_trace(go.Scatter(
            x=[int(c[1]) for c in fires_act],
            y=[int(c[0]) for c in fires_act],
            mode="text+markers",
            text=["🔥"] * len(fires_act),
            textfont=dict(size=16),
            marker=dict(size=15, color="rgba(239, 68, 68, 0.45)"),
            name="Lửa cháy",
            hoverinfo="name",
            showlegend=False,
        ))
    if len(fires_ash) > 0:
        fig.add_trace(go.Scatter(
            x=[int(c[1]) for c in fires_ash],
            y=[int(c[0]) for c in fires_ash],
            mode="markers",
            marker=dict(symbol="square", size=16, color="#1e293b", line=dict(color="#0f172a", width=1)),
            name="Tàn tro",
            hoverinfo="name",
            showlegend=False,
        ))

    # 4. Robot Paths (AI Trajectories)
    bot_colors = ["#38bdf8", "#facc15", "#f43f5e", "#c084fc", "#34d399"]
    for i, r in enumerate(frame["robots"]):
        color = bot_colors[i % len(bot_colors)]
        if r["path"]:
            px_coords = [r["x"]] + [pt["x"] for pt in r["path"]]
            py_coords = [r["y"]] + [pt["y"] for pt in r["path"]]
            fig.add_trace(go.Scatter(
                x=px_coords, y=py_coords,
                mode="lines",
                line=dict(color=color, width=3, dash="dot"),
                name=f"Lộ trình #{r['id']}",
                showlegend=False,
                hoverinfo="skip",
            ))

    # 5. Victims
    v_icons = {"waiting": "🧑", "rescued": "✅", "trapped": "⚠️", "dead": "💀"}
    for v in frame["victims"]:
        icon = v_icons.get(v["status"], "🧑")
        p_border = "#ef4444" if v["priority"] == 3 else ("#f59e0b" if v["priority"] == 2 else "#38bdf8")
        fig.add_trace(go.Scatter(
            x=[v["x"]], y=[v["y"]],
            mode="text+markers",
            text=[icon],
            textfont=dict(size=16),
            marker=dict(size=22, color="#ffffff", line=dict(color=p_border, width=2.5)),
            name=f"Nạn nhân #{v['id']}",
            hovertext=f"Nạn nhân #{v['id']} | Ưu tiên: {v['priority']} | Trạng thái: {v['status']} | Chờ: {v['remaining_wait_time']}s",
            hoverinfo="text",
            showlegend=False,
        ))

    # 6. Robots
    for i, r in enumerate(frame["robots"]):
        color = bot_colors[i % len(bot_colors)]
        fig.add_trace(go.Scatter(
            x=[r["x"]], y=[r["y"]],
            mode="text+markers",
            text=["🤖"],
            textfont=dict(size=18),
            marker=dict(size=26, color=color, line=dict(color="#ffffff", width=2)),
            name=f"Robot #{r['id']}",
            hovertext=f"Robot #{r['id']} | Trạng thái: {r['status']} | Mục tiêu: #{r['target_victim_id']}",
            hoverinfo="text",
            showlegend=False,
        ))

    # Layout with visible cell grid lines and distinct tactical border
    fig.update_layout(
        height=570,
        xaxis=dict(
            range=[-0.5, w - 0.5],
            showgrid=True,
            zeroline=False,
            dtick=1,
            gridcolor="rgba(255, 255, 255, 0.14)",
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor="#3b4f6e",
            mirror=True,
        ),
        yaxis=dict(
            range=[h - 0.5, -0.5],
            showgrid=True,
            zeroline=False,
            dtick=1,
            gridcolor="rgba(255, 255, 255, 0.14)",
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor="#3b4f6e",
            mirror=True,
        ),
        margin=dict(l=5, r=10, t=10, b=10),
        plot_bgcolor="#163d27",   # Default lush forest background
        paper_bgcolor="#0d1421",  # Dark tactical container background
        font=dict(color="#cbd5e1"),
        showlegend=False,
    )
    return fig


# ==============================================================================
# SIDEBAR CONTROLS (6 DEDICATED MODULAR FRAMES)
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="background:#131c2c; border:1px solid #28374d; border-radius:10px; padding:12px; margin-bottom:12px; text-align:center;">
        <span style="font-size:1.5rem;">🔥🚁</span>
        <div style="font-size:1.02rem; font-weight:800; color:#f8fafc; margin-top:2px;">BẢNG ĐIỀU KHIỂN SWARM</div>
        <div style="font-size:0.75rem; color:#94a3b8;">Hệ thống Điều phối Robot Cứu hộ</div>
    </div>
    """, unsafe_allow_html=True)

    # Ô 1: CHẾ ĐỘ GIẢI THUẬT
    with st.container(border=True):
        st.markdown('<div class="sidebar-box-header"><span style="font-size:1.1rem;">🕹️</span> 1. CHẾ ĐỘ GIẢI THUẬT</div>', unsafe_allow_html=True)
        sim_mode_choice = st.selectbox(
            "Chọn thuật toán tác chiến:",
            ["proposed", "baseline", "compare"],
            format_func=lambda x: "✨ Proposed (PSO + Fire-Aware A*)" if x == "proposed" else ("⚙️ Baseline (Greedy + Standard A*)" if x == "baseline" else "⚔️ So sánh Đối đầu (Proposed vs Baseline)"),
            index=0,
        )

    # Ô 2: THAM SỐ AN TOÀN & RỦI RO
    with st.container(border=True):
        st.markdown('<div class="sidebar-box-header"><span style="font-size:1.1rem;">🛡️</span> 2. AN TOÀN & RỦI RO</div>', unsafe_allow_html=True)
        risk_weight_val = st.slider("Hệ số rủi ro (λ Risk Weight)", 1.0, 20.0, 8.0, 0.5)
        safety_buffer_val = st.slider("Bán kính vùng đệm an toàn", 0, 4, 2, 1)

    # Ô 3: CẤU HÌNH BẦY ĐÀN PSO
    with st.container(border=True):
        st.markdown('<div class="sidebar-box-header"><span style="font-size:1.1rem;">🐝</span> 3. BẦY ĐÀN PSO (SWARM AI)</div>', unsafe_allow_html=True)
        pso_pop_val = st.number_input("Dân số bầy (Pop Size)", 10, 60, 30, 5)
        pso_gen_val = st.number_input("Số thế hệ (Generations)", 10, 60, 35, 5)

    # Ô 4: ĐIỀU KIỆN MÔI TRƯỜNG & KHÍ HẬU
    with st.container(border=True):
        st.markdown('<div class="sidebar-box-header"><span style="font-size:1.1rem;">🌪️</span> 4. KHÍ HẬU & MÔI TRƯỜNG</div>', unsafe_allow_html=True)
        wind_spd_val = st.slider("Tốc độ gió (m/s)", 0.0, 4.0, 1.5, 0.1)
        wind_dir_deg_val = st.slider("Hướng gió (độ)", 0, 360, 45, 15)
        wind_rad_val = np.radians(wind_dir_deg_val)
        wind_vec_val = [float(np.cos(wind_rad_val)), float(np.sin(wind_rad_val))]
        st.caption(f"🧭 Hướng vector gió: `({wind_vec_val[0]:.2f}, {wind_vec_val[1]:.2f})`")

    # Ô 5: TỐC ĐỘ MÔ PHỎNG REAL-TIME
    with st.container(border=True):
        st.markdown('<div class="sidebar-box-header"><span style="font-size:1.1rem;">⏱️</span> 5. TỐC ĐỘ PHÁT (ANIMATION)</div>', unsafe_allow_html=True)
        play_delay = st.slider("Thời gian delay mỗi bước (giây)", 0.05, 0.8, 0.15, 0.05)
        st.caption("Kéo sang trái để mô phỏng chạy nhanh hơn")

    # Ô 6: TRẠNG THÁI HỆ THỐNG
    with st.container(border=True):
        st.markdown('<div class="sidebar-box-header"><span style="font-size:1.1rem;">🟢</span> 6. TRẠNG THÁI HỆ THỐNG</div>', unsafe_allow_html=True)
        model_file = os.path.join(BASE_DIR, "models", "best_unet_fire.pth")
        if os.path.exists(model_file):
            st.success("🟢 U-Net Checkpoint: Đã nạp (`best_unet_fire.pth`)")
        else:
            st.warning("🟡 U-Net Checkpoint: Mặc định")
        st.caption("Thiết bị tính toán: **PyTorch CPU/CUDA Engine**")


# ==============================================================================
# MAIN BRAND BANNER
# ==============================================================================
st.markdown("""
<div class="brand-box">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="brand-title">🔥 Wildfire Rescue Swarm Intelligence</h1>
            <div class="brand-desc">Hệ thống Điều phối Bầy đàn Robot Cứu hộ Đám cháy Rừng Tự động với PyTorch U-Net & PSO Swarm</div>
        </div>
        <div style="display: flex; gap: 8px; margin-top: 8px;">
            <span class="status-badge-p">● Deep Learning U-Net Sẵn sàng</span>
            <span class="status-badge-b">● Multi-Agent PSO Hoạt động</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

nav_tabs = st.tabs([
    "🎮 Mô Phỏng Trực Tiếp (Live Simulation)",
    "📊 Đánh Giá Benchmark (10 Test Scenarios)",
    "🧠 Mô Hình Deep Learning (U-Net Fire Predictor)",
])


# ==============================================================================
# TAB 1: LIVE SIMULATION DASHBOARD (FRAMED SECTIONS)
# ==============================================================================
with nav_tabs[0]:

    # --------------------------------------------------------------------------
    # KHUNG 1: THIẾT LẬP KỊCH BẢN (SCENARIO CONTROL FRAME)
    # --------------------------------------------------------------------------
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">🎮 KHUNG 1: THIẾT LẬP VÀ SINH KỊCH BẢN TÁC CHIẾN</div>
            <span style="font-size:0.8rem; color:#94a3b8;">Chọn kịch bản cố định hoặc sinh ngẫu nhiên hoàn toàn mới</span>
        </div>
    """, unsafe_allow_html=True)

    top_c1, top_c2, top_c3 = st.columns([2, 2, 2])
    with top_c1:
        scenario_source = st.radio(
            "Nguồn Kịch Bản:",
            ["🎲 Sinh Ngẫu Nhiên (Tránh biết trước)", "📁 Chọn Từ Bộ Kịch Bản Có Sẵn"],
            horizontal=False,
        )

    # Manage Active Scenario in session_state
    if "active_scenario" not in st.session_state:
        st.session_state["active_scenario"] = generate_single_scenario("random_init", seed=int(time.time()) % 100000, grid_size=20)
        st.session_state["scenario_name"] = "Kịch bản Ngẫu nhiên Khởi tạo"

    if scenario_source == "🎲 Sinh Ngẫu Nhiên (Tránh biết trước)":
        with top_c2:
            st.write("")
            rand_btn = st.button("🎲 Sinh Ngẫu Nhiên Bản Đồ Mới", type="primary", use_container_width=True)
            if rand_btn:
                new_seed = int(time.time() * 1000) % 1000000
                st.session_state["active_scenario"] = generate_single_scenario(
                    f"random_{new_seed % 1000:03d}",
                    seed=new_seed,
                    grid_size=20,
                )
                st.session_state["scenario_name"] = f"Kịch bản Ngẫu Nhiên (Mã #{new_seed % 1000:03d})"
                if "sim_cache" in st.session_state:
                    del st.session_state["sim_cache"]
                st.rerun()

        with top_c3:
            sc_obj = st.session_state["active_scenario"]
            st.info(f"**Bản đồ đang nạp:** {st.session_state.get('scenario_name', 'Kịch bản')}\n- Hạt giống (Seed): `{sc_obj.get('seed')}`\n- {len(sc_obj['victims'])} Nạn nhân | {len(sc_obj['robots'])} Robot")
    else:
        sc_dir = os.path.join(BASE_DIR, "data", "scenarios")
        with top_c2:
            preset_file = st.selectbox("Tập kịch bản:", ["scenarios_test.json", "scenarios_dev.json", "scenarios_val.json"])
        with top_c3:
            with open(os.path.join(sc_dir, preset_file), "r", encoding="utf-8") as f:
                loaded_presets = json.load(f)
            preset_id = st.selectbox("Mã kịch bản:", [p["id"] for p in loaded_presets])
            selected_preset = next(p for p in loaded_presets if p["id"] == preset_id)
            if st.session_state.get("scenario_name") != preset_id:
                st.session_state["active_scenario"] = selected_preset
                st.session_state["scenario_name"] = preset_id
                if "sim_cache" in st.session_state:
                    del st.session_state["sim_cache"]

    st.markdown("</div>", unsafe_allow_html=True)

    sc_active = st.session_state["active_scenario"]

    # --------------------------------------------------------------------------
    # EXECUTION ENGINE & CACHING
    # --------------------------------------------------------------------------
    sim_cache_key = f"res_{sc_active.get('seed')}_{sim_mode_choice}_{risk_weight_val}_{safety_buffer_val}_{wind_spd_val}_{wind_dir_deg_val}"

    if "sim_cache" not in st.session_state or st.session_state.get("last_cache_key") != sim_cache_key:
        exec_cfg = dict(cfg)
        exec_cfg["risk_weight"] = risk_weight_val
        exec_cfg["safety_buffer_radius"] = safety_buffer_val
        exec_cfg["pso"] = {"pop_size": pso_pop_val, "max_gen": pso_gen_val, "seed": sc_active.get("seed", 42)}

        custom_sc = dict(sc_active)
        custom_sc["wind_direction"] = wind_vec_val
        custom_sc["wind_speed"] = wind_spd_val

        if sim_mode_choice in ("proposed", "baseline"):
            with st.spinner("Đang tính toán quỹ đạo di chuyển và tương tác môi trường..."):
                engine = SimulationEngine(config=exec_cfg, scenario_data=custom_sc, mode=sim_mode_choice)
                res_main = engine.run(record_frames=True)
                st.session_state["sim_cache"] = {"main": res_main}
                st.session_state["last_cache_key"] = sim_cache_key
        else:
            with st.spinner("Đang chạy đối kháng cả 2 giải thuật (Proposed vs Baseline)..."):
                eng_p = SimulationEngine(config=exec_cfg, scenario_data=custom_sc, mode="proposed")
                res_p = eng_p.run(record_frames=True)
                eng_b = SimulationEngine(config=exec_cfg, scenario_data=custom_sc, mode="baseline")
                res_b = eng_b.run(record_frames=True)
                st.session_state["sim_cache"] = {"prop": res_p, "base": res_b}
                st.session_state["last_cache_key"] = sim_cache_key

    # --------------------------------------------------------------------------
    # KHUNG 2: ĐỒNG HỒ ĐO CHỈ SỐ NHIỆM VỤ (MISSION TELEMETRY FRAME)
    # --------------------------------------------------------------------------
    if sim_mode_choice in ("proposed", "baseline"):
        res_active: SimulationResult = st.session_state["sim_cache"]["main"]
        frames = res_active.frames
        max_f = len(frames)

        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <div class="section-title">📊 KHUNG 2: ĐỒNG HỒ ĐO CHỈ SỐ NHIỆM VỤ (MISSION TELEMETRY)</div>
                <span style="font-size:0.8rem; color:#94a3b8;">5 Chỉ số cốt lõi đánh giá hiệu quả giải cứu và an toàn</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi-item" style="border-top: 3px solid #10b981;">
                <div class="kpi-label">Tỉ Lệ Cứu Hộ</div>
                <div class="kpi-value" style="color: {'#10b981' if res_active.rescue_success_rate >= 80 else '#f59e0b'};">
                    {res_active.rescue_success_rate:.1f}%
                </div>
                <div class="kpi-sub">Đã cứu: {res_active.rescued_count}/{res_active.num_victims} nạn nhân</div>
            </div>
            <div class="kpi-item" style="border-top: 3px solid #6366f1;">
                <div class="kpi-label">Tổng Quãng Đường</div>
                <div class="kpi-value" style="color: #818cf8;">{res_active.total_distance} <span style="font-size:0.9rem;">bước</span></div>
                <div class="kpi-sub">Trung bình: {res_active.total_distance / max(1, len(sc_active['robots'])):.1f} bước / robot</div>
            </div>
            <div class="kpi-item" style="border-top: 3px solid #f43f5e;">
                <div class="kpi-label">Rủi Ro Phơi Nhiễm</div>
                <div class="kpi-value" style="color: {'#f43f5e' if res_active.fire_risk_exposure > 8 else '#38bdf8'};">
                    {res_active.fire_risk_exposure}
                </div>
                <div class="kpi-sub">Số bước đi sát đám cháy</div>
            </div>
            <div class="kpi-item" style="border-top: 3px solid #0ea5e9;">
                <div class="kpi-label">Thời Gian Tác Chiến</div>
                <div class="kpi-value" style="color: #38bdf8;">{res_active.execution_time_steps} <span style="font-size:0.9rem;">steps</span></div>
                <div class="kpi-sub">Giới hạn tối đa: {sc_active['max_steps']} steps</div>
            </div>
            <div class="kpi-item" style="border-top: 3px solid #a855f7;">
                <div class="kpi-label">Lượt Tái Lập Tuyến</div>
                <div class="kpi-value" style="color: #c084fc;">{res_active.replanning_count}</div>
                <div class="kpi-sub">Thích nghi động khi lửa lan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # ----------------------------------------------------------------------
        # KHUNG 3: TRUNG TÂM TÁC CHIẾN BẢN ĐỒ & HOẠT HỌA (MAP & SIMULATION FRAME)
        # ----------------------------------------------------------------------
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <div class="section-title">🗺️ KHUNG 3: TRUNG TÂM TÁC CHIẾN BẢN ĐỒ 2D & HOẠT HỌA THỜI GIAN THỰC (60 FPS)</div>
                <span style="font-size:0.8rem; color:#34d399; font-weight:600;">● Engine đồ họa Canvas mượt mà — Chống chớp giật 100%</span>
            </div>
        """, unsafe_allow_html=True)

        events_history = extract_simulation_events(frames, sc_active, res_active.mode)

        player_html = render_canvas_player_html(
            frames=frames,
            scenario_info=sc_active,
            mode_name=res_active.mode,
            events_history=events_history,
        )
        components.html(player_html, height=775, scrolling=False)

        # Optional Static Plotly View
        with st.expander("🔍 Chế độ Phân tích Tọa độ Tĩnh (Plotly Grid & Xuất ảnh)", expanded=False):
            st.caption("Khảo sát tĩnh từng bước thời gian và dùng công cụ Plotly để đo tọa độ chi tiết hoặc tải ảnh.")
            cur_step = st.slider("⏱️ Kéo bước khảo sát tĩnh:", 0, max_f - 1, 0, key="manual_step_slider")
            f_current = frames[cur_step]

            col_map, col_details = st.columns([3, 1])
            with col_map:
                fig_frame = render_plotly_grid(f_current)
                st.plotly_chart(fig_frame, use_container_width=True)

            with col_details:
                st.markdown("**📝 Trạng thái Nạn nhân:**")
                for v in f_current["victims"]:
                    status_badge = {"waiting": "🟡 Chờ cứu", "rescued": "🟢 Đã cứu", "trapped": "🟠 Mắc kẹt", "dead": "🔴 Đã mất"}
                    st.caption(f"**Nạn nhân #{v['id']}** (Ưu tiên {v['priority']}) | {status_badge.get(v['status'], v['status'])} | Chờ: {v['remaining_wait_time']}s")

                st.markdown("---")
                st.markdown("**🤖 Đội Robot Cứu Hộ:**")
                for r in f_current["robots"]:
                    st.caption(f"**Robot #{r['id']}**: {r['status']} | Quãng đường: {r['total_distance']} | Rủi ro: {r['fire_risk_exposure']}")

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # DUAL HEAD-TO-HEAD COMPARISON MODE (FRAMED)
        res_p: SimulationResult = st.session_state["sim_cache"]["prop"]
        res_b: SimulationResult = st.session_state["sim_cache"]["base"]

        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <div class="section-title">⚔️ KHUNG SO SÁNH ĐỐI ĐẦU ĐỒNG THỜI (PROPOSED VS BASELINE)</div>
                <span style="font-size:0.8rem; color:#34d399; font-weight:600;">● Engine đồ họa đồng bộ 60 FPS — Chống chớp giật 100%</span>
            </div>
        """, unsafe_allow_html=True)

        # Comparison summary metrics
        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        with c_m1:
            diff_sr = res_p.rescue_success_rate - res_b.rescue_success_rate
            st.metric("Tỉ Lệ Cứu Hộ", f"{res_p.rescue_success_rate:.1f}%", f"{diff_sr:+.1f}% vs Baseline", delta_color="normal")
        with c_m2:
            diff_risk = res_b.fire_risk_exposure - res_p.fire_risk_exposure
            st.metric("Giảm Thiểu Phơi Nhiễm", f"{res_p.fire_risk_exposure} lần", f"{diff_risk:+d} bước an toàn hơn", delta_color="normal")
        with c_m3:
            diff_dist = res_b.total_distance - res_p.total_distance
            st.metric("Tổng Quãng Đường", f"{res_p.total_distance} bước", f"{diff_dist:+d} bước", delta_color="inverse")
        with c_m4:
            st.metric("Khả Năng Tái Lập Tuyến (Replan)", f"{res_p.replanning_count} lần", f"{res_p.replanning_count - res_b.replanning_count:+d} so với Baseline")

        events_p = extract_simulation_events(res_p.frames, sc_active, "proposed")
        events_b = extract_simulation_events(res_b.frames, sc_active, "baseline")

        dual_player_html = render_dual_canvas_player_html(
            frames_p=res_p.frames,
            frames_b=res_b.frames,
            scenario_info=sc_active,
            events_p=events_p,
            events_b=events_b,
        )
        components.html(dual_player_html, height=720, scrolling=False)

        with st.expander("🔍 Chế độ Phân tích Đối đầu Tĩnh (Plotly Grid & Xuất ảnh)", expanded=False):
            max_dual_steps = max(len(res_p.frames), len(res_b.frames))
            dual_step = st.slider("⏱️ Kéo Thanh Thời Gian Cả 2 Phương Pháp:", 0, max_dual_steps - 1, min(12, max_dual_steps - 1), key="dual_static_slider")

            f_p = res_p.frames[min(dual_step, len(res_p.frames) - 1)]
            f_b = res_b.frames[min(dual_step, len(res_b.frames) - 1)]

            dual_col1, dual_col2 = st.columns(2)
            with dual_col1:
                st.caption(f"✨ PROPOSED (PSO + U-Net) — Bước {dual_step}")
                fig_p = render_plotly_grid(f_p)
                st.plotly_chart(fig_p, use_container_width=True)

            with dual_col2:
                st.caption(f"⚙️ BASELINE (Greedy + A*) — Bước {dual_step}")
                fig_b = render_plotly_grid(f_b)
                st.plotly_chart(fig_b, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 2: BENCHMARK & EVALUATION (FRAMED)
# ==============================================================================
with nav_tabs[1]:
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">📊 BÁO CÁO THỬ NGHIỆM KHOA HỌC (10 KỊCH BẢN TEST ĐỘC LẬP)</div>
            <span style="font-size:0.8rem; color:#94a3b8;">Kiểm chứng thống kê lặp lại với hạt giống cố định</span>
        </div>
    """, unsafe_allow_html=True)

    csv_file_path = os.path.join(BASE_DIR, "benchmark_results.csv")
    b_left, b_right = st.columns([3, 1])
    with b_right:
        run_bench_btn = st.button("🚀 Chạy Lại Toàn Bộ Benchmark", type="primary", use_container_width=True)

    if run_bench_btn or not os.path.exists(csv_file_path):
        with st.spinner("Đang chạy 10 kịch bản thử nghiệm đối chứng..."):
            df_b = run_benchmark(output_csv="benchmark_results.csv")
            st.success("Đã hoàn thành đánh giá thực nghiệm!")
    else:
        df_b = pd.read_csv(csv_file_path)

    if not df_b.empty:
        base_df = df_b[df_b["mode"] == "baseline"]
        prop_df = df_b[df_b["mode"] == "proposed"]

        metrics_def = [
            ("rescue_success_rate", "Tỉ Lệ Cứu Hộ Thành Công (%)", True),
            ("total_distance", "Tổng Quãng Đường Di Chuyển (Grid steps)", False),
            ("fire_risk_exposure", "Mức Độ Phơi Nhiễm Rủi Ro Lửa (Count)", False),
            ("execution_time_steps", "Thời Gian Hoàn Thành (Steps)", False),
            ("replanning_count", "Số Lượt Tái Lập Tuyến Đường (Count)", None),
        ]

        summary_data = []
        for key, name, is_higher_better in metrics_def:
            b_mean, b_std = base_df[key].mean(), base_df[key].std()
            p_mean, p_std = prop_df[key].mean(), prop_df[key].std()

            if is_higher_better is True:
                diff = ((p_mean - b_mean) / (b_mean + 1e-6)) * 100.0
                tag = f"🟢 **{diff:+.1f}%**"
            elif is_higher_better is False:
                diff = ((b_mean - p_mean) / (b_mean + 1e-6)) * 100.0
                tag = f"🟢 **{diff:+.1f}% (an toàn hơn)**" if diff > 0 else f"🔴 {diff:+.1f}%"
            else:
                tag = f"🟣 **{p_mean - b_mean:+.1f} (thích nghi cao)**"

            summary_data.append({
                "Chỉ Số Đánh Giá (Metric)": name,
                "Baseline (Greedy + Standard A*)": f"{b_mean:.2f} ± {b_std:.2f}",
                "Proposed (PSO + Fire-Aware A*)": f"{p_mean:.2f} ± {p_std:.2f}",
                "Mức Độ Cải Thiện": tag,
            })

        st.markdown("##### 📌 Bảng Thống Kê So Sánh (Mean ± Std qua 10 Kịch Bản Test)")
        st.table(pd.DataFrame(summary_data))

        # Charts
        st.markdown("##### 📈 Biểu Đồ Thống Kê Đối Chứng")
        chart1, chart2 = st.columns(2)
        with chart1:
            f1 = px.bar(
                df_b, x="scenario_id", y="rescue_success_rate", color="mode", barmode="group",
                title="Tỉ Lệ Cứu Hộ Thành Công (%)",
                color_discrete_map={"baseline": "#ef4444", "proposed": "#10b981"},
            )
            f1.update_layout(paper_bgcolor="#090d16", plot_bgcolor="#090d16", font=dict(color="#cbd5e1"))
            st.plotly_chart(f1, use_container_width=True)

        with chart2:
            f2 = px.bar(
                df_b, x="scenario_id", y="fire_risk_exposure", color="mode", barmode="group",
                title="Mức Độ Phơi Nhiễm Rủi Ro Lửa (Thấp hơn là an toàn hơn)",
                color_discrete_map={"baseline": "#ef4444", "proposed": "#38bdf8"},
            )
            f2.update_layout(paper_bgcolor="#090d16", plot_bgcolor="#090d16", font=dict(color="#cbd5e1"))
            st.plotly_chart(f2, use_container_width=True)

        with st.expander("🔍 Xem Bảng Dữ Liệu Chi Tiết"):
            st.dataframe(df_b, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# TAB 3: DEEP LEARNING FIRE PREDICTOR (FRAMED)
# ==============================================================================
with nav_tabs[2]:
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-title">🧠 MÔ HÌNH HỌC SÂU U-NET 2D DỰ ĐOÁN LỬA LAN KHÔNG GIAN - THỜI GIAN</div>
            <span style="font-size:0.8rem; color:#94a3b8;">Next Day Wildfire Spread (Google Research / Kaggle)</span>
        </div>
    """, unsafe_allow_html=True)

    spec_c, plot_c = st.columns([1, 1])
    with spec_c:
        st.markdown(r"""
        **Kiến Trúc Mạng & Cơ Chế Kiểm Soát Overfitting:**
        - **Kiến trúc mạng**: `UNet2D(in_channels=5, out_channels=1)` với 4 tầng Down/Up và Skip Connections.
        - **5 Kênh đầu vào**:
          1. `Ch 0: Fire_t` — Vết cháy / Điểm bắt lửa tại thời điểm hiện tại.
          2. `Ch 1: Elevation` — Địa hình độ cao DEM chuẩn hóa.
          3. `Ch 2: Vegetation` — Mật độ thực vật / Sinh khối nhiên liệu.
          4. `Ch 3: Wind U` — Vector gió trục Đông - Tây.
          5. `Ch 4: Wind V` — Vector gió trục Bắc - Nam.
        - **Kênh đầu ra**: Xác suất cháy $P(x, y) \in [0.0, 1.0]$ thời điểm $t+1$.
        - **Hàm Loss**: `BCEDiceLoss` ($\mathcal{L}_{\text{BCE}} + \mathcal{L}_{\text{Dice}}$) xử lý mất cân bằng dữ liệu cực đoan.
        - **Kỹ thuật chống Overfitting**:
          - Geometric Data Augmentation (Flip, Rotation xoay kèm vector gió).
          - Dropout 2D ($p=0.2$).
          - Optimizer `AdamW` (Weight decay $10^{-4}$) & `CosineAnnealingLR`.
        """)

        hist_json = os.path.join(BASE_DIR, "models", "training_history.json")
        if os.path.exists(hist_json):
            with open(hist_json, "r") as f:
                h_info = json.load(f)
            st.success(f"""
            🏆 **Thành Tích Tốt Nhất Trên 30% Test Set (Epoch {h_info['best_epoch']}):**
            - **F1-Score**: `{h_info['best_f1']:.4f}`
            - **IoU (Jaccard Index)**: `{h_info['iou'][h_info['best_epoch']-1]:.4f}`
            - **Precision**: `{h_info['precision'][h_info['best_epoch']-1]:.4f}`
            - **Recall**: `{h_info['recall'][h_info['best_epoch']-1]:.4f}`
            - **Validation Loss**: `{h_info['val_loss'][h_info['best_epoch']-1]:.4f}`
            """)

    with plot_c:
        curve_png = os.path.join(BASE_DIR, "logs", "loss_curve.png")
        if os.path.exists(curve_png):
            st.image(Image.open(curve_png), caption="Biểu đồ Hội tụ Loss & 5 Chỉ số Đánh giá trên 30% Test Set", use_container_width=True)

    st.markdown("---")
    st.markdown("##### 🔬 Thử Nghiệm Dự Đoán Bản Đồ Nhiệt Xác Suất Cháy (Live Heatmap Generator)")

    heat_c1, heat_c2, heat_c3 = st.columns(3)
    with heat_c1:
        test_ignitions = st.slider("Số điểm bắt lửa thử nghiệm:", 1, 4, 2)
    with heat_c2:
        test_wind_s = st.slider("Tốc độ gió thử nghiệm (m/s):", 0.0, 4.0, 1.8, 0.1)
    with heat_c3:
        test_wind_deg = st.slider("Hướng gió thử nghiệm (độ):", 0, 360, 45, 15)

    test_rad = np.radians(test_wind_deg)
    test_vec = (float(np.cos(test_rad)), float(np.sin(test_rad)))

    # Generate synthetic input
    dim = 24
    fire_in = np.zeros((dim, dim), dtype=np.float32)
    rng_vis = np.random.RandomState(42)
    for _ in range(test_ignitions):
        fire_in[rng_vis.randint(6, dim - 6), rng_vis.randint(6, dim - 6)] = 1.0

    veg_in = rng_vis.uniform(0.4, 0.9, size=(dim, dim)).astype(np.float32)
    elev_in = np.zeros((dim, dim), dtype=np.float32)

    predictor = FirePredictor()
    pred_risk_map = predictor.predict_risk_map(
        fire_grid=fire_in,
        fuel_grid=veg_in,
        wind_direction=test_vec,
        wind_speed=test_wind_s,
        elevation_grid=elev_in,
    )

    out_c1, out_c2 = st.columns(2)
    with out_c1:
        fig_src = px.imshow(
            fire_in,
            title="Đầu vào: Vết cháy & Mồi lửa hiện tại (t)",
            color_continuous_scale=[[0, "#0f172a"], [1, "#ef4444"]],
        )
        fig_src.update_layout(paper_bgcolor="#090d16", font=dict(color="#cbd5e1"))
        st.plotly_chart(fig_src, use_container_width=True)

    with out_c2:
        fig_heat = px.imshow(
            pred_risk_map,
            title="Đầu ra U-Net 2D: Xác suất cháy lan P(x, y) thời điểm t+1",
            color_continuous_scale="Inferno",
            zmin=0.0,
            zmax=1.0,
        )
        fig_heat.update_layout(paper_bgcolor="#090d16", font=dict(color="#cbd5e1"))
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
