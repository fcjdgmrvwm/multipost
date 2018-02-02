import mp_config
import mp_scan
import mp_socket
import mp_analysis


class MultiPost(object):

    def __init__(self):
        self.task_queue = mp_config.TaskQueue()
        self.hosts = mp_config.HOSTS

    def start(self):
        self.start_all_threads()
        self.main_loop()

    def main_loop(self):
        try:
            while True:
                pass
        except:
            pass

    def start_all_threads(self):
        scan_thread = mp_scan.ScanThread(self.task_queue, self.hosts)
        analysis_thread = mp_analysis.AnalysisThread(self.task_queue)

        scan_thread.start()
        analysis_thread.start()


def main():
    app = MultiPost()
    app.start()


if __name__ == "__main__":
    main()
