#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aria2下载模块，负责通过Aria2下载文件
支持直接命令行调用和RPC调用两种方式
"""

import os
import time
import random
import logging
import subprocess
import xmlrpc.client
from urllib.parse import urlparse
from typing import Dict, Optional, Callable, List, Union, Any

from ..config.config_manager import get_config_manager


class Aria2Base:
    """Aria2下载基类，提供通用功能"""
    
    def __init__(self):
        """初始化Aria2基类"""
        self.logger = logging.getLogger(__name__)
        self.config = get_config_manager()
        self.headers = self.config.get('http.headers', {})
        self.retries = self.config.get('download.retries', 3)
    
    def _random_sleep(self) -> None:
        """添加随机延迟，模拟人类行为"""
        min_delay = self.config.get('download.delay.min', 1)
        max_delay = self.config.get('download.delay.max', 3)
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def _prepare_headers(self, referer: str = "https://www.pixiv.net/") -> Dict[str, str]:
        """
        准备请求头
        
        Args:
            referer: Referer头，默认为Pixiv主页
            
        Returns:
            Dict[str, str]: 请求头字典
        """
        headers = self.headers.copy()
        headers.update({'Referer': referer})
        return headers


class Aria2CLI(Aria2Base):
    """通过命令行调用Aria2下载文件"""
    
    def __init__(self):
        """初始化Aria2 CLI下载器"""
        super().__init__()
    
    def download_file(self, url: str, save_path: str, 
                     referer: str = "https://www.pixiv.net/", 
                     progress_callback: Optional[Callable] = None) -> bool:
        """
        使用aria2c命令行工具下载文件
        
        Args:
            url: 文件URL
            save_path: 保存路径
            referer: Referer头，默认为Pixiv主页
            progress_callback: 进度回调函数，在此方法中不使用
            
        Returns:
            bool: 下载是否成功
        """
        # 添加随机延迟
        self._random_sleep()
        
        # 准备请求头
        headers = self._prepare_headers(referer)
        header_args = []
        for key, value in headers.items():
            header_args.extend(['--header', f'{key}: {value}'])
        
        # 创建保存目录
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 检查文件是否已存在
        if os.path.exists(save_path) and not self.config.get('output.overwrite', False):
            self.logger.info(f"文件已存在，跳过下载: {save_path}")
            return True
        
        # 准备aria2c参数
        aria2_params = self.config.get('download.aria2.params', {})
        max_connections = aria2_params.get('max_connection_per_server', 5)
        min_split_size = aria2_params.get('min_split_size', '1M')
        split = aria2_params.get('split', 5)
        
        command = [
            'aria2c',
            '--max-connection-per-server', str(max_connections),
            '--min-split-size', str(min_split_size),
            '--split', str(split),
            '--max-tries', str(self.retries),
            '--dir', os.path.dirname(save_path),
            '--out', os.path.basename(save_path),
            *header_args,
            url
        ]
        
        # 配置代理
        if self.config.get('http.use_proxy', False):
            proxies = self.config.get('http.proxies', {})
            if proxies.get('http'):
                command.extend(['--http-proxy', proxies['http']])
            if proxies.get('https'):
                command.extend(['--https-proxy', proxies['https']])
        
        try:
            self.logger.info(f"开始aria2c下载: {url} -> {save_path}")
            
            # 执行下载命令
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                self.logger.error(f"aria2c下载失败: {result.stderr}")
                return False
            
            self.logger.info(f"aria2c下载成功: {save_path}")
            return True
        except Exception as e:
            self.logger.error(f"aria2c下载出错: {e}")
            return False


class Aria2RPC(Aria2Base):
    """通过RPC调用Aria2下载文件"""
    
    def __init__(self):
        """初始化Aria2 RPC下载器"""
        super().__init__()
        self.rpc_url = self.config.get('download.aria2.rpc_url', 'http://localhost:6800/jsonrpc')
        self.token = self.config.get('download.aria2.token', '')
        self.use_wss = self.config.get('download.aria2.use_wss', False)
        self.verify_cert = self.config.get('download.aria2.verify_cert', True)
        self.cert_path = self.config.get('download.aria2.cert_path', '')
        
        # 准备RPC服务器
        self._prepare_rpc_server()
    
    def _prepare_rpc_server(self) -> None:
        """准备RPC服务器连接"""
        try:
            # 处理不同协议
            parsed_url = urlparse(self.rpc_url)
            protocol = parsed_url.scheme.lower()
            
            if protocol == 'ws' or protocol == 'wss':
                try:
                    from xmlrpc_aria2 import aria2
                    
                    # 配置WSS证书验证
                    kwargs = {}
                    if protocol == 'wss':
                        if not self.verify_cert:
                            kwargs['verify_cert'] = False
                        if self.cert_path:
                            kwargs['cert_path'] = self.cert_path
                    
                    # 创建WebSocket连接
                    self.server = aria2.Client(
                        self.rpc_url,
                        token=self.token or None,
                        **kwargs
                    )
                    self.logger.info(f"已连接到Aria2 WebSocket RPC服务器: {self.rpc_url}")
                    
                except ImportError:
                    self.logger.error("无法导入xmlrpc_aria2模块，请确保已安装依赖：pip install xmlrpc-aria2")
                    raise
            else:
                # 创建XML-RPC连接
                server_url = self.rpc_url
                if self.token:
                    server_url = server_url.replace('://', f'://token:{self.token}@')
                
                self.server = xmlrpc.client.ServerProxy(server_url)
                self.logger.info(f"已连接到Aria2 XML-RPC服务器: {self.rpc_url}")
            
        except Exception as e:
            self.logger.error(f"连接到Aria2 RPC服务器失败: {e}")
            raise
    
    def download_file(self, url: str, save_path: str, 
                     referer: str = "https://www.pixiv.net/", 
                     progress_callback: Optional[Callable] = None) -> bool:
        """
        使用Aria2 RPC下载文件
        
        Args:
            url: 文件URL
            save_path: 保存路径
            referer: Referer头，默认为Pixiv主页
            progress_callback: 进度回调函数，可选
            
        Returns:
            bool: 下载是否成功
        """
        # 添加随机延迟
        self._random_sleep()
        
        # 准备请求头
        headers = self._prepare_headers(referer)
        header_list = [f"{k}: {v}" for k, v in headers.items()]
        
        # 创建保存目录
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 检查文件是否已存在
        if os.path.exists(save_path) and not self.config.get('output.overwrite', False):
            self.logger.info(f"文件已存在，跳过下载: {save_path}")
            return True
        
        # 准备aria2参数
        aria2_params = self.config.get('download.aria2.params', {})
        options = {
            'dir': os.path.dirname(save_path),
            'out': os.path.basename(save_path),
            'max-connection-per-server': str(aria2_params.get('max_connection_per_server', 5)),
            'min-split-size': str(aria2_params.get('min_split_size', '1M')),
            'split': str(aria2_params.get('split', 5)),
            'max-tries': str(self.retries),
            'header': header_list
        }
        
        # 配置代理
        if self.config.get('http.use_proxy', False):
            proxies = self.config.get('http.proxies', {})
            if proxies.get('http'):
                options['http-proxy'] = proxies['http']
            if proxies.get('https'):
                options['https-proxy'] = proxies['https']
        
        try:
            self.logger.info(f"开始Aria2 RPC下载: {url} -> {save_path}")
            
            # 提交下载任务
            if hasattr(self.server, 'aria2'):
                # xmlrpc_aria2库
                gid = self.server.addUri([url], options)
            else:
                # 标准xmlrpc
                gid = self.server.aria2.addUri([url], options)
            
            self.logger.info(f"Aria2任务已创建，GID: {gid}")
            
            # 等待下载完成
            return self._wait_for_download(gid, progress_callback)
            
        except Exception as e:
            self.logger.error(f"Aria2 RPC下载出错: {e}")
            return False
    
    def _wait_for_download(self, gid: str, progress_callback: Optional[Callable]) -> bool:
        """
        等待下载任务完成
        
        Args:
            gid: 下载任务ID
            progress_callback: 进度回调函数
            
        Returns:
            bool: 下载是否成功
        """
        try:
            while True:
                # 获取任务状态
                status = self._get_download_status(gid)
                
                if status['status'] == 'complete':
                    self.logger.info(f"下载成功完成: {status['files'][0]['path']}")
                    return True
                
                elif status['status'] == 'error':
                    error_code = status.get('errorCode', 'unknown')
                    self.logger.error(f"下载失败，错误代码: {error_code}")
                    return False
                
                elif status['status'] == 'active':
                    # 更新进度
                    if progress_callback:
                        total_length = int(status.get('totalLength', '0'))
                        completed_length = int(status.get('completedLength', '0'))
                        if total_length > 0:
                            progress_callback(completed_length, total_length)
                
                # 等待一段时间后再次检查
                time.sleep(0.5)
                
        except Exception as e:
            self.logger.error(f"等待下载任务时出错: {e}")
            return False
    
    def _get_download_status(self, gid: str) -> Dict:
        """
        获取下载任务状态
        
        Args:
            gid: 下载任务ID
            
        Returns:
            Dict: 下载任务状态信息
        """
        try:
            if hasattr(self.server, 'aria2'):
                # xmlrpc_aria2库
                return self.server.tellStatus(gid)
            else:
                # 标准xmlrpc
                return self.server.aria2.tellStatus(gid)
        except Exception as e:
            self.logger.error(f"获取下载状态时出错: {e}")
            return {'status': 'error', 'errorCode': str(e)}


# 工厂函数
def create_downloader(method: str = 'direct'):
    """
    根据指定的方法创建下载器实例
    
    Args:
        method: 下载方法，支持'direct', 'aria2c', 'aria2-rpc'
        
    Returns:
        下载器实例
    
    Raises:
        ValueError: 如果指定了不支持的下载方法
    """
    if method == 'direct':
        from .direct import get_direct_downloader
        return get_direct_downloader()
    elif method == 'aria2c':
        return Aria2CLI()
    elif method == 'aria2-rpc':
        return Aria2RPC()
    else:
        raise ValueError(f"不支持的下载方法: {method}")


# 全局Aria2下载器实例
_aria2_cli = None
_aria2_rpc = None


def get_aria2_cli() -> Aria2CLI:
    """
    获取全局Aria2 CLI下载器实例
    
    Returns:
        Aria2CLI: 下载器实例
    """
    global _aria2_cli
    if _aria2_cli is None:
        _aria2_cli = Aria2CLI()
    return _aria2_cli


def get_aria2_rpc() -> Aria2RPC:
    """
    获取全局Aria2 RPC下载器实例
    
    Returns:
        Aria2RPC: 下载器实例
    """
    global _aria2_rpc
    if _aria2_rpc is None:
        _aria2_rpc = Aria2RPC()
    return _aria2_rpc