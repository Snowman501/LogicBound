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
            --bg-dark: #0f0f12;
            --card-bg: #16161a;
            --panel-dark: #0a0a0c;
            --blue-prime: #007acc;
            --blue-glow: #00a2ff;
            --text-main: #e2e8f0;
            --text-muted: #718096;
            --correct-green: #38a169;
            --incorrect-red: #e53e3e;
            --amber-warn: #dd6b20;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-dark);
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
            border-radius: 12px;
            border: 1px solid #2d3748;
            box-shadow: 0 12px 36px rgba(0,0,0,0.7);
            overflow: hidden;
            margin-top: 10px;
        }}
        .header-bar {{
            background: var(--panel-dark);
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #2d3748;
        }}
        .header-title {{ font-size: 18px; font-weight: bold; color: var(--blue-glow); letter-spacing: 0.75px; font-family: monospace; }}
        .status-pill {{ background: #1c2d24; color: #68d391; font-size: 11px; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: 1px solid #22543d; }}
        
        .tab-nav {{ display: flex; background: #121215; border-bottom: 1px solid #2d3748; overflow-x: auto; }}
        .tab-nav.hidden {{ display: none !important; }}
        .tab-btn {{ flex: 1; background: none; border: none; color: var(--text-muted); padding: 14px 10px; font-size: 12px; font-weight: bold; cursor: pointer; text-align: center; white-space: nowrap; transition: all 0.2s ease; }}
        .tab-btn:hover {{ color: var(--text-main); background: rgba(255,255,255,0.02); }}
        .tab-btn.active {{ color: var(--blue-glow); background: var(--card-bg); border-bottom: 2px solid var(--blue-prime); }}
        
        .workspace {{ padding: 20px; min-height: 450px; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        .telemetry-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 15px; }}
        .telemetry-tile {{ background: var(--panel-dark); padding: 12px; border-radius: 6px; border: 1px solid #2d3748; }}
        .tile-lbl {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }}
        .tile-val {{ font-size: 18px; font-weight: bold; color: var(--text-main); font-family: monospace; }}
        
        .dtc-box {{ background: #2a1b1b; border: 1px solid #742a2a; border-radius: 6px; padding: 12px; margin-top: 15px; }}
        .dtc-title {{ font-size: 13px; font-weight: bold; color: #feb2b2; margin-bottom: 6px; }}
        .dtc-item {{ font-family: monospace; font-size: 13px; color: #fc8181; padding: 4px 0; }}
        
        .search-box {{ display: flex; gap: 10px; margin-bottom: 15px; }}
        .search-input {{ flex: 1; background: var(--panel-dark); border: 1px solid #4a5568; padding: 12px; color: #fff; border-radius: 6px; font-size: 15px; font-family: monospace; }}
        
        .progress-wrapper {{ margin-bottom: 20px; }}
        .progress-text {{ font-size: 12px; color: var(--text-muted); display: flex; justify-content: space-between; margin-bottom: 5px; }}
        .progress-bar {{ width: 100%; height: 6px; background: #333; border-radius: 3px; overflow: hidden; }}
        .progress-fill {{ height: 100%; width: 0%; background: var(--blue-prime); transition: width 0.3s ease; }}
        .category-badge {{ display: inline-block; background: #2a2a2a; color: var(--blue-glow); font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 4px; margin-bottom: 10px; text-transform: uppercase; border: 1px solid #333; }}
        .q-card {{ font-size: 16px; line-height: 1.5; margin-bottom: 20px; min-height: 70px; }}
        .options-grid {{ display: flex; flex-direction: column; gap: 10px; }}
        .opt-btn {{ width: 100%; background: #22252a; color: var(--text-main); border: 1px solid #3a4454; padding: 14px; border-radius: 6px; font-size: 15px; text-align: left; cursor: pointer; }}
        
        .modal {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); display: flex; justify-content: center; align-items: center; padding: 20px; z-index: 1000; }}
        .modal-content {{ background: var(--card-bg); width: 100%; max-width: 400px; padding: 24px; border-radius: 12px; text-align: left; border: 1px solid #4a5568; }}
        .status-title {{ font-size: 22px; font-weight: bold; margin-bottom: 12px; }}
        .status-correct {{ color: var(--correct-green); }}
        .status-incorrect {{ color: var(--incorrect-red); }}
        .explanation {{ font-size: 15px; line-height: 1.5; color: #cbd5e0; margin-bottom: 20px; }}
        
        .btn {{ width: 100%; background: var(--blue-prime); color: #fff; border: none; padding: 14px; border-radius: 6px; font-size: 15px; font-weight: bold; cursor: pointer; }}
        .btn:hover {{ background: #1976D2; }}
        .hidden {{ display: none !important; }}
        
        .list-container {{ display: flex; flex-direction: column; gap: 12px; }}
        .list-item {{ background: var(--panel-dark); border: 1px solid #2d3748; padding: 15px; border-radius: 6px; }}
        .list-header {{ font-weight: bold; font-family: monospace; color: var(--blue-glow); margin-bottom: 6px; font-size: 15px; }}
        .step-block {{ margin-left: 10px; margin-top: 8px; font-size: 13px; border-left: 2px solid #2d3748; padding-left: 10px; color: #cbd5e0; }}
        .step-num {{ color: var(--blue-glow); font-weight: bold; font-family: monospace; }}
        .translation-text {{ color: #a0aec0; font-style: italic; font-size: 13px; display: block; margin-top: 2px; }}

        .bench-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }}
        .bench-input {{ width: 100%; background: var(--panel-dark); border: 1px solid #4a5568; padding: 10px; color: #fff; border-radius: 4px; font-family: monospace; font-size: 14px; margin-top: 4px; }}
        .bench-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; text-align: left; }}
        .bench-table th {{ color: var(--blue-glow); border-bottom: 1px solid #4a5568; padding: 6px 4px; }}
        .bench-table td {{ padding: 6px 4px; border-bottom: 1px solid #2d3748; }}
        
        .legal-notice {{ background: #000; border: 1px solid #333; padding: 15px; border-radius: 6px; font-size: 13px; color: var(--text-muted); line-height: 1.5; margin-bottom: 20px; max-height: 160px; overflow-y: auto; text-align: left; }}
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
                <div class="telemetry-row">
                    <div class="telemetry-tile"><div class="tile-lbl">Datalink Interface</div><div class="tile-val" style="color:var(--correct-green); font-size:14px;">CAN-BUS (ISO 15765)</div></div>
                    <div class="telemetry-tile"><div class="tile-lbl">System Voltage</div><div class="tile-val">14.26 V</div></div>
                </div>
                <div class="telemetry-row">
                    <div class="telemetry-tile"><div class="tile-lbl">Engine RPM</div><div class="tile-val">748 rpm</div></div>
                    <div class="telemetry-tile"><div class="tile-lbl">Coolant Temp (ECT)</div><div class="tile-val">196 °F</div></div>
                </div>
                <div class="telemetry-row">
                    <div class="telemetry-tile"><div class="tile-lbl">Throttle Position</div><div class="tile-val">14.2 %</div></div>
                    <div class="telemetry-tile"><div class="tile-lbl">Calculated Load</div><div class="tile-val">22.5 %</div></div>
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
                    
                    <div class="list-item">
                        <div class="list-header">🔧 DIGITAL FUSE VOLTAGE DROP PARASITIC DRAW RUN</div>
                        <span class="translation-text">(How to locate what is secretly draining your battery overnight while the car is turned off)</span>
                        <div class="step-block">
                            <p><span class="step-num">01.</span> Set your Multimeter to DC Millivolts (mV). Turn the key OFF, latch the doors, and wait 45 minutes for all computer modules to enter "Sleep Mode".</p>
                            <p><span class="step-num">02.</span> Touch your meter's metal test probes directly to the two tiny exposed metal test points on the plastic back of the fuse.</p>
                            <p><span class="step-num">03.</span> Note the mV reading. If it shows 0.0mV, that branch circuit is asleep and drawing zero battery current.</p>
                            <p><span class="step-num">04.</span> If you see any millivolt numbers, electricity is actively leaking out. Cross-reference that mV number with a fuse chart to find the exact hidden milliamp battery draw without accidentally waking up the vehicle network lines by pulling fuses.</p>
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

                    <div class="list-item">
                        <div class="list-header">📊 WIRE GAUGE (AWG) MAXIMUM CURRENT LOAD SCALE</div>
                        <span class="translation-text">(The safety metric matching wire diameter thickness to maximum continuous electrical load limits)</span>
                        <table class="bench-table">
                            <thead><tr><th>Wire Size</th><th>Max Amps</th><th>Common Shop Application</th></tr></thead>
                            <tbody>
                                <tr><td>10 AWG (Thick)</td><td>30 Amps</td><td>Main power feeds, high-output electric fans</td></tr>
                                <tr><td>12 AWG</td><td>20 Amps</td><td>Fuel pumps, heavy headlight relays, horns</td></tr>
                                <tr><td>14 AWG</td><td>15 Amps</td><td>Brake light strings, accessory power sockets</td></tr>
                                <tr><td>16 AWG</td><td>10 Amps</td><td>Standard sensor triggers, fuel injector lines</td></tr>
                                <tr><td>18/20 AWG (Thin)</td><td>5 Amps</td><td>Computer data lines, low-energy instrument sensor wires</td></tr>
                            </tbody>
                        </table>
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
                
                <div id="end-screen" class="hidden">
                    <h3 id="end-title" style="color:var(--blue-glow); margin-bottom:10px;">DIAGNOSTIC BLOCK FINISHED</h3>
                    <p id="end-score" style="font-size:16px; font-weight:bold; margin-bottom:5px;">Score: 0/0</p>
                    <div id="telemetry-box" style="font-size:12px; font-weight:bold; text-transform:uppercase; margin-bottom:15px;"></div>
                    <div id="review-container"></div>
                    <button class="btn" onclick="restartRig()" style="margin-top:15px;">CYCLE RUN BUNDLE</button>
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
        function acceptTerms() {{
            document.getElementById('splash-screen').classList.add('hidden');
            document.getElementById('main-nav').classList.remove('hidden');
            document.getElementById('scanner-tab').classList.add('active');
            
            const status = document.getElementById('mainframe-status');
            status.innerText = "SYSTEM ONLINE // NOMINAL";
            status.style.background = "#1c2d24";
            status.style.color = "#68d391";
            status.style.borderColor = "#22543d";
        }}

        function switchTab(evt, tabId) {{
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            evt.currentTarget.classList.add('active');
        }}

        function runOhmCalc() {{
            const v = parseFloat(document.getElementById('calc-volt').value);
            const r = parseFloat(document.getElementById('calc-ohm').value);
            const node = document.getElementById('calc-result');
            if(!v || !r) {{ node.innerText = "Target Current Flow: -- Amps"; return; }}
            const current = (v / r).toFixed(2);
            node.innerText = `Target Current Flow: ${{current}} Amps`;
        }}

        // Expanded Production Database Core Asset Matrix
        const codeLibrary = [
            {{ code: "P0102", desc: "Mass Air Flow (MAF) Circuit Low Input <span class='translation-text'>(The engine's air intake volume sensor signal is way too low, causing severe engine hesitation)</span>", symp: "Engine stalling immediately on start, severe acceleration lag, rich fuel trim correction codes.", cause: "Contaminated sensor hot-wire, unmetered air leaking past a cracked intake boot, open ground circuit, or a shorted 5V sensor reference line." }},
            {{ code: "P0113", desc: "Intake Air Temperature (IAT) Sensor 1 Circuit High Input <span class='translation-text'>(The computer reads cold air temperatures maxed at -40°F due to an open circuit connection)</span>", symp: "Hard starting when cold, poor fuel economy, engine control unit defaults to a backup safe tracking lookup table.", cause: "Broken internal sensor element, open circuit in the signal return wire, or a disconnected wiring harness plug element." }},
            {{ code: "P0171", desc: "System Too Lean (Bank 1) <span class='translation-text'>(The computer detects way too much raw air or not enough fuel entering the cylinders)</span>", symp: "Check Engine Light on, engine hesitation or sagging on acceleration, rough shaky idling.", cause: "Unmetered vacuum air leaks, a split rubber intake boot, a weak fuel pump running low on pressure, or dirty/clogged fuel fuel injectors." }},
            {{ code: "P0174", desc: "System Too Lean (Bank 2) <span class='translation-text'>(Too much raw air or weak fuel levels on the second cylinder bank side)</span>", symp: "Power loss when driving up hills, check engine light flashing, lazy low-performance throttle response.", cause: "Intake manifold plenum seal leak, or restricted fuel delivery blocks." }},
            {{ code: "P0300", desc: "Random/Multiple Cylinder Misfire Detected <span class='translation-text'>(Cylinders are failing to explode/fire properly at unpredictable random intervals)</span>", symp: "Heavy engine shaking, flashing Check Engine Light, severe engine bucking, raw gas smell out the tailpipe.", cause: "Unstable vehicle fuel pressure delivery, massive broad vacuum leaks affecting all cylinders, or a bad batch of water-contaminated fuel." }},
            {{ code: "P0302", desc: "Cylinder 2 Misfire Detected <span class='translation-text'>(Cylinder Number 2 is specifically failing to create internal spark or explosion)</span>", symp: "Rhythmic engine chug or skip, rough idle, loss of cruising power.", cause: "Defective Cylinder 2 secondary ignition coil pack, fouled or cracked spark plug, or a broken fuel injector wire." }},
            {{ code: "P0420", desc: "Catalytic Converter System Efficiency Below Threshold (Bank 1) <span class='translation-text'>(The emission exhaust filter device is failing its cleanup efficiency test)</span>", symp: "Usually zero driving symptoms, potential sulfur/rotten-egg odor coming from the exhaust pipe under load.", cause: "Exhaust leaks upstream, engine misfires melting the converter internals, or old degraded core metal substrate layers." }},
            {{ code: "P0562", desc: "System Voltage Low <span class='translation-text'>(The car's main electrical operating voltage has dropped way below standard limits)</span>", symp: "Dim dashboard lights, erratic or delayed transmission shifts, global communication module dropouts.", cause: "Failing alternator internal field voltage regulator, loose drive belt, or heavily corroded main battery ground cables." }},
            {{ code: "U0100", desc: "Lost Communication With ECM/PCM <span class='translation-text'>(The main engine control computer has completely dropped off the electronic network line)</span>", symp: "Starter motor won't crank or turn over, dashboard instrument needles freeze completely, scan tool reads 'No Link'.", cause: "Open or shorted network data trunk lines, a blown main electronic engine control fuse block link, or a broken main chassis frame ground strap." }},
            {{ code: "U0155", desc: "Lost Communication With Instrument Panel Cluster Control Module <span class='translation-text'>(The dashboard display gauges have lost their connection network line back to the vehicle)</span>", symp: "Speedometer and tachometer needles freeze instantly at zero, warning lights lock on, odometer display goes blank.", cause: "Loose or backed-out electrical connector pins on the back of the dashboard frame housing, or a severed data wire branch." }}
        ];

        function searchCodes() {{
            const query = document.getElementById('code-search').value.toUpperCase();
            const container = document.getElementById('code-results');
            container.innerHTML = '';
            if(!query) return;
            const matches = codeLibrary.filter(item => item.code.includes(query) || item.desc.toUpperCase().includes(query));
            if(matches.length === 0) {{
                container.innerHTML = '<div style="font-size:13px; color:var(--text-muted); text-align:center; padding:10px;">No code blueprints located in database.</div>';
                return;
            }}
            matches.forEach(item => {{
                const div = document.createElement('div');
                div.className = 'list-item';
                div.innerHTML = `
                    <div class="list-header">⚠️ CODE: ${{item.code}}</div>
                    <div style="font-size:14px; margin: 6px 0; font-weight:bold; color:var(--text-main);">${{item.desc}}</div>
                    <div style="font-size:13px; margin: 4px 0;"><span style="color:var(--text-muted); font-weight:bold;">Real Symptoms:</span> ${{item.symp}}</div>
                    <div style="font-size:13px;"><span style="color:var(--blue-glow); font-weight:bold;">Suspected Fault Root Cause:</span> ${{item.cause}}</div>
                `;
                container.appendChild(div);
            }});
        }}

        document.addEventListener("DOMContentLoaded", () => {{
            document.getElementById('code-search').value = "";
        }});

        const database = {json.dumps(questions)};
        let currentIdx = 0; let score = 0; let missedReport = [];

        function startRig() {{
            document.getElementById('rig-splash-screen').classList.add('hidden');
            document.getElementById('game-screen').classList.remove('hidden');
            loadQuestion();
        }}

        function loadQuestion() {{
            if (currentIdx >= database.length) {{ showFinalReport(); return; }}
            const qData = database[currentIdx];
            const progPct = Math.round((currentIdx / database.length) * 100);
            document.getElementById('tracker-count').innerText = `Question ${{currentIdx + 1}} of ${{database.length}}`;
            document.getElementById('tracker-pct').innerText = `${{progPct}}%`;
            document.getElementById('progress-fill').style.width = `${{progPct}}%`;

            const badge = document.getElementById('category-box');
            const lowerQ = qData.q.toLowerCase();
            if(lowerQ.includes("can-bus") || lowerQ.includes("communication")) {{ badge.innerText = "🌐 Network & Data Bus"; }}
            else if(lowerQ.includes("ohm") || lowerQ.includes("circuit theory")) {{ badge.innerText = "📊 Electrical Theory"; }}
            else if(lowerQ.includes("drop") || lowerQ.includes("multimeter") || lowerQ.includes("parasitic")) {{ badge.innerText = "⚡️ Circuit Diagnostics"; }}
            else if(lowerQ.includes("starter") || lowerQ.includes("cranking") || lowerQ.includes("alternator") || lowerQ.includes("diode")) {{ badge.innerText = "🔋 Starting & Charging Systems"; }}
            else {{ badge.innerText = "🔧 System Diagnostics"; }}

            document.getElementById('question-text').innerText = qData.q;
            const container = document.getElementById('options-container');
            container.innerHTML = '';
            qData.options.forEach(opt => {{
                const btn = document.createElement('button');
                btn.className = 'opt-btn';
                btn.innerText = opt;
                btn.onclick = () => verifyAnswer(opt, qData.a, qData.explanation, qData.q);
                container.appendChild(btn);
            }});
        }}

        function verifyAnswer(chosen, correct, exp, qText) {{
            const modal = document.getElementById('diagnostic-modal');
            const statusNode = document.getElementById('modal-status');
            const expNode = document.getElementById('modal-explanation');
            if (chosen === correct) {{
                score++;
                statusNode.className = "status-title status-correct";
                statusNode.innerHTML = "✅ CORE VERIFIED";
            }} else {{
                statusNode.className = "status-title status-incorrect";
                statusNode.innerHTML = "❌ LOGIC FAULT";
                missedReport.push({{ q: qText, correct: correct }});
            }}
            expNode.innerText = exp;
            modal.classList.remove('hidden');
        }}

        function closeDiagnosticModal() {{
            document.getElementById('diagnostic-modal').classList.add('hidden');
            currentIdx++;
            loadQuestion();
        }}

        function showFinalReport() {{
            document.getElementById('game-screen').classList.add('hidden');
            const endScreen = document.getElementById('end-screen');
            endScreen.classList.remove('hidden');
            const scorePct = Math.round((score / database.length) * 100);
            document.getElementById('end-score').innerText = `Final Core Score: ${{score}} / ${{database.length}} (${{scorePct}}%)`;
            
            const telemetry = document.getElementById('telemetry-box');
            if (scorePct >= 80) {{
                document.getElementById('end-title').innerText = "🥇 SCANNER CORE MASTERED";
                telemetry.style.color = "var(--correct-green)";
                telemetry.innerText = "🏅 CORE LOGIC NOMINAL";
            }} else {{
                document.getElementById('end-title').innerText = "🔧 CORRECTION REQUESTED";
                telemetry.style.color = "var(--incorrect-red)";
                telemetry.innerText = "⚠️ SYSTEM GAPS IDENTIFIED IN THEORY BLOCK";
            }}
            const reviewBox = document.getElementById('review-container');
            reviewBox.innerHTML = '';
            if (score === database.length) {{
                reviewBox.innerHTML = '<p style="text-align:center; color:var(--correct-green); font-size:14px;">Flawless diagnostic loop run. Core logic verified.</p>';
            }} else {{
                reviewBox.innerHTML = '<h4 style="font-size:13px; margin-bottom:5px; color:var(--text-muted);">Targeted Master Review Checklist:</h4>';
                missedReport.forEach(item => {{
                    const div = document.createElement('div');
                    div.className = 'review-item';
                    div.innerHTML = `<div style="font-weight:bold; margin-bottom:4px;">${{item.q}}</div><div style="color:var(--correct-green)">🔧 Target Blueprint: ${{item.correct}}</div>`;
                    reviewBox.appendChild(div);
                }});
            }}
        }}

        function restartRig() {{
            currentIdx = 0; score = 0; missedReport = [];
            document.getElementById('end-screen').classList.add('hidden');
            document.getElementById('rig-splash-screen').classList.remove('hidden');
        }}
    </script>
</body>
</html>
"""
    
    os.makedirs('factory_output', exist_ok=True)
    output_path = 'factory_output/a6_electrical_v1.html'
    
    with open(output_path, 'w') as f:
        f.write(html_content)
    print("\n⚡️ SHATTERSCAN EXTENDED CORE PACKED: Multi-module asset matrix expansion complete.")

    zip_name = 'A6_Master_Study_Pack.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(output_path, os.path.basename(output_path))
    print(f"📦 PACKAGING COMPLETE: Fresh master archive generated successfully.")

if __name__ == '__main__':
    generate_html()
