"""
微信公众号文章爬虫
功能：根据公众号名称，爬取该公众号的文章列表和文章内容
方案：
  1. 通过搜狗微信搜索获取公众号文章（无需登录，但仅能获取最近文章）
  2. 通过微信公众号后台接口获取文章（需要登录微信公众平台）

作者：DZH123553
"""

import os
import re
import time
import json
import random
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
from datetime import datetime


class WeChatCrawler:
    """微信公众号文章爬虫基类"""

    def __init__(self, output_dir="./output"):
        """
        初始化爬虫
        
        Args:
            output_dir: 文章保存目录
        """
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        os.makedirs(output_dir, exist_ok=True)

    def _random_delay(self, min_sec=2, max_sec=5):
        """随机延时，避免被反爬"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _save_article(self, article, account_name):
        """
        保存文章到本地文件
        
        Args:
            article: 文章字典，包含 title, content, url, publish_time 等
            account_name: 公众号名称
        """
        account_dir = os.path.join(self.output_dir, self._sanitize_filename(account_name))
        os.makedirs(account_dir, exist_ok=True)

        title = self._sanitize_filename(article.get("title", "untitled"))
        filename = f"{title}.md"
        filepath = os.path.join(account_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {article.get('title', '')}\n\n")
            f.write(f"**公众号**: {account_name}\n\n")
            f.write(f"**发布时间**: {article.get('publish_time', '未知')}\n\n")
            f.write(f"**原文链接**: {article.get('url', '')}\n\n")
            f.write("---\n\n")
            f.write(article.get("content", ""))

        print(f"  [已保存] {filepath}")
        return filepath

    @staticmethod
    def _sanitize_filename(name):
        """清理文件名中的非法字符"""
        return re.sub(r'[\\/*?:"<>|]', "_", name).strip()[:100]


class SogouWeChatCrawler(WeChatCrawler):
    """
    方案一：通过搜狗微信搜索爬取公众号文章
    
    优点：不需要登录微信公众平台，操作简单
    缺点：只能获取最近约10篇文章，搜狗有反爬机制
    适用场景：快速获取某公众号最近的文章
    """

    SOGOU_SEARCH_URL = "https://weixin.sogou.com/weixin"

    def search_account(self, account_name):
        """
        搜索公众号
        
        Args:
            account_name: 公众号名称
            
        Returns:
            公众号信息字典，包含名称、链接等
        """
        params = {
            "type": "1",  # 1=搜公众号, 2=搜文章
            "query": account_name,
            "ie": "utf8",
            "s_from": "input",
        }

        try:
            response = self.session.get(self.SOGOU_SEARCH_URL, params=params, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 解析搜索结果
            accounts = []
            items = soup.select("div.txt-box")
            for item in items:
                name_tag = item.select_one("p.tit a")
                if name_tag:
                    name = name_tag.get_text(strip=True)
                    link = name_tag.get("href", "")
                    if link and not link.startswith("http"):
                        link = "https://weixin.sogou.com" + link
                    
                    wechat_id_tag = item.select_one("label[name='em_weixinhao']")
                    wechat_id = wechat_id_tag.get_text(strip=True) if wechat_id_tag else ""
                    
                    accounts.append({
                        "name": name,
                        "wechat_id": wechat_id,
                        "profile_url": link,
                    })

            return accounts

        except Exception as e:
            print(f"[错误] 搜索公众号失败: {e}")
            return []

    def get_articles_by_account(self, account_name, max_articles=10):
        """
        根据公众号名称获取文章列表
        
        Args:
            account_name: 公众号名称
            max_articles: 最大获取文章数
            
        Returns:
            文章列表
        """
        print(f"\n[搜狗方案] 正在搜索公众号: {account_name}")
        
        # 先搜索文章
        params = {
            "type": "2",  # 搜文章
            "query": account_name,
            "ie": "utf8",
            "s_from": "input",
        }

        try:
            response = self.session.get(self.SOGOU_SEARCH_URL, params=params, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            articles = []
            items = soup.select("div.txt-box")

            for item in items[:max_articles]:
                title_tag = item.select_one("h3 a")
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)
                url = title_tag.get("href", "")
                if url and not url.startswith("http"):
                    url = "https://weixin.sogou.com" + url

                # 获取来源和时间
                source_tag = item.select_one("div.s-p")
                account = ""
                pub_time = ""
                if source_tag:
                    account_tag = source_tag.select_one("a")
                    account = account_tag.get_text(strip=True) if account_tag else ""
                    time_tag = source_tag.select_one("span.s2")
                    pub_time = time_tag.get_text(strip=True) if time_tag else ""

                # 获取摘要
                summary_tag = item.select_one("p.txt-info")
                summary = summary_tag.get_text(strip=True) if summary_tag else ""

                articles.append({
                    "title": title,
                    "url": url,
                    "account": account,
                    "publish_time": pub_time,
                    "summary": summary,
                })

            print(f"  找到 {len(articles)} 篇文章")
            return articles

        except Exception as e:
            print(f"[错误] 获取文章列表失败: {e}")
            return []

    def get_article_content(self, article_url):
        """
        获取文章正文内容
        
        Args:
            article_url: 文章URL
            
        Returns:
            文章内容字典
        """
        try:
            self._random_delay(1, 3)
            response = self.session.get(article_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 微信文章页面解析
            title = ""
            content = ""

            # 尝试解析标题
            title_tag = soup.select_one("#activity-name") or soup.select_one("h1.rich_media_title")
            if title_tag:
                title = title_tag.get_text(strip=True)

            # 尝试解析正文
            content_tag = soup.select_one("#js_content") or soup.select_one("div.rich_media_content")
            if content_tag:
                # 提取文本内容，保留段落结构
                content = self._html_to_markdown(content_tag)

            # 尝试解析发布时间
            pub_time = ""
            time_tag = soup.select_one("#publish_time") or soup.select_one("em#publish_time")
            if time_tag:
                pub_time = time_tag.get_text(strip=True)

            # 尝试解析作者
            author = ""
            author_tag = soup.select_one("#js_name") or soup.select_one("a.rich_media_meta_link")
            if author_tag:
                author = author_tag.get_text(strip=True)

            return {
                "title": title,
                "content": content,
                "publish_time": pub_time,
                "author": author,
                "url": article_url,
            }

        except Exception as e:
            print(f"[错误] 获取文章内容失败: {e}")
            return None

    def crawl(self, account_name, max_articles=10, save=True):
        """
        爬取指定公众号的文章
        
        Args:
            account_name: 公众号名称
            max_articles: 最大爬取文章数
            save: 是否保存到本地
            
        Returns:
            文章列表（含内容）
        """
        articles = self.get_articles_by_account(account_name, max_articles)
        results = []

        for i, article in enumerate(articles):
            print(f"  正在获取第 {i+1}/{len(articles)} 篇: {article['title']}")
            content_data = self.get_article_content(article["url"])

            if content_data:
                article.update(content_data)
                if save:
                    self._save_article(article, account_name)
                results.append(article)
            
            self._random_delay(2, 5)

        print(f"\n[完成] 共获取 {len(results)} 篇文章")
        return results

    def _html_to_markdown(self, element):
        """将HTML元素转换为Markdown格式文本"""
        lines = []
        for child in element.children:
            if hasattr(child, 'name'):
                if child.name in ['p', 'div', 'section']:
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(text + "\n")
                elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    level = int(child.name[1])
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(f"{'#' * level} {text}\n")
                elif child.name == 'img':
                    src = child.get('data-src') or child.get('src', '')
                    alt = child.get('alt', '图片')
                    if src:
                        lines.append(f"![{alt}]({src})\n")
                elif child.name in ['ul', 'ol']:
                    for li in child.find_all('li'):
                        text = li.get_text(strip=True)
                        if text:
                            lines.append(f"- {text}\n")
                elif child.name == 'blockquote':
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(f"> {text}\n")
                else:
                    # 递归处理其他元素
                    inner = self._html_to_markdown(child)
                    if inner.strip():
                        lines.append(inner)
            else:
                text = str(child).strip()
                if text:
                    lines.append(text + "\n")

        return "\n".join(lines)


class MPWeChatCrawler(WeChatCrawler):
    """
    方案二：通过微信公众平台后台接口爬取文章
    
    优点：可以获取公众号所有历史文章，数据完整
    缺点：需要有公众号账号并登录，需要获取cookie和token
    适用场景：需要获取完整历史文章的情况
    
    使用步骤：
    1. 登录微信公众平台 (https://mp.weixin.qq.com)
    2. 在浏览器开发者工具中获取 cookie 和 token
    3. 使用本类进行爬取
    """

    MP_BASE_URL = "https://mp.weixin.qq.com"
    SEARCH_API = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    ARTICLE_API = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    def __init__(self, cookie, token, output_dir="./output"):
        """
        初始化
        
        Args:
            cookie: 微信公众平台的cookie
            token: 微信公众平台的token（从URL参数中获取）
            output_dir: 输出目录
        """
        super().__init__(output_dir)
        self.cookie = cookie
        self.token = token
        self.session.headers.update({
            "Cookie": cookie,
            "Referer": "https://mp.weixin.qq.com/",
        })

    def search_account(self, account_name):
        """
        在公众平台搜索公众号
        
        Args:
            account_name: 公众号名称
            
        Returns:
            搜索结果列表
        """
        params = {
            "action": "search_biz",
            "begin": "0",
            "count": "5",
            "query": account_name,
            "token": self.token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
        }

        try:
            response = self.session.get(self.SEARCH_API, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("base_resp", {}).get("ret") == 0:
                return data.get("list", [])
            else:
                print(f"[错误] 搜索失败: {data.get('base_resp', {}).get('err_msg', '未知错误')}")
                return []

        except Exception as e:
            print(f"[错误] 搜索公众号失败: {e}")
            return []

    def get_articles(self, fakeid, begin=0, count=5):
        """
        获取指定公众号的文章列表
        
        Args:
            fakeid: 公众号的fakeid
            begin: 起始位置
            count: 每页数量
            
        Returns:
            文章列表
        """
        params = {
            "action": "list_ex",
            "begin": str(begin),
            "count": str(count),
            "fakeid": fakeid,
            "type": "9",
            "query": "",
            "token": self.token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
        }

        try:
            response = self.session.get(self.ARTICLE_API, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("base_resp", {}).get("ret") == 0:
                return data.get("app_msg_list", [])
            else:
                print(f"[错误] 获取文章列表失败: {data.get('base_resp', {}).get('err_msg', '未知错误')}")
                return []

        except Exception as e:
            print(f"[错误] 获取文章列表失败: {e}")
            return []

    def get_article_content(self, article_url):
        """
        获取文章正文内容
        
        Args:
            article_url: 文章URL
            
        Returns:
            文章内容
        """
        try:
            self._random_delay(1, 3)
            response = self.session.get(article_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = ""
            content = ""

            title_tag = soup.select_one("#activity-name")
            if title_tag:
                title = title_tag.get_text(strip=True)

            content_tag = soup.select_one("#js_content")
            if content_tag:
                content = self._html_to_markdown(content_tag)

            pub_time = ""
            time_tag = soup.select_one("#publish_time")
            if time_tag:
                pub_time = time_tag.get_text(strip=True)

            return {
                "title": title,
                "content": content,
                "publish_time": pub_time,
                "url": article_url,
            }

        except Exception as e:
            print(f"[错误] 获取文章内容失败: {e}")
            return None

    def _html_to_markdown(self, element):
        """将HTML元素转换为Markdown格式文本"""
        lines = []
        for child in element.children:
            if hasattr(child, 'name'):
                if child.name in ['p', 'div', 'section']:
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(text + "\n")
                elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    level = int(child.name[1])
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(f"{'#' * level} {text}\n")
                elif child.name == 'img':
                    src = child.get('data-src') or child.get('src', '')
                    alt = child.get('alt', '图片')
                    if src:
                        lines.append(f"![{alt}]({src})\n")
                elif child.name in ['ul', 'ol']:
                    for li in child.find_all('li'):
                        text = li.get_text(strip=True)
                        if text:
                            lines.append(f"- {text}\n")
                elif child.name == 'blockquote':
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(f"> {text}\n")
                else:
                    inner = self._html_to_markdown(child)
                    if inner.strip():
                        lines.append(inner)
            else:
                text = str(child).strip()
                if text:
                    lines.append(text + "\n")

        return "\n".join(lines)

    def crawl(self, account_name, max_articles=20, save=True):
        """
        爬取指定公众号的所有文章
        
        Args:
            account_name: 公众号名称
            max_articles: 最大爬取文章数
            save: 是否保存到本地
            
        Returns:
            文章列表
        """
        print(f"\n[公众平台方案] 正在搜索公众号: {account_name}")

        # 搜索公众号
        accounts = self.search_account(account_name)
        if not accounts:
            print("[错误] 未找到该公众号")
            return []

        # 使用第一个搜索结果
        target = accounts[0]
        fakeid = target.get("fakeid", "")
        print(f"  找到公众号: {target.get('nickname', '')} (ID: {fakeid})")

        # 分页获取文章
        all_articles = []
        begin = 0
        count = 5

        while len(all_articles) < max_articles:
            self._random_delay(3, 6)
            articles = self.get_articles(fakeid, begin, count)

            if not articles:
                break

            all_articles.extend(articles)
            begin += count
            print(f"  已获取 {len(all_articles)} 篇文章信息...")

        # 获取文章内容
        results = []
        for i, article in enumerate(all_articles[:max_articles]):
            title = article.get("title", "")
            url = article.get("link", "")
            print(f"  正在获取第 {i+1}/{min(len(all_articles), max_articles)} 篇: {title}")

            content_data = self.get_article_content(url)
            if content_data:
                content_data["title"] = title
                content_data["url"] = url
                content_data["publish_time"] = datetime.fromtimestamp(
                    article.get("create_time", 0)
                ).strftime("%Y-%m-%d %H:%M:%S") if article.get("create_time") else ""

                if save:
                    self._save_article(content_data, account_name)
                results.append(content_data)

            self._random_delay(3, 6)

        print(f"\n[完成] 共获取 {len(results)} 篇文章")
        return results


class DirectURLCrawler(WeChatCrawler):
    """
    方案三：直接通过微信文章URL爬取内容
    
    适用场景：已知文章URL，直接获取内容
    """

    def get_article_content(self, article_url):
        """
        获取单篇文章内容
        
        Args:
            article_url: 微信文章URL (mp.weixin.qq.com)
            
        Returns:
            文章内容字典
        """
        try:
            response = self.session.get(article_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 解析标题
            title = ""
            title_tag = soup.select_one("#activity-name")
            if title_tag:
                title = title_tag.get_text(strip=True)

            # 解析作者/公众号
            author = ""
            author_tag = soup.select_one("#js_name")
            if author_tag:
                author = author_tag.get_text(strip=True)

            # 解析发布时间
            pub_time = ""
            time_tag = soup.select_one("#publish_time")
            if time_tag:
                pub_time = time_tag.get_text(strip=True)

            # 解析正文
            content = ""
            content_tag = soup.select_one("#js_content")
            if content_tag:
                content = self._html_to_markdown(content_tag)

            return {
                "title": title,
                "author": author,
                "publish_time": pub_time,
                "content": content,
                "url": article_url,
            }

        except Exception as e:
            print(f"[错误] 获取文章内容失败: {e}")
            return None

    def _html_to_markdown(self, element):
        """将HTML元素转换为Markdown格式文本"""
        lines = []
        for child in element.children:
            if hasattr(child, 'name'):
                if child.name in ['p', 'div', 'section']:
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(text + "\n")
                elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    level = int(child.name[1])
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(f"{'#' * level} {text}\n")
                elif child.name == 'img':
                    src = child.get('data-src') or child.get('src', '')
                    alt = child.get('alt', '图片')
                    if src:
                        lines.append(f"![{alt}]({src})\n")
                elif child.name in ['ul', 'ol']:
                    for li in child.find_all('li'):
                        text = li.get_text(strip=True)
                        if text:
                            lines.append(f"- {text}\n")
                elif child.name == 'blockquote':
                    text = child.get_text(strip=True)
                    if text:
                        lines.append(f"> {text}\n")
                else:
                    inner = self._html_to_markdown(child)
                    if inner.strip():
                        lines.append(inner)
            else:
                text = str(child).strip()
                if text:
                    lines.append(text + "\n")

        return "\n".join(lines)

    def crawl_urls(self, urls, save=True, account_name="未知公众号"):
        """
        批量爬取文章URL
        
        Args:
            urls: 文章URL列表
            save: 是否保存
            account_name: 公众号名称（用于保存目录）
            
        Returns:
            文章内容列表
        """
        results = []
        for i, url in enumerate(urls):
            print(f"  正在获取第 {i+1}/{len(urls)} 篇...")
            content = self.get_article_content(url)
            if content:
                if save:
                    self._save_article(content, account_name)
                results.append(content)
            self._random_delay(2, 4)

        return results
