#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pixiv API模块单元测试
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pixiv_tag_downloader.api.pixiv import PixivAPI


class TestPixivAPI(unittest.TestCase):
    """Pixiv API测试类"""
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 模拟配置和会话
        self.mock_session_patcher = patch('pixiv_tag_downloader.api.pixiv.get_cookie_manager')
        self.mock_config_patcher = patch('pixiv_tag_downloader.api.pixiv.get_config_manager')
        
        self.mock_cookie_manager = self.mock_session_patcher.start()
        self.mock_config_manager = self.mock_config_patcher.start()
        
        # 配置模拟对象
        self.mock_session = MagicMock()
        self.mock_config = MagicMock()
        
        self.mock_cookie_manager().get_session.return_value = self.mock_session
        self.mock_config_manager.return_value = self.mock_config
        
        # 设置默认配置
        self.mock_config.get.side_effect = lambda key, default=None: {
            'http.headers': {'User-Agent': 'Test Agent'},
            'http.use_proxy': False,
            'download.timeout': 30,
            'download.delay.min': 0,
            'download.delay.max': 0,
        }.get(key, default)
        
        # 创建API实例
        self.pixiv_api = PixivAPI()
    
    def tearDown(self):
        """每个测试方法结束后执行"""
        self.mock_session_patcher.stop()
        self.mock_config_patcher.stop()
    
    def test_get_user_info_success(self):
        """测试成功获取用户信息"""
        # 准备模拟的响应数据
        mock_user_data = {
            'error': False,
            'message': '',
            'body': {
                'userId': '12345',
                'name': 'Test User',
                'profileImageUrl': 'https://example.com/avatar.jpg',
                'imageBig': 'https://example.com/avatar_big.jpg',
                'premium': True,
                'isFollowed': False,
                'isMypixiv': False,
            }
        }
        
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = mock_user_data
        mock_response.raise_for_status = MagicMock()
        self.mock_session.request.return_value = mock_response
        
        # 调用要测试的方法
        result = self.pixiv_api.get_user_info('12345')
        
        # 验证结果
        self.assertEqual(result, mock_user_data)
        self.mock_session.request.assert_called_once()
        args, kwargs = self.mock_session.request.call_args
        self.assertEqual(args[0], 'GET')
        self.assertTrue(args[1].startswith('https://www.pixiv.net/ajax/user/'))
    
    def test_get_user_info_error(self):
        """测试获取用户信息时出错"""
        # 准备模拟的错误响应数据
        mock_error_data = {
            'error': True,
            'message': 'User not found',
            'body': {}
        }
        
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = mock_error_data
        mock_response.raise_for_status = MagicMock()
        self.mock_session.request.return_value = mock_response
        
        # 调用要测试的方法并验证是否抛出异常
        with self.assertRaises(Exception) as context:
            self.pixiv_api.get_user_info('invalid_id')
        
        # 验证异常信息
        self.assertTrue('Pixiv API错误' in str(context.exception))
    
    def test_get_user_artworks_success(self):
        """测试成功获取用户作品列表"""
        # 准备模拟的响应数据
        mock_artworks_data = {
            'error': False,
            'message': '',
            'body': {
                'illusts': {
                    '123': {
                        'id': '123',
                        'title': 'Test Artwork',
                        'illustType': 0,
                        'url': 'https://example.com/123.jpg',
                        'tags': ['test', 'example']
                    },
                    '456': {
                        'id': '456',
                        'title': 'Another Artwork',
                        'illustType': 0,
                        'url': 'https://example.com/456.jpg',
                        'tags': ['example']
                    }
                }
            }
        }
        
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = mock_artworks_data
        mock_response.raise_for_status = MagicMock()
        self.mock_session.request.return_value = mock_response
        
        # 调用要测试的方法
        result = self.pixiv_api.get_user_artworks('12345')
        
        # 验证结果
        self.assertEqual(result, mock_artworks_data)
        self.mock_session.request.assert_called_once()
        args, kwargs = self.mock_session.request.call_args
        self.assertEqual(args[0], 'GET')
        self.assertTrue(args[1].startswith('https://www.pixiv.net/ajax/user/'))
    
    def test_get_artwork_detail_success(self):
        """测试成功获取作品详情"""
        # 准备模拟的响应数据
        mock_detail_data = {
            'error': False,
            'message': '',
            'body': {
                'illustId': '123',
                'illustTitle': 'Test Artwork',
                'userId': '12345',
                'userName': 'Test User',
                'createDate': '2023-01-01T00:00:00+00:00',
                'tags': {
                    'tags': [
                        {'tag': 'test'},
                        {'tag': 'example'}
                    ]
                },
                'urls': {
                    'original': 'https://example.com/123.jpg'
                }
            }
        }
        
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = mock_detail_data
        mock_response.raise_for_status = MagicMock()
        self.mock_session.request.return_value = mock_response
        
        # 调用要测试的方法
        result = self.pixiv_api.get_artwork_detail('123')
        
        # 验证结果
        self.assertEqual(result, mock_detail_data['body'])
        self.mock_session.request.assert_called_once()
        args, kwargs = self.mock_session.request.call_args
        self.assertEqual(args[0], 'GET')
        self.assertTrue(args[1].startswith('https://www.pixiv.net/ajax/illust/'))
    
    def test_get_download_url_success(self):
        """测试成功获取下载URL"""
        # 模拟作品详情数据
        artwork_detail = {
            'urls': {
                'original': 'https://i.pximg.net/img-original/img/2023/01/01/12345_p0.jpg'
            }
        }
        
        # 调用要测试的方法
        result = self.pixiv_api._get_download_url(artwork_detail, 0)
        
        # 验证结果
        self.assertEqual(result, 'https://i.pximg.net/img-original/img/2023/01/01/12345_p0.jpg')

if __name__ == '__main__':
    unittest.main()
