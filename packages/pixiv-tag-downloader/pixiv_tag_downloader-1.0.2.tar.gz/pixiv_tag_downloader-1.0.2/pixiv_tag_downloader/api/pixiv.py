#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pixiv API模块，负责与Pixiv网站API进行交互
提供用户信息获取、作品列表获取、作品详情获取等功能
"""

import time
import random
import logging
import requests
from typing import Dict, List, Set

from ..auth.cookie import get_cookie_manager
from ..config.config_manager import get_config_manager


class PixivAPI:
    """Pixiv API交互类，提供与Pixiv网站API交互的方法"""
    
    def __init__(self):
        """初始化PixivAPI"""
        self.logger = logging.getLogger(__name__)
        self.session = get_cookie_manager().get_session()
        self.config = get_config_manager()
        self.headers = self.config.get('http.headers', {})
        
        # 配置代理设置
        if self.config.get('http.use_proxy', False):
            proxies = self.config.get('http.proxies', {})
            if proxies.get('http') or proxies.get('https'):
                self.session.proxies.update(proxies)
                self.logger.info(f"已设置代理: {proxies}")
    
    def _request(self, url: str, method: str = 'GET', params: Dict = None, 
                data: Dict = None, json: Dict = None) -> Dict:
        """
        发送请求到Pixiv API并处理响应
        
        Args:
            url: 请求URL
            method: 请求方法，默认为GET
            params: URL查询参数
            data: POST表单数据
            json: POST JSON数据
            
        Returns:
            Dict: API响应的JSON数据
        
        Raises:
            requests.RequestException: 请求出错
            ValueError: 响应解析出错
            Exception: 其他错误
        """
        # 添加随机延迟
        self._random_sleep()
        
        # 更新请求头，增加更多的浏览器特征
        updated_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Referer': 'https://www.pixiv.net/',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # 合并配置的头信息和更新的头信息
        merged_headers = {**self.headers, **updated_headers}
        
        # 准备请求
        request_kwargs = {
            'headers': merged_headers,
            'timeout': self.config.get('download.timeout', 30)
        }
        if params:
            request_kwargs['params'] = params
        if data:
            request_kwargs['data'] = data
        if json:
            request_kwargs['json'] = json
        
        # 发送请求
        response = self.session.request(method, url, **request_kwargs)
        response.raise_for_status()
        
        # 解析响应
        response_json = response.json()
          # 检查API错误
        if response_json.get('error') is not None and response_json.get('error'):
            error_message = response_json.get('message', '未知API错误')
            raise Exception(f"Pixiv API错误: {error_message}")
            
        return response_json
    
    def _random_sleep(self) -> None:
        """添加随机延迟，模拟人类行为"""
        min_delay = self.config.get('download.delay.min', 1)
        max_delay = self.config.get('download.delay.max', 3)
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def get_user_info(self, uid: str) -> Dict:
        """
        获取用户信息
        
        Args:
            uid: 用户ID
            
        Returns:
            Dict: 用户信息字典
        
        Raises:
            Exception: 获取用户信息出错
        """
        try:
            url = f'https://www.pixiv.net/ajax/user/{uid}'
            response = self._request(url)
            user_data = response.get('body', {}) # 将 'body' 修改为 'userData'，如果确认API变动
            self.logger.debug(f"Get User Info API Response for UID {uid}: {response}") # 添加日志
            
            if not user_data:
                raise Exception(f"无法获取UID为{uid}的用户信息")
                
            self.logger.info(f"成功获取用户信息: UID={uid}, 用户名={user_data.get('name')}")
            return user_data
        except Exception as e:
            self.logger.error(f"获取用户信息失败: {e}")
            raise Exception(f"获取用户信息失败: {e}")
    
    def get_user_artworks_ids(self, uid: str) -> Dict[str, List[str]]:
        """
        获取用户的作品ID列表，分类为插画/漫画和小说
        
        Args:
            uid: 用户ID
            
        Returns:
            Dict[str, List[str]]: 包含作品ID的字典，格式为{'illustrations': [...], 'novels': [...]}
        
        Raises:
            Exception: 获取作品ID列表出错
        """
        try:
            results = {'illustrations': [], 'novels': []}
            
            # 获取插画和漫画ID列表
            illust_url = f'https://www.pixiv.net/ajax/user/{uid}/profile/all'
            illust_response = self._request(illust_url)
            illust_data = illust_response.get('body', {})
            
            # 合并插画和漫画ID
            illusts_data = illust_data.get('illusts', {})
            manga_data = illust_data.get('manga', {})
            illustrations = list(illusts_data.keys()) if isinstance(illusts_data, dict) else []
            manga = list(manga_data.keys()) if isinstance(manga_data, dict) else []
            results['illustrations'] = illustrations + manga
            
            # 从 /profile/all 接口的响应中提取小说ID (illust_data 即为 profile/all 的 body)
            novels_map_from_profile = illust_data.get('novels', {})
            novel_ids = list(novels_map_from_profile.keys()) if isinstance(novels_map_from_profile, dict) else []
            results['novels'] = novel_ids
            
            total_works = len(results['illustrations']) + len(results['novels'])
            self.logger.info(f"成功获取用户作品ID列表: UID={uid}, 总数={total_works} (插画/漫画: {len(results['illustrations'])}, 小说: {len(results['novels'])})")
            return results
        except Exception as e:
            self.logger.error(f"获取用户作品ID列表失败: {e}")
            self.logger.debug("详细错误信息:", exc_info=True) # 添加详细错误日志
            raise Exception(f"获取用户作品ID列表失败: {e}")
    
    def get_artwork_details(self, pid: str) -> Dict:
        """
        获取作品详细信息
        
        Args:
            pid: 作品ID
            
        Returns:
            Dict: 作品详细信息
            
        Raises:
            Exception: 获取作品详情出错
        """
        try:
            url = f'https://www.pixiv.net/ajax/illust/{pid}'
            response = self._request(url)
            artwork_data = response.get('body', {})
            
            if not artwork_data:
                raise Exception(f"无法获取PID为{pid}的作品信息")
            
            # 获取作品页数信息
            if int(artwork_data.get('pageCount', 1)) > 1:
                pages = self.get_artwork_pages(pid)
                artwork_data['pages'] = pages
            
            self.logger.info(f"成功获取作品详情: PID={pid}, 标题={artwork_data.get('title')}")
            return artwork_data
        except Exception as e:
            self.logger.error(f"获取作品详情失败: {e}")
            raise Exception(f"获取作品详情失败: {e}")
    
    def get_artwork_pages(self, pid: str) -> List[Dict]:
        """
        获取多页作品的所有页面信息
        
        Args:
            pid: 作品ID
            
        Returns:
            List[Dict]: 包含所有页面信息的列表
            
        Raises:
            Exception: 获取页面信息出错
        """
        try:
            url = f'https://www.pixiv.net/ajax/illust/{pid}/pages'
            response = self._request(url)
            pages_data = response.get('body', [])
            
            if not pages_data:
                raise Exception(f"无法获取PID为{pid}的作品页面信息")
            
            self.logger.info(f"成功获取多页作品信息: PID={pid}, 页数={len(pages_data)}")
            return pages_data
        except Exception as e:
            self.logger.error(f"获取多页作品信息失败: {e}")
            raise Exception(f"获取多页作品信息失败: {e}")
    
    def get_novel_details(self, pid: str) -> Dict:
        """
        获取单篇小说的详细信息，包括元数据和内容
        
        Args:
            pid: 小说ID
            
        Returns:
            Dict: 小说详情字典
        
        Raises:
            Exception: 获取小说详情出错
        """
        try:
            # 获取小说元数据
            url_meta = f'https://www.pixiv.net/ajax/novel/{pid}'
            self.logger.debug(f"Fetching novel metadata from: {url_meta}")
            response_meta = self._request(url_meta) # This is the full JSON response dictionary
            
            self.logger.debug(f"Full metadata response for novel PID {pid}: {response_meta}")

            # Try to extract the main novel data dictionary.
            # It might be in a 'body' field, or the response_meta itself might be the data.
            novel_data_dict = response_meta.get('body', response_meta) 
            if not isinstance(novel_data_dict, dict): # If 'body' wasn't there or response_meta isn't a dict
                self.logger.error(f"Could not extract a valid dictionary from novel metadata response for PID {pid}. Response: {response_meta}")
                raise Exception("无法解析小说元数据结构")

            self.logger.debug(f"Extracted novel data dictionary for PID {pid}: {novel_data_dict}")

            # 检查元数据中是否已包含小说内容
            # Common keys for novel text are 'content', 'text', 'novel_text'.
            # Assuming 'content' is the key for the actual novel text.
            if 'content' in novel_data_dict and novel_data_dict['content']:
                self.logger.info(f"小说内容已在元数据中找到 (PID: {pid})。将跳过对 /content 端点的调用。")
                # Assuming novel_data_dict now contains all necessary fields (id, title, author, content, tags, etc.)
                return novel_data_dict
            else:
                self.logger.warning(f"小说内容未在元数据中找到 (PID: {pid})。将尝试访问 /content 端点 (已知可能返回404)。")
                # 如果元数据中没有内容，则按原逻辑尝试获取 /content (这部分代码保持不变，并将触发用户报告的404错误)
                # 这表明内容无法通过当前已知的方法获取

            # 获取小说内容 (原逻辑，如果上面if条件不满足则执行)
            url_content = f'https://www.pixiv.net/ajax/novel/{pid}/content'
            self.logger.debug(f"Fetching novel content from: {url_content}")
            response_content = self._request(url_content) # This request is expected to fail with 404 based on user report
            
            # Similar extraction for content data
            content_data_dict = response_content.get('body', response_content)
            if not isinstance(content_data_dict, dict):
                self.logger.error(f"Could not extract a valid dictionary from novel content response for PID {pid}. Response: {response_content}")
                # If /content call was successful but response is not as expected
                content_data_dict = {} # Avoid erroring out if we just want to merge what we got
            
            self.logger.debug(f"Extracted novel content dictionary for PID {pid}: {content_data_dict}")

            # 合并元数据和内容数据
            final_data = novel_data_dict.copy() # Start with data from metadata endpoint
            final_data.update(content_data_dict) # Merge data from content endpoint (if any)
            
            if not final_data.get('content'):
                 self.logger.warning(f"最终未能获取到小说 PID {pid} 的内容。")

            return final_data
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"获取小说详情时发生HTTP错误 (PID: {pid}): {http_err}", exc_info=True)
            raise Exception(f"获取小说详情失败: {http_err}")
        except Exception as e:
            self.logger.error(f"获取小说详情时发生未知错误 (PID: {pid}): {e}", exc_info=True)
            raise Exception(f"获取小说详情失败: {e}")
    
    def get_all_tags_from_works(self, artwork_ids: List[str]) -> Set[str]:
        """
        从作品列表中提取所有唯一的标签
        
        Args:
            artwork_ids: 作品ID列表
            
        Returns:
            Set[str]: 唯一标签集合
        """
        all_tags = set()
        
        for pid in artwork_ids[:100]:  # 限制为前100个作品，避免请求过多
            try:
                if not pid:
                    continue
                
                self.logger.debug(f"正在获取作品PID={pid}的标签")
                artwork = self.get_artwork_details(pid)
                tags = artwork.get('tags', {}).get('tags', [])
                
                for tag in tags:
                    tag_name = tag.get('tag', '')
                    if tag_name:
                        all_tags.add(tag_name)
                        
                self.logger.debug(f"成功获取作品PID={pid}的标签: {[t.get('tag', '') for t in tags]}")
            except Exception as e:
                self.logger.warning(f"获取作品PID={pid}的标签失败: {e}")
                continue
                
        self.logger.info(f"成功提取所有作品的唯一标签，共{len(all_tags)}个")
        return all_tags
    
    def filter_artworks_by_tags(self, artworks: Dict, 
                              selected_tags: List[str], 
                              logic: str = 'OR') -> Dict[str, List[str]]:
        """
        根据选定的标签过滤作品
        
        Args:
            artworks: 作品字典，格式为{'illustrations': [...], 'novels': [...]}
            selected_tags: 选定的标签列表
            logic: 过滤逻辑，'AND'表示作品必须包含所有选定标签，'OR'表示作品包含任一选定标签
            
        Returns:
            Dict[str, List[str]]: 过滤后的作品字典
        """
        if not selected_tags:
            self.logger.info("未选定标签，返回所有作品")
            return artworks
            
        filtered = {'illustrations': [], 'novels': []}
        
        # 过滤插画/漫画
        for pid in artworks['illustrations']:
            try:
                artwork = self.get_artwork_details(pid)
                tags = [tag.get('tag', '') for tag in artwork.get('tags', {}).get('tags', [])]
                
                if self._match_tags(tags, selected_tags, logic):
                    filtered['illustrations'].append(pid)
                    
            except Exception as e:
                self.logger.warning(f"过滤作品PID={pid}时出错: {e}")
                continue
                
        # 过滤小说
        for pid in artworks['novels']:
            try:
                novel = self.get_novel_details(pid)
                tags = [tag.get('tag', '') for tag in novel.get('tags', {}).get('tags', [])]
                
                if self._match_tags(tags, selected_tags, logic):
                    filtered['novels'].append(pid)
                    
            except Exception as e:
                self.logger.warning(f"过滤小说PID={pid}时出错: {e}")
                continue
                
        total_filtered = len(filtered['illustrations']) + len(filtered['novels'])
        self.logger.info(f"标签过滤完成，过滤后作品数量: {total_filtered} (插画/漫画: {len(filtered['illustrations'])}, 小说: {len(filtered['novels'])})")
        return filtered
    
    def _match_tags(self, artwork_tags: List[str], selected_tags: List[str], logic: str) -> bool:
        """
        判断作品标签是否匹配选定标签
        
        Args:
            artwork_tags: 作品的标签列表
            selected_tags: 选定的标签列表
            logic: 匹配逻辑，'AND'或'OR'
            
        Returns:
            bool: 是否匹配
        """
        if logic.upper() == 'AND':
            return all(tag in artwork_tags for tag in selected_tags)
        else:  # OR
            return any(tag in artwork_tags for tag in selected_tags)


# 全局API实例
_pixiv_api = None


def get_pixiv_api() -> PixivAPI:
    """
    获取全局PixivAPI实例
    
    Returns:
        PixivAPI: API实例
    """
    global _pixiv_api
    if _pixiv_api is None:
        _pixiv_api = PixivAPI()
    return _pixiv_api