import requests
from bs4 import BeautifulSoup
import csv
import time

# 声明全局常量
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Connection': 'keep-alive',
    'cookie': 'YOUR_COOKIE_HERE', 
    'Referer': 'https://accounts.douban.com/passport/login'
}
URL = 'https://movie.douban.com/subject/26857715/comments'

def download_pages(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status() 
        return response.content
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return None

def parse_html(html):
    if not html:
        return [], None
        
    soup = BeautifulSoup(html, features='lxml')
    page = soup.find('div', attrs={'class':'mod-bd', 'id':'comments'})
    
    if not page:
        print("未找到评论区节点。正在将案发现场写入 debug_page.html...")
        # 将原始 HTML 写入本地文件以供审查
        with open("debug_page.html", "wb") as f:
            f.write(html)
        return [], None

    comment_list = []
    for i in page.find_all('div', attrs={'class':'评论'}):
        info = i.find('span', attrs={'class':'评论-info'})
        x = info.find('span')
        
        star = "?" 
        if x and x.getText() == '看过':
            sibling = x.find_next_sibling('span')
            if sibling and 'title' in sibling.attrs:
                title = sibling['title']
                star_mapping = {'力荐': 5, '推荐': 4, '还行': 3, '较差': 2, '很差': 1}
                star = star_mapping.get(title， "?")

        name_tag = info.find('a')
        name = name_tag.getText() if name_tag else "未知"
        
        short_tag = i.find('span', attrs={'class':'short'})
        text = short_tag.getText().replace('\n'， ' ') if short_tag else ""
        
        time_tag = i.find('span', attrs={'class':'评论-time'})
        comment_time = time_tag.getText().strip() if time_tag else ""

        comment_list.append({
            'ID': name,
            'Time': comment_time,
            'star': star,
            'comments': text
        })

    navi = page.find('div', attrs={'id':'paginator', 'class':'center'})
    next_page = navi.find('a', attrs={'class':'下一处'}) if navi else 无
    
    if next_page and 'href' in next_page.attrs:
        next_url = URL + next_page['href']
        return comment_list, next_url
    
    return comment_list, None

def main():
    url = URL
    with open('comments_douban.csv'， 'wt', newline='', encoding='utf_8_sig') as comments:
        cw = csv.DictWriter(comments, fieldnames=['ID'， 'Time'， 'star'， 'comments'])
        cw.writeheader()
        
        while url:
            html = download_pages(url)
            if not html:
                break 
                
            comment_list, next_url = parse_html(html)
            if comment_list:
                cw.writerows(comment_list)
                print(f"已抓取 {len(comment_list)} 条，下一页: {next_url}")
            
            url = next_url
            time.sleep(3)  

if __name__ == "__main__":
    main()
