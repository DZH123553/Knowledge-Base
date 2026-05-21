# Web Content Extractor

从任意网页提取干净、可读的 Markdown 内容。支持多种转换服务 + 爬虫兜底，覆盖绝大多数网站。

## 触发条件

当用户要求以下操作时触发本 skill：
- "读取网页内容" / "提取网页内容" / "网页转 markdown"
- "抓取 URL" / "获取页面内容"
- 用户提供 URL 并要求总结、分析、提取信息

## 提取策略（按优先级）

### 方法 1: markdown.new（推荐，Cloudflare 站点首选）

在目标 URL 前加上 `https://markdown.new/`，即可获取该页面的 Markdown 版本。

**适用场景**: 使用 Cloudflare 的网站（大多数现代站点）

**示例**:
```
原始 URL:    https://example.com/article
转换 URL:    https://markdown.new/https://example.com/article
```

### 方法 2: defuddle.md（备选）

在目标 URL 前加上 `https://defuddle.md/`，获取 Markdown 版本。

**适用场景**: 方法 1 失败时尝试

**示例**:
```
原始 URL:    https://example.com/article
转换 URL:    https://defuddle.md/https://example.com/article
```

### 方法 3: r.jina.ai（通用备选）

在目标 URL 前加上 `https://r.jina.ai/`，获取 Markdown 版本。

**适用场景**: 通用 fallback，对新闻站、博客支持良好

**示例**:
```
原始 URL:    https://example.com/article
转换 URL:    https://r.jina.ai/https://example.com/article
```

### 方法 4: Scrapling 爬虫（最终兜底）

当以上三种服务都无法提取内容时，使用 Scrapling 爬虫工具直接抓取页面。

**安装**:
```bash
pip install scrapling
```

**使用示例**:
```python
from scrapling import Fetcher

fetcher = Fetcher()
page = fetcher.get("https://example.com/article")

# 提取主要内容（自动过滤导航/广告）
content = page.get_by_text_around(
    tag="article",
    max_depth=3
)
print(content.text)

# 或提取整个页面的 markdown
print(page.markdown)
```

## 完整工作流

```
给定 URL
  ↓
尝试 markdown.new/{URL}
  ↓ 成功？
是 → 返回 Markdown
否 → 尝试 defuddle.md/{URL}
       ↓ 成功？
     是 → 返回 Markdown
     否 → 尝试 r.jina.ai/{URL}
            ↓ 成功？
          是 → 返回 Markdown
          否 → 使用 Scrapling 爬虫
                 ↓
               返回 Markdown / 纯文本
```

## 使用规范

1. **优先使用服务，少用爬虫**
   - 三个 markdown 服务通常比直接爬虫更稳定、更快
   - 爬虫作为兜底，避免被反爬

2. **验证内容完整性**
   - 提取后检查内容是否为空或只有导航栏
   - 如果内容明显不完整，换下一个方法重试

3. **处理相对链接**
   - 提取的 Markdown 中的相对链接可能需要补全为绝对链接
   - 使用原始 URL 的 domain 进行补全

4. **异常处理**
   - 429/403 错误：切换下一个服务或等待后重试
   - 超时：直接尝试 Scrapling
   - 内容为空：尝试添加 `?output=text` 或 `?format=md` 参数

## 示例：完整提取脚本

```python
import requests
from urllib.parse import quote

def extract_web_content(url: str) -> str:
    """
    从网页提取 Markdown 内容，依次尝试多种服务。
    """
    services = [
        f"https://markdown.new/{url}",
        f"https://defuddle.md/{url}",
        f"https://r.jina.ai/{url}",
    ]
    
    for service_url in services:
        try:
            resp = requests.get(service_url, timeout=30, headers={
                "User-Agent": "Mozilla/5.0 (compatible; WebContentBot/1.0)"
            })
            if resp.status_code == 200 and len(resp.text) > 200:
                return resp.text
        except Exception:
            continue
    
    # 兜底：Scrapling
    try:
        from scrapling import Fetcher
        fetcher = Fetcher()
        page = fetcher.get(url)
        return page.markdown
    except Exception as e:
        return f"[提取失败] {e}"

# 使用
content = extract_web_content("https://example.com/article")
print(content)
```

## 注意事项

- `markdown.new` 和 `defuddle.md` 本质是 Cloudflare Workers，对 Cloudflare 保护的站点效果最佳
- `r.jina.ai` 由 Jina AI 提供，对中文内容支持良好
- Scrapling 基于 Playwright，首次运行会自动安装浏览器，需要本地有 Chrome/Edge/Chromium
- 对于需要登录的页面，Scrapling 支持 cookie/session 传递，但三个服务无法处理登录态页面
