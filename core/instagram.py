import time
import random
from typing import List, Dict, Optional
from instagrapi import Client
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class InstagramScraper:
    def __init__(self, client: Client, request_delay: int = 2):
        self.client = client
        self.request_delay = request_delay
        
    def _sleep(self):
        """Add delay between requests with jitter"""
        delay = self.request_delay + random.uniform(0, 1)
        time.sleep(delay)
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_user_followings(self, username: str, max_followings: int = 5000) -> List[str]:
        """Get list of users that the target follows"""
        try:
            user_id = self.client.user_id_from_username(username)
            self._sleep()
            
            followings = []
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Collecting followings for @{username}...", total=None)
                
                # Get followings with pagination
                following_users = self.client.user_following(user_id, amount=max_followings)
                
                for user in following_users:
                    followings.append(user.username)
                    if len(followings) >= max_followings:
                        break
                        
                progress.update(task, description=f"Found {len(followings)} followings")
                
            return followings
            
        except Exception as e:
            console.print(f"❌ Error getting followings for @{username}: {e}", style="red")
            return []
            
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_recent_posts(self, username: str, max_posts: int = 10) -> List[Dict]:
        """Get recent posts from a user"""
        try:
            user_id = self.client.user_id_from_username(username)
            self._sleep()
            
            posts = []
            medias = self.client.user_medias(user_id, amount=max_posts)
            
            for media in medias:
                posts.append({
                    'id': media.id,
                    'code': media.code,
                    'url': f"https://www.instagram.com/p/{media.code}/",
                    'caption': media.caption_text if media.caption_text else "",
                    'like_count': media.like_count,
                    'timestamp': media.taken_at.timestamp()
                })
                
            return posts
            
        except Exception as e:
            console.print(f"❌ Error getting posts for @{username}: {e}", style="red")
            return []
            
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def check_user_liked_post(self, post_id: str, target_username: str) -> bool:
        """Check if a user liked a specific post"""
        try:
            self._sleep()
            
            # Get post likers (limited by Instagram)
            likers = self.client.media_likers(post_id)
            
            for liker in likers:
                if liker.username == target_username:
                    return True
                    
            return False
            
        except Exception as e:
            # If we can't get likers (private, hidden, etc), return False
            return False
            
    def is_profile_public(self, username: str) -> bool:
        """Check if a profile is public"""
        try:
            user_info = self.client.user_info_by_username(username)
            return not user_info.is_private
        except Exception:
            return False
