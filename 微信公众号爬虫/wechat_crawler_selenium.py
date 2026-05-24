"""
微信公众号文章爬虫 - Selenium增强版
使用Selenium模拟浏览器操作，绕过反爬机制

功能：
  1. 通过搜狗微信搜索，使用Selenium模拟浏览器获取文章
  2. 自动处理验证码页面（需要手动输入验证码）
  3. 支持翻页获取更多文章

依赖：
  pip install selenium webdriver-manager beautifulsoup4

作者：DZH123553
"""

import os
import re
import time
import json
import random
from datetime import datetime
from bs4 import BeautifulSoup

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("[警告] 未安装selenium，请运行: pip install selenium webdriver-manager")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False


class SeleniumWeChatCrawler:
    """
    使用Selenium的微信公众号爬虫
    
    通过搜狗微信搜索，使用真实浏览器获取文章内容，
    能够更好地处理JavaScript渲染和反爬机制。
    """

    SOGOU_SEARCH_URL = "https://weixin.sogou.com/weixin"

    def __init__(self, output_dir="./output", headless=False):
        """
        初始化Selenium爬虫
        
        Args:
            output_dir: 文章保存目录
            headless: 是否使用无头模式（不显示浏览器窗口）
        """
        if not SELENIUM_AVAILABLE:
            raise ImportError("请先安装selenium: pip install selenium webdriver-manager")

        self.output_dir = output_dir
        self.headless = headless
        self.driver = None
        os.makedirs(output_dir, exist_ok=True)

    def _init_driver(self):
        """初始化Chrome WebDriver"""
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 防止被检测为自动化
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        try:
            if WEBDRIVER_MANAGER_AVAILABLE:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"[错误] 初始化Chrome驱动失败: {e}")
            print("请确保已安装Chrome浏览器和对应版本的ChromeDriver")
            raise

        # 执行CDP命令隐藏自动化特征
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.navigator.chrome = {runtime: {}};
            """
        })

    def _random_delay(self, min_sec=2, max_sec=5):
        """随机延时"""
        time.sleep(random.uniform(min_sec, max_sec))

    def search_articles(self, account_name, max_pages=3):
        """
        通过搜狗微信搜索文章
        
        Args:
            account_name: 公众号名称
            max_pages: 最大搜索页数
            
        Returns:
            文章信息列表
        """
        if not self.driver:
            self._init_driver()

        print(f"\n[Selenium方案] 正在搜索公众号文章: {account_name}")
        articles = []

        try:
            # 访问搜狗微信搜索
            search_url = f"{self.SOGOU_SEARCH_URL}?type=2&query={account_name}&ie=utf8"
            self.driver.get(search_url)
            self._random_delay(2, 4)

            for page in range(max_pages):
                print(f"  正在解析第 {page + 1} 页...")
                
                # 检查是否需要验证码
                if self._check_captcha():
                    print("  [提示] 检测到验证码，请在浏览器中手动完成验证...")
                    input("  按回车键继续...")
                    self._random_delay(1, 2)

                # 解析当前页面
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                items = soup.select("div.txt-box")

                for item in items:
                    title_tag = item.select_one("h3 a")
                    if not title_tag:
                        continue

                    title = title_tag.get_text(strip=True)
                    
                    # 获取来源
                    source_tag = item.select_one("div.s-p a")
                    source = source_tag.get_text(strip=True) if source_tag else ""

                    # 获取摘要
                    summary_tag = item.select_one("p.txt-info")
                    summary = summary_tag.get_text(strip=True) if summary_tag else ""

                    # 获取时间
                    time_tag = item.select_one("div.s-p span.s2")
                    pub_time = time_tag.get_text(strip=True) if time_tag else ""

                    articles.append({
                        "title": title,
                        "source": source,
                        "summary": summary,
                        "publish_time": pub_time,
                    })

                # 尝试翻页
                if page < max_pages - 1:
                    try:
                        next_btn = self.driver.find_element(By.ID, "sogou_next")
                        next_btn.click()
                        self._random_delay(3, 6)
                    except (NoSuchElementException, Exception):
                        print("  没有更多页面了")
                        break

        except Exception as e:
            print(f"[错误] 搜索文章失败: {e}")

        print(f"  共找到 {len(articles)} 篇文章")
        return articles

    def get_article_content_by_search(self, account_name, max_articles=10):
        """
        搜索并获取文章内容
        
        Args:
            account_name: 公众号名称
            max_articles: 最大获取文章数
            
        Returns:
            文章内容列表
        """
        if not self.driver:
            self._init_driver()

        print(f"\n[Selenium方案] 正在获取公众号文章内容: {account_name}")
        results = []

        try:
            # 搜索文章
            search_url = f"{self.SOGOU_SEARCH_URL}?type=2&query={account_name}&ie=utf8"
            self.driver.get(search_url)
            self._random_delay(2, 4)

            # 检查验证码
            if self._check_captcha():
                print("  [提示] 检测到验证码，请在浏览器中手动完成验证...")
                input("  按回车键继续...")

            # 获取文章链接
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            article_links = []
            
            items = soup.select("div.txt-box h3 a")
            for item in items[:max_articles]:
                href = item.get("href", "")
                if href:
                    if not href.startswith("http"):
                        href = "https://weixin.sogou.com" + href
                    article_links.append({
                        "title": item.get_text(strip=True),
                        "url": href,
                    })

            # 逐个获取文章内容
            for i, link in enumerate(article_links):
                print(f"  正在获取第 {i+1}/{len(article_links)} 篇: {link['title']}")
                
                try:
                    self.driver.get(link["url"])
                    self._random_delay(2, 4)

                    # 等待页面加载
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    
                    # 解析文章内容
                    title = ""
                    title_tag = soup.select_one("#activity-name")
                    if title_tag:
                        title = title_tag.get_text(strip=True)
                    else:
                        title = link["title"]

                    content = ""
                    content_tag = soup.select_one("#js_content")
                    if content_tag:
                        content = self._html_to_markdown(content_tag)

                    pub_time = ""
                    time_tag = soup.select_one("#publish_time")
                    if time_tag:
                        pub_time = time_tag.get_text(strip=True)

                    author = ""
                    author_tag = soup.select_one("#js_name")
                    if author_tag:
                        author = author_tag.get_text(strip=True)

                    article_data = {
                        "title": title,
                        "content": content,
                        "publish_time": pub_time,
                        "author": author,
                        "url": link["url"],
                    }

                    self._save_article(article_data, account_name)
                    results.append(article_data)

                except Exception as e:
                    print(f"    获取失败: {e}")
                    continue

                self._random_delay(3, 6)

        except Exception as e:
            print(f"[错误] 获取文章内容失败: {e}")

        print(f"\n[完成] 共获取 {len(results)} 篇文章内容")
        return results

    def _check_captcha(self):
        """检查是否出现验证码"""
        try:
            page_source = self.driver.page_source
            if "请输入验证码" in page_source or "antispider" in page_source:
                return True
            return False
        except:
            return False

    def _save_article(self, article, account_name):
        """保存文章到本地"""
        account_dir = os.path.join(self.output_dir, self._sanitize_filename(account_name))
        os.makedirs(account_dir, exist_ok=True)

        title = self._sanitize_filename(article.get("title", "untitled"))
        filename = f"{title}.md"
        filepath = os.path.join(account_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {article.get('title', '')}\n\n")
            f.write(f"**公众号**: {account_name}\n\n")
            f.write(f"**作者**: {article.get('author', '')}\n\n")
            f.write(f"**发布时间**: {article.get('publish_time', '未知')}\n\n")
            f.write(f"**原文链接**: {article.get('url', '')}\n\n")
            f.write("---\n\n")
            f.write(article.get("content", ""))

        print(f"    [已保存] {filepath}")
        return filepath

    def _html_to_markdown(self, element):
        """将HTML元素转换为Markdown格式"""
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

    @staticmethod
    def _sanitize_filename(name):
        """清理文件名"""
        return re.sub(r'[\\/*?:"<>|]', "_", name).strip()[:100]

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __del__(self):
        """析构时关闭浏览器"""
        self.close()
