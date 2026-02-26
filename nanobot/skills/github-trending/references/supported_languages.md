# 支持的编程语言列表

GitHub Trending 支持以下主要编程语言筛选：

## 热门语言

| 语言 | URL 参数 | 说明 |
|------|----------|------|
| Python | python | 最流行的语言之一 |
| JavaScript | javascript | Web 开发主流语言 |
| TypeScript | typescript | JavaScript 超集 |
| Go | go | Google 开发的高效语言 |
| Rust | rust | 系统编程语言 |
| Java | java | 企业级应用 |
| C++ | c++ | 系统级开发 |
| C# | csharp | .NET 生态 |
| Ruby | ruby | Web 开发 |
| PHP | php | 服务端脚本 |

## 其他支持的语言

- Swift - iOS/macOS 开发
- Kotlin - Android 开发
- Scala - 函数式编程
- R - 统计分析
- MATLAB - 数值计算
- Shell - 脚本编程
- Vue - 前端框架
- Objective-C - iOS 开发
- Perl - 脚本语言
- Haskell - 函数式编程
- Lua - 嵌入式脚本
- Dart - Flutter 开发
- Elixir - 函数式编程
- Clojure - Lisp 方言

## 使用示例

```bash
# Python 本周趋势
python3 fetch_trending.py --weekly --language python

# JavaScript 今日趋势
python3 fetch_trending.py --daily --language javascript

# Go 语言本月趋势
python3 fetch_trending.py --monthly --language go

# 所有语言（不筛选）
python3 fetch_trending.py --daily
```

## 注意事项

1. 语言名称大小写不敏感
2. 部分语言需要使用特定参数名（如 C# 使用 `csharp`）
3. 如果某语言当日无数据，可能不会显示
