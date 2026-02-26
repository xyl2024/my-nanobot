#!/usr/bin/env python3
"""
GitHub Trending 爬虫脚本
获取 GitHub 每日/每周/每月的热门项目
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError
from html import unescape

# GitHub Trending URL
BASE_URL = "https://github.com/trending"

# 支持的时间范围
SINCE_OPTIONS = {
    "daily": "daily",
    "weekly": "weekly", 
    "monthly": "monthly"
}

# 请求头，模拟浏览器
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def build_url(language: str = None, since: str = "daily") -> str:
    """构建 GitHub Trending URL"""
    url = BASE_URL
    params = []
    
    if since in SINCE_OPTIONS:
        params.append(f"since={SINCE_OPTIONS[since]}")
    if language:
        # URL 编码语言名称
        lang = language.lower().strip()
        # 处理语言名称中的空格
        lang = lang.replace(" ", "%20")
        url = f"{url}/{lang}"
    
    if params:
        url += "?" + "&".join(params)
    
    return url


def fetch_page(url: str) -> str:
    """获取网页内容"""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8")
    except URLError as e:
        print(f"❌ 获取页面失败: {e}", file=sys.stderr)
        sys.exit(1)


def parse_trending(html: str) -> list:
    """解析 HTML 获取 Trending 项目列表"""
    projects = []
    
    # 匹配每个仓库条目
    # GitHub Trending 页面结构
    article_pattern = r'<article class="Box-row">(.*?)</article>'
    articles = re.findall(article_pattern, html, re.DOTALL)
    
    for article in articles:
        try:
            # 获取仓库名和链接
            repo_pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
            repo_match = re.search(repo_pattern, article)
            if not repo_match:
                continue
            
            repo_path = repo_match.group(1).strip()
            repo_name = repo_match.group(2).strip()
            
            # 获取描述
            desc_pattern = r'<p[^>]*class="[^"]*color-fg-muted[^"]*"[^>]*>([^<]+)</p>'
            desc_match = re.search(desc_pattern, article)
            description = ""
            if desc_match:
                description = unescape(desc_match.group(1).strip())
            
            # 获取语言
            lang_pattern = r'<span[^>]*class="[^"]*color-fg-[^"]*"[^>]*>[^<]*</span>\s*<span[^>]*>([^<]+)</span>'
            lang_match = re.search(lang_pattern, article)
            language = lang_match.group(1).strip() if lang_match else "Unknown"
            
            # 获取 stars 数
            stars_pattern = r'aria-label="(\d+(?:\.\d+)?[kK]?) stars"'
            stars_match = re.search(stars_pattern, article)
            stars = stars_match.group(1) if stars_match else "0"
            
            # 获取今日新增 stars
            today_stars_pattern = r'(\d+(?:\.\d+)?[kK]?)\s*stars today'
            today_match = re.search(today_stars_pattern, article, re.IGNORECASE)
            stars_today = today_match.group(1) if today_match else "0"
            
            # 构建项目信息
            project = {
                "name": repo_name,
                "path": repo_path,
                "url": f"https://github.com{repo_path}",
                "description": description,
                "language": language,
                "stars": stars,
                "stars_today": stars_today
            }
            projects.append(project)
            
        except Exception as e:
            # 跳过解析错误的条目
            continue
    
    return projects


def format_output(projects: list, language: str = None, since: str = "daily") -> str:
    """格式化输出"""
    if not projects:
        return "⚠️ 未能获取到Trending数据，请稍后重试"
    
    # 语言显示
    lang_display = f" - {language}" if language else ""
    
    # 时间范围显示
    since_display = {
        "daily": "今日",
        "weekly": "本周", 
        "monthly": "本月"
    }.get(since, "今日")
    
    output = []
    output.append(f"🔥 GitHub Trending {since_display}{lang_display}")
    output.append("=" * 50)
    output.append("")
    
    for i, p in enumerate(projects[:25], 1):  # 限制显示25个
        output.append(f"{i}. {p['name']}")
        output.append(f"   ⭐ {p['stars']} stars | +{p['stars_today']} today")
        if p['description']:
            # 限制描述长度
            desc = p['description'][:80] + "..." if len(p['description']) > 80 else p['description']
            output.append(f"   📝 {desc}")
        output.append(f"   🔗 {p['url']}")
        output.append(f"   🖥️ {p['language']}")
        output.append("")
    
    output.append("=" * 50)
    output.append(f"共 {len(projects)} 个项目")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="获取 GitHub Trending 热门项目")
    parser.add_argument(
        "--daily", 
        action="store_true", 
        help="获取今日热门（默认）"
    )
    parser.add_argument(
        "--weekly", 
        action="store_true", 
        help="获取本周热门"
    )
    parser.add_argument(
        "--monthly", 
        action="store_true", 
        help="获取本月热门"
    )
    parser.add_argument(
        "--language", 
        "-l",
        type=str,
        help="指定编程语言（如 python, javascript, go, rust）"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 格式"
    )
    
    args = parser.parse_args()
    
    # 确定时间范围
    if args.monthly:
        since = "monthly"
    elif args.weekly:
        since = "weekly"
    else:
        since = "daily"
    
    language = args.language
    
    # 构建 URL
    url = build_url(language, since)
    
    print(f"📡 正在获取 GitHub Trending ({since})...", file=sys.stderr)
    if language:
        print(f"   语言: {language}", file=sys.stderr)
    
    # 获取页面
    html = fetch_page(url)
    
    # 解析
    projects = parse_trending(html)
    
    # 输出
    if args.json:
        print(json.dumps(projects, ensure_ascii=False, indent=2))
    else:
        print(format_output(projects, language, since))


if __name__ == "__main__":
    main()
