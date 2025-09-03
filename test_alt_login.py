#!/usr/bin/env python3

import time
from instagram_private_api import Client as AltClient
from rich.console import Console

console = Console()

def test_alt_login():
    """Test login with alternative library"""
    
    username = "viespolitico"
    password = "x96nA6M!9pCaCfK4"
    
    console.print("🔄 Testing alternative Instagram library...", style="yellow")
    
    try:
        # Try with alternative library
        api = AltClient(username, password)
        
        console.print("✅ Alternative library login successful!", style="green")
        
        # Test basic functionality
        user_info = api.current_user()
        console.print(f"Logged in as: @{user_info['username']}", style="green")
        console.print(f"Full name: {user_info.get('full_name', 'N/A')}", style="green")
        
        return api
        
    except Exception as e:
        console.print(f"❌ Alternative library failed: {e}", style="red")
        return None

if __name__ == "__main__":
    client = test_alt_login()
    
    if not client:
        console.print("\n🤔 Both libraries failed. This suggests:", style="yellow")
        console.print("1. Instagram is actively blocking API access for this account")
        console.print("2. The account may need verification")
        console.print("3. Instagram detected automation attempts")
        console.print("\n💡 Solutions:", style="blue")
        console.print("1. Use the account normally in browser/app for a few days")
        console.print("2. Try a completely fresh account")
        console.print("3. Use a different approach (manual data collection)")
        console.print("4. Try from a different device/network")
