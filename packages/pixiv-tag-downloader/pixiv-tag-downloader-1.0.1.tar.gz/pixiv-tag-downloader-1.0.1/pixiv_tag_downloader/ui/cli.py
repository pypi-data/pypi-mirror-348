#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行界面模块，提供交互式的命令行用户界面
"""

import os
import sys
import logging
import argparse
from typing import List, Set, Dict, Any, Optional, Tuple

try:
    from colorama import init, Fore, Style
    COLORAMA_AVAILABLE = True
    init()
except ImportError:
    COLORAMA_AVAILABLE = False

from ..config.config_manager import get_config_manager
from ..auth.cookie import get_cookie_manager
from ..api.pixiv import get_pixiv_api
from ..i18n.translation import get_translation_manager


class CLI:
    """命令行界面类，处理用户交互和参数解析"""
    
    def __init__(self):
        """初始化命令行界面"""
        self.logger = logging.getLogger(__name__)
        self.config = get_config_manager()
        self.i18n = get_translation_manager()
        self.use_color = COLORAMA_AVAILABLE and self.config.get('ui.use_color', True)
        self.tags_per_page = self.config.get('ui.tags_per_page', 20)
    
    def parse_arguments(self) -> argparse.Namespace:
        """
        解析命令行参数
        
        Returns:
            argparse.Namespace: 解析后的参数
        """
        parser = argparse.ArgumentParser(
            description=self.i18n.get('app.description'),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        parser.add_argument('-u', '--uid', type=str, help=self.i18n.get('cli.arg.uid'))
        parser.add_argument('-t', '--tags', type=str, help=self.i18n.get('cli.arg.tags'))
        parser.add_argument('-l', '--logic', type=str, choices=['and', 'or'], default='or',
                          help=self.i18n.get('cli.arg.logic'))
        parser.add_argument('--output-dir', type=str, help=self.i18n.get('cli.arg.output_dir'))
        parser.add_argument('--threads', type=int, help=self.i18n.get('cli.arg.threads'))
        parser.add_argument('--download-method', type=str, choices=['direct', 'aria2c', 'aria2-rpc'],
                          help=self.i18n.get('cli.arg.download_method'))
        parser.add_argument('--aria2-rpc-url', type=str, help=self.i18n.get('cli.arg.aria2_rpc_url'))
        parser.add_argument('--config', type=str, help=self.i18n.get('cli.arg.config'))
        parser.add_argument('--language', type=str, help='Set interface language (e.g., zh-CN, en-US, ja-JP)')
        
        return parser.parse_args()
    
    def print_colored(self, text: str, color: str = None, style: str = None) -> None:
        """
        打印彩色文本
        
        Args:
            text: 要打印的文本
            color: 文本颜色
            style: 文本样式
        """
        if not self.use_color:
            print(text)
            return
        
        color_code = ''
        style_code = ''
        
        # 设置颜色
        if color:
            if color.lower() == 'red':
                color_code = Fore.RED
            elif color.lower() == 'green':
                color_code = Fore.GREEN
            elif color.lower() == 'yellow':
                color_code = Fore.YELLOW
            elif color.lower() == 'blue':
                color_code = Fore.BLUE
            elif color.lower() == 'magenta':
                color_code = Fore.MAGENTA
            elif color.lower() == 'cyan':
                color_code = Fore.CYAN
            elif color.lower() == 'white':
                color_code = Fore.WHITE
        
        # 设置样式
        if style:
            if style.lower() == 'bright':
                style_code = Style.BRIGHT
            elif style.lower() == 'dim':
                style_code = Style.DIM
        
        # 打印带颜色的文本
        print(f"{style_code}{color_code}{text}{Style.RESET_ALL}")
    
    def prompt_input(self, prompt_text: str, default: str = None) -> str:
        """
        提示用户输入
        
        Args:
            prompt_text: 提示文本
            default: 默认值
            
        Returns:
            str: 用户输入或默认值
        """
        if default:
            prompt_display = f"{prompt_text} [{default}]: "
        else:
            prompt_display = f"{prompt_text}: "
        
        if self.use_color:
            user_input = input(f"{Fore.CYAN}{Style.BRIGHT}{prompt_display}{Style.RESET_ALL}")
        else:
            user_input = input(prompt_display)
        
        return user_input if user_input else default
    
    def prompt_uid(self) -> str:
        """
        提示用户输入UID
        
        Returns:
            str: 用户输入的有效UID
        """
        while True:
            uid = self.prompt_input("请输入Pixiv用户ID (UID)")
            
            if not uid:
                self.print_colored("错误: UID不能为空", "red")
                continue
            
            if not uid.isdigit():
                self.print_colored("错误: UID必须是纯数字", "red")
                continue
            
            return uid
    
    def display_tags(self, tags: Set[str]) -> None:
        """
        分页显示标签列表
        
        Args:
            tags: 标签集合
        """
        tags_list = sorted(list(tags))
        total_tags = len(tags_list)
        total_pages = (total_tags + self.tags_per_page - 1) // self.tags_per_page
        
        if not tags_list:
            self.print_colored("未找到任何标签", "yellow")
            return
        
        current_page = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            start_idx = current_page * self.tags_per_page
            end_idx = min(start_idx + self.tags_per_page, total_tags)
            
            self.print_colored(f"标签列表 (第 {current_page + 1}/{total_pages} 页, 共 {total_tags} 个):", "green", "bright")
            print()
            
            # 显示标签
            for i, tag in enumerate(tags_list[start_idx:end_idx], start=start_idx + 1):
                if self.use_color:
                    index_str = f"{Fore.YELLOW}{i:3d}{Style.RESET_ALL}"
                    print(f"{index_str}. {tag}")
                else:
                    print(f"{i:3d}. {tag}")
            
            print()
            if total_pages > 1:
                self.print_colored("导航操作:", "cyan")
                print("  n - 下一页")
                print("  p - 上一页")
                print("  q - 退出查看")
                print()
            
            if current_page < total_pages - 1:
                choice = input("按 'n' 查看下一页，或按 'q' 退出查看: ").strip().lower()
                if choice == 'n':
                    current_page += 1
                elif choice == 'p' and current_page > 0:
                    current_page -= 1
                elif choice == 'q':
                    break
            else:
                input("按任意键退出查看")
                break
    
    def prompt_tag_selection(self, tags: Set[str]) -> Tuple[List[str], str]:
        """
        提示用户选择标签和过滤逻辑
        
        Args:
            tags: 可选标签集合
            
        Returns:
            Tuple[List[str], str]: 选择的标签列表和过滤逻辑
        """
        self.print_colored("标签选择", "green", "bright")
        print("1. 选择特定标签")
        print("2. 查看所有可用标签")
        print("3. 下载所有作品 (不使用标签过滤)")
        print()
        
        while True:
            option = self.prompt_input("请选择操作 [1-3]", "1")
            
            if option == '1':
                # 手动输入标签
                tags_input = self.prompt_input("请输入标签，多个标签用逗号分隔")
                selected_tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                
                if not selected_tags:
                    self.print_colored("未选择任何标签，将下载所有作品", "yellow")
                    return [], 'or'
                
                # 验证输入的标签是否存在
                invalid_tags = [tag for tag in selected_tags if tag not in tags]
                if invalid_tags:
                    self.print_colored(f"警告: 以下标签在目标用户的作品中不存在: {', '.join(invalid_tags)}", "yellow")
                    confirm = self.prompt_input("是否继续? (y/n)", "y").lower()
                    if confirm != 'y':
                        continue
                
                # 选择过滤逻辑
                logic = self.prompt_tag_logic()
                return selected_tags, logic
                
            elif option == '2':
                # 查看所有标签
                self.display_tags(tags)
                continue
                
            elif option == '3':
                # 下载所有作品
                self.print_colored("将下载所有作品", "green")
                return [], 'or'
            
            else:
                self.print_colored("无效选择，请重新输入", "red")
    
    def prompt_tag_logic(self) -> str:
        """
        提示用户选择标签过滤逻辑
        
        Returns:
            str: 标签过滤逻辑 ('and' 或 'or')
        """
        self.print_colored("请选择标签过滤逻辑:", "green")
        print("1. AND - 作品必须包含所有选定的标签")
        print("2. OR  - 作品只需包含任意一个选定的标签")
        
        while True:
            choice = self.prompt_input("请选择 [1-2]", "2")
            
            if choice == '1':
                return 'and'
            elif choice == '2':
                return 'or'
            else:
                self.print_colored("无效选择，请重新输入", "red")
    
    def display_summary(self, uid: str, username: str, selected_tags: List[str], 
                      logic: str, artworks_count: Dict[str, int]) -> None:
        """
        显示下载摘要信息
        
        Args:
            uid: 用户ID
            username: 用户名
            selected_tags: 选择的标签列表
            logic: 标签过滤逻辑
            artworks_count: 作品数量字典
        """
        self.print_colored("下载摘要", "green", "bright")
        print(f"用户: {username} (UID: {uid})")
        
        if selected_tags:
            logic_display = "同时包含所有" if logic.lower() == 'and' else "包含任意一个"
            self.print_colored(f"标签过滤: {logic_display} [{', '.join(selected_tags)}]", "cyan")
        else:
            self.print_colored("标签过滤: 无 (下载所有作品)", "cyan")
        
        total_count = sum(artworks_count.values())
        self.print_colored(f"将下载 {total_count} 个作品:", "yellow")
        print(f"  - 插画/漫画: {artworks_count.get('illustrations', 0)}个")
        print(f"  - 小说: {artworks_count.get('novels', 0)}个")
        
        print()
        confirm = self.prompt_input("是否继续? (y/n)", "y").lower()
        
        if confirm != 'y':
            self.print_colored("操作已取消", "yellow")
            sys.exit(0)
    
    def init_and_validate_cookie(self) -> None:
        """
        初始化和验证Cookie
        """
        cookie_manager = get_cookie_manager()
        
        self.print_colored("验证Cookie中...", "cyan")
        success, message = cookie_manager.load_cookie()
        
        if not success:
            self.print_colored(f"Cookie加载失败: {message}", "red")
            self.print_colored("请确保当前目录下存在有效的cookie.txt文件", "yellow")
            sys.exit(1)
        
        # 测试连接有效性
        success, result = cookie_manager.test_connection()
        
        if not success:
            self.print_colored(f"Cookie验证失败: {result}", "red")
            self.print_colored("请检查cookie.txt中的Cookie是否有效", "yellow")
            sys.exit(1)
        
        self.print_colored("Cookie验证成功！", "green")
        
        if isinstance(result, dict) and result.get('name'):
            self.print_colored(f"已登录为: {result.get('name')} (ID: {result.get('id', 'Unknown')})", "green")
    
    def interactive_mode(self) -> Tuple[str, List[str], str]:
        """
        交互式模式，引导用户输入必要信息
        
        Returns:
            Tuple[str, List[str], str]: 用户ID, 选定的标签列表, 过滤逻辑
        """
        # 提示用户输入UID
        uid = self.prompt_uid()
        
        # 获取用户信息和作品
        self.print_colored(f"正在获取UID={uid}的用户信息...", "cyan")
        pixiv_api = get_pixiv_api()
        
        try:
            # 获取用户信息
            user_info = pixiv_api.get_user_info(uid)
            username = user_info.get('name', 'Unknown')
            self.logger.debug(f"User Info from API: {user_info}") # 添加日志
            self.print_colored(f"用户名: {username}", "green")
            
            # 获取所有作品ID
            self.print_colored("正在获取作品列表...", "cyan")
            artworks = pixiv_api.get_user_artworks_ids(uid)
            illustrations_count = len(artworks.get('illustrations', []))
            novels_count = len(artworks.get('novels', []))
            
            self.print_colored(f"找到 {illustrations_count} 个插画/漫画作品和 {novels_count} 个小说", "green")
            
            if illustrations_count == 0 and novels_count == 0:
                self.print_colored("未找到任何作品，请检查UID是否正确", "red")
                sys.exit(1)
            
            # 获取所有标签
            self.print_colored("正在提取作品标签...", "cyan")
            all_tags = pixiv_api.get_all_tags_from_works(artworks.get('illustrations', []) + artworks.get('novels', []))
            self.print_colored(f"共提取到 {len(all_tags)} 个唯一标签", "green")
            
            # 提示用户选择标签
            selected_tags, logic = self.prompt_tag_selection(all_tags)
            
            return uid, selected_tags, logic
            
        except Exception as e:
            self.print_colored(f"出错: {e}", "red")
            sys.exit(1)


# 全局CLI实例
_cli = None


def get_cli() -> CLI:
    """
    获取全局CLI实例
    
    Returns:
        CLI: CLI实例
    """
    global _cli
    if _cli is None:
        _cli = CLI()
    return _cli