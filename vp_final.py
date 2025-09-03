#!/usr/bin/env python3

import sys
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from rich.console import Console
from core.scoring import PoliticalScorer
from core.cache import Cache

console = Console()

def analyze_final(target_profile: str):
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🎯 ViesPolítico Final: @{target_username}", style="bold blue")
    
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    
    # Cache check
    cached_result = cache.get_analysis(target_username)
    if cached_result:
        console.print("📋 Resultado em cache", style="yellow")
        scorer.display_results(target_username, cached_result)
        return
    
    # Setup Chrome simples
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        console.print("🌐 Abrindo Instagram...", style="cyan")
        driver.get("https://www.instagram.com/accounts/login/")
        
        console.print("=" * 60, style="yellow")
        console.print("👤 FAÇA LOGIN MANUALMENTE", style="bold yellow")
        console.print("📱 Complete 2FA se necessário", style="yellow")
        console.print("🏠 Aguarde chegar na página inicial", style="yellow")
        console.print("=" * 60, style="yellow")
        
        input("⏳ Pressione ENTER quando estiver logado...")
        
        # Ir para perfil
        console.print(f"👤 Navegando para @{target_username}...", style="cyan")
        driver.get(f"https://www.instagram.com/{target_username}/")
        time.sleep(3)
        
        if "Page Not Found" in driver.page_source:
            console.print(f"❌ @{target_username} não existe", style="red")
            return
        
        # Abrir seguidos
        console.print("📋 Clique no número de SEGUIDOS no perfil", style="yellow")
        input("⏳ Pressione ENTER quando o modal de seguidos abrir...")
        
        # Buscar perfis
        try:
            search_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder]"))
            )
            
            console.print("🔍 Iniciando busca automática...", style="cyan")
            
            with open('data/seed_profiles.json', 'r', encoding='utf-8') as f:
                seed_profiles = json.load(f)
            
            matches = []
            total = len(seed_profiles)
            
            for i, profile in enumerate(seed_profiles, 1):
                username = profile['username']
                score = profile['score']
                
                console.print(f"[{i}/{total}] @{username}...", style="dim")
                
                try:
                    # Limpar e digitar
                    search_box.clear()
                    time.sleep(0.2)
                    search_box.send_keys(username)
                    time.sleep(1)
                    
                    # Verificar resultado
                    try:
                        result = WebDriverWait(driver, 2).until(
                            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/{username}/')]"))
                        )
                        
                        if result.is_displayed():
                            matches.append({
                                'username': username,
                                'score': score,
                                'category': profile.get('category', 'Unknown')
                            })
                            console.print(f"✅ @{username} (score: {score})", style="green")
                    except:
                        pass
                    
                    time.sleep(random.uniform(0.3, 0.7))
                    
                except Exception as e:
                    console.print(f"⚠️ Erro @{username}", style="dim")
                    continue
            
            # Resultados
            if matches:
                final_score = sum(match['score'] for match in matches) / len(matches)
                
                result_data = {
                    'matches': matches,
                    'final_score': final_score,
                    'total_matches': len(matches)
                }
                
                cache.store_analysis(target_username, result_data)
                scorer.display_results(target_username, result_data)
            else:
                console.print("❌ Nenhum match encontrado", style="red")
                
        except Exception as e:
            console.print(f"❌ Erro na busca: {str(e)}", style="red")
            
    except Exception as e:
        console.print(f"❌ Erro: {str(e)}", style="red")
    finally:
        if driver:
            input("Pressione ENTER para fechar...")
            driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Uso: python vp_final.py @perfil", style="red")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('@'):
        target = f"@{target}"
    
    analyze_final(target)
