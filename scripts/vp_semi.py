#!/usr/bin/env python3

import sys
import time
import atexit
from rich.console import Console
from core.selenium_scraper import SeleniumInstagramScraper
from core.scoring import PoliticalScorer
from core.cache import Cache

console = Console()
scraper = None

def cleanup():
    """Cleanup function to close browser"""
    global scraper
    if scraper:
        scraper.close()

atexit.register(cleanup)

def analyze_semi_auto(target_profile: str):
    """Semi-automatic analysis with targeted search"""
    global scraper
    
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🔍 Análise Semi-Automática: @{target_username}", style="bold blue")
    
    # Initialize components
    scraper = SeleniumInstagramScraper()
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    
    # Check cache first
    cached_result = cache.get_analysis(target_username)
    if cached_result:
        console.print("📋 Usando resultado em cache", style="yellow")
        scorer.display_results(target_username, cached_result)
        return
    
    # Setup browser
    if not scraper._setup_driver():
        return
        
    console.print("🌐 Abrindo Instagram...", style="cyan")
    scraper.driver.get("https://www.instagram.com/accounts/login/")
    
    console.print("👤 FAÇA LOGIN MANUALMENTE no navegador que abriu", style="bold yellow")
    console.print("⏳ Pressione ENTER aqui quando estiver logado...", style="yellow")
    
    input()  # Wait for user to login manually
    
    # Check if logged in
    try:
        scraper.driver.get("https://www.instagram.com/")
        time.sleep(3)
        
        if "login" not in scraper.driver.current_url:
            console.print("✅ Login detectado!", style="green")
            scraper.logged_in = True
        else:
            console.print("❌ Login não detectado", style="red")
            return
            
    except Exception as e:
        console.print(f"❌ Erro verificando login: {e}", style="red")
        return
    
    # Get seed profiles list
    seed_profiles = list(scorer.seed_profiles.keys())
    console.print(f"📋 Procurando por {len(seed_profiles)} perfis semente", style="cyan")
    
    # Search for seed profiles in target's following list
    console.print("🔍 Fazendo busca direcionada...", style="cyan")
    
    cached_followings = cache.get_followings(target_username)
    if cached_followings:
        followings = cached_followings
        console.print("📋 Usando lista de seguidos em cache", style="yellow")
    else:
        followings = scraper.get_user_followings_by_search(target_username, seed_profiles)
        if followings:
            cache.set_followings(target_username, followings)
        else:
            console.print("❌ Não foi possível obter lista de seguidos", style="red")
            return
    
    console.print(f"✅ Encontrados {len(followings)} matches com perfis semente", style="green")
    
    # Calculate score
    console.print("🧮 Calculando score político...", style="cyan")
    results = scorer.calculate_score(followings, {})
    
    # Cache results
    cache.set_analysis(target_username, results)
    
    # Display results
    scorer.display_results(target_username, results)
    
    console.print("\n✅ Análise concluída! Pressione ENTER para fechar o navegador...", style="green")
    input()

def main():
    if len(sys.argv) < 2:
        console.print("Uso:", style="bold")
        console.print("  python vp_semi.py @perfil")
        console.print("\nExemplo:")
        console.print("  python vp_semi.py @perfilalvo")
        console.print("\n📋 Como funciona:")
        console.print("1. Abre o Chrome no Instagram")
        console.print("2. Você faz login manualmente")
        console.print("3. Sistema busca especificamente pelos perfis semente")
        console.print("4. Muito mais eficiente que scroll infinito!")
        return
    
    profile = sys.argv[1]
    
    try:
        analyze_semi_auto(profile)
    except KeyboardInterrupt:
        console.print("\n🛑 Interrompido pelo usuário", style="yellow")
    except Exception as e:
        console.print(f"\n❌ Erro: {e}", style="red")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
