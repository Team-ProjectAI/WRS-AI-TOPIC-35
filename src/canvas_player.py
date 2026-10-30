"""
High-Performance HTML5 Canvas Simulation Player for Wildfire Rescue Swarm.
Client-side 60 FPS rendering with zero screen flickering, interactive controls,
tactical high-contrast pine forest grid, and live terminal event stream.
"""

import json
from typing import List, Dict, Any


def render_canvas_player_html(
    frames: List[Dict[str, Any]],
    scenario_info: Dict[str, Any],
    mode_name: str,
    events_history: List[str],
) -> str:
    """
    Renders single simulation mode in an interactive, non-flickering HTML5 Canvas player.
    """
    frames_json = json.dumps(frames)
    scenario_json = json.dumps(scenario_info)
    events_json = json.dumps(events_history)

    mode_badge = (
        '<span style="background:rgba(16,185,129,0.25); color:#34d399; border:1px solid #059669; padding:4px 12px; border-radius:16px; font-weight:700; font-size:0.82rem;">✨ PROPOSED (PSO + U-Net)</span>'
        if mode_name == "proposed"
        else '<span style="background:rgba(239,68,68,0.25); color:#f87171; border:1px solid #dc2626; padding:4px 12px; border-radius:16px; font-weight:700; font-size:0.82rem;">⚙️ BASELINE (Greedy + A*)</span>'
    )

    html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
    <meta charset="UTF-8">
    <style>
        * {{
            box-sizing: border-box;
            user-select: none;
        }}
        body {{
            margin: 0;
            padding: 4px;
            background: #090d16;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            overflow-x: hidden;
        }}
        .player-container {{
            background: #0f172a;
            border: 1.5px solid #253852;
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        }}
        /* Top HUD Bar */
        .hud-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            background: #131d31;
            border: 1px solid #223249;
            padding: 10px 16px;
            border-radius: 10px;
            margin-bottom: 12px;
        }}
        .hud-title {{
            font-size: 0.98rem;
            font-weight: 700;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .hud-pill {{
            background: #1e293b;
            border: 1px solid #334155;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8rem;
            color: #cbd5e1;
            font-weight: 600;
        }}
        .hud-pill b {{
            color: #38bdf8;
        }}

        /* Control Panel */
        .control-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            background: #111a2c;
            border: 1px solid #1e2d42;
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 12px;
        }}
        .btn-group {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-ctl {{
            background: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        .btn-ctl:hover {{
            background: #334155;
            border-color: #64748b;
        }}
        .btn-ctl.primary {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border-color: #3b82f6;
            color: #ffffff;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.35);
        }}
        .btn-ctl.primary:hover {{
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        }}
        .btn-ctl.active-pause {{
            background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
            border-color: #f59e0b;
        }}

        .select-ctl {{
            background: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 0.8rem;
            outline: none;
            cursor: pointer;
        }}
        .chk-wrap {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.8rem;
            color: #94a3b8;
            cursor: pointer;
        }}
        .chk-wrap input {{
            cursor: pointer;
            accent-color: #2563eb;
        }}

        /* Scrubber Slider */
        .timeline-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            padding: 0 4px;
        }}
        .range-slider {{
            flex: 1;
            height: 6px;
            -webkit-appearance: none;
            background: #1e293b;
            border-radius: 4px;
            outline: none;
            cursor: pointer;
        }}
        .range-slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #38bdf8;
            border: 2px solid #ffffff;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.6);
            cursor: pointer;
            transition: transform 0.1s ease;
        }}
        .range-slider::-webkit-slider-thumb:hover {{
            transform: scale(1.2);
        }}
        .step-label {{
            min-width: 90px;
            font-size: 0.85rem;
            font-weight: 700;
            color: #38bdf8;
            text-align: right;
            font-family: monospace;
        }}

        /* Main Canvas Layout */
        .viewport-row {{
            display: flex;
            gap: 14px;
            align-items: flex-start;
        }}
        .canvas-card {{
            flex: 0 0 530px;
            position: relative;
            background: #080d1a;
            border: 2px solid #1e3a5f;
            border-radius: 10px;
            padding: 6px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
        }}
        #simCanvas {{
            display: block;
            background: #123820;
            border-radius: 6px;
            cursor: crosshair;
        }}
        .canvas-tooltip {{
            position: absolute;
            display: none;
            background: rgba(15, 23, 42, 0.95);
            border: 1px solid #38bdf8;
            color: #f8fafc;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 0.76rem;
            pointer-events: none;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            line-height: 1.4;
        }}

        /* Live Details & Telemetry Side Panel */
        .telemetry-side {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 10px;
            min-width: 260px;
        }}
        .side-card {{
            background: #111a2b;
            border: 1px solid #1e2c40;
            border-radius: 10px;
            padding: 10px 14px;
        }}
        .side-title {{
            font-size: 0.82rem;
            font-weight: 700;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
        }}
        .stat-box {{
            background: #0d1422;
            border: 1px solid #1a2638;
            border-radius: 8px;
            padding: 8px;
            text-align: center;
        }}
        .stat-num {{
            font-size: 1.3rem;
            font-weight: 800;
            color: #f8fafc;
        }}
        .stat-lbl {{
            font-size: 0.7rem;
            color: #94a3b8;
            margin-top: 2px;
        }}

        /* Terminal Logs */
        .terminal-box {{
            background: #070b14;
            border: 1px solid #192538;
            border-radius: 8px;
            padding: 8px 12px;
            font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
            font-size: 0.73rem;
            color: #38bdf8;
            height: 180px;
            overflow-y: auto;
            line-height: 1.5;
        }}
        .terminal-log-item {{
            margin-bottom: 3px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 2px;
        }}

        /* Legend Footer */
        .legend-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            background: #0d1422;
            border: 1px solid #1a2638;
            border-radius: 8px;
            padding: 8px 12px;
            margin-top: 12px;
            font-size: 0.76rem;
            color: #cbd5e1;
        }}
        .legend-item {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .legend-dot {{
            width: 12px;
            height: 12px;
            border-radius: 3px;
            display: inline-block;
        }}
    </style>
    </head>
    <body>

    <div class="player-container">
        <!-- Top HUD Header -->
        <div class="hud-header">
            <div class="hud-title">
                <span>📍 BẢN ĐỒ TÁC CHIẾN 2D (REAL-TIME ENGINE)</span>
                {mode_badge}
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="hud-pill">Mã kịch bản: <b>{scenario_info.get('id', 'N/A')}</b></span>
                <span class="hud-pill">Seed: <b>{scenario_info.get('seed', 'N/A')}</b></span>
                <span class="hud-pill">Lưới: <b>20 × 20</b></span>
            </div>
        </div>

        <!-- Controls Bar -->
        <div class="control-row">
            <div class="btn-group">
                <button id="btnPlay" class="btn-ctl primary">▶ Phát Tự Động</button>
                <button id="btnPrev" class="btn-ctl" title="Lùi 1 bước">⏮</button>
                <button id="btnNext" class="btn-ctl" title="Tiến 1 bước">⏭</button>
                <button id="btnReset" class="btn-ctl" title="Về bước đầu">🔄 Đặt Lại</button>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 0.8rem; color: #94a3b8;">Tốc độ:</span>
                <select id="selSpeed" class="select-ctl">
                    <option value="350">0.5× (Chậm rãi)</option>
                    <option value="150" selected>1.0× (Chuẩn - Mượt)</option>
                    <option value="75">2.0× (Nhanh)</option>
                    <option value="30">4.0× (Siêu tốc)</option>
                </select>
                <label class="chk-wrap">
                    <input type="checkbox" id="chkLoop"> Tự động lặp lại
                </label>
            </div>
        </div>

        <!-- Timeline Scrubber -->
        <div class="timeline-row">
            <input type="range" id="stepRange" min="0" max="{len(frames) - 1}" value="0" class="range-slider">
            <span id="lblStep" class="step-label">Bước 0/{len(frames) - 1}</span>
        </div>

        <!-- Viewport + Sidebar Details -->
        <div class="viewport-row">
            <div class="canvas-card">
                <canvas id="simCanvas" width="518" height="518"></canvas>
                <div id="tooltip" class="canvas-tooltip"></div>
            </div>

            <div class="telemetry-side">
                <!-- Live Mission Metrics -->
                <div class="side-card">
                    <div class="side-title">
                        <span>📊 TRẠNG THÁI GIẢI CỨU</span>
                        <span id="lblStatusBadge" style="color: #38bdf8; font-weight: 700;">Đang hoạt động</span>
                    </div>
                    <div class="stat-grid">
                        <div class="stat-box">
                            <div id="valRescued" class="stat-num" style="color: #10b981;">0</div>
                            <div class="stat-lbl">ĐÃ CỨU THÀNH CÔNG</div>
                        </div>
                        <div class="stat-box">
                            <div id="valWaiting" class="stat-num" style="color: #f59e0b;">0</div>
                            <div class="stat-lbl">NẠN NHÂN ĐANG CHỜ</div>
                        </div>
                        <div class="stat-box">
                            <div id="valDead" class="stat-num" style="color: #f43f5e;">0</div>
                            <div class="stat-lbl">BỊ THIÊU RỤI</div>
                        </div>
                        <div class="stat-box">
                            <div id="valReplans" class="stat-num" style="color: #c084fc;">0</div>
                            <div class="stat-lbl">LƯỢT TÁI LẬP TUYẾN</div>
                        </div>
                    </div>
                </div>

                <!-- Synchronized Event Log -->
                <div class="side-card" style="flex: 1;">
                    <div class="side-title">
                        <span>📜 NHẬT KÝ THỜI GIAN THỰC</span>
                        <span style="font-size: 0.72rem; color: #64748b;">(Tự động cuộn)</span>
                    </div>
                    <div id="logTerminal" class="terminal-box"></div>
                </div>
            </div>
        </div>

        <!-- High-Contrast Tactical Legend -->
        <div class="legend-bar">
            <span class="legend-item"><span class="legend-dot" style="background:#14462a; border:1px solid #246b41;"></span> 🌲 Rừng an toàn</span>
            <span class="legend-item"><span class="legend-dot" style="background:#ea580c; border:1px solid #f97316;"></span> ⚠️ Cảnh báo nhiệt</span>
            <span class="legend-item"><span class="legend-dot" style="background:#ef4444; border:1px solid #f87171;"></span> 🔥 Đang bốc cháy</span>
            <span class="legend-item"><span class="legend-dot" style="background:#1e293b; border:1px solid #475569;"></span> ⬛ Tàn tro</span>
            <span class="legend-item"><span class="legend-dot" style="background:#475569; border:1px solid #64748b;"></span> 🪨 Vật cản đá</span>
            <span class="legend-item"><span class="legend-dot" style="background:#38bdf8; border:1px solid #ffffff;"></span> 🧑 Nạn nhân</span>
            <span class="legend-item"><span class="legend-dot" style="background:#facc15; border:1px solid #ffffff;"></span> 🤖 Robot cứu hộ</span>
            <span class="legend-item"><span style="border-bottom: 2px dashed #38bdf8; width: 14px; display: inline-block;"></span> Lộ trình AI</span>
        </div>
    </div>

    <script>
    (function() {{
        const frames = {frames_json};
        const scenario = {scenario_json};
        const eventLogs = {events_json};
        const totalSteps = frames.length;

        const canvas = document.getElementById("simCanvas");
        const ctx = canvas.getContext("2d");
        const tooltip = document.getElementById("tooltip");

        const btnPlay = document.getElementById("btnPlay");
        const btnPrev = document.getElementById("btnPrev");
        const btnNext = document.getElementById("btnNext");
        const btnReset = document.getElementById("btnReset");
        const selSpeed = document.getElementById("selSpeed");
        const chkLoop = document.getElementById("chkLoop");
        const stepRange = document.getElementById("stepRange");
        const lblStep = document.getElementById("lblStep");

        const valRescued = document.getElementById("valRescued");
        const valWaiting = document.getElementById("valWaiting");
        const valDead = document.getElementById("valDead");
        const valReplans = document.getElementById("valReplans");
        const logTerminal = document.getElementById("logTerminal");

        let curStep = 0;
        let isPlaying = false;
        let timer = null;
        let speedMs = parseInt(selSpeed.value, 10);

        const GRID_SIZE = 20;
        const CELL_SIZE = canvas.width / GRID_SIZE;
        const ROBOT_COLORS = ["#38bdf8", "#facc15", "#f43f5e", "#c084fc", "#34d399"];

        // Color interpolation for fire risk heatmap
        function getCellColor(risk) {{
            risk = Math.max(0, Math.min(1, risk));
            if (risk < 0.2) {{
                // Pine forest green #14462a to #1b5e38
                const r = Math.round(20 + risk * 35);
                const g = Math.round(70 + risk * 120);
                const b = Math.round(42 + risk * 70);
                return `rgb(${{r}},${{g}},${{b}})`;
            }} else if (risk < 0.5) {{
                // Amber warning #b45309
                const t = (risk - 0.2) / 0.3;
                const r = Math.round(27 + t * 153);
                const g = Math.round(94 - t * 11);
                const b = Math.round(56 - t * 47);
                return `rgb(${{r}},${{g}},${{b}})`;
            }} else if (risk < 0.8) {{
                // High risk fiery orange #ea580c
                const t = (risk - 0.5) / 0.3;
                const r = Math.round(180 + t * 54);
                const g = Math.round(83 + t * 5);
                const b = Math.round(9 + t * 3);
                return `rgb(${{r}},${{g}},${{b}})`;
            }} else {{
                // Crimson red danger front #dc2626
                const t = (risk - 0.8) / 0.2;
                const r = Math.round(234 - t * 14);
                const g = Math.round(88 - t * 50);
                const b = Math.round(12 + t * 26);
                return `rgb(${{r}},${{g}},${{b}})`;
            }}
        }}

        function drawFrame(stepIdx) {{
            if (stepIdx < 0 || stepIdx >= totalSteps) return;
            const f = frames[stepIdx];
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Draw Ground Grid & Fire Risk Heatmap
            for (let y = 0; y < GRID_SIZE; y++) {{
                for (let x = 0; x < GRID_SIZE; x++) {{
                    const risk = (f.risk_map && f.risk_map[y]) ? f.risk_map[y][x] : 0.0;
                    ctx.fillStyle = getCellColor(risk);
                    ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);

                    // Crisp cell grid lines
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.14)";
                    ctx.lineWidth = 1;
                    ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                }}
            }}

            // 2. Draw Fire Grid: Active Fire (🔥) and Burnt Ash (⬛)
            for (let y = 0; y < GRID_SIZE; y++) {{
                for (let x = 0; x < GRID_SIZE; x++) {{
                    const fireVal = (f.fire_grid && f.fire_grid[y]) ? f.fire_grid[y][x] : 0;
                    if (fireVal === 2) {{
                        // Burnt ash
                        ctx.fillStyle = "#1e293b";
                        ctx.fillRect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2);
                        ctx.strokeStyle = "#334155";
                        ctx.lineWidth = 1;
                        ctx.strokeRect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2);
                    }} else if (fireVal === 1) {{
                        // Burning flame front
                        ctx.fillStyle = "rgba(239, 68, 68, 0.45)";
                        ctx.fillRect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2);
                        ctx.font = `${{CELL_SIZE * 0.65}}px sans-serif`;
                        ctx.textAlign = "center";
                        ctx.textBaseline = "middle";
                        ctx.fillText("🔥", x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2);
                    }}
                }}
            }}

            // 3. Draw Obstacles (Stone blocks)
            if (f.obstacles) {{
                for (let i = 0; i < f.obstacles.length; i++) {{
                    const ox = f.obstacles[i][0];
                    const oy = f.obstacles[i][1];
                    ctx.fillStyle = "#475569";
                    ctx.fillRect(ox * CELL_SIZE + 2, oy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
                    ctx.strokeStyle = "#1e293b";
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(ox * CELL_SIZE + 2, oy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
                }}
            }}

            // 4. Draw Robot AI Trajectories (Dashed glowing lines)
            if (f.robots) {{
                for (let i = 0; i < f.robots.length; i++) {{
                    const r = f.robots[i];
                    const color = ROBOT_COLORS[i % ROBOT_COLORS.length];
                    if (r.path && r.path.length > 0) {{
                        ctx.beginPath();
                        ctx.setLineDash([4, 3]);
                        ctx.strokeStyle = color;
                        ctx.lineWidth = 2.5;
                        ctx.moveTo(r.x * CELL_SIZE + CELL_SIZE / 2, r.y * CELL_SIZE + CELL_SIZE / 2);
                        for (let p = 0; p < r.path.length; p++) {{
                            ctx.lineTo(r.path[p].x * CELL_SIZE + CELL_SIZE / 2, r.path[p].y * CELL_SIZE + CELL_SIZE / 2);
                        }}
                        ctx.stroke();
                        ctx.setLineDash([]);
                    }}
                }}
            }}

            // 5. Draw Victims
            if (f.victims) {{
                for (let i = 0; i < f.victims.length; i++) {{
                    const v = f.victims[i];
                    const cx = v.x * CELL_SIZE + CELL_SIZE / 2;
                    const cy = v.y * CELL_SIZE + CELL_SIZE / 2;
                    const radius = CELL_SIZE * 0.42;

                    // Priority border color
                    const pColor = v.priority === 3 ? "#ef4444" : (v.priority === 2 ? "#f59e0b" : "#38bdf8");

                    ctx.beginPath();
                    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                    ctx.fillStyle = "#ffffff";
                    ctx.fill();
                    ctx.strokeStyle = pColor;
                    ctx.lineWidth = 2.8;
                    ctx.stroke();

                    // Icon based on status
                    let icon = "🧑";
                    if (v.status === "rescued") icon = "✅";
                    else if (v.status === "trapped") icon = "⚠️";
                    else if (v.status === "dead") icon = "💀";

                    ctx.font = `${{CELL_SIZE * 0.5}}px sans-serif`;
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(icon, cx, cy);
                }}
            }}

            // 6. Draw Robots
            if (f.robots) {{
                for (let i = 0; i < f.robots.length; i++) {{
                    const r = f.robots[i];
                    const cx = r.x * CELL_SIZE + CELL_SIZE / 2;
                    const cy = r.y * CELL_SIZE + CELL_SIZE / 2;
                    const radius = CELL_SIZE * 0.46;
                    const color = ROBOT_COLORS[i % ROBOT_COLORS.length];

                    // Outer halo
                    ctx.beginPath();
                    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
                    ctx.fillStyle = color;
                    ctx.fill();
                    ctx.strokeStyle = "#ffffff";
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    ctx.font = `${{CELL_SIZE * 0.55}}px sans-serif`;
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText("🤖", cx, cy);
                }}
            }}
        }}

        function updateUI(stepIdx) {{
            const f = frames[stepIdx];
            stepRange.value = stepIdx;
            lblStep.textContent = `Bước ${{stepIdx}}/${{totalSteps - 1}}`;

            // Update Telemetry
            if (f.victims) {{
                const rescued = f.victims.filter(v => v.status === "rescued").length;
                const waiting = f.victims.filter(v => v.status === "waiting" || v.status === "trapped").length;
                const dead = f.victims.filter(v => v.status === "dead").length;
                valRescued.textContent = rescued;
                valWaiting.textContent = waiting;
                valDead.textContent = dead;
            }}

            if (f.robots) {{
                const totalReplans = f.robots.reduce((acc, r) => acc + (r.replanning_count || 0), 0);
                valReplans.textContent = totalReplans;
            }}

            // Update status badge
            const lblBadge = document.getElementById("lblStatusBadge");
            if (lblBadge) {{
                if (stepIdx >= totalSteps - 1) {{
                    lblBadge.textContent = "🏁 Hoàn thành tác chiến";
                    lblBadge.style.color = "#10b981";
                    btnPlay.textContent = "🔄 Phát Lại Từ Đầu";
                }} else if (!isPlaying) {{
                    lblBadge.textContent = "Tạm dừng";
                    lblBadge.style.color = "#94a3b8";
                    btnPlay.textContent = "▶ Phát Tự Động";
                }} else {{
                    lblBadge.textContent = "Đang hoạt động";
                    lblBadge.style.color = "#38bdf8";
                }}
            }}

            // Update Terminal Log (Chronological up to current step)
            const subLogs = eventLogs.filter(e => {{
                const match = e.match(/\\[Step (\\d+)\\]/);
                return match ? parseInt(match[1], 10) <= stepIdx : true;
            }});
            const recent = subLogs.slice(-12).reverse();
            logTerminal.innerHTML = recent.map(l => `<div class="terminal-log-item">${{l}}</div>`).join("");
        }}

        function setStep(idx) {{
            curStep = Math.max(0, Math.min(totalSteps - 1, idx));
            drawFrame(curStep);
            updateUI(curStep);
        }}

        function play() {{
            if (isPlaying) return;
            isPlaying = true;
            btnPlay.textContent = "⏸ Tạm Dừng";
            btnPlay.classList.add("active-pause");
            const lblBadge = document.getElementById("lblStatusBadge");
            if (lblBadge && curStep < totalSteps - 1) {{
                lblBadge.textContent = "Đang hoạt động";
                lblBadge.style.color = "#38bdf8";
            }}

            timer = setInterval(() => {{
                if (curStep < totalSteps - 1) {{
                    setStep(curStep + 1);
                }} else {{
                    if (chkLoop.checked) {{
                        setStep(0);
                    }} else {{
                        pause();
                        if (lblBadge) {{
                            lblBadge.textContent = "🏁 Hoàn thành tác chiến";
                            lblBadge.style.color = "#10b981";
                        }}
                        btnPlay.textContent = "🔄 Phát Lại Từ Đầu";
                    }}
                }}
            }}, speedMs);
        }}

        function pause() {{
            isPlaying = false;
            btnPlay.textContent = "▶ Phát Tự Động";
            btnPlay.classList.remove("active-pause");
            if (timer) {{
                clearInterval(timer);
                timer = null;
            }}
        }}

        btnPlay.addEventListener("click", () => {{
            if (isPlaying) pause();
            else {{
                if (curStep >= totalSteps - 1) setStep(0);
                play();
            }}
        }});

        btnPrev.addEventListener("click", () => {{
            pause();
            setStep(curStep - 1);
        }});

        btnNext.addEventListener("click", () => {{
            pause();
            setStep(curStep + 1);
        }});

        btnReset.addEventListener("click", () => {{
            pause();
            setStep(0);
        }});

        selSpeed.addEventListener("change", (e) => {{
            speedMs = parseInt(e.target.value, 10);
            if (isPlaying) {{
                pause();
                play();
            }}
        }});

        stepRange.addEventListener("input", (e) => {{
            pause();
            setStep(parseInt(e.target.value, 10));
        }});

        // Tooltip on hover
        canvas.addEventListener("mousemove", (e) => {{
            const rect = canvas.getBoundingClientRect();
            const mx = e.clientX - rect.left;
            const my = e.clientY - rect.top;
            const gx = Math.floor(mx / CELL_SIZE);
            const gy = Math.floor(my / CELL_SIZE);

            if (gx >= 0 && gx < GRID_SIZE && gy >= 0 && gy < GRID_SIZE) {{
                const f = frames[curStep];
                const risk = (f.risk_map && f.risk_map[gy]) ? f.risk_map[gy][gx].toFixed(3) : "0.000";
                const fire = (f.fire_grid && f.fire_grid[gy]) ? f.fire_grid[gy][gx] : 0;

                let desc = `Tọa độ: (${{gx}}, ${{gy}})<br>Rủi ro lửa lan: ${{risk}}`;
                if (fire === 1) desc += `<br><b style="color:#ef4444;">🔥 Đang cháy dữ dội!</b>`;
                else if (fire === 2) desc += `<br><b style="color:#94a3b8;">⬛ Khu vực tàn tro</b>`;

                // Check victims
                const v = f.victims ? f.victims.find(item => item.x === gx && item.y === gy) : null;
                if (v) {{
                    desc += `<br><b style="color:#38bdf8;">🧑 Nạn nhân #${{v.id}} (Ưu tiên ${{v.priority}})</b> - ${{v.status}}`;
                }}
                // Check robots
                const r = f.robots ? f.robots.find(item => item.x === gx && item.y === gy) : null;
                if (r) {{
                    desc += `<br><b style="color:#facc15;">🤖 Robot #${{r.id}} (${{r.status}})</b>`;
                }}

                tooltip.innerHTML = desc;
                tooltip.style.left = (mx + 12) + "px";
                tooltip.style.top = (my + 12) + "px";
                tooltip.style.display = "block";
            }} else {{
                tooltip.style.display = "none";
            }}
        }});

        canvas.addEventListener("mouseleave", () => {{
            tooltip.style.display = "none";
        }});

        // Initial render
        setStep(0);
    }})();
    </script>
    </body>
    </html>
    """
    return html


def render_dual_canvas_player_html(
    frames_p: List[Dict[str, Any]],
    frames_b: List[Dict[str, Any]],
    scenario_info: Dict[str, Any],
    events_p: List[str],
    events_b: List[str],
) -> str:
    """
    Renders dual head-to-head comparison (Proposed vs Baseline) in a synchronized HTML5 Canvas player.
    """
    frames_p_json = json.dumps(frames_p)
    frames_b_json = json.dumps(frames_b)
    scenario_json = json.dumps(scenario_info)
    events_p_json = json.dumps(events_p)
    events_b_json = json.dumps(events_b)
    max_steps = max(len(frames_p), len(frames_b))

    html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
    <meta charset="UTF-8">
    <style>
        * {{
            box-sizing: border-box;
            user-select: none;
        }}
        body {{
            margin: 0;
            padding: 4px;
            background: #090d16;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            overflow-x: hidden;
        }}
        .player-container {{
            background: #0f172a;
            border: 1.5px solid #253852;
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        }}
        .hud-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #131d31;
            border: 1px solid #223249;
            padding: 10px 16px;
            border-radius: 10px;
            margin-bottom: 12px;
        }}
        .hud-title {{
            font-size: 0.98rem;
            font-weight: 700;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .control-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
            background: #111a2c;
            border: 1px solid #1e2d42;
            padding: 10px 14px;
            border-radius: 10px;
            margin-bottom: 12px;
        }}
        .btn-group {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .btn-ctl {{
            background: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .btn-ctl:hover {{
            background: #334155;
        }}
        .btn-ctl.primary {{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border-color: #3b82f6;
            color: #ffffff;
        }}
        .btn-ctl.active-pause {{
            background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
            border-color: #f59e0b;
        }}
        .select-ctl {{
            background: #1e293b;
            color: #f8fafc;
            border: 1px solid #334155;
            padding: 6px 10px;
            border-radius: 8px;
            font-size: 0.8rem;
            outline: none;
        }}
        .timeline-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 14px;
        }}
        .range-slider {{
            flex: 1;
            height: 6px;
            -webkit-appearance: none;
            background: #1e293b;
            border-radius: 4px;
            outline: none;
            cursor: pointer;
        }}
        .range-slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #38bdf8;
            border: 2px solid #ffffff;
            cursor: pointer;
        }}
        .step-label {{
            min-width: 90px;
            font-size: 0.85rem;
            font-weight: 700;
            color: #38bdf8;
            text-align: right;
            font-family: monospace;
        }}
        .dual-view {{
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .dual-panel {{
            flex: 1;
            min-width: 380px;
            max-width: 480px;
            background: #080d1a;
            border: 2px solid #1e3a5f;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
        }}
        .panel-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 0.84rem;
            font-weight: 700;
        }}
        .panel-canvas {{
            display: block;
            margin: 0 auto;
            background: #123820;
            border-radius: 6px;
        }}
        .legend-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            background: #0d1422;
            border: 1px solid #1a2638;
            border-radius: 8px;
            padding: 8px 12px;
            margin-top: 12px;
            font-size: 0.76rem;
            color: #cbd5e1;
        }}
        .legend-dot {{
            width: 12px;
            height: 12px;
            border-radius: 3px;
            display: inline-block;
        }}
    </style>
    </head>
    <body>

    <div class="player-container">
        <!-- Top HUD Header -->
        <div class="hud-header">
            <div class="hud-title">
                <span>⚔️ SO SÁNH ĐỐI ĐẦU ĐỒNG THỜI (DUAL PLAYBACK ENGINE)</span>
            </div>
            <div style="font-size:0.8rem; color:#94a3b8;">
                Đang chạy đồng bộ 2 thuật toán trên cùng 1 kịch bản
            </div>
        </div>

        <!-- Master Controls -->
        <div class="control-row">
            <div class="btn-group">
                <button id="btnPlay" class="btn-ctl primary">▶ Phát Cả 2</button>
                <button id="btnPrev" class="btn-ctl">⏮</button>
                <button id="btnNext" class="btn-ctl">⏭</button>
                <button id="btnReset" class="btn-ctl">🔄 Đặt Lại</button>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 0.8rem; color: #94a3b8;">Tốc độ:</span>
                <select id="selSpeed" class="select-ctl">
                    <option value="350">0.5×</option>
                    <option value="150" selected>1.0×</option>
                    <option value="75">2.0×</option>
                </select>
                <label style="font-size:0.8rem; color:#94a3b8; cursor:pointer;">
                    <input type="checkbox" id="chkLoop"> Tự động lặp lại
                </label>
            </div>
        </div>

        <!-- Timeline Scrubber -->
        <div class="timeline-row">
            <input type="range" id="stepRange" min="0" max="{max_steps - 1}" value="0" class="range-slider">
            <span id="lblStep" class="step-label">Bước 0/{max_steps - 1}</span>
        </div>

        <!-- Dual Canvases Side-by-Side -->
        <div class="dual-view">
            <!-- Left: Proposed -->
            <div class="dual-panel" style="border-color: #059669;">
                <div class="panel-header" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #059669;">
                    <span>✨ PROPOSED (PSO + U-Net)</span>
                    <span id="propLiveStat">Đã cứu: 0</span>
                </div>
                <canvas id="canvasP" class="panel-canvas" width="420" height="420"></canvas>
            </div>

            <!-- Right: Baseline -->
            <div class="dual-panel" style="border-color: #dc2626;">
                <div class="panel-header" style="background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #dc2626;">
                    <span>⚙️ BASELINE (Greedy + A*)</span>
                    <span id="baseLiveStat">Đã cứu: 0</span>
                </div>
                <canvas id="canvasB" class="panel-canvas" width="420" height="420"></canvas>
            </div>
        </div>

        <!-- Legend -->
        <div class="legend-bar">
            <span><span class="legend-dot" style="background:#14462a;"></span> 🌲 Rừng an toàn</span>
            <span><span class="legend-dot" style="background:#ea580c;"></span> ⚠️ Cảnh báo nhiệt</span>
            <span><span class="legend-dot" style="background:#ef4444;"></span> 🔥 Lửa cháy</span>
            <span><span class="legend-dot" style="background:#1e293b;"></span> ⬛ Tàn tro</span>
            <span><span class="legend-dot" style="background:#475569;"></span> 🪨 Vật cản</span>
            <span><span class="legend-dot" style="background:#38bdf8;"></span> 🧑 Nạn nhân</span>
            <span><span class="legend-dot" style="background:#facc15;"></span> 🤖 Robot</span>
        </div>
    </div>

    <script>
    (function() {{
        const framesP = {frames_p_json};
        const framesB = {frames_b_json};
        const totalSteps = {max_steps};

        const canvasP = document.getElementById("canvasP");
        const ctxP = canvasP.getContext("2d");
        const canvasB = document.getElementById("canvasB");
        const ctxB = canvasB.getContext("2d");

        const btnPlay = document.getElementById("btnPlay");
        const btnPrev = document.getElementById("btnPrev");
        const btnNext = document.getElementById("btnNext");
        const btnReset = document.getElementById("btnReset");
        const selSpeed = document.getElementById("selSpeed");
        const chkLoop = document.getElementById("chkLoop");
        const stepRange = document.getElementById("stepRange");
        const lblStep = document.getElementById("lblStep");
        const propLiveStat = document.getElementById("propLiveStat");
        const baseLiveStat = document.getElementById("baseLiveStat");

        let curStep = 0;
        let isPlaying = false;
        let timer = null;
        let speedMs = parseInt(selSpeed.value, 10);

        const GRID_SIZE = 20;
        const CELL_SIZE = canvasP.width / GRID_SIZE;
        const ROBOT_COLORS = ["#38bdf8", "#facc15", "#f43f5e", "#c084fc", "#34d399"];

        function getCellColor(risk) {{
            risk = Math.max(0, Math.min(1, risk));
            if (risk < 0.2) return "#14462a";
            if (risk < 0.5) return "#b45309";
            if (risk < 0.8) return "#ea580c";
            return "#dc2626";
        }}

        function renderEngine(ctx, c, f) {{
            if (!f) return;
            ctx.clearRect(0, 0, c.width, c.height);

            // Ground & Risk
            for (let y = 0; y < GRID_SIZE; y++) {{
                for (let x = 0; x < GRID_SIZE; x++) {{
                    const risk = (f.risk_map && f.risk_map[y]) ? f.risk_map[y][x] : 0.0;
                    ctx.fillStyle = getCellColor(risk);
                    ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.12)";
                    ctx.lineWidth = 1;
                    ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                }}
            }}

            // Fires
            for (let y = 0; y < GRID_SIZE; y++) {{
                for (let x = 0; x < GRID_SIZE; x++) {{
                    const fVal = (f.fire_grid && f.fire_grid[y]) ? f.fire_grid[y][x] : 0;
                    if (fVal === 2) {{
                        ctx.fillStyle = "#1e293b";
                        ctx.fillRect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2);
                    }} else if (fVal === 1) {{
                        ctx.fillStyle = "rgba(239, 68, 68, 0.4)";
                        ctx.fillRect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2);
                        ctx.font = `${{CELL_SIZE * 0.65}}px sans-serif`;
                        ctx.textAlign = "center";
                        ctx.textBaseline = "middle";
                        ctx.fillText("🔥", x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2);
                    }}
                }}
            }}

            // Obstacles
            if (f.obstacles) {{
                for (let i = 0; i < f.obstacles.length; i++) {{
                    const ox = f.obstacles[i][0];
                    const oy = f.obstacles[i][1];
                    ctx.fillStyle = "#475569";
                    ctx.fillRect(ox * CELL_SIZE + 2, oy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4);
                }}
            }}

            // Paths
            if (f.robots) {{
                for (let i = 0; i < f.robots.length; i++) {{
                    const r = f.robots[i];
                    const color = ROBOT_COLORS[i % ROBOT_COLORS.length];
                    if (r.path && r.path.length > 0) {{
                        ctx.beginPath();
                        ctx.setLineDash([3, 3]);
                        ctx.strokeStyle = color;
                        ctx.lineWidth = 2;
                        ctx.moveTo(r.x * CELL_SIZE + CELL_SIZE / 2, r.y * CELL_SIZE + CELL_SIZE / 2);
                        for (let p = 0; p < r.path.length; p++) {{
                            ctx.lineTo(r.path[p].x * CELL_SIZE + CELL_SIZE / 2, r.path[p].y * CELL_SIZE + CELL_SIZE / 2);
                        }}
                        ctx.stroke();
                        ctx.setLineDash([]);
                    }}
                }}
            }}

            // Victims
            if (f.victims) {{
                for (let i = 0; i < f.victims.length; i++) {{
                    const v = f.victims[i];
                    const cx = v.x * CELL_SIZE + CELL_SIZE / 2;
                    const cy = v.y * CELL_SIZE + CELL_SIZE / 2;
                    ctx.beginPath();
                    ctx.arc(cx, cy, CELL_SIZE * 0.4, 0, Math.PI * 2);
                    ctx.fillStyle = "#ffffff";
                    ctx.fill();
                    ctx.strokeStyle = v.priority === 3 ? "#ef4444" : "#f59e0b";
                    ctx.lineWidth = 2.5;
                    ctx.stroke();

                    let icon = "🧑";
                    if (v.status === "rescued") icon = "✅";
                    else if (v.status === "dead") icon = "💀";
                    ctx.font = `${{CELL_SIZE * 0.5}}px sans-serif`;
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(icon, cx, cy);
                }}
            }}

            // Robots
            if (f.robots) {{
                for (let i = 0; i < f.robots.length; i++) {{
                    const r = f.robots[i];
                    const cx = r.x * CELL_SIZE + CELL_SIZE / 2;
                    const cy = r.y * CELL_SIZE + CELL_SIZE / 2;
                    ctx.beginPath();
                    ctx.arc(cx, cy, CELL_SIZE * 0.44, 0, Math.PI * 2);
                    ctx.fillStyle = ROBOT_COLORS[i % ROBOT_COLORS.length];
                    ctx.fill();
                    ctx.strokeStyle = "#ffffff";
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    ctx.font = `${{CELL_SIZE * 0.55}}px sans-serif`;
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText("🤖", cx, cy);
                }}
            }}
        }}

        function drawBoth(stepIdx) {{
            const fP = framesP[Math.min(stepIdx, framesP.length - 1)];
            const fB = framesB[Math.min(stepIdx, framesB.length - 1)];
            renderEngine(ctxP, canvasP, fP);
            renderEngine(ctxB, canvasB, fB);

            stepRange.value = stepIdx;
            lblStep.textContent = `Bước ${{stepIdx}}/${{totalSteps - 1}}`;

            if (fP && fP.victims) {{
                const rP = fP.victims.filter(v => v.status === "rescued").length;
                propLiveStat.textContent = `Đã cứu: ${{rP}}/${{fP.victims.length}}`;
            }}
            if (fB && fB.victims) {{
                const rB = fB.victims.filter(v => v.status === "rescued").length;
                baseLiveStat.textContent = `Đã cứu: ${{rB}}/${{fB.victims.length}}`;
            }}
        }}

        function setStep(idx) {{
            curStep = Math.max(0, Math.min(totalSteps - 1, idx));
            drawBoth(curStep);
        }}

        function play() {{
            if (isPlaying) return;
            isPlaying = true;
            btnPlay.textContent = "⏸ Tạm Dừng";
            btnPlay.classList.add("active-pause");
            timer = setInterval(() => {{
                if (curStep < totalSteps - 1) {{
                    setStep(curStep + 1);
                }} else {{
                    if (chkLoop.checked) {{
                        setStep(0);
                    }} else {{
                        pause();
                        btnPlay.textContent = "🔄 Phát Lại Cả 2";
                    }}
                }}
            }}, speedMs);
        }}

        function pause() {{
            isPlaying = false;
            btnPlay.textContent = "▶ Phát Cả 2";
            btnPlay.classList.remove("active-pause");
            if (timer) {{
                clearInterval(timer);
                timer = null;
            }}
        }}

        btnPlay.addEventListener("click", () => {{
            if (isPlaying) pause();
            else {{
                if (curStep >= totalSteps - 1) setStep(0);
                play();
            }}
        }});
        btnPrev.addEventListener("click", () => {{ pause(); setStep(curStep - 1); }});
        btnNext.addEventListener("click", () => {{ pause(); setStep(curStep + 1); }});
        btnReset.addEventListener("click", () => {{ pause(); setStep(0); }});
        selSpeed.addEventListener("change", (e) => {{
            speedMs = parseInt(e.target.value, 10);
            if (isPlaying) {{ pause(); play(); }}
        }});
        stepRange.addEventListener("input", (e) => {{
            pause();
            setStep(parseInt(e.target.value, 10));
        }});

        setStep(0);
    }})();
    </script>
    </body>
    </html>
    """
    return html

