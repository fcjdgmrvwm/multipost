import requests
import threadpool
import threading
import time


class AnalysisThread(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result = [{}]
        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}

    def run(self):
        while True:
            tasks = self.task_queue.pop()

            t1 = time.time()

            self.analysis(tasks)

            t2 = time.time()
            print(t2 - t1)

    def analysis(self, tasks):
        self.result = [{}] * len(tasks)
        pools = []
        for index, web_server in enumerate(tasks):
            pool = threadpool.ThreadPool(10)
            pools.append(pool)
            task = [[index, page_link] for page_link in web_server.page_links]
            thread_requests = threadpool.makeRequests(self.get_timestamp, task)
            [pool.putRequest(req) for req in thread_requests]
        for pool in pools:
            pool.wait()

        abnormal = self.select_majority(self.result)
        print(abnormal)

    def get_timestamp(self, task):
        response = requests.head(task[1], headers=self.head)
        self.result[task[0]][task[1]] = response.headers['Last-Modified']

    '''
    说明: 择多算法,在给定列表中选择最多的作为正常页面
    输入: 一个列表
    输出: 返回异常元素的索引集合
    '''

    @staticmethod
    def select_majority(array):
        if len(array) == 0:
            return
        hash_map = {}
        for key in array:
            key_str = str(key)
            if key_str in hash_map:
                hash_map[key_str] += 1
            else:
                hash_map[key_str] = 1

        max_value = array[0]
        max_num = 1

        for key_str in hash_map:
            if hash_map[key_str] > max_num:
                max_num = hash_map[key_str]
                max_value = key_str

        abnormal = set()
        for index, key in enumerate(array):
            if str(key) != max_value:
                abnormal.add(index)
        return abnormal


