#!/usr/bin/env python3

import sys
from rich.console import Console
from core.scoring import PoliticalScorer

console = Console()

def analyze_manual(target_profile, followings_list):
    """Analyze profile using manually provided followings list"""
    
    console.print(f"🔍 Análise Manual: @{target_profile}", style="bold blue")
    
    # Initialize scorer
    scorer = PoliticalScorer()
    
    # Parse followings list
    if isinstance(followings_list, str):
        followings = [f.strip().replace('@', '').lower() for f in followings_list.split(',')]
    else:
        followings = followings_list
    
    console.print(f"📥 Analisando {len(followings)} perfis seguidos", style="cyan")
    
    # For now, just analyze followings (no liked posts)
    console.print("🧮 Calculando score político...", style="cyan")
    results = scorer.calculate_score(followings, {})
    
    # Display results
    scorer.display_results(target_profile, results)
    
    return results

def main():
    if len(sys.argv) < 3:
        console.print("Uso:", style="bold")
        console.print("  python vp_manual.py @perfil 'user1,user2,user3'")
        console.print("  python vp_manual.py @perfil --file followings.txt")
        console.print("\nExemplo:")
        console.print("  python vp_manual.py @perfilalvo 'lulaoficial,jairmessiasbolsonaro,simonetebet'")
        return
    
    target = sys.argv[1].replace('@', '')
    
    if sys.argv[2] == '--file':
        # Read from file
        if len(sys.argv) < 4:
            console.print("❌ Especifique o arquivo: --file followings.txt", style="red")
            return
        
        try:
            with open(sys.argv[3], 'r') as f:
                followings_text = f.read()
        except FileNotFoundError:
            console.print(f"❌ Arquivo não encontrado: {sys.argv[3]}", style="red")
            return
    else:
        # Read from command line
        followings_text = sys.argv[2]
    
    analyze_manual(target, followings_text)

if __name__ == "__main__":
    main()
