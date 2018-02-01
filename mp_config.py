import queue

HOSTS = {'VmwareUbuntu': 'http://192.168.0.133/',
         'VmwareWin7': 'http://192.168.0.133/', }




class TaskQueue:
    def __init__(self):
        self.queues = queue.Queue()

    def push(self, task):
        self.queues.put(task)

    def pop(self):
        return self.queues.get()
