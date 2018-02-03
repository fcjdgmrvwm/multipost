import queue

#SERVER_HOSTS = {'VmwareUbuntu': 'http://192.168.0.133/', 'VmwareWin7': 'http://192.168.0.133/', }

SERVER_HOSTS={'1':'http://127.0.0.1:8080',
'2':'http://127.0.0.1:8081',
'3':'http://127.0.0.1:8082',
'4':'http://127.0.0.1:8083',
'5':'http://127.0.0.1:8084'
}


CONTROLLER_HOST = '127.0.0.1'
CONTROLLER_PORT = 12345



class TaskQueue:
    def __init__(self):
        self.queues = queue.Queue()

    def push(self, task):
        self.queues.put(task)

    def pop(self):
        return self.queues.get()
