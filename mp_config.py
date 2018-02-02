import queue

SERVER_HOSTS = {'VmwareUbuntu': 'http://192.168.0.133/',
                'VmwareWin7': 'http://192.168.0.133/', }

CONTROLLER_HOST = '127.0.0.1'
CONTROLLER_PORT = 12345



class TaskQueue:
    def __init__(self):
        self.queues = queue.Queue()

    def push(self, task):
        self.queues.put(task)

    def pop(self):
        return self.queues.get()
