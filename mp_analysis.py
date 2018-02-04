import requests
import locallib.threadpool as threadpool
import threading
import time

class AnalysisThread(threading.Thread):
    def __init__(self, task_queue, socket_client):
        super().__init__()
        self.task_queue = task_queue
        self.socket_client = socket_client
        self.result = [{}]
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        self.pool = threadpool.ThreadPool(10)

    def run(self):
        while True:
            tasks = self.task_queue.pop()

            t1 = time.time()

            abnormal = self.analysis(tasks)

            self.exception_handling(tasks, abnormal)

            # print(abnormal)
            t2 = time.time()
            print("analysis time use:",t2 - t1)

    def analysis(self, tasks):
        self.result=[{} for i in range(len(tasks))] # 4 pointer, 4 dict.
        #self.result = [{}] * len(tasks) this will cause error, since 4 pointer, 1 dict.
        page = ""
        for index, web_server in enumerate(tasks):
            page = web_server.sub_url
            task = [[index, page_link] for page_link in web_server.page_links]
            thread_requests = threadpool.makeRequests(self.get_timestamp, task)
            [self.pool.putRequest(req) for req in thread_requests]

        self.pool.wait()

        abnormal = self.select_majority(self.result)
        print("for page", page, ":", end=" ")
        if len(abnormal) == 0:
            print("normal", end=" ")
        else:
            print("abnormal:", end=" ")
        for i in abnormal:
            print(tasks[i].name,",",end=" ")
        return abnormal

    '''
    说明: 异常处理函数,将异常页面的主机名称发送给控制器,进行下线自清洗
    输入: 当前所有的服务器结构体列表,异常主机集合
    输出: 
    '''
    def exception_handling(self, tasks, abnormal):
        for index in abnormal:
            self.socket_client.send_cmd(tasks[index].name)
        self.socket_client.send_cmd("None")

    def get_timestamp(self, task):
        response = requests.head(task[1], headers=self.head)
        num = len('http://127.0.0.1:8080')
        #7 http:// 8 https://
        idx = task[1].find('/',10)
        relative_path = task[1][idx:]
        if 'Last-Modified' in response.headers:
            self.result[task[0]][relative_path] = response.headers['Last-Modified']
        else:
            # for sake of corruption
            print("No Last-Modified", task[1])
            self.result[task[0]][relative_path] = "0"

    '''
    说明: 择多算法,在给定列表中选择最多的作为正常页面
    输入: 一个列表
    输出: 返回异常元素的索引集合
    '''
    @staticmethod
    def select_majority(array):
        if len(array) == 0:
            return
        vote = {}
        # collect vote result
        for index, zhixing in enumerate(array):
            for url in zhixing:
                if url not in vote:
                    vote[url] = {}
                if zhixing[url] not in vote[url]:
                    vote[url][zhixing[url]] = [index]
                else:
                    vote[url][zhixing[url]].append(index)
        abnormal = set()
        # start analysis
        zxnum = len(array)
        for url in vote:
            for ts in vote[url]:
                if len(vote[url][ts]) < zxnum/2:
                    for i in vote[url][ts]:
                        abnormal.add(i)
                    print("encounter abnormal due to page",url)

        return abnormal

    # def select_majority(array):
    #     if len(array) == 0:
    #         return
    #     hash_map = {}
    #     key_strs = []
    #     for key in array:
    #         key_strs.append(str([(k,key[k]) for k in sorted(key.keys())]))
    #
    #     for key_str in key_strs:
    #         if key_str in hash_map:
    #             hash_map[key_str] += 1
    #         else:
    #             hash_map[key_str] = 1
    #
    #     max_value = str(array[0])
    #     max_num = 1
    #
    #     for key_str in hash_map:
    #         if hash_map[key_str] > max_num:
    #             max_num = hash_map[key_str]
    #             max_value = key_str
    #
    #     abnormal = set()
    #     for index, key_str in enumerate(key_strs):
    #         if key_str != max_value:
    #             abnormal.add(index)
    #     return abnormal
