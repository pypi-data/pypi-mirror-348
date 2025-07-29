#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aria2下载模块单元测试
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.download.aria2 import Aria2CLI, Aria2RPC


class TestAria2CLI(unittest.TestCase):
    """Aria2命令行下载模块测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 模拟配置管理器
        self.mock_config_patcher = patch('pixiv_tag_downloader.download.aria2.get_config_manager')
        self.mock_config_manager = self.mock_config_patcher.start()
        
        # 配置模拟对象
        self.mock_config = MagicMock()
        self.mock_config_manager.return_value = self.mock_config
        
        # 设置默认配置
        self.mock_config.get.side_effect = lambda key, default=None: {
            'http.headers': {'User-Agent': 'Test Agent', 'Cookie': 'test=123'},
            'download.delay.min': 0,
            'download.delay.max': 0,
            'output.overwrite': False,
            'download.aria2.params': {
                'max_connection_per_server': 5,
                'min_split_size': '1M',
                'split': 5
            },
            'download.retries': 2
        }.get(key, default)
        
        # 创建下载器实例
        self.downloader = Aria2CLI()
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        self.mock_config_patcher.stop()
    
    def test_download_file_success(self):
        """测试使用aria2c命令成功下载文件"""
        # 准备测试数据
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        referer = "https://www.pixiv.net/"
        
        # 模拟subprocess.run成功返回
        mock_process = MagicMock()
        mock_process.returncode = 0
        
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs') as mock_makedirs, \
             patch('subprocess.run', return_value=mock_process) as mock_run:
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path, referer)
            
            # 验证结果
            self.assertTrue(result)
            mock_makedirs.assert_called_once_with(os.path.dirname(save_path), exist_ok=True)
            mock_run.assert_called_once()
            
            # 验证命令行参数
            args, _ = mock_run.call_args
            command = args[0]
            self.assertIn('aria2c', command)
            self.assertIn(url, command)
            self.assertIn('--referer=' + referer, command)
            self.assertIn('--dir=' + os.path.dirname(save_path), command)
            self.assertIn('--out=' + os.path.basename(save_path), command)
    
    def test_download_file_exists(self):
        """测试下载时文件已存在且不覆盖"""
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        
        # 模拟文件已存在
        with patch('os.path.exists', return_value=True), \
             patch('subprocess.run') as mock_run:
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path)
            
            # 验证结果：成功返回但没有实际下载
            self.assertTrue(result)
            mock_run.assert_not_called()
    
    def test_download_file_failure(self):
        """测试使用aria2c命令下载文件失败"""
        # 准备测试数据
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        
        # 模拟subprocess.run返回错误
        mock_process = MagicMock()
        mock_process.returncode = 1
        
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs'), \
             patch('subprocess.run', return_value=mock_process):
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path)
            
            # 验证结果
            self.assertFalse(result)


class TestAria2RPC(unittest.TestCase):
    """Aria2 RPC下载模块测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 模拟配置管理器
        self.mock_config_patcher = patch('pixiv_tag_downloader.download.aria2.get_config_manager')
        self.mock_config_manager = self.mock_config_patcher.start()
        
        # 配置模拟对象
        self.mock_config = MagicMock()
        self.mock_config_manager.return_value = self.mock_config
        
        # 模拟xmlrpc.client.ServerProxy
        self.mock_xmlrpc_patcher = patch('xmlrpc.client.ServerProxy')
        self.mock_server_proxy = self.mock_xmlrpc_patcher.start()
        
        # 设置默认配置
        self.mock_config.get.side_effect = lambda key, default=None: {
            'http.headers': {'User-Agent': 'Test Agent', 'Cookie': 'test=123'},
            'download.delay.min': 0,
            'download.delay.max': 0,
            'output.overwrite': False,
            'download.aria2.rpc_url': 'http://localhost:6800/rpc',
            'download.aria2.rpc_token': 'test_token',
            'download.retries': 2
        }.get(key, default)
        
        # 创建下载器实例
        self.downloader = Aria2RPC()
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        self.mock_config_patcher.stop()
        self.mock_xmlrpc_patcher.stop()
    
    def test_download_file_success(self):
        """测试通过RPC成功下载文件"""
        # 准备测试数据
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        referer = "https://www.pixiv.net/"
        
        # 模拟RPC调用成功
        mock_server = MagicMock()
        self.mock_server_proxy.return_value = mock_server
        mock_server.aria2.addUri.return_value = "gid-12345"
        mock_server.aria2.tellStatus.return_value = {"status": "complete"}
        
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs') as mock_makedirs, \
             patch('time.sleep'):  # 忽略sleep延迟
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path, referer)
            
            # 验证结果
            self.assertTrue(result)
            mock_makedirs.assert_called_once_with(os.path.dirname(save_path), exist_ok=True)
            
            # 验证RPC调用
            mock_server.aria2.addUri.assert_called_once()
            args, _ = mock_server.aria2.addUri.call_args
            self.assertEqual(args[0], f"token:test_token")
            self.assertEqual(args[1], [url])
            
            # 验证参数包含referer和输出路径
            options = args[2]
            self.assertEqual(options['dir'], os.path.dirname(save_path))
            self.assertEqual(options['out'], os.path.basename(save_path))
            self.assertEqual(options['referer'], referer)
    
    def test_download_file_exists(self):
        """测试RPC下载时文件已存在且不覆盖"""
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        
        # 模拟文件已存在
        with patch('os.path.exists', return_value=True), \
             patch('xmlrpc.client.ServerProxy') as mock_proxy:
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path)
            
            # 验证结果：成功返回但没有实际下载
            self.assertTrue(result)
            mock_proxy.assert_not_called()
    
    def test_download_file_failure(self):
        """测试通过RPC下载文件失败"""
        # 准备测试数据
        url = "https://example.com/image.jpg"
        save_path = "/test/path/image.jpg"
        
        # 模拟RPC调用失败（超出等待时间）
        mock_server = MagicMock()
        self.mock_server_proxy.return_value = mock_server
        mock_server.aria2.addUri.return_value = "gid-12345"
        mock_server.aria2.tellStatus.return_value = {"status": "error", "errorMessage": "Download error"}
        
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs'), \
             patch('time.sleep'):  # 忽略sleep延迟
            
            # 调用被测试方法
            result = self.downloader.download_file(url, save_path)
            
            # 验证结果
            self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
