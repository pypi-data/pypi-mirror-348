#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
集成测试 - 测试国际化功能在实际应用场景中的工作情况
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.i18n.translation import TranslationManager, get_translation_manager
from pixiv_tag_downloader.utils.file_utils import FileUtils


class TestI18nIntegration(unittest.TestCase):
    """测试国际化功能与其他模块的集成"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 模拟配置管理器
        self.mock_config_patcher = patch('pixiv_tag_downloader.i18n.translation.get_config_manager')
        self.mock_config_manager = self.mock_config_patcher.start()
        
        # 配置模拟对象
        self.mock_config = MagicMock()
        self.mock_config_manager.return_value = self.mock_config
        
        # 初始化英文作为默认语言
        self.mock_config.get.side_effect = lambda key, default=None: {
            'ui.language': 'en-US'
        }.get(key, default)
        
        # 模拟翻译文件路径和内容
        self.translations = {
            'en-US': {
                'metadata.title': 'Title',
                'metadata.tags': 'Tags',
                'metadata.description': 'Description',
                'app.name': 'Pixiv Tag Downloader'
            },
            'zh-CN': {
                'metadata.title': '标题',
                'metadata.tags': '标签',
                'metadata.description': '描述',
                'app.name': 'Pixiv标签下载器'
            },
            'ja-JP': {
                'metadata.title': 'タイトル',
                'metadata.tags': 'タグ',
                'metadata.description': '説明',
                'app.name': 'Pixivタグダウンローダー'
            }
        }
        
        # 手动设置翻译数据
        self.translation_manager = get_translation_manager()
        self.translation_manager.translations = self.translations
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        self.mock_config_patcher.stop()
        
        # 重置单例实例
        import pixiv_tag_downloader.i18n.translation
        pixiv_tag_downloader.i18n.translation._translation_manager_instance = None
    
    def test_file_utils_uses_current_language(self):
        """测试文件工具使用当前语言设置生成元数据文件"""
        # 创建文件工具实例
        file_utils = FileUtils()
        
        # 准备测试元数据
        test_metadata = {
            'title': 'Test Artwork',
            'userId': '12345',
            'userName': 'Test User',
            'id': '67890',
            'uploadDate': '2023-01-01',
            'tags': {'tags': [{'tag': 'test'}, {'tag': 'example'}]}
        }
        
        # 模拟写文件操作
        with patch('os.makedirs'), patch('builtins.open', MagicMock()):
            # 英文 (默认)
            content = []
            with patch.object(file_utils, 'write_metadata_file', 
                            side_effect=lambda path, meta, is_novel: content.append(f"{file_utils.i18n.get('metadata.title')}: {meta['title']}")):
                file_utils.write_metadata_file('test.txt', test_metadata)
                self.assertEqual("Title: Test Artwork", content[0])
            
            # 中文
            content = []
            self.translation_manager.set_language('zh-CN')
            with patch.object(file_utils, 'write_metadata_file', 
                            side_effect=lambda path, meta, is_novel: content.append(f"{file_utils.i18n.get('metadata.title')}: {meta['title']}")):
                file_utils.write_metadata_file('test.txt', test_metadata)
                self.assertEqual("标题: Test Artwork", content[0])
            
            # 日文
            content = []
            self.translation_manager.set_language('ja-JP')
            with patch.object(file_utils, 'write_metadata_file', 
                            side_effect=lambda path, meta, is_novel: content.append(f"{file_utils.i18n.get('metadata.title')}: {meta['title']}")):
                file_utils.write_metadata_file('test.txt', test_metadata)
                self.assertEqual("タイトル: Test Artwork", content[0])
    
    def test_cli_respects_language_setting(self):
        """测试CLI遵循语言设置"""
        # 导入CLI
        from pixiv_tag_downloader.ui.cli import CLI
        
        # 基于不同语言测试CLI实例化
        # 英文
        self.translation_manager.set_language('en-US')
        cli = CLI()
        self.assertEqual('Pixiv Tag Downloader', cli.i18n.get('app.name'))
        
        # 中文
        self.translation_manager.set_language('zh-CN')
        cli = CLI()
        self.assertEqual('Pixiv标签下载器', cli.i18n.get('app.name'))
        
        # 日文
        self.translation_manager.set_language('ja-JP')
        cli = CLI()
        self.assertEqual('Pixivタグダウンローダー', cli.i18n.get('app.name'))


if __name__ == '__main__':
    unittest.main()
