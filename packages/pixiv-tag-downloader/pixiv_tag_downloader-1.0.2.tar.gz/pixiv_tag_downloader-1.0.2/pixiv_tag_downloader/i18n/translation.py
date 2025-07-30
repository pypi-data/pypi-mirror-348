#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
翻译管理模块，负责加载和管理多语言翻译
"""

import os
import json
import logging
from typing import Dict, Optional

from ..config.config_manager import get_config_manager

# 单例实例
_translation_manager_instance = None


def get_translation_manager() -> 'TranslationManager':
    """获取翻译管理器单例实例"""
    global _translation_manager_instance
    if _translation_manager_instance is None:
        _translation_manager_instance = TranslationManager()
    return _translation_manager_instance


class TranslationManager:
    """翻译管理器，负责加载和提供翻译"""
    
    def __init__(self):
        """初始化翻译管理器"""
        self.logger = logging.getLogger(__name__)
        self.config = get_config_manager()
        self.translations: Dict[str, Dict[str, str]] = {}
        self.current_language = self.config.get('ui.language', 'zh-CN')
        
        # 加载翻译
        self._load_translations()
    
    def _load_translations(self) -> None:
        """加载所有可用的翻译文件"""
        # 获取翻译文件目录
        package_dir = os.path.dirname(os.path.abspath(__file__))
        translations_dir = os.path.join(package_dir, 'translations')
        
        # 如果目录不存在，创建它
        if not os.path.exists(translations_dir):
            os.makedirs(translations_dir)
            self.logger.warning(f"已创建翻译目录: {translations_dir}")
        
        # 扫描并加载翻译文件
        try:
            for filename in os.listdir(translations_dir):
                if filename.endswith('.json'):
                    language_code = filename.replace('.json', '')
                    file_path = os.path.join(translations_dir, filename)
                    self._load_translation_file(language_code, file_path)
            
            # 如果没有找到任何翻译文件，创建默认翻译
            if not self.translations:
                self._create_default_translations(translations_dir)
        
        except Exception as e:
            self.logger.error(f"加载翻译文件时出错: {e}")
    
    def _load_translation_file(self, language_code: str, file_path: str) -> None:
        """
        加载单个翻译文件
        
        Args:
            language_code: 语言代码
            file_path: 翻译文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translation_data = json.load(f)
                self.translations[language_code] = translation_data
                self.logger.info(f"已加载 {language_code} 翻译 ({len(translation_data)} 条)")
        except Exception as e:
            self.logger.error(f"加载翻译文件 {file_path} 时出错: {e}")
    
    def _create_default_translations(self, translations_dir: str) -> None:
        """
        创建默认翻译文件
        
        Args:
            translations_dir: 翻译文件目录
        """
        # 默认支持中文、英文和日文
        default_translations = {
            'zh-CN': self._get_default_zh_cn(),
            'en-US': self._get_default_en_us(),
            'ja-JP': self._get_default_ja_jp()
        }
        
        # 写入翻译文件
        for lang_code, translations in default_translations.items():
            file_path = os.path.join(translations_dir, f"{lang_code}.json")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(translations, f, ensure_ascii=False, indent=2)
                self.translations[lang_code] = translations
                self.logger.info(f"已创建默认 {lang_code} 翻译文件")
            except Exception as e:
                self.logger.error(f"创建默认翻译文件 {file_path} 时出错: {e}")
    
    def _get_default_zh_cn(self) -> Dict[str, str]:
        """获取默认中文翻译"""
        return {
            # 通用
            "app.name": "Pixiv标签下载器",
            "app.description": "下载指定用户的作品，支持标签过滤",
            
            # 命令行参数
            "cli.arg.uid": "指定Pixiv用户ID",
            "cli.arg.tags": "要下载的标签，多个标签用逗号分隔",
            "cli.arg.logic": "标签过滤逻辑，\"and\"表示同时包含所有标签，\"or\"表示包含任一标签",
            "cli.arg.output_dir": "指定输出目录，覆盖配置文件中的设置",
            "cli.arg.threads": "指定下载线程数，覆盖配置文件中的设置",
            "cli.arg.download_method": "指定下载方式",
            "cli.arg.aria2_rpc_url": "指定Aria2 RPC服务地址",
            "cli.arg.config": "指定配置文件路径",
            
            # 用户界面
            "ui.welcome": "欢迎使用 Pixiv标签下载器",
            "ui.cookie.prompt": "请输入Pixiv Cookie (PHPSESSID):",
            "ui.cookie.success": "Cookie验证成功！用户名: {username}",
            "ui.cookie.failure": "Cookie验证失败: {error}",
            "ui.uid.prompt": "请输入要下载的Pixiv用户ID:",
            "ui.tag.prompt": "请输入要下载的标签 (留空下载全部, 多个标签用逗号分隔):",
            "ui.logic.prompt": "标签过滤逻辑 [1=OR, 2=AND]:",
            "ui.download.start": "开始下载用户 {uid} ({username}) 的作品",
            "ui.download.complete": "下载完成！共下载 {success_count} 个文件, {failed_count} 个失败",
            "ui.download.progress": "进度: {current}/{total}",
            
            # 错误信息
            "error.config.load": "加载配置文件时出错: {error}",
            "error.network": "网络错误: {error}",
            "error.api": "API错误: {error}",
            "error.download": "下载文件时出错: {error}",
            
            # 文件元数据
            "metadata.title": "标题",
            "metadata.author_uid": "作者UID",
            "metadata.author_username": "作者用户名",
            "metadata.artwork_pid": "作品PID",
            "metadata.novel_pid": "小说PID",
            "metadata.upload_date": "上传时间",
            "metadata.create_date": "创建时间",
            "metadata.tags": "标签",
            "metadata.series": "系列",
            "metadata.description": "描述",
            "metadata.content": "正文"
        }
    
    def _get_default_en_us(self) -> Dict[str, str]:
        """获取默认英文翻译"""
        return {
            # General
            "app.name": "Pixiv Tag Downloader",
            "app.description": "Download artworks from specified users, with tag filtering support",
            
            # Command line arguments
            "cli.arg.uid": "Specify Pixiv user ID",
            "cli.arg.tags": "Tags to download, separate multiple tags with commas",
            "cli.arg.logic": "Tag filtering logic, \"and\" means include all tags, \"or\" means include any tag",
            "cli.arg.output_dir": "Specify output directory, overrides the setting in config file",
            "cli.arg.threads": "Specify download threads, overrides the setting in config file",
            "cli.arg.download_method": "Specify download method",
            "cli.arg.aria2_rpc_url": "Specify Aria2 RPC server address",
            "cli.arg.config": "Specify config file path",
            
            # User interface
            "ui.welcome": "Welcome to Pixiv Tag Downloader",
            "ui.cookie.prompt": "Please enter your Pixiv Cookie (PHPSESSID):",
            "ui.cookie.success": "Cookie validation successful! Username: {username}",
            "ui.cookie.failure": "Cookie validation failed: {error}",
            "ui.uid.prompt": "Please enter the Pixiv user ID to download:",
            "ui.tag.prompt": "Please enter tags to download (leave empty for all, separate multiple tags with commas):",
            "ui.logic.prompt": "Tag filtering logic [1=OR, 2=AND]:",
            "ui.download.start": "Starting download for user {uid} ({username})",
            "ui.download.complete": "Download complete! Total: {success_count} files downloaded, {failed_count} failed",
            "ui.download.progress": "Progress: {current}/{total}",
            
            # Error messages
            "error.config.load": "Error loading config file: {error}",
            "error.network": "Network error: {error}",
            "error.api": "API error: {error}",
            "error.download": "Error downloading file: {error}",
            
            # File metadata
            "metadata.title": "Title",
            "metadata.author_uid": "Author UID",
            "metadata.author_username": "Author Username",
            "metadata.artwork_pid": "Artwork PID",
            "metadata.novel_pid": "Novel PID",
            "metadata.upload_date": "Upload Date",
            "metadata.create_date": "Create Date",
            "metadata.tags": "Tags",
            "metadata.series": "Series",
            "metadata.description": "Description",
            "metadata.content": "Content"
        }
    
    def _get_default_ja_jp(self) -> Dict[str, str]:
        """获取默认日文翻译"""
        return {
            # 一般
            "app.name": "Pixivタグダウンローダー",
            "app.description": "指定されたユーザーの作品をダウンロードし、タグフィルタリングをサポート",
            
            # コマンドライン引数
            "cli.arg.uid": "PixivユーザーIDを指定",
            "cli.arg.tags": "ダウンロードするタグ、複数のタグはカンマで区切り",
            "cli.arg.logic": "タグフィルタリングロジック、「and」は全てのタグを含む、「or」はいずれかのタグを含む",
            "cli.arg.output_dir": "出力ディレクトリを指定、設定ファイルの設定を上書き",
            "cli.arg.threads": "ダウンロードスレッド数を指定、設定ファイルの設定を上書き",
            "cli.arg.download_method": "ダウンロード方法を指定",
            "cli.arg.aria2_rpc_url": "Aria2 RPCサーバーアドレスを指定",
            "cli.arg.config": "設定ファイルのパスを指定",
            
            # ユーザーインターフェース
            "ui.welcome": "Pixivタグダウンローダーへようこそ",
            "ui.cookie.prompt": "PixivのCookie (PHPSESSID)を入力してください:",
            "ui.cookie.success": "Cookie認証成功！ユーザー名: {username}",
            "ui.cookie.failure": "Cookie認証失敗: {error}",
            "ui.uid.prompt": "ダウンロードするPixivユーザーIDを入力してください:",
            "ui.tag.prompt": "ダウンロードするタグを入力してください (空白ですべてをダウンロード、複数のタグはカンマで区切り):",
            "ui.logic.prompt": "タグフィルタリングロジック [1=OR, 2=AND]:",
            "ui.download.start": "ユーザー {uid} ({username}) の作品のダウンロードを開始します",
            "ui.download.complete": "ダウンロード完了！合計: {success_count} ファイルダウンロード、{failed_count} 失敗",
            "ui.download.progress": "進捗: {current}/{total}",
            
            # エラーメッセージ
            "error.config.load": "設定ファイルの読み込みエラー: {error}",
            "error.network": "ネットワークエラー: {error}",
            "error.api": "APIエラー: {error}",
            "error.download": "ファイルダウンロードエラー: {error}",
            
            # ファイルメタデータ
            "metadata.title": "タイトル",
            "metadata.author_uid": "作者UID",
            "metadata.author_username": "作者ユーザー名",
            "metadata.artwork_pid": "作品PID",
            "metadata.novel_pid": "小説PID",
            "metadata.upload_date": "アップロード日時",
            "metadata.create_date": "作成日時",
            "metadata.tags": "タグ",
            "metadata.series": "シリーズ",
            "metadata.description": "説明",
            "metadata.content": "本文"
        }
    
    def get_language(self) -> str:
        """
        获取当前语言
        
        Returns:
            str: 当前语言代码
        """
        return self.current_language
    
    def set_language(self, language: str) -> bool:
        """
        设置当前语言
        
        Args:
            language: 语言代码
            
        Returns:
            bool: 是否设置成功
        """
        if language in self.translations:
            self.current_language = language
            self.config.set('ui.language', language)
            return True
        else:
            self.logger.warning(f"不支持的语言: {language}")
            return False
    
    def get_available_languages(self) -> Dict[str, str]:
        """
        获取所有可用的语言
        
        Returns:
            Dict[str, str]: 语言代码到语言名称的映射
        """
        languages = {
            'zh-CN': '简体中文',
            'en-US': 'English',
            'ja-JP': '日本語'
        }
        # 只返回已加载翻译的语言
        return {code: name for code, name in languages.items() if code in self.translations}
    
    def get(self, key: str, default: Optional[str] = None, **kwargs) -> str:
        """
        获取指定键的翻译文本
        
        Args:
            key: 翻译键
            default: 默认文本，如果没有找到翻译则返回此值
            **kwargs: 用于格式化翻译文本的参数
            
        Returns:
            str: 翻译后的文本
        """
        # 从当前语言中获取翻译
        translation = self.translations.get(self.current_language, {}).get(key)
        
        # 如果当前语言没有找到翻译，尝试从英文翻译中获取
        if translation is None and self.current_language != 'en-US':
            translation = self.translations.get('en-US', {}).get(key)
        
        # 如果仍然没有找到翻译，尝试从中文翻译中获取
        if translation is None and self.current_language != 'zh-CN':
            translation = self.translations.get('zh-CN', {}).get(key)
        
        # 如果所有语言都没有找到翻译，使用默认值或键名
        if translation is None:
            translation = default if default is not None else key
        
        # 应用格式化参数
        if kwargs and isinstance(translation, str):
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                self.logger.warning(f"翻译格式化出错，缺少参数 {e} 在键 {key} 中")
        
        return translation
