#!/usr/bin/env python3

import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from rich.console import Console

console = Console()

class DebugInstagramScraper:
    def __init__(self):
        self.driver = None
        
    def setup_driver(self):
        try:
            options = Options()
            options.set_preference("dom.webdriver.enabled", False)
            self.driver = webdriver.Firefox(options=options)
            self.driver.set_window_size(1366, 768)
            return True
        except Exception as e:
            console.print(f"❌ Erro Firefox: {str(e)}", style="red")
            return False
    
    def debug_login(self, email, password):
        try:
            console.print("🌐 Navegando para Instagram...", style="cyan")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            console.print("🔍 Procurando campos de login...", style="cyan")
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            console.print(f"📧 Digitando email: {email}", style="cyan")
            username_field.clear()
            username_field.send_keys(email)
            time.sleep(1)
            
            console.print("🔐 Digitando senha...", style="cyan")
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            console.print("🚀 Clicando login...", style="cyan")
            login_button.click()
            
            console.print("⏳ Aguardando 5 segundos...", style="yellow")
            time.sleep(5)
            
            # Debug detalhado
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            console.print("=" * 60, style="blue")
            console.print("🔍 RESULTADO DO LOGIN:", style="bold blue")
            console.print(f"URL atual: {current_url}", style="white")
            console.print(f"Título: {page_title}", style="white")
            
            # Verificar mensagens de erro
            try:
                error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Sorry') or contains(text(), 'incorrect') or contains(text(), 'error') or contains(text(), 'wrong')]")
                if error_elements:
                    console.print("❌ ERROS ENCONTRADOS:", style="red")
                    for error in error_elements:
                        if error.is_displayed():
                            console.print(f"   • {error.text}", style="red")
                else:
                    console.print("✅ Nenhum erro visível", style="green")
            except:
                console.print("⚠️ Não foi possível verificar erros", style="yellow")
            
            # Verificar se ainda está na página de login
            if "/accounts/login" in current_url:
                console.print("❌ AINDA NA PÁGINA DE LOGIN", style="red")
                
                # Verificar se há campos preenchidos
                try:
                    username_value = self.driver.find_element(By.NAME, "username").get_attribute("value")
                    console.print(f"Campo usuário: '{username_value}'", style="dim")
                except:
                    pass
                    
                return False
            
            # Verificar se precisa de 2FA
            if any(word in current_url for word in ["challenge", "two_factor", "checkpoint"]):
                console.print("📱 VERIFICAÇÃO 2FA NECESSÁRIA", style="yellow")
                console.print("Complete manualmente no navegador", style="yellow")
                input("Pressione ENTER quando completar...")
                return True
            
            # Verificar se chegou na home
            if current_url == "https://www.instagram.com/" or "/accounts/onetap" in current_url:
                console.print("✅ LOGIN SUCESSO - NA HOME", style="green")
                return True
            
            console.print("⚠️ ESTADO DESCONHECIDO", style="yellow")
            console.print("=" * 60, style="blue")
            
            # Perguntar ao usuário
            response = input("Login funcionou? (s/n): ").lower()
            return response == 's'
            
        except Exception as e:
            console.print(f"❌ Erro durante login: {str(e)}", style="red")
            return False
    
    def close(self):
        if self.driver:
            self.driver.quit()

def test_login():
    console.print("🔍 TESTE DE LOGIN DEBUG", style="bold blue")
    
    scraper = DebugInstagramScraper()
    
    try:
        if not scraper.setup_driver():
            return
        
        # Ler credenciais
        with open('data/instacreds.txt', 'r') as f:
            lines = f.read().strip().split('\n')
            email = lines[0].split(':')[1]
            password = lines[1].split(':')[1]
        
        console.print(f"📧 Email: {email}", style="dim")
        console.print(f"🔐 Senha: {'*' * len(password)}", style="dim")
        
        success = scraper.debug_login(email, password)
        
        if success:
            console.print("✅ LOGIN FUNCIONOU!", style="green")
        else:
            console.print("❌ LOGIN FALHOU!", style="red")
            
    except Exception as e:
        console.print(f"❌ Erro: {str(e)}", style="red")
    finally:
        input("Pressione ENTER para fechar...")
        scraper.close()

if __name__ == "__main__":
    test_login()
