#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
直接下载模块单元测试
"""

import os
import sys
import requests
import unittest
from unittest.mock import patch, mock_open, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.download.direct import DirectDownloader


class TestDirectDownloader(unittest.TestCase):
    """直接下载模块测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 模拟配置管理器
        self.mock_config_patcher = patch('pixiv_tag_downloader.download.direct.get_config_manager')
        self.mock_config_manager = self.mock_config_patcher.start()
        
        # 配置模拟对象
        self.mock_config = MagicMock()
        self.mock_config_manager.return_value = self.mock_config
        
        # 设置默认配置
        self.mock_config.get.side_effect = lambda key, default=None: {
            'http.headers': {'User-Agent': 'Test Agent'},
            'http.use_proxy': False,
            'download.timeout': 10,
            'download.retries': 2,
            'download.delay.min': 0,
            'download.delay.max': 0,
            'output.overwrite': False,
            'logging.verbose_progress': False,
        }.get(key, default)
        
        # 创建下载器实例
        self.downloader = DirectDownloader()
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        self.mock_config_patcher.stop()
    
    def test_download_file_success(self):
        """测试成功下载文件"""
        # 准备测试数据
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        referer = "https://www.pixiv.net/"
        
        # 模拟 requests.get 返回值
        mock_response = MagicMock()
        mock_response.headers.get.return_value = "1024"
        mock_response.iter_content.return_value = [b'test data']
        mock_response.raise_for_status = MagicMock()
        
        # 模拟文件存储
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs') as mock_makedirs, \
             patch('builtins.open', mock_open()) as mock_file, \
             patch('requests.get', return_value=mock_response) as mock_get, \
             patch('tqdm') as mock_tqdm:
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path, referer)
            
            # 验证结果
            self.assertTrue(result)
            mock_makedirs.assert_called_once_with(os.path.dirname(save_path), exist_ok=True)
            mock_get.assert_called_once()
            
            # 验证请求参数
            _, kwargs = mock_get.call_args
            self.assertEqual(kwargs['timeout'], 10)
            self.assertTrue('Referer' in kwargs['headers'])
            self.assertEqual(kwargs['headers']['Referer'], referer)
            
            # 验证文件写入
            mock_file.assert_called_once_with(save_path, 'wb')
            file_handle = mock_file()
            file_handle.write.assert_called_with(b'test data')
    
    def test_download_file_exists(self):
        """测试下载时文件已存在且不覆盖"""
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        
        # 模拟文件已存在
        with patch('os.path.exists', return_value=True), \
             patch('requests.get') as mock_get:
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path)
            
            # 验证结果：成功返回但没有实际下载
            self.assertTrue(result)
            mock_get.assert_not_called()
    
    def test_download_file_retry_success(self):
        """测试下载重试成功"""
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        
        # 第一次请求失败，第二次成功
        mock_response_success = MagicMock()
        mock_response_success.headers.get.return_value = "1024"
        mock_response_success.iter_content.return_value = [b'test data']
        mock_response_success.raise_for_status = MagicMock()
        
        # 设置第一次请求会抛出异常
        mock_get = MagicMock(side_effect=[
            requests.exceptions.RequestException("Connection error"),
            mock_response_success
        ])
        
        # 模拟文件存储
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs'), \
             patch('builtins.open', mock_open()), \
             patch('requests.get', mock_get), \
             patch('tqdm'):
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path)
            
            # 验证结果
            self.assertTrue(result)
            # 验证请求被调用了两次（一次失败一次成功）
            self.assertEqual(mock_get.call_count, 2)
    
    def test_download_file_all_retries_fail(self):
        """测试所有下载重试都失败"""
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        
        # 所有请求都失败
        mock_get = MagicMock(side_effect=requests.exceptions.RequestException("Connection error"))
        
        # 模拟文件存储
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs'), \
             patch('requests.get', mock_get):
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path)
            
            # 验证结果
            self.assertFalse(result)
            # 验证请求被调用了三次（初始请求 + 两次重试）
            self.assertEqual(mock_get.call_count, 3)


if __name__ == '__main__':
    unittest.main()
