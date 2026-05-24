# 微信公众号爬虫

一个功能完善的微信公众号文章爬虫工具，支持根据公众号名称自动爬取文章内容，并保存为 Markdown 格式。

## 功能特点

- **多种爬取方式**：支持搜狗微信搜索、微信公众平台接口、Selenium 浏览器模拟、直接 URL 爬取
- **智能解析**：自动解析文章标题、正文、发布时间、作者等信息
- **Markdown 输出**：文章内容自动转换为 Markdown 格式保存
- **反爬处理**：内置随机延时、User-Agent 伪装等反爬策略
- **交互式界面**：支持命令行参数和交互式两种使用方式

## 爬取方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 搜狗微信搜索 | 无需登录，操作简单 | 仅能获取最近约10篇文章 | 快速获取最新文章 |
| 微信公众平台接口 | 可获取所有历史文章 | 需要登录公众号后台 | 完整数据采集 |
| Selenium 浏览器 | 模拟真实浏览器，反爬能力强 | 速度较慢，需要安装Chrome | 搜狗被封时使用 |
| 直接 URL 爬取 | 精确获取指定文章 | 需要已知文章链接 | 定向采集 |

## 安装

### 环境要求

- Python 3.7+
- Chrome 浏览器（Selenium 模式需要）

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 交互式模式

```bash
python main.py
```

运行后按照提示选择爬取模式和输入参数即可。

### 命令行模式

#### 1. 搜狗微信搜索模式

```bash
# 爬取公众号最近文章
python main.py --mode sogou --account "公众号名称" --max 10

# 仅搜索不获取内容
python main.py --mode sogou --account "公众号名称" --search-only
```

#### 2. 微信公众平台模式

```bash
python main.py --mode mp --account "公众号名称" --cookie "your_cookie" --token "your_token" --max 20
```

**获取 Cookie 和 Token 的方法：**

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 按 F12 打开浏览器开发者工具
3. 切换到 Network 标签
4. 在页面上进行任意操作（如点击"素材管理"）
5. 从请求头中复制 Cookie 值
6. 从 URL 参数中获取 token 值（如 `&token=123456`）

#### 3. Selenium 浏览器模式

```bash
# 有界面模式
python main.py --mode selenium --account "公众号名称" --max 10

# 无头模式（不显示浏览器窗口）
python main.py --mode selenium --account "公众号名称" --headless
```

#### 4. 直接 URL 模式

```bash
python main.py --mode url --urls "https://mp.weixin.qq.com/s/xxx" "https://mp.weixin.qq.com/s/yyy" --account "公众号名称"
```

### 在代码中使用

```python
from wechat_crawler import SogouWeChatCrawler, MPWeChatCrawler, DirectURLCrawler

# 方式1：搜狗搜索
crawler = SogouWeChatCrawler(output_dir="./output")
articles = crawler.crawl("人民日报", max_articles=5)

# 方式2：公众平台接口
crawler = MPWeChatCrawler(
    cookie="your_cookie_here",
    token="your_token_here",
    output_dir="./output"
)
articles = crawler.crawl("人民日报", max_articles=20)

# 方式3：直接URL
crawler = DirectURLCrawler(output_dir="./output")
articles = crawler.crawl_urls(
    ["https://mp.weixin.qq.com/s/xxx"],
    account_name="人民日报"
)

# 方式4：Selenium（需要额外安装）
from wechat_crawler_selenium import SeleniumWeChatCrawler
crawler = SeleniumWeChatCrawler(output_dir="./output", headless=True)
articles = crawler.get_article_content_by_search("人民日报", max_articles=5)
crawler.close()
```

## 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | 爬取模式：sogou/mp/selenium/url/interactive | interactive |
| `--account, -a` | 公众号名称 | - |
| `--max, -m` | 最大爬取文章数 | 10 |
| `--output, -o` | 输出目录 | ./output |
| `--cookie` | 微信公众平台Cookie | - |
| `--token` | 微信公众平台Token | - |
| `--urls` | 文章URL列表 | - |
| `--headless` | Selenium无头模式 | False |
| `--search-only` | 仅搜索不获取内容 | False |

## 输出格式

爬取的文章将保存为 Markdown 文件，目录结构如下：

```
output/
├── 公众号名称/
│   ├── 文章标题1.md
│   ├── 文章标题2.md
│   └── ...
└── metadata.json
```

每篇文章的 Markdown 文件包含：

- 文章标题
- 公众号名称
- 发布时间
- 原文链接
- 正文内容（含图片链接）

## 注意事项

1. **合理使用**：请遵守相关法律法规，合理使用爬虫工具，不要过于频繁地请求
2. **反爬机制**：搜狗微信搜索有反爬机制，频繁请求可能触发验证码
3. **Cookie 有效期**：微信公众平台的 Cookie 有效期有限，过期需要重新获取
4. **延时设置**：建议保持默认的随机延时设置，避免被封禁
5. **代理使用**：如果 IP 被封，可以在 `config.py` 中配置代理

## 常见问题

**Q: 搜狗搜索返回空结果？**
A: 可能是触发了反爬机制，建议等待一段时间后重试，或使用 Selenium 模式。

**Q: 微信公众平台模式提示认证失败？**
A: Cookie 或 Token 可能已过期，请重新登录获取。

**Q: Selenium 模式启动失败？**
A: 请确保已安装 Chrome 浏览器，并安装了对应版本的 ChromeDriver。使用 `webdriver-manager` 可以自动管理驱动版本。

**Q: 文章内容为空？**
A: 部分文章可能需要在微信客户端中查看，网页版无法访问完整内容。

## 项目结构

```
微信公众号爬虫/
├── main.py                    # 主入口文件
├── wechat_crawler.py          # 核心爬虫模块
├── wechat_crawler_selenium.py # Selenium增强版
├── config.py                  # 配置文件
├── requirements.txt           # 依赖列表
├── README.md                  # 说明文档
└── output/                    # 默认输出目录
```

## License

MIT License

## 免责声明

本工具仅供学习和研究使用，请勿用于任何商业用途或违法行为。使用本工具所产生的一切后果由使用者自行承担。请尊重微信公众号作者的知识产权，合理使用爬取的内容。
