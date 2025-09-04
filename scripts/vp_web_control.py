#!/usr/bin/env python3

import sys
import json
import time
import webbrowser
from flask import Flask, render_template, request, jsonify
from threading import Thread
from rich.console import Console
from core.scoring import PoliticalScorer
from core.cache import Cache

console = Console()
app = Flask(__name__)

class WebController:
    def __init__(self):
        self.results = []
        self.status = "waiting"
        self.target_username = ""
        
    def set_target(self, username):
        self.target_username = username
        self.results = []
        self.status = "ready"

web_controller = WebController()

@app.route('/')
def index():
    return render_template('control.html', 
                         target=web_controller.target_username,
                         seed_profiles=get_seed_profiles())

@app.route('/api/status')
def get_status():
    return jsonify({
        'status': web_controller.status,
        'target': web_controller.target_username,
        'results_count': len(web_controller.results)
    })

@app.route('/api/result', methods=['POST'])
def receive_result():
    data = request.json
    web_controller.results.append(data)
    console.print(f"✅ Match: @{data['username']} (score: {data['score']})", style="green")
    return jsonify({'success': True})

@app.route('/api/complete', methods=['POST'])
def analysis_complete():
    web_controller.status = "complete"
    
    if web_controller.results:
        # Calcular e salvar resultados
        final_score = sum(r['score'] for r in web_controller.results) / len(web_controller.results)
        
        result_data = {
            'matches': web_controller.results,
            'final_score': final_score,
            'total_matches': len(web_controller.results)
        }
        
        # Cache
        cache = Cache(cache_duration_hours=24)
        cache.store_analysis(web_controller.target_username, result_data)
        
        # Display
        scorer = PoliticalScorer()
        scorer.display_results(web_controller.target_username, result_data)
    else:
        console.print("❌ Nenhum match encontrado", style="red")
    
    return jsonify({'success': True})

def get_seed_profiles():
    with open('data/seed_profiles.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def run_server():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def analyze_web(target_profile: str):
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🌐 Análise Web: @{target_username}", style="bold blue")
    
    # Check cache
    cache = Cache(cache_duration_hours=24)
    cached_result = cache.get_analysis(target_username)
    if cached_result:
        console.print("📋 Resultado em cache", style="yellow")
        scorer = PoliticalScorer()
        scorer.display_results(target_username, cached_result)
        return
    
    # Setup web controller
    web_controller.set_target(target_username)
    
    # Start server in background
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    time.sleep(1)  # Wait for server to start
    
    # Open browser
    url = "http://127.0.0.1:5000"
    console.print(f"🌐 Abrindo {url} no Firefox...", style="cyan")
    webbrowser.open(url)
    
    console.print("=" * 60, style="yellow")
    console.print("🦊 CONTROLE WEB ATIVO", style="bold yellow")
    console.print("1. Faça login no Instagram na aba que abriu", style="yellow")
    console.print("2. Siga as instruções na página web", style="yellow")
    console.print("3. A análise será automática", style="yellow")
    console.print("=" * 60, style="yellow")
    
    # Wait for completion
    while web_controller.status != "complete":
        time.sleep(1)
    
    console.print("✅ Análise concluída!", style="green")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Uso: python vp_web_control.py @perfil", style="red")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('@'):
        target = f"@{target}"
    
    analyze_web(target)
