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
from selenium.webdriver.common.keys import Keys
from rich.console import Console
from core.scoring import PoliticalScorer
from core.cache import Cache

console = Console()

class RobustInstagramScraper:
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
            
            # Disable various detection methods
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")  # Faster loading
            options.add_argument("--disable-javascript-harmony-shipping")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-backgrounding-occluded-windows")
            
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
    
    def human_type(self, element, text, delay_range=(50, 150)):
        """Type text with human-like delays"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(delay_range[0]/1000, delay_range[1]/1000))
    
    def human_click(self, element):
        """Click with human-like behavior"""
        # Move to element first
        ActionChains(self.driver).move_to_element(element).perform()
        time.sleep(random.uniform(0.1, 0.3))
        
        # Click
        ActionChains(self.driver).click(element).perform()
        time.sleep(random.uniform(0.2, 0.5))
    
    def login(self, username, password):
        """Robust login with anti-detection"""
        try:
            console.print("🌐 Navegando para Instagram...", style="cyan")
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # Random delay to simulate human behavior
            time.sleep(random.uniform(3, 5))
            
            # Wait for login form
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            password_field = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            
            console.print("🔐 Preenchendo credenciais...", style="cyan")
            
            # Human-like typing
            self.human_type(username_field, username)
            time.sleep(random.uniform(0.5, 1.5))
            
            self.human_type(password_field, password)
            time.sleep(random.uniform(1, 2))
            
            # Click login
            console.print("🚀 Fazendo login...", style="cyan")
            self.human_click(login_button)
            
            # Wait for login to complete
            time.sleep(random.uniform(4, 6))
            
            # Check for various post-login scenarios
            current_url = self.driver.current_url
            
            # Check if we're on home page (successful login)
            if "instagram.com" in current_url and "/accounts/login" not in current_url:
                console.print("✅ Login realizado com sucesso!", style="green")
                return True
                
            # Check for 2FA or verification
            if "challenge" in current_url or "two_factor" in current_url:
                console.print("⚠️ Verificação adicional necessária", style="yellow")
                console.print("👤 Complete a verificação manualmente no navegador", style="yellow")
                input("⏳ Pressione ENTER quando completar...")
                return True
                
            # Check if still on login page (failed login)
            if "/accounts/login" in current_url:
                console.print("❌ Login falhou - credenciais incorretas?", style="red")
                return False
                
            return True
            
        except Exception as e:
            console.print(f"❌ Erro durante login: {str(e)}", style="red")
            return False
    
    def navigate_to_profile(self, username):
        """Navigate to user profile"""
        try:
            console.print(f"👤 Navegando para @{username}...", style="cyan")
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.uniform(2, 4))
            
            # Check if profile exists
            if "Page Not Found" in self.driver.page_source or "Sorry, this page isn't available" in self.driver.page_source:
                console.print(f"❌ Perfil @{username} não encontrado", style="red")
                return False
                
            return True
            
        except Exception as e:
            console.print(f"❌ Erro ao navegar para perfil: {str(e)}", style="red")
            return False
    
    def open_following_modal(self):
        """Open following modal with multiple strategies"""
        try:
            console.print("📋 Abrindo lista de seguidos...", style="cyan")
            
            # Strategy 1: Try direct link
            try:
                following_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following/')]"))
                )
                self.human_click(following_link)
                time.sleep(random.uniform(2, 4))
                return True
            except:
                pass
            
            # Strategy 2: Try by text content
            try:
                following_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'following') or contains(text(), 'seguindo')]")
                for element in following_elements:
                    if element.is_displayed() and element.is_enabled():
                        self.human_click(element)
                        time.sleep(random.uniform(2, 4))
                        return True
            except:
                pass
            
            # Strategy 3: Try by partial href
            try:
                following_link = self.driver.find_element(By.XPATH, "//a[contains(@href, 'following')]")
                self.human_click(following_link)
                time.sleep(random.uniform(2, 4))
                return True
            except:
                pass
                
            console.print("❌ Não foi possível abrir lista de seguidos", style="red")
            return False
            
        except Exception as e:
            console.print(f"❌ Erro ao abrir modal: {str(e)}", style="red")
            return False
    
    def search_in_following(self, seed_profiles):
        """Perform targeted search in following modal"""
        try:
            # Wait for modal and search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder and (contains(@placeholder, 'Search') or contains(@placeholder, 'Pesquisar'))]"))
            )
            
            console.print("🔍 Iniciando busca direcionada...", style="cyan")
            
            matches = []
            total_profiles = len(seed_profiles)
            
            for i, profile in enumerate(seed_profiles, 1):
                username = profile['username']
                score = profile['score']
                
                console.print(f"🔍 [{i}/{total_profiles}] Testando @{username}...", style="dim")
                
                try:
                    # Clear search box
                    search_box.clear()
                    time.sleep(random.uniform(0.2, 0.5))
                    
                    # Type username
                    self.human_type(search_box, username, delay_range=(30, 80))
                    time.sleep(random.uniform(1, 2))
                    
                    # Check if profile appears in results
                    try:
                        result_element = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/{username}/')]"))
                        )
                        
                        if result_element.is_displayed():
                            matches.append({
                                'username': username,
                                'score': score,
                                'category': profile.get('category', 'Unknown')
                            })
                            console.print(f"✅ Match: @{username} (score: {score})", style="green")
                            
                    except:
                        # No match found for this profile
                        pass
                    
                    # Small delay between searches
                    time.sleep(random.uniform(0.3, 0.8))
                    
                except Exception as e:
                    console.print(f"⚠️ Erro ao testar @{username}: {str(e)}", style="yellow")
                    continue
            
            return matches
            
        except Exception as e:
            console.print(f"❌ Erro durante busca: {str(e)}", style="red")
            return []
    
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()

def analyze_robust(target_profile: str):
    """Robust automatic analysis"""
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🤖 Análise Robusta: @{target_username}", style="bold blue")
    
    # Initialize components
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    scraper = RobustInstagramScraper()
    
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
        
        # Login
        if not scraper.login("viespolitico", "r@FRzo8FGeg@4pr4"):
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
            
    except Exception as e:
        console.print(f"❌ Erro durante análise: {str(e)}", style="red")
    finally:
        scraper.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Uso: python vp_robust.py @perfil", style="red")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('@'):
        target = f"@{target}"
    
    analyze_robust(target)
