#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv
from rich.console import Console

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.auth import InstagramAuth
from core.cache import Cache
from core.instagram import InstagramScraper
from core.scoring import PoliticalScorer

# Load environment variables
load_dotenv()

console = Console()

def login_command(username, password):
    """Login to Instagram and save session"""
    auth = InstagramAuth()
        
    success = auth.login(username, password)
    if success:
        console.print("✅ Login realizado com sucesso!", style="green")
    else:
        console.print("❌ Falha no login", style="red")
        return False
    return True

def analyze_command(profile):
    """Analyze political inclination of an Instagram profile"""
    
    # Clean profile name
    target_username = profile.replace('@', '').lower()
    
    console.print(f"🔍 Analisando perfil: @{target_username}", style="bold blue")
    
    # Initialize components
    auth = InstagramAuth()
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    
    # Check for cached results first
    cached_result = cache.get_analysis(target_username)
    if cached_result:
        console.print("📋 Usando resultado em cache", style="yellow")
        scorer.display_results(target_username, cached_result)
        return
    
    # Login
    if not auth.login():
        console.print("❌ Falha na autenticação", style="red")
        return
        
    client = auth.get_client()
    scraper = InstagramScraper(client, request_delay=2)
    
    # Check if profile is public
    if not scraper.is_profile_public(target_username):
        console.print(f"❌ Perfil @{target_username} é privado ou não existe", style="red")
        return
        
    # Get followings
    console.print("📥 Coletando lista de seguidos...", style="cyan")
    
    followings = cache.get_followings(target_username)
        
    if not followings:
        followings = scraper.get_user_followings(target_username, 1000)  # Limit for testing
        if followings:
            cache.set_followings(target_username, followings)
        else:
            console.print("❌ Não foi possível obter lista de seguidos", style="red")
            return
    else:
        console.print("📋 Usando lista de seguidos em cache", style="yellow")
        
    console.print(f"✅ Encontrados {len(followings)} perfis seguidos", style="green")
    
    # Simple analysis - just check followings for now
    console.print("🧮 Calculando score político...", style="cyan")
    results = scorer.calculate_score(followings, {})  # Empty liked_posts for now
    
    # Cache results
    cache.set_analysis(target_username, results)
    
    # Display results
    scorer.display_results(target_username, results)

def main():
    if len(sys.argv) < 2:
        console.print("Uso:", style="bold")
        console.print("  python vp_simple.py login usuario senha")
        console.print("  python vp_simple.py analyze @perfil")
        return
    
    command = sys.argv[1]
    
    if command == "login":
        if len(sys.argv) < 4:
            console.print("❌ Uso: python vp_simple.py login usuario senha", style="red")
            return
        username = sys.argv[2]
        password = sys.argv[3]
        login_command(username, password)
    elif command == "analyze":
        if len(sys.argv) < 3:
            console.print("❌ Especifique o perfil: python vp_simple.py analyze @perfil", style="red")
            return
        profile = sys.argv[2]
        analyze_command(profile)
    else:
        console.print(f"❌ Comando desconhecido: {command}", style="red")

if __name__ == "__main__":
    main()
