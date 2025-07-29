#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import json

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 创建会话
session = requests.Session()

# 从cookie.txt读取Cookie
try:
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
        logger.debug(f"设置Cookie: {name}={value}")
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://www.pixiv.net/',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest',
        'dnt': '1'
    }
    
    # 尝试请求
    response = session.get('https://www.pixiv.net/ajax/user/self', headers=headers)
    logger.debug(f"状态码: {response.status_code}")
    logger.debug(f"响应头: {dict(response.headers)}")
    
    # 打印响应内容
    try:
        data = response.json()
        print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        logger.error(f"解析响应内容失败: {e}")
        print(f"响应内容: {response.text}")
        
except Exception as e:
    logger.error(f"发生错误: {e}", exc_info=True)
