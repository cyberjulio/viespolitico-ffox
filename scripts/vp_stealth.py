#!/usr/bin/env python3

import sys
import time
import random
import json
import pickle
import os
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

class StealthInstagramScraper:
    def __init__(self):
        self.driver = None
        self.profile_dir = "/Users/cyberjulio/Coding/viespolitico/chrome_profile"
        self.cookies_file = "/Users/cyberjulio/Coding/viespolitico/instagram_cookies.pkl"
        
    def setup_driver(self):
        try:
            options = Options()
            
            # Usar perfil persistente
            options.add_argument(f"--user-data-dir={self.profile_dir}")
            
            # Stealth máximo
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            # User agent realista
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Anti-detecção
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            
            self.driver = webdriver.Chrome(options=options)
            
            # Remover propriedade webdriver
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return True
            
        except Exception as e:
            console.print(f"❌ Erro Chrome: {str(e)}", style="red")
            return False
    
    def check_login_status(self):
        """Verifica se já está logado"""
        try:
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)
            
            # Procura elementos que indicam login
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//nav"))
                )
                console.print("✅ Já está logado!", style="green")
                return True
            except:
                console.print("❌ Não está logado", style="yellow")
                return False
                
        except Exception as e:
            console.print(f"⚠️ Erro ao verificar login: {str(e)}", style="yellow")
            return False
    
    def perform_login(self):
        """Login com comportamento humano"""
        try:
            console.print("🔐 Fazendo login...", style="cyan")
            
            # Ir para página de login
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(random.uniform(2, 4))
            
            # Ler credenciais
            with open('data/instacreds.txt', 'r') as f:
                lines = f.read().strip().split('\n')
                email = lines[0].split(':')[1]
                password = lines[1].split(':')[1]
            
            # Aguardar campos
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Digitação humana
            username_field.clear()
            for char in email:
                username_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(0.5, 1.5))
            
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(random.uniform(1, 2))
            
            # Clicar login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            ActionChains(self.driver).move_to_element(login_button).click().perform()
            
            # Aguardar resultado
            time.sleep(5)
            
            # Verificar sucesso
            current_url = self.driver.current_url
            if "/accounts/login" not in current_url:
                console.print("✅ Login realizado!", style="green")
                
                # Salvar cookies
                try:
                    cookies = self.driver.get_cookies()
                    with open(self.cookies_file, 'wb') as f:
                        pickle.dump(cookies, f)
                    console.print("💾 Cookies salvos", style="dim")
                except:
                    pass
                    
                return True
            else:
                console.print("❌ Login falhou", style="red")
                return False
                
        except Exception as e:
            console.print(f"❌ Erro no login: {str(e)}", style="red")
            return False
    
    def ensure_logged_in(self):
        """Garante que está logado"""
        if self.check_login_status():
            return True
        
        # Tentar carregar cookies
        if os.path.exists(self.cookies_file):
            try:
                console.print("🍪 Carregando cookies...", style="cyan")
                self.driver.get("https://www.instagram.com/")
                
                with open(self.cookies_file, 'rb') as f:
                    cookies = pickle.load(f)
                
                for cookie in cookies:
                    try:
                        self.driver.add_cookie(cookie)
                    except:
                        pass
                
                self.driver.refresh()
                time.sleep(3)
                
                if self.check_login_status():
                    return True
            except:
                console.print("⚠️ Cookies inválidos", style="yellow")
        
        # Login manual se necessário
        return self.perform_login()
    
    def navigate_to_profile(self, username):
        try:
            console.print(f"👤 Indo para @{username}...", style="cyan")
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.uniform(2, 3))
            
            if "Page Not Found" in self.driver.page_source:
                console.print(f"❌ @{username} não existe", style="red")
                return False
                
            return True
        except Exception as e:
            console.print(f"❌ Erro: {str(e)}", style="red")
            return False
    
    def open_following_modal(self):
        try:
            console.print("📋 Procurando seguidos...", style="cyan")
            
            # Múltiplas estratégias
            strategies = [
                "//a[contains(@href, '/following/')]",
                "//*[contains(text(), 'following')]//ancestor::a",
                "//*[contains(text(), 'seguindo')]//ancestor::a"
            ]
            
            for i, xpath in enumerate(strategies, 1):
                try:
                    console.print(f"🔍 Tentativa {i}...", style="dim")
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            console.print("✅ Link encontrado!", style="green")
                            
                            # Scroll e click
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(1)
                            ActionChains(self.driver).move_to_element(element).click().perform()
                            time.sleep(3)
                            
                            # Verificar modal
                            try:
                                WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder]"))
                                )
                                console.print("✅ Modal aberto!", style="green")
                                return True
                            except:
                                console.print("⚠️ Modal não abriu, tentando próximo...", style="yellow")
                                continue
                                
                except Exception as e:
                    console.print(f"⚠️ Estratégia {i} falhou", style="dim")
                    continue
            
            console.print("❌ Modal não encontrado", style="red")
            return False
            
        except Exception as e:
            console.print(f"❌ Erro modal: {str(e)}", style="red")
            return False
    
    def search_profiles(self, seed_profiles):
        try:
            search_box = self.driver.find_element(By.XPATH, "//input[@placeholder]")
            matches = []
            
            console.print("🔍 Buscando...", style="cyan")
            
            for i, profile in enumerate(seed_profiles[:20], 1):  # Limitar para teste
                username = profile['username']
                score = profile['score']
                
                console.print(f"[{i}/20] @{username}...", style="dim")
                
                try:
                    search_box.clear()
                    time.sleep(0.2)
                    
                    for char in username:
                        search_box.send_keys(char)
                        time.sleep(random.uniform(0.03, 0.08))
                    
                    time.sleep(1)
                    
                    # Verificar resultado
                    try:
                        result = WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/{username}/')]"))
                        )
                        
                        if result.is_displayed():
                            matches.append({
                                'username': username,
                                'score': score,
                                'category': profile.get('category', 'Unknown')
                            })
                            console.print(f"✅ @{username}", style="green")
                    except:
                        pass
                    
                    time.sleep(random.uniform(0.3, 0.6))
                    
                except Exception as e:
                    console.print(f"⚠️ @{username}: {str(e)}", style="dim")
                    continue
            
            return matches
            
        except Exception as e:
            console.print(f"❌ Erro busca: {str(e)}", style="red")
            return []
    
    def close(self):
        if self.driver:
            self.driver.quit()

