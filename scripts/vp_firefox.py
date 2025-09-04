#!/usr/bin/env python3

import os
import sys
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from rich.console import Console
from core.scoring import PoliticalScorer
from core.cache import Cache

console = Console()

class FirefoxInstagramScraper:
    def __init__(self):
        self.driver = None
        
    def setup_driver(self):
        """Setup Firefox driver with anti-detection"""
        try:
            options = Options()
            
            # Firefox anti-detection options
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference('useAutomationExtension', False)
            options.set_preference("general.useragent.override", 
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0")
            
            # Performance optimizations
            options.set_preference("media.volume_scale", "0.0")  # Mute audio
            options.set_preference("permissions.default.image", 2)  # Block images
            
            # Create driver
            self.driver = webdriver.Firefox(options=options)
            
            # Set window size
            self.driver.set_window_size(1366, 768)
            
            # Set realistic timeouts
            self.driver.implicitly_wait(10)
            
            return True
            
        except Exception as e:
            console.print(f"❌ Erro ao configurar Firefox: {str(e)}", style="red")
            console.print("💡 Certifique-se que o geckodriver está instalado: brew install geckodriver", style="yellow")
            return False
    
    def human_type(self, element, text, delay_range=(80, 200)):
        """Type text with human-like delays"""
        element.clear()
        time.sleep(0.2)
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(delay_range[0]/1000, delay_range[1]/1000))
    
    def auto_login(self, email, password):
        """Automatic login with Firefox"""
        try:
            console.print("🌐 Navegando para Instagram...", style="cyan")
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # Wait for page to load
            time.sleep(random.uniform(3, 5))
            
            console.print("🔍 Procurando campos de login...", style="cyan")
            
            # Wait for login form
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            password_field = self.driver.find_element(By.NAME, "password")
            
            console.print("📧 Preenchendo email...", style="cyan")
            self.human_type(username_field, email)
            
            time.sleep(random.uniform(1, 2))
            
            console.print("🔐 Preenchendo senha...", style="cyan")
            self.human_type(password_field, password)
            
            time.sleep(random.uniform(1, 2))
            
            # Find and click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            
            console.print("🚀 Clicando em login...", style="cyan")
            ActionChains(self.driver).move_to_element(login_button).click().perform()
            
            # Wait for login to process
            console.print("⏳ Aguardando resposta do login...", style="yellow")
            time.sleep(random.uniform(4, 6))
            
            # Check current URL to determine login status
            current_url = self.driver.current_url
            console.print(f"🔍 URL atual: {current_url}", style="dim")
            
            # Success cases
            if any(path in current_url for path in ["/", "/accounts/onetap/", "/accounts/edit/"]):
                console.print("✅ Login realizado com sucesso!", style="green")
                return True
            
            # 2FA or challenge required
            if any(path in current_url for path in ["challenge", "two_factor", "checkpoint"]):
                console.print("📱 Verificação adicional detectada", style="yellow")
                console.print("👤 Complete a verificação no navegador", style="yellow")
                input("⏳ Pressione ENTER quando completar a verificação...")
                return True
            
            # Still on login page - check for errors
            if "/accounts/login" in current_url:
                # Check for error messages
                try:
                    error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'incorrect') or contains(text(), 'Sorry') or contains(text(), 'error')]")
                    if error_elements:
                        console.print("❌ Credenciais incorretas ou erro de login", style="red")
                    else:
                        console.print("⚠️ Login não completou - pode precisar de verificação", style="yellow")
                        console.print("👤 Verifique o navegador e complete manualmente se necessário", style="yellow")
                        input("⏳ Pressione ENTER quando estiver logado...")
                        return True
                except:
                    pass
                return False
            
            # Unknown state - assume success and continue
            console.print("⚠️ Estado de login incerto - continuando...", style="yellow")
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
            
            # Check for various error conditions
            page_source = self.driver.page_source.lower()
            current_url = self.driver.current_url
            
            if "page not found" in page_source or "this page isn't available" in page_source:
                console.print(f"❌ Perfil @{username} não encontrado", style="red")
                return False
            
            if "login" in current_url:
                console.print("❌ Redirecionado para login - sessão expirou", style="red")
                return False
            
            if "this account is private" in page_source or "esta conta é privada" in page_source:
                console.print(f"🔒 Perfil @{username} é privado", style="yellow")
                return False
            
            console.print(f"✅ Perfil @{username} carregado", style="green")
            return True
            
        except Exception as e:
            console.print(f"❌ Erro ao navegar para perfil: {str(e)}", style="red")
            return False
    
    def open_following_modal(self):
        """Open following modal"""
        try:
            console.print("📋 Procurando link de seguidos...", style="cyan")
            
            # Wait for page to load
            time.sleep(2)
            
            # Multiple strategies to find following link
            strategies = [
                "//a[contains(@href, '/following/')]",
                "//*[contains(text(), 'following')]//ancestor::a",
                "//*[contains(text(), 'seguindo')]//ancestor::a",
                "//a[contains(@href, 'following')]"
            ]
            
            for i, xpath in enumerate(strategies, 1):
                try:
                    console.print(f"🔍 Estratégia {i}...", style="dim")
                    
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            console.print(f"✅ Link encontrado! Clicando...", style="green")
                            
                            # Scroll to element
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(1)
                            
                            # Click
                            ActionChains(self.driver).move_to_element(element).click().perform()
                            time.sleep(3)
                            
                            # Verify modal opened
                            try:
                                WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder]"))
                                )
                                console.print("✅ Modal de seguidos aberto!", style="green")
                                return True
                            except:
                                continue
                                
                except Exception as e:
                    console.print(f"⚠️ Estratégia {i} falhou: {str(e)}", style="dim")
                    continue
            
            console.print("❌ Não foi possível abrir lista de seguidos", style="red")
            return False
            
        except Exception as e:
            console.print(f"❌ Erro ao abrir modal: {str(e)}", style="red")
            return False
    
    def search_in_following(self, seed_profiles):
        """Perform targeted search"""
        try:
            # Find search box
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder]"))
            )
            
            console.print("🔍 Iniciando busca direcionada...", style="cyan")
            
            matches = []
            total_profiles = len(seed_profiles)
            
            for i, profile in enumerate(seed_profiles, 1):
                username = profile['username']
                score = profile['score']
                
                console.print(f"🔍 [{i}/{total_profiles}] @{username}...", style="dim")
                
                try:
                    # Clear and type
                    search_box.clear()
                    time.sleep(0.3)
                    
                    for char in username:
                        search_box.send_keys(char)
                        time.sleep(random.uniform(0.05, 0.12))
                    
                    time.sleep(random.uniform(1, 1.5))
                    
                    # Check for results
                    try:
                        result_element = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/{username}/')]"))
                        )
                        
                        if result_element.is_displayed():
                            matches.append({
                                'username': username,
                                'score': score,
                                'category': profile.get('category', 'Unknown')
                            })
                            console.print(f"✅ @{username} (score: {score})", style="green")
                            
                    except:
                        pass
                    
                    time.sleep(random.uniform(0.2, 0.5))
                    
                except Exception as e:
                    console.print(f"⚠️ Erro @{username}: {str(e)}", style="dim")
                    continue
            
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

