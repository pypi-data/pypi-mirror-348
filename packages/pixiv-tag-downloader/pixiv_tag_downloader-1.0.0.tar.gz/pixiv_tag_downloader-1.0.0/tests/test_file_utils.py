#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件工具模块单元测试
"""

import os
import sys
import unittest
from unittest.mock import patch, mock_open

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.utils.file_utils import FileUtils


class TestFileUtils(unittest.TestCase):
    """文件工具测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        self.file_utils = FileUtils()
    
    def test_write_metadata_file_artwork(self):
        """测试写入作品元数据文件"""
        # 准备测试数据
        metadata = {
            'title': 'Test Artwork',
            'userId': '12345',
            'userName': 'Test User',
            'id': '67890',
            'uploadDate': '2023-01-01T12:00:00+00:00',
            'tags': {
                'tags': [
                    {'tag': 'test'},
                    {'tag': 'example'}
                ]
            },
            'description': 'This is a test artwork'
        }
        
        # 模拟写文件操作
        with patch('os.makedirs') as mock_makedirs, \
             patch('builtins.open', mock_open()) as mock_file:
            
            # 调用被测试方法
            result = self.file_utils.write_metadata_file('/test/path/metadata.txt', metadata)
            
            # 验证结果
            self.assertTrue(result)
            mock_makedirs.assert_called_once_with('/test/path', exist_ok=True)
            mock_file.assert_called_once_with('/test/path/metadata.txt', 'w', encoding='utf-8')
            
            # 验证写入的内容包含关键信息
            write_handle = mock_file()
            self.assertTrue(any('标题 (Title): Test Artwork' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('作者UID (Author UID): 12345' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('作品PID (Artwork PID): 67890' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('上传时间 (Upload Date): 2023-01-01T12:00:00+00:00' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('标签 (Tags): test, example' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('描述 (Description):' in args[0] for args, _ in write_handle.write.call_args_list))
    
    def test_write_metadata_file_novel(self):
        """测试写入小说元数据文件"""
        # 准备小说测试数据
        metadata = {
            'title': 'Test Novel',
            'userId': '12345',
            'userName': 'Test User',
            'id': '67890',
            'createDate': '2023-01-01T12:00:00+00:00',
            'tags': [
                {'tag': 'novel'},
                {'tag': 'story'}
            ],
            'description': 'This is a test novel',
            'content': 'Once upon a time...'
        }
        
        # 模拟写文件操作
        with patch('os.makedirs') as mock_makedirs, \
             patch('builtins.open', mock_open()) as mock_file:
            
            # 调用被测试方法
            result = self.file_utils.write_metadata_file('/test/path/novel.txt', metadata, is_novel=True)
            
            # 验证结果
            self.assertTrue(result)
            mock_makedirs.assert_called_once_with('/test/path', exist_ok=True)
            mock_file.assert_called_once_with('/test/path/novel.txt', 'w', encoding='utf-8')
            
            # 验证写入的内容包含关键信息
            write_handle = mock_file()
            self.assertTrue(any('标题 (Title): Test Novel' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('作者UID (Author UID): 12345' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('小说PID (Novel PID): 67890' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('创建时间 (Create Date): 2023-01-01T12:00:00+00:00' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('标签 (Tags): novel, story' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('正文 (Content):' in args[0] for args, _ in write_handle.write.call_args_list))
            self.assertTrue(any('Once upon a time...' in args[0] for args, _ in write_handle.write.call_args_list))
    
    def test_write_metadata_file_error(self):
        """测试写入元数据文件时出错"""
        # 准备测试数据
        metadata = {
            'title': 'Test Artwork',
            'userId': '12345',
            'userName': 'Test User',
            'id': '67890'
        }
        
        # 模拟写文件操作抛出异常
        with patch('os.makedirs') as mock_makedirs, \
             patch('builtins.open', side_effect=IOError("测试错误")):
            
            # 调用被测试方法
            result = self.file_utils.write_metadata_file('/test/path/metadata.txt', metadata)
            
            # 验证结果
            self.assertFalse(result)
            mock_makedirs.assert_called_once_with('/test/path', exist_ok=True)
    
    def test_write_metadata_file_with_series(self):
        """测试写入包含系列信息的元数据文件"""
        # 准备测试数据，包含系列信息
        metadata = {
            'title': 'Test Artwork in Series',
            'userId': '12345',
            'userName': 'Test User',
            'id': '67890',
            'uploadDate': '2023-01-01T12:00:00+00:00',
            'tags': {'tags': [{'tag': 'test'}, {'tag': 'series'}]},
            'seriesNavData': {
                'title': 'Test Series',
                'id': '1001'
            }
        }
        
        # 模拟写文件操作
        with patch('os.makedirs') as mock_makedirs, \
             patch('builtins.open', mock_open()) as mock_file:
            
            # 调用被测试方法
            result = self.file_utils.write_metadata_file('/test/path/metadata.txt', metadata)
            
            # 验证结果
            self.assertTrue(result)
            
            # 验证写入的内容包含系列信息
            write_handle = mock_file()
            self.assertTrue(any('系列 (Series): Test Series / 1001' in args[0] for args, _ in write_handle.write.call_args_list))

if __name__ == '__main__':
    unittest.main()
