#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主程序入口模块
"""

import os
import sys
import time
import logging
import threading
import concurrent.futures
from typing import Dict, List, Tuple, Any, Optional, Union

from .config.config_manager import get_config_manager
from .auth.cookie import get_cookie_manager
from .api.pixiv import get_pixiv_api
from .download import aria2
from .download.direct import get_direct_downloader
from .utils.path_formatter import get_path_formatter
from .utils.file_utils import get_file_utils
from .ui.cli import get_cli


class PixivTagDownloader:
    """Pixiv标签下载器主类"""
    
    def __init__(self):
        """初始化下载器"""
        # 设置日志
        self._setup_logging()
        
        # 获取组件实例
        self.logger = logging.getLogger(__name__)
        self.config = get_config_manager()
        self.cli = get_cli()
        self.pixiv_api = get_pixiv_api()
        self.path_formatter = get_path_formatter()
        self.file_utils = get_file_utils()
        
        # 下载设置
        self.download_method = self.config.get('download.method', 'direct')
        self.threads = self.config.get('download.threads', 4)
    
    def _setup_logging(self) -> None:
        """设置日志系统"""
        config = get_config_manager()
        log_level_str = config.get('logging.level', 'INFO')
        log_file = config.get('logging.file', '')
        log_to_console = config.get('logging.console', True)
        
        # 将字符串日志级别转换为数值
        log_level = getattr(logging, log_level_str.upper(), logging.INFO)
        
        # 创建根日志记录器
        logger = logging.getLogger()
        logger.setLevel(log_level)
        
        # 清除现有处理器
        logger.handlers = []
        
        # 设置格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 添加控制台处理器
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # 添加文件处理器
        if log_file:
            try:
                # 确保日志目录存在
                log_dir = os.path.dirname(log_file)
                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)
                    
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"Warning: Could not set up log file: {e}")
    
    def run(self) -> None:
        """运行下载器"""
        try:
            # 解析命令行参数
            args = self.cli.parse_arguments()
            
            # 如果指定了配置文件，重新加载配置
            if args.config:
                self.config.load_config(args.config)
            
            # 应用命令行参数覆盖配置
            self._apply_command_line_overrides(args)
            
            # 初始化和验证Cookie
            self.cli.init_and_validate_cookie()
            
            # 确定运行模式和获取必要参数
            if args.uid:
                # 命令行模式
                uid = args.uid
                selected_tags = args.tags.split(',') if args.tags else []
                logic = args.logic.lower()
            else:
                # 交互式模式
                uid, selected_tags, logic = self.cli.interactive_mode()
            
            # 获取用户信息
            user_info = self.pixiv_api.get_user_info(uid)
            username = user_info.get('name', 'Unknown')
            
            # 获取所有作品
            artworks = self.pixiv_api.get_user_artworks_ids(uid)
            
            # 如果有选定的标签，进行过滤
            if selected_tags:
                self.cli.print_colored("根据标签过滤作品...", "cyan")
                filtered_artworks = self.pixiv_api.filter_artworks_by_tags(artworks, selected_tags, logic)
            else:
                filtered_artworks = artworks
            
            # 显示下载摘要
            artworks_count = {
                'illustrations': len(filtered_artworks.get('illustrations', [])),
                'novels': len(filtered_artworks.get('novels', []))
            }
            
            self.cli.display_summary(uid, username, selected_tags, logic, artworks_count)
            
            # 开始下载
            self._download_works(filtered_artworks, uid, username)
            
            self.cli.print_colored("所有下载任务已完成！", "green", "bright")
            
        except KeyboardInterrupt:
            self.cli.print_colored("\n下载已被用户中断", "yellow")
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"执行过程中发生错误: {e}", exc_info=True)
            self.cli.print_colored(f"错误: {e}", "red")
            sys.exit(1)
    
    def _apply_command_line_overrides(self, args) -> None:
        """应用命令行参数覆盖配置"""
        if args.output_dir:
            self.config.set('output.root_dir', args.output_dir)
        
        if args.threads:
            self.config.set('download.threads', args.threads)
            self.threads = args.threads
        
        if args.download_method:
            self.config.set('download.method', args.download_method)
            self.download_method = args.download_method
        
        if args.aria2_rpc_url:
            self.config.set('download.aria2.rpc_url', args.aria2_rpc_url)
    
    def _download_works(self, artworks: Dict[str, List[str]], uid: str, username: str) -> None:
        """
        下载作品
        
        Args:
            artworks: 作品ID字典
            uid: 用户ID
            username: 用户名
        """
        total_works = len(artworks.get('illustrations', [])) + len(artworks.get('novels', []))
        if total_works == 0:
            self.cli.print_colored("没有找到符合条件的作品", "yellow")
            return
        
        self.cli.print_colored(f"开始下载 {total_works} 个作品，使用 {self.download_method} 方式，{self.threads} 线程", "cyan")
        
        # 创建下载器
        downloader = aria2.create_downloader(self.download_method)
        
        # 使用线程池进行并发下载
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            # 提交插画/漫画下载任务
            illustration_futures = [
                executor.submit(self._download_illustration, pid, downloader)
                for pid in artworks.get('illustrations', [])
            ]
            
            # 提交小说下载任务
            novel_futures = [
                executor.submit(self._download_novel, pid, downloader)
                for pid in artworks.get('novels', [])
            ]
            
            # 等待所有任务完成
            total_futures = illustration_futures + novel_futures
            completed = 0
            
            for future in concurrent.futures.as_completed(total_futures):
                completed += 1
                try:
                    success, work_type, pid = future.result()
                    status = "成功" if success else "失败"
                    self.cli.print_colored(
                        f"[{completed}/{total_works}] {work_type} (PID: {pid}) 下载{status}",
                        "green" if success else "red"
                    )
                except Exception as e:
                    self.logger.error(f"下载任务出错: {e}")
                    self.cli.print_colored(f"[{completed}/{total_works}] 下载出错: {e}", "red")
    
    def _download_illustration(self, pid: str, downloader) -> Tuple[bool, str, str]:
        """
        下载插画/漫画
        
        Args:
            pid: 作品ID
            downloader: 下载器实例
            
        Returns:
            Tuple[bool, str, str]: (是否成功, 作品类型, 作品ID)
        """
        try:
            # 获取作品详情
            artwork = self.pixiv_api.get_artwork_details(pid)
            
            # 判断是单页还是多页
            page_count = int(artwork.get('pageCount', 1))
            is_multi_page = page_count > 1
            
            # 如果是多页且没有pages字段，需要获取所有页面
            if is_multi_page and 'pages' not in artwork:
                pages = self.pixiv_api.get_artwork_pages(pid)
                artwork['pages'] = pages
            
            success = True
            
            if is_multi_page:
                # 处理多页作品
                pages = artwork.get('pages', [])
                for i, page in enumerate(pages):
                    # 获取图片URL
                    img_url = page.get('urls', {}).get('original')
                    if not img_url:
                        self.logger.warning(f"无法获取作品PID={pid}第{i+1}页的URL")
                        continue
                    
                    # 获取文件扩展名
                    file_ext = self.file_utils.get_file_extension(img_url)
                    
                    # 格式化保存路径
                    save_path = self.path_formatter.format_artwork_path(
                        artwork, is_multi_page=True, page_index=i, file_ext=file_ext
                    )
                    
                    # 下载图片
                    page_success = downloader.download_file(img_url, save_path, referer=f'https://www.pixiv.net/artworks/{pid}')
                    success = success and page_success
                    
                    # 只需要为第一页创建元数据文件
                    if i == 0:
                        metadata_path = self.path_formatter.format_metadata_path(save_path, is_multi_page=True)
                        self.file_utils.write_metadata_file(metadata_path, artwork)
            else:
                # 处理单页作品
                img_url = artwork.get('urls', {}).get('original')
                if not img_url:
                    self.logger.warning(f"无法获取作品PID={pid}的URL")
                    return False, "插画/漫画", pid
                
                # 获取文件扩展名
                file_ext = self.file_utils.get_file_extension(img_url)
                
                # 格式化保存路径
                save_path = self.path_formatter.format_artwork_path(
                    artwork, is_multi_page=False, page_index=0, file_ext=file_ext
                )
                
                # 下载图片
                success = downloader.download_file(img_url, save_path, referer=f'https://www.pixiv.net/artworks/{pid}')
                
                # 创建元数据文件
                if success:
                    metadata_path = self.path_formatter.format_metadata_path(save_path, is_multi_page=False)
                    self.file_utils.write_metadata_file(metadata_path, artwork)
            
            return success, "插画/漫画", pid
            
        except Exception as e:
            self.logger.error(f"下载插画/漫画PID={pid}出错: {e}", exc_info=True)
            return False, "插画/漫画", pid
    
    def _download_novel(self, pid: str, downloader) -> Tuple[bool, str, str]:
        """
        下载小说
        
        Args:
            pid: 作品ID
            downloader: 下载器实例（对于小说不实际使用）
            
        Returns:
            Tuple[bool, str, str]: (是否成功, 作品类型, 作品ID)
        """
        try:
            # 获取小说详情
            novel = self.pixiv_api.get_novel_details(pid)
            
            # 格式化保存路径
            save_path = self.path_formatter.format_novel_path(novel)
            
            # 创建目录
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 对于小说，我们直接写入内容而不是下载文件
            success = self.file_utils.write_metadata_file(save_path, novel, is_novel=True)
            
            return success, "小说", pid
            
        except Exception as e:
            self.logger.error(f"下载小说PID={pid}出错: {e}", exc_info=True)
            return False, "小说", pid


def main():
    """主函数入口点"""
    downloader = PixivTagDownloader()
    downloader.run()


if __name__ == "__main__":
    main()