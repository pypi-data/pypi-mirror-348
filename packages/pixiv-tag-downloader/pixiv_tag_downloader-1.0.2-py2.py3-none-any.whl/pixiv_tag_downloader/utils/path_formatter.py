#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
路径格式化工具，负责处理文件路径和名称的格式化
"""

import os
import re
import string
from datetime import datetime
from typing import Dict, Any, Optional, List

from ..config.config_manager import get_config_manager


class PathFormatter:
    """路径格式化类，用于根据模板格式化文件路径和名称"""
    
    def __init__(self):
        """初始化路径格式化器"""
        self.config = get_config_manager()
        
        # 获取主要配置
        self.root_dir = self.config.get('output.root_dir', 'Output')
        self.templates = self.config.get('output.templates', {})
        self.main_dir_template = self.templates.get('main_dir', '{uid}_{username}/{type}/{series}')
        self.image_filename_template = self.templates.get('image_filename', '{date}_{pid}_p{index}_{title}.{ext}')
        self.novel_filename_template = self.templates.get('novel_filename', '{date}_{pid}_{title}.txt')
        self.date_format = self.templates.get('date_format', 'yyyymmdd')
        self.tag_separator = self.templates.get('tag_separator', '_')
        self.pid_dir_with_title = self.config.get('output.pid_dir_with_title', True)
        
        # 文件名非法字符
        self.illegal_filename_chars = r'[<>:"/\\|?*\x00-\x1f]'
        self.max_filename_length = 240  # 留出一些空间给路径
    
    def format_artwork_path(self, metadata: Dict[str, Any], is_multi_page: bool = False, 
                         page_index: int = 0, file_ext: str = 'jpg') -> str:
        """
        格式化图片/插画/漫画类作品的保存路径
        
        Args:
            metadata: 作品元数据
            is_multi_page: 是否为多页作品
            page_index: 页码索引（从0开始）
            file_ext: 文件扩展名
            
        Returns:
            str: 格式化后的完整路径
        """
        # 提取基本信息
        artwork_type = self._get_artwork_type(metadata)
        series_title = self._get_series_title(metadata)
        path_data = self._prepare_path_data(metadata, artwork_type, series_title, page_index, file_ext)
        
        # 格式化主目录结构
        main_dir = self._format_template(self.main_dir_template, path_data)
        
        # 处理多页作品的路径
        if is_multi_page:
            if self.pid_dir_with_title:
                pid_dir = f"{path_data['pid']}_{path_data['title']}"
            else:
                pid_dir = f"{path_data['pid']}"
            
            pid_dir = self._sanitize_filename(pid_dir)
            main_dir = os.path.join(main_dir, pid_dir)
        
        # 格式化文件名
        filename = self._format_template(self.image_filename_template, path_data)
        filename = self._sanitize_filename(filename)
        
        # 组合完整路径
        return os.path.join(self.root_dir, main_dir, filename)
    
    def format_novel_path(self, metadata: Dict[str, Any]) -> str:
        """
        格式化小说类作品的保存路径
        
        Args:
            metadata: 作品元数据
            
        Returns:
            str: 格式化后的完整路径
        """
        # 提取基本信息
        artwork_type = "Novels"
        series_title = self._get_series_title(metadata)
        path_data = self._prepare_path_data(metadata, artwork_type, series_title)
        
        # 格式化主目录结构
        main_dir = self._format_template(self.main_dir_template, path_data)
        
        # 格式化文件名
        filename = self._format_template(self.novel_filename_template, path_data)
        filename = self._sanitize_filename(filename)
        
        # 组合完整路径
        return os.path.join(self.root_dir, main_dir, filename)
    
    def format_metadata_path(self, artwork_path: str, is_multi_page: bool = False) -> str:
        """
        格式化元数据文件的保存路径
        
        Args:
            artwork_path: 作品文件路径
            is_multi_page: 是否为多页作品
            
        Returns:
            str: 元数据文件路径
        """
        if is_multi_page:
            # 多页作品的元数据文件保存在PID目录下
            artwork_dir = os.path.dirname(artwork_path)
            return os.path.join(artwork_dir, 'metadata.txt')
        else:
            # 单页作品的元数据文件与作品文件同名，但扩展名为.txt
            base_path = os.path.splitext(artwork_path)[0]
            return f"{base_path}.txt"
    
    def _get_artwork_type(self, metadata: Dict[str, Any]) -> str:
        """
        根据元数据确定作品类型
        
        Args:
            metadata: 作品元数据
            
        Returns:
            str: 作品类型 (Images, Manga, Novels)
        """
        work_type = metadata.get('type', '').lower()
        
        if 'novel' in work_type:
            return 'Novels'
        elif 'manga' in work_type:
            return 'Manga'
        else:
            return 'Images'
    
    def _get_series_title(self, metadata: Dict[str, Any]) -> str:
        """
        获取作品的系列标题
        
        Args:
            metadata: 作品元数据
            
        Returns:
            str: 系列标题，如果不属于任何系列则返回"无系列"
        """
        series = metadata.get('seriesNavData', {})
        if isinstance(series, list) and len(series) > 0:
            return series[0].get('title', 'No_Series')
        elif isinstance(series, dict) and series.get('title'):
            return series.get('title', 'No_Series')
        
        # 尝试其他可能的系列字段
        for field in ['seriesTitle', 'series', 'seriesId']:
            if metadata.get(field):
                return metadata.get(field)
        
        return 'No_Series'
    
    def _prepare_path_data(self, metadata: Dict[str, Any], artwork_type: str, 
                          series_title: str, page_index: int = 0, 
                          file_ext: str = 'jpg') -> Dict[str, str]:
        """
        准备路径格式化所需的数据
        
        Args:
            metadata: 作品元数据
            artwork_type: 作品类型
            series_title: 系列标题
            page_index: 页码索引
            file_ext: 文件扩展名
            
        Returns:
            Dict[str, str]: 路径数据字典
        """
        # 提取基本信息
        uid = metadata.get('userId', '')
        username = metadata.get('userName', '')
        pid = metadata.get('id', '')
        title = metadata.get('title', '')
        upload_date = metadata.get('uploadDate', '')
        create_date = metadata.get('createDate', '')
        
        # 转换日期格式
        date_str = self._format_date(upload_date or create_date)
        
        # 提取标签
        tags = []
        if metadata.get('tags'):
            if isinstance(metadata['tags'], dict) and metadata['tags'].get('tags'):
                tags = [tag.get('tag', '') for tag in metadata['tags']['tags'] if tag.get('tag')]
            elif isinstance(metadata['tags'], list):
                tags = [tag.get('tag', '') for tag in metadata['tags'] if tag.get('tag')]
        
        tags_str = self.tag_separator.join(tags)
        
        # 返回数据字典
        return {
            'uid': uid,
            'username': username,
            'pid': pid,
            'title': title,
            'type': artwork_type,
            'series': series_title,
            'index': page_index,
            'date': date_str,
            'tags': tags_str,
            'ext': file_ext
        }
    
    def _format_date(self, date_str: str) -> str:
        """
        根据配置的日期格式格式化日期字符串
        
        Args:
            date_str: ISO格式的日期字符串
            
        Returns:
            str: 格式化后的日期字符串
        """
        try:
            if not date_str:
                # 如果没有日期信息，使用当前日期
                dt = datetime.now()
            else:
                # 尝试解析ISO格式日期
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            
            # 根据配置的模板格式化
            format_str = self.date_format
            format_str = format_str.replace('yyyy', '%Y')
            format_str = format_str.replace('yy', '%y')
            format_str = format_str.replace('mm', '%m')
            format_str = format_str.replace('dd', '%d')
            
            return dt.strftime(format_str)
        except Exception:
            # 返回当前日期作为后备
            return datetime.now().strftime('%Y%m%d')
    
    def _format_template(self, template: str, data: Dict[str, str]) -> str:
        """
        使用提供的数据填充模板字符串中的占位符
        
        Args:
            template: 包含占位符的模板字符串
            data: 用于填充模板的数据
            
        Returns:
            str: 填充后的字符串
        """
        try:
            # 处理日期和标签的特殊格式
            result = template
            
            # 处理 {date:format} 格式
            date_matches = re.findall(r'{date:([^}]+)}', template)
            if date_matches and 'date' in data:
                for date_format in date_matches:
                    try:
                        dt = datetime.strptime(data['date'], self.date_format.replace('yyyy', '%Y').replace('mm', '%m').replace('dd', '%d'))
                        format_str = date_format.replace('yyyy', '%Y').replace('yy', '%y').replace('mm', '%m').replace('dd', '%d')
                        formatted_date = dt.strftime(format_str)
                        result = result.replace(f"{{date:{date_format}}}", formatted_date)
                    except Exception:
                        result = result.replace(f"{{date:{date_format}}}", data['date'])
            
            # 处理 {tags:separator} 格式
            tags_matches = re.findall(r'{tags:([^}]+)}', template)
            if tags_matches and 'tags' in data:
                tags_list = data['tags'].split(self.tag_separator)
                for separator in tags_matches:
                    formatted_tags = separator.join(tags_list)
                    result = result.replace(f"{{tags:{separator}}}", formatted_tags)
            
            # 处理常规占位符
            result = string.Formatter().vformat(result, [], data)
            
            return result
        except KeyError as e:
            # 如果模板中包含数据中没有的占位符，使用空字符串替换
            return re.sub(r'{[^}]+}', '', template)
        except Exception as e:
            # 出现其他错误时返回原始模板
            return template
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除非法字符并确保不超过最大长度
        
        Args:
            filename: 原始文件名
            
        Returns:
            str: 清理后的文件名
        """
        # 替换非法字符
        sanitized = re.sub(self.illegal_filename_chars, '_', filename)
        
        # 处理文件名过长问题
        if len(sanitized) > self.max_filename_length:
            name, ext = os.path.splitext(sanitized)
            name = name[:self.max_filename_length - len(ext)]
            sanitized = name + ext
        
        return sanitized


# 全局路径格式化器实例
_path_formatter = None


def get_path_formatter() -> PathFormatter:
    """
    获取全局路径格式化器实例
    
    Returns:
        PathFormatter: 路径格式化器实例
    """
    global _path_formatter
    if _path_formatter is None:
        _path_formatter = PathFormatter()
    return _path_formatter