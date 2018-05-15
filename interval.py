from threading import Timer

class Interval:
    def __init__(self, interval, callback):
        self.interval = interval
        self.callback = callback
        self.start()

    def start(self):
        Timer(self.interval, self.run).start()

    def run(self):
        self.callback()
        self.start()
