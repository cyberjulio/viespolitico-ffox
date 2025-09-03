import sqlite3
import json
import time
from pathlib import Path
from typing import Optional, List, Dict

class Cache:
    def __init__(self, cache_duration_hours: int = 24):
        self.db_path = Path("data/cache.db")
        self.cache_duration = cache_duration_hours * 3600  # Convert to seconds
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite database"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS followings_cache (
                    username TEXT PRIMARY KEY,
                    followings TEXT,
                    timestamp REAL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS posts_cache (
                    profile_username TEXT,
                    post_data TEXT,
                    timestamp REAL,
                    PRIMARY KEY (profile_username)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analysis_cache (
                    target_username TEXT PRIMARY KEY,
                    result TEXT,
                    timestamp REAL
                )
            """)
            
    def is_expired(self, timestamp: float) -> bool:
        """Check if cached data is expired"""
        return (time.time() - timestamp) > self.cache_duration
        
    def get_followings(self, username: str) -> Optional[List[str]]:
        """Get cached followings for a user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT followings, timestamp FROM followings_cache WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            
            if row and not self.is_expired(row[1]):
                return json.loads(row[0])
        return None
        
    def set_followings(self, username: str, followings: List[str]):
        """Cache followings for a user"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO followings_cache (username, followings, timestamp) VALUES (?, ?, ?)",
                (username, json.dumps(followings), time.time())
            )
            
    def get_posts(self, profile_username: str) -> Optional[List[Dict]]:
        """Get cached posts for a profile"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT post_data, timestamp FROM posts_cache WHERE profile_username = ?",
                (profile_username,)
            )
            row = cursor.fetchone()
            
            if row and not self.is_expired(row[1]):
                return json.loads(row[0])
        return None
        
    def set_posts(self, profile_username: str, posts: List[Dict]):
        """Cache posts for a profile"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO posts_cache (profile_username, post_data, timestamp) VALUES (?, ?, ?)",
                (profile_username, json.dumps(posts), time.time())
            )
            
    def get_analysis(self, target_username: str) -> Optional[Dict]:
        """Get cached analysis result"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT result, timestamp FROM analysis_cache WHERE target_username = ?",
                (target_username,)
            )
            row = cursor.fetchone()
            
            if row and not self.is_expired(row[1]):
                return json.loads(row[0])
        return None
        
    def set_analysis(self, target_username: str, result: Dict):
        """Cache analysis result"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO analysis_cache (target_username, result, timestamp) VALUES (?, ?, ?)",
                (target_username, json.dumps(result), time.time())
            )
