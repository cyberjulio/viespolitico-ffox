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

class HybridInstagramScraper:
    def __init__(self):
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome driver with advanced anti-detection"""
        try:
            options = Options()
            
            # Advanced anti-detection options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Realistic user agent
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Window size and position
            options.add_argument("--window-size=1366,768")
            options.add_argument("--window-position=100,100")
            
            # Performance optimizations
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            
            # Create driver
            self.driver = webdriver.Chrome(options=options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set realistic timeouts
            self.driver.implicitly_wait(10)
            
            return True
            
        except Exception as e:
            console.print(f"❌ Erro ao configurar driver: {str(e)}", style="red")
            return False
    
    def manual_login_setup(self):
        """Setup for manual login with better UX"""
        try:
            console.print("🌐 Abrindo Instagram para login manual...", style="cyan")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(2)
            
            console.print("=" * 60, style="yellow")
            console.print("👤 FAÇA LOGIN MANUALMENTE no navegador que abriu", style="bold yellow")
            console.print("📱 Se aparecer verificação 2FA, complete também", style="yellow")
            console.print("🏠 Aguarde chegar na página inicial do Instagram", style="yellow")
            console.print("=" * 60, style="yellow")
            
            input("⏳ Pressione ENTER aqui quando estiver logado e na página inicial...")
            
            # Verify login was successful
            current_url = self.driver.current_url
            if "instagram.com" in current_url and "/accounts/login" not in current_url:
                console.print("✅ Login verificado com sucesso!", style="green")
                return True
            else:
                console.print("⚠️ Parece que ainda não está logado. Continuando mesmo assim...", style="yellow")
                return True
                
        except Exception as e:
            console.print(f"❌ Erro durante setup de login: {str(e)}", style="red")
            return False
    
    def navigate_to_profile(self, username):
        """Navigate to user profile with better error handling"""
        try:
            console.print(f"👤 Navegando para @{username}...", style="cyan")
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.uniform(2, 4))
            
            # Check for various error conditions
            page_source = self.driver.page_source.lower()
            
            if "page not found" in page_source or "this page isn't available" in page_source:
                console.print(f"❌ Perfil @{username} não encontrado", style="red")
                return False
            
            if "login" in self.driver.current_url:
                console.print("❌ Sessão expirou - faça login novamente", style="red")
                return False
            
            # Check if profile is private
            if "this account is private" in page_source or "esta conta é privada" in page_source:
                console.print(f"🔒 Perfil @{username} é privado", style="yellow")
                return False
            
            console.print(f"✅ Perfil @{username} carregado", style="green")
            return True
            
        except Exception as e:
            console.print(f"❌ Erro ao navegar para perfil: {str(e)}", style="red")
            return False
    
    def open_following_modal(self):
        """Open following modal with multiple robust strategies"""
        try:
            console.print("📋 Abrindo lista de seguidos...", style="cyan")
            
            # Wait a bit for page to fully load
            time.sleep(2)
            
            # Strategy 1: Look for following link by href
            strategies = [
                "//a[contains(@href, '/following/')]",
                "//*[contains(text(), 'following')]//ancestor::a",
                "//*[contains(text(), 'seguindo')]//ancestor::a",
                "//a[contains(@href, 'following')]",
                "//*[@role='link' and contains(text(), 'following')]",
                "//*[@role='link' and contains(text(), 'seguindo')]"
            ]
            
            for i, xpath in enumerate(strategies, 1):
                try:
                    console.print(f"🔍 Tentativa {i}: Procurando link de seguidos...", style="dim")
                    
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            console.print(f"✅ Encontrado! Clicando no link...", style="green")
                            
                            # Scroll to element first
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(1)
                            
                            # Try clicking
                            ActionChains(self.driver).move_to_element(element).click().perform()
                            time.sleep(3)
                            
                            # Check if modal opened
                            try:
                                WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder and (contains(@placeholder, 'Search') or contains(@placeholder, 'Pesquisar'))]"))
                                )
                                console.print("✅ Modal de seguidos aberto!", style="green")
                                return True
                            except:
                                console.print("⚠️ Modal não abriu, tentando próxima estratégia...", style="yellow")
                                continue
                                
                except Exception as e:
                    console.print(f"⚠️ Estratégia {i} falhou: {str(e)}", style="dim")
                    continue
            
            console.print("❌ Não foi possível abrir lista de seguidos", style="red")
            console.print("💡 Dica: Verifique se o perfil tem seguidos públicos", style="yellow")
            return False
            
        except Exception as e:
            console.print(f"❌ Erro ao abrir modal: {str(e)}", style="red")
            return False
    
    def search_in_following(self, seed_profiles):
        """Perform targeted search with enhanced error handling"""
        try:
            # Find search box with multiple strategies
            search_selectors = [
                "//input[@placeholder and (contains(@placeholder, 'Search') or contains(@placeholder, 'Pesquisar'))]",
                "//input[contains(@placeholder, 'Search')]",
                "//input[contains(@placeholder, 'Pesquisar')]",
                "//input[@type='text' and @placeholder]"
            ]
            
            search_box = None
            for selector in search_selectors:
                try:
                    search_box = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not search_box:
                console.print("❌ Caixa de pesquisa não encontrada", style="red")
                return []
            
            console.print("🔍 Iniciando busca direcionada...", style="cyan")
            
            matches = []
            total_profiles = len(seed_profiles)
            errors = 0
            max_errors = 10  # Stop if too many errors
            
            for i, profile in enumerate(seed_profiles, 1):
                if errors >= max_errors:
                    console.print(f"⚠️ Muitos erros ({errors}), parando busca", style="yellow")
                    break
                    
                username = profile['username']
                score = profile['score']
                
                console.print(f"🔍 [{i}/{total_profiles}] Testando @{username}...", style="dim")
                
                try:
                    # Clear search box with multiple methods
                    search_box.clear()
                    search_box.send_keys("")
                    time.sleep(0.3)
                    
                    # Type username character by character
                    for char in username:
                        search_box.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.15))
                    
                    # Wait for search results
                    time.sleep(random.uniform(1, 2))
                    
                    # Check if profile appears in results
                    result_selectors = [
                        f"//a[contains(@href, '/{username}/')]",
                        f"//*[contains(text(), '{username}')]//ancestor::a[contains(@href, '/')]",
                        f"//a[contains(@href, '{username}')]"
                    ]
                    
                    found = False
                    for selector in result_selectors:
                        try:
                            result_elements = self.driver.find_elements(By.XPATH, selector)
                            for element in result_elements:
                                if element.is_displayed() and username.lower() in element.get_attribute('href').lower():
                                    matches.append({
                                        'username': username,
                                        'score': score,
                                        'category': profile.get('category', 'Unknown')
                                    })
                                    console.print(f"✅ Match: @{username} (score: {score})", style="green")
                                    found = True
                                    break
                            if found:
                                break
                        except:
                            continue
                    
                    # Small delay between searches
                    time.sleep(random.uniform(0.2, 0.6))
                    
                except Exception as e:
                    errors += 1
                    console.print(f"⚠️ Erro ao testar @{username}: {str(e)}", style="dim")
                    time.sleep(0.5)
                    continue
            
            console.print(f"🎯 Busca concluída: {len(matches)} matches encontrados", style="cyan")
            return matches
            
        except Exception as e:
            console.print(f"❌ Erro durante busca: {str(e)}", style="red")
            return []
    
    def close(self):
        """Close browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

