import threading

class asyncThread(threading.Thread):
    def __init__(self, func, arglist):
        threading.Thread.__init__(self, target=func, args=arglist)
        self.start()

#super basic thread manager
class asyncThreader():
    def __init__(self):
        self.threads = []

    def do_async(self, func, arglist = []):
        thread = asyncThread(func, arglist)
        self.threads.append(thread)

    def join(self):
        for thread in self.threads:
            thread.join()
        self.threads = []