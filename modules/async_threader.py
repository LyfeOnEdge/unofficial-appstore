#LyfeOnEdge 2019
#GPL3
import threading

class asyncThread(threading.Thread):
    def __init__(self, func, arglist):
        threading.Thread.__init__(self, target=func, args=arglist)
        self.handled = False

    def begin(self):
        self.start()

#super basic thread manager
#Only start threads you have no intention of retrieving data from with this
class asyncThreader():
    def __init__(self, max_threads = 20):
        self.high_priority_threads = []
        self.medium_priority_threads = []
        self.low_priority_threads = []
        self.unique_thread = {}
        self.running_threads = []
        self.max_threads = max_threads
        self.update_running_threads()

        self.priority_map = {
                            "high" : self.high_priority_threads,
                            "med" : self.medium_priority_threads,
                            "medium" : self.medium_priority_threads,
                            "low" : self.low_priority_threads
                            }

    def do_async(self, func, arglist = [], priority = "low"):
        t = asyncThread(func, arglist)
        #If there is room for another thread do it now, else prioritize it
        if len(self.running_threads) < self.max_threads:
            t.begin()
            self.running_threads.append(t)
        else:
            self.priority_map[priority].append(t)

    def join(self):
        if self.running_threads:
            for t in self.running_threads:
                t.join()
            self.running_threads = []

    def clear_dead_threads(self):
        if self.running_threads:
            for t in self.running_threads:
                if not t.isAlive():
                    t.handled = True
            self.running_threads = [t for t in self.running_threads if not t.handled]

    #Not to be called by user
    def update_running_threads(self):
        self.clear_dead_threads()
        #Do high, then medium, then low-priority tasks, only do the next if the previous que was empty or finished
        if self.start_threads_and_move_to_running(self.high_priority_threads):
            if self.start_threads_and_move_to_running(self.medium_priority_threads):
                self.start_threads_and_move_to_running(self.low_priority_threads)

        #Schedule Self
        threading.Timer(0.05, self.update_running_threads).start()

    #Returns true if there are no remaining threads in the passed list, else we are maxed out
    def start_threads_and_move_to_running(self, threads):
        if threads:
            while len(self.running_threads) < self.max_threads:
                if threads:
                    t = threads.pop(0)
                    t.begin()
                    self.running_threads.append(t)
                else:
                    return True
        else:
            return True