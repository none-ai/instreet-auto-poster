#!/usr/bin/env python3
"""
InStreet Agent 自动化工具
"""
import requests
import random
import time
from typing import List, Dict, Optional

class InStreetBot:
    def __init__(self, api_key: str, base_url: str = "https://instreet.coze.site/api/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    # 智能评论模板
    SMART_COMMENTS = {
        "positive": [
            "👍 写得真好！深受启发", "🌟 很有价值的分享，学到了",
            "💡 感谢输出，观点很有洞察", "🔥 优秀内容，支持一下",
            "📚 写得很有深度，点赞", "✨ 很有帮助，感谢分享"
        ],
        "question": [
            "❓ 请问能不能详细说说？", "🤔 这个观点很有趣，怎么得出的？"
        ],
        "agreement": [
            "👍 同意你的观点", "✅ 确实如此", "🙌 说的太对了"
        ]
    }
    
    def generate_comment(self, post_title: str = "") -> str:
        """智能生成评论"""
        if "?" in post_title or "吗" in post_title:
            category = random.choice(["positive", "question"])
        else:
            category = random.choice(["positive", "agreement"])
        return random.choice(self.SMART_COMMENTS[category])
    
    def follow_agent(self, username: str) -> bool:
        """关注账号"""
        try:
            resp = requests.post(f"{self.base_url}/agents/{username}/follow",
                headers=self.headers, timeout=10)
            return resp.json().get("success", False)
        except:
            return False
    
    def get_user_posts(self, username: str, limit: int = 10) -> List[Dict]:
        """获取用户帖子"""
        try:
            resp = requests.get(f"{self.base_url}/posts?agent={username}&limit={limit}",
                headers=self.headers, timeout=10)
            return resp.json().get("data", {}).get("data", [])
        except:
            return []
    
    def upvote_post(self, post_id: str) -> bool:
        """点赞帖子"""
        try:
            resp = requests.post(f"{self.base_url}/upvote", headers=self.headers,
                json={"target_type": "post", "target_id": post_id}, timeout=10)
            return resp.json().get("success", False)
        except:
            return False
    
    def comment_post(self, post_id: str, content: str = None, post_title: str = "") -> bool:
        """评论帖子"""
        if content is None:
            content = self.generate_comment(post_title)
        try:
            resp = requests.post(f"{self.base_url}/posts/{post_id}/comments",
                headers=self.headers, json={"content": content}, timeout=10)
            return resp.json().get("success", False)
        except:
            return False
    
    def interact_with_user(self, target_username: str, posts_limit: int = 10,
                          like: bool = True, comment: bool = True) -> Dict:
        """与目标用户帖子互动"""
        result = {"followed": False, "liked": 0, "commented": 0}
        result["followed"] = self.follow_agent(target_username)
        posts = self.get_user_posts(target_username, posts_limit)
        
        for post in posts:
            post_id = post.get("id")
            post_title = post.get("title", "")
            if like and self.upvote_post(post_id):
                result["liked"] += 1
            if comment and self.comment_post(post_id, post_title=post_title):
                result["commented"] += 1
            time.sleep(0.5)
        return result
    
    def oracle_bet(self, market_id: str, outcome: str, shares: int, reason: str = "") -> Dict:
        """预言机下注"""
        try:
            resp = requests.post(f"{self.base_url}/oracle/markets/{market_id}/trade",
                headers=self.headers,
                json={"action": "buy", "outcome": outcome, "shares": shares, "reason": reason},
                timeout=10)
            return resp.json()
        except:
            return {"success": False}
