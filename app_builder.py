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
    <title>ShatterScan Core: Advanced Diagnostic Terminal</title>
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
        
        .tab-nav {{
            display: flex;
            background: #121215;
            border-bottom: 1px solid #2d3748;
            overflow-x: auto;
        }}
        .tab-btn {{
            flex: 1;
            background: none;
            border: none;
            color: var(--text-muted);
            padding: 14px 10px;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            white-space: nowrap;
            transition: all 0.2s ease;
        }}
        .tab-btn:hover {{ color: var(--text-main); background: rgba(255,255,255,0.02); }}
        .tab-btn.active {{ color: var(--blue-glow); background: var(--card-bg); border-bottom: 2px solid var(--blue-prime); }}
        
        .workspace {{ padding: 20px; min-height: 450px; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        .telemetry-row {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 15px;
        }}
        .telemetry-tile {{
            background: var(--panel-dark); padding: 12px; border-radius: 6px; border: 1px solid #2d3748;
        }}
        .tile-lbl {{ font-size: 11px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }}
        .tile-val {{ font-size: 18px; font-weight: bold; color: var(--text-main); font-family: monospace; }}
        
        .dtc-box {{
            background: #2a1b1b; border: 1px solid #742a2a; border-radius: 6px; padding: 12px; margin-top: 15px;
        }}
        .dtc-title {{ font-size: 13px; font-weight: bold; color: #feb2b2; margin-bottom: 6px; }}
        .dtc-item {{ font-family: monospace; font-size: 13px; color: #fc8181; padding: 4px 0; }}
        
        .search-box {{
            display: flex; gap: 10px; margin-bottom: 15px;
        }}
        .search-input {{
            flex: 1; background: var(--panel-dark); border: 1px solid #4a5568; padding: 12px;
            color: #fff; border-radius: 6px; font-size: 15px; font-family: monospace;
        }}
        .search-input:focus {{ outline: none; border-color: var(--blue-prime); }}
        
        .progress-wrapper {{ margin-bottom: 20px; }}
        .progress-text {{ font-size: 12px; color: var(--text-muted); display: flex; justify-content: space-between; margin-bottom: 5px; }}
        .progress-bar {{ width: 100%; height: 6px; background: #333; border-radius: 3px; overflow: hidden; }}
        .progress-fill {{ height: 100%; width: 0%; background: var(--blue-prime); transition: width 0.3s ease; }}
        .category-badge {{
            display: inline-block; background: #2a2a2a; color: var(--blue-glow);
            font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 4px;
            margin-bottom: 10px; text-transform: uppercase; border: 1px solid #333;
        }}
        .q-card {{ font-size: 16px; line-height: 1.5; margin-bottom: 20px; min-height: 70px; }}
        .options-grid {{ display: flex; flex-direction: column; gap: 10px; }}
        .opt-btn {{
            width: 100%; background: #22252a; color: var(--text-main); border: 1px solid #3a4454;
            padding: 14px; border-radius: 6px; font-size: 15px; text-align: left; cursor: pointer; transition: background 0.15s;
        }}
        .opt-btn:hover {{ background: #2d323b; border-color: var(--blue-prime); }}
        
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
        
        .review-item {{ background: #1c1d22; padding: 12px; border-radius: 6px; margin-top: 10px; border-left: 3px solid var(--incorrect-red); font-size: 14px; }}
    </style>
</head>
<body>
    <div class="mainframe">
        <div class="header-bar">
            <div class="header-title">⚡️ SHATTERSCAN // CORE</div>
            <div class="status-pill">SYSTEM ONLINE</div>
        </div>
        
        <div class="tab-nav">
            <button class="tab-btn active" onclick="switchTab(event, 'scanner-tab')">📟 SCANNER</button>
            <button class="tab-btn" onclick="switchTab(event, 'codes-tab')">🔌 OBD CODES</button>
            <button class="tab-btn" onclick="switchTab(event, 'manual-tab')">📚 REPAIR MANUAL</button>
            <button class="tab-btn" onclick="switchTab(event, 'rig-tab')">🧠 ASE TEST RIG</button>
        </div>
        
        <div class="workspace">
            <div id="scanner-tab" class="tab-content active">
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
                        <p style="font-size:13px; color:var(--text-muted);">Isolates high resistance in wiring, connections, or switches without taking the harness apart.</p>
                        <div class="step-block">
                            <p><span class="step-num">01.</span> Set DMM to DC Volts (V). Do NOT disconnect any connectors.</p>
                            <p><span class="step-num">02.</span> Power up the circuit and engage the component load (ON position).</p>
                            <p><span class="step-num">03.</span> Connect the RED lead to the source side of the connection being verified.</p>
                            <p><span class="step-num">04.</span> Connect the BLACK lead to the load side of the same connection block.</p>
                            <p><span class="step-num">05.</span> Read the display. A perfect copper junction shows less than 0.1V. If it reads above 0.2V, high resistance is present inside that connection junction.</p>
                        </div>
                    </div>
                    
                    <div class="list-item">
                        <div class="list-header">🔧 DIGITAL FUSE VOLTAGE DROP PARASITIC DRAW RUN</div>
                        <p style="font-size:13px; color:var(--text-muted);">Locates module battery drain without waking up the vehicle's network modules.</p>
                        <div class="step-block">
                            <p><span class="step-num">01.</span> Set DMM to DC Millivolts (mV). Key off, doors latched, wait 45 minutes for full network sleep mode.</p>
                            <p><span class="step-num">02.</span> Touch DMM test probes directly across the two small metal test tabs on the back of the fuse.</p>
                            <p><span class="step-num">03.</span> Note the mV reading. A reading of 0.0mV indicates zero current flow through that branch circuit.</p>
                            <p><span class="step-num">04.</span> If millivolts are detected, cross-reference the mV reading with an industry standard fuse conversion chart for that specific fuse type (Mini, ATO, Maxi) to get the exact milliamp parasitic draw.</p>
                        </div>
                    </div>

                    <div class="list-item">
                        <div class="list-header">🔧 CONTROLLER AREA NETWORK (CAN) RESISTANCE BENCH CHECK</div>
                        <p style="font-size:13px; color:var(--text-muted);">Verifies data bus wire integrity and matching terminating resistor loops.</p>
                        <div class="step-block">
                            <p><span class="step-num">01.</span> Disconnect the negative battery cable to clear floating voltage potentials from the data network lines.</p>
                            <p><span class="step-num">02.</span> Set DMM to Ohms (Ω). Access the DLC (Data Link Connector) port frame.</p>
                            <p><span class="step-num">03.</span> Connect test leads across Pin 6 (CAN High) and Pin 14 (CAN Low).</p>
                            <p><span class="step-num">04.</span> Nominal reading must be exactly 60 Ω (Two 120 Ω resistors in parallel loop configuration).</p>
                            <p><span class="step-num">05.</span> A reading of 120 Ω indicates an open circuit in one of the terminal resistor modules or a severed wire branch.</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div id="rig-tab" class="tab-content">
                <div id="splash-screen">
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
        function switchTab(evt, tabId) {{
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            evt.currentTarget.classList.add('active');
        }}

        const codeLibrary = [
            {{ code: "P0171", desc: "System Too Lean (Bank 1)", symp: "MIL Illuminated, lean hesitation, rough idle, fuel trims above +15%.", cause: "Vacuum distribution leaks, unmetered air leaking past MAF boot, weak fuel pump delivery, or restricted fuel injectors." }},
            {{ code: "P0174", desc: "System Too Lean (Bank 2)", symp: "Engine sag under load, lazy oxygen sensor tracking, surging cruise speeds.", cause: "Intake manifold gasket leakage specific to Bank 2 plenum base, contaminated fuel distribution block modules." }},
            {{ code: "P0300", desc: "Random/Multiple Cylinder Misfire Detected", symp: "Flashing Check Engine Light, severe engine rumble, catalytic converter overheating.", cause: "Fluctuating system fuel pressure delivery, broad vacuum leak distributions, bad batch fuel." }},
            {{ code: "P0302", desc: "Cylinder 2 Misfire Detected", symp: "Rhythmic engine stumble, unburned fuel odor exiting tailpipe.", cause: "Defective Cylinder 2 secondary ignition coil pack, fouled plug gap, shorted driver circuit inside PCM, or dead cylinder injector coil." }},
            {{ code: "P0420", desc: "Catalytic Converter System Efficiency Below Threshold (Bank 1)", symp: "None or minor tailpipe odor, failed emissions probe readings.", cause: "Exhaust leaks upstream of converter, oil contamination from leaking valve guide seals, or degraded internal catalyst substrate block." }},
            {{ code: "P0562", desc: "System Voltage Low", symp: "Dim dash layouts, erratic transmission shift delays, global module network drops.", cause: "Failing alternator internal field regulator, slip ring brush wear, loose belt, corroded main power cables." }},
            {{ code: "U0100", desc: "Lost Communication With ECM/PCM", symp: "No-crank condition, instrument cluster instruments freeze, absolute scan data link loss.", cause: "Open or shorted network wiring trunk line, blown electronic engine control module main fuse link, or blown ground strap." }},
            {{ code: "U0155", desc: "Lost Communication With Instrument Panel Cluster (IPC) Control Module", symp: "Gauge pointers freeze at zero position, warning lights illuminate, odometer displays dashes.", cause: "Loose connector pins on back of dashboard frame cluster layout, data bus branch line shorted to ground." }}
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
                    <div class="list-header">⚠️ ${{item.code}} - ${{item.desc}}</div>
                    <div style="font-size:13px; margin: 4px 0;"><span style="color:var(--text-muted); font-weight:bold;">Symptom:</span> ${{item.symp}}</div>
                    <div style="font-size:13px;"><span style="color:var(--blue-glow); font-weight:bold;">Suspected Fault Side:</span> ${{item.cause}}</div>
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
            document.getElementById('splash-screen').classList.add('hidden');
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
            document.getElementById('splash-screen').classList.open;
            document.getElementById('splash-screen').classList.remove('hidden');
        }}
    </script>
</body>
</html>
"""
    
    os.makedirs('factory_output', exist_ok=True)
    output_path = 'factory_output/a6_electrical_v1.html'
    
    with open(output_path, 'w') as f:
        f.write(html_content)
    print("\n⚡️ SHATTERSCAN DATA CORE SECURED: String layout formatting fault bypass successful.")

    zip_name = 'A6_Master_Study_Pack.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(output_path, os.path.basename(output_path))
    print(f"📦 PACKAGING COMPLETE: {zip_name} shipped to output warehouse.")

if __name__ == '__main__':
    generate_html()
