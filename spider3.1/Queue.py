import queue
import threading
import time

MAX_PUEUE = 2 # 默认20

class ThreadPool(object):  #创建线程池类
    def __init__(self, max_num=20):  #创建一个最大长度为20的队列
        self.queue = queue.Queue(max_num)  #创建一个队列
        for i in range(max_num):  #循环把线程对象加入到队列中
            self.queue.put(threading.Thread)  #把线程的类名放进去，执行完这个Queue

    def get_thread(self):  #定义方法从队列里获取线程
        return self.queue.get()  #在队列中获取值

    def add_thread(self):  #线程执行完任务后，在队列里添加线程
        self.queue.put(threading.Thread)


pool = ThreadPool(MAX_PUEUE)



