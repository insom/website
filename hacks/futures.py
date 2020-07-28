from threading import *
import time

class Future(Thread):
    def __init__(self, func):
        self.func = func
        Thread.__init__(self)
        self.setDaemon(True)
        # so that we don't hang the interpreter,
        # generating results we don't use.
        self.start()
    def run(self):
        try:
            self.value = self.func()
        except Exception, e:
            self.exception = e
    def has_value(self):
        return not self.isAlive()
    def get_value(self):
        self.join()
        if hasattr(self, 'value'):
            return self.value
        else:
            raise self.exception
    def __call__(self):
        return self.get_value()

if __name__ == '__main__':
    def sleep_then_return(value):
        time.sleep(value)
        return 10

    delta = time.time()
    print "Start time:", int(time.time() - delta)
    f = Future(lambda: sleep_then_return(10))
    print "Do something time consuming ...",
    time.sleep(5)
    print "done! Lap time:", int(time.time() - delta)
    print "Value:", f(), "Finish time:", int(time.time() - delta)