def analyze_stealth(target_profile: str):
    target_username = target_profile.replace('@', '').lower()
    
    console.print(f"🥷 Análise Stealth: @{target_username}", style="bold blue")
    
    cache = Cache(cache_duration_hours=24)
    scorer = PoliticalScorer()
    scraper = StealthInstagramScraper()
    
    # Cache check
    cached_result = cache.get_analysis(target_username)
    if cached_result:
        console.print("📋 Cache hit", style="yellow")
        scorer.display_results(target_username, cached_result)
        return
    
    try:
        if not scraper.setup_driver():
            return
        
        if not scraper.ensure_logged_in():
            console.print("❌ Login falhou", style="red")
            return
        
        if not scraper.navigate_to_profile(target_username):
            return
        
        if not scraper.open_following_modal():
            return
        
        with open('data/seed_profiles.json', 'r', encoding='utf-8') as f:
            seed_profiles = json.load(f)
        
        matches = scraper.search_profiles(seed_profiles)
        
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
            console.print("❌ Sem matches", style="red")
            
    except Exception as e:
        console.print(f"❌ Erro: {str(e)}", style="red")
    finally:
        scraper.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        console.print("Uso: python vp_stealth.py @perfil", style="red")
        sys.exit(1)
    
    target = sys.argv[1]
    if not target.startswith('@'):
        target = f"@{target}"
    
    analyze_stealth(target)
