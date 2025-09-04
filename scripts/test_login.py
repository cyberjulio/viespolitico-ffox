#!/usr/bin/env python3

import time
import json
from pathlib import Path
from instagrapi import Client
from rich.console import Console

console = Console()

def test_login():
    """Test login with different configurations"""
    
    username = "viespolitico"
    password = "x96nA6M!9pCaCfK4"
    
    console.print("🔄 Testing login configurations...", style="yellow")
    
    # Configuration 1: Basic client
    console.print("\n1️⃣ Testing basic client...", style="blue")
    try:
        cl = Client()
        cl.login(username, password)
        console.print("✅ Basic client worked!", style="green")
        return cl
    except Exception as e:
        console.print(f"❌ Basic client failed: {e}", style="red")
    
    # Configuration 2: With delays
    console.print("\n2️⃣ Testing with delays...", style="blue")
    try:
        cl = Client()
        cl.delay_range = [1, 3]
        time.sleep(2)
        cl.login(username, password)
        console.print("✅ Delayed client worked!", style="green")
        return cl
    except Exception as e:
        console.print(f"❌ Delayed client failed: {e}", style="red")
    
    # Configuration 3: With custom settings
    console.print("\n3️⃣ Testing with custom settings...", style="blue")
    try:
        cl = Client()
        
        # Set custom settings
        cl.set_settings({
            "user_agent": "Instagram 219.0.0.12.117 Android (28/9; 480dpi; 1080x1920; samsung; SM-G973F; beyond1; exynos9820; en_US; 314665256)",
            "country": "US",
            "country_code": 1,
            "locale": "en_US",
            "timezone_offset": -14400
        })
        
        time.sleep(3)
        cl.login(username, password)
        console.print("✅ Custom settings worked!", style="green")
        return cl
    except Exception as e:
        console.print(f"❌ Custom settings failed: {e}", style="red")
    
    # Configuration 4: Try with session file approach
    console.print("\n4️⃣ Testing session approach...", style="blue")
    try:
        cl = Client()
        
        # Try to create a session first
        session_file = Path("test_session.json")
        if session_file.exists():
            cl.load_settings(str(session_file))
            
        cl.login(username, password)
        
        # Save session
        cl.dump_settings(str(session_file))
        console.print("✅ Session approach worked!", style="green")
        return cl
    except Exception as e:
        console.print(f"❌ Session approach failed: {e}", style="red")
    
    console.print("\n❌ All login methods failed", style="red")
    return None

if __name__ == "__main__":
    client = test_login()
    
    if client:
        console.print("\n🎉 Login successful! Testing basic functionality...", style="green")
        try:
            account_info = client.account_info()
            console.print(f"Account: @{account_info.username}", style="green")
            console.print(f"Followers: {account_info.follower_count}", style="green")
        except Exception as e:
            console.print(f"❌ Error getting account info: {e}", style="red")
    else:
        console.print("\n💡 Suggestions:", style="blue")
        console.print("1. Try logging into Instagram app first")
        console.print("2. Check if account has any restrictions")
        console.print("3. Try from a different network/VPN")
        console.print("4. Wait a few minutes and try again")
