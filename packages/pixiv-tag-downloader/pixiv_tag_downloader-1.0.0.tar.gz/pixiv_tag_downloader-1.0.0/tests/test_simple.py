#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

# 创建会话
session = requests.Session()

# 从cookie.txt读取Cookie
with open('cookie.txt', 'r', encoding='utf-8') as f:
    cookie_str = f.read().strip()
    
# 解析Cookie
cookies = {}
for pair in cookie_str.split(';'):
    if '=' in pair:
        key, value = pair.split('=', 1)
        cookies[key.strip()] = value.strip()

# 设置Cookie
for name, value in cookies.items():
    session.cookies.set(name, value, domain='.pixiv.net')
    print(f"设置Cookie: {name}={value[:5]}***")

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.pixiv.net/',
    'Accept': 'application/json',
}

print("正在发送请求...")
response = session.get('https://www.pixiv.net/ajax/user/self', headers=headers)
print(f"状态码: {response.status_code}")

# 打印响应内容
try:
    data = response.json()
    print(f"错误状态: {data.get('error')}")
    print(f"消息: {data.get('message')}")
except Exception as e:
    print(f"解析响应内容失败: {e}")
    print(f"响应内容: {response.text[:200]}")
