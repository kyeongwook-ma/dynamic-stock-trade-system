import threading
import Queue
from html_parser import *

class TaskController(object):
    
    __metaclass__ = Singleton
    
    def __init__(self):
        super(TaskController, self).__init__()
        self.queue = Queue.Queue()
        self.queue_lock = threading.Lock()
        self.result_list = []

    def enqueue_task(self, task):
        self.queue_lock.acquire()
        task.start()
        self.queue.put(task)
        self.queue_lock.release()

    def deque_task(self):

        while not self.queue.empty():
            self.queue_lock.acquire()
            t = self.queue.get()
            t.join()
            self.result_list.append(t.get_result())
            self.queue_lock.release()
        return self.result_list

    def is_task_done(self):
        return self.queue.task_done()


class Task(threading.Thread):

    def __init__(self, job, arg = None):
        super (Task, self).__init__()
        threading.Thread.__init__(self)
        self.execute = job
        self.arg = arg
        self.result = ""

    def run(self):
        self.result = self.execute( self.arg )

    def get_result(self):
        return self.result

