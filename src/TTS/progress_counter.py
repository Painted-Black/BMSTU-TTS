import threading


class Progress:
    def __init__(self):
        self.cur_progress = 0
        self.lock = threading.RLock()
        self.__tick = 0
        self.total_items = 0
        self.__done = False
        self.__running = False
        self.message = ""

    def get_tick(self):
        return self.__tick

    def done(self):
        self.lock.acquire()
        self.__done = True
        self.__running = False
        self.lock.release()

    def is_running(self):
        return self.__running

    def run(self):
        self.lock.acquire()
        self.__done = False
        self.__running = True
        self.cur_progress = 0
        self.lock.release()

    def is_done(self):
        return self.__done

    def set_total_items(self, total_items):
        self.total_items = total_items
        if self.total_items != 0:
            self.__tick = 100 / self.total_items

    def tick(self):
        self.lock.acquire()
        if self.cur_progress < 100:
            self.cur_progress += self.__tick
            if abs(100 - self.cur_progress) < self.__tick:
                self.cur_progress = 100
        self.lock.release()

    def set_progress(self, progress):
        self.lock.acquire()
        self.cur_progress = progress
        self.lock.release()

    def get_progress(self):
        return self.cur_progress
