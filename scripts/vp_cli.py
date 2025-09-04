#!/usr/bin/env python3

import os
import typer
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from core.auth import InstagramAuth
from core.cache import Cache
from core.instagram import InstagramScraper
from core.scoring import PoliticalScorer

# Load environment variables
load_dotenv()

app = typer.Typer(help="ViesPolítico - Análise de inclinação política no Instagram")
console = Console()

@app.command()
def login(username: str = None, password: str = None):
    """Login to Instagram and save session"""
    auth = InstagramAuth()
    
    if not username:
        username = os.getenv('INSTAGRAM_USERNAME')
    if not password:
        password = os.getenv('INSTAGRAM_PASSWORD')
        
    success = auth.login(username, password)
    if success:
        console.print("✅ Login realizado com sucesso!", style="green")
    else:
        console.print("❌ Falha no login", style="red")
        raise typer.Exit(1)

@app.command()
def analyze(profile: str, max_followings: int = 5000, max_posts: int = 10, force_refresh: bool = False):
    """Analyze political inclination of an Instagram profile"""
    
    # Clean profile name
    target_username = profile.replace('@', '').lower()
    
    console.print(f"🔍 Analisando perfil: @{target_username}", style="bold blue")
    
    # Initialize components
    auth = InstagramAuth()
    cache = Cache(cache_duration_hours=int(os.getenv('CACHE_DURATION', 24)))
    scorer = PoliticalScorer()
    
    # Check for cached results first
    if not force_refresh:
        cached_result = cache.get_analysis(target_username)
        if cached_result:
            console.print("📋 Usando resultado em cache", style="yellow")
            scorer.display_results(target_username, cached_result)
            return
    
    # Login
    if not auth.login():
        console.print("❌ Falha na autenticação", style="red")
        raise typer.Exit(1)
        
    client = auth.get_client()
    scraper = InstagramScraper(client, request_delay=int(os.getenv('REQUEST_DELAY', 2)))
    
    # Check if profile is public
    if not scraper.is_profile_public(target_username):
        console.print(f"❌ Perfil @{target_username} é privado ou não existe", style="red")
        raise typer.Exit(1)
        
    # Get followings
    console.print("📥 Coletando lista de seguidos...", style="cyan")
    
    if not force_refresh:
        followings = cache.get_followings(target_username)
    else:
        followings = None
        
    if not followings:
        followings = scraper.get_user_followings(target_username, max_followings)
        if followings:
            cache.set_followings(target_username, followings)
        else:
            console.print("❌ Não foi possível obter lista de seguidos", style="red")
            raise typer.Exit(1)
    else:
        console.print("📋 Usando lista de seguidos em cache", style="yellow")
        
    console.print(f"✅ Encontrados {len(followings)} perfis seguidos", style="green")
    
    # Analyze liked posts for seed profiles
    console.print("❤️ Analisando curtidas em posts...", style="cyan")
    liked_posts = {}
    
    # Load seed profiles to check
    seed_profiles = list(scorer.seed_profiles.keys())
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Verificando curtidas...", total=len(seed_profiles))
        
        for seed_profile in seed_profiles:
            if seed_profile in [f.lower() for f in followings]:
                # Get recent posts from this seed profile
                if not force_refresh:
                    posts = cache.get_posts(seed_profile)
                else:
                    posts = None
                    
                if not posts:
                    posts = scraper.get_recent_posts(seed_profile, max_posts)
                    if posts:
                        cache.set_posts(seed_profile, posts)
                        
                # Check if target liked any of these posts
                if posts:
                    liked_post_urls = []
                    for post in posts:
                        if scraper.check_user_liked_post(post['id'], target_username):
                            liked_post_urls.append(post['url'])
                            
                    if liked_post_urls:
                        liked_posts[seed_profile] = liked_post_urls
                        
            progress.advance(task)
            
    # Calculate score
    console.print("🧮 Calculando score político...", style="cyan")
    results = scorer.calculate_score(followings, liked_posts)
    
    # Cache results
    cache.set_analysis(target_username, results)
    
    # Display results
    scorer.display_results(target_username, results)

@app.command()
def clear_cache():
    """Clear all cached data"""
    cache_file = Path("data/cache.db")
    if cache_file.exists():
        cache_file.unlink()
        console.print("✅ Cache limpo com sucesso", style="green")
    else:
        console.print("ℹ️ Nenhum cache encontrado", style="blue")

if __name__ == "__main__":
    app()
