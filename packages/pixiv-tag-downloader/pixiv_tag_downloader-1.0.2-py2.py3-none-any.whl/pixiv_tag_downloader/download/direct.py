#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
直接下载模块，负责通过HTTP直接下载文件
"""

import os
import time
import random
import logging
import requests
from tqdm import tqdm
from typing import Dict, Callable, Optional

from ..config.config_manager import get_config_manager


class DirectDownloader:
    """直接通过HTTP下载文件的类"""
    
    def __init__(self):
        """初始化直接下载器"""
        self.logger = logging.getLogger(__name__)
        self.config = get_config_manager()
        self.headers = self.config.get('http.headers', {})
        self.timeout = self.config.get('download.timeout', 30)
        self.retries = self.config.get('download.retries', 3)
        
        # 配置代理设置
        self.proxies = None
        if self.config.get('http.use_proxy', False):
            proxies = self.config.get('http.proxies', {})
            if proxies.get('http') or proxies.get('https'):
                self.proxies = proxies
                self.logger.info(f"已设置代理: {proxies}")
    
    def download_file(self, url: str, save_path: str, 
                    referer: str = "https://www.pixiv.net/", 
                    progress_callback: Optional[Callable] = None) -> bool:
        """
        下载文件到指定路径
        
        Args:
            url: 文件URL
            save_path: 保存路径
            referer: Referer头，默认为Pixiv主页
            progress_callback: 进度回调函数，接收参数(current, total)
            
        Returns:
            bool: 下载是否成功
        """
        # 添加随机延迟
        self._random_sleep()
        
        # 准备请求头
        headers = self.headers.copy()
        headers.update({'Referer': referer})
        
        # 创建保存目录
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 检查文件是否已存在
        if os.path.exists(save_path) and not self.config.get('output.overwrite', False):
            self.logger.info(f"文件已存在，跳过下载: {save_path}")
            return True
            
        # 下载文件
        for attempt in range(self.retries + 1):
            try:
                response = requests.get(
                    url, 
                    headers=headers, 
                    stream=True,
                    timeout=self.timeout,
                    proxies=self.proxies
                )
                response.raise_for_status()
                
                # 获取文件总大小
                file_size = int(response.headers.get('content-length', 0))
                
                # 设置进度条
                show_progress = self.config.get('logging.verbose_progress', True)
                progress_bar = None
                
                if show_progress:
                    progress_bar = tqdm(
                        total=file_size,
                        unit='B',
                        unit_scale=True,
                        desc=os.path.basename(save_path),
                        leave=False
                    )
                
                # 写入文件
                with open(save_path, 'wb') as f:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 更新进度
                            if progress_bar:
                                progress_bar.update(len(chunk))
                            
                            # 调用进度回调
                            if progress_callback and file_size > 0:
                                progress_callback(downloaded, file_size)
                
                if progress_bar:
                    progress_bar.close()
                
                self.logger.info(f"文件下载成功: {save_path}")
                return True
                
            except requests.RequestException as e:
                self.logger.warning(f"下载失败 (尝试 {attempt+1}/{self.retries+1}): {e}")
                if attempt < self.retries:
                    # 递增延迟重试
                    time.sleep(2 ** attempt)
            except Exception as e:
                self.logger.error(f"下载时发生错误: {e}")
                break
        
        self.logger.error(f"下载失败，已达最大重试次数: {url}")
        return False
    
    def _random_sleep(self) -> None:
        """添加随机延迟，模拟人类行为"""
        min_delay = self.config.get('download.delay.min', 1)
        max_delay = self.config.get('download.delay.max', 3)
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)


# 全局下载器实例
_direct_downloader = None


def get_direct_downloader() -> DirectDownloader:
    """
    获取全局直接下载器实例
    
    Returns:
        DirectDownloader: 下载器实例
    """
    global _direct_downloader
    if _direct_downloader is None:
        _direct_downloader = DirectDownloader()
    return _direct_downloader