#!/usr/bin/env python3

import sys
import time
import random
from rich.console import Console
from core.scoring import PoliticalScorer
from core.cache import Cache

console = Console()

def analyze_auto(target_profile: str):
    """Fully automatic analysis with robust login"""
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🤖 Análise Automática: @{target_username}", style="bold blue")
    
    # Initialize components
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    
    # Check cache first
    cached_result = cache.get_analysis(target_username)
    if cached_result:
        console.print("📋 Usando resultado em cache", style="yellow")
        scorer.display_results(target_username, cached_result)
        return
    
    try:
        # Use Playwright MCP for robust automation
        console.print("🚀 Iniciando automação com Playwright...", style="cyan")
        
        # Create new browser context with anti-detection
        browser_result = playwright___create_browser_context({
            "headless": False,
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "viewport": {"width": 1366, "height": 768},
            "locale": "pt-BR",
            "timezone_id": "America/Sao_Paulo"
        })
        
        if not browser_result.get("success"):
            console.print("❌ Erro ao criar contexto do navegador", style="red")
            return
            
        # Navigate to Instagram login
        console.print("🌐 Navegando para Instagram...", style="cyan")
        nav_result = playwright___navigate({
            "url": "https://www.instagram.com/accounts/login/",
            "wait_until": "networkidle"
        })
        
        if not nav_result.get("success"):
            console.print("❌ Erro ao navegar para Instagram", style="red")
            return
            
        # Wait for page to load and add human-like delay
        time.sleep(random.uniform(2, 4))
        
        # Perform login with anti-detection measures
        console.print("🔐 Fazendo login...", style="cyan")
        
        # Fill username with human-like typing
        username_result = playwright___fill_element({
            "selector": "input[name='username']",
            "text": "viespolitico",
            "delay": random.randint(50, 150)  # Random typing delay
        })
        
        if not username_result.get("success"):
            console.print("❌ Erro ao preencher usuário", style="red")
            return
            
        # Small delay between fields
        time.sleep(random.uniform(0.5, 1.5))
        
        # Fill password with human-like typing
        password_result = playwright___fill_element({
            "selector": "input[name='password']",
            "text": "r@FRzo8FGeg@4pr4",
            "delay": random.randint(50, 150)
        })
        
        if not password_result.get("success"):
            console.print("❌ Erro ao preencher senha", style="red")
            return
            
        # Human-like delay before clicking login
        time.sleep(random.uniform(1, 2))
        
        # Click login button
        login_result = playwright___click_element({
            "selector": "button[type='submit']"
        })
        
        if not login_result.get("success"):
            console.print("❌ Erro ao clicar em login", style="red")
            return
            
        # Wait for login to complete
        console.print("⏳ Aguardando login...", style="yellow")
        time.sleep(random.uniform(3, 5))
        
        # Check if login was successful by looking for home page elements
        home_check = playwright___wait_for_element({
            "selector": "a[href='/']",
            "timeout": 10000
        })
        
        if not home_check.get("success"):
            console.print("❌ Login falhou - verificação manual necessária", style="red")
            return
            
        console.print("✅ Login realizado com sucesso!", style="green")
        
        # Navigate to target profile
        console.print(f"👤 Navegando para @{target_username}...", style="cyan")
        profile_result = playwright___navigate({
            "url": f"https://www.instagram.com/{target_username}/",
            "wait_until": "networkidle"
        })
        
        if not profile_result.get("success"):
            console.print("❌ Erro ao navegar para perfil", style="red")
            return
            
        # Wait for profile to load
        time.sleep(random.uniform(2, 3))
        
        # Click on following count to open modal
        console.print("📋 Abrindo lista de seguidos...", style="cyan")
        following_result = playwright___click_element({
            "selector": "a[href*='/following/']"
        })
        
        if not following_result.get("success"):
            console.print("❌ Erro ao abrir lista de seguidos", style="red")
            return
            
        # Wait for modal to open
        time.sleep(random.uniform(2, 3))
        
        # Find search box in modal
        search_box_result = playwright___wait_for_element({
            "selector": "input[placeholder*='Pesquisar']",
            "timeout": 5000
        })
        
        if not search_box_result.get("success"):
            console.print("❌ Caixa de pesquisa não encontrada", style="red")
            return
            
        console.print("🔍 Iniciando busca direcionada...", style="cyan")
        
        # Load seed profiles
        import json
        with open('data/seed_profiles.json', 'r', encoding='utf-8') as f:
            seed_profiles = json.load(f)
        
        matches = []
        total_profiles = len(seed_profiles)
        
        for i, profile in enumerate(seed_profiles, 1):
            username = profile['username']
            score = profile['score']
            
            console.print(f"🔍 [{i}/{total_profiles}] Testando @{username}...", style="dim")
            
            # Clear search box
            clear_result = playwright___fill_element({
                "selector": "input[placeholder*='Pesquisar']",
                "text": "",
                "clear": True
            })
            
            # Search for specific profile
            search_result = playwright___fill_element({
                "selector": "input[placeholder*='Pesquisar']",
                "text": username,
                "delay": random.randint(30, 80)
            })
            
            if not search_result.get("success"):
                continue
                
            # Wait for search results
            time.sleep(random.uniform(1, 2))
            
            # Check if profile appears in results
            result_check = playwright___wait_for_element({
                "selector": f"a[href='/{username}/']",
                "timeout": 2000
            })
            
            if result_check.get("success"):
                matches.append({
                    'username': username,
                    'score': score,
                    'category': profile.get('category', 'Unknown')
                })
                console.print(f"✅ Match: @{username} (score: {score})", style="green")
            
            # Small delay between searches
            time.sleep(random.uniform(0.5, 1))
        
        # Calculate and display results
        if matches:
            final_score = sum(match['score'] for match in matches) / len(matches)
            
            # Cache results
            cache.store_analysis(target_username, {
                'matches': matches,
                'final_score': final_score,
                'total_matches': len(matches)
            })
            
            # Display results
            scorer.display_results(target_username, {
                'matches': matches,
                'final_score': final_score,
                'total_matches': len(matches)
            })
        else:
            console.print("❌ Nenhum match encontrado", style="red")
            
    except Exception as e:
        console.print(f"❌ Erro durante análise: {str(e)}", style="red")
    finally:
        # Close browser
        try:
            playwright___close_browser()
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Uso: python vp_auto.py @perfil", style="red")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('@'):
        target = f"@{target}"
    
    analyze_auto(target)
