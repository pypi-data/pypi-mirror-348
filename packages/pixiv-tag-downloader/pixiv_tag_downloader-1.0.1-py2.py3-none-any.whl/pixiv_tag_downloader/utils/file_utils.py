#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件处理工具，负责文件的创建、元数据写入等操作
"""

import os
import logging
from typing import Dict, Any, List, Optional

from ..i18n.translation import get_translation_manager


class FileUtils:
    """文件处理工具类"""
    
    def __init__(self):
        """初始化文件工具类"""
        self.logger = logging.getLogger(__name__)
        self.i18n = get_translation_manager()
    
    def write_metadata_file(self, path: str, metadata: Dict[str, Any], is_novel: bool = False) -> bool:
        """
        将元数据写入文件
        
        Args:
            path: 元数据文件路径
            metadata: 元数据字典
            is_novel: 是否为小说类型
            
        Returns:
            bool: 写入是否成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # 提取基本元数据
            title = metadata.get('title', 'Unknown Title')
            author_id = metadata.get('userId', 'Unknown')
            author_name = metadata.get('userName', 'Unknown')
            artwork_id = metadata.get('id', 'Unknown')
            create_date = metadata.get('createDate', '')
            upload_date = metadata.get('uploadDate', '')
            
            # 提取标签
            tags = []
            if 'tags' in metadata:
                if isinstance(metadata['tags'], dict) and 'tags' in metadata['tags']:
                    tags = [tag.get('tag', '') for tag in metadata['tags']['tags'] if tag.get('tag')]
                elif isinstance(metadata['tags'], list):
                    tags = [tag.get('tag', '') for tag in metadata['tags'] if tag.get('tag')]
            
            # 处理系列信息
            series_info = ''
            series = metadata.get('seriesNavData', {})
            if isinstance(series, list) and len(series) > 0:
                series_title = series[0].get('title', '')
                series_id = series[0].get('id', '')
                if series_title and series_id:
                    series_info = f"{series_title} / {series_id}"
            elif isinstance(series, dict) and series.get('title'):
                series_title = series.get('title', '')
                series_id = series.get('id', '')
                if series_title and series_id:
                    series_info = f"{series_title} / {series_id}"
            
            # 提取描述
            description = metadata.get('description', '')
            if isinstance(description, str):
                description = description.strip()
            
            # 组织写入内容
            content = []
            content.append(f"{self.i18n.get('metadata.title')}: {title}")
            content.append(f"{self.i18n.get('metadata.author_uid')}: {author_id}")
            content.append(f"{self.i18n.get('metadata.author_username')}: {author_name}")
            
            # 根据是小说还是作品使用不同的字段名
            pid_key = 'metadata.novel_pid' if is_novel else 'metadata.artwork_pid'
            content.append(f"{self.i18n.get(pid_key)}: {artwork_id}")
            
            # 添加上传日期
            if upload_date:
                content.append(f"{self.i18n.get('metadata.upload_date')}: {upload_date}")
            elif create_date:
                content.append(f"{self.i18n.get('metadata.create_date')}: {create_date}")
            
            # 添加标签
            content.append(f"{self.i18n.get('metadata.tags')}: {', '.join(tags)}")
            
            # 添加系列信息（如果有）
            if series_info:
                content.append(f"{self.i18n.get('metadata.series')}: {series_info}")
            
            # 添加描述（如果有）
            if description:
                content.append(f"{self.i18n.get('metadata.description')}:\n{description}")
            
            # 对于小说，添加正文
            if is_novel and 'content' in metadata:
                content.append("\n--- (分隔符) ---\n")
                content.append(f"{self.i18n.get('metadata.content')}:\n{metadata['content']}")
            
            # 写入文件
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
            
            self.logger.info(f"已成功写入元数据文件: {path}")
            return True
            
        except Exception as e:
            self.logger.error(f"写入元数据文件失败: {e}")
            return False
    
    def get_file_extension(self, url: str) -> str:
        """
        从URL中提取文件扩展名
        
        Args:
            url: 文件URL
            
        Returns:
            str: 文件扩展名（不含点号）
        """
        try:
            # 尝试从URL路径中提取扩展名
            extension = os.path.splitext(url.split('?')[0])[1]
            
            # 移除前导点号
            if extension.startswith('.'):
                extension = extension[1:]
            
            # 如果扩展名为空或过长，使用默认值
            if not extension or len(extension) > 5:
                return 'jpg'
            
            return extension.lower()
        except Exception:
            # 默认返回jpg
            return 'jpg'
    
    def ensure_directory_exists(self, path: str) -> bool:
        """
        确保目录存在，如果不存在则创建
        
        Args:
            path: 目录路径
            
        Returns:
            bool: 操作是否成功
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"创建目录失败: {e}")
            return False
    
    def is_file_exists(self, path: str) -> bool:
        """
        检查文件是否已存在
        
        Args:
            path: 文件路径
            
        Returns:
            bool: 文件是否存在
        """
        return os.path.isfile(path)


# 全局文件工具实例
_file_utils = None


def get_file_utils() -> FileUtils:
    """
    获取全局文件工具实例
    
    Returns:
        FileUtils: 文件工具实例
    """
    global _file_utils
    if (_file_utils is None):
        _file_utils = FileUtils()
    return _file_utils