#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cookie认证模块单元测试
"""

import os
import sys
import unittest
import tempfile
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.auth.cookie import CookieManager


class TestCookieManager(unittest.TestCase):
    """Cookie管理器测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 创建一个临时目录
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cookie_path = os.path.join(self.temp_dir.name, 'cookie.txt')
        
        # 测试Cookie内容
        self.test_cookie = "PHPSESSID=abc123; device_token=def456; privacy_policy_agreement=1"
        
        # 写入测试Cookie文件
        with open(self.cookie_path, 'w', encoding='utf-8') as f:
            f.write(self.test_cookie)
        
        # 创建Cookie管理器实例
        self.cookie_manager = CookieManager(cookie_path=self.cookie_path)
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        # 清理临时目录
        self.temp_dir.cleanup()
    
    def test_load_cookie_success(self):
        """测试成功加载Cookie文件"""
        # 加载Cookie
        success, message = self.cookie_manager.load_cookie()
        
        # 验证加载成功
        self.assertTrue(success)
        self.assertIn("成功", message)
    
    def test_load_cookie_file_not_found(self):
        """测试加载不存在的Cookie文件"""
        # 使用不存在的Cookie路径
        cookie_manager = CookieManager(cookie_path='non_existent_file.txt')
        
        # 加载Cookie
        success, message = cookie_manager.load_cookie()
        
        # 验证加载失败
        self.assertFalse(success)
        self.assertIn("找不到", message)
    
    def test_load_cookie_empty_file(self):
        """测试加载空的Cookie文件"""
        # 创建空Cookie文件
        empty_cookie_path = os.path.join(self.temp_dir.name, 'empty_cookie.txt')
        open(empty_cookie_path, 'w').close()
        
        # 使用空Cookie路径
        cookie_manager = CookieManager(cookie_path=empty_cookie_path)
        
        # 加载Cookie
        success, message = cookie_manager.load_cookie()
        
        # 验证加载失败
        self.assertFalse(success)
        self.assertIn("为空", message)
    
    def test_load_cookie_invalid_format(self):
        """测试加载格式无效的Cookie文件"""
        # 创建格式无效的Cookie文件
        invalid_cookie_path = os.path.join(self.temp_dir.name, 'invalid_cookie.txt')
        with open(invalid_cookie_path, 'w', encoding='utf-8') as f:
            f.write("这不是有效的Cookie格式")
        
        # 使用无效Cookie路径
        cookie_manager = CookieManager(cookie_path=invalid_cookie_path)
        
        # 加载Cookie
        success, message = cookie_manager.load_cookie()
        
        # 验证加载成功但有警告
        self.assertTrue(success)  # 即使格式不是标准的，我们仍然尝试使用它
        self.assertIn("可能无效", message)
    
    @patch('requests.Session')
    def test_get_session(self, mock_session):
        """测试获取会话对象"""
        # 模拟Session
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # 加载Cookie
        self.cookie_manager.load_cookie()
        
        # 获取会话
        session = self.cookie_manager.get_session()
        
        # 验证会话
        self.assertEqual(session, mock_session_instance)
        
        # 验证Cookie已设置
        cookie_dict = self.cookie_manager._parse_cookie_to_dict(self.test_cookie)
        for key, value in cookie_dict.items():
            mock_session_instance.cookies.set.assert_any_call(key, value)
    
    @patch('requests.Session')
    def test_test_connection_success(self, mock_session):
        """测试连接测试成功"""
        # 模拟Session
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # 模拟成功响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'body': {
                'name': 'TestUser',
                'userId': '12345'
            }
        }
        mock_session_instance.get.return_value = mock_response
        
        # 加载Cookie
        self.cookie_manager.load_cookie()
        
        # 测试连接
        success, result = self.cookie_manager.test_connection()
        
        # 验证测试成功
        self.assertTrue(success)
        self.assertEqual(result['name'], 'TestUser')
        self.assertEqual(result['userId'], '12345')
    
    @patch('requests.Session')
    def test_test_connection_failure(self, mock_session):
        """测试连接测试失败"""
        # 模拟Session
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # 模拟HTTP错误
        mock_session_instance.get.side_effect = Exception("Connection error")
        
        # 加载Cookie
        self.cookie_manager.load_cookie()
        
        # 测试连接
        success, result = self.cookie_manager.test_connection()
        
        # 验证测试失败
        self.assertFalse(success)
        self.assertIn("连接失败", result)
    
    @patch('requests.Session')
    def test_test_connection_unauthorized(self, mock_session):
        """测试连接测试未授权"""
        # 模拟Session
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # 模拟未授权响应
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': 'Unauthorized'}
        mock_session_instance.get.return_value = mock_response
        
        # 加载Cookie
        self.cookie_manager.load_cookie()
        
        # 测试连接
        success, result = self.cookie_manager.test_connection()
        
        # 验证测试失败
        self.assertFalse(success)
        self.assertIn("未授权", result)
    
    def test_parse_cookie_to_dict(self):
        """测试解析Cookie字符串为字典"""
        # 解析Cookie
        cookie_dict = self.cookie_manager._parse_cookie_to_dict(self.test_cookie)
        
        # 验证解析结果
        self.assertEqual(cookie_dict['PHPSESSID'], 'abc123')
        self.assertEqual(cookie_dict['device_token'], 'def456')
        self.assertEqual(cookie_dict['privacy_policy_agreement'], '1')


if __name__ == '__main__':
    unittest.main()
