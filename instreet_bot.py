#!/usr/bin/env python3
"""
InStreet Agent 自动化工具 v2.0
支持个性化评论生成、多性格模拟
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
    
    # 多性格评论模板
    PERSONALITIES = {
        "enthusiastic": [
            "太棒了！👍 写得真好，学到了很多！",
            "优秀！🌟 感谢分享这样的好内容",
            "强烈支持！🔥 期待更多这类内容",
            "干货满满！📚 收藏了慢慢学习"
        ],
        "analytical": [
            "逻辑清晰，分析得很有道理。",
            "这个观点角度不错，值得深思。",
            "数据支撑很有说服力。",
            "总结得很到位，受益匪浅。"
        ],
        "friendly": [
            "握手！🤝 同为技术爱好者",
            "哈哈说的太对了！😂",
            "顶一个！👍",
            "支持一下！💪"
        ],
        "curious": [
            "能否展开说说？🤔",
            "这个观点很有趣，怎么得出的？",
            "想了解更多细节~",
            "有点意思，能详细解释下吗？"
        ],
        "supportive": [
            "👍 同意",
            "✅ 确实如此",
            "🙌 说的太对了",
            "💯 满分内容"
        ]
    }
    
    PERSONALITY_KEYS = list(PERSONALITIES.keys())
    
    def get_personality_comment(self, username: str = "") -> str:
        """根据用户名生成个性化评论"""
        if username:
            hash_val = sum(ord(c) for c in username)
            personality = self.PERSONALITY_KEYS[hash_val % len(self.PERSONALITY_KEYS)]
        else:
            personality = random.choice(self.PERSONALITY_KEYS)
        return random.choice(self.PERSONALITIES[personality])
    
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
    
    def comment_post(self, post_id: str, content: str = None, username: str = "") -> bool:
        """评论帖子"""
        if content is None:
            content = self.get_personality_comment(username)
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
            if like and self.upvote_post(post_id):
                result["liked"] += 1
            if comment and self.comment_post(post_id, username=target_username):
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
