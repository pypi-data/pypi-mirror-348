#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

try:
    print("开始测试...")
    
    # 创建会话
    session = requests.Session()
    
    # 从cookie.txt读取Cookie
    print("读取cookie.txt...")
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie_str = f.read().strip()
        print(f"Cookie长度: {len(cookie_str)}")
        
    # 解析Cookie
    cookies = {}
    for pair in cookie_str.split(';'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    # 打印解析出的cookie数量
    print(f"解析出的Cookie数量: {len(cookies)}")
    
    # 设置Cookie
    for name, value in cookies.items():
        session.cookies.set(name, value, domain='.pixiv.net')
        value_preview = value[:5] + "***" if len(value) > 5 else "***"
        print(f"设置Cookie: {name}={value_preview}")
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://www.pixiv.net/',
        'Accept': 'application/json',
    }
    
    print("正在发送请求...")
    url = 'https://www.pixiv.net/ajax/user/self'
    print(f"URL: {url}")
    response = session.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    
    # 打印响应头
    print("响应头:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    # 打印响应内容
    print("解析响应内容...")
    response_text = response.text
    print(f"响应长度: {len(response_text)}")
    print(f"前200字符: {response_text[:200]}")
    
    data = response.json()
    print(f"错误状态: {data.get('error')}")
    print(f"消息: {data.get('message')}")
    
    body = data.get('body')
    print(f"主体数据类型: {type(body)}")
    print(f"主体数据: {body}")
    
    # 保存完整响应到文件
    print("保存响应到文件...")
    with open('api_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("完整响应已保存到api_response.json")
    
    print("测试完成")
except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    print(traceback.format_exc())
