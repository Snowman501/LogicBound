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
    <title>A6 Electrical Master Stack</title>
    <style>
        :root {{
            --bg-dark: #121212;
            --card-bg: #1e1e1e;
            --blue-prime: #2196F3;
            --blue-hover: #1976D2;
            --text-main: #ffffff;
            --text-muted: #b0b0b0;
            --correct-green: #4CAF50;
            --incorrect-red: #F44336;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-dark);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 15px;
        }}
        .shop-container {{
            width: 100%;
            max-width: 500px;
            background: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
        }}
        h2 {{ color: var(--blue-prime); text-align: center; margin-bottom: 15px; font-size: 22px; }}
        .notice {{ background: #000; padding: 15px; border-radius: 8px; font-size: 13px; color: var(--text-muted); margin-bottom: 20px; border-left: 4px solid var(--blue-prime); }}
        .btn {{
            width: 100%; background: var(--blue-prime); color: #fff; border: none; padding: 15px;
            border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 10px;
        }}
        .btn:hover {{ background: var(--blue-hover); }}
        .hidden {{ display: none !important; }}
        
        .progress-wrapper {{ margin-bottom: 20px; }}
        .progress-text {{ font-size: 12px; color: var(--text-muted); display: flex; justify-content: space-between; margin-bottom: 5px; }}
        .progress-bar {{ width: 100%; height: 6px; background: #333; border-radius: 3px; overflow: hidden; }}
        .progress-fill {{ height: 100%; width: 0%; background: var(--blue-prime); transition: width 0.3s ease; }}
        
        .category-badge {{
            display: inline-block; background: #2a2a2a; color: var(--blue-prime);
            font-size: 11px; font-weight: bold; padding: 4px 8px; border-radius: 4px;
            margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;
            border: 1px solid #333;
        }}
        
        .q-card {{ font-size: 17px; line-height: 1.5; margin-bottom: 20px; min-height: 80px; }}
        .options-grid {{ display: flex; flex-direction: column; gap: 12px; }}
        .opt-btn {{
            width: 100%; background: #2d2d2d; color: var(--text-main); border: 1px solid #444;
            padding: 14px; border-radius: 8px; font-size: 15px; text-align: left; cursor: pointer;
        }}
        .opt-btn:hover {{ background: #3d3d3d; }}
        
        .modal {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85);
            display: flex; justify-content: center; align-items: center; padding: 20px; z-index: 1000;
        }}
        .modal-content {{ background: var(--card-bg); width: 100%; max-width: 400px; padding: 24px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: left; }}
        .status-title {{ font-size: 24px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }}
        .status-correct {{ color: var(--correct-green); }}
        .status-incorrect {{ color: var(--incorrect-red); }}
        .explanation {{ font-size: 16px; line-height: 1.5; color: #e0e0e0; margin-bottom: 20px; }}
        
        .review-item {{ background: #252525; padding: 12px; border-radius: 6px; margin-top: 10px; border-left: 3px solid var(--incorrect-red); font-size: 14px; }}
        .review-q {{ font-weight: bold; margin-bottom: 4px; }}
        .review-a {{ color: var(--correct-green); }}
        
        .telemetry-grade {{ font-size: 14px; font-weight: bold; text-align: center; margin-top: 5px; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="shop-container">
        <div id="splash-screen">
            <h2>A6 Electrical: Logic & Diagnostics</h2>
            <div class="notice">
                <strong>SHOP SAFETY NOTICE:</strong> This is an automated educational tool for ASE A6 prep. 
                Always reference factory wiring schematics. Logic Bound Studios assumes no liability for blown fuses or toasted ECUs.
            </div>
            <button class="btn" onclick="startEngine()">I ACCEPT & START ENGINE</button>
        </div>

        <div id="game-screen" class="hidden">
            <div class="progress-wrapper">
                <div class="progress-text">
                    <span id="tracker-count">Loading...</span>
                    <span id="tracker-pct">0%</span>
                </div>
                <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>
            </div>

            <div id="category-box" class="category-badge">⚡️ General Electrical</div>
            <div class="q-card" id="question-text">Loading question text...</div>
            <div class="options-grid" id="options-container"></div>
        </div>

        <div id="end-screen" class="hidden">
            <h2 id="end-title">A6 DIAGNOSTIC RUN COMPLETE</h2>
            <p style="text-align: center; margin-top: 15px; color: var(--text-main); font-size: 18px; font-weight: bold;" id="end-score">Score: 0/0</p>
            <div id="telemetry-box" class="telemetry-grade"></div>
            <div id="review-container" style="margin-top: 20px;"></div>
            <button class="btn" onclick="restartBundle()">RESTART BUNDLE</button>
        </div>
    </div>

    <div id="diagnostic-modal" class="modal hidden">
        <div class="modal-content">
            <div id="modal-status" class="status-title"></div>
            <div id="modal-explanation" class="explanation"></div>
            <button class="btn" onclick="closeDiagnosticModal()">OK</button>
        </div>
    </div>

    <script>
        const database = {json.dumps(questions)};
        let currentIdx = 0;
        let score = 0;
        let missedReport = [];

        function startEngine() {{
            document.getElementById('splash-screen').classList.add('hidden');
            document.getElementById('game-screen').classList.remove('hidden');
            loadQuestion();
        }}

        function loadQuestion() {{
            if (currentIdx >= database.length) {{
                showFinalReport();
                return;
            }}

            const qData = database[currentIdx];
            const progPct = Math.round((currentIdx / database.length) * 100);
            document.getElementById('tracker-count').innerText = `Question ${{currentIdx + 1}} of ${{database.length}}`;
            document.getElementById('tracker-pct').innerText = `${{progPct}}%`;
            document.getElementById('progress-fill').style.width = `${{progPct}}%`;

            const badge = document.getElementById('category-box');
            const lowerQ = qData.q.toLowerCase();
            if(lowerQ.includes("can-bus") || lowerQ.includes("communication")) {{
                badge.innerText = "🌐 Network & Data Bus";
            }} else if(lowerQ.includes("ohm") || lowerQ.includes("circuit theory")) {{
                badge.innerText = "📊 Electrical Theory";
            }} else if(lowerQ.includes("drop") || lowerQ.includes("multimeter") || lowerQ.includes("parasitic")) {{
                badge.innerText = "⚡️ Circuit Diagnostics";
            }} else if(lowerQ.includes("starter") || lowerQ.includes("cranking") || lowerQ.includes("alternator") || lowerQ.includes("diode")) {{
                badge.innerText = "🔋 Starting & Charging Systems";
            }} else {{
                badge.innerText = "🔧 System Diagnostics";
            }}

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
                statusNode.innerHTML = "✅ CORRECT";
            }} else {{
                statusNode.className = "status-title status-incorrect";
                statusNode.innerHTML = "❌ INCORRECT";
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
            document.getElementById('end-score').innerText = `Final Score: ${{score}} / ${{database.length}} (${{scorePct}}%)`;
            
            const telemetry = document.getElementById('telemetry-box');
            if (scorePct >= 80) {{
                document.getElementById('end-title').innerText = "🥇 CERTIFICATION READY";
                telemetry.style.color = "var(--correct-green)";
                telemetry.innerText = "🏅 PASSING SCORE - EXCELLENT LOGIC";
            }} else {{
                document.getElementById('end-title').innerText = "🔧 RETEST RECOMMENDED";
                telemetry.style.color = "var(--incorrect-red)";
                telemetry.innerText = "⚠️ ATTENTION REQUIRED IN SHOP THEORY";
            }}

            const reviewBox = document.getElementById('review-container');
            reviewBox.innerHTML = '';

            if (score === database.length) {{
                reviewBox.innerHTML = '<p style="text-align:center; color:var(--correct-green); font-size:15px;">Flawless diagnostic run. Ready for the field.</p>';
            }} else {{
                reviewBox.innerHTML = '<h3 style="font-size:14px; margin-bottom:5px; color:var(--text-muted);">Review Targeted Subsystems:</h3>';
                missedReport.forEach(item => {{
                    const div = document.createElement('div');
                    div.className = 'review-item';
                    div.innerHTML = `<div class="review-q">${{item.q}}</div><div class="review-a">🔧 Correct Answer: ${{item.correct}}</div>`;
                    reviewBox.appendChild(div);
                }});
            }}
        }}

        function restartBundle() {{
            currentIdx = 0;
            score = 0;
            missedReport = [];
            document.getElementById('end-screen').classList.add('hidden');
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
    print("\n🚀 FACTORY ONLINE: Upgraded 10-Question Master Stack generated successfully.")

    zip_name = 'A6_Master_Study_Pack.zip'
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(output_path, os.path.basename(output_path))
    print(f"📦 PACKAGING COMPLETE: {zip_name} has been manufactured!")

if __name__ == '__main__':
    generate_html()
