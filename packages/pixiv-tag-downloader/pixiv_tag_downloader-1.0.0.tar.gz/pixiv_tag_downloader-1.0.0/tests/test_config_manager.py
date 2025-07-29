#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理模块单元测试
"""

import os
import sys
import unittest
import tempfile
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.config.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    """配置管理器测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 创建一个临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, 'test_config.yaml')
        
        # 基础测试配置
        self.test_config = {
            'output': {
                'root_dir': 'TestOutput',
                'templates': {
                    'main_dir': '{uid}_{username}',
                    'image_filename': '{date}_{pid}.{ext}'
                }
            },
            'download': {
                'method': 'direct',
                'threads': 2
            },
            'http': {
                'headers': {
                    'User-Agent': 'Test User Agent'
                }
            }
        }
        
        # 写入临时配置文件
        with open(self.config_path, 'w', encoding='utf-8') as f:
            import yaml
            yaml.dump(self.test_config, f)
        
        # 创建配置管理器实例
        self.config_manager = ConfigManager()
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        # 清理临时目录
        self.temp_dir.cleanup()
    
    def test_load_config(self):
        """测试加载配置文件"""
        # 加载临时配置文件
        result = self.config_manager.load_config(self.config_path)
        
        # 验证加载成功
        self.assertTrue(result)
        
        # 验证配置内容
        self.assertEqual(self.config_manager.get('output.root_dir'), 'TestOutput')
        self.assertEqual(self.config_manager.get('download.threads'), 2)
        self.assertEqual(self.config_manager.get('http.headers.User-Agent'), 'Test User Agent')
    
    def test_get_default_value(self):
        """测试获取不存在的配置项时返回默认值"""
        # 不存在的配置项
        value = self.config_manager.get('non_existent.config', 'default_value')
        self.assertEqual(value, 'default_value')
    
    def test_set_config_value(self):
        """测试设置配置值"""
        # 设置一个新值
        self.config_manager.set('download.threads', 8)
        self.assertEqual(self.config_manager.get('download.threads'), 8)
        
        # 设置一个新的配置路径
        self.config_manager.set('new.config.path', 'new_value')
        self.assertEqual(self.config_manager.get('new.config.path'), 'new_value')
    
    def test_to_dict(self):
        """测试转换为字典"""
        # 加载测试配置
        self.config_manager.load_config(self.config_path)
        
        # 获取配置字典
        config_dict = self.config_manager.to_dict()
        
        # 验证字典内容
        self.assertEqual(config_dict['output']['root_dir'], 'TestOutput')
        self.assertEqual(config_dict['download']['threads'], 2)
    
    def test_save_config(self):
        """测试保存配置"""
        # 加载测试配置
        self.config_manager.load_config(self.config_path)
        
        # 修改一个值
        self.config_manager.set('download.threads', 10)
        
        # 保存到新文件
        save_path = os.path.join(self.temp_dir.name, 'saved_config.yaml')
        self.config_manager.save(save_path)
        
        # 创建新的配置管理器并加载保存的文件
        new_manager = ConfigManager()
        new_manager.load_config(save_path)
        
        # 验证保存的值
        self.assertEqual(new_manager.get('download.threads'), 10)
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        # 尝试加载不存在的文件
        result = self.config_manager.load_config('non_existent_file.yaml')
        
        # 验证加载失败
        self.assertFalse(result)
    
    def test_default_config(self):
        """测试默认配置"""
        # 创建一个新的配置管理器（使用默认配置）
        default_config = ConfigManager()
        
        # 验证一些默认值
        self.assertEqual(default_config.get('output.root_dir'), 'Output')
        self.assertIsInstance(default_config.get('download.threads'), int)
    
    @patch('os.path.exists')
    @patch('pixiv_tag_downloader.config.config_manager.ConfigManager.load_config')
    def test_search_config_file(self, mock_load_config, mock_exists):
        """测试搜索配置文件"""
        # 设置模拟行为
        mock_exists.return_value = True
        mock_load_config.return_value = True
        
        # 创建新的配置管理器，触发搜索配置文件
        config = ConfigManager()
        
        # 验证尝试加载了默认配置文件
        mock_load_config.assert_called()


if __name__ == '__main__':
    unittest.main()
