import os
import json
import zipfile

def generate_html():
    try:
        from ase_a6_questions import questions
    except ImportError:
        print("❌ ERROR: ase_a6_questions.py not found on the shop floor!")
        return

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShatterScan Core: Production Diagnostic Terminal</title>
    <style>
        :root {{
            --bg-dark: #0a0a0d;
            --card-bg: rgba(22, 22, 26, 0.85);
            --panel-dark: #050507;
            --blue-prime: #007acc;
            --blue-glow: #00a2ff;
            --text-main: #e2e8f0;
            --text-muted: #64748b;
            --correct-green: #38a169;
            --incorrect-red: #e53e3e;
            --amber-warn: #dd6b20;
            --border-glow: rgba(0, 162, 255, 0.15);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at center, #111b2d 0%, #06080d 100%),
                radial-gradient(rgba(255, 255, 255, 0.15) 1px, transparent 1px);
            background-size: 100% 100%, 20px 20px;
            background-attachment: fixed;
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 10px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }}
        .mainframe {{
            width: 100%;
            max-width: 650px;
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 12px;
            border: 1px solid rgba(0, 162, 255, 0.25);
            box-shadow: 0 20px 50px rgba(0,0,0,0.8), 0 0 30px rgba(0, 162, 255, 0.05);
            overflow: hidden;
            margin-top: 10px;
        }}
        .header-bar {{
            background: var(--panel-dark);
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }}
        .header-title {{ font-size: 18px; font-weight: bold; color: var(--blue-glow); letter-spacing: 0.75px; font-family: monospace; text-shadow: 0 0 10px rgba(0,162,255,0.4); }}
        .status-pill {{ background: #1c2d24; color: #68d391; font-size: 11px; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #22543d; }}
        
        .tab-nav {{ display: flex; background: #0c0d10; border-bottom: 1px solid rgba(255,255,255,0.08); overflow-x: auto; }}
        .tab-nav.hidden {{ display: none !important; }}
        .tab-btn {{ flex: 1; background: none; border: none; color: var(--text-muted); padding: 14px 10px; font-size: 12px; font-weight: bold; cursor: pointer; text-align: center; white-space: nowrap; transition: all 0.2s ease; }}
        .tab-btn:hover {{ color: var(--text-main); background: rgba(255,255,255,0.02); }}
        .tab-btn.active {{ color: var(--blue-glow); background: rgba(22, 22, 26, 0.5); border-bottom: 2px solid var(--blue-glow); text-shadow: 0 0 8px rgba(0,162,255,0.3); }}
        
        .workspace {{ padding: 20px; min-height: 450px; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        /* Interactive Gauge Display Panels */
        .gauge-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; text-align: center; }}
        .gauge-card {{ background: rgba(5, 5, 7, 0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); border-top: 2px solid var(--blue-prime); display: flex; flex-direction: column; align-items: center; }}
        .gauge-canvas {{ background: transparent; width: 140px; height: 140px; }}
        .gauge-lbl {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.75px; margin-top: 8px; font-weight: bold; }}
        
        .telemetry-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 15px; }}
        .telemetry-tile {{ background: rgba(5, 5, 7, 0.4); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.04); }}
        .tile-lbl {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.5px; }}
        .tile-val {{ font-size: 16px; font-weight: bold; color: var(--text-main); font-family: monospace; }}
        
        .dtc-box {{ background: rgba(42, 27, 27, 0.5); border: 1px solid #742a2a; border-radius: 6px; padding: 12px; margin-top: 15px; }}
        .dtc-title {{ font-size: 13px; font-weight: bold; color: #feb2b2; margin-bottom: 6px; }}
        .dtc-item {{ font-family: monospace; font-size: 13px; color: #fc8181; padding: 4px 0; }}
        
        .search-box {{ display: flex; gap: 10px; margin-bottom: 15px; }}
        .search-input {{ flex: 1; background: var(--panel-dark); border: 1px solid rgba(0, 162, 255, 0.2); padding: 12px; color: #fff; border-radius: 6px; font-size: 15px; font-family: monospace; }}
        .search-input:focus {{ outline: none; border-color: var(--blue-glow); box-shadow: 0 0 8px rgba(0,162,255,0.2); }}
        
        .progress-wrapper {{ margin-bottom: 20px; }}
        .progress-text {{ font-size: 12px; color: var(--text-muted); display: flex; justify-content: space-between; margin-bottom: 5px; }}
        .progress-bar {{ width: 100%; height: 6px; background: #222; border-radius: 3px; overflow: hidden; }}
        .progress-fill {{ height: 100%; width: 0%; background: var(--blue-glow); transition: width 0.3s ease; }}
        .category-badge {{ display: inline-block; background: #1e293b; color: var(--blue-glow); font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 4px; margin-bottom: 10px; text-transform: uppercase; border: 1px solid rgba(0,162,255,0.2); }}
        .q-card {{ font-size: 16px; line-height: 1.5; margin-bottom: 20px; min-height: 70px; }}
        .options-grid {{ display: flex; flex-direction: column; gap: 10px; }}
        .opt-btn {{ width: 100%; background: #1e222b; color: var(--text-main); border: 1px solid rgba(255,255,255,0.08); padding: 14px; border-radius: 6px; font-size: 15px; text-align: left; cursor: pointer; }}
        .opt-btn:hover {{ background: #242936; border-color: var(--blue-glow); }}
        
        .modal {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center; padding: 20px; z-index: 1000; }}
        .modal-content {{ background: #16161a; width: 100%; max-width: 400px; padding: 24px; border-radius: 12px; text-align: left; border: 1px solid rgba(0, 162, 255, 0.3); box-shadow: 0 0 30px rgba(0,162,255,0.15); }}
        .status-title {{ font-size: 22px; font-weight: bold; margin-bottom: 12px; }}
        .status-correct {{ color: var(--correct-green); }}
        .status-incorrect {{ color: var(--incorrect-red); }}
        .explanation {{ font-size: 15px; line-height: 1.5; color: #cbd5e0; margin-bottom: 20px; }}
        
        .btn {{ width: 100%; background: linear-gradient(180deg, var(--blue-glow) 0%, var(--blue-prime) 100%); color: #fff; border: none; padding: 14px; border-radius: 6px; font-size: 15px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(0,122,204,0.3); }}
        .btn:hover {{ filter: brightness(1.1); box-shadow: 0 4px 16px rgba(0,162,255,0.4); }}
        .hidden {{ display: none !important; }}
        
        .list-container {{ display: flex; flex-direction: column; gap: 12px; }}
        .list-item {{ background: rgba(5, 5, 7, 0.4); border: 1px solid rgba(255,255,255,0.05); border-left: 3px solid var(--blue-prime); padding: 15px; border-radius: 6px; }}
        .list-header {{ font-weight: bold; font-family: monospace; color: var(--blue-glow); margin-bottom: 6px; font-size: 15px; }}
        .step-block {{ margin-left: 10px; margin-top: 8px; font-size: 13px; border-left: 2px solid rgba(255,255,255,0.06); padding-left: 10px; color: #cbd5e0; }}
        .step-num {{ color: var(--blue-glow); font-weight: bold; font-family: monospace; }}
        .translation-text {{ color: #94a3b8; font-style: italic; font-size: 13px; display: block; margin-top: 2px; }}

        .bench-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }}
        .bench-input {{ width: 100%; background: var(--panel-dark); border: 1px solid rgba(255,255,255,0.1); padding: 10px; color: #fff; border-radius: 4px; font-family: monospace; font-size: 14px; margin-top: 4px; }}
        .bench-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; text-align: left; }}
        .bench-table th {{ color: var(--blue-glow); border-bottom: 1px solid rgba(255,255,255,0.1); padding: 8px 4px; }}
        .bench-table td {{ padding: 8px 4px; border-bottom: 1px solid rgba(255,255,255,0.04); }}
        
        .legal-notice {{ background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.08); padding: 15px; border-radius: 6px; font-size: 13px; color: #94a3b8; line-height: 1.5; margin-bottom: 20px; max-height: 160px; overflow-y: auto; text-align: left; }}
    </style>
</head>
<body>
    <div class="mainframe">
        <div class="header-bar">
            <div class="header-title">⚡️ SHATTERSCAN // CORE</div>
            <div id="mainframe-status" class="status-pill" style="background:#4a2b12; color:var(--amber-warn); border-color:#7b341e;">STANDBY / LOCKED</div>
        </div>
        
        <div id="main-nav" class="tab-nav hidden">
            <button class="tab-btn active" onclick="switchTab(event, 'scanner-tab')">📟 SCANNER</button>
            <button class="tab-btn" onclick="switchTab(event, 'codes-tab')">🔌 OBD CODES</button>
            <button class="tab-btn" onclick="switchTab(event, 'manual-tab')">📚 REPAIR MANUAL</button>
            <button class="tab-btn" onclick="switchTab(event, 'bench-tab')">🧰 TOOL BENCH</button>
            <button class="tab-btn" onclick="switchTab(event, 'rig-tab')">🧠 ASE TEST RIG</button>
        </div>
        
        <div class="workspace">
            <div id="splash-screen" style="text-align: center;">
                <h2 style="color:var(--blue-glow); margin-bottom: 10px; font-family: monospace;">INITIALIZE CORE</h2>
                <p style="font-size:14px; color:var(--text-main); margin-bottom: 20px;">ShatterScan Diagnostic Platform Suite v1.0.0<br><span style="color:var(--text-muted)">Logic Bound Studios Premium Release</span></p>
                
                <div class="legal-notice">
                    <strong>⚠️ LIABILITY WARRANTY DISCLAIMER & TERMS OF SERVICE:</strong><br>
                    This software application is delivered strictly as an educational reference database for automotive diagnostic theory. All repair procedures, code definitions, and electrical calculators contained herein are built from generic operational principles and should never supersede specific OEM manufacturer service manuals or factory wiring schematics.<br><br>
                    Automotive electrical troubleshooting carries inherent risks of high-current short circuits, battery gas explosions, component thermal failures, and sensitive solid-state control module destruction. By initializing this terminal, the user explicitly assumes all operational risks. Logic Bound Studios assumes absolutely zero civil liability for any property damage, mechanical component failure, burned wiring harnesses, fried engine control units (ECUs), or personal injury resulting from the application or misinterpretation of data provided within this application interface. Always clear the bay, isolate open feeds, and wear eye protection.
                </div>
                
                <button class="btn" onclick="acceptTerms()">I ACCEPT TERMS & ENGAGE SYSTEM</button>
            </div>

            <div id="scanner-tab" class="tab-content">
                <div style="margin-bottom:15px;">
                    <button id="bt-connect-btn" class="btn" onclick="connectBluetooth()" style="padding: 10px; font-size:13px; font-family:monospace;">🔌 CONNECT BLUETOOTH OBD-II ADAPTER</button>
                </div>

                <div class="gauge-row">
                    <div class="gauge-card">
                        <canvas id="gauge-volt" class="gauge-canvas" width="280" height="280"></canvas>
                        <div class="gauge-lbl">System Voltage</div>
                    </div>
                    <div class="gauge-card">
                        <canvas id="gauge-rpm" class="gauge-canvas" width="280" height="280"></canvas>
                        <div class="gauge-lbl">Engine Telemetry (RPM)</div>
                    </div>
                </div>

                <div class="telemetry-row">
                    <div class="telemetry-tile"><div class="tile-lbl">Datalink Interface</div><div class="tile-val" id="tele-link" style="color:var(--text-muted);">NOT CONNECTED</div></div>
                    <div class="telemetry-tile"><div class="tile-lbl">Throttle Position</div><div class="tile-val">14.2 %</div></div>
                </div>
                <div class="telemetry-row">
                    <div class="telemetry-tile"><div class="tile-lbl">Coolant Temp (ECT)</div><div class="tile-val">196 °F</div></div>
                    <div class="telemetry-tile"><div class="tile-lbl">Calculated Engine Load</div><div class="tile-val">22.5 %</div></div>
                </div>
                
                <div class="dtc-box">
                    <div class="dtc-title">⚠️ ACTIVE DIAGNOSTIC TROUBLE CODES (DTC)</div>
                    <div class="dtc-item">» P0171 - System Too Lean (Bank 1)</div>
                    <div class="dtc-item">» P0300 - Random/Multiple Cylinder Misfire Detected</div>
                </div>
            </div>
            
            <div id="codes-tab" class="tab-content">
                <div class="search-box">
                    <input type="text" id="code-search" class="search-input" placeholder="Search Fault Codes (e.g., P0171, P0302, U0100)..." onkeyup="searchCodes()">
                </div>
                <div id="code-results" class="list-container"></div>
            </div>
            
            <div id="manual-tab" class="tab-content">
                <div class="list-container">
                    <div class="list-item">
                        <div class="list-header">🔧 CIRCUIT VOLTAGE DROP METHODOLOGY (LOADED)</div>
                        <span class="translation-text">(How to find a hidden loose, rusty, or broken wire without pulling the whole car apart)</span>
                        <div class="step-block">
                            <p><span class="step-num">01.</span> Set your Digital Multimeter to DC Volts (V). Keep the circuit completely connected and plugged in.</p>
                            <p><span class="step-num">02.</span> Turn the vehicle key on and activate the component or load.</p>
                            <p><span class="step-num">03.</span> Connect the RED meter lead to the power-delivery side of the wire connector plug.</p>
                            <p><span class="step-num">04.</span> Connect the BLACK meter lead to the opposite wire side of that same connector block.</p>
                            <p><span class="step-num">05.</span> Read the meter display. A perfect, clean wire joint will show less than 0.1V. If it reads above 0.2V, there is hidden corrosion or loose pins inside that connector block eating up your electricity.</p>
                        </div>
                    </div>
                </div>
            </div>

            <div id="bench-tab" class="tab-content">
                <div class="list-container">
                    <div class="list-item">
                        <div class="list-header">📊 INTERACTIVE OHM'S LAW CALCULATOR</div>
                        <span class="translation-text">(Type in your voltage and resistance values to see exactly how many amps should flow)</span>
                        <div class="bench-grid">
                            <div><label style="font-size:12px; color:var(--text-muted);">Voltage (Volts)</label><input type="number" id="calc-volt" class="bench-input" value="12.6" oninput="runOhmCalc()"></div>
                            <div><label style="font-size:12px; color:var(--text-muted);">Resistance (Ohms)</label><input type="number" id="calc-ohm" class="bench-input" value="2.0" oninput="runOhmCalc()"></div>
                        </div>
                        <div id="calc-result" style="margin-top:12px; font-weight:bold; font-family:monospace; color:var(--correct-green); font-size:15px;">Target Current Flow: 6.30 Amps</div>
                    </div>
                </div>
            </div>
            
            <div id="rig-tab" class="tab-content">
                <div id="rig-splash-screen">
                    <h3 style="color:var(--blue-glow); margin-bottom:10px;">Interactive Logic Rig</h3>
                    <p style="font-size:14px; color:var(--text-muted); margin-bottom:15px; line-height:1.4;">Evaluate your field logic. This interactive simulator checks subsystem problem-solving speeds and logs missed workflows onto your final order sheet.</p>
                    <button class="btn" onclick="startRig()">INITIALIZE DIAGNOSTIC RUN</button>
                </div>
                
                <div id="game-screen" class="hidden">
                    <div class="progress-wrapper">
                        <div class="progress-text"><span id="tracker-count">Question 1</span><span id="tracker-pct">0%</span></div>
                        <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>
                    </div>
                    <div id="category-box" class="category-badge">⚡️ General Electrical</div>
                    <div class="q-card" id="question-text">Loading question text...</div>
                    <div class="options-grid" id="options-container"></div>
                </div>
            </div>
        </div>
    </div>

    <div id="diagnostic-modal" class="modal hidden">
        <div class="modal-content">
            <div id="modal-status" class="status-title"></div>
            <div id="modal-explanation" class="explanation"></div>
            <button class="btn" onclick="closeDiagnosticModal()">CLEAR ERROR CODE</button>
        </div>
    </div>

    <script>
        let animationActive = false;
        let voltValue = 0.0;
        let rpmValue = 0;

        function acceptTerms() {{
            document.getElementById('splash-screen').classList.add('hidden');
            document.getElementById('main-nav').classList.remove('hidden');
            document.getElementById('scanner-tab').classList.add('active');
            
            const status = document.getElementById('mainframe-status');
            status.innerText = "SYSTEM ONLINE // NOMINAL";
            status.style.background = "#1c2d24";
            status.style.color = "#68d391";
            status.style.borderColor = "#22543d";
            
            // Trigger Gauge Render Engines immediately on paint
            drawGauge("gauge-volt", 0, 16, "V", "VOLTS");
            drawGauge("gauge-rpm", 0, 8000, "rpm", "RPM");
        }}

        function switchTab(evt, tabId) {{
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            evt.currentTarget.classList.add('active');
        }}

        // Dynamic Canvas Instrument Gauge Pipeline (Torque Pro Architecture Match)
        function drawGauge(canvasId, val, maxVal, unitStr, lblStr) {{
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, 280, 280);

            // Dial Center Positioning Configuration
            const cx = 140; const cy = 140; const r = 110;
            const startAngle = 0.75 * Math.PI;
            const endAngle = 2.25 * Math.PI;
            const currentAngle = startAngle + (val / maxVal) * (endAngle - startAngle);

            // 1. Draw Background Dial Track Block
            ctx.beginPath();
            ctx.arc(cx, cy, r, startAngle, endAngle);
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 14;
            ctx.lineCap = 'round';
            ctx.stroke();

            // 2. Draw Active Sweeping Glowing Color Band
            ctx.beginPath();
            ctx.arc(cx, cy, r, startAngle, currentAngle);
            ctx.strokeStyle = (canvasId === 'gauge-volt' && val < 12.0) ? '#e53e3e' : '#00a2ff';
            ctx.lineWidth = 14;
            ctx.lineCap = 'round';
            ctx.shadowBlur = 10;
            ctx.shadowColor = ctx.strokeStyle;
            ctx.stroke();
            ctx.shadowBlur = 0; // Reset blur channel

            // 3. Center Numeric Readout Displays
            ctx.fillStyle = '#e2e8f0';
            ctx.font = 'bold 36px monospace';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(val.toString(), cx, cy - 10);

            ctx.fillStyle = '#64748b';
            ctx.font = 'bold 16px sans-serif';
            ctx.fillText(unitStr, cx, cy + 25);
        }}

        // Native Bluetooth Driver Simulator Engine
        function connectBluetooth() {{
            const btn = document.getElementById('bt-connect-btn');
            const linkTile = document.getElementById('tele-link');
            
            btn.innerText = "⚡ INITIALIZING SECURITY DATALINK PIN PAIRING...";
            btn.style.filter = "brightness(0.7)";
            
            setTimeout(() => {{
                btn.innerText = "✅ OBD-II ADAPTER PAIRED LINK SUCCESSFUL";
                btn.style.background = "linear-gradient(180deg, #38a169 0%, #276749 100%)";
                btn.style.filter = "none";
                linkTile.innerText = "CAN-BUS (ISO 15765)";
                linkTile.style.color = "var(--correct-green)";
                
                // Initialize Live Rolling Telemetry Wave Loop
                animationActive = true;
                runLiveTelemetrySim();
            }}, 1500);
        }}

        function runLiveTelemetrySim() {{
            if (!animationActive) return;
            
            // Simulate natural mechanical engine oscillations
            voltValue = (14.15 + Math.random() * 0.18).toFixed(2);
            rpmValue = Math.floor(735 + Math.random() * 32);

            drawGauge("gauge-volt", voltValue, 16, "V", "VOLTS");
            drawGauge("gauge-rpm", rpmValue, 8000, "rpm", "RPM");

            setTimeout(runLiveTelemetrySim, 120); // 120ms update delay matches vehicle refresh sweeps
        }}

        function runOhmCalc() {{
            const v = parseFloat(document.getElementById('calc-volt').value);
            const r = parseFloat(document.getElementById('calc-ohm').value);
            const node = document.getElementById('calc-result');
            if(!v || !r) {{ node.innerText = "Target Current Flow: -- Amps"; return; }}
            node.innerText = `Target Current Flow: ${(v / r).toFixed(2)} Amps`;
        }}

        const codeLibrary = [
            {{ code: "P0171", desc: "System Too Lean (Bank 1) <span class='translation-text'>(The computer detects way too much raw air or not enough fuel entering the cylinders)</span>", symp: "Check Engine Light on, engine hesitation or sagging on acceleration, rough shaky idling.", cause: "Unmetered vacuum air leaks, a split rubber intake boot, a weak fuel pump running low on pressure, or dirty/clogged fuel fuel injectors." }}
        ];

        function searchCodes() {{
            const query = document.getElementById('code-search').value.toUpperCase();
            const container = document.getElementById('code-results');
            container.innerHTML = '';
            if(!query) return;
            const matches = codeLibrary.filter(item => item.code.includes(query));
            matches.forEach(item => {{
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `<div class="list-header">⚠️ CODE: ${{item.code}}</div><div style="font-size:14px; margin: 6px 0; font-weight:bold; color:var(--text-main);">${{item.desc}}</div>`;
                container.appendChild(div);
            }});
        }}

        const database = {json.dumps(questions)};
        let currentIdx = 0; let score = 0; let missedReport = [];

        function startRig() {{
            document.getElementById('rig-splash-screen').classList.add('hidden');
            document.getElementById('game-screen').classList.remove('hidden');
            loadQuestion();
        }}

        function loadQuestion() {{
            if (currentIdx >= database.length) return;
            const qData = database[currentIdx];
            document.getElementById('question-text').innerText = qData.q;
            const container = document.getElementById('options-container');
            container.innerHTML = '';
            qData.options.forEach(opt => {{
                const btn = document.createElement('button');
                btn.className = 'opt-btn';
                btn.innerText = opt;
                btn.onclick = () => {{ currentIdx++; loadQuestion(); }};
                container.appendChild(btn);
            }});
        }}
    </script>
</body>
</html>
"""
    
    os.makedirs('factory_output', exist_ok=True)
    output_path = 'factory_output/a6_electrical_v1.html'
    
    with open(output_path, 'w') as f:
        f.write(html_content)
    print("\n⚡ INSTRUMENT GAUGE UPGRADE PACKED: High-tech dials compiled successfully.")

    zip_name = 'A6_Master_Study_Pack.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(output_path, os.path.basename(output_path))
    print(f"📦 PACKAGING COMPLETE: Fresh master storefront bundle generated successfully.")

if __name__ == '__main__':
    generate_html()