def analyze_hybrid(target_profile: str):
    """Hybrid analysis with manual login and automated search"""
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🤖 Análise Híbrida: @{target_username}", style="bold blue")
    console.print("📋 Login manual + Busca automática", style="dim")
    
    # Initialize components
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    scraper = HybridInstagramScraper()
    
    # Check cache first
    cached_result = cache.get_analysis(target_username)
    if cached_result:
        console.print("📋 Usando resultado em cache", style="yellow")
        scorer.display_results(target_username, cached_result)
        return
    
    try:
        # Setup browser
        if not scraper.setup_driver():
            return
        
        # Manual login
        if not scraper.manual_login_setup():
            return
        
        # Navigate to target profile
        if not scraper.navigate_to_profile(target_username):
            return
        
        # Open following modal
        if not scraper.open_following_modal():
            return
        
        # Load seed profiles
        with open('data/seed_profiles.json', 'r', encoding='utf-8') as f:
            seed_profiles = json.load(f)
        
        # Perform targeted search
        matches = scraper.search_in_following(seed_profiles)
        
        # Calculate and display results
        if matches:
            final_score = sum(match['score'] for match in matches) / len(matches)
            
            result_data = {
                'matches': matches,
                'final_score': final_score,
                'total_matches': len(matches)
            }
            
            # Cache results
            cache.store_analysis(target_username, result_data)
            
            # Display results
            scorer.display_results(target_username, result_data)
        else:
            console.print("❌ Nenhum match encontrado", style="red")
            console.print("💡 Possíveis causas:", style="yellow")
            console.print("   • Perfil privado ou sem seguidos públicos", style="dim")
            console.print("   • Perfil não segue políticos da base de dados", style="dim")
            console.print("   • Problemas de conectividade", style="dim")
            
    except KeyboardInterrupt:
        console.print("\n⚠️ Análise interrompida pelo usuário", style="yellow")
    except Exception as e:
        console.print(f"❌ Erro durante análise: {str(e)}", style="red")
    finally:
        console.print("🔄 Fechando navegador...", style="dim")
        scraper.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Uso: python vp_hybrid.py @perfil", style="red")
        console.print("Exemplo: python vp_hybrid.py @barbarastudart", style="dim")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('@'):
        target = f"@{target}"
    
    analyze_hybrid(target)
