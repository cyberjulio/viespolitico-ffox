import os
import json
import time
import random
from pathlib import Path
from instagrapi import Client
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class InstagramAuth:
    def __init__(self):
        self.client = Client()
        self.session_file = Path("data/session.json")
        
        # Configure client settings for better success rate
        self.client.delay_range = [3, 7]
        
        # Set more realistic user agent and device settings
        self.client.set_user_agent("Instagram 219.0.0.12.117 Android")
        self.client.set_device({
            "app_version": "219.0.0.12.117",
            "android_version": 28,
            "android_release": "9.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "samsung",
            "device": "SM-G973F",
            "model": "galaxy_s10",
            "cpu": "exynos9820",
            "version_code": "314665256"
        })
        
    def login(self, username: str = None, password: str = None):
        """Login to Instagram and save session"""
        
        # Try to load existing session
        if self.session_file.exists():
            try:
                self.client.load_settings(str(self.session_file))
                # Try to get account info to verify session
                self.client.account_info()
                console.print("✅ Logged in using saved session", style="green")
                return True
            except Exception as e:
                console.print(f"❌ Saved session failed: {e}", style="red")
                # Remove invalid session file
                self.session_file.unlink()
                
        # Fresh login
        if not username:
            username = Prompt.ask("Instagram username")
        if not password:
            password = Prompt.ask("Instagram password", password=True)
            
        try:
            console.print("🔄 Attempting login...", style="yellow")
            
            # Add random delay before login attempt
            delay = random.uniform(3, 6)
            time.sleep(delay)
            
            # Try login
            self.client.login(username, password)
            
            # Add delay after login
            time.sleep(2)
            
            # Verify login worked
            account_info = self.client.account_info()
            console.print(f"✅ Logged in as @{account_info.username}", style="green")
            
            # Save session
            self.session_file.parent.mkdir(exist_ok=True)
            self.client.dump_settings(str(self.session_file))
            
            console.print("✅ Session saved successfully", style="green")
            return True
            
        except Exception as e:
            error_msg = str(e).lower()
            console.print(f"❌ Login error details: {e}", style="red")
            
            if "challenge" in error_msg or "verification" in error_msg:
                console.print("💡 Try: Login to Instagram app first, then try again", style="blue")
            elif "checkpoint" in error_msg:
                console.print("💡 Account needs verification through Instagram app", style="blue")
            elif "rate limit" in error_msg or "please wait" in error_msg:
                console.print("💡 Rate limited. Wait 10-15 minutes and try again", style="blue")
            elif "password" in error_msg or "credentials" in error_msg:
                console.print("💡 Double-check username and password", style="blue")
            elif "suspicious" in error_msg or "blacklist" in error_msg:
                console.print("💡 IP may be blocked. Try using a VPN or different network", style="blue")
            
            return False
            
    def get_client(self):
        """Get authenticated Instagram client"""
        return self.client
