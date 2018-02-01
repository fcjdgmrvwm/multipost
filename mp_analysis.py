import requests
import threadpool
import threading


class AnalysisThread(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue

        self.head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}

    def run(self):
        while True:
            task = self.task_queue.pop()
            print(task)
            a = []
            for e in task:
                a.append(e.page_links)
                print(e.name, e.host, e.sub_url, e.page_links)
            print(a[0] == a[1])


