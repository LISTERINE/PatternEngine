#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM
from Queue import Queue
from json import dumps


class DataPipe(object):
    # Store all pipes here.
    # Pipes are created at the bottom of this file.
    Pipes = {}

    def __init__(self, func=None, types=["accel","finger"], allow=True):
        """ Send glove data to other channels.
        If func is supplied the data will be passed to the
        function even if you do not set up a pipe.
        If allow is set to false the data pipe will not send data until
        allow is set to True.
        """
        if func is None:
            func = lambda x:x
        self.func = func
        self.send = lambda x:x
        self.types = types
        self.pipe_obj = None
        self.allow = allow

    def bind(self, name):
        """ Call this function to put the pipe in the main pipe
        dictionary.
        """
        DataPipe.Pipes[name] = self

    def build_pipe(self *args, **kwargs):
        """ override function to setup the pipes push function
        If the pipe is going to use a socket, use the from_socket
        method.
        If using a queue, use from_queue.
        from_socket and from_pipe are just convenience methods so
        you don't always need to use build_pipe.
        To build a pipe just set the function self.send to whatever
        method receives data. Then set self.pipe_obj to the instance
        whos receive metho you're calling. Look at from_socket for
        an example.
        """
        pass

    def from_socket(self, address, port):
        try:
            self.address = address
            self.port = port
            self.host = (address,port)
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(self.host)
            self.send = self.sock.send
            self.pipe_obj = self.sock
        except Exception:
            pass

    def from_queue(self, queue_size=100, queue=None):
        """ Use self.pipe_obj to obtain a queue endpoint
        """
        if queue is not None:
            self.queue = Queue(queue_size)
        self.send = self.queue.put
        self.pipe_obj = self.queue

    def push(self, data):
        try:
            if data["type"] in self.types and self.allow:
                data = self.func(data)
                self.send(dumps(data))
        except:
            pass


#######################################
##
## Build pipes here
##
#######################################

# Make a pipe that connects to pipe_test.py
test_pipe = DataPipe()
test_pipe.from_socket("192.168.1.3", 9000)
test_pipe.bind("test pipe")

