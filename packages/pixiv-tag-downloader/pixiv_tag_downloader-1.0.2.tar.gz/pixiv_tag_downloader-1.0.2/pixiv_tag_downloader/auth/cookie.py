#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
认证模块，负责处理Cookie读取和会话管理
"""

import os
import logging
import requests
from typing import Dict, Optional, Tuple, Union


class CookieManager:
    """Cookie管理类，负责读取Cookie文件和创建会话"""
    
    def __init__(self, cookie_path: str = "cookie.txt"):
        """
        初始化Cookie管理器
        
        Args:
            cookie_path: Cookie文件路径，默认为当前目录下的cookie.txt
        """
        self.logger = logging.getLogger(__name__)
        self.cookie_path = cookie_path
        self.session = requests.Session()
    
    def load_cookie(self) -> Tuple[bool, str]:
        """
        从文件加载Cookie
        
        Returns:
            Tuple[bool, str]: (是否成功, 错误消息)
        """
        try:
            if not os.path.exists(self.cookie_path):
                return False, f"Cookie文件不存在: {self.cookie_path}"
                
            with open(self.cookie_path, 'r', encoding='utf-8') as f:
                cookie_str = f.read().strip()
                
            if not cookie_str:
                return False, "Cookie文件为空"
                
            cookies = self.parse_cookie_string(cookie_str)
            if not cookies:
                return False, "Cookie格式不正确或为空"
                
            # 检查必要的Cookie
            if 'PHPSESSID' not in cookies:
                return False, "Cookie中缺少PHPSESSID，可能无效"
                
            # 将Cookie添加到会话
            for name, value in cookies.items():
                self.session.cookies.set(name, value, domain='.pixiv.net')
            
            self.logger.info(f"已成功加载Cookie文件，Cookie数量: {len(cookies)}")
            return True, ""
        except Exception as e:
            return False, f"加载Cookie时出错: {str(e)}"
    
    def parse_cookie_string(self, cookie_str: str) -> Dict[str, str]:
        """
        解析Cookie字符串为字典
        
        Args:
            cookie_str: Cookie字符串，格式为"key1=value1; key2=value2"
            
        Returns:
            Dict[str, str]: Cookie字典
        """
        cookies = {}
        # 使用与 test_debug.py 类似的解析逻辑，以处理潜在的格式边缘情况
        raw_pairs = cookie_str.split(';')
        
        for pair_segment in raw_pairs:
            # 每个段落必须包含 '=' 才是一个有效的cookie键值对
            if '=' in pair_segment:
                key, value = pair_segment.split('=', 1)
                # 分别去除键和值两端的空白字符
                key_stripped = key.strip()
                value_stripped = value.strip()
                # 确保 stripping 后 key 不是空的
                if key_stripped:
                    cookies[key_stripped] = value_stripped
        
        return cookies
    
    def test_connection(self) -> Tuple[bool, Union[str, Dict]]:
        """
        测试使用当前Cookie的连接是否有效
        
        Returns:
            Tuple[bool, Union[str, Dict]]: (是否成功, 错误消息或用户信息)
        """
        try:
            # 设置更新的请求头，模拟更真实的浏览器环境
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Referer': 'https://www.pixiv.net/',
                'Accept': 'application/json',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # 尝试访问需要登录的Pixiv API
            response = self.session.get(
                'https://www.pixiv.net/ajax/user/self',
                headers=headers
            )            # 检查连接和响应
            if response.status_code != 200:
                return False, f"服务器返回错误状态码: {response.status_code}"
                
            data = response.json()
            self.logger.debug(f"Pixiv API Response: {data}") # 添加这行来打印完整的响应
            if data.get('error') is not None and data.get('error'):
                error_message = data.get('message', '未知错误')
                return False, f"API返回错误: {error_message}"
                  # 提取用户信息
            user_data = data.get('userData') # 修改此行，将 'body' 改为 'userData'
            if user_data is None:
                return False, "无法获取用户数据，服务器返回null"
            elif not user_data:
                return False, "无法获取用户数据，Cookie可能已过期"
                
            self.logger.info("Cookie验证成功，成功获取用户信息")
            return True, user_data
        except requests.RequestException as e:
            return False, f"网络请求错误: {str(e)}"
        except ValueError as e:
            return False, f"解析响应数据错误: {str(e)}"
        except Exception as e:
            return False, f"测试连接时发生错误: {str(e)}"
    
    def get_session(self) -> requests.Session:
        """
        获取已配置的请求会话
        
        Returns:
            requests.Session: 配置好的会话对象
        """
        return self.session


# 全局Cookie管理器实例
_cookie_manager = None


def get_cookie_manager(cookie_path: Optional[str] = None) -> CookieManager:
    """
    获取全局Cookie管理器实例
    
    Args:
        cookie_path: Cookie文件路径，仅在第一次调用时有效
        
    Returns:
        CookieManager: Cookie管理器实例
    """
    global _cookie_manager
    if (_cookie_manager is None):
        _cookie_manager = CookieManager(cookie_path or "cookie.txt")
    return _cookie_manager