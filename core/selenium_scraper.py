import time
import random
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from rich.console import Console

console = Console()

class SeleniumInstagramScraper:
    def __init__(self):
        self.driver = None
        self.logged_in = False
        
    def _setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return True
        except Exception as e:
            console.print(f"❌ Failed to setup Chrome driver: {e}", style="red")
            return False
            
    def search_in_following_modal(self, search_term: str) -> bool:
        """Search for a specific user in the following modal"""
        try:
            # Find the search input in the modal
            search_selectors = [
                "//div[@role='dialog']//input[@placeholder='Search']",
                "//div[@role='dialog']//input[@type='text']",
                "//div[@role='dialog']//input[contains(@placeholder, 'search')]",
                "//div[@role='dialog']//input[contains(@placeholder, 'Search')]"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    console.print(f"✅ Found search input with selector: {selector[:30]}...", style="green")
                    break
                except TimeoutException:
                    continue
                    
            if not search_input:
                console.print("❌ Could not find search input in modal", style="red")
                return False
                
            # Clear and type search term
            search_input.clear()
            time.sleep(0.5)
            
            console.print(f"🔍 Searching for: {search_term}", style="cyan")
            search_input.send_keys(search_term)
            time.sleep(2)  # Wait for search results
            
            # Look for the exact username in results
            try:
                # Try to find a link with the exact username
                result_selectors = [
                    f"//div[@role='dialog']//a[contains(@href, '/{search_term}/')]",
                    f"//div[@role='dialog']//span[text()='{search_term}']",
                    f"//div[@role='dialog']//a[contains(@href, '/{search_term}')]"
                ]
                
                for selector in result_selectors:
                    try:
                        result = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        console.print(f"✅ Found {search_term} in following list!", style="green")
                        return True
                    except TimeoutException:
                        continue
                        
                console.print(f"❌ {search_term} not found in following list", style="red")
                return False
                
            except Exception as e:
                console.print(f"❌ Error searching for {search_term}: {e}", style="red")
                return False
                
        except Exception as e:
            console.print(f"❌ Error in search function: {e}", style="red")
            return False
            
    def get_user_followings_by_search(self, username: str, seed_profiles: List[str]) -> List[str]:
        """Search for specific seed profiles in user's following list"""
        if not self.logged_in or not self.driver:
            console.print("❌ Not logged in", style="red")
            return []
            
        try:
            console.print(f"🔄 Searching followings for @{username}...", style="yellow")
            
            # Go to user profile
            self.driver.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.uniform(3, 5))
            
            # Find and click following link
            try:
                following_selectors = [
                    "//a[contains(@href, '/following/')]",
                    "//a[contains(text(), 'following')]",
                    "//span[contains(text(), 'following')]/parent::a"
                ]
                
                following_link = None
                for selector in following_selectors:
                    try:
                        following_link = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        break
                    except TimeoutException:
                        continue
                
                if not following_link:
                    console.print("❌ Could not find following link", style="red")
                    return []
                
                console.print("✅ Found following link", style="green")
                following_link.click()
                time.sleep(random.uniform(3, 5))
                
            except Exception as e:
                console.print(f"❌ Error clicking following link: {e}", style="red")
                return []
                
            # Wait for modal to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                console.print("✅ Following modal opened", style="green")
            except TimeoutException:
                console.print("❌ Following modal did not open", style="red")
                return []
                
            # Search for each seed profile
            found_followings = []
            
            console.print(f"🔍 Searching for {len(seed_profiles)} seed profiles...", style="yellow")
            
            for seed_profile in seed_profiles:
                console.print(f"🔍 Checking: @{seed_profile}", style="dim")
                
                if self.search_in_following_modal(seed_profile):
                    found_followings.append(seed_profile)
                    console.print(f"✅ Match found: @{seed_profile}", style="green")
                else:
                    console.print(f"❌ No match: @{seed_profile}", style="red")
                
                # Small delay between searches
                time.sleep(random.uniform(1, 2))
                
            console.print(f"✅ Found {len(found_followings)} matches out of {len(seed_profiles)} seed profiles", style="green")
            return found_followings
            
        except Exception as e:
            console.print(f"❌ Error in search process: {e}", style="red")
            return []
            
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            console.print("🔄 Browser closed", style="dim")
