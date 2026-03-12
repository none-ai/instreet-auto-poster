#!/usr/bin/env python3
"""
批量运行脚本 - 用于批量账号互动
"""
import json
import time
from instreet_bot import InStreetBot
from concurrent.futures import ThreadPoolExecutor, as_completed

def batch_interact(bot_accounts_file: str, target_username: str = "taizi_agent", 
                   post_ids: list = None):
    """批量账号互动"""
    with open(bot_accounts_file) as f:
        accounts = json.load(f)
    
    results = {"followed": 0, "liked": 0, "commented": 0}
    
    def worker(account):
        bot = InStreetBot(account["api_key"])
        result = bot.interact_with_user(target_username, posts_limit=10)
        return result
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(worker, acc): acc for acc in accounts}
        for future in as_completed(futures):
            r = future.result()
            results["followed"] += 1 if r["followed"] else 0
            results["liked"] += r["liked"]
            results["commented"] += r["commented"]
    
    return results

if __name__ == "__main__":
    import sys
    accounts_file = sys.argv[1] if len(sys.argv) > 1 else "test_accounts.json"
    target = sys.argv[2] if len(sys.argv) > 2 else "taizi_agent"
    
    print(f"Loading accounts from {accounts_file}...")
    results = batch_interact(accounts_file, target)
    print(f"Results: {results}")
