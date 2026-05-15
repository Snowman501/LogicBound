import json, os, shutil
# This reaches into your other file to grab the parts
try:
    from ase_a6_questions import a6_level_1
except ImportError:
    # Fallback parts bin if the file is missing
    a6_level_1 = [{"q": "Error: ase_a6_questions.py not found.", "options": ["Fix it", "Skip"], "a": "Fix it", "explanation": "Check your file name."}]

def build_a6_game(title, data_list, theme="#2980b9"):
    json_data = json.dumps(data_list)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: sans-serif; background: #121212; color: white; text-align: center; margin: 0; }}
        #app {{ padding: 15px; max-width: 450px; margin: auto; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; }}
        .card {{ background: #1e1e1e; padding: 25px; border-radius: 15px; border-top: 5px solid {theme}; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }}
        .btn {{ background: #333; color: white; border: 1px solid #444; padding: 15px; border-radius: 8px; width: 100%; margin: 8px 0; text-align: left; font-size: 1rem; cursor: pointer; }}
        .start-btn {{ background: {theme}; color: white; border: none; padding: 18px; border-radius: 8px; width: 100%; font-weight: bold; font-size: 1.2rem; cursor: pointer; }}
        .disclaimer-text {{ font-size: 0.8rem; color: #aaa; text-align: left; line-height: 1.4; background: #000; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; }}
        #game-ui {{ display: none; }}
    </style>
</head>
<body>
    <div id="app">
        <div id="safety-page">
            <h2 style="color:{theme}">{title}</h2>
            <div class="disclaimer-text">
                <b>SHOP SAFETY NOTICE:</b> This is an educational study tool for ASE A6 prep. 
                Automotive diagnostics involve high-current circuits and sensitive electronics. 
                Always refer to the official Service Manual. Logic Bound Studios is not liable 
                for damages or injuries resulting from improper tool use.
            </div>
            <button class="start-btn" onclick="startEngine()">I ACCEPT & START ENGINE</button>
        </div>

        <div id="game-ui">
            <div id="t" style="color:#ff4757; font-weight:bold; margin-bottom:10px; font-size:1.2rem;">TIME: 60s</div>
            <div class="card">
                <p id="q" style="font-size: 1.1rem; line-height: 1.4;"></p>
                <div id="ops"></div>
            </div>
        </div>
    </div>

    <script>
        const qList = {json_data};
        let c = 0, t = 60, timer;

        function startEngine() {{
            document.getElementById('safety-page').style.display = 'none';
            document.getElementById('game-ui').style.display = 'block';
            show();
            timer = setInterval(() => {{
                t--; document.getElementById('t').innerText = "TIME: " + t + "s";
                if(t <= 0) {{ clearInterval(timer); alert("⌛ Diagnostic Timeout! Keep studying."); location.reload(); }}
            }}, 1000);
        }}

        function show() {{
            if(c >= qList.length) {{ 
                clearInterval(timer); 
                document.getElementById('app').innerHTML = "<h1>🎓 A6 MASTERED!</h1><p>You are ready for the shop floor.</p><button class='start-btn' onclick='location.reload()'>RESTART BUNDLE</button>"; 
                return; 
            }}
            const item = qList[c];
            document.getElementById('q').innerText = item.q;
            const oDiv = document.getElementById('ops'); oDiv.innerHTML = "";
            item.options.forEach(o => {{
                const b = document.createElement('button');
                b.className = "btn";
                b.innerText = o;
                b.onclick = () => {{ 
                    if(o === item.a) {{ 
                        alert("✅ CORRECT\\n\\n" + item.explanation);
                        c++; show(); 
                    }} else {{ 
                        t -= 10; 
                        alert("❌ INCORRECT\\n\\n" + item.explanation);
                        b.style.borderColor = "#ff4757";
                    }} 
                }};
                oDiv.appendChild(b);
            }});
        }}
    </script>
</body>
</html>"""
    return html_content

# --- MANUFACTURING RUN ---
if os.path.exists('factory_output'): shutil.rmtree('factory_output')
os.makedirs('factory_output')

# Building the A6 Level 1 using the imported questions
html = build_a6_game("A6 Electrical: Logic & Diagnostics", a6_level_1)

with open("factory_output/a6_electrical_v1.html", "w") as f:
    f.write(html)

shutil.make_archive('A6_Master_Study_Pack', 'zip', 'factory_output')
print("\\n🚀 FACTORY ONLINE: A6_Master_Study_Pack.zip has been manufactured!")
