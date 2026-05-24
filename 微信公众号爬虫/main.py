"""
微信公众号文章爬虫 - 主入口
支持多种爬取方式，可根据实际需求选择

使用方法：
  python main.py

作者：DZH123553
"""

import argparse
import sys
import json
from wechat_crawler import SogouWeChatCrawler, MPWeChatCrawler, DirectURLCrawler


def mode_sogou(args):
    """搜狗微信搜索模式"""
    crawler = SogouWeChatCrawler(output_dir=args.output)
    
    if args.search_only:
        # 仅搜索，不获取内容
        articles = crawler.get_articles_by_account(args.account, max_articles=args.max)
        print("\n搜索结果:")
        for i, article in enumerate(articles, 1):
            print(f"  {i}. {article['title']}")
            print(f"     来源: {article.get('account', '')}")
            print(f"     时间: {article.get('publish_time', '')}")
            print(f"     摘要: {article.get('summary', '')[:50]}...")
            print()
    else:
        # 搜索并获取内容
        results = crawler.crawl(args.account, max_articles=args.max, save=True)
        
        # 保存元数据
        if results:
            meta_file = f"{args.output}/metadata.json"
            meta = [{
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "publish_time": r.get("publish_time", ""),
            } for r in results]
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            print(f"\n元数据已保存到: {meta_file}")


def mode_mp(args):
    """微信公众平台模式"""
    if not args.cookie or not args.token:
        print("[错误] 使用公众平台模式需要提供 --cookie 和 --token 参数")
        print("\n获取方法:")
        print("  1. 登录 https://mp.weixin.qq.com")
        print("  2. 打开浏览器开发者工具 (F12)")
        print("  3. 在 Network 标签中找到任意请求")
        print("  4. 从请求头中复制 Cookie")
        print("  5. 从URL参数中获取 token 值")
        sys.exit(1)

    crawler = MPWeChatCrawler(
        cookie=args.cookie,
        token=args.token,
        output_dir=args.output,
    )
    results = crawler.crawl(args.account, max_articles=args.max, save=True)
    
    if results:
        meta_file = f"{args.output}/metadata.json"
        meta = [{
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "publish_time": r.get("publish_time", ""),
        } for r in results]
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        print(f"\n元数据已保存到: {meta_file}")


def mode_url(args):
    """直接URL模式"""
    if not args.urls:
        print("[错误] 请提供文章URL列表")
        print("  使用 --urls 参数，多个URL用空格分隔")
        sys.exit(1)

    crawler = DirectURLCrawler(output_dir=args.output)
    results = crawler.crawl_urls(
        args.urls,
        save=True,
        account_name=args.account or "未知公众号",
    )
    print(f"\n共获取 {len(results)} 篇文章")


def mode_selenium(args):
    """Selenium模式"""
    try:
        from wechat_crawler_selenium import SeleniumWeChatCrawler
    except ImportError:
        print("[错误] 请先安装selenium: pip install selenium webdriver-manager")
        sys.exit(1)

    crawler = SeleniumWeChatCrawler(
        output_dir=args.output,
        headless=args.headless,
    )

    try:
        results = crawler.get_article_content_by_search(
            args.account,
            max_articles=args.max,
        )
        
        if results:
            meta_file = f"{args.output}/metadata.json"
            meta = [{
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "publish_time": r.get("publish_time", ""),
            } for r in results]
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            print(f"\n元数据已保存到: {meta_file}")
    finally:
        crawler.close()


