import threading, queue, time
TICKRATE = 100

class asyncThreader():
    def __init__(self):
        self.queue = queue.Queue()
        self.finished_queue = {}
        self.threads = []

    def async_download(self,url,filename):
        thread = downloadThread(self.queue, url, filename)
        thread.start()
        self.threads.append(thread)
        self.periodiccall()
        reference = url
        return url

    def install_package(self, repo, appstore_handler_object, progress_function, reload_function):
        installThread(self.queue, repo, appstore_handler_object, progress_function, reload_function)

    def periodiccall(self):
        self.checkqueue()

        schedule_call = False
        for thread in self.threads:
            if thread.is_alive():
                schedule_call = True
                
        if schedule_call:
            self.after(100, self.periodiccall)

    def checkqueue(self):
        if self.queue.qsize():
            while self.queue.qsize():
                try:
                    msg = self.queue.get(0)
                    self.finished_queue.update(msg)
                except Queue.Empty:
                    pass

            return True

    def get_finished(self, reference):
        try:
            return self.finished_queue.pop(reference)
        except:
            pass



# #Async download thread, returns reference to msg in que
# class downloadThread(asyncThread):
#     def __init__(self, queue, remote_name, local_name):
#         asyncThread.__init__(self, queue)
#         self.remote_name = remote_name
#         self.local_name = local_name

#     def run(self):
#         self.download()

#     def download(self):
#         print("Test download")
#         time.sleep(10)
#         msg = {remote_name : True}
#         print("Test download complete...")
#         self.queue.put(msg)

class installThread():
    def __init__(self, queue, repo, appstore_handler_object, progress_function, reload_function):
        self.queue = queue
        self.repo = repo
        thread = threading.Thread(target=appstore_handler_object.install_package, args=(self.repo, progress_function, reload_function))
        thread.start()