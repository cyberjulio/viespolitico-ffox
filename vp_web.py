#!/usr/bin/env python3

import sys
from rich.console import Console
from core.web_scraper import WebInstagramScraper
from core.scoring import PoliticalScorer
from core.cache import Cache

console = Console()

def login_command(username: str, password: str):
    """Login using web scraping"""
    scraper = WebInstagramScraper()
    success = scraper.login(username, password)
    
    if success:
        console.print("✅ Login realizado com sucesso!", style="green")
        # Save scraper instance for later use (in a real app, you'd persist this)
        return scraper
    else:
        console.print("❌ Falha no login", style="red")
        return None

def analyze_command(target_profile: str):
    """Analyze profile using web scraping"""
    
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🔍 Analisando perfil: @{target_username}", style="bold blue")
    
    # Initialize components
    scraper = WebInstagramScraper()
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
        followings = scraper.get_user_followings(target_username, 1000)
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
        console.print("  python vp_web.py login")
        console.print("  python vp_web.py analyze @perfil")
        return
    
    command = sys.argv[1]
    
    if command == "login":
        login_command("viespolitico", "r@FRzo8FGeg@4pr4")
    elif command == "analyze":
        if len(sys.argv) < 3:
            console.print("❌ Especifique o perfil: python vp_web.py analyze @perfil", style="red")
            return
        profile = sys.argv[2]
        analyze_command(profile)
    else:
        console.print(f"❌ Comando desconhecido: {command}", style="red")

if __name__ == "__main__":
    main()
