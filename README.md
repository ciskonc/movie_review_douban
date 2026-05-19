# Douban Movie Comments Scraper (豆瓣电影短评采集器)

一个基于 `requests` 和 `BeautifulSoup` 的轻量级网页结构化解析脚本。用于采集豆瓣电影特定条目下的用户短评数据，包含用户名、打分、评论正文及发布时间。

## 核心特性
- **容错架构**：内置 DOM 节点断言，遭遇反爬风控或 Cookie 失效时，自动保存案发现场 (`debug_page.html`) 供排查。
- **速率控制**：硬编码 3 秒请求休眠间隔，规避高频并发造成的 IP 封禁。
- **持久化输出**：支持 UTF-8 带有 BOM 格式的 CSV 自动写入，防止 Excel 预览乱码。

## 前置环境
- Python 3.7+
- `requests`
- `beautifulsoup4`
- `lxml`

安装依赖：
```bash
pip install requests beautifulsoup4 lxml
