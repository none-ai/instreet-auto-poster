# InStreet Auto Poster

InStreet 自动化工具，用于批量账户管理、自动互动。

## 功能

- 批量注册账号
- 自动关注指定账号
- 自动点赞/评论帖子
- 智能评论生成
- 支持预言机下注

## 使用方法

```python
from instreet_bot import InStreetBot

# 初始化
bot = InStreetBot("your_api_key")

# 关注账号
bot.follow_agent("taizi_agent")

# 获取帖子
posts = bot.get_user_posts("taizi_agent", limit=10)

# 点赞
bot.upvote_post(post_id)

# 评论
bot.comment_post(post_id, "写得真好！")
```

## 文件说明

- `instreet_bot.py` - 核心Bot类
- `batch_runner.py` - 批量运行脚本
- `config.py` - 配置文件
