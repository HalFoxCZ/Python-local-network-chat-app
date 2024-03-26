import threading as th

class ThreadPool:

    threads = []
    thread_count = 0

    def __init__(self, thread_count):
        self.thread_count = thread_count
        self.threads = [th.Thread() for _ in range(thread_count)]

    def add_task(self, *args, task):
        for thread in self.threads:
            if not thread.is_alive():
                thread = th.Thread(target=task, args=args)
                thread.start()
                break
        else:
            print("All threads are busy. Please wait.")

    def wait_completion(self):
        for i in range(self.thread_count):
            try:
                self.threads[i].join()
            except RuntimeError:
                pass
            # self.threads[i].join()

