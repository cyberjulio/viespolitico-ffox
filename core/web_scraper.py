import requests
import json
import time
import random
import re
from typing import List, Dict, Optional
from rich.console import Console

console = Console()

class WebInstagramScraper:
    def __init__(self):
        self.session = requests.Session()
        
        # Set browser-like headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.logged_in = False
        
    def login(self, username: str, password: str) -> bool:
        """Login using web interface"""
        try:
            console.print("🔄 Accessing Instagram login page...", style="yellow")
            
            # Get login page
            login_url = "https://www.instagram.com/accounts/login/"
            response = self.session.get(login_url)
            
            if response.status_code != 200:
                console.print(f"❌ Failed to access login page: {response.status_code}", style="red")
                return False
                
            # Extract CSRF token using multiple methods
            csrf_token = None
            
            # Method 1: Look for csrf_token in various formats
            patterns = [
                r'"csrf_token":"([^"]+)"',
                r'csrf_token["\s]*:["\s]*([^"]+)',
                r'csrftoken["\s]*:["\s]*([^"]+)',
                r'name="csrfmiddlewaretoken" value="([^"]+)"'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text)
                if matches:
                    csrf_token = matches[0]
                    console.print(f"✅ Found CSRF token using pattern: {pattern[:20]}...", style="green")
                    break
                    
            # Method 2: Look in cookies
            if not csrf_token:
                for cookie in self.session.cookies:
                    if 'csrf' in cookie.name.lower():
                        csrf_token = cookie.value
                        console.print("✅ Found CSRF token in cookies", style="green")
                        break
                        
            # Method 3: Extract from window._sharedData
            if not csrf_token:
                shared_data_match = re.search(r'window\._sharedData = ({.*?});', response.text)
                if shared_data_match:
                    try:
                        shared_data = json.loads(shared_data_match.group(1))
                        csrf_token = shared_data.get('config', {}).get('csrf_token')
                        if csrf_token:
                            console.print("✅ Found CSRF token in _sharedData", style="green")
                    except:
                        pass
                        
            if not csrf_token:
                console.print("❌ Could not find CSRF token", style="red")
                console.print("🔍 Trying without CSRF token...", style="yellow")
                csrf_token = ""
                
            # Prepare login data
            login_data = {
                'username': username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            # Set headers for login request
            login_headers = {
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/accounts/login/',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            if csrf_token:
                login_headers['X-CSRFToken'] = csrf_token
            
            # Add delay
            time.sleep(random.uniform(2, 4))
            
            console.print("🔄 Attempting login...", style="yellow")
            
            # Submit login
            login_response = self.session.post(
                "https://www.instagram.com/accounts/login/ajax/",
                data=login_data,
                headers=login_headers
            )
            
            console.print(f"Login response status: {login_response.status_code}", style="dim")
            
            if login_response.status_code == 200:
                try:
                    result = login_response.json()
                    console.print(f"Login response: {result}", style="dim")
                    
                    if result.get('authenticated'):
                        console.print("✅ Login successful!", style="green")
                        self.logged_in = True
                        return True
                    else:
                        console.print(f"❌ Login failed: {result.get('message', 'Unknown error')}", style="red")
                        return False
                except json.JSONDecodeError:
                    # Sometimes Instagram returns HTML instead of JSON
                    if 'instagram.com' in login_response.text and 'login' not in login_response.url:
                        console.print("✅ Login appears successful (redirected)", style="green")
                        self.logged_in = True
                        return True
                    else:
                        console.print("❌ Invalid response format", style="red")
                        console.print(f"Response preview: {login_response.text[:200]}...", style="dim")
                        return False
            else:
                console.print(f"❌ Login request failed: {login_response.status_code}", style="red")
                console.print(f"Response: {login_response.text[:200]}...", style="dim")
                return False
                
        except Exception as e:
            console.print(f"❌ Login error: {e}", style="red")
            return False
            
    def get_user_followings(self, username: str, max_count: int = 1000) -> List[str]:
        """Get user followings using web scraping"""
        if not self.logged_in:
            console.print("❌ Not logged in", style="red")
            return []
            
        try:
            console.print(f"🔄 Getting followings for @{username}...", style="yellow")
            
            # Get user profile page
            profile_url = f"https://www.instagram.com/{username}/"
            response = self.session.get(profile_url)
            
            if response.status_code != 200:
                console.print(f"❌ Could not access profile: {response.status_code}", style="red")
                return []
                
            console.print("✅ Accessed profile page", style="green")
            
            # For now, return empty list - we'll implement this after login works
            console.print("⚠️ Following extraction not yet implemented", style="yellow")
            return []
            
        except Exception as e:
            console.print(f"❌ Error getting followings: {e}", style="red")
            return []
