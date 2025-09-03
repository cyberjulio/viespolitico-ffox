import time
import random
import json
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from rich.console import Console

console = Console()

class RobustInstagramScraper:
    def __init__(self):
        self.driver = None
        self.logged_in = False
        
    def _setup_driver(self):
        """Setup Chrome driver with advanced anti-detection"""
        chrome_options = Options()
        
        # Basic stealth options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Advanced anti-detection
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        
        # Realistic window size
        chrome_options.add_argument("--window-size=1366,768")
        
        # Rotate user agents
        user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Execute stealth scripts
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            return True
        except Exception as e:
            console.print(f"❌ Failed to setup Chrome driver: {e}", style="red")
            return False
            
    def _human_like_delay(self, min_seconds=1, max_seconds=3):
        """Add human-like delays"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def _human_like_typing(self, element, text):
        """Type text with human-like delays"""
        element.clear()
        self._human_like_delay(0.5, 1.5)
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
            
    def _random_mouse_movement(self):
        """Add random mouse movements"""
        try:
            actions = ActionChains(self.driver)
            for _ in range(random.randint(1, 3)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                actions.move_by_offset(x, y)
                actions.perform()
                time.sleep(random.uniform(0.1, 0.5))
        except Exception:
            pass
            
    def login(self, username: str, password: str, max_attempts: int = 3) -> bool:
        """Robust login with multiple strategies"""
        
        for attempt in range(max_attempts):
            console.print(f"🔄 Login attempt {attempt + 1}/{max_attempts}", style="yellow")
            
            if not self._setup_driver():
                continue
                
            try:
                # Strategy 1: Direct login page
                if self._try_direct_login(username, password):
                    return True
                    
                self.driver.quit()
                self._human_like_delay(5, 10)  # Wait between attempts
                
            except Exception as e:
                console.print(f"❌ Attempt {attempt + 1} failed: {e}", style="red")
                if self.driver:
                    self.driver.quit()
                self._human_like_delay(10, 20)
                
        console.print("❌ All login attempts failed", style="red")
        return False
        
    def _try_direct_login(self, username: str, password: str) -> bool:
        """Try direct login to Instagram"""
        try:
            console.print("🌐 Navigating to Instagram...", style="cyan")
            
            # Go to Instagram homepage first (more natural)
            self.driver.get("https://www.instagram.com/")
            self._human_like_delay(3, 6)
            self._random_mouse_movement()
            
            # Handle cookies if present
            try:
                cookies_selectors = [
                    "//button[contains(text(), 'Accept')]",
                    "//button[contains(text(), 'Allow')]",
                    "//button[contains(text(), 'OK')]"
                ]
                
                for selector in cookies_selectors:
                    try:
                        cookies_btn = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        cookies_btn.click()
                        self._human_like_delay(1, 2)
                        break
                    except TimeoutException:
                        continue
            except Exception:
                pass
                
            # Navigate to login page
            console.print("🔐 Going to login page...", style="cyan")
            self.driver.get("https://www.instagram.com/accounts/login/")
            self._human_like_delay(4, 7)
            
            # Wait for login form
            try:
                username_input = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
            except TimeoutException:
                console.print("❌ Login form not found", style="red")
                return False
                
            console.print("✅ Login form found", style="green")
            self._random_mouse_movement()
            
            # Fill username
            console.print("👤 Entering username...", style="cyan")
            self._human_like_typing(username_input, username)
            self._human_like_delay(1, 2)
            
            # Fill password
            password_input = self.driver.find_element(By.NAME, "password")
            console.print("🔑 Entering password...", style="cyan")
            self._human_like_typing(password_input, password)
            self._human_like_delay(2, 4)
            
            # Click login button
            console.print("🚀 Clicking login...", style="cyan")
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            
            # Scroll to button if needed
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            self._human_like_delay(0.5, 1)
            
            login_button.click()
            
            # Wait for login to process
            console.print("⏳ Waiting for login response...", style="yellow")
            self._human_like_delay(8, 15)
            
            # Check for various outcomes
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            # Success indicators
            if ("instagram.com" in current_url and 
                "login" not in current_url and 
                "challenge" not in current_url):
                
                console.print("✅ Login successful!", style="green")
                self.logged_in = True
                
                # Handle post-login popups
                self._handle_post_login_popups()
                return True
                
            # Check for specific error conditions
            elif "challenge" in current_url or "challenge" in page_source:
                console.print("❌ Challenge required (2FA/verification)", style="red")
                return False
                
            elif "error" in page_source or "incorrect" in page_source:
                console.print("❌ Invalid credentials", style="red")
                return False
                
            elif "suspicious" in page_source or "unusual" in page_source:
                console.print("❌ Suspicious activity detected", style="red")
                return False
                
            else:
                console.print("❌ Login failed - unknown reason", style="red")
                console.print(f"Current URL: {current_url}", style="dim")
                return False
                
        except Exception as e:
            console.print(f"❌ Login error: {e}", style="red")
            return False
            
    def _handle_post_login_popups(self):
        """Handle popups that appear after login"""
        popups_to_dismiss = [
            "//button[contains(text(), 'Not Now')]",
            "//button[contains(text(), 'Not now')]",
            "//button[contains(text(), 'Skip')]",
            "//button[contains(text(), 'Later')]",
            "//button[contains(text(), 'Cancel')]"
        ]
        
        for _ in range(3):  # Try to dismiss up to 3 popups
            try:
                for selector in popups_to_dismiss:
                    try:
                        popup_btn = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        popup_btn.click()
                        console.print("✅ Dismissed popup", style="green")
                        self._human_like_delay(1, 2)
                        break
                    except TimeoutException:
                        continue
                else:
                    break  # No more popups found
            except Exception:
                break
                
    def search_in_following_modal(self, search_term: str) -> bool:
        """Search for a specific user in the following modal"""
        try:
            # Find search input with multiple strategies
            search_selectors = [
                "//div[@role='dialog']//input[@placeholder='Search']",
                "//div[@role='dialog']//input[@type='text']",
                "//div[@role='dialog']//input[contains(@placeholder, 'search')]",
                "//div[@role='dialog']//input[contains(@placeholder, 'Search')]"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
                    
            if not search_input:
                console.print("❌ Search input not found", style="red")
                return False
                
            # Clear and search
            search_input.clear()
            self._human_like_delay(0.5, 1)
            
            console.print(f"🔍 Searching for: {search_term}", style="dim")
            self._human_like_typing(search_input, search_term)
            self._human_like_delay(2, 4)  # Wait for search results
            
            # Look for results
            result_selectors = [
                f"//div[@role='dialog']//a[contains(@href, '/{search_term}/')]",
                f"//div[@role='dialog']//span[text()='{search_term}']",
                f"//div[@role='dialog']//a[contains(@href, '/{search_term}')]"
            ]
            
            for selector in result_selectors:
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    console.print(f"✅ Found {search_term}", style="green")
                    return True
                except TimeoutException:
                    continue
                    
            console.print(f"❌ {search_term} not found", style="red")
            return False
            
        except Exception as e:
            console.print(f"❌ Search error for {search_term}: {e}", style="red")
            return False
            
    def get_user_followings_by_search(self, username: str, seed_profiles: List[str]) -> List[str]:
        """Search for seed profiles in user's following list"""
        if not self.logged_in or not self.driver:
            console.print("❌ Not logged in", style="red")
            return []
            
        try:
            console.print(f"🔄 Analyzing @{username}...", style="yellow")
            
            # Navigate to profile
            self.driver.get(f"https://www.instagram.com/{username}/")
            self._human_like_delay(4, 7)
            
            # Find following link
            following_selectors = [
                "//a[contains(@href, '/following/')]",
                "//a[contains(text(), 'following')]",
                "//span[contains(text(), 'following')]/parent::a"
            ]
            
            following_link = None
            for selector in following_selectors:
                try:
                    following_link = WebDriverWait(self.driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not following_link:
                console.print("❌ Following link not found", style="red")
                return []
            
            console.print("✅ Opening following modal...", style="green")
            following_link.click()
            self._human_like_delay(4, 7)
            
            # Wait for modal
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
            except TimeoutException:
                console.print("❌ Following modal not opened", style="red")
                return []
                
            # Search for each seed profile
            found_followings = []
            console.print(f"🔍 Searching {len(seed_profiles)} profiles...", style="cyan")
            
            for i, seed_profile in enumerate(seed_profiles):
                console.print(f"[{i+1}/{len(seed_profiles)}] Checking @{seed_profile}", style="dim")
                
                if self.search_in_following_modal(seed_profile):
                    found_followings.append(seed_profile)
                
                # Random delay between searches
                self._human_like_delay(1, 3)
                
            console.print(f"✅ Found {len(found_followings)} matches", style="green")
            return found_followings
            
        except Exception as e:
            console.print(f"❌ Analysis error: {e}", style="red")
            return []
            
    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            console.print("🔄 Browser closed", style="dim")
