import json
from pathlib import Path
from typing import Dict, List, Tuple
from rich.console import Console
from rich.table import Table

console = Console()

class PoliticalScorer:
    def __init__(self):
        self.seed_profiles = {}
        self.seed_posts = {}
        self.load_seed_data()
        
    def load_seed_data(self):
        """Load seed profiles and posts from JSON file"""
        seed_file = Path("data/seed_profiles.json")
        
        if not seed_file.exists():
            console.print("❌ Seed profiles file not found!", style="red")
            return
            
        try:
            with open(seed_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Load profiles
            for profile in data.get('profiles', []):
                handle = profile['handle'].replace('@', '').lower()
                self.seed_profiles[handle] = {
                    'score': profile['score'],
                    'category': profile['category'],
                    'description': profile.get('description', '')
                }
                
            # Load posts
            for post in data.get('posts', []):
                self.seed_posts[post['url']] = {
                    'score': post['score'],
                    'category': post['category'],
                    'description': post.get('description', '')
                }
                
            console.print(f"✅ Loaded {len(self.seed_profiles)} seed profiles and {len(self.seed_posts)} seed posts", style="green")
            
        except Exception as e:
            console.print(f"❌ Error loading seed data: {e}", style="red")
            
    def calculate_score(self, followings: List[str], liked_posts: Dict[str, List[str]]) -> Dict:
        """Calculate political score based on followings and liked posts"""
        
        total_weight = 0
        weighted_score = 0
        evidence = []
        
        # Process followings (weight = 1.0)
        following_matches = 0
        for following in followings:
            following_clean = following.lower()
            if following_clean in self.seed_profiles:
                seed_data = self.seed_profiles[following_clean]
                weight = 1.0
                contribution = seed_data['score'] * weight
                
                total_weight += weight
                weighted_score += contribution
                following_matches += 1
                
                evidence.append({
                    'type': 'following',
                    'handle': following,
                    'score': seed_data['score'],
                    'category': seed_data['category'],
                    'weight': weight,
                    'contribution': contribution
                })
                
        # Process liked posts (additional weight = +2.0)
        liked_matches = 0
        for profile_handle, posts in liked_posts.items():
            profile_clean = profile_handle.lower()
            if profile_clean in self.seed_profiles:
                seed_data = self.seed_profiles[profile_clean]
                
                for post_url in posts:
                    # Additional weight for liking posts from seed profiles
                    weight = 2.0
                    contribution = seed_data['score'] * weight
                    
                    total_weight += weight
                    weighted_score += contribution
                    liked_matches += 1
                    
                    evidence.append({
                        'type': 'liked_post',
                        'handle': profile_handle,
                        'post_url': post_url,
                        'score': seed_data['score'],
                        'category': seed_data['category'],
                        'weight': weight,
                        'contribution': contribution
                    })
                    
        # Calculate final score
        if total_weight == 0:
            final_score = 0
            category = "Indeterminado"
            confidence = 0
        else:
            final_score = weighted_score / total_weight
            category = self._score_to_category(final_score)
            confidence = min(100, (following_matches + liked_matches) * 5)  # Rough confidence metric
            
        # Sort evidence by absolute contribution
        evidence.sort(key=lambda x: abs(x['contribution']), reverse=True)
        
        return {
            'final_score': round(final_score, 3),
            'category': category,
            'confidence': confidence,
            'following_matches': following_matches,
            'liked_matches': liked_matches,
            'total_signals': following_matches + liked_matches,
            'evidence': evidence[:10]  # Top 10 evidence pieces
        }
        
    def _score_to_category(self, score: float) -> str:
        """Convert numerical score to political category"""
        if score <= -1.5:
            return "Extrema Esquerda"
        elif score <= -0.5:
            return "Esquerda"
        elif score <= 0.5:
            return "Centro"
        elif score <= 1.5:
            return "Direita"
        else:
            return "Extrema Direita"
            
    def display_results(self, username: str, results: Dict):
        """Display analysis results in a formatted table"""
        
        # Main results
        console.print(f"\n🎯 Análise Política: @{username}", style="bold blue")
        console.print("=" * 50)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="white")
        
        table.add_row("Score Final", f"{results['final_score']}")
        table.add_row("Categoria", f"{results['category']}")
        table.add_row("Confiança", f"{results['confidence']}%")
        table.add_row("Perfis Seguidos", f"{results['following_matches']}")
        table.add_row("Posts Curtidos", f"{results['liked_matches']}")
        table.add_row("Total de Sinais", f"{results['total_signals']}")
        
        console.print(table)
        
        # Evidence table
        if results['evidence']:
            console.print("\n📊 Principais Evidências:", style="bold yellow")
            
            evidence_table = Table(show_header=True, header_style="bold magenta")
            evidence_table.add_column("Tipo", style="cyan")
            evidence_table.add_column("Perfil", style="white")
            evidence_table.add_column("Categoria", style="green")
            evidence_table.add_column("Score", style="red")
            evidence_table.add_column("Peso", style="blue")
            evidence_table.add_column("Contribuição", style="yellow")
            
            for evidence in results['evidence']:
                evidence_table.add_row(
                    "Seguindo" if evidence['type'] == 'following' else "Curtiu",
                    f"@{evidence['handle']}",
                    evidence['category'],
                    str(evidence['score']),
                    str(evidence['weight']),
                    f"{evidence['contribution']:.2f}"
                )
                
            console.print(evidence_table)
