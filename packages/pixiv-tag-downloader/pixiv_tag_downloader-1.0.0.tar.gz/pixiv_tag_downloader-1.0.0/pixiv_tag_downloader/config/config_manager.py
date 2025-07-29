#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理模块，负责读取、验证和提供配置信息
"""

import os
import yaml
import json
import logging
import jsonschema
from typing import Dict, Any, Optional

# 配置文件JSON Schema定义
CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "output": {
            "type": "object",
            "properties": {
                "root_dir": {"type": "string"},
                "templates": {
                    "type": "object",
                    "properties": {
                        "main_dir": {"type": "string"},
                        "image_filename": {"type": "string"},
                        "novel_filename": {"type": "string"},
                        "date_format": {"type": "string"},
                        "tag_separator": {"type": "string"}
                    }
                },
                "overwrite": {"type": "boolean"},
                "pid_dir_with_title": {"type": "boolean"}
            },
            "required": ["root_dir"]
        },
        "download": {
            "type": "object",
            "properties": {
                "method": {"type": "string", "enum": ["direct", "aria2c", "aria2-rpc"]},
                "threads": {"type": "integer", "minimum": 1},
                "retries": {"type": "integer", "minimum": 0},
                "timeout": {"type": "number", "minimum": 1},
                "delay": {
                    "type": "object",
                    "properties": {
                        "min": {"type": "number", "minimum": 0},
                        "max": {"type": "number", "minimum": 0}
                    },
                    "required": ["min", "max"]
                },
                "aria2": {
                    "type": "object",
                    "properties": {
                        "rpc_url": {"type": "string"},
                        "token": {"type": "string"},
                        "use_wss": {"type": "boolean"},
                        "verify_cert": {"type": "boolean"},
                        "cert_path": {"type": "string"},
                        "params": {
                            "type": "object",
                            "properties": {
                                "max_connection_per_server": {"type": "integer"},
                                "min_split_size": {"type": "string"},
                                "split": {"type": "integer"}
                            }
                        }
                    }
                }
            },
            "required": ["method", "threads", "delay"]
        },
        "http": {
            "type": "object",
            "properties": {
                "headers": {"type": "object"},
                "proxies": {
                    "type": "object",
                    "properties": {
                        "http": {"type": "string"},
                        "https": {"type": "string"}
                    }
                },
                "use_proxy": {"type": "boolean"}
            }
        },
        "logging": {
            "type": "object",
            "properties": {
                "level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]},
                "file": {"type": "string"},
                "console": {"type": "boolean"},
                "verbose_progress": {"type": "boolean"}
            }
        },
        "ui": {
            "type": "object",
            "properties": {
                "use_color": {"type": "boolean"},
                "language": {"type": "string", "enum": ["en", "zh-cn", "ja"]},
                "tags_per_page": {"type": "integer", "minimum": 1}
            }
        }
    }
}

# 默认配置
DEFAULT_CONFIG = {
    "output": {
        "root_dir": "Output",
        "templates": {
            "main_dir": "{uid}_{username}/{type}/{series}",
            "image_filename": "{date}_{pid}_p{index}_{title}.{ext}",
            "novel_filename": "{date}_{pid}_{title}.txt",
            "date_format": "yyyymmdd",
            "tag_separator": "_"
        },
        "overwrite": False,
        "pid_dir_with_title": True
    },
    "download": {
        "method": "direct",
        "threads": 4,
        "retries": 3,
        "timeout": 30,
        "delay": {
            "min": 1,
            "max": 3
        },
        "aria2": {
            "rpc_url": "http://localhost:6800/jsonrpc",
            "token": "",
            "use_wss": False,
            "verify_cert": True,
            "cert_path": "",
            "params": {
                "max_connection_per_server": 5,
                "min_split_size": "1M",
                "split": 5
            }
        }
    },
    "http": {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Referer": "https://www.pixiv.net/"
        },
        "proxies": {
            "http": "",
            "https": ""
        },
        "use_proxy": False
    },
    "logging": {
        "level": "INFO",
        "file": "",
        "console": True,
        "verbose_progress": True
    },
    "ui": {
        "use_color": True,
        "language": "en",
        "tags_per_page": 20
    }
}


class ConfigManager:
    """配置管理类，负责读取、验证和提供配置信息"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，如果为None则查找默认位置
        """
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = DEFAULT_CONFIG.copy()
        
        # 如果没有提供配置文件路径，则查找默认位置
        if config_path is None:
            # 按优先级检查多个可能的位置
            possible_paths = [
                "./config.yaml",
                "./config.yml",
                os.path.expanduser("~/.pixiv_tag_downloader/config.yaml"),
            ]
            for path in possible_paths:
                if os.path.isfile(path):
                    config_path = path
                    break
        
        # 如果找到了配置文件，则加载它
        if config_path and os.path.isfile(config_path):
            self.load_config(config_path)
        else:
            self.logger.warning("未找到配置文件，使用默认配置")

    def load_config(self, config_path: str) -> bool:
        """
        加载并验证配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
            
            # 验证配置
            jsonschema.validate(instance=user_config, schema=CONFIG_SCHEMA)
            
            # 合并配置
            self._merge_config(self.config, user_config)
            
            self.logger.info(f"成功加载配置文件: {config_path}")
            return True
        except yaml.YAMLError as e:
            self.logger.error(f"解析配置文件出错: {e}")
        except jsonschema.exceptions.ValidationError as e:
            self.logger.error(f"配置文件验证失败: {e}")
        except Exception as e:
            self.logger.error(f"加载配置文件时出错: {e}")
        
        return False
    
    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> None:
        """
        深度合并两个配置字典，用户配置会覆盖默认配置
        
        Args:
            default: 默认配置字典
            user: 用户配置字典
        """
        for key, value in user.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                default[key] = value
    
    def get(self, key: str = None, default: Any = None) -> Any:
        """
        获取配置项
        
        Args:
            key: 配置键，使用点号分隔层级，如"output.root_dir"
            default: 如果配置项不存在，返回的默认值
            
        Returns:
            Any: 配置项的值，如果不存在则返回默认值
        """
        if key is None:
            return self.config
        
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置项
        
        Args:
            key: 配置键，使用点号分隔层级，如"output.root_dir"
            value: 要设置的值
        """
        keys = key.split('.')
        config = self.config
        
        # 导航到最后一层
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        返回完整的配置字典
        
        Returns:
            Dict[str, Any]: 配置字典
        """
        return self.config.copy()
    
    def save(self, path: str) -> bool:
        """
        保存当前配置到文件
        
        Args:
            path: 配置文件保存路径
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
            
            # 保存配置
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            self.logger.info(f"配置已保存到: {path}")
            return True
        except Exception as e:
            self.logger.error(f"保存配置文件时出错: {e}")
            return False


# 全局配置管理器实例
_config_manager = None


def get_config_manager(config_path: Optional[str] = None) -> ConfigManager:
    """
    获取全局配置管理器实例
    
    Args:
        config_path: 配置文件路径，仅在第一次调用时有效
        
    Returns:
        ConfigManager: 配置管理器实例
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_path)
    return _config_manager