def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("  微信公众号文章爬虫")
    print("=" * 60)
    print("\n请选择爬取模式:")
    print("  1. 搜狗微信搜索（无需登录，获取最近文章）")
    print("  2. 微信公众平台接口（需要登录，获取历史文章）")
    print("  3. Selenium浏览器模式（模拟真实浏览器）")
    print("  4. 直接输入文章URL")
    print("  0. 退出")
    
    choice = input("\n请输入选项 [1-4]: ").strip()

    if choice == "0":
        print("再见！")
        return

    account_name = input("请输入公众号名称: ").strip()
    if not account_name and choice != "4":
        print("[错误] 公众号名称不能为空")
        return

    output_dir = input("请输入保存目录 [默认: ./output]: ").strip() or "./output"
    max_articles = input("请输入最大爬取数量 [默认: 10]: ").strip()
    max_articles = int(max_articles) if max_articles.isdigit() else 10

    if choice == "1":
        crawler = SogouWeChatCrawler(output_dir=output_dir)
        crawler.crawl(account_name, max_articles=max_articles)

    elif choice == "2":
        print("\n请提供微信公众平台的认证信息:")
        print("  (登录 https://mp.weixin.qq.com 后从浏览器开发者工具获取)")
        cookie = input("请输入Cookie: ").strip()
        token = input("请输入Token: ").strip()
        
        if not cookie or not token:
            print("[错误] Cookie和Token不能为空")
            return

        crawler = MPWeChatCrawler(cookie=cookie, token=token, output_dir=output_dir)
        crawler.crawl(account_name, max_articles=max_articles)

    elif choice == "3":
        try:
            from wechat_crawler_selenium import SeleniumWeChatCrawler
        except ImportError:
            print("[错误] 请先安装: pip install selenium webdriver-manager")
            return

        headless = input("是否使用无头模式？[y/N]: ").strip().lower() == "y"
        crawler = SeleniumWeChatCrawler(output_dir=output_dir, headless=headless)
        try:
            crawler.get_article_content_by_search(account_name, max_articles=max_articles)
        finally:
            crawler.close()

    elif choice == "4":
        print("请输入文章URL（每行一个，输入空行结束）:")
        urls = []
        while True:
            url = input().strip()
            if not url:
                break
            urls.append(url)

        if urls:
            crawler = DirectURLCrawler(output_dir=output_dir)
            crawler.crawl_urls(urls, save=True, account_name=account_name or "未知公众号")
        else:
            print("[错误] 未输入任何URL")

    else:
        print("[错误] 无效的选项")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="微信公众号文章爬虫 - 支持多种爬取方式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 搜狗搜索模式
  python main.py --mode sogou --account "人民日报" --max 10

  # 微信公众平台模式
  python main.py --mode mp --account "人民日报" --cookie "your_cookie" --token "your_token"

  # Selenium模式
  python main.py --mode selenium --account "人民日报" --headless

  # 直接URL模式
  python main.py --mode url --urls "https://mp.weixin.qq.com/s/xxx" "https://mp.weixin.qq.com/s/yyy"

  # 交互式模式
  python main.py
        """,
    )

    parser.add_argument("--mode", choices=["sogou", "mp", "selenium", "url", "interactive"],
                        default="interactive", help="爬取模式")
    parser.add_argument("--account", "-a", type=str, help="公众号名称")
    parser.add_argument("--max", "-m", type=int, default=10, help="最大爬取文章数 (默认: 10)")
    parser.add_argument("--output", "-o", type=str, default="./output", help="输出目录 (默认: ./output)")
    parser.add_argument("--cookie", type=str, help="微信公众平台Cookie (mp模式需要)")
    parser.add_argument("--token", type=str, help="微信公众平台Token (mp模式需要)")
    parser.add_argument("--urls", nargs="+", help="文章URL列表 (url模式需要)")
    parser.add_argument("--headless", action="store_true", help="Selenium无头模式")
    parser.add_argument("--search-only", action="store_true", help="仅搜索不获取内容")

    args = parser.parse_args()

    if args.mode == "interactive" and len(sys.argv) == 1:
        interactive_mode()
    elif args.mode == "sogou":
        if not args.account:
            print("[错误] 请提供公众号名称: --account <名称>")
            sys.exit(1)
        mode_sogou(args)
    elif args.mode == "mp":
        if not args.account:
            print("[错误] 请提供公众号名称: --account <名称>")
            sys.exit(1)
        mode_mp(args)
    elif args.mode == "selenium":
        if not args.account:
            print("[错误] 请提供公众号名称: --account <名称>")
            sys.exit(1)
        mode_selenium(args)
    elif args.mode == "url":
        mode_url(args)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