def analyze_firefox(target_profile: str):
    """Firefox-based analysis"""
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🦊 Análise Firefox: @{target_username}", style="bold blue")
    
    # Initialize components
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    scraper = FirefoxInstagramScraper()
    
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
        
        # Login automatically
        # Credentials should be provided via environment variables
        username = os.getenv('INSTAGRAM_USERNAME')
        password = os.getenv('INSTAGRAM_PASSWORD')
        
        if not username or not password:
            console.print("❌ Instagram credentials not found in environment variables", style="red")
            console.print("Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD", style="yellow")
            return
            
        if not scraper.auto_login(username, password):
            console.print("❌ Login automático falhou", style="red")
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
        
        # Perform search
        matches = scraper.search_in_following(seed_profiles)
        
        # Results
        if matches:
            final_score = sum(match['score'] for match in matches) / len(matches)
            
            result_data = {
                'matches': matches,
                'final_score': final_score,
                'total_matches': len(matches)
            }
            
            cache.store_analysis(target_username, result_data)
            scorer.display_results(target_username, result_data)
        else:
            console.print("❌ Nenhum match encontrado", style="red")
            
    except KeyboardInterrupt:
        console.print("\n⚠️ Interrompido pelo usuário", style="yellow")
    except Exception as e:
        console.print(f"❌ Erro: {str(e)}", style="red")
    finally:
        scraper.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Uso: python vp_firefox.py @perfil", style="red")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('@'):
        target = f"@{target}"
    
    analyze_firefox(target)
