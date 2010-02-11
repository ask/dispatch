"""Simple sample showing basic usage pattern"""
import time

from dispatch import Signal

request_started = Signal(providing_args=["remote_addr"])
request_ended = Signal(providing_args=["time_start", "time_end"])


class Request(object):

    def __init__(self, remote_addr):
        self.remote_addr = remote_addr
        self.time_start = time.time()

    def enter(self):
        request_started.send(sender=self, remote_addr=self.remote_addr)

    def leave(self):
        time_end = time.time()
        request_ended.send(sender=self, time_start=self.time_start,
                                        time_end=time_end)


def mycallback(signal, sender, **kwargs):
    print("Received signal: %s" % repr(kwargs))


if __name__ == "__main__":

    request_started.connect(mycallback)
    request_ended.connect(mycallback)

    request = Request("localhost")
    request.enter()
    request.leave()

