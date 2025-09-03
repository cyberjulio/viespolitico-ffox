#!/usr/bin/env python3

import os
import sys
from rich.console import Console

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.scoring import PoliticalScorer

console = Console()

def test_analysis():
    """Test the scoring system with simulated data"""
    
    console.print("🧪 Modo de Teste - Simulando análise política", style="bold blue")
    
    # Initialize scorer
    scorer = PoliticalScorer()
    
    # Simulate different test cases
    test_cases = [
        {
            "name": "Perfil de Esquerda",
            "followings": ["lulaoficial", "pstu_oficial", "gleisi", "boulos", "manuela"],
            "liked_posts": {"lulaoficial": ["post1", "post2"]},
            "expected": "Esquerda"
        },
        {
            "name": "Perfil de Direita", 
            "followings": ["jairmessiasbolsonaro", "eduardoleite", "nikolas_dm", "carlosjordy"],
            "liked_posts": {"jairmessiasbolsonaro": ["post1"]},
            "expected": "Direita/Extrema Direita"
        },
        {
            "name": "Perfil Centro",
            "followings": ["simonetebet", "rodrigomaia", "aecio", "marina_silva"],
            "liked_posts": {},
            "expected": "Centro"
        },
        {
            "name": "Perfil Misto",
            "followings": ["lulaoficial", "jairmessiasbolsonaro", "simonetebet"],
            "liked_posts": {},
            "expected": "Centro (balanceado)"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        console.print(f"\n{'='*50}")
        console.print(f"🧪 Teste {i}: {test_case['name']}", style="bold yellow")
        console.print(f"Expectativa: {test_case['expected']}", style="dim")
        
        # Calculate score
        results = scorer.calculate_score(test_case["followings"], test_case["liked_posts"])
        
        # Display results
        scorer.display_results(f"teste_{i}", results)
        
        console.print(f"✅ Teste concluído", style="green")

def test_seed_loading():
    """Test if seed profiles are loading correctly"""
    console.print("🧪 Testando carregamento de perfis semente", style="bold blue")
    
    scorer = PoliticalScorer()
    
    console.print(f"✅ Carregados {len(scorer.seed_profiles)} perfis semente:", style="green")
    for handle, data in scorer.seed_profiles.items():
        console.print(f"  @{handle}: {data['score']} ({data['category']})")
    
    console.print(f"\n✅ Carregados {len(scorer.seed_posts)} posts semente:", style="green")
    for url, data in scorer.seed_posts.items():
        console.print(f"  {url}: {data['score']} ({data['category']})")

def main():
    if len(sys.argv) < 2:
        console.print("Uso:", style="bold")
        console.print("  python vp_test.py seeds    # Testar carregamento de perfis")
        console.print("  python vp_test.py analysis # Testar análise com dados simulados")
        return
    
    command = sys.argv[1]
    
    if command == "seeds":
        test_seed_loading()
    elif command == "analysis":
        test_analysis()
    else:
        console.print(f"❌ Comando desconhecido: {command}", style="red")

if __name__ == "__main__":
    main()
