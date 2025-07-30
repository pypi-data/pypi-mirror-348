#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
国际化支持模块单元测试
"""

import os
import sys
import json
import unittest
import tempfile
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.i18n.translation import TranslationManager


class TestTranslationManager(unittest.TestCase):
    """翻译管理器测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 创建临时目录
        self.temp_dir = tempfile.TemporaryDirectory()
        self.translations_dir = os.path.join(self.temp_dir.name, 'translations')
        os.makedirs(self.translations_dir, exist_ok=True)
        
        # 准备测试翻译文件
        self.test_zh_trans = {
            "test.key1": "测试文本1",
            "test.key2": "你好，{name}！",
            "test.key3": "这是中文"
        }
        
        self.test_en_trans = {
            "test.key1": "Test text 1",
            "test.key2": "Hello, {name}!",
            "test.key3": "This is English"
        }
        
        # 写入测试翻译文件
        with open(os.path.join(self.translations_dir, 'zh-CN.json'), 'w', encoding='utf-8') as f:
            json.dump(self.test_zh_trans, f, ensure_ascii=False)
            
        with open(os.path.join(self.translations_dir, 'en-US.json'), 'w', encoding='utf-8') as f:
            json.dump(self.test_en_trans, f, ensure_ascii=False)
        
        # 模拟配置管理器
        self.mock_config_patcher = patch('pixiv_tag_downloader.i18n.translation.get_config_manager')
        self.mock_config_manager = self.mock_config_patcher.start()
        
        # 配置模拟对象
        self.mock_config = MagicMock()
        self.mock_config_manager.return_value = self.mock_config
        
        # 模拟配置获取
        self.mock_config.get.side_effect = lambda key, default=None: {
            'ui.language': 'zh-CN'
        }.get(key, default)
        
        # 模拟翻译文件路径
        with patch('pixiv_tag_downloader.i18n.translation.os.path.dirname', return_value=self.temp_dir.name):
            # 创建翻译管理器实例
            self.translation_manager = TranslationManager()
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        # 停止模拟
        self.mock_config_patcher.stop()
        
        # 清理临时目录
        self.temp_dir.cleanup()
    
    def test_load_translations(self):
        """测试加载翻译文件"""
        # 验证翻译已加载
        self.assertIn('zh-CN', self.translation_manager.translations)
        self.assertIn('en-US', self.translation_manager.translations)
        
        # 验证翻译内容
        self.assertEqual(self.test_zh_trans, self.translation_manager.translations['zh-CN'])
        self.assertEqual(self.test_en_trans, self.translation_manager.translations['en-US'])
    
    def test_get_translation(self):
        """测试获取翻译"""
        # 测试获取简单的字符串
        self.assertEqual("测试文本1", self.translation_manager.get("test.key1"))
        
        # 测试带格式化参数的字符串
        self.assertEqual("你好，World！", self.translation_manager.get("test.key2", name="World"))
        
        # 测试不存在的键
        self.assertEqual("test.nonexistent", self.translation_manager.get("test.nonexistent"))
        self.assertEqual("默认文本", self.translation_manager.get("test.nonexistent", default="默认文本"))
    
    def test_change_language(self):
        """测试更改语言"""
        # 更改为英文
        result = self.translation_manager.set_language('en-US')
        self.assertTrue(result)
        self.assertEqual('en-US', self.translation_manager.get_language())
        
        # 验证翻译已切换为英文
        self.assertEqual("Test text 1", self.translation_manager.get("test.key1"))
        self.assertEqual("Hello, World!", self.translation_manager.get("test.key2", name="World"))
        
        # 测试设置不存在的语言
        result = self.translation_manager.set_language('fr-FR')
        self.assertFalse(result)
        self.assertEqual('en-US', self.translation_manager.get_language())  # 语言没有改变
    
    def test_fallback_translation(self):
        """测试翻译回退机制"""
        # 添加一个只有部分翻译的日文翻译文件
        test_ja_trans = {
            "test.key1": "テストテキスト1"
            # 故意不包含 test.key2 和 test.key3
        }
        
        with open(os.path.join(self.translations_dir, 'ja-JP.json'), 'w', encoding='utf-8') as f:
            json.dump(test_ja_trans, f, ensure_ascii=False)
        
        # 重新加载翻译
        self.translation_manager._load_translations()
        
        # 切换到日文
        self.translation_manager.set_language('ja-JP')
        
        # 验证日文翻译存在的键
        self.assertEqual("テストテキスト1", self.translation_manager.get("test.key1"))
        
        # 验证缺失的日文翻译会回退到英文
        self.assertEqual("Hello, World!", self.translation_manager.get("test.key2", name="World"))
    
    def test_get_available_languages(self):
        """测试获取可用语言"""
        # 获取可用语言
        languages = self.translation_manager.get_available_languages()
        
        # 验证语言列表
        self.assertIn('zh-CN', languages)
        self.assertIn('en-US', languages)
        self.assertEqual('简体中文', languages['zh-CN'])
        self.assertEqual('English', languages['en-US'])


if __name__ == '__main__':
    unittest.main()
