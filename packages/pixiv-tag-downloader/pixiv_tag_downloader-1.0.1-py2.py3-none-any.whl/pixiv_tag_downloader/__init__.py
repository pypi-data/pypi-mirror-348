#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pixiv Tag Downloader - 根据标签下载Pixiv用户作品

本模块提供了下载Pixiv用户作品的功能，支持按标签过滤，
并提供多种下载方式和输出格式选项。
"""

__version__ = '1.0.1'
__author__ = 'Mannix Sun'
__email__ = 'root@teamcs.org'
__license__ = 'MIT'

from .api.pixiv import get_pixiv_api
from .auth.cookie import get_cookie_manager
from .config.config_manager import get_config_manager
from .download.direct import get_direct_downloader
from .download.aria2 import get_aria2_cli, get_aria2_rpc, create_downloader
from .utils.path_formatter import get_path_formatter
from .utils.file_utils import get_file_utils
from .ui.cli import get_cli