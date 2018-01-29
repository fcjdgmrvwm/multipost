import requests
import re

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 '
                  'Safari/537.36 SE 2.X MetaSr 1.0'}
base_url = 'http://192.168.0.133/'
sub_urls = set(['/'])

def CollectPage():
    pass


'''
说明: 提取页面中的链接，并将外部链接过滤去除
输入: http的response报文
输出: 经过提取的相对url列表
'''

def extract_link(html):
    matchs = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')|"
                        r"(?<=src=\").+?(?=\")|(?<=src=\').+?(?=\')", html.text)
    matchs = [match for match in matchs if match[:4] != "http"]

    for link in matchs:
        print(link)
    return matchs

'''
说明: 更新全站URL目录结构,将每次爬取获得的新URL加入到已有的集合当中
输入: 此次爬取获得的新URL列表
输出:  
'''

def update_sitemap(cur_sub_urls):
    for sub_url in cur_sub_urls:
        sub_urls.add(sub_url)



html = requests.get(base_url, headers=head)
print(html.headers)
if html.status_code == 200:
    print("yeah!")
else:
    print("fuck!")

cur_sub_urls = extract_link(html)
update_sitemap(cur_sub_urls)

print(sub_urls.__len__())


