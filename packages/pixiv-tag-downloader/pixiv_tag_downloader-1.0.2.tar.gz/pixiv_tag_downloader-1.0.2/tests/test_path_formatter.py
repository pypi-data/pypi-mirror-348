#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
路径格式化工具单元测试
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.utils.path_formatter import PathFormatter


class TestPathFormatter(unittest.TestCase):
    """路径格式化器测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 模拟配置管理器
        self.mock_config = MagicMock()
        self.mock_config.get.side_effect = self._mock_config_get
        
        # 默认配置
        self.default_config = {
            'output.root_dir': 'TestOutput',
            'output.templates': {
                'main_dir': '{uid}_{username}/{type}/{series}',
                'image_filename': '{date}_{pid}_p{index}_{title}.{ext}',
                'novel_filename': '{date}_{pid}_{title}.txt',
                'date_format': 'yyyymmdd',
                'tag_separator': '_'
            },
            'output.overwrite': False,
            'output.pid_dir_with_title': True
        }
        
        # 创建路径格式化器实例
        with patch('pixiv_tag_downloader.utils.path_formatter.get_config_manager', return_value=self.mock_config):
            self.path_formatter = PathFormatter()
        
        # 测试元数据
        self.test_artwork_metadata = {
            'id': '12345678',
            'title': '测试作品',
            'userId': '87654321',
            'userName': '测试用户',
            'type': 'illust',
            'uploadDate': '2023-01-01T12:00:00+00:00',
            'pageCount': 1,
            'tags': {
                'tags': [
                    {'tag': 'tag1'},
                    {'tag': 'tag2'}
                ]
            }
        }
        
        self.test_manga_metadata = {
            'id': '12345679',
            'title': '测试漫画',
            'userId': '87654321',
            'userName': '测试用户',
            'type': 'manga',
            'uploadDate': '2023-01-02T12:00:00+00:00',
            'pageCount': 3,
            'tags': {
                'tags': [
                    {'tag': 'manga'},
                    {'tag': 'comic'}
                ]
            }
        }
        
        self.test_novel_metadata = {
            'id': '12345680',
            'title': '测试小说',
            'userId': '87654321',
            'userName': '测试用户',
            'type': 'novel',
            'uploadDate': '2023-01-03T12:00:00+00:00',
            'tags': [
                {'tag': 'novel'},
                {'tag': 'story'}
            ]
        }
        
        # 带系列的元数据
        self.test_series_metadata = {
            'id': '12345681',
            'title': '系列作品',
            'userId': '87654321',
            'userName': '测试用户',
            'type': 'illust',
            'uploadDate': '2023-01-04T12:00:00+00:00',
            'pageCount': 1,
            'seriesNavData': [{'title': '测试系列', 'id': '9876'}],
            'tags': {
                'tags': [
                    {'tag': 'series'},
                    {'tag': 'test'}
                ]
            }
        }
    
    def _mock_config_get(self, key, default=None):
        """模拟配置获取方法"""
        if key in self.default_config:
            return self.default_config[key]
        
        # 嵌套键处理
        if '.' in key:
            parts = key.split('.')
            current = self.default_config
            
            for part in parts:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return default
            
            return current
        
        return default
    
    def test_format_artwork_path_single(self):
        """测试格式化单页作品路径"""
        # 格式化路径
        path = self.path_formatter.format_artwork_path(
            self.test_artwork_metadata,
            is_multi_page=False,
            page_index=0,
            file_ext='jpg'
        )
        
        # 验证路径
        expected_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Images',
            'No_Series',
            '20230101_12345678_p0_测试作品.jpg'
        )
        
        self.assertEqual(path, expected_path)
    
    def test_format_artwork_path_multi(self):
        """测试格式化多页作品路径"""
        # 格式化路径
        path = self.path_formatter.format_artwork_path(
            self.test_manga_metadata,
            is_multi_page=True,
            page_index=1,
            file_ext='png'
        )
        
        # 验证路径
        expected_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Manga',
            'No_Series',
            '12345679_测试漫画',
            '20230102_12345679_p1_测试漫画.png'
        )
        
        self.assertEqual(path, expected_path)
    
    def test_format_novel_path(self):
        """测试格式化小说路径"""
        # 格式化路径
        path = self.path_formatter.format_novel_path(self.test_novel_metadata)
        
        # 验证路径
        expected_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Novels',
            'No_Series',
            '20230103_12345680_测试小说.txt'
        )
        
        self.assertEqual(path, expected_path)
    
    def test_format_metadata_path_single(self):
        """测试格式化单页作品元数据路径"""
        # 作品路径
        artwork_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Images',
            'No_Series',
            '20230101_12345678_p0_测试作品.jpg'
        )
        
        # 格式化元数据路径
        metadata_path = self.path_formatter.format_metadata_path(artwork_path, is_multi_page=False)
        
        # 验证路径
        expected_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Images',
            'No_Series',
            '20230101_12345678_p0_测试作品.txt'
        )
        
        self.assertEqual(metadata_path, expected_path)
    
    def test_format_metadata_path_multi(self):
        """测试格式化多页作品元数据路径"""
        # 作品路径
        artwork_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Manga',
            'No_Series',
            '12345679_测试漫画',
            '20230102_12345679_p1_测试漫画.png'
        )
        
        # 格式化元数据路径
        metadata_path = self.path_formatter.format_metadata_path(artwork_path, is_multi_page=True)
        
        # 验证路径
        expected_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Manga',
            'No_Series',
            '12345679_测试漫画',
            'metadata.txt'
        )
        
        self.assertEqual(metadata_path, expected_path)
    
    def test_series_path(self):
        """测试带系列的作品路径"""
        # 格式化路径
        path = self.path_formatter.format_artwork_path(
            self.test_series_metadata,
            is_multi_page=False,
            page_index=0,
            file_ext='jpg'
        )
        
        # 验证路径
        expected_path = os.path.join(
            'TestOutput',
            '87654321_测试用户',
            'Images',
            '测试系列',
            '20230104_12345681_p0_系列作品.jpg'
        )
        
        self.assertEqual(path, expected_path)
    
    def test_sanitize_filename(self):
        """测试清理文件名"""
        # 创建带有非法字符的元数据
        invalid_metadata = self.test_artwork_metadata.copy()
        invalid_metadata['title'] = 'test/file:with*illegal"chars?<>'
        
        # 格式化路径
        path = self.path_formatter.format_artwork_path(
            invalid_metadata,
            is_multi_page=False,
            page_index=0,
            file_ext='jpg'
        )
        
        # 验证路径中没有非法字符
        self.assertNotIn('/', path.split(os.sep)[-1])
        self.assertNotIn(':', path.split(os.sep)[-1])
        self.assertNotIn('*', path.split(os.sep)[-1])
        self.assertNotIn('"', path.split(os.sep)[-1])
        self.assertNotIn('?', path.split(os.sep)[-1])
        self.assertNotIn('<', path.split(os.sep)[-1])
        self.assertNotIn('>', path.split(os.sep)[-1])
    
    def test_format_date_custom(self):
        """测试自定义日期格式"""
        # 修改日期格式
        self.default_config['output.templates']['date_format'] = 'yyyy-mm-dd'
        
        # 格式化路径
        path = self.path_formatter.format_artwork_path(
            self.test_artwork_metadata,
            is_multi_page=False,
            page_index=0,
            file_ext='jpg'
        )
        
        # 验证路径
        self.assertIn('2023-01-01', path)
    
    def test_get_artwork_type(self):
        """测试获取作品类型"""
        # 测试插画类型
        self.assertEqual(
            self.path_formatter._get_artwork_type(self.test_artwork_metadata),
            'Images'
        )
        
        # 测试漫画类型
        self.assertEqual(
            self.path_formatter._get_artwork_type(self.test_manga_metadata),
            'Manga'
        )
        
        # 测试小说类型
        self.assertEqual(
            self.path_formatter._get_artwork_type(self.test_novel_metadata),
            'Novels'
        )
    
    def test_long_filename_truncation(self):
        """测试长文件名截断"""
        # 创建带超长标题的元数据
        long_title_metadata = self.test_artwork_metadata.copy()
        long_title_metadata['title'] = 'a' * 300
        
        # 格式化路径
        path = self.path_formatter.format_artwork_path(
            long_title_metadata,
            is_multi_page=False,
            page_index=0,
            file_ext='jpg'
        )
        
        # 验证文件名长度受限
        filename = os.path.basename(path)
        self.assertLessEqual(len(filename), 240 + 4)  # +4 for .jpg
    
    def test_custom_templates(self):
        """测试自定义模板"""
        # 修改模板
        self.default_config['output.templates']['main_dir'] = '{uid}/{type}'
        self.default_config['output.templates']['image_filename'] = '{pid}_{title}.{ext}'
        
        # 格式化路径
        path = self.path_formatter.format_artwork_path(
            self.test_artwork_metadata,
            is_multi_page=False,
            page_index=0,
            file_ext='jpg'
        )
        
        # 验证路径
        expected_path = os.path.join(
            'TestOutput',
            '87654321',
            'Images',
            '12345678_测试作品.jpg'
        )
        
        self.assertEqual(path, expected_path)


if __name__ == '__main__':
    unittest.main()
