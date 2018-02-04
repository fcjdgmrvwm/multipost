import requests
import re
import locallib.threadpool as threadpool
import threading
import time

from mp_utils import check_url
from mp_sampler import sampler

'''
Web服务器结构体:{
    name:名称
    host:主机地址
    sub_url:当前扫描网页的后缀URL
    page_links:当前扫描网页中的所有链接
}
'''
class WebServer(object):
    def __init__(self, name, host):
        self.name = name
        self.host = host
        self.sub_url = '/'
        self.page_links = []

    def get_name(self):
        return self.name

    def get_host(self):
        return self.host

    def set_sub_url(self, sub_url):
        self.sub_url = sub_url

    def get_sub_url(self):
        return self.sub_url

    def set_page_links(self, page_links):
        self.page_links = page_links

    def get_page_links(self):
        return self.page_links


class ScanThread(threading.Thread):
    def __init__(self, task_queue, hosts):
        super().__init__()
        self.task_queue = task_queue
        self.tasks = []
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}
        self.web_servers = [WebServer(i, hosts[i]) for i in hosts]
        self.sub_urls = {'/'}
        self.sub_urls_cnt = {}

    def run(self):
        pool = threadpool.ThreadPool(10)
        selected_sub_url = "/"
        while True:
            self.tasks = []
            self.sub_urls_cnt = {}
            # print("selected sub_url: ",selected_sub_url)
            for web_server in self.web_servers:
                web_server.set_sub_url(selected_sub_url)
            selected_sub_url = self.select_sub_url(self.sub_urls)
            thread_requests = threadpool.makeRequests(self.scan, self.web_servers)
            [pool.putRequest(req) for req in thread_requests]
            pool.wait()
            self.task_queue.push(self.tasks)

            # update sub_urls using sub_urls_cnt
            nump = len(self.web_servers)
            for surl in self.sub_urls_cnt:
                if self.sub_urls_cnt[surl] > nump/2:
                    sufidx = surl.rfind('.')
                    suffix = surl[sufidx:]
                    mime = [".html",".htm"] # ,".css", ".js"
                    if sufidx == -1 or suffix in mime:
                        self.sub_urls.add(surl)
            # print(self.sub_urls)
            time.sleep(5)

    def scan(self, web_server):
        root_path = web_server.get_host()
        if root_path[-1] == '/':
            root_path = root_path[0: -1]
        sub_url = web_server.get_sub_url()
        if sub_url[0] == '/':
            start_url = root_path + sub_url
        else:
            print("Error Handling of sub urls")
            start_url = root_path + "/" + sub_url
        page = requests.get(start_url, headers=self.head)
        cur_sub_urls = self.extract_link(page)
        ncur_sub_urls = []
        page_links = []
        for cur_sub_url in cur_sub_urls:
            vurl = check_url(cur_sub_url, start_url)
            if len(vurl) == 0:
                continue
            ncur_sub_urls.append(vurl)
            page_links.append(root_path + vurl)

        page_links.append(start_url)
        self.update_sitemap(ncur_sub_urls)

        web_server.set_page_links(page_links)
        self.tasks.append(web_server)

    '''
    说明: 选择当前扫描的子目录,重点关注首页,其他页面随机抽取
    输入: 当前的所有子URL列表
    输出: 经过提取的一个URL
    '''
    @staticmethod
    def select_sub_url(sub_urls):
        return sampler.basic_sampler(sub_urls)

    '''
    说明: 提取页面中的链接,并将外部链接过滤去除
    输入: http的response报文
    输出: 经过提取的相对url列表
    '''
    @staticmethod
    def extract_link(page):
        matchs = re.findall(r"(?<= href=\").+?(?=\")|(?<=href=\').+?(?=\')|"
                            r"(?<= src=\").+?(?=\")|(?<=src=\').+?(?=\')", page.text)
        matchs = [match for match in matchs if match[:4] != "http"]
        return matchs

    '''
    说明: 更新全站URL目录结构,将每次爬取获得的新URL加入到已有的集合当中
    输入: 此次爬取获得的新URL列表
    输出: 无
    '''
    def update_sitemap(self, cur_sub_urls):
        for sub_url in cur_sub_urls:
            if sub_url in self.sub_urls_cnt:
                self.sub_urls_cnt[sub_url] += 1
            else:
                self.sub_urls_cnt[sub_url] = 1