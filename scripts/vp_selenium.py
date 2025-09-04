#!/usr/bin/env python3

import sys
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

# Register cleanup function
atexit.register(cleanup)

def analyze_command(target_profile: str):
    """Analyze profile using Selenium"""
    global scraper
    
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🔍 Analisando perfil: @{target_username}", style="bold blue")
    
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
    
    # Login
    console.print("🔐 Fazendo login...", style="cyan")
    if not scraper.login("viespolitico", "r@FRzo8FGeg@4pr4"):
        console.print("❌ Falha na autenticação", style="red")
        return
    
    # Get followings
    console.print("📥 Coletando lista de seguidos...", style="cyan")
    
    cached_followings = cache.get_followings(target_username)
    if cached_followings:
        followings = cached_followings
        console.print("📋 Usando lista de seguidos em cache", style="yellow")
    else:
        followings = scraper.get_user_followings(target_username, 500)  # Limit for testing
        if followings:
            cache.set_followings(target_username, followings)
        else:
            console.print("❌ Não foi possível obter lista de seguidos", style="red")
            return
    
    console.print(f"✅ Encontrados {len(followings)} perfis seguidos", style="green")
    
    # Calculate score
    console.print("🧮 Calculando score político...", style="cyan")
    results = scorer.calculate_score(followings, {})  # No liked posts for now
    
    # Cache results
    cache.set_analysis(target_username, results)
    
    # Display results
    scorer.display_results(target_username, results)

def main():
    if len(sys.argv) < 2:
        console.print("Uso:", style="bold")
        console.print("  python vp_selenium.py @perfil")
        console.print("\nExemplo:")
        console.print("  python vp_selenium.py @barbarastudart")
        console.print("\n⚠️  Este modo abre um navegador Chrome e é mais lento")
        console.print("💡 Certifique-se de ter o Chrome instalado")
        return
    
    profile = sys.argv[1]
    
    try:
        analyze_command(profile)
    except KeyboardInterrupt:
        console.print("\n🛑 Interrompido pelo usuário", style="yellow")
    except Exception as e:
        console.print(f"\n❌ Erro: {e}", style="red")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